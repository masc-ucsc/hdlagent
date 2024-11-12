import subprocess
import os
import sys
import re

# Define mappings
llm_mapping = {
    "gpt-4-1106-preview": "GPT-4",
    "gpt-3.5-turbo-0125": "GPT-3.5n",
    "gpt-3.5-turbo-1106": "GPT-3.5o",
    "gemini-1.0-pro-002": "GPro-1.0",
    "gemini-1.5-flash-002": "Gpro_1.5",
    "llama3-405b": "llama"
}

benchmark_mapping = {
    "HDLEval-comb": "HC",
    "HDLEval-pipe": "HP",
    "VerilogEval2-comb": "VE2-C",
    "VerilogEval2-pipe": "VE2-P"
}

# Labels in the specific order required
# labels_order = ['Fixes', 'Compile', 'Few-shot', 'Description', 'Base']
commands_order = ['simple', 'init_desc', 'few_shot', 'init', 'supp']

# Mapping commands to their specific parameters
command_details = {
    'simple': {
        'subdir': 'simple',
        'extra_args': ''
    },
    'init_desc': {
        'subdir': 'init',
        'extra_args': '--desc'
    },
    'few_shot': {
        'subdir': 'few_shot',
        'extra_args': ''
    },
    'init': {
        'subdir': 'init',
        'extra_args': ''
    },
    'supp': {
        'subdir': 'supp',
        'extra_args': ''
    }
}

llms = [
    "gpt-4-1106-preview", 
    "gpt-3.5-turbo-0125", 
    "gpt-3.5-turbo-1106",
    "gemini-1.0-pro-002", 
    "gemini-1.5-flash-002", 
    "llama3-405b"
]
languages = ["Verilog", "Chisel", "PyRTL", "DSLX"]
benchmarks = ["HDLEval-comb", "HDLEval-pipe", "VerilogEval2-comb", "VerilogEval2-pipe"]


data = {
    lang: {
        llm_name: {category: [0] * len(commands_order) for category in benchmark_mapping.values()}
        for llm_name in llm_mapping.values()
    }
    for lang in languages
}

def run_command(command):
    try:
        result = subprocess.run(
            command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        output = result.stdout.strip()

        # Try parsing the output
        # First, attempt to find a number inside parentheses (e.g., "(53/84)")
        match = re.search(r'\((\d+)/\d+\)', output)
        if match:
            value = int(match.group(1))
            print(f"Parsed value from output: {value}")
            return value, output
        else:
            # Next, try extracting a percentage (e.g., "63.10%")
            match = re.search(r'(\d+(\.\d+)?)%', output)
            if match:
                value = int(float(match.group(1)))
                print(f"Parsed percentage value from output: {value}")
                return value, output
            else:
                # Finally, try parsing the output as an integer directly
                try:
                    value = int(output)
                    print(f"Parsed integer value from output: {value}")
                    return value, output
                except ValueError:
                    print(f"Unable to parse output for command: {command}", file=sys.stderr)
                    print(f"Output: {output}", file=sys.stderr)
                    return 0, output  # Return a tuple
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {command}", file=sys.stderr)
        print(f"Error: {e.stderr.strip()}", file=sys.stderr)
        return 0, e.stderr.strip()  # Return a tuple
    except Exception as ex:
        print(f"An unexpected error occurred: {command}", file=sys.stderr)
        print(f"Error: {str(ex)}", file=sys.stderr)
        return 0, ""  # Return a tuple


def generate_and_execute_commands():
    for llm_id in llms:
        llm_name = llm_mapping.get(llm_id)
        if not llm_name:
            print(f"LLM ID '{llm_id}' not found in mapping. Skipping.", file=sys.stderr)
            continue

        for benchmark in benchmarks:
            category = benchmark_mapping.get(benchmark)
            if not category:
                print(f"Benchmark '{benchmark}' not found in mapping. Skipping.", file=sys.stderr)
                continue

            for lang in languages:
                previous_max_value = 0
                for cmd_index, cmd in enumerate(commands_order):
                    details = command_details.get(cmd)
                    if not details:
                        print(f"Command '{cmd}' not defined in command_details. Skipping.", file=sys.stderr)
                        continue

                    subdir = details['subdir']
                    extra_args = details['extra_args']

                    # Construct the working directory path
                    w_dir = f"../DAC_results/{llm_id}/{benchmark}/{lang}/{subdir}/"

                    # Check if the working directory exists
                    if not os.path.exists(w_dir):
                        print(f"Working directory '{w_dir}' does not exist. Skipping.", file=sys.stderr)
                        continue

                    # Construct the base command
                    command = f"poetry run hdlagent/cli_agent.py log --w_dir {w_dir}"

                    # Append extra arguments if any
                    if extra_args:
                        command += f" {extra_args}"

                    # Print the command being executed
                    print(f"Executing command: {command}")

                    # Run the command and get the output
                    current_value, output = run_command(command)
                    print(f"Command output: {output}\n")

                    
                    # Compute delta
                    delta = current_value - previous_max_value
                    if delta > 0:
                        data[lang][llm_name][category][cmd_index] = delta
                        previous_max_value = current_value  # Update previous max value
                    else:
                        data[lang][llm_name][category][cmd_index] = 0  # No increase, report 0
                    print(f"Updated data[{lang}][{llm_name}][{category}][{cmd_index}] = {data[lang][llm_name][category][cmd_index]}")

    # Save the data per language
    for lang in languages:
        formatted_data = {}
        for llm_name, categories in data[lang].items():
            formatted_data[llm_name] = []
            for category_label in ['HC', 'HP', 'VE2-C', 'VE2-P']:
                if category_label in categories:
                    formatted_data[llm_name].append(categories[category_label])
                else:
                    formatted_data[llm_name].append([0] * len(commands_order))

        # Save the data to a Python file for each language
        with open(f'data_{lang}.py', 'w') as f:
            f.write("# Data extracted for plotting\n")
            f.write("# Each LLM maps to a list of benchmarks in the following order:\n")
            f.write("# ['HC', 'HP', 'VE2-C', 'VE2-P']\n")
            f.write("# Each benchmark contains a list of values corresponding to commands in the following order:\n")
            f.write("# ['simple', 'init_desc', 'few_shot', 'init', 'supp']\n")
            f.write("data = {\n")
            for llm, category_data in formatted_data.items():
                f.write(f"    '{llm}': [  # Data for {llm}\n")
                for idx, category_list in enumerate(category_data):
                    benchmark_label = ['HC', 'HP', 'VE2-C', 'VE2-P'][idx]
                    f.write(f"        # {benchmark_label}\n")
                    f.write(f"        {category_list},\n")
                f.write("    ],\n")
            f.write("}\n")
        print(f"Data extraction complete. Data saved to 'data_{lang}.py'.")

# Execute the command generation and data extraction
if __name__ == "__main__":
    generate_and_execute_commands()