import os
import re
import subprocess

def custom_check_errors(compiler_output):
    res_string = (str(compiler_output.stderr))[2:-1].replace("\\n", "\n")
    if "Error:" in res_string:
        return res_string
    else:
        return None


def custom_reformat_verilog(name: str, ref_file: str, in_file: str, io_list):
    with open(in_file) as file:
        lines = file.readlines()
    # Remove unnecessary clk and rst signals
    if ('clk' not in io_list) and ('    input clk;\n' in lines):
        lines[4] = lines[4].replace("(clk, ", "(").replace("(clk)", "()")
        lines.pop(5)
    with open(in_file, 'w') as f:
        for line in lines:
            f.write(line)
    return (ref_file, in_file)
