import os
import re
import subprocess

def custom_check_errors(compiler_output):
    res_string = (str(compiler_output.stderr))[2:-1].replace("\\n", "\n")
    if ("Error:" not in res_string) and ("failure" not in res_string):
        return None
    return res_string

def custom_reformat_verilog(name: str, ref_file: str, in_file: str, io_list):
    outputs = []
    inputs  = []

    for io in io_list:
        #print(io)
        if io[0] == "output":
            outputs.append(io)
        elif io[0] == "input":
            inputs.append(io)
        else:
            print("Error: unknown signal found, exiting...")
            exit()
    
    with open(in_file, 'r') as file:
        in_file_content = file.read()

    if len(outputs) == 1:
        output_name = outputs[0][3]
        in_file_content = in_file_content.replace("out\n", output_name + "\n")
        in_file_content = in_file_content.replace("out;", output_name + ";")
        in_file_content = in_file_content.replace(" out ", " " + output_name + " ")
    else:
        # Replace modules header 'out' with outputs directly
        output_declarations = ""
        for output in outputs:
            output_declarations += ",\n\t" + output[0] + " " + output[1] + " " + output[2] + " " + output[3]
        in_file_content = in_file_content.replace(",\n\tout\n", output_declarations)
        # Remove in-module 'out' definition and declarations of wires that should be outputs
        in_file_lines = in_file_content.splitlines()
        in_file_lines = [line for line in in_file_lines if 'output wire' not in line]
        for name in outputs:    # This is bad, O(n^2)
            if name[2] == "[0:0]":
                bad_line = "wire " + name[3] + ";"
            else:
                bad_line = "wire " + name[2] + " " + name[3] + ";"
            in_file_lines = [line for line in in_file_lines if bad_line not in line]
        # Remove last 2 lines past the assignments of the outputs
        if 'assign out ' in in_file_lines[-2]:
            if 'assign out = tuple_' in in_file_lines[-2]:
                in_file_lines[-3] = ""
            in_file_lines[-2] = ""
        in_file_content = '\n'.join(in_file_lines)

    with open(in_file, 'w') as file:
        file.write(in_file_content)
    return (ref_file, in_file)
