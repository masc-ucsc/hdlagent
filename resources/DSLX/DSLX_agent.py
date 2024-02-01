import os
import re
import subprocess

def custom_check_errors(compiler_output):
    res_string = (str(compiler_output.stderr))[2:-1].replace("\\n", "\n")
    if ("Error:" not in res_string) and ("failure" not in res_string):
        return ""
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
    file.close()

    if len(outputs) == 1:
        output_name = outputs[0][2]
        in_file_content = in_file_content.replace("out\n", output_name + "\n")
        in_file_content = in_file_content.replace("out;", output_name + ";")
        in_file_content = in_file_content.replace(" out ", " " + output_name + " ")
    else:
        # Replace modules header 'out' with outputs directly
        output_declarations = ""
        for output in outputs:
            output_declarations += ",\n\t" + output[0] + " " + output[1] + " " + output[2]
        in_file_content = in_file_content.replace(",\n\tout\n", output_declarations)
        # Remove in-module 'out' definition and declarations of wires that should be outputs
        in_file_lines = in_file_content.splitlines()
        in_file_lines = [line for line in in_file_lines if 'output wire' not in line]
        for name in outputs:    # This is bad, O(n^2)
            if name[1] == "[0:0]":
                bad_line = "wire " + name[2] + ";"
            else:
                bad_line = "wire " + name[1] + " " + name[2] + ";"
            in_file_lines = [line for line in in_file_lines if bad_line not in line]
            
        #in_file_lines_next = []
        #for line in in_file_lines:
        #    in_file_lines_next.append(line)
        #    if '\toutput wire' in line:
        #        line = ""
        #        break
        # Remove last 2 lines past the assignments of the outputs
        if 'assign out ' in in_file_lines[-2]:
            if 'assign out = tuple_' in in_file_lines[-2]:
                in_file_lines[-3] = ""
            in_file_lines[-2] = ""
    with open(in_file, 'w') as file:
        for line in in_file_lines:
            file.write(line + '\n')
    file.close()
    return (ref_file, in_file)


def old_custom_reformat_verilog(name: str, ref_file: str, in_file: str, io_list):
    #pid = os.getpid()   # makes the tmp gate file have a unique name
    with open(in_file, 'r') as file:
        lines = file.readlines()
    # Isolate DSLX generated Verilog module declaration and output assignment
    wrapper: str = ""
    io_count = 0
    for line in lines:
        io_count = io_count + 1
        wrapper  = wrapper + line
        if ");" in line:    # capture module declaration
            break
    assign_out = lines[-2]; # always second to last line
    if "{" not in assign_out:
        assign = assign_out.split("=")[0]
        out    = lines[-3].split("=")[1]
        assign_out = assign + "=" + out
    for i in range (io_count, (2*io_count) - 2):
        wrapper = wrapper + lines[i]
    file.close()

    with open(ref_file, 'r') as file:
        lines = file.readlines()
    module_declaration = []
    for line in lines:
        if ");" in line:
            break
        module_declaration.append(line.replace('wire',''))
    #print(module_declaration)
    in_declaration  = []
    out_declaration = []
    for line in module_declaration:
        if " output " in line:
            bus = line.split("//")[0]  # Strip off comments
            if " output " in bus:
                bus = bus.split(" output ")[1].strip().replace(",", "").replace('reg','')
                out_declaration.append(bus.split(" ")[-1])
                wrapper += "        wire " + bus + ";\n"
        elif " input " in line:
            bus = line.split("//")[0]
            if " input " in bus:
                bus = bus.split(" input ")[1].strip().replace(",", "")
                in_declaration.append(bus.split(" ")[-1])
    #print(lines[0])
    lines[0] = lines[0].replace("module ", "module _")
    wrapper = wrapper + "        " + lines[0].replace("module ","").replace("("," internal_rtl (")
    for bus in in_declaration:
            wrapper = wrapper + "        ." + bus + "(" + bus + "),\n"
    for bus in out_declaration:
        if bus == out_declaration[-1]:
            wrapper = wrapper + "        ." + bus + "(" + bus + "));\n"
        else:
            wrapper = wrapper + "        ." + bus + "(" + bus + "),\n"
    # sometimes the io is awkwardly renamed, but very similiarly, we replace similiar names
    # turn assign out members into list
    if "{" not in assign_out:
        outputs_list = [] # TODO: figure out literal outputs
    else:
        outputs_list = re.search(r'\{(.*?)\}', assign_out).group(1).split(',')
    #print(outputs_list)
    fixed_outputs = []
    idx = 0
    if (len(outputs_list) == 0)  or (len(outputs_list) == 1):
        assign_out = "assign out = " + out_declaration[0] + ";\n";
    elif len(out_declaration) == len(outputs_list):
        for output in outputs_list:     # dslx verilog outputs
            if out_declaration[idx] != output:
                if out_declaration[idx] in output:
                    assign_out = assign_out.replace(output, out_declaration[idx])
            idx = idx + 1
    else:
        for output in outputs_list: #dslx verilog outputs
            for bus in out_declaration: # json verilog outputs
                if bus in output:
                    assign_out = assign_out.replace(output, bus)
    #print(assign_out)
    wrapper = wrapper + assign_out + "\nendmodule\n"
    for line in lines:
        wrapper = wrapper + line
    file.close()
    out_file = "tmp_" + name + ".v"
    with open(out_file, 'w') as file:
        file.write(wrapper)
    file.close()
    # Reformatted gold
    return (out_file, in_file)
