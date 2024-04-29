from agent import Agent
import json
import os

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
    def __init__(self, agent: Agent = None):
        self.agent = agent

        self.comp_iter          = 4
        self.lec_iter           = 1
        self.tb_iter            = 1
        self.lec_feedback_limit = 1
        self.top_k              = 1

        self.id                 = None

    # Assign one agent to handler
    #
    # Intended use: Initialization of Handler
    def set_agent(self, agent: Agent):
        self.agent = agent

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

    # Reads the compile log file of the entry, returns the relevant results in a dictionary
    #
    # Intended use: for checking the status of previous runs
    def get_results(self, entry, base_w_dir: str):
        log_path = os.path.join(base_w_dir, entry['name'], "logs", entry['name'] + "_compile_log.md")
        if os.path.exists(log_path):
            with open(log_path, 'r') as file:
                for last_line in file:
                    pass

            parts = last_line.strip().split(':')
            _, _, comp_n, comp_f, lec_n, lec_f, top_k, _, _, _, _ = [int(part.strip()) if part.strip().isdigit() else part for part in parts]
            res_dict = {}
            res_dict['comp_n'] = comp_n
            res_dict['comp_f'] = comp_f
            res_dict['lec_n']  = lec_n
            res_dict['lec_f']  = lec_f
            res_dict['top_k']  = top_k
            return res_dict
        return None

    # If the test was already completed in the w_dir, it is skipped instead of being re-done
    # This is proven by the existence of a log dump and all top_k being completed
    #
    # Intended use: Save tokens while benchmarking
    def check_completion(self, entry, base_w_dir: str):
        results = self.get_results(entry, base_w_dir)
        if results is not None:
            return results['top_k'] == self.top_k
        return False

    # If the test has already succeeded in the w_dir, it is skipped instead of being re-done
    # This is proven by reading the compile log and checking for a difference between lec_n and lec_f
    #
    # Intended use: Save tokens while benchmarking
    def check_success(self, entry, base_w_dir: str):
        results = self.get_results(entry, base_w_dir)
        if results is not None:
            return results['lec_f'] < results['lec_n']
        return False

    # Individual attempt at a .json benchmark problem, solvable through passing
    # a Yosys LEC check. top_k sets limit for how many unsuccessful attempts
    # can be made until marked as a failure.
    #
    # Indended use: benchmarking LLMs
    def single_json_run(self, entry: dict, base_w_dir, skip_completed, update):
            self.agent.reset_k()
            self.agent.set_interface(entry['interface'])
            self.agent.set_pipeline_stages(int(entry['pipeline_stages']))
            self.agent.set_w_dir(os.path.join(base_w_dir, self.agent.name))

            prompt = entry['instruction']
            if self.agent.spec is not None:
                if not self.agent.spec_exists():
                    self.agent.generate_spec(prompt)
                prompt = self.agent.read_spec()

            self.agent.dump_gold(entry['response'])
            pass_k = self.top_k
            if skip_completed:
                results = self.get_results(entry, base_w_dir)
                if results is not None:
                    pass_k -= results['top_k']
                    self.agent.set_k(results['top_k'] + 1)

            for _ in range(pass_k):
                successful   = self.check_success(entry, base_w_dir)
                completed    = self.check_completion(entry, base_w_dir)
                update_entry = completed and (not successful) and update
                if self.agent.lec_loop(prompt, self.lec_iter, self.lec_feedback_limit, self.comp_iter, update_entry):
                    break
                self.agent.incr_k()


    # Wrapper around single_json_run(), keeps track of individual problems' statuses.
    # Checking if they were passed to not repeat them.
    #
    # Intended use: benchmarking LLMs
    def json_run(self, json_data: dict, skip_completed: bool = False, skip_successful: bool = False, update: bool = False):
        base_w_dir = self.agent.w_dir
        for entry in json_data:
            successful   = self.check_success(entry, base_w_dir)
            completed    = self.check_completion(entry, base_w_dir)
            run          = not ((skip_completed and completed) or (skip_successful and successful))
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
            print("Error: {reference} not found, exiting...")
            exit()
        with open (reference, 'r') as f:
            self.agent.generate_spec(f.read())                                  # may get more complex once nested modules are introduced

    # Typical user run, where a 'spec' must exist, to formally define
    # the interface and desired behavior of the target circuit.
    def spec_run(self, target_spec: str, iterations: int):
        if not os.path.exists(target_spec):
            print("Error: {target_spec} not found, exiting...")
            exit()
        prompt = self.agent.read_spec(target_spec)                              # sets name internally
        self.agent.set_w_dir(os.path.join(self.agent.w_dir, self.agent.name))   # depends on name being set
        self.agent.spec_run_loop(prompt, iterations)

    def sequential_entrypoint(self, spath: str, llm: str, lang: str, json_data: dict = None, skip_completed: bool = False, skip_successful: bool = False, update: bool = False, w_dir: str = './', bench_spec: bool = False, gen_spec: str = None, target_spec: str = None, init_context: bool = False, supp_context: bool = False, temperature: float = None, short_context: bool = False):
        use_spec = bench_spec or (gen_spec is not None) or (target_spec is not None)
        self.set_agent(Agent(spath, llm, lang, init_context, supp_context, use_spec))
        self.agent.set_w_dir(w_dir)
        self.agent.set_model_temp(temperature)
        if short_context:
            self.agent.set_short_context

        if json_data is not None:
            self.json_run(json_data, skip_completed, skip_successful, update)
        else:
            if gen_spec is not None:
                self.generate_spec_from_ref(gen_spec)
            if target_spec is not None:
                self.spec_run(target_spec, self.comp_iter)
