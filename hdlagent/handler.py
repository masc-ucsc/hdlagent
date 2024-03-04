from agent import Agent
import json
import os

def check_json(json_path: str):
    data = None
    if (json_path is not None):
        if not os.path.exists(json_path):
            print("Error: json_path supplied does not exist, exiting...")
            exit()
        else:
            try:
                with open(json_path, 'r') as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                print("Error: json_path supplied is not a valid .json file, exiting...")
                exit()
    return data

def set_json_bounds(json_data, limit: int = -1, start_from: str = None):
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

    # If the test was already completed in the w_dir, it is skipped instead of being re-done
    # This is proven by the existence of a log dump being done in its w_dir
    #
    # Intended use: Save tokens while benchmarking
    def check_completion(self, entry, base_w_dir: str):
        log_path = os.path.join(base_w_dir, entry['name'], "logs")
        if os.path.exists(log_path) and os.path.isdir(log_path):
            for file_name in os.listdir(log_path):
                if file_name.endswith('.md'):
                    return True
        return False

    # If the test has already succeeded in the w_dir, it is skipped instead of being re-done
    # This is proven by the lack of a failure dump being done in its w_dir
    #
    # Intended use: Save tokens while benchmarking
    def check_success(self, entry, base_w_dir: str):
        fail_log_path = os.path.join(base_w_dir, entry['name'], "logs", f"{entry['name']}_fail.md")
        return os.path.exists(fail_log_path)

    def single_json_run(self, entry, base_w_dir):
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
            for _ in range(self.top_k):
                if self.agent.lec_loop(prompt, self.lec_iter, self.lec_feedback_limit, self.comp_iter):
                    break
                self.agent.incr_k()
        

    def json_run(self, json_data, skip_completed: bool = False, skip_successful: bool = False):
        base_w_dir = self.agent.w_dir
        for entry in json_data:
            if not (skip_completed and self.check_completion(entry, base_w_dir)):
                self.single_json_run(entry, base_w_dir)
            
    def sequential_entrypoint(self, spath: str, llm: str, lang: str, json_data, skip_completed: bool = False, skip_successful: bool = False, w_dir: str = './', use_spec: bool = False, init_context: bool = False, supp_context: bool = False, temperature: float = None):
        self.set_agent(Agent(spath, llm, lang, init_context, supp_context, use_spec))
        self.agent.set_w_dir(w_dir)
        self.agent.set_model_temp(temperature)

        # Sanity test json file before starting anything
        #data = set_json_bounds(check_json(json_path), json_limit, start_from)
        self.json_run(json_data, skip_completed, skip_successful)
