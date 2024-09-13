#!/usr/bin/env python3

import click

import agent
import handler
from handler import Handler
from importlib import resources
import multiprocessing
import os
from agent import Agent
from pathlib import Path
import yaml


# WARNING: FEATURES BELOW ARE EXPERIMENTAL - FURTHER VALIDATION AND TESTING REQUIRED
def worker(shared_list, shared_index, lock, spath, llm, lang, comp_limit, lec_limit, lec_limit_feedback, top_k, skip_completed, skip_successful, update, w_dir, bench_spec, init_context, supp_context, temperature, short_context):
    # Each worker has its own Handler instance.
    handler = Handler()
    handler.create_agents(spath, llm, lang, init_context, supp_context, bench_spec, w_dir, temperature, short_context)
    handler.set_comp_iter(comp_limit)
    handler.set_lec_iter(lec_limit)
    handler.set_lec_feedback_limit(lec_limit_feedback)
    handler.set_k(top_k)
    handler.set_id(multiprocessing.current_process().name)

    while True:
        with lock:
            # Check if there are still entries left to process
            if shared_index.value < len(shared_list):
                entry = shared_list[shared_index.value]
                shared_index.value += 1
            else:
                break
        print(f"\nProcessing by {handler.id}: {handler.agents[0].name}\n")
        successful   = handler.check_success(entry, w_dir)
        completed    = handler.check_completion(entry, w_dir)
        run          = not ((skip_completed and completed) or (skip_successful and successful))
        if run:
            handler.single_json_run(entry, w_dir, skip_completed, update)

def parallel_run(spath: str, llm: list, lang: str, json_data, comp_limit: int, lec_limit: int, lec_limit_feedback: int, top_k: int, skip_completed: bool, skip_successful: bool, update: bool, w_dir: str, bench_spec: bool, init_context: list, supp_context: bool, temperature: float, short_context: bool):
    # Create a multiprocessing manager to manage shared state
    manager      = multiprocessing.Manager()

    #shared list will need to change based on json formatting
    shared_list  = manager.list(json_data)
    shared_index = manager.Value('i', 0)  # Shared json index initialized to 0
    lock         = manager.Lock()  # Lock for synchronizing access to the shared index

    # List to keep track of processes
    processes    = []
    # Create and start multiprocessing workers
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=worker, args=(shared_list, shared_index, lock, spath, llm, lang, comp_limit, lec_limit, lec_limit_feedback, top_k, skip_completed, skip_successful, update, w_dir, bench_spec, init_context, supp_context, temperature, short_context))
        processes.append(p)
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

def load_config(ctx, param, value):
    # Loads configuration settings from a YAML file and updates the context defaults
    if value is not None:
        with open(value, 'r') as f:
            data = yaml.safe_load(f)
        # Override default values with values from the config file
        for param in ctx.command.params:
            if param.name in data:
                param.default = data[param.name]
        ctx.ensure_object(dict)
        ctx.obj.update(data)
    return value


@click.command()
@click.option('--list_models', is_flag=True, default=False, help='List all available models (OpenAI, OctoAI, VertexAI, SambaNova), some may have too short context.')
@click.option('--config', type=click.Path(exists=True), callback=load_config, expose_value=False, is_eager=True, help='Path to a configuration YAML file.')

@click.option('--llm', type=str, multiple=True, default=["gpt-3.5-turbo-0613"], help='Specify one of more LLM models. Use --list_models to list models.')
@click.option('--lang', type=click.Choice(['Verilog', 'Chisel', 'PyRTL', 'DSLX'], case_sensitive=False), default="Verilog", help='Language for code generation. It can only be "Verilog", "Chisel", "PyRTL", or "DSLX".')
@click.option('--parallel', is_flag=True, default=False, help='Parallelize hdlagent.')

@click.option('--bench', type=str, default=None, help='Path to the json file for benchmarking.')
@click.option('--bench_limit', type=int, default=-1, help='Allows to specify the number of tests to run in the benchmark json file.')
@click.option('--bench_from', type=str, default=None, help='Allows to specify from which entry to try in the benchmark json file.')
@click.option('--bench_spec', is_flag=True, default=False, help='Create and use a spec when using benchmarking.')

@click.option('--gen_spec', type=str, default=None, help='Use LLM to convert raw natural-language prompt to generate formal spec file.')
@click.option('--target_spec', type=str, default=None, help='Triggers an RTL generation run given a target spec')

@click.option('--w_dir', type=str, default="./", help='Working dir to generate resource and log files.')
@click.option('--comp_limit', type=int, default=4, help='The amount of LLM attempts, max iterations = (top_k * lec_limit * comp_limit).')
@click.option('--lec_limit', type=int, default=1, help='The amount of LEC attemps to fix code after generation.')
@click.option('--lec_limit_feedback', type=int, default=4, help='How many  Yosys LEC failures are passed for each --lec_limit attempt.')

@click.option('--top_k', type=int, default=1, help='Number of overall LLM attempts.')
@click.option('--temperature', type=float, help='Modify default LLM temperature.')

@click.option('--init_context', type=str, multiple=True, default=[], help='Specify one or more initial context(s) to append to chat. Use per language specialized initial context by adding \'default\'.')
@click.option('--supp_context', is_flag=True, default=False, help='Use per each compile error a supplemental context.')
@click.option('--skip_completed', is_flag=True, default=False, help='If w_dir has previous completed runs, do not regenerate even if failed.')
@click.option('--skip_successful', is_flag=True, default=False, help='If w_dir has previous successful runs with LEC passing, do not regenerate.')
@click.option('--update', is_flag=True, default=False, help='Retry LEC iterations on current RTL code generated.')
@click.option('--short_context', is_flag=True, default=False, help='Exclude previous code responses and queries from context window.')

@click.argument('files', nargs=-1, type=click.Path())
@click.pass_context
def process_args(ctx, list_models:bool, llm, lang:str, parallel:bool, bench:str, bench_limit:int, bench_from:str, bench_spec:bool, gen_spec:str, target_spec:str, w_dir:str, comp_limit:int, lec_limit:int, lec_limit_feedback:int, top_k: int, temperature:float, init_context:list, supp_context:bool, skip_completed: bool, skip_successful: bool, update: bool, short_context: bool, files):
    ctx.ensure_object(dict)
    llm = ctx.obj.get('llm', llm)
    if isinstance(llm, str):
        llm = [llm]
    init_context = ctx.obj.get('init_context', init_context)
    if isinstance(init_context, str):
        init_context = [init_context]

    if list_models:
        if "OPENAI_API_KEY" in os.environ:
            models = agent.list_openai_models()
            if len(models):
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
                print("OctoAI models:")
                for m in models:
                    print(" ", m)
                print("\n")
        else:
            print("OctoAI unavailable unless OCTOAI_TOKEN is set")

        # TODO: It would be nice to have a cleaner API or way to test for access and/or ask to login if VertexAI model is used. Not just a try/except at runtime
        models = agent.list_vertexai_models()
        if len(models):
            print("VertexAI models:")
            for m in models:
                print(" ", m)
            print("\n")

        if "SAMBANOVA_API_KEY" in os.environ:
            models = agent.list_sambanova_models()
            if len(models):
                print("SambaNova models:")
                for m in models:
                        print(" ", m)
                print("\n")
        else:
            print("SambaNova unavailable unless SAMBANOVA_API_KEY is set")

    elif bench is not None:
        spath      = resources.files('resources')
        json_data  = handler.set_json_bounds(handler.check_json(bench), bench_limit, bench_from)

        if skip_completed and update:
            print("Error: cannot invoke --skip_completed and --update at the same time, exiting...")
            exit()
        if gen_spec is not None:
            print("Error: cannot invoke --bench and --gen_spec at the same time, exiting...")
            exit()
        if target_spec is not None:
            print("Error: cannot invoke --bench and --target_spec at the same time, exiting...")
            exit()
        if (parallel):
            parallel_run(spath, llm, lang, json_data, comp_limit, lec_limit, lec_limit_feedback, top_k, skip_completed, skip_successful, update, w_dir, bench_spec, init_context, supp_context, temperature, short_context)
        else:
            my_handler = Handler()
            my_handler.set_comp_iter(comp_limit)
            my_handler.set_lec_iter(lec_limit)
            my_handler.set_lec_feedback_limit(lec_limit_feedback)
            my_handler.set_k(top_k)
            my_handler.sequential_entrypoint(spath, llm, lang, json_data, skip_completed, skip_successful, update, w_dir, bench_spec, gen_spec, target_spec, init_context, supp_context, temperature, short_context)
    elif (gen_spec is not None) or (target_spec is not None):
            spath      = resources.files('resources')
            my_handler = Handler()
            my_handler.set_comp_iter(comp_limit)
            my_handler.sequential_entrypoint(spath, llm, lang, None, skip_completed, skip_successful, update, w_dir, bench_spec, gen_spec, target_spec, init_context, supp_context, temperature, short_context)
    else:
        print(ctx.get_help())
        for f in files:
            print("XXX {}\n", f)

        file_path = Path('spec.yaml')
        if file_path.exists():
          print("HERE\n")
        else:
          print("no spec.yaml found\n")
          exit(3)


if __name__ == "__main__":
    process_args.main(standalone_mode=False)
