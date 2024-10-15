from agent import Agent, Role
import json
import os
from pathlib import Path
import yaml 
import logging


def check_json(json_path: str):
    data = None
    if (json_path is not None):
        if not os.path.exists(json_path):
            print(f"Error: json_path {json_path} does not exist, exiting...")
            exit()
        else:
            try:
                with open(json_path, 'r') as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                print("Error: json_path supplied is not a valid .json file, exiting...")
                exit()
    return data

def set_json_bounds(json_data: dict, limit: int = -1, start_from: str = None):
    if json_data is None:
        print("Error: no json file registered, exiting...")
        exit()
    data = json_data['verilog_problems']

    start_idx = 0
    if start_from is not None:
        start_idx = next((i for i, entry in enumerate(data) if entry['name'] == start_from), None)
        if start_idx is None:
            print("Error: start_from .json entry was not found, exiting...")
            exit()
    limit += start_idx

    if (limit < 1) or (limit > len(data)) or (limit < start_idx):
        limit = len(data)

    return data[start_idx: limit]

class Handler:
    def __init__(self):
        self.agents             = []

        self.comp_iter          = 4
        self.lec_iter           = 1
        self.tb_iter            = 1
        self.lec_feedback_limit = 1
        self.top_k              = 1

        self.id                 = None

    # Assign a new agent to handler
    #
    # Intended use: arbitration of Agents
    def add_agent(self, agent: Agent):
        self.agents.append(agent)

    # Parallel processing Handler enumeration
    #
    # Intended use: testing
    def set_id(self, proc_id: str):
        self.id = proc_id

    # Sets the amount of allowed iterations for a compile loop, which can be
    # nested within a LEC loop or a testbench loop. The maximum amount of queries
    # sent is then calculated by (comp_iter * lec_iter) or (comp_iter * tb_iter)
    # depending on if the run is LEC driven of testbench driven, respectively.
    #
    # Intended use: before a new run
    def set_comp_iter(self, n: int):
        if n < 1:
            print("Error: cannot set compilation iterations to less than 1, exiting...")
            exit()
        self.comp_iter = n
    
    # Sets the amount of allowed iterations for a LEC loop.
    #
    # Intended use: before a new run
    def set_lec_iter(self, n: int):
        if n < 1:
            print("Error: cannot set LEC iterations to less than 1, exiting...")
            exit()
        self.lec_iter = n

    # Sets the amount of allowed iterations for a testbench loop.
    #
    # Intended use: before a new run
    def set_tb_iter(self, n: int):
        if n < 1:
            print("Error: cannot set testbench iterations to less than 1, exiting...")
            exit()
        self.tb_iter = n

    # Sets the amount of top k results are retreived from the LLM.
    #
    # Intended use: before a new run
    def set_k(self, n: int):
        if n < 1:
            print("Error: cannot set top k iterations to less than 1, exiting...")
            exit()
        self.top_k = n

    # Limits how many testcases can be given back from Yosys LEC for iterative feedback
    #
    # Intended use: before a new run
    def set_lec_feedback_limit(self, n: int):
        self.lec_feedback_limit = n

    # Returns the Agent with 'role' of 'DESIGN'
    # Returns 'None' if designer is not found
    #
    # Intended use: reference intended designer Agent
    def get_designer(self):
        return next((agent for agent in self.agents if agent.role == Role.DESIGN), None)

    # Returns the list of tester Agents with 'role' of 'VALIDATION'
    #
    # Intended use: extract sublists of Agents by 'role'
    def get_testers(self):
        return [agent for agent in self.agents if agent.role == Role.VALIDATION]

    # Creates and adds each Agent to the Handlers list, assigning respective roles
    #
    # Intended use: setup before doing any runs
    def create_agents(self, spath, llms, lang, init_context, supp_context, use_spec, w_dir, temperature, short_context):
        role = Role.DESIGN
        for llm in llms:
            new_agent = Agent(spath, llm, lang, init_context, supp_context, use_spec)
            new_agent.set_w_dir(w_dir)
            new_agent.set_model_temp(temperature)
            new_agent.set_role(role)
            if short_context:
                new_agent.set_short_context
            self.add_agent(new_agent)
            role = Role.VALIDATION          # Default only one LLM can be generate the RTL

    # Reads the compile log file of the entry, returns the relevant results in a dictionary
    #
    # Intended use: for checking the status of previous runs
    # def get_results(self, entry, base_w_dir: str):
    #     log_path = os.path.join(base_w_dir, entry['name'], "logs", entry['name'] + "_compile_log.md")
    #     if os.path.exists(log_path):
    #         with open(log_path, 'r') as file:
    #             for last_line in file:
    #                 pass

    #         parts = last_line.strip().split(':')
    #         _, _, _, comp_n, comp_f, lec_n, lec_f, top_k, _, _, _, _ = [int(part.strip()) if part.strip().isdigit() else part for part in parts]
    #         res_dict = {}
    #         res_dict['comp_n'] = comp_n
    #         res_dict['comp_f'] = comp_f
    #         res_dict['lec_n']  = lec_n
    #         res_dict['lec_f']  = lec_f
    #         res_dict['top_k']  = top_k
    #         return res_dict
    #     return None

    # # If the test was already completed in the w_dir, it is skipped instead of being re-done
    # # This is proven by the existence of a log dump and all top_k being completed
    # #
    # # Intended use: Save tokens while benchmarking
    # def check_completion(self, entry, base_w_dir: str):
    #     results = self.get_results(entry, base_w_dir)
    #     if results is not None:
    #         return results['top_k'] == self.top_k
    #     return False

    # If the test has already succeeded in the w_dir, it is skipped instead of being re-done
    # This is proven by reading the compile log and checking for a difference between lec_n and lec_f
    #
    # Intended use: Save tokens while benchmarking
    # def check_success(self, entry, base_w_dir: str):
    #     results = self.get_results(entry, base_w_dir)
    #     if results is not None:
    #         return results['lec_f'] < results['lec_n']
    #     return False

    def get_results(self, spec_name: str, base_w_dir: str):
        if not isinstance(base_w_dir, Path):
            base_w_dir = Path(base_w_dir)
        base_w_dir = base_w_dir.resolve()

        log_path = base_w_dir / "logs" / f"{spec_name}_compile_log.md"
 
        if log_path.exists():
            with open(log_path, 'r') as file:
                lines = file.readlines()
                if lines:
                    last_line = lines[-1]
                    if "RESULTS" in last_line:
                        parts = [part.strip() for part in last_line.strip().split(':')]
                        res_dict = {
                            'comp_n': int(parts[3]),
                            'comp_f': int(parts[4]),
                            'lec_n': int(parts[5]),
                            'lec_f': int(parts[6]),
                            'top_k': int(parts[7]),
                        }
                        print(f"[DEBUG] Parsed results: {res_dict}")
                        return res_dict
        else:
            pass
        return None

    def check_completion(self, spec_name: str, benchmark_w_dir: str):
        results = self.get_results(spec_name, benchmark_w_dir)
        if results is not None:
            return results['top_k'] >= self.top_k
        return False

    def check_success(self, spec_name: str, benchmark_w_dir: str):
        results = self.get_results(spec_name, benchmark_w_dir)
        if results is not None:
            return results['lec_f'] < results['lec_n']
        return False

    # Individual attempt at a .json benchmark problem, solvable through passing
    # a Yosys LEC check. top_k sets limit for how many unsuccessful attempts
    # can be made until marked as a failure. When multiple LLMs are specified,
    # only one will write the RTL while the others generate testbenches.
    #
    # Indended use: benchmarking LLMs
    def single_json_run(self, entry: dict, base_w_dir, skip_completed, update):
        for agent in self.agents:
            agent.reset_k()
            agent.set_interface(entry['interface'])
            agent.set_pipeline_stages(int(entry['pipeline_stages']))
            agent.set_w_dir(os.path.join(base_w_dir, agent.name))

        designer = self.get_designer()
        testers  = self.get_testers()
        prompt   = entry['instruction']
        if designer.spec is not None:
            if not designer.spec_exists():
                designer.generate_spec(prompt)
            prompt = designer.read_spec()

        designer.dump_gold(entry['response'])
        pass_k = self.top_k
        if skip_completed:
            results = self.get_results(entry, base_w_dir)
            if results is not None:
                pass_k -= results['top_k']
                designer.set_k(results['top_k'] + 1)

        for _ in range(pass_k):
            successful   = self.check_success(entry, base_w_dir)
            completed    = self.check_completion(entry, base_w_dir)
            update_entry = completed and (not successful) and update
            # Single LLM only needs to generate RTL then verify versus gold
            if not testers:
                if designer.lec_loop(prompt, self.lec_iter, self.lec_feedback_limit, self.comp_iter, update_entry):
                    break
            else:   # Other LLMs will create additional testbenches to run design through before gold verification
                designer.reset_conversations()
                designer.reset_perf_counters()
                code_compiled, failure_reason = designer.code_compilation_loop(prompt, 0, self.comp_iter)
                if code_compiled:
                    designer.reformat_verilog(designer.name, designer.gold, designer.verilog, designer.io)
                    testers[0].reset_conversations()
                    testers[0].reset_perf_counters()
                    tb_pass, failure_reason = testers[0].tb_loop(prompt, 2, designer, self.comp_iter)
                    if tb_pass is not None:
                        failure_reason = designer.test_lec()
                if designer.finish_run(failure_reason):
                    break
            designer.incr_k()


    def single_yaml_run(self, yaml_file: str, base_w_dir: str, skip_completed: bool, update: bool):
        # Read and parse the YAML file
        
        logging.basicConfig(
            level=logging.DEBUG,  # Capture all levels of log messages
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()  # Output logs to the console
            ]
        )
        logging.debug(f"Entering single_yaml_run with yaml_file: {yaml_file}")
        print(f"[DEBUG] Entering single_yaml_run with yaml_file: {yaml_file}")
        with open(yaml_file, 'r') as f:
            try:
                entry = yaml.safe_load(f)
                print(f"[DEBUG] Parsed YAML content: {entry}")
            except yaml.YAMLError as e:
                print(f"Error parsing YAML file {yaml_file}: {e}")
                exit(1)
        spec_name = os.path.splitext(os.path.basename(yaml_file))[0]
        print(f"[DEBUG] Derived spec_name: {spec_name}")
        for agent in self.agents:
            agent.reset_k()
            agent.set_interface(entry.get('interface', ''))
            agent.set_pipeline_stages(int(entry.get('pipeline_stages', 0)))
            agent.set_w_dir(os.path.join(base_w_dir, agent.name, spec_name))
            print(f"[DEBUG] Configured agent: {agent.name}")

        designer = self.get_designer()
        testers  = self.get_testers()
        if designer is None:
            print("[ERROR] No DESIGN agent found. Exiting...")
            exit(1)
        print(f"[DEBUG] Designer agent found: {designer.name}")

        designer.read_spec(yaml_file)
        prompt = designer.spec_content
        # self.lec_loop(prompt)
        print(f"[DEBUG] Spec prompt: {prompt}")
        # prompt = entry.get('instruction', '')
        designer.dump_gold(entry.get('bench_response', ''))
        print(f"[DEBUG] Dumped golden Verilog for spec: {spec_name}")

        pass_k = self.top_k
        if skip_completed:
            results = self.get_results(spec_name, base_w_dir)
            print(f"[DEBUG] Results from get_results: {results}")
            if results is not None:
                pass_k -= results['top_k']
                designer.set_k(results['top_k'] + 1)
                print(f"[DEBUG] Updated pass_k: {pass_k}")

        print(f"[DEBUG] Starting execution loop with pass_k: {pass_k}")
        for iteration in range(pass_k):
            print(f"[DEBUG] Iteration {iteration + 1} of {pass_k}")
            # successful   = self.check_success(yaml_file, base_w_dir)
            # completed    = self.check_completion(yaml_file, base_w_dir)
            successful = self.check_success(spec_name, base_w_dir)
            completed = self.check_completion(spec_name, base_w_dir)
            print(f"[DEBUG] Successful: {successful}, Completed: {completed}")

            update_entry = completed and (not successful) and update
            logging.debug(f"Parsed YAML content: {entry}")
            if not testers:
                print("[DEBUG] No VALIDATION agents found. Invoking lec_loop.")
                lec_result = designer.lec_loop(prompt, self.lec_iter, self.lec_feedback_limit, self.comp_iter, update_entry)
                print(f"[DEBUG] lec_loop returned: {lec_result}")
                if lec_result:
                    print("[DEBUG] lec_loop signaled to break the loop.")
                    break
            else:
                print("[DEBUG] VALIDATION agents found. Running testbench loop.")
                designer.reset_conversations()
                designer.reset_perf_counters()
                code_compiled, failure_reason = designer.code_compilation_loop(prompt, 0, self.comp_iter)
                if code_compiled:
                    designer.reformat_verilog(designer.name, designer.gold, designer.verilog, designer.io)
                    print(f"[DEBUG] Reformatting Verilog completed for spec: {spec_name}")

                    testers[0].reset_conversations()
                    testers[0].reset_perf_counters()
                    tb_pass, failure_reason = testers[0].tb_loop(prompt, 2, designer, self.comp_iter)
                    if tb_pass is not None:
                        print("[DEBUG] Invoking test_lec from testbench loop.")
                        failure_reason = designer.test_lec()
                if designer.finish_run(failure_reason):
                    print("[DEBUG] finish_run signaled to break the loop.")
                    break
                designer.incr_k()
                print(f"[DEBUG] Incremented designer's k to: {designer.k}")

            # if designer.spec_run_loop(prompt, self.comp_iter):
            #     if testers:
            #         for agent in testers:
            #             agent.tb_loop(prompt)
            #     break
            # designer.incr_k()

    # Wrapper around single_json_run(), keeps track of individual problems' statuses.
    # Checking if they were passed to not repeat them.
    #
    # Intended use: benchmarking LLMs
    def json_run(self, json_data: dict, skip_completed: bool = False, skip_successful: bool = False, update: bool = False):
        base_w_dir = self.get_designer().w_dir
        for entry in json_data:
            successful = self.check_success(entry, base_w_dir)
            completed  = self.check_completion(entry, base_w_dir)
            run        = not ((skip_completed and completed) or (skip_successful and successful))
            if run:
                self.single_json_run(entry, base_w_dir, skip_completed, update)

    # If the user does not wish to create their own spec, but has an
    # informal definition of their desired behavior in a text file,
    # this will use an LLM to create a formatted spec to be used for RTL
    # generation.
    #
    # Intended use: format and formalize desired circuit into spec file
    def generate_spec_from_ref(self, reference: str):
        if not os.path.exists(reference):
            print(f"Error: {reference} not found, exiting...")
            exit()
        num_agents = len(self.agents)
        if num_agents > 1:
            print(f"Error: found {num_agents} LLMs specified, only 1 allowed for spec generation, exiting...")
            exit()

        with open (reference, 'r') as f:
            self.get_designer().generate_spec(f.read())  # may get more complex once nested modules are introduced

    # Typical user run, where a 'spec' must exist, to formally define
    # the interface and desired behavior of the target circuit.
    # Additional Agents may be used to testbench the generated RTL
    #
    # Intended use: user-facing code and test generation
    def spec_run(self, target_spec: str, iterations: int, w_dir: str = None,
                 skip_completed: bool = True, update: bool = False, skip_successful: bool = True):
        #print(f"spec_run: skip_completed={skip_completed}, skip_successful={skip_successful}")
        #print(f"Processing spec file: {target_spec}")
        if not os.path.exists(target_spec):
            print(f"Error: {target_spec} not found, exiting...")
            exit()
    
        designer = self.get_designer()
        spec_name = os.path.splitext(os.path.basename(target_spec))[0]
        # print(f"Spec name: {spec_name}")
    
        designer.read_spec(target_spec)
        designer.name = spec_name
        prompt = designer.spec_content
        #print(f"After read_spec, designer.name: {designer.name}")
    
        if w_dir is not None:
            base_w_dir = Path(w_dir)
        else:
            base_w_dir = Path('.')
        base_w_dir = base_w_dir.resolve()
    
        benchmark_w_dir = base_w_dir / spec_name
        benchmark_w_dir = benchmark_w_dir.resolve()
        designer.set_w_dir(benchmark_w_dir)
        #print(f"Designer w_dir set to: {designer.w_dir}")
        successful = self.check_success(designer.name, benchmark_w_dir)
        completed = self.check_completion(designer.name, benchmark_w_dir)
        run = True
        if skip_completed and completed:
            run = False
            #print(f"Skipping '{spec_name}' as it is already completed.")
        elif skip_successful and successful:
            run = False
            #print(f"Skipping '{spec_name}' as it is already successful.")
    
        print(f"Successful: {successful}")
        print(f"Completed: {completed}")
        print(f"Run: {run}")
    
        if not run:
            return
        #print(f"Before spec_run_loop, designer.name: {designer.name}")
        compiled = designer.spec_run_loop(designer.read_spec(target_spec), iterations)
        # print(f"After spec_run_loop, designer.name: {designer.name}")
        if compiled:
            designer.lec_loop(prompt)
            for agent in self.get_testers():
                agent.set_w_dir(w_dir)
                print(f"__________________________________________________________________")
                agent.tb_loop(agent.read_spec(target_spec))
    
    def sequential_entrypoint(self, spath: str, llms: list, lang: str, yaml_files: list = None,
                          skip_completed: bool = True, skip_successful: bool = True, update: bool = False,
                          w_dir: str = './', bench_spec: bool = False, gen_spec: str = None, target_spec: str = None,
                          init_context: list = [], supp_context: bool = False, temperature: float = None,
                          short_context: bool = False):
        #print(f"%%%%%: skip_completed={skip_completed}, skip_successful={skip_successful}")
        use_spec = bench_spec or (gen_spec is not None) or (target_spec is not None)
        self.create_agents(spath, llms, lang, init_context, supp_context, use_spec, w_dir, temperature, short_context)

        if yaml_files is not None:
            yaml_files = list(set(yaml_files))  # Remove duplicates
            print(f"[DEBUG] Invoking yaml_run with files: {yaml_files}")
            self.yaml_run(yaml_files, skip_completed, skip_successful, update)
        else:
            if gen_spec is not None:
                self.generate_spec_from_ref(gen_spec)
            if target_spec is not None:
                self.spec_run(target_spec, self.comp_iter, w_dir=w_dir, skip_completed=skip_completed,
                      update=update, skip_successful=skip_successful)

        #if json_data is not None:
        #    self.json_run(json_data, skip_completed, skip_successful, update)
        #else:
        #    if gen_spec is not None:
        #        self.generate_spec_from_ref(gen_spec)
        #    if target_spec is not None:
        #        self.spec_run(target_spec, self.comp_iter)

    def yaml_run(self, yaml_files: list, skip_completed: bool = True, skip_successful: bool = False, update: bool = False):
        base_w_dir = self.get_designer().w_dir
        print(f"[DEBUG] Starting yaml_run with base_w_dir: {base_w_dir}")

        for yaml_file in yaml_files:
            spec_name = os.path.splitext(os.path.basename(yaml_file))[0]
            # with open(yaml_file, 'r') as f:
            #     try:
            #         entry = yaml.safe_load(f)
            #     except yaml.YAMLError as e:
            #         print(f"Error parsing YAML file {yaml_file}: {e}")
            #         continue  # Skip this file

            successful = self.check_success(spec_name, base_w_dir)
            completed = self.check_completion(spec_name, base_w_dir)
            print(f"[DEBUG] Test '{spec_name}' - Successful: {successful}, Completed: {completed}")
            # successful = self.check_success(yaml_file, base_w_dir)
            # completed  = self.check_completion(yaml_file, base_w_dir)
            run        = not ((skip_completed and completed) or (skip_successful and successful))
            if run:
                print(f"[DEBUG] Running single_yaml_run for spec: {spec_name}")
                self.single_yaml_run(yaml_file, base_w_dir, skip_completed, update)
            else:
                print(f"[DEBUG] Skipping spec '{spec_name}' as per skip flags.")