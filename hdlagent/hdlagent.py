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
  --llm                         Large Language Model choice for code generation
                                Supported Vendors: OpenAI, OctoAI, VertexAI
                                See 'list_x_models' below to view the available options

  --lang                        Language choice for code generation
                                Supported languages: [Verilog, Chisel, PyRTL, DSLX]

  --json_path <path>            Path for .json file where target programs are specified (in bulk).
                                Each entry must appear under list named 'verilog_problems'

Options:
  --help                        Print this message

  --use_spec                    Uses the *_spec.yaml file in the working directory that shares the
                                same name as the lec_source source file. If one does not exist, then
                                uses the selected LLM to generate one. The spec file includes entries
                                for 'instruction' and 'interface'. The spec is meant to iterate over the
                                raw prompt and formalize it, along with validate that the LLM understands
                                the core design.

  --start_from <name>           Allows the user to specify which entry in the supplied .json file to start
                                the run from, effectively setting the starting index.

  --w_dir <path>                Path for working directory, all resulting source code and log files
                                will be left here.

  --comp_limit <val>            The amount of attempts the LLM is allowed to make the program successfully
                                compile without warning or error within a single LEC iteration. 
                                Simply put: max iterations = (top_k * lec_limit * comp_limit)

  --lec_limit <val>             Used only with json_path, sets how many iterations of LEC mismatches are 
                                allowed and fixes are attempted until failure.

  --lec_feedback_limit <val>    Used only with json_path and --lec_limit. Controls how many failing
                                cases of Yosys LEC will be specified as another lec iteration query.

  --top_k <val>                 The amount of attempts the LLM is allowed until a satisfatory implementation is developed

  --init_context                Allows the agent to append the language specific tutorial and context to
                                provide the LLM with initial knowledge on the language syntax and grammar.

  --supp_context                Allows the agent to access the 'supplemental context' database to provide
                                the LLM with suggestions on compile errors and their fixes.

  --openai_models_list          Prints a list of available OpenAI models to use for the LLM parameter

  --octoai_models_list          Prints a list of available OctoAI models to use for the LLM parameter

  --vertexai_models_list        Prints a list of available VertexAI models to use for the LLM parameter
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
    pass

def main(llm: str = None, lang: str = None, json_path: str = None, json_limit: int = -1, comp_limit: int = 4, lec_limit: int = 1, lec_feedback_limit: int = -1, top_k: int = 1, start_from: str = None, w_dir: str = './', use_spec: bool = False, init_context: bool = False, supp_context: bool = False, help: bool = False, openai_models_list: bool = False, octoai_models_list: bool = False, vertexai_models_list: bool = False):
    if (llm is not None) and (lang is not None) and (json_path is not None):
        spath      = resources.files('resources')
        my_handler = Handler()
        my_handler.set_comp_iter(comp_limit)
        my_handler.set_lec_iter(lec_limit)
        my_handler.set_lec_feedback_limit(lec_feedback_limit)
        my_handler.set_k(top_k)
        my_handler.sequential_entrypoint(spath, llm, lang, json_path, json_limit, start_from, w_dir, use_spec, init_context, supp_context)
    elif openai_models_list:
        print(agent.list_openai_models())
    elif octoai_models_list:
        print(agent.list_octoai_models())
    elif vertexai_models_list:
        print(agent.list_vertexai_models())
    else:
        print(help_string)


if __name__ == "__main__":
    fire.Fire(main)
