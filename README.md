
AI Coding Agent for specification to hardware code.

The HDL Agent uses self-reflection, context, and grounding with EDA tools to generate hardware description language (HDL) code from specifications.


## Installation instructions
### **Prerequisites**

- **Python 3.8** or higher
- **[Poetry](https://python-poetry.org/docs/#installation)** for managing dependencies
- **Yosys**: Required for benchmarking and testing

Install with python poetry:
```
poetry install
```

If updating hdlagent, you may need to update poetry dependencies too:
```
poetry lock
poetry install
```

Set the required keys (depends on the model that you use)
```
export OPENAI_API_KEY=.....
export SAMBANOVA_API_KEY=....
```
## Usage
The `hdlagent` script provides several commands to help you generate HDL code from specifications, run benchmarks, build code, and more.

### General Help
To display general help with a list of all commands:
```
poetry run ../hdlagent/cli_agent.py --help
```
### **Available Commands**

Here are the available commands:
- **start** - Start a new spec from a simple explanation
- **bench** - Run benchmarks using YAML specification files
- **build** - Build the code from spec files
- **list-models** - List available models
- **log** - Collect and display logs from previous runs

### **`start` Command**
**Description**: Start a new structured spec file from a plain text problem description.
```
poetry run hdlagent/cli_agent.py start [options] <text_file1> [<text_file2> ...]
```
Example:
```
poetry run hdlagent/cli_agent.py start description.txt
```
Options:

- `--llm LLM_MODEL`: Specify the LLM model to use (default: `gpt-4o`)
- `--lang {Verilog,Chisel,PyRTL,DSLX}`: Language for code generation (default: `Verilog`)
- Additional options are available; run `hdlagent start --help` for more details.

### **`bench` Command**
**Description**: Run benchmarks using YAML specification files.

Usage:
```
poetry run hdlagent/cli_agent.py bench [options] <spec_file1.yaml> [<spec_file2.yaml> ...]
```
Example:
```
poetry run hdlagent/cli_agent.py bench sample/RCA_spec.yaml
```
Options:

- `--skip_completed`: Skip already generated tests
- `--llm LLM_MODEL`: Specify the LLM model to use
- Additional options are available; run `hdlagent bench --help` for more details.
### **`build` Command**
**Description**: Build the HDL code (and test benches) from spec files.

Usage:
```
poetry run hdlagent/cli_agent.py build [options] [spec_file1.yaml spec_file2.yaml ...]
```
If no spec files are specified, it will find all *spec.yaml files in the working directory.

Example:
```
poetry run hdlagent/cli_agent.py build
```
Options:

- `--llm LLM_MODEL`: Specify the LLM model to use
- Additional options are available; `run hdlagent build --help` for more details.
### **`list-models` Command**
**Description**: List the existing models available for use.

Usage:
```
poetry run hdlagent/cli_agent.py list-models [options]
```
Example:
```
poetry run hdlagent/cli_agent.py list-models
```
### **`log` Command**
**Description**: Collect and save RESULTS lines from previous runs, or display details of a specific run.

Usage:
```
poetry run hdlagent/cli_agent.py log [options] [benchmark_name]
```
Examples:

 - Collect all RESULTS lines:
   ```
   poetry run hdlagent/cli_agent.py log
   ```
 - List all available runs:
   ```
   poetry run hdlagent/cli_agent.py log --list-runs
   ```
 - Display details of a specific run:
   ```
   poetry run hdlagent/cli_agent.py log RCA_spec.yaml
   ```
 - Filter logs:
   ```
   poetry run hdlagent/cli_agent.py log --status=failed --date-from=2023-10-01 --date-to=2023-10-05
   ```

Options:

- `--output-file OUTPUT_FILE`: Specify the output file to save collected RESULTS lines.
- `--list-runs`: List all available runs and their timestamps.
- `--status {all,success,failed}`: Filter logs by run status (default: all).
- `--date-from YYYY-MM-DD`: Show logs from this date.
- `--date-to YYYY-MM-DD`: Show logs up to this date.
- `--top_k TOP_K_VALUE`: Filter logs where top_k is greater than or equal to the specified value.

### Run a Simple test from json

```
cd sample
poetry run ../hdlagent/hdlagent.py --supp_context  --llm gpt-4-turbo-preview --bench ./sample-test.json
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.

