#!/usr/bin/env python3

import shutil
import agent
import argparse
from handler import Handler
from importlib import resources
import os
import glob
import datetime

DEFAULT_MODEL = 'gpt-4o'

def batch(args):
    print("Batch command invoked for directory:", args.directory_path)
    directory_path = os.path.abspath(args.directory_path)

    if not os.path.exists(directory_path):
        print(f"Specified directory does not exist: {directory_path}")
        return

    yaml_files = [f for f in os.listdir(directory_path) if f.endswith('.yaml') or f.endswith('_spec.yaml')]

    if not yaml_files:
        print("No .spec.yaml files found in the specified directory.")
        return

    spath = resources.files('resources')
    my_handler = Handler()
    my_handler.set_comp_iter(args.comp_limit)
    my_handler.create_agents(spath=str(spath), llms=args.llm, lang=args.lang, use_spec=True, temperature=None, w_dir=directory_path, init_context=args.init_context, supp_context=args.supp_context, short_context=args.short_context)

    for yaml_file in yaml_files:
        spec_file_path = os.path.join(directory_path, yaml_file)
        print(f"Processing {spec_file_path}...")
        my_handler.spec_run(target_spec=spec_file_path, iterations=args.comp_limit)


def start(args):
    if args.help:
        print("\n\nStart a new structured spec file out of a plain problem explanation")
        return

    if len(args.file_list)==0:
        print("ERROR: start needs a file list of plain text")
        exit(4)

    spath      = resources.files('resources')
    my_handler = Handler()
    my_handler.set_comp_iter(args.comp_limit)

    for f in args.file_list:
        if args.help:
            print(f"creating spec from {f}")
        else:
            my_handler.sequential_entrypoint(spath=str(spath), llms=args.llm, lang=args.lang, update=args.update, w_dir=args.w_dir, gen_spec=f, init_context=args.init_context, supp_context=args.supp_context, short_context=args.short_context)

def bench(args):
    if args.help:
        print("\n\nPerformance against benchmarks")
        return

    if args.skip_completed and args.update:
        print("ERROR: Benchmarks can not invoke --skip_completed and --update at the same time")
        exit()

    print("This example will show how you can run a yaml file: `poetry run hdlagent/cli_agent.py bench sample/RCA_spec.yaml`\n")

    spath      = resources.files('resources')
    my_handler = Handler()
    my_handler.set_comp_iter(args.comp_limit)
    my_handler.create_agents(spath=str(spath), llms=args.llm, lang=args.lang, use_spec=True, temperature= None, w_dir=args.w_dir, init_context=args.init_context, supp_context=args.supp_context, short_context=args.short_context)
    for f in args.bench_list:
        print(f"BENCHMARKING file... {f}")
        my_handler.spec_run(target_spec=f, iterations=args.comp_limit)

    if len(args.bench_list) == 0: # Check current directory to build
        files = os.listdir(args.w_dir)
        args.bench_list = [file for file in files if file.endswith("spec.yaml")]

def log(args):
    base_output_dir = os.path.expanduser('~/hdlagent/hdlagent/out')

    if args.list_runs:
        benchmark_dirs = glob.glob(os.path.join(base_output_dir, '*'))

        print("Available Runs:\n")
        for idx, bench_dir in enumerate(benchmark_dirs, start=1):
            last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(bench_dir)).strftime('%Y-%m-%d %H:%M:%S')
            bench_name = os.path.basename(bench_dir)
            print(f"{idx}. {bench_name} - Run on {last_modified}")
        return

    elif args.benchmark_name:
        benchmark_name = args.benchmark_name
        logs_dir = os.path.join(base_output_dir, benchmark_name, 'logs')

        if not os.path.exists(logs_dir):
            print(f"No logs directory found for benchmark '{benchmark_name}'.")
            return

        compile_log_pattern = os.path.join(logs_dir, '*_compile_log.md')
        compile_logs = glob.glob(compile_log_pattern)

        if not compile_logs:
            print(f"No compile log found for benchmark '{benchmark_name}'.")
            return

        # Assuming there's only one compile log per benchmark
        compile_log_file = compile_logs[0]

        with open(compile_log_file, 'r') as file:
            lines = file.readlines()

        results_line = None
        for line in reversed(lines):
            if line.startswith('RESULTS :'):
                results_line = line.strip()
                break

        if not results_line:
            print(f"No RESULTS line found in the compile log for benchmark '{benchmark_name}'.")
            return

        parts = results_line.split(' : ')
        if len(parts) != 12:
            print(f"Invalid RESULTS line format in the compile log for benchmark '{benchmark_name}'.")
            return

        _, model, name, comp_n, comp_f, lec_n, lec_f, top_k, prompt_tokens, completion_tokens, world_clock_time, llm_query_time = parts

        status = "Success" if int(comp_f) == 0 and int(lec_f) == 0 else "Failure"

        run_date = datetime.datetime.fromtimestamp(os.path.getmtime(compile_log_file)).strftime('%Y-%m-%d %H:%M:%S')

        print(f"Benchmark: {benchmark_name}")
        print(f"Run Date: {run_date}")
        print(f"Model: {model}")
        print(f"Status: {status}\n")
        print("Performance Metrics:")
        print(f"- Compilation Attempts: {comp_n}")
        print(f"- Compilation Failures: {comp_f}")
        print(f"- LEC Attempts: {lec_n}")
        print(f"- LEC Failures: {lec_f}")
        total_tokens = int(prompt_tokens) + int(completion_tokens)
        print(f"- Total Tokens Used: {total_tokens} (Prompt: {prompt_tokens}, Completion: {completion_tokens})")
        print(f"- Total Time: {world_clock_time} seconds (LLM Query Time: {llm_query_time} seconds)")
        print(f"- Top_k: {top_k}\n")
        print("Output Files:")
        generated_code = os.path.join(base_output_dir, benchmark_name, f"{name}.v")
        compile_log = compile_log_file
        spec_log = os.path.join(logs_dir, f"{name}_spec_log.md")

        print(f"- Generated Code: {generated_code}")
        print(f"- Compile Log: {compile_log}")
        print(f"- Spec Log: {spec_log}")

        return

    else:
        logs_dir_pattern = os.path.join(base_output_dir, '*', 'logs')
        log_directories = glob.glob(logs_dir_pattern)

        if not log_directories:
            print(f"No logs directory found matching pattern {logs_dir_pattern}.")
            return

        results_entries = []
        results_lines = []

        for logs_dir in log_directories:
            compile_log_pattern = os.path.join(logs_dir, '*_compile_log.md')
            compile_logs = glob.glob(compile_log_pattern)

            for log_file in compile_logs:
                with open(log_file, 'r') as file:
                    lines = file.readlines()
                    results_line = None
                    for line in reversed(lines):
                        if line.startswith('RESULTS :'):
                            results_line = line.strip()
                            results_lines.append(results_line + '\n')
                            break

                if results_line:
                    parts = results_line.split(' : ')
                    if len(parts) != 12:
                        continue

                    _, model, name, comp_n, comp_f, lec_n, lec_f, top_k, prompt_tokens, completion_tokens, world_clock_time, llm_query_time = parts

                    run_date = datetime.datetime.fromtimestamp(os.path.getmtime(log_file))

                    status = 'success' if int(comp_f) == 0 and int(lec_f) == 0 else 'failed'

                    entry = {
                        'benchmark_name': name,
                        'model': model,
                        'comp_n': int(comp_n),
                        'comp_f': int(comp_f),
                        'lec_n': int(lec_n),
                        'lec_f': int(lec_f),
                        'top_k': int(top_k),
                        'prompt_tokens': int(prompt_tokens),
                        'completion_tokens': int(completion_tokens),
                        'world_clock_time': float(world_clock_time),
                        'llm_query_time': float(llm_query_time),
                        'run_date': run_date,
                        'log_file': log_file,
                        'status': status,
                        'results_line': results_line,
                    }

                    results_entries.append(entry)

        if not results_entries:
            print("No RESULTS entries found in the compile logs.")
            return

        filters_specified = (args.status != 'all' or args.date_from or args.date_to or args.top_k is not None)

        if filters_specified:
            filtered_entries = []

            for entry in results_entries:
                if args.status != 'all' and entry['status'] != args.status:
                    continue

                if args.date_from:
                    try:
                        date_from = datetime.datetime.strptime(args.date_from, '%Y-%m-%d')
                    except ValueError:
                        print("Invalid date format for --date-from. Use YYYY-MM-DD.")
                        return
                    if entry['run_date'] < date_from:
                        continue
                if args.date_to:
                    try:
                        date_to = datetime.datetime.strptime(args.date_to, '%Y-%m-%d') + datetime.timedelta(days=1)
                    except ValueError:
                        print("Invalid date format for --date-to. Use YYYY-MM-DD.")
                        return
                    if entry['run_date'] >= date_to:
                        continue

                if args.top_k is not None:
                    if entry['top_k'] < args.top_k:
                        continue

                filtered_entries.append(entry)

            if not filtered_entries:
                print("No entries match the specified filters.")
                return

            filtered_entries.sort(key=lambda x: x['run_date'])

            if args.status != 'all':
                print(f"{args.status.capitalize()} Runs", end='')
                if args.date_from or args.date_to:
                    print(" between", end=' ')
                    if args.date_from:
                        print(f"{args.date_from}", end=' ')
                    if args.date_to:
                        print(f"and {args.date_to}", end=' ')
                print(":\n")
            else:
                print("Filtered Runs:\n")

            for idx, entry in enumerate(filtered_entries, start=1):
                run_date_str = entry['run_date'].strftime('%Y-%m-%d %H:%M:%S')
                print(f"{idx}. {entry['benchmark_name']} - Run on {run_date_str}")

            if args.output_file:
                with open(args.output_file, 'w') as file:
                    for entry in filtered_entries:
                        file.write(entry['results_line'] + '\n')
                print(f"\nFiltered results have been saved to {args.output_file}")

        else:
            if not results_lines:
                print("No RESULTS lines found in the compile logs.")
                return

            output_file = args.output_file if args.output_file else 'all_results.txt'
            with open(output_file, 'w') as file:
                file.writelines(results_lines)

            print(f"Collected RESULTS lines have been saved to {output_file}")

def build(args):
    if args.help:
        print("\n\nBuild the HDL out of the spec file[s] or spec files in directory")
        return

    spath      = resources.files('resources')
    my_handler = Handler()
    my_handler.set_comp_iter(args.comp_limit)
    my_handler.create_agents(spath=str(spath), llms=args.llm, lang=args.lang, use_spec=True, temperature= None, w_dir=args.w_dir, init_context=args.init_context, supp_context=args.supp_context, short_context=args.short_context)

    if len(args.file_list) == 0: # Check current directory to build
        files = os.listdir(args.w_dir)
        args.file_list = [file for file in files if file.endswith("spec.yaml")]

    if args.help:
        print("\n\nOnce help is disabled, it will build the following spec files:")
        for f in args.file_list:
            print(f"spec:{f}")
    else:
        for f in args.file_list:
            my_handler.spec_run(target_spec=f, iterations=args.comp_limit)

def list_models(args):
    if args.help:
        return []

    all_models = []
    if not hasattr(args,'model'):
        args.model = []

    showall = len(args.model)==0
    if "openai" in args.model or showall:
        if "OPENAI_API_KEY" in os.environ:
            models = agent.list_openai_models()
            if len(models):
                all_models += models
                if not args.silent:
                    print("OpenAI models:")
                    for m in models:
                        if "gpt" in m:
                            print(" ", m)
                    print("\n")
        else:
            print("OpenAI unavailable unless OPENAI_API_KEY is set")

    if "octoai" in args.model or showall:
        if "OCTOAI_TOKEN" in os.environ:
            models = agent.list_octoai_models()
            if len(models):
                all_models += models
                if not args.silent:
                    print("OctoAI models:")
                    for m in models:
                        print(" ", m)
                    print("\n")
        else:
            print("OctoAI unavailable unless OCTOAI_TOKEN is set")

    if "vertex" in args.model or showall:
        models = agent.list_vertexai_models()
        if len(models):
            all_models += models
            if not args.silent:
                print("VertexAI models:")
                for m in models:
                    print(" ", m)
                print("\n")

    if "sambanova" in args.model or showall:
        if "SAMBANOVA_API_KEY" in os.environ:
                models = agent.list_sambanova_models()
                if len(models):
                    all_models += models
                    print("SambaNova models:")
                    for m in models:
                            print(" ", m)
                    print("\n")
        else:
            print("SambaNova unavailable unless SAMBANOVA_API_KEY is set")    

    return all_models

def add_shared_args(model):

    model.add_argument('--config',        type=str,   action="store",       help='Path to a configuration YAML file')
    model.add_argument('--llm',           type=str,   action="store",      default=[DEFAULT_MODEL], help='LLM model. Use list_models to see models')
    model.add_argument('--lang',          type=str,   action="store",       default="Verilog",                choices=['Verilog', 'Chisel', 'PyRTL', 'DSLX'], help='Language for code generation. It can only be "Verilog", "Chisel", "PyRTL", or "DSLX"')
    model.add_argument('--parallel',      action="store_false", help='Parallelize hdlagent runs')

    model.add_argument('--w_dir',         type=str,   action="store",       default="./",         help='Working dir to generate resource and log files')
    model.add_argument('--comp_limit',    type=int,   action="store",       default=4,            help='The amount of LLM attempts, max iterations = (top_k * lec_limit * comp_limit)')

    model.add_argument('--init_context',  action="append",      default=[], help='Use per language specialized initial context')
    model.add_argument('--supp_context',  action="store_false", help='Use per each compile error a supplemental context')
    model.add_argument('--short_context', action="store_false", help='Exclude previous code responses and queries from context window')

    model.add_argument('--update',        action="store_false", default=False, help='Retry LEC iterations on current RTL code generated')

def check_tools(args):
    if shutil.which('yosys') is None:
        print("Yosys is needed for benchmarking and testing")
        exit(3)

    if (shutil.which('slang') is None) and (shutil.which('iverilog') is None):
        print("To improve Verilog generation iteration install sland and/or iverilog")
        exit(3)

def check_args(args):
    if not hasattr(args,'file_list'):
        args.file_list = []

    for f in args.file_list:
        if not os.path.exists(f):
            print(f"ERROR, file {f} does not exist")
            exit(3)

    qargs = args
    qargs.silent = True
    l = list_models(qargs)
    qargs.silent = False

    if len(l) == 0:
        print("ERROR: no model available. Try setting OPENAI/Gemini/OCTOAI tokens")
        exit(5)

    if isinstance(args.llm, str):
        args.llm = [args.llm]

    if (args.llm and l) == None:
        print(f"ERROR: model {args.llm} is not in list-models available")
        exit(3)

def add_start_command(subparsers):
    parser = subparsers.add_parser("start", help="Start a spec from a simple explanation", add_help=False)
    add_shared_args(parser)
    parser.add_argument("file_list", nargs="*", help="Explicit list of text files to start spec.yaml specs")

    return parser

def add_bench_command(subparsers):
    parser = subparsers.add_parser("bench", help="Benchmark the existing hdlagent setup", add_help=False)
    add_shared_args(parser)
    parser.add_argument('--skip_completed',        action="store_false", help='Skip generated already generated tests')
    parser.add_argument("bench_list", nargs="*", help="List of files to clean")

    return parser

def add_build_command(subparsers):
    parser = subparsers.add_parser("build", help="Build the code (HDL+test) from the spec file", add_help=False)
    add_shared_args(parser)
    parser.add_argument("file_list", nargs="*", help="Explicit list of spec files, or find *spec.yaml in w_dir")

    return parser

def add_list_models_command(subparsers):
    parser = subparsers.add_parser("list-models", help="List the existing models available", add_help=False)
    add_shared_args(parser)
    parser.add_argument("model", nargs="*", help="platform (openai, octoai, vertex)")

    return parser

def add_log_command(subparsers):
    parser = subparsers.add_parser('log', help="Collect and save RESULTS lines from previous runs.", add_help=False)
    add_shared_args(parser)
    parser.add_argument('--output-file', help="The output file to save collected RESULTS lines.")
    parser.add_argument('--list-runs', action='store_true', help="List all available runs and their timestamps.")
    parser.add_argument('benchmark_name', nargs='?', help="Name of the benchmark to log details for", default=None)

    parser.add_argument('--status', choices=['all', 'success', 'failed'], default='all', help='Filter logs by run status.')
    parser.add_argument('--date-from', type=str, help='Show logs from this date (YYYY-MM-DD).')
    parser.add_argument('--date-to', type=str, help='Show logs up to this date (YYYY-MM-DD).')
    parser.add_argument('--top_k', type=int, help='Filter logs where top_k is greater than or equal to the specified value.')

    return parser

def add_batch_command(subparsers):
    parser = subparsers.add_parser("batch", help="Perform batch operations on all .spec.yaml files within a directory", add_help=False)
    add_shared_args(parser)
    parser.add_argument('directory_path', type=str, help="Directory containing .spec.yaml files to process")

    return parser

def cli_agent():

    parser     = argparse.ArgumentParser(description = "hdlagent: A Hardware Description Language Agent",
                                         epilog="""
Examples:
  hdlagent start description.txt
  hdlagent bench sample/RCA_spec.yaml
  hdlagent build
  hdlagent batch sample/
  hdlagent list-models
  hdlagent log [--list-runs: List all available runs and their timestamps.| benchmark_name: log details| --status, --date-from, --date-to, --top_k: Filter logs|--output-file: to save collected RESULTS lines]
""",
    formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False)
    subparsers = parser.add_subparsers(dest          = "command")

    parser_bench       = add_bench_command(subparsers)
    parser_build       = add_build_command(subparsers)
    parser_list_models = add_list_models_command(subparsers)
    parser_start       = add_start_command(subparsers)
    parser_log         = add_log_command(subparsers)
    parser_batch = add_batch_command(subparsers)  # Add the batch parser

    args, unknown = parser.parse_known_args()

    if '-h' in unknown or '--help' in unknown:
        args.help = True
    else:
        args.help = False

    args.silent = False
    check_tools(args)

    if args.command == "start":
        if args.help:
            parser_start.print_help()
        else:
            check_args(args)
        start(args)
    elif args.command == "bench":
        if args.help:
            parser_bench.print_help()
        else:
            check_args(args)
        bench(args)
    elif args.command == "build":
        if args.help:
            parser_build.print_help()
        else:
            check_args(args)
        build(args)
    elif args.command == "list-models":
        if args.help:
            parser_list_models.print_help()
        list_models(args)
    elif args.command == "log":
        if args.help:
            parser_list_models.print_help()
        log(args)
    elif args.command == "batch":
        if args.help:
            parser_batch.print_help()
        else:
            batch(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    cli_agent()
