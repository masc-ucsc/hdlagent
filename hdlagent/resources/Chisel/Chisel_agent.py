import os
import re
import subprocess

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
        return ""


def custom_reformat_verilog(name: str, ref_file: str, in_file: str, io_list):
    with open(in_file) as file:
        lines = file.readlines()
    file.close()
    # Populate these!
    possible_clock_names = ["clk","Clk","clock","Clock"]
    possible_reset_names = ["rst","Rst","reset","Reset"]
    clock_name   = None
    rename_clock = False
    reset_name   = None
    rename_reset = False
    for name in possible_clock_names:
        if name in io_list:
            clock_name = name
            break
    for name in possible_reset_names:
        if name in io_list:
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
    newlines  = []
    for line in lines:
        if "io_" in line:       # remove 'io_' prepend from module io names
            newlines.append(line.replace("io_", ""))
        elif rename_clock and clock_name in line:
            newlines.append(line.replace("clock", clock_name))
        elif rename_reset and reset_name in line:
            newlines.append(line.replace("reset", reset_name))
        else:
            newlines.append(line)
    with open(in_file, 'w') as f:
        for line in newlines:
            f.write(line)
    f.close()
    # Reformatted gate inplace
    return (ref_file, in_file)
