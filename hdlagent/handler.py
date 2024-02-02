from agent import Agent
import json
import os

class Handler:
    def __init__(self, agent: Agent = None):
        self.agent = agent

        self.comp_iter = 4
        self.lec_iter  = 1
        self.tb_iter   = 1

    def set_agent(self, agent: Agent):
        self.agent = agent

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

    def json_run(self, json_file: str, limit: int = -1, use_spec: bool = False):
        if json_file is None:
            print("Error: no json file registered, exiting...")
            exit()

        with open(json_file, 'r') as file:
            data = json.load(file)['verilog_problems']

        if limit == -1 or limit > len(data):
            limit = len(data)

        for i in range(limit):
            entry        = data[i]
            name         = entry['name']
            prompt       = entry['instruction']
            gold_verilog = entry['response']
            pipe_stages  = int(entry['pipeline_stages'])

            self.agent.set_module_name(name)
            self.agent.set_pipeline_stages(pipe_stages)

            if use_spec:
                if not self.agent.spec_exists():
                    self.agent.generate_spec(prompt)
                prompt = self.agent.read_spec()

            self.agent.dump_gold(gold_verilog)
            self.agent.lec_loop(prompt, self.lec_iter, self.comp_iter)
            
    def entrypoint(self, spath: str, llm: str, lang: str, json_path: str = None, json_limit: int = -1, w_dir: str = './', use_spec: bool = False, init_context: bool = False, supp_context: bool = False):
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
                        json.load(file)
                except json.JSONDecodeError:
                    print("Error: json_path supplied is not a valid .json file, exiting...")
                    exit()
                self.json_run(json_path, json_limit, use_spec)
