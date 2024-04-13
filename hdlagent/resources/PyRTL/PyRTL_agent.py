import os
import re
import subprocess

def custom_check_errors(compiler_output):
    res_string = (str(compiler_output.stderr))[2:-1].replace("\\n", "\n").replace('\\','')
    if "Error:" in res_string:
        return res_string
    else:
        return None


def custom_reformat_verilog(name: str, ref_file: str, in_file: str, io_list):
    with open(in_file) as file:
        lines = file.readlines()
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
    # either remove or rename clk and rst signals
    pop_idx = 6
    if clock_name !=  "clk":
        if clock_name is None:  # remove
            lines[4] = lines[4].replace("(clk, ", "(").replace("(clk)", "()")
            pop_idx = 5
            lines.pop(pop_idx)
        else:                   # rename
            rename_clock = True
    if reset_name != "rst":
        if (reset_name is None) and ("input rst;" in lines[pop_idx]):  # remove
        # (clk, rst) , (rst), (clk, rst, xxx), (rst, xxx) -> ", rst)" , "(rst)" , " rst," , "(rst, "
            lines[4] = lines[4].replace(", rst) ", ")").replace("(rst)", "()").replace(" rst,", "").replace("(rst, ", "(")
            lines.pop(pop_idx)
        else:                   # rename
            rename_reset = True
    newlines = []
    for line in lines:
        if rename_clock and ("clk" in line):
            line = line.replace("clk", clock_name)
        if rename_reset and ("rst" in line):
            line = line.replace("rst", reset_name)
        newlines.append(line)
    with open(in_file, 'w') as f:
        for line in lines:
            f.write(line)
    return (ref_file, in_file)

def get_interface(interface: str):
        # Remove unnecessary reg type
        interface = interface.replace(' reg ', ' ').replace(' reg[', ' [')
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
    in_file = "fmadd_pyrtl.v"
    io_list = get_interface("module fmadd( input [31:0] instruction, output reg [4:0] rd, output reg [31:0] result, output reg err);")
    custom_reformat_verilog(name, ref_file, in_file, io_list)

if __name__ == "__main__":
    main()
