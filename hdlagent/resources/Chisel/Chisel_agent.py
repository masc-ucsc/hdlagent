import re

def custom_check_errors(compiler_output):
    res_string = (str(compiler_output.stdout))[2:-1].replace("\\n", "\n")
    err_string = (str(compiler_output.stderr))[2:-1].replace("\\n", "\n")
    firrtl_exception = "Exception" in err_string
    program_compiled = ("error" not in res_string) and (firrtl_exception == False)
    if program_compiled == False:
        newlines = []
        if (firrtl_exception == False):
            # Isolate the error message from the SBT info
            for line in res_string.splitlines():
                if "[error]" in line:
                    newlines.append(line)
            res_string = '\n'.join(newlines[:-2])
        else:
            # Tell LLM about exception
            for line in res_string.splitlines():
                if "Error" in line:
                    newlines.append(line)
            newlines.append(err_string)
            res_string = '\n'.join(newlines)
        return res_string
    else:
        return None


def custom_reformat_verilog(name: str, ref_file: str, in_file: str, io_list):
    with open(in_file) as file:
        contents = file.read()
    # Remove randomization block
    contents = re.sub(r"// Register and memory initialization.*?(?=endmodule)", "", contents, flags=re.DOTALL)
    lines = contents.splitlines()
    # Populate these!
    possible_clock_names = ["clk","Clk","clock","Clock"]
    possible_reset_names = ["rst","Rst","reset","Reset","aresetn"]
    clock_name   = None
    rename_clock = False
    reset_name   = None
    rename_reset = False
    for name in possible_clock_names:
        for io in io_list:
            if name in io:
                clock_name = name
                break
    for name in possible_reset_names:
        for io in io_list:
            if name in io:
                reset_name = name
                break
    # either remove or rename clock and reset signals
    pop_idx = 2
    if clock_name != "clock":
        if clock_name is None:  # remove
            pop_idx = 1
            lines.pop(pop_idx)
        else:                   # rename
            rename_clock = True
    if reset_name != "reset":
        if reset_name is None:  # remove
            lines.pop(pop_idx)
        else:                   # rename
            rename_reset = True
    newlines = []
    for line in lines:
        if "io_" in line:       # remove 'io_' prepend from module io names
            for io in io_list:
                chisel_name = "io_" + io[3]
                if chisel_name in line:
                    line = line.replace(chisel_name, io[3])
        if rename_clock and ("clock" in line):
            line = line.replace("clock", clock_name)
        if rename_reset and ("reset" in line):
            line = line.replace("reset", reset_name)
        newlines.append(line)
    if 'endmodule' not in newlines[-1]:
        newlines.append('endmodule')
    with open(in_file, 'w') as f:
        for line in newlines:
            f.write(line + '\n')
    # Reformatted gate inplace
    return (ref_file, in_file)

def get_interface(interface: str):
        # Remove unnecessary reg/wire type
        interface = interface.replace(' reg ', ' ').replace(' reg[', ' [')
        interface = interface.replace(' wire ', ' ').replace(' wire[', ' [')
        # Remove (legal) whitespaces from between brackets
        interface =  re.sub(r'\[\s*(.*?)\s*\]', lambda match: f"[{match.group(1).replace(' ', '')}]", interface)
        interface = interface.replace('\n', ' ')
        self_io = []
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
                self_io.append(parts)
        return self_io

def main():
    name = ""
    ref_file = ""
    in_file = "one_hot_state_register.v"
    io_list = get_interface("module one_hot_state_register(input  [0:0] clk,input  [0:0] rst,input  [0:0] enable,input  [2:0] state_in,output  [2:0] state_out,input  [0:0] scan_enable,input  [0:0] scan_in,output  [0:0] scan_out);")
    custom_reformat_verilog(name, ref_file, in_file, io_list)

if __name__ == "__main__":
    main()
