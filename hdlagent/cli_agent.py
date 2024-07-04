#!/usr/bin/env python3

import shutil
import agent
import argparse
from handler import Handler, check_json
from importlib import resources
import os

def start(args):
    if args.help:
        print("\n\nStart a new structured spec file out of a plain problem explanation")
        return

    if len(args.file_list) == 0:
        print("ERROR: start needs a file list of plain text")
        exit(4)

    spath = resources.files('resources')
    my_handler = Handler()
    my_handler.set_comp_iter(args.comp_limit)

    for f in args.file_list:
        if args.help:
            print(f"Creating spec from {f}")
        else:
            my_handler.sequential_entrypoint(spath=str(spath), llms=args.llm, lang=args.lang, update=args.update, w_dir=args.w_dir, gen_spec=f, init_context=args.init_context, supp_context=args.supp_context, short_context=args.short_context)

def bench(args):
    if args.help:
        print("\n\nPerformance against benchmarks")
        return

    json_path = args.json_file
    json_data = check_json(json_path)

    if not json_data:
        print("Error: Failed to load or parse the JSON file at", json_path)
        return

    my_handler = Handler()
    my_handler.set_comp_iter(args.comp_limit)
    my_handler.create_agents(resources.files('resources'), args.llm, args.lang, [], False, True, args.w_dir, None, False)

    for entry in json_data['verilog_problems']:
        print(f"BENCHMARKING... {entry['name']}")
        my_handler.single_json_run(entry, args.w_dir, args.skip_completed, args.update)

def build(args):
    if args.help:
        print("\n\nBuild the HDL out of the spec file[s] or spec files in directory")
        return

    spath = resources.files('resources')
    my_handler = Handler()
    my_handler.set_comp_iter(args.comp_limit)
    my_handler.create_agents(spath=str(spath), llms=args.llm, lang=args.lang, use_spec=True, temperature=None, w_dir=args.w_dir, init_context=args.init_context, supp_context=args.supp_context, short_context=args.short_context)

    if len(args.file_list) == 0:  # Check current directory to build
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
    if not hasattr(args, 'model'):
        args.model = []

    showall = len(args.model) == 0
    if "openai" in args.model or showall:
        if "OPENAI_API_KEY" in os.environ:
            models = agent.list_openai_models()
            if len(models):
                all_models += models
                if not args.silent:
                    print("OpenAI models:")
                    for m in models:
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

    return all_models

def add_shared_args(model):
    model.add_argument('--config', type=str, action="store", help='Path to a configuration YAML file')
    model.add_argument('--llm', type=str, action="append", default=['gpt-4o'], help='LLM model. Use list_models to see models')
    model.add_argument('--lang', type=str, action="store", default="Verilog", choices=['Verilog', 'Chisel', 'PyRTL', 'DSLX'], help='Language for code generation. It can only be "Verilog", "Chisel", "PyRTL", or "DSLX")')
    model.add_argument('--parallel', action="store_false", help='Parallelize hdlagent runs')
    model.add_argument('--w_dir', type=str, action="store", default="./", help='Working dir to generate resource and log files')
    model.add_argument('--comp_limit', type=int, action="store", default=4, help='The amount of LLM attempts, max iterations = (top_k * lec_limit * comp_limit)')
    model.add_argument('--init_context', action="append", default=[], help='Use per language specialized initial context')
    model.add_argument('--supp_context', action="store_false", help='Use per each compile error a supplemental context')
    model.add_argument('--short_context', action="store_false", help='Exclude previous code responses and queries from context window')
    model.add_argument('--update', action="store_true", help='Retry LEC iterations on current RTL code generated')

def check_tools(args):
    if shutil.which('yosys') is None:
        print("Yosys is needed for benchmarking and testing")
        exit(3)

    if (shutil.which('slang') is None) and (shutil.which('iverilog') is None):
        print("To improve Verilog generation iteration install sland and/or iverilog")
        exit(3)

def check_args(args):
    if not hasattr(args, 'file_list'):
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

    for x in args.llm:
        if not (x in l):
            print(f"ERROR: model {x} is not in list-models available")
            exit(3)

def add_start_command(subparsers):
    parser = subparsers.add_parser("start", help="Start a spec from a simple explanation", add_help=False)
    add_shared_args(parser)
    parser.add_argument("file_list", nargs="*", help="Explicit list of text files to start spec.yaml specs")
    return parser

def add_bench_command(subparsers):
    parser = subparsers.add_parser("bench", help="Benchmark the existing hdlagent setup", add_help=False)
    add_shared_args(parser)
    parser.add_argument('json_file', type=str, help="Path to the JSON file containing benchmarks")
    parser.add_argument('--skip_completed', action="store_true", help='Skip already completed tests')
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

def cli_agent():
    parser = argparse.ArgumentParser(description="hdlagent: A Hardware Description Language Agent", add_help=False)
    subparsers = parser.add_subparsers(dest="command")

    parser_bench = add_bench_command(subparsers)
    parser_build = add_build_command(subparsers)
    parser_list_models = add_list_models_command(subparsers)
    parser_start = add_start_command(subparsers)

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
    else:
        parser.print_help()

if __name__ == "__main__":
    cli_agent()

