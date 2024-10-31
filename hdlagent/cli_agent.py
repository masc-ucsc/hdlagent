#!/usr/bin/env python3

import shutil
import agent
import argparse
from handler import Handler
from importlib import resources
import os
import glob
import datetime
from hdeval import HDEvalInterface
import logging
import pdb
#from interface import HDEvalInterface

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
DEFAULT_MODEL = 'gpt-4o'
#DEFAULT_MODEL = 'llama3-405b'
#DEFAULT_MODEL = 'gpt-4-1106-preview'

def opt(args):
    if args.help:
        print("\n\nOptimize Verilog code using LLM")
        return

    spath = resources.files('resources')
    my_handler = Handler()
    my_handler.set_comp_iter(args.comp_limit)
    my_handler.set_lec_iter(args.lec_limit)
    my_handler.create_agents(
        spath=str(spath),
        llms=args.llm,
        lang=args.lang,
        use_spec=False,
        temperature=None,
        w_dir=args.w_dir,
        init_context=args.init_context,
        supp_context=args.supp_context,
        short_context=args.short_context
    )

    if len(args.verilog_files) == 0:
        # No files provided, look for Verilog files in the working directory
        files = os.listdir(args.w_dir)
        args.verilog_files = [os.path.join(args.w_dir, file) for file in files if file.endswith(".v")]

    for verilog_file in args.verilog_files:
        if not os.path.exists(verilog_file):
            print(f"Error: Verilog file '{verilog_file}' not found.")
            continue  # Skip to the next file

        print(f"Optimizing Verilog file: {verilog_file}")
        my_handler.opt_run(verilog_file, lec_iterations=args.lec_limit, comp_iterations=args.comp_limit)

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
    my_handler.set_lec_iter(args.lec_limit)

    for f in args.file_list:
        if args.help:
            print(f"creating spec from {f}")
        else:
            my_handler.sequential_entrypoint(spath=str(spath), llms=args.llm, lang=args.lang, skip_completed=args.skip_completed, update=args.update, w_dir=args.w_dir, gen_spec=f, init_context=args.init_context, supp_context=args.supp_context, short_context=args.short_context)

def bench(args):
    if args.help:
        print("\n\nPerformance against benchmarks")
        return

    if args.skip_completed and args.update:
        print("ERROR: Benchmarks can not invoke --skip_completed and --update at the same time")
        exit()

    print("This example will show how you can run a yaml file: `poetry run hdlagent/cli_agent.py bench sample/RCA_spec.yaml`\n")
    # pdb.set_trace()
    spath      = resources.files('resources')
    my_handler = Handler()
    my_handler.set_comp_iter(args.comp_limit)
    my_handler.set_lec_iter(args.lec_limit)
    my_handler.create_agents(spath=str(spath), llms=args.llm, lang=args.lang, use_spec=True, temperature= None, w_dir=args.w_dir, init_context=args.init_context, supp_context=args.supp_context, short_context=args.short_context)

    if len(args.bench_list) == 0: # Check current directory to build
        files = os.listdir(args.w_dir)
        args.bench_list = [file for file in files if file.endswith("spec.yaml")]
    for benchmark_spec in args.bench_list:
        print(f"BENCHMARKING... {benchmark_spec}")

        if benchmark_spec.startswith('hdeval:'):
            # Handle hdeval benchmarks
            benchmark_name = benchmark_spec.split(':', 1)[1]
            print(f"Processing hdeval benchmark: {benchmark_name}")

           # hdeval_interface = HDEvalInterface(hdeval_repo_path='/home/farzaneh/hdeval')
            hdeval_interface = HDEvalInterface()
            yaml_files  = hdeval_interface.hdeval_open(benchmark_name)

            if not yaml_files:
                print(f"No YAML files generated for benchmark '{benchmark_name}'.")
                continue

            for yaml_file in yaml_files:
                
                print(f"Processing YAML file: {yaml_file}")
                my_handler.spec_run(target_spec=yaml_file, lec_iterations=args.lec_limit,comp_iterations=args.comp_limit)
                for agent in my_handler.agents:
                    agent.reset_state()
            return
        else:
            # Assume it's a YAML file path
            benchmark_file = benchmark_spec
            if not os.path.exists(benchmark_file):
                print(f"Error: Benchmark file '{benchmark_file}' not found.")
                continue  # Skip to the next benchmark

            for f in args.file_list:
                my_handler.spec_run(target_spec=f, lec_iterations=args.lec_limit,comp_iterations=args.comp_limit)
                print(f"Processing YAML file: {yaml_file}")
            
        # print(f"Processing YAML file: {benchmark_file}")
        my_handler.spec_run(target_spec=benchmark_file, lec_iterations=args.lec_limit,comp_iterations=args.comp_limit)

def process_logs(logs_dir, test_case_name):
    compile_log_pattern = os.path.join(logs_dir, '*_compile_log.md')
    compile_logs = glob.glob(compile_log_pattern)

    if not compile_logs:
        print(f"No compile log files found in '{logs_dir}'.")
        return []

    test_results = []

    # Process each compile log file
    for compile_log_file in compile_logs:
        with open(compile_log_file, 'r') as file:
            lines = file.readlines()

        # Find the 'RESULTS :' line
        results_line = None
        for line in reversed(lines):
            if line.startswith('RESULTS :'):
                results_line = line.strip()
                break

        if not results_line:
            print(f"No RESULTS line found in the compile log '{compile_log_file}'.")
            continue

        parts = results_line.split(' : ')
        if len(parts) != 12:
            print(f"Invalid RESULTS line format in the compile log '{compile_log_file}'.")
            continue

        # Parse the parts
        _, model, name, comp_n, comp_f, lec_n, lec_f, top_k, prompt_tokens, completion_tokens, world_clock_time, llm_query_time = parts

        # Determine success or failure
        status = 'Success' if int(comp_f) == 0 and int(lec_f) == 0 else 'Failure'

        test_results.append((test_case_name, status))

    return test_results

def process_logs_and_output(logs_dir, output_file, benchmark_name):
    test_results = process_logs(logs_dir, benchmark_name)

    if not test_results:
        print(f"No test results found for benchmark '{benchmark_name}'.")
        return

    # Write the results to the output file
    output_file = output_file if output_file else 'test_results.txt'

    with open(output_file, 'w') as f:
        for name, status in test_results:
            f.write(f"{name}: {status}\n")

    # Output result to console
    status = test_results[0][1]  # Assuming only one result per benchmark
    print(f"Benchmark '{benchmark_name}' status: {status}")
    print(f"Test result has been saved to {output_file}")

def normalize_name(name):
    if name.endswith('_spec'):
        return name[:-5]  # Remove the last 5 characters ('_spec')
    else:
        return name

def log(args):
    if args.benchmark_name:
        # If benchmark_name is provided, search for it in ~/hdlagent/
        base_dir = os.path.expanduser('~/hdlagent/')
        benchmark_name_normalized = normalize_name(args.benchmark_name)

        # Recursively search for the benchmark directory
        found = False
        for root, dirs, files in os.walk(base_dir):
            dir_name = os.path.basename(root)
            dir_name_normalized = normalize_name(dir_name)
            if dir_name_normalized == benchmark_name_normalized:
                # Found the benchmark directory
                logs_dir = os.path.join(root, 'logs')
                if not os.path.exists(logs_dir):
                    print(f"No logs directory found for benchmark '{args.benchmark_name}'.")
                    return
                # Process the logs for this benchmark
                found = True
                break
        if not found:
            print(f"Benchmark '{args.benchmark_name}' not found under '{base_dir}'.")
            return

        # Process logs and output result
        process_logs_and_output(logs_dir, args.output_file, args.benchmark_name)
    else:
        w_dir = os.path.abspath(args.w_dir)
        print(f"[DEBUG] Working directory: {w_dir}")
    
        # Recursively find all 'logs' directories under w_dir
        logs_dirs = []
        for root, dirs, files in os.walk(w_dir):
            if 'logs' in dirs:
                logs_dir = os.path.join(root, 'logs')
                logs_dirs.append(logs_dir)
    
        if not logs_dirs:
            print(f"No logs directories found under working directory '{w_dir}'.")
            return
    
        test_results = []
    
        for logs_dir in logs_dirs:
            compile_log_pattern = os.path.join(logs_dir, '*_compile_log.md')
            compile_logs = glob.glob(compile_log_pattern)
    
            if not compile_logs:
                print(f"No compile log files found in '{logs_dir}'.")
                continue
    
            # Extract the test case name from the parent directory of the logs directory
            test_case_dir = os.path.dirname(logs_dir)
            test_case_name = os.path.basename(test_case_dir)
            print(f"[DEBUG] Processing test case: {test_case_name}")
    
            # Process each compile log file
            for compile_log_file in compile_logs:
                print(f"[DEBUG] Processing compile log: {compile_log_file}")
                with open(compile_log_file, 'r') as file:
                    lines = file.readlines()
    
                # Find the 'RESULTS :' line
                results_line = None
                for line in reversed(lines):
                    if line.startswith('RESULTS :'):
                        results_line = line.strip()
                        break
    
                if not results_line:
                    print(f"No RESULTS line found in the compile log '{compile_log_file}'.")
                    continue
    
                parts = results_line.split(' : ')
                if len(parts) != 12:
                    print(f"Invalid RESULTS line format in the compile log '{compile_log_file}'.")
                    continue
    
                # Parse the parts
                _, model, name, comp_n, comp_f, lec_n, lec_f, top_k, prompt_tokens, completion_tokens, world_clock_time, llm_query_time = parts
    
                # Determine success or failure
                status = 'Success' if int(comp_f) == 0 and int(lec_f) == 0 else 'Failure'
    
                # Use the test_case_name as the test name
                test_results.append((test_case_name, status))

        if not test_results:
            print("No test results found.")
            return

        # Compute success rate
        success_count = sum(1 for _, status in test_results if status == 'Success')
        total_count = len(test_results)
        success_percentage = (success_count / total_count) * 100 if total_count > 0 else 0
    
        if not test_results:
            print("No test results found.")
            return
    
        # Write the results to the output file
        output_file = args.output_file if args.output_file else 'test_results.txt'
        print(f"[DEBUG] Output file: {output_file}")
    
        with open(output_file, 'w') as f:
            for name, status in test_results:
                f.write(f"{name}: {status}\n")
            f.write(f"\nSuccess rate: {success_percentage:.2f}% ({success_count}/{total_count})\n")
        print(f"Overall success rate: {success_percentage:.2f}% ({success_count}/{total_count})")
        print(f"Test results have been saved to {output_file}")

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
            my_handler.spec_run(target_spec=f, lec_iterations=args.lec_limit,comp_iterations=args.comp_limit)

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
    model.add_argument('--lec_limit',    type=int,   action="store",       default=1,            help='The amount of LLM attempts, max iterations = (top_k * lec_limit * comp_limit)')

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
        print("ERROR: no model available. Try setting OPENAI/Gemini/SambaNova tokens")
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
    parser.add_argument("model", nargs="*", help="platform (openai, sambanova, vertex)")

    return parser

def add_log_command(subparsers):
    parser = subparsers.add_parser('log', help="Collect and save RESULTS lines from previous runs.", add_help=False)
    add_shared_args(parser)
    parser.add_argument('--output-file', type=str, default='test_results.txt', help="The output file to save test results.")
    # parser.add_argument('--list-runs', action='store_true', help="List all available runs and their timestamps.")
    parser.add_argument('benchmark_name', nargs='?', help="Name of the benchmark to log details for", default=None)
    # parser.add_argument('--log_dir', type=str, action="store", default="./", help='Working directory containing log files')
    parser.add_argument('--status', choices=['all', 'success', 'failed'], default='all', help='Filter logs by run status.')
    parser.add_argument('--top_k', type=int, help='Filter logs where top_k is greater than or equal to the specified value.')

    return parser

def add_batch_command(subparsers):
    parser = subparsers.add_parser("batch", help="Perform batch operations on all .spec.yaml files within a directory", add_help=False)
    add_shared_args(parser)
    parser.add_argument('directory_path', type=str, help="Directory containing .spec.yaml files to process")

    return parser

def add_opt_command(subparsers):
    parser = subparsers.add_parser("opt", help="Optimize Verilog code using LLM", add_help=False)
    add_shared_args(parser)
    parser.add_argument("verilog_files", nargs="*", help="List of Verilog files to optimize")
    return parser

def cli_agent():

    parser     = argparse.ArgumentParser(description = "hdlagent: A Hardware Description Language Agent",
                                         epilog="""
Examples:
  hdlagent start description.txt
  hdlagent bench sample/RCA_spec.yaml
  hdlagent build
  hdlagent opt your_verilog_file.v
  hdlagent list-models
  hdlagent log [--list-runs: List all available runs and their timestamps.| benchmark_name: log details| --status, --date-from, --date-to, --top_k: Filter logs|--output-file: to save collected RESULTS lines]
""",
    formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False)
    subparsers = parser.add_subparsers(dest          = "command")

    parser_bench       = add_bench_command(subparsers)
    parser_build       = add_build_command(subparsers)
    parser_list_models = add_list_models_command(subparsers)
    parser_start       = add_start_command(subparsers)
    parser_opt = add_opt_command(subparsers)
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
            parser_log.print_help()
        log(args)
    elif args.command == "opt":
        if args.help:
            parser_opt.print_help()
        else:
            check_args(args)
        opt(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    cli_agent()
