#!/usr/bin/env python3

import shutil
import agent
import argparse
from handler import Handler
from importlib import resources
import os

def create(args):
    spath      = resources.files('resources')
    my_handler = Handler()
    my_handler.set_comp_iter(args.comp_limit)

    for f in args.file_list:
        if args.help:
            print(f"creating spec from {f}")
        else:
            my_handler.sequential_entrypoint(spath=str(spath), llms=args.llm, lang=args.lang, update=args.update, w_dir=args.w_dir, gen_spec=f, init_context=args.init_context, supp_context=args.supp_context, short_context=args.short_context)

def bench(args):
    print(f"Running build command with LLM: {args.llm}")
    # Add your logic for the build command here

def build(args):
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
    all_models = []
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

    # TODO: It would be nice to have a cleaner API or way to test for access and/or ask to login if VertexAI model is used. Not just a try/except at runtime
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

    model.add_argument('--config',        type=str,   action="store",       help='Path to a configuration YAML file')
    model.add_argument('--llm',           type=str,   action="append",      default=['gpt-4o'], help='LLM model. Use list_models to see models')
    model.add_argument('--lang',          type=str,   action="store",       default="Verilog",                choices=['Verilog', 'Chisel', 'PyRTL', 'DSLX'], help='Language for code generation. It can only be "Verilog", "Chisel", "PyRTL", or "DSLX"')
    model.add_argument('--parallel',      action="store_false", help='Parallelize hdlagent runs')

    model.add_argument('--w_dir',         type=str,   action="store",       default="./",         help='Working dir to generate resource and log files')
    model.add_argument('--comp_limit',    type=int,   action="store",       default=4,            help='The amount of LLM attempts, max iterations = (top_k * lec_limit * comp_limit)')

    model.add_argument('--init_context',  action="append",      default=[], help='Use per language specialized initial context')
    model.add_argument('--supp_context',  action="store_false", help='Use per each compile error a supplemental context')
    model.add_argument('--short_context', action="store_false", help='Exclude previous code responses and queries from context window')

    model.add_argument('--update',        action="store_false", help='Retry LEC iterations on current RTL code generated')

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

    for x in args.llm:
        if not (x in l):
            print(f"ERROR: model {x} is not in list-models available")
            exit(3)

def add_create_command(subparsers):
    parser = subparsers.add_parser("create", help="Create a spec from a simple explanation", add_help=False)
    add_shared_args(parser)
    parser.add_argument("file_list", nargs="+", help="Explicit list of text files to create spec.yaml specs")

    return parser

def add_bench_command(subparsers):
    parser = subparsers.add_parser("bench", help="Benchmark the existing hdlagent setup", add_help=False)
    add_shared_args(parser)
    parser.add_argument("file_list", nargs="+", help="List of files to clean")

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

    parser     = argparse.ArgumentParser(description = "hdlagent: A Hardware Description Language Agent", add_help=False)
    subparsers = parser.add_subparsers(dest          = "command")

    parser_create = add_create_command(subparsers)
    parser_bench  = add_bench_command(subparsers)
    parser_build  = add_build_command(subparsers)
    parser_list_models = add_list_models_command(subparsers)

    args, unknown = parser.parse_known_args()

    if '-h' in unknown or '--help' in unknown:
        args.help = True
    else:
        args.help = False

    # args = parser.parse_args()
    if args.command:
        check_args(args)

    check_tools(args)

    if args.command == "create":
        if args.help:
            parser_create.print_help()
        create(args)
    elif args.command == "bench":
        if args.help:
            parser_bench.print_help()
        bench(args)
    elif args.command == "build":
        if args.help:
            parser_build.print_help()
        build(args)
    elif args.command == "list-models":
        if args.help:
            parser_list_models.print_help()
        list_models(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    cli_agent()
