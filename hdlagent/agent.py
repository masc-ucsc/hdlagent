import importlib
import markdown
import openai
from openai import OpenAI
import os
import octoai
from pathlib import Path
import re
import subprocess
import sys
import time
import vertexai
from vertexai.generative_models import *
import yaml

from hdlang import get_hdlang

from importlib import resources

from enum import Enum

class Role(Enum):
    INVALID     = 0
    DESIGN      = 1
    VALIDATION  = 2

def list_openai_models(warn: bool = True):
    if "OPENAI_API_KEY" in os.environ:
        try:
            response = openai.models.list()
        except Exception as e:
            if warn:
                print("Warning: could not connect to OpenAI, Skipping")
            return []

        ret_list = []
        for entry in response.data:
            ret_list.append(entry.id)

        # FIXME: Return only models that work with client.chat E.g: gpt-3.5-turbo-instruct fails
        return ret_list
    else:
        if warn:
            print("Warning: OPENAI_API_KEY not set")
        return []

def list_octoai_models(warn: bool = True):
    # Experimental list:
    exp_list = ['smaug-72b-chat', 'mixtral-8x22b', 'meta-llama-3-70b-instruct']
    if "OCTOAI_TOKEN" in os.environ:
        # NOTE: Even without internet, it returns a list
        l = octoai.chat.get_model_list()
        return l + exp_list
    else:
        if warn:
            print("OCTOAI_TOKEN not set")
        return []

# XXX - hacky until Vertex adds a list API
vertexai_models = ["gemini-1.0-pro-002", "gemini-1.0-pro-001", "gemini-1.0-pro", "gemini-1.5-pro-preview-0409"]

def list_vertexai_models():
    return vertexai_models

SAMBANOVA_API_URL = "https://fast-api.snova.ai/v1"
SAMBANOVA_API_KEY = os.environ.get("SAMBANOVA_API_KEY")

def list_sambanova_models(warn: bool = True):
    sambanova_models = ["llama3-8b", "llama3-70b", "llama3-405b"]
    if "SAMBANOVA_API_KEY" in os.environ:
        return sambanova_models
    else:
        if warn:
            print("Warning: SAMBANOVA_API_KEY not set")
        return []
    


def md_to_convo(md_file):
    with open(md_file, 'r') as f:
        lines = f.readlines()

    conversation    = []
    current_content = ""
    current_role    = ""
    system_content  = ""
    for line in lines:
        line = line.rstrip()
        if '**User:**' in line or '**Assistant:**' in line or '**System:**' in line:
            if current_content:
                if current_role == "system":
                    system_content += current_content.rstrip('\n')
                else:
                    conversation.append({"role": current_role, "content": current_content.rstrip('\n')})
                current_content = ""

            if '**User:**' in line:
                current_role = "user"
            elif '**Assistant:**' in line:
                current_role = "assistant"
            elif '**System:**' in line:
                current_role = "system"

            line_content = re.sub(r'\*\*(User:|Assistant:|System:)\*\*\s*', '', line)
            if line_content:
                current_content += line_content + "\n"
        else:
            current_content += line + "\n"

    if len(conversation) == 0:
        current_role = "system"

    if current_content:
        conversation.append({"role": current_role, "content": current_content.rstrip('\n')})

    if system_content:
        conversation.insert(0, {"role": "system", "content": system_content })

    return conversation

def get_name_from_interface(interface: str):
    # regex search for module name
    match = re.search(r'module\s+([^\s]+)\s*\(', interface)
    if match:
        return match.group(1).strip()
    print(f"Error: 'interface' {interface} does not declare module name properly, exiting...")
    exit()

class Agent:
    def __init__(self, spath: str, model: str, lang: str, init_context_files:list = [], use_supp_context: bool = False, use_spec: bool = False):

        self.script_dir = spath
        # Common responses
        with open(os.path.join(self.script_dir,"common/common.yaml"), 'r') as file:
            common = yaml.safe_load(file)

        # Set by Lang
        with open(os.path.join(self.script_dir, lang, lang + ".yaml"), 'r') as file:
            config = yaml.safe_load(file)

        self.hdlang = get_hdlang(lang)
        self.hdlang_verilog = get_hdlang("Verilog")  # code gen, interface.... is always verilog

        # Default prefixes and suffixes for queries
        self.responses = config['responses']
        self.responses.update(common['responses'])

        # Pre-loads long initial language context from user supplied and Lang default file(s)
        self.init_context_files = init_context_files
        self.initial_contexts   = []
        for init_context_file in init_context_files:
            if init_context_file == "default":
                for context in config['initial_contexts']:
                    file = os.path.join(self.script_dir, lang, context)
                    self.initial_contexts.extend(md_to_convo(file))
            else:
                self.initial_contexts.extend(md_to_convo(init_context_file))

        # For multi-model modes, set Role to determine functionality
        self.role = Role.INVALID

        # Supplemental contexts are loaded from yaml file, dictionary of {error: suggestion} pairs
        self.used_supp_context     = use_supp_context
        self.supplemental_contexts = {}
        if use_supp_context:
            self.supplemental_contexts = config['supplemental_contexts']

        # Compilation script for the target language
        self.compile_script = config['compile_script'] + " "

        # File extension of the target language
        self.file_ext = config['file_extension']

        # Determine the root directory of the project
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_script_dir)
        sys.path.append(project_root)

        # Error message check from compiler for target language
        module_name, func_name = config['error_check_function'].rsplit('.', 1)
        module = importlib.import_module(module_name)
        self.check_errors = getattr(module, func_name)

        # Formats compiled verilog into style that allows for Yosys' Logical Equivalence Checks
        module_name, func_name = config['reformat_verilog_function'].rsplit('.', 1)
        module = importlib.import_module(module_name)
        self.reformat_verilog = getattr(module, func_name)

        # Filters and reformats Yosys LEC feedback
        module_name, func_name = common['lec_filter_function'].rsplit('.', 1)
        module = importlib.import_module(module_name)
        self.lec_filter_function = getattr(module, func_name)

        # Name to be specified in chat completion API of target LLM
        self.chat_completion = None
        if model in list_octoai_models(False):
            self.chat_completion = self.octoai_chat_completion
            self.client          = octoai.client.Client()
        elif model in list_openai_models(False):
            self.chat_completion = self.openai_chat_completion
            self.client          = OpenAI()
        elif model in list_sambanova_models():
            self.chat_completion = self.sambanova_chat_completion
            self.client = OpenAI(
                base_url=SAMBANOVA_API_URL,
                api_key=SAMBANOVA_API_KEY,
                default_headers={
                    "Authorization": f"Basic {SAMBANOVA_API_KEY}",
                    "Content-Type": "application/json"
                }
            )
        elif model in list_vertexai_models():
            self.chat_completion = self.vertexai_chat_completion
            try:
                self.client          = GenerativeModel(model)
            except Exception as e:
                print(f"VertexAI failed with this error: {e}")
                print("WARNING: VertexAI uses a different API/authentitification. It requires this:")
                print("pip3 install --upgrade --user google-cloud-aiplatform")
                print("gcloud auth application-default login")
                exit(-2)

        elif ("OPENAI_API_KEY" not in os.environ) and ("OCTOAI_TOKEN" not in os.environ) and ("PROJECT_ID" not in os.environ):
            print("Please set either OPENAI_API_KEY or OCTOAI_TOKEN or PROJECT_ID environment variable(s) before continuing, exiting...")
            exit()
        if self.chat_completion is None:
            print(f"Error: {model} is an invalid model, please check --list_models for available LLM selection, exiting...")
            exit()
        self.model = model
        self.temp  = None

        # Resources used as a part of conversational flow and performance counters
        self.spec_conversation    = []
        self.compile_conversation = []
        self.compile_history_log  = []
        self.tb_conversation      = []
        self.short_context        = False
        self.name                 = ""
        self.interface            = ""
        self.io                   = []
        self.pipe_stages          = 0
        self.lec_script           = os.path.join(self.script_dir,"common/comb_lec")
        self.tb_script            = os.path.join(self.script_dir,"common/iverilog_tb")
        self.tb_compile_script    = os.path.join(self.script_dir,"common/iverilog_tb_compile")
        self.comp_n               = 0
        self.comp_f               = 0
        self.lec_n                = 0
        self.lec_f                = 0
        self.top_k                = 1
        self.prompt_tokens        = 0
        self.completion_tokens    = 0
        self.llm_query_time       = 0.0
        self.world_clock_time     = 0.0
        self.prev_test_cases      = -1

        # Where the resulting source files and logs will be managed and left
        self.w_dir       = './'
        self.spec_log    = "./logs/spec_log.md"
        self.compile_log = "./logs/compile_log.md"
        self.tb_log      = "./logs/tb_log.md"
        self.fail_log    = "./logs/fail.md"
        if use_spec:
            self.spec    = "spec.yaml"
        else:
            self.spec = None
        self.code        = "out" + self.file_ext
        self.verilog     = "out.v"
        self.tb          = "./tests/tb.v"
        self.gold        = None

    # Sets the role of the Agent and it's LLM for the given Handler set task
    # Changes initial context to Testbench based when given VALIDATION role
    #
    # Intended use: multi-LLM workflow
    def set_role(self, role: Role):
        self.role = role
        if role == Role.VALIDATION: # TODO - do this smarter
            self.initial_contexts.clear()
            with open(os.path.join(self.script_dir,"common/common.yaml"), 'r') as file:
                common = yaml.safe_load(file)
            for init_context_file in self.init_context_files:
                if init_context_file == "default":
                    for context in common['testbench_initial_contexts']:
                        file = os.path.join(self.script_dir, 'common', context)
                        self.initial_contexts.extend(md_to_convo(file))
                else:
                    self.initial_contexts.extend(md_to_convo(init_context_file))

    # Sets 'short_context' operational mode where only the last response is
    # maintained in the conversational history, useful for short context
    # windows
    #
    # Intended use: initialization of Agent
    def set_short_context(self):
        self.short_context = True

    # Top K count is set back to default of 1, only necessary when looping
    # over batch specs.
    #
    # Intended use: at the beginning of a new spec process
    def reset_k(self):
        self.top_k = 1

    # Top K count is incremented by 1, only necessary when looping
    # over batch specs.
    #
    # Intended use: if another k is going to start a conversation
    def incr_k(self):
        self.top_k += 1

    # Sets K value
    #
    # Intended use: benchmarking, fairness when connection crashes
    def set_k(self, k: int):
        if k < 1:
            print("Error: cannot set top_k less than 1, exiting...")
            exit()
        self.top_k = k

    # Sets the API query param 'temp' for the LLM, if such a param is
    # exposed in the API chat completion call
    #
    # Intended use: Whenever temperature of chat completions needs changing
    def set_model_temp(self, temp: float):
        self.temp = temp

    # The current run will assume this is the name of the target module
    # and will name files, perform queries, and define modules accordingly.
    #
    # Intended use: at the beginning of a new initial prompt submission
    def set_module_name(self, name: str):
        self.name = name
        self.update_paths()

    # The current run will assume this is the amount of pipeline stages
    # desired for the prompted RTL design, this will modify the LEC
    # method and queries accordingly.
    #
    # Intended use: at the beginning of a new initial prompt submission
    def set_pipeline_stages(self, pipe_stages: int):
        if (pipe_stages > 0):
            self.lec_script = os.path.join(self.script_dir,"common/temp_lec")
        else:
            self.lec_script = os.path.join(self.script_dir,"common/comb_lec")
        self.pipe_stages = pipe_stages

    # The current run will assume this is the interface of the target module,
    # styled in a Verilog-legal module declaration syntax.
    #
    # Intended use: at the beginning of a new initial prompt submission
    def set_interface(self, interface: str):
        # Remove unnecessary reg/wire type
        interface = interface.replace(' reg ', ' ').replace(' reg[', ' [')
        interface = interface.replace(' wire ', ' ').replace(' wire[', ' [')
        # Remove (legal) whitespaces from between brackets
        interface =  re.sub(r'\[\s*(.*?)\s*\]', lambda match: f"[{match.group(1).replace(' ', '')}]", interface)
        interface = interface.replace('\n', ' ')
        interface = interface.replace('endmodule', ' ')
        self.set_module_name(get_name_from_interface(interface))
        self.io = []
        # regex search for substring between '(' and ');'
        pattern = r"\((.*?)\);"
        match   = re.search(pattern, interface)
        if match:
            result = match.group(1)
            ports  = result.split(',')
            # io format is ['direction', 'signness', 'bitwidth', 'name']
            for port in ports:
                parts = port.split()
                if parts[0] not in ["input","output","inout"]:
                    print(f"Error: 'interface' {interface} contains invalid port direction, exiting...")
                    exit()
                if not parts[1] == "signed":    # empty string for unsigned
                    parts.insert(1, '')
                if not parts[2].startswith('['): # explicitly add bit wire length
                    parts.insert(2, '[0:0]')
                self.io.append(parts)
        else:
            print(f"Error: 'interface' {interface} is not valid Verilog-style module declaration, exiting...")
            exit()
        self.interface  = f"module {self.name}("
        self.interface += ','.join([' '.join(inner_list) for inner_list in self.io])
        self.interface += ");"
        self.interface = self.interface.replace('  ', ' ')

    # Resolves and returns w_dir as absolute path
    #
    # Intended use: read of w_dir
    def get_w_dir(self):
        return self.w_dir.resolve()

    # Creates and registers the 'working directory' for the current run as
    # so all output from the run including logs and produced source code
    # are left in this directory when the run is complete
    #
    # Intended use: right after the beginning of a new Agent's instantiation
    def set_w_dir(self, path: str, spec_path: str = None):
        # Now create the dir if it does not exist
        directory = Path(path) / ""
        if directory:
            os.makedirs(directory, exist_ok=True)
        self.w_dir = directory
        self.update_paths(spec_path)

    # Helper function to others that may change or set file names and paths.
    # Keeps all file pointers up to date
    #
    # Intended use: inside of 'set_w_dir' or 'set_module_name'
    def update_paths(self, spec_path: str = None):
        self.compile_log  = os.path.join(self.w_dir, "logs", self.name + "_compile_log.md")
        self.fail_log     = os.path.join(self.w_dir, "logs", self.name + "_fail.md")
        self.tb_log       = os.path.join(self.w_dir, "logs", f"{self.name}_{self.model}_tb_log.md")
        if self.spec is not None:
            self.spec_log = os.path.join(self.w_dir, "logs", self.name + "_spec_log.md")
            self.spec     = os.path.join(self.w_dir, self.name + "_spec.yaml")
            if self.name != "" and spec_path is not None:   # XXX - partition spec_path contents into submodules, when nested
                with open (spec_path, 'r') as path:
                    contents = path.read()
                    with open (self.spec, 'w') as file:     # this spec can be used in-place, produces no copy
                        file.write(contents + "\nin_directory: True")
        self.code         = os.path.join(self.w_dir, self.name + self.file_ext)
        self.verilog      = os.path.join(self.w_dir, self.name + ".v")
        self.tb           = os.path.join(self.w_dir, "tests", f"{self.name}_{self.model}_tb.v")

    # Helper function to check if the spec exists or not
    #
    # Intended use: when deciding whether to use the contents of a spec
    def spec_exists(self):
        return os.path.exists(self.spec)

    # Helper function that maintains a copy of the spec within the w_dir.
    #
    # Intended use: within read_spec()
    def resolve_spec_path(self, target_spec: str, in_directory: bool):
        w_dir = self.get_w_dir()            # auto-set w_dir to spec parent dir when unspecified
        if w_dir == Path('./').resolve():
            w_dir = os.path.dirname(os.path.abspath(target_spec))

        if in_directory:                    # w_dir is parent dir of spec
            self.set_w_dir(w_dir)
        else:                               # w_dir is set to child dir next to spec
            self.set_w_dir(os.path.join(w_dir, self.name), target_spec)
        
    # Helper function that extracts and reformats information from spec yaml file
    # to create initial prompt(s) for compilation loop and testbench
    # loop (if applicable). Sets interface and module name, and copies spec to 
    # w_dir if necessary.
    #
    # Intended use: before a generation/lec loop is started so the prompt can be reformatted and formalized
    def read_spec(self, target_spec: str = None):
        if target_spec is None:
            target_spec = self.spec

        if target_spec is None:
            print("Error: attempting to read spec in a run where it is not employed, exiting...")
            exit()
        with open(target_spec, 'r') as file:
            spec = yaml.safe_load(file)

        self.resolve_spec_path(target_spec, spec.get('in_directory') is True)
        if 'description' not in spec:
            print(f"Error: valid yaml 'description' key not found in {self.spec} file, exiting...")
            exit()
        if 'interface' not in spec:
            print(f"Error: valid yaml 'interface' key not found in {self.spec} file, exiting...")
            exit()
        self.set_interface(spec['interface'])
        return spec['description']

    # Registers the file path of the golden Verilog to be used for LEC
    # and dumps the contents into the file.
    #
    # Intended use: at the beginning of a new initial prompt submission
    def dump_gold(self, contents: str):
        verilog_lines = contents.split('\n')
        gold_contents = ""
        for line in verilog_lines:
            gold_contents += line.rstrip()
            gold_contents += "\n"
        gold_contents += "\n"
        self.gold      = os.path.join(self.w_dir, "tests", self.name + "_gold.v")
        os.makedirs(os.path.dirname(self.gold), exist_ok=True)
        with open (self.gold, "w") as file:
            file.write(gold_contents)
        self.check_gold(self.gold)

    # Helper function to prevent API charges in case gold Verilog
    # supplied is not valid or the file path is incorrect.
    #
    # Intended use: only when registering a gold module path
    def check_gold(self, file_path: str):
        # Helps users identify if their "golden" model has issues
        if not os.path.exists(file_path):
            print("Error: supplied Verilog file path {} invalid, exiting...".format(file_path))
            exit()
        script     = os.path.join(self.script_dir,"common/check_verilog") + " " + file_path # better way to do this?
        res        = subprocess.run([script], capture_output=True, shell=True)
        res_string = (str(res.stdout))[2:-1].replace("\\n", "\n")
        if "SUCCESS" not in res_string:
            print("Error: supplied Verilog file path {} did not pass Yosys compilation check, fix the following errors/warnings and try again".format(file_path))
            print(res_string)
            print("exiting...")
            exit()

    # Parses common.yaml file for the 'request_spec' strings to create the
    # contents of the 'spec initial instruction' tuple which are the 2 queries
    # given to the LLM that requests a spec be generated given an informal
    # request for the design.
    #
    # Intended use: to begin the spec generation process
    def get_spec_initial_instructions(self, prompt: str):
        description = (self.responses['request_spec_description']).format(prompt=prompt)
        interface   = self.responses['request_spec_interface']
        return (description, interface)

    # Parses language-specific *.yaml file for the 'give_instr' strings
    # to create the 'compile initial instruction' which is the first query given
    # to the LLM that specifies the desired behavior, name, and pipeline stages
    # of the RTL. This query is preceeded by the Initial Contexts
    # "I want a circuit that does this <def>, named <name>, write the RTL"
    #
    # Intended use: to begin the iterative part of the compilation conversation
    def get_compile_initial_instruction(self, prompt: str):
        pipe_stages = self.pipe_stages
        prefix = self.responses['comb_give_instr_prefix']
        output_count = 0    # XXX - fixme hacky, Special case for DSLX
        for wire in self.io:
            if wire[0] == "output":
                output_count += 1
        if (output_count == 1) and ('simple_give_instr_suffix' in self.responses):
            suffix = self.responses['simple_give_instr_suffix']
        else:
            suffix = self.responses['give_instr_suffix']
        if pipe_stages > 0:
            prefix = self.responses['pipe_give_instr_prefix']
        # Escape curly braces for string formatting
        prompt = prompt.replace("{", "{{").replace("}", "}}")
        return (prefix + prompt + suffix).format(interface=self.interface,name=self.name, pipe_stages=pipe_stages)

    # Parses language-specific *.yaml file for the 'compile_err' strings
    # to create the 'iteration instruction' which is the query sent to the
    # LLM after a compilation error was detected from its previous response.
    # "I got this compiler error: <err_mesg>, fix it"
    #
    # Intended use: inside compile conversation loop, after get_initial_instruction()
    def get_compile_iteration_instruction(self, compiler_output: str):
        clarification = self.responses['compile_err_prefix'] + compiler_output
        if self.used_supp_context:
            clarification += self.suggest_fix(compiler_output)
        return clarification

    def get_tb_initial_instruction(self, prompt: str):
        instruction = self.responses['request_testbench']
        return instruction.format(prompt=prompt, interface=self.interface) 

    def get_compile_tb_iteration_instruction(self, compiler_output: str):
        clarification = self.responses['compile_testbench_iteration']
        return clarification.format(compiler_output=compiler_output)

    def get_tb_iteration_instruction(self, feedback: str):
        clarification = self.responses['testbench_fail_iteration']
        with open (self.tb, 'r') as tb_file:
            testbench = tb_file.read()
        return clarification.format(testbench=testbench, feedback=feedback)

    # Parses language-specific *.yaml file for the 'lec_fail' strings
    # to create the 'lec fail instruction' which is the query sent to the
    # LLM after Yosys Logical Equivalence Check failed versus the golden model..
    # "Comparing your code to desired truth table here are mismatches: <lec_mesg>, fix it"
    #
    # Intended use: inside lec loop, after lec failure detected and more lec iterations available
    def get_lec_fail_instruction(self, test_fail_count: int, lec_output: str, lec_feedback_limit: int):
        if lec_feedback_limit == 0:
            return self.responses['no_feedback_lec_fail_suffix']
        lec_fail_prefix = self.responses['comb_lec_fail_prefix']
        if test_fail_count == -1:
            lec_fail_prefix = self.responses['bad_port_lec_fail_prefix']
        elif test_fail_count == -2:
            lec_fail_prefix = self.responses['latch_lec_fail_prefix']
        elif (test_fail_count < self.prev_test_cases) and (self.prev_test_cases > 0):
            lec_fail_prefix = self.responses['improve_comb_lec_fail_prefix']
        lec_fail_suffix = self.responses['lec_fail_suffix']
        if self.pipe_stages > 0:
            lec_fail_prefix = self.responses['pipe_lec_fail_prefix']
        return lec_fail_prefix.format(test_fail_count=test_fail_count, feedback=lec_output, lec_feedback_limit=min(lec_feedback_limit, test_fail_count)) + lec_fail_suffix

    def get_lec_bootstrap_instruction(self, prompt, test_fail_count, lec_feedback_limit, feedback):
        verilog = open(self.verilog,'r').read()
        if lec_feedback_limit == 0:
            return self.responses['no_feedback_lec_fail_bootstrap'].format(prompt=prompt, gold_verilog=verilog)
        form    = self.responses['comb_lec_fail_bootstrap']
        if test_fail_count == -1:
            form = self.responses['bad_port_lec_fail_prefix']
        elif test_fail_count == -2:
            form = self.responses['latch_lec_fail_prefix']
        return form.format(prompt=prompt, gold_verilog=verilog, test_fail_count=test_fail_count, feedback=feedback, lec_feedback_limit=min(int(lec_feedback_limit),test_fail_count))

    # Parses common.yaml file and returns formatted 'request_testbench' string
    # which asks for an assertion based testbench given the implementation prompt.
    #
    # Intended use: querying LLM for testbench generation
    def get_tb_initial_instruction(self, prompt: str):
        return (self.responses['request_testbench']).format(prompt=prompt, interface=self.interface)

    def vertexai_chat_completion(self, conversation, compile_convo: bool = False):
        contents  = []
        last_role = ''    # Gemini only supports alternating conversations between model/user
        for entry in self.compile_conversation:
            entry_content = entry['content']
            if entry['role'] == 'assistant':
                role = 'model'
            else:
                role = 'user'
            # enforce alternating conversation
            if role == last_role:
                prev_content  = str(contents[-1].parts)
                entry_content = prev_content + "\n" + entry_content
                contents.pop()

            last_role = role
            part      = [Part.from_text(entry_content)]
            contents.append(Content(role=role, parts=part))
        try:
            safety_settings = {
                vertexai.generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                vertexai.generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: vertexai.generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                vertexai.generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: vertexai.generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            }
            completion = self.client.generate_content(contents=contents, safety_settings=safety_settings)
        except Exception as e:
            print("Send failed due to ", e)
            exit(3)

        self.prompt_tokens     += completion.to_dict()['usage_metadata']['prompt_token_count']
        self.completion_tokens += completion.to_dict()['usage_metadata']['candidates_token_count']
        return completion.to_dict()['candidates'][0]['content']['parts'][0]['text']

    def octoai_chat_completion(self, conversation, compile_convo: bool = False):
        try:
            if self.temp is None:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=conversation,
                    max_tokens=2048,
                    presence_penalty=0,
                    top_p=0.9,
                )
            else:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=conversation,
                    max_tokens=2048,  # FIXME: automatic by model? 34B can do 16K, 70B only 4K
                    presence_penalty=0,
                    temperature=self.temp,
                    top_p=0.9,
                )
            self.prompt_tokens     += completion.dict()['usage']['prompt_tokens']
            self.completion_tokens += completion.dict()['usage']['completion_tokens']
            return completion.dict()['choices'][0]['message']['content']
        except Exception as e:
            print("octoai model failed: ", e)
            exit(3)

    def openai_chat_completion(self, conversation, compile_convo: bool = False):
        if self.temp is None:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=conversation,
            )
        else:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=conversation,
                temperature=self.temp,
            )
        self.prompt_tokens     += completion.usage.prompt_tokens
        self.completion_tokens += completion.usage.completion_tokens
        return completion.choices[0].message.content
    
    def sambanova_chat_completion(self, conversation, compile_convo: bool = False, **kwargs,):
        if self.temp is None:
            completion = self.client.chat.completions.create(
                model="llama3-405b",
                messages=conversation,
                # stream=True,
                **kwargs,
            )
        else:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=conversation,
                temperature=self.temp,
            )
        self.prompt_tokens     += completion.usage.prompt_tokens
        self.completion_tokens += completion.usage.completion_tokens
        return completion.choices[0].message.content

    # Primary interface between supported LLM's API and the Agent.
    # Send queries and returns their response(s), all while maintaining
    # the context by appending both query and response to the context history,
    # managed performance counters for token usage, time, etc...
    #
    # Intended use: primary interface with LLM
    def query_model(self, conversation, clarification: str, compile_convo: bool = False):
        # Add a clarification message, continuing the conversation
        conversation.append({
            'role': 'user',
            'content': clarification
        })
        print("---------------------------")
        print("**User:**\n" + clarification)


        query_start_time     = time.time()
        response             = self.chat_completion(conversation, compile_convo)
        self.llm_query_time += (time.time() - query_start_time)

        # Keep context to {initial_context, initial prompt, response} -> compile error
        if self.short_context and compile_convo:
            if len(conversation) == (len(self.initial_contexts) + 3):
                conversation.pop()
                conversation.pop()

        # Add the model's response to the messages list to keep the conversation context
        print("**Assistant:**\n" + response)

        if compile_convo:
            self.compile_history_log.append({'role': 'user', 'content' : clarification})
            self.compile_history_log.append({'role': 'assistant', 'content' : response})
            response = "```\n" + self.hdlang.extract_code(response, self.verilog) + "\n```"

        conversation.append({
            'role': 'assistant',
            'content': response
        })

        delay = 1
        time.sleep(delay) # wait to limit API rate
        self.world_clock_time += float(delay) # ignore injected delays in performance timing
        return response

    # Generates *_spec.yaml file that acts as the formal specification document for the
    # desired design. The spec is intended to be iterated upon by the human if the resulting
    # RTL is not good enough. If being generated will also be the new acting prompt upon the
    # first shot of the compilation loop flow.
    #
    # Intended use: before the compile loop flow is initiated to bootstrap a spec doc
    def generate_spec(self, prompt: str):
        self.reset_conversations()
        (description_req, interface_req) = self.get_spec_initial_instructions(prompt)
        spec_contents  = "description: |\n  \n"
        description    = self.query_model(self.spec_conversation, description_req)
        description_lines = description.split('\n')
        indented_lines = ["  " + line.lstrip() for line in description_lines]
        description    = '\n'.join(indented_lines)
        spec_contents += description
        spec_contents += "\ninterface: |\n  \n  "
        interface      = (self.hdlang_verilog.extract_code(self.query_model(self.spec_conversation, interface_req), self.verilog)).replace('\n','\n    ')
        spec_contents += interface

        # Ensure module name is always set
        if self.name == "":
            self.set_module_name(get_name_from_interface(interface))

        os.makedirs(os.path.dirname(self.spec), exist_ok=True)
        with open(self.spec, 'w') as file:
            file.write(spec_contents)
        self.dump_spec_conversation()

    # The entrypoint to the Supplemental Contexts through dictionary look-up.
    # Parses error-pattern-matching dictionary instantiated by language-specific *.yaml file
    # to give a generic example and fix of a known error message. This acts as a pseudo-RAG
    # to identify simple and consistent embeddings in compiler feedback.
    #
    # Intended use: in addition to 'compile_err' string when the Agent is using Supplemental Contexts
    def suggest_fix(self, err_msg: str):
        # Iterate over known compiler errs and check if there is a hit
        for known_error, suggested_fix in self.supplemental_contexts.items():
            if known_error in err_msg:
                return self.responses['suggest_prefix'] + suggested_fix
        # Say nothing if unrecognized err
        return ""

    # Executes the language-specific compiler script specified in the *.yaml
    # document, returning the compiler feedback and error if any were detected.
    #
    # Intended use: compile new code response from LLM that was dumped to file
    def test_code_compile(self):
        my_path = os.path.dirname(os.path.abspath(__file__))
        script  = self.compile_script + self.code
        if 'resources' in self.compile_script:
            script  = my_path + script
        res     = subprocess.run([script], capture_output=True, shell=True)
        errors  = self.check_errors(res)
        self.comp_n += 1
        if errors is not None:
            self.comp_f += 1
        return errors

    # Executes (temp | comb)_lec script to test LLM generated RTL versus
    # golden Verilog. *_lec script uses Yosys' SAT solver methods to find
    # counter-examples to disprove equivalence. The output of the script
    # will be 'SUCCESS' if no counter-example is found, or will be a (time-step)
    # truth table dump of the golden vs gate output values.
    # Note: lec_filter_function() is intended to reformat the output of Yosys LEC
    #
    # Intended use: for lec check after RTL has successfully compiled into Verilog
    def test_lec(self, gold: str = None, gate: str = None, lec_feedback_limit: int = -1):
        # ./*_lec <golden_verilog> <llm_verilog>
        if gold is None:
            if self.gold is None:
                print("Error: attemping LEC without setting gold path, exiting...")
                exit()
            gold = self.gold
        if gate is None:
            gate = self.verilog
        script      = self.lec_script + " " + gold + " " + gate
        res         = subprocess.run([script], capture_output=True, shell=True)
        res_string  = (str(res.stdout))[2:-1].replace("\\n","\n")
        self.lec_n += 1
        if "SUCCESS" not in res_string:
            self.lec_f += 1
            return self.lec_filter_function(res_string, lec_feedback_limit)
        return None

    # Executes the iVerilog tb compile script specified in the common.yaml
    # document, returning iVerilog errors if any were detected.
    #
    # Intended use: compile new tb response from LLM that was dumped to file
    def test_tb_compile(self):
        script     = self.tb_compile_script + " " + self.tb + " " + self.verilog
        res        = subprocess.run([script], capture_output=True, shell=True)
        res_string = (str(res.stderr)).replace("\\n","\n")
        self.comp_n += 1
        # This should probably be its own function chosen by yaml file, if we stop using iverilog
        if "error" in res_string:
            self.comp_f += 1
            return res_string
        return None

    # Creates Icarus Verilog testbench then executes it, carrying through the output
    # from either Icarus compiler errors or testbench results and feedback
    #
    # Intended use: for testbenching DUT after RTL has successfully compiled into Verilog
    def test_tb(self):
        script     = self.tb_script + " " + self.verilog + " " + self.tb
        res        = subprocess.run([script], capture_output=True, shell=True)
        res_string = (str(res.stdout))[2:-1].replace("\\n","\n")
        print(res_string)
        self.lec_n += 1
        if ("error" in res_string) or ("ERROR" in res_string):   # iverilog compile error
            self.lec_f += 1
            return res_string
        return None

    # Sets conversations to 'step 0', a state where no RTL generation queries have
    # been sent, only Initial Contexts if applied for compile conversation.
    #
    # Intended use: before starting a new Agent run
    def reset_conversations(self):
        self.compile_conversation = self.initial_contexts.copy()
        self.compile_history_log  = []
        self.spec_conversation    = []
        self.tb_conversation      = []

    # Clears all performance counters kept by Agent
    #
    # Intended use: before starting a new Agent run
    def reset_perf_counters(self):
        self.comp_n            = 0
        self.comp_f            = 0
        self.lec_n             = 0
        self.lec_f             = 0
        self.prompt_tokens     = 0
        self.completion_tokens = 0
        self.llm_query_time    = 0.0
        self.world_clock_time  = time.time()

    # The "inner loop" of the testbench generation process, checks for compile
    # errors while writing Verilog testbench to validate target design
    #
    # Intended use: inside of lec loop, depends on present generated Verilog
    def tb_compilation_loop(self, prompt: str, iterations: int = 2):
        current_query = self.get_tb_initial_instruction(prompt)
        for _ in range(iterations):
            self.dump_codeblock(self.query_model(self.tb_conversation, current_query, True), self.tb)
            compile_out = self.test_tb_compile()
            if compile_out is not None:
                current_query = self.get_compile_tb_iteration_instruction(compile_out)
            else:
                return True, None
        return False, compile_out 

    # The "outer loop" of the testbench generation process, which confirms
    # the tb compiled and the RTL exists, and runs them against one another.
    # Can also be used to direct an Agent to re-write the RTL based on tb feedback.
    # Return 'None' for the result indicates something failed, so the tb cannot not be run.
    #
    # Intended use: inside of lec loop, or to bootstrap a design verification
    def tb_loop(self, prompt: str, iterations: int = 1, designer: 'Agent' = None, code_compile_iterations: int = 1):
        if not os.path.exists(self.verilog):
            print(f"Error: attempting to run testbenching loop on non-existent {self.verilog}, exiting...")
            exit()

        if designer is None:
            designer = self

        # Create only one version of testbench, make sure it compiles
        tb_compiled, failure_reason = self.tb_compilation_loop(prompt, code_compile_iterations)  # same iterations as code compile
        if not tb_compiled:
            self.dump_failure(failure_reason, self.tb_conversation)
            self.dump_tb_conversation()
            return None, failure_reason     # tb never compiled

        code_compiled: bool = None
        for i in range(iterations):
            failure_reason = self.test_tb()
            if failure_reason is None:
                self.success_message(self.tb_conversation)
                self.dump_tb_conversation()
                if code_compiled is not None:
                    designer.dump_compile_conversation()
                return True, None
            elif i != iterations - 1:
                prompt = self.get_tb_iteration_instruction(failure_reason)
                code_compiled, failure_reason = designer.code_compilation_loop(prompt, 1, code_compile_iterations)
                if not code_compiled:
                    designer.dump_failure(failure_reason, designer.compile_history_log)
                    self.dump_failure(failure_reason, self.tb_conversation)
                    self.dump_tb_conversation()
                    if code_compiled is not None:
                        designer.dump_compile_conversation()
                    return None, failure_reason     # new version of code failed to compile
                else:
                    designer.reformat_verilog(designer.name, designer.gold, designer.verilog, designer.io)

        self.dump_failure(failure_reason, self.tb_conversation)
        self.dump_tb_conversation()
        if code_compiled is not None:
            designer.dump_compile_conversation()
        return False, failure_reason

    # The "inner loop" of the RTL generation process, attempts to iteratively
    # write compiling code in the target language through use of feedback and
    # supplemental context if enabled
    #
    # Intended use: inside of the lec loop
    def code_compilation_loop(self, prompt: str, lec_iteration: int = 0, iterations: int = 1):
        if lec_iteration == 0:
            current_query = self.get_compile_initial_instruction(prompt)
        else:
            current_query = prompt
        for _ in range(iterations):
            self.dump_codeblock(self.query_model(self.compile_conversation, current_query, True), self.code)
            compile_out = self.test_code_compile()
            if compile_out is not None:
                current_query = self.get_compile_iteration_instruction(compile_out)
            else:
                return True, None
        return False, compile_out

    # Control wrapper for code_compilation_loop(), user-controlled RTL generation
    # defined by a spec in a target language. Generates the code for a single module,
    # and dumps the conversation.
    #
    # Intended use: user facing RTL generation
    def spec_run_loop(self, prompt: str, iterations: int = 1, continued: bool = False):
        if not continued:   # Maintain conversation history when iterating over design
            self.reset_conversations()
            self.reset_perf_counters()

        return self.finish_run(self.code_compilation_loop(prompt, 0, iterations)[1])

    # Rolls back the conversation to the LLM codeblock response which failed the least amount of
    # testcases. This is to avoid regression and save on context token usage.
    #
    # Intended use: experimental LLM LEC steering
    def lec_regression_filter(self, test_fail_count: int, lec_feedback_limit: int):
        next_limit = lec_feedback_limit
        if test_fail_count >= self.prev_test_cases:
            # Remove current answer and query from conversation history
            self.compile_conversation.pop()
            if len(self.compile_conversation) > 1:  # --update condition has codeblock in first query
                self.compile_conversation.pop()
            # Writeback previous codeblock
            if len(self.compile_conversation) > 0:
                self.dump_codeblock(self.compile_conversation[-1]["content"], self.verilog)
            if len(self.compile_conversation) == 1:  # shrink feedback in codeblock in first query
                self.compile_conversation.pop()
            if lec_feedback_limit > 1:
                next_limit = min(lec_feedback_limit - 1, test_fail_count)
            elif lec_feedback_limit != 0:
                next_limit = min(8, test_fail_count) # sets LFL default upper range
        else:
            self.prev_test_cases = test_fail_count
        return next_limit

    # Main generation and validation loop for benchmarking. Inner loop attempts complations
    # and outer loop checks generated RTL versus supplied 'gold' Verilog for logical equivalence
    #
    # Intended use: benchmarking effectiveness of the agent
    def lec_loop(self, prompt: str, lec_iterations: int = 1, lec_feedback_limit: int = -1, compile_iterations: int = 1, update: bool = False, testbench_iterations: int = 0):
        self.reset_conversations()
        self.reset_perf_counters()
        self.prev_test_cases   = float('inf')
        original_prompt = prompt
        for i in range(lec_iterations):
            if (update) and (len(self.compile_conversation) == 0):
                if self.test_code_compile() is None:    # Only try to update if code already compiles and LEC returns valid feedback
                    gold, gate = self.reformat_verilog(self.name, self.gold, self.verilog, self.io)
                    lec_out    = self.test_lec(gold, gate, lec_feedback_limit)
                    test_fail_count, failure_reason = lec_out.split('\n', 1)
                    test_fail_count      = int(test_fail_count)
                    self.prev_test_cases = test_fail_count
                    self.lec_f           -= 1
                    self.lec_n           -= 1  # preliminary checks dont count
                    if test_fail_count > 0:
                        prompt = self.get_lec_bootstrap_instruction(original_prompt, test_fail_count, lec_feedback_limit, failure_reason)
            compiled, failure_reason = self.code_compilation_loop(prompt, i, compile_iterations)
            if compiled:
                # Reformat is free to modify both the gold and the gate
                gold, gate = self.reformat_verilog(self.name, self.gold, self.verilog, self.io)
                lec_out    = self.test_lec(gold, gate, lec_feedback_limit)
                if lec_out is not None:
                    test_fail_count, failure_reason = lec_out.split('\n', 1)
                    test_fail_count = int(test_fail_count)
                    if i != lec_iterations - 1:
                        prev_lec_feedback_limit = lec_feedback_limit
                        lec_feedback_limit      = self.lec_regression_filter(test_fail_count, lec_feedback_limit)
                        lec_out                 = self.test_lec(gold, gate, lec_feedback_limit) # re-do LEC after popping conversation
                        _, failure_reason       = lec_out.split('\n', 1)
                        self.lec_f             -= 1
                        self.lec_n             -= 1  # preliminary checks dont count
                        prompt = self.get_lec_fail_instruction(self.prev_test_cases, failure_reason, lec_feedback_limit)
                else:
                    return self.finish_run()
            else:
                return self.finish_run(failure_reason)
        return self.finish_run(failure_reason)

    # Helper function to handle results and logs of compile based runs
    #
    # Intended use: after test_lec() is called
    def finish_run(self, failure_reason: str = None):
        success = failure_reason is not None
        if success:
            self.dump_failure(failure_reason, self.compile_history_log)
        else:
            self.success_message(self.compile_history_log)

        self.dump_compile_conversation()
        return success

    # Helper function that reads and formats an LLM conversation
    # into a Markdown string
    #
    # Intended use: when dumping a conversation to a *_log.md file
    def format_conversation(self, conversation, start_idx: int = 0):
        md_content = ""
        for entry in conversation[start_idx:]:
            if 'role' in entry and 'content' in entry:
                role        = entry['role'].capitalize()
                content     = entry['content']
                md_content += f"**{role}:**\n{content}\n\n"
        return md_content

    def dump_spec_conversation(self):
        md_content  = "# Spec Conversation\n\n"
        md_content += self.format_conversation(self.spec_conversation)
        os.makedirs(os.path.dirname(self.spec_log), exist_ok=True)
        with open(self.spec_log, 'w') as md_file:
            md_file.write(md_content)

    def dump_compile_conversation(self):
        start_idx  = 0
        md_content = "# Compile Conversation\n\n"
        if self.initial_contexts:
            md_content += "**System:** Initial contexts were appended to this conversation\n\n"
            start_idx   = len(self.initial_contexts)
        md_content += self.format_conversation(self.compile_history_log, 0)
        md_content += self.report_statistics()
        os.makedirs(os.path.dirname(self.compile_log), exist_ok=True)
        with open(self.compile_log, 'w') as md_file:
            md_file.write(md_content)

    def dump_tb_conversation(self):
        md_content  = "# Testbench Conversation\n\n"
        md_content += self.format_conversation(self.tb_conversation)
        md_content += self.report_statistics()
        os.makedirs(os.path.dirname(self.tb_log), exist_ok=True)
        with open(self.tb_log, 'w') as md_file:
            md_file.write(md_content)

    # Writes reason for failure to fail log
    #
    # Intended use: when *_loop fails, mainly for benchmarking
    def dump_failure(self, reason: str, conversation):
        self.failure_message(conversation)
        os.makedirs(os.path.dirname(self.fail_log), exist_ok=True)
        with open(self.fail_log, "w") as md_file:
            md_file.write("Reason for failure:\n" + reason)

    def dump_codeblock(self, text: str, filepath: str):
        isolated_code = text.replace('```','')
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as file:
            file.write(isolated_code)

    def failure_message(self, conversation):
        msg = f"Failure!\nAfter {self.comp_f} compilations failures and {self.lec_f} testing failures, your desired circuit could not be faithfully generated!\nSee {self.fail_log} for final failure reason."
        print("**System:** "+ msg)
        conversation.append({"role":"System", "content":msg})

    def success_message(self, conversation):
        msg = f"Success!\nAfter {self.comp_f} compilation failures and {self.lec_f} testing failures, your desired circuit was generated!"
        print("**System:** "+ msg)
        conversation.append({"role":"System", "content":msg})

    def report_statistics(self):
        self.world_clock_time = time.time() - self.world_clock_time
        stats = f"\nRESULTS : {self.model} : {self.name} : {self.comp_n} : {self.comp_f} : {self.lec_n} : {self.lec_f} : {self.top_k} : {self.prompt_tokens} : {self.completion_tokens} : {self.world_clock_time} : {self.llm_query_time}"
        return stats
