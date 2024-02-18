from agent import Agent
import json
import os

class Handler:
    def __init__(self, agent: Agent = None):
        self.agent = agent

        self.comp_iter          = 4
        self.lec_iter           = 1
        self.tb_iter            = 1
        self.lec_feedback_limit = 1

        self.id                 = None

    # Assign one agent to handler
    #
    # Intended use: Initialization of Handler
    def set_agent(self, agent: Agent):
        self.agent = agent

    # Parallel processing Handler enumeration
    #
    # Intended use: testing
    def set_id(self, num: int):
        self.id = num

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

    # Limits how many testcases can be given back from Yosys LEC for iterative feedback
    #
    # Intended use: before a new run
    def set_lec_feedback_limit(self, n: int):
        self.lec_feedback_limit = n

    def single_json_run(self, entry, base_w_dir):
            self.agent.set_interface(entry['interface'])
            self.agent.set_pipeline_stages(int(entry['pipeline_stages']))
            self.agent.set_w_dir(os.path.join(base_w_dir, self.agent.name))

            prompt = entry['instruction']
            if self.agent.spec is not None:
                if not self.agent.spec_exists():
                    self.agent.generate_spec(prompt)
                prompt = self.agent.read_spec()

            self.agent.dump_gold(entry['response'])
            self.agent.lec_loop(prompt, self.lec_iter, self.lec_feedback_limit, self.comp_iter)
        

    def json_run(self, json_data, limit: int = -1, start_from: str = None):
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

        base_w_dir = self.agent.w_dir
        for i in range(start_idx, limit):
            self.single_json_run(data[i], base_w_dir)
            
    def sequential_entrypoint(self, spath: str, llm: str, lang: str, json_path: str = None, json_limit: int = -1, start_from: str = None, w_dir: str = './', use_spec: bool = False, init_context: bool = False, supp_context: bool = False):
        self.set_agent(Agent(spath, llm, lang, init_context, supp_context, use_spec))
        self.agent.set_w_dir(w_dir)

        # Sanity test json file before starting anything
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
                self.json_run(data, json_limit, start_from)
