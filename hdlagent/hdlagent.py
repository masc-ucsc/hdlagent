#!/usr/bin/env python3
import openai
import octoai
import fire

import agent
import handler
from handler import Handler
from importlib import resources
import multiprocessing
import json
import os
from agent import Agent

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

  --parallel                    Parallelize hdlagent

  --start_from <name>           Allows the user to specify which entry in the supplied .json file to start
                                the run from, effectively setting the starting index.

  --json_limit <val>            Used only with json_path, limits how many entries from the .json file
                                will be attempted. Used with start_from to select a subset from .json
                                file that does not begin with the first entry.

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

  --skip_completed              If the w_dir is pointing to a directory which had previous HDLAgent runs done,
                                this option skips those which already have already completed generation.

  --skip_successful             Just like skip_completed, except only skips those which also passed LEC

  --update                      Re-attempt LEC iterations on current version of RTL found in a completed
                                run dir. Cannot be invoked alongside skip_completed, as that conflicts with
                                the idea of a re-attempt.

  --openai_models_list          Prints a list of available OpenAI models to use for the LLM parameter

  --octoai_models_list          Prints a list of available OctoAI models to use for the LLM parameter

  --vertexai_models_list        Prints a list of available VertexAI models to use for the LLM parameter
 """

# WARNING: FEATURES BELOW ARE EXPERIMENTAL - FURTHER VALIDATION AND TESTING REQUIRED
def worker(shared_list, shared_index, lock, spath, llm, lang, comp_limit, lec_limit, lec_feedback_limit, top_k, skip_completed, skip_successful, update, w_dir, use_spec, init_context, supp_context, temperature):
    # Each worker has its own Handler instance.
    handler = Handler()
    handler.set_agent(Agent(spath, llm, lang, init_context, supp_context, use_spec))
    handler.set_comp_iter(comp_limit)
    handler.set_lec_iter(lec_limit)
    handler.set_lec_feedback_limit(lec_feedback_limit)
    handler.set_k(top_k)
    handler.agent.set_w_dir(w_dir)
    handler.agent.set_model_temp(temperature)
    handler.set_id(multiprocessing.current_process().name)

    while True:
        with lock:
            # Check if there are still entries left to process
            if shared_index.value < len(shared_list):
                entry = shared_list[shared_index.value]
                shared_index.value += 1
            else:
                break
        print(f"\nProcessing by {handler.id}: {handler.agent.name}\n")
        successful   = handler.check_success(entry, w_dir)
        if successful:
            print("successful")
        completed    = handler.check_completion(entry, w_dir)
        if completed:
            print("completed")
        update_entry = completed and (not successful) and update
        if update_entry:
            print("update_entry")
        run          = not ((skip_completed and completed) or (skip_successful and successful))
        if run:
            handler.single_json_run(entry, w_dir, update_entry)

def parallel_run(spath: str, llm: str, lang: str, json_data, comp_limit: int, lec_limit: int, lec_feedback_limit: int, top_k: int, skip_completed: bool, skip_successful: bool, update: bool, w_dir: str, use_spec: bool, init_context: bool, supp_context: bool, temperature: float):
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
        p = multiprocessing.Process(target=worker, args=(shared_list, shared_index, lock, spath, llm, lang, comp_limit, lec_limit, lec_feedback_limit, top_k, skip_completed, skip_successful, update, w_dir, use_spec, init_context, supp_context, temperature))
        processes.append(p)
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

def main(llm: str = None, lang: str = None, json_path: str = None, json_limit: int = -1, comp_limit: int = 4, lec_limit: int = 1, lec_feedback_limit: int = -1, top_k: int = 1, start_from: str = None, w_dir: str = './', skip_completed: bool = False, skip_successful: bool = False, update: bool = False, use_spec: bool = False, init_context: bool = False, supp_context: bool = False,  temperature: float = None, help: bool = False, parallel: bool = False, openai_models_list: bool = False, octoai_models_list: bool = False, vertexai_models_list: bool = False):
    if (llm is not None) and (lang is not None) and (json_path is not None):
        spath      = resources.files('resources')
        json_data  = handler.set_json_bounds(handler.check_json(json_path), json_limit, start_from)

        if skip_completed and update:
            print("Error: cannot invoke --skip_completed and --update at the same time, exiting...")
            exit()
        if (parallel):
            parallel_run(spath, llm, lang, json_data, comp_limit, lec_limit, lec_feedback_limit, top_k, skip_completed, skip_successful, update, w_dir, use_spec, init_context, supp_context, temperature)
        else:
            my_handler = Handler()
            my_handler.set_comp_iter(comp_limit)
            my_handler.set_lec_iter(lec_limit)
            my_handler.set_lec_feedback_limit(lec_feedback_limit)
            my_handler.set_k(top_k)
            my_handler.sequential_entrypoint(spath, llm, lang, json_data, skip_completed, skip_successful, update, w_dir, use_spec, init_context, supp_context, temperature)
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
