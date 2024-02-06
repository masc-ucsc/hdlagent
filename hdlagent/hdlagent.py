#!/usr/bin/env python3
import openai
import octoai
import fire

import agent
from handler import Handler
from importlib import resources

help_string = """
Usage: hdlagent --llm=xxx --lang=xxx --json_path=xxx [options]

Parameters:
  --llm                 Large Language Model choice for code generation
                        Supported Vendors: OpenAI, OctoAI
                        See 'list_x_models' below to view the available options
  --lang                Language choice for code generation
                        Supported languages: [Verilog, Chisel, PyRTL, DSLX]
  --json_path <path>    Path for .json file where target programs are specified (in bulk).
                        Each entry must appear under list named 'verilog_problems'

Options:
  --help                Print this message
  --use_spec            Uses the *_spec.yaml file in the working directory that shares the
                        same name as the lec_source source file. If one does not exist, then
                        uses the selected LLM to generate one. The spec file includes entries
                        for 'instruction' and 'interface'. The spec is meant to iterate over the
                        raw prompt and formalize it, along with validate that the LLM understands
                        the core design.
  --w_dir <path>        Path for working directory, all resulting source code and log files
                        will be left here.
  --init_context        Allows the agent to append the language specific tutorial and context to
                        provide the LLM with initial knowledge on the language syntax and grammar.
  --supp_context        Allows the agent to access the 'supplemental context' database to provide
                        the LLM with suggestions on compile errors and their fixes.
  --openai_models_list  Prints a list of available OpenAI models to use for the LLM parameter
  --octoai_models_list  Prints a list of available OctoAI models to use for the LLM parameter
 """

# WARNING: FEATURES BELOW ARE EXPERIMENTAL - FURTHER VALIDATION AND TESTING REQUIRED
def worker(shared_list, shared_index, lock, spath: str, llm: str, lang: str, json_limit: int, w_dir: str, use_spec: bool, init_context: bool, supp_context: bool):
    # Each worker has its own Handler instance.
    handler = Handler()

    while True:
        with lock:
            # Check if there are still entries left to process
            if shared_index.value < len(shared_list):
                entry = shared_list[shared_index.value]
                shared_index.value += 1
            else:
                break

        # Use the Handler instance to process the entry
        handler.set_name(entry)
        print(f"Processing by {multiprocessing.current_process().name}: {handler.name}")
        # Here, you could add more logic to process the entry further.

def parallel_run(spath: str, llm: str, lang: str, json_path: str, json_limit: int, w_dir: str, use_spec: bool, init_context: bool, supp_context: bool):


def main(llm: str = None, lang: str = None, json_path: str = None, json_limit: int = -1, w_dir: str = './', use_spec: bool = False, init_context: bool = False, supp_context: bool = False, help: bool = False, openai_models_list: bool = False, octoai_models_list: bool = False):
    if (llm is not None) and (lang is not None) and (json_path is not None):
        spath      = resources.files('resources')
        my_handler = Handler()
        my_handler.sequential_entrypoint(spath, llm, lang, json_path, json_limit, w_dir, use_spec, init_context, supp_context)
    elif openai_models_list:
        print(list_openai_models())
    elif octoai_models_list:
        print(list_octoai_models())
    else:
        print(help_string)


if __name__ == "__main__":
    fire.Fire(main)
