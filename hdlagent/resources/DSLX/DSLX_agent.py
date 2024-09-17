import re

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

    #if len(inputs) == 1:
    #    input_name = inputs[0][3]
        # Get name of single input
    #    in_file_input_name = in_file_content.splitlines()[1].replace('\t','').replace(',','')
    #    if input_name != in_file_input_name:
    #        in_file_content = in_file_content.replace()

    if len(outputs) == 1:
        output_name = outputs[0][3]
        # Rename all lines that may have the output_name as a local wire
        in_file_content = in_file_content.replace(f"{output_name}\n", f"{output_name}_w\n")
        in_file_content = in_file_content.replace(f"{output_name};", f"{output_name}_w;")
        in_file_content = in_file_content.replace("{" + output_name + "};", "{" + output_name + "_w};")
        in_file_content = in_file_content.replace(f" {output_name} ", f" {output_name}_w ")
        in_file_content = in_file_content.replace(f"({output_name});", f"({output_name}_w);")
        # Rename output as desired output_name
        in_file_content = in_file_content.replace("out\n", output_name + "\n")
        in_file_content = in_file_content.replace("out;", output_name + ";")
        in_file_content = in_file_content.replace(" out ", " " + output_name + " ")
        in_file_content = in_file_content.replace("(out);", "(" + output_name + ");")
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
                del in_file_lines[-3]
            del in_file_lines[-2]
        in_file_content = '\n'.join(in_file_lines)
        # Check if last remaining lines are superstrings of the outputs names
        last_assigns = in_file_lines[-2: -(2 + len(outputs)): -1]
        # Starting with longest entries prevent overlapping name matching, eg: 'or' and 'xor'
        outputs.sort(key=lambda x: len(x[3]), reverse=True)
        for assign in last_assigns:
            pattern = r'assign\s+(\w+)\s+='
            match = re.search(pattern, assign)
            if match:
                assign_name = match.group(1)
                for output in outputs:
                    output_name = output[3]
                    if output_name == assign_name:
                        break
                    if output_name in assign_name:  # Output names as substrings are replaced
                        new_assign      = assign.replace(assign_name, output_name)
                        in_file_content = in_file_content.replace(assign, new_assign)

    with open(in_file, 'w') as file:
        file.write(in_file_content)
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
    in_file = "../../init_context_tests/gpt-4-1106_o2_context4_hdleval/ripple_carry_adder_8bit/ripple_carry_adder_8bit.v"
    io_list = get_interface("module ripple_carry_adder_8bit(input  [7:0] a,input  [7:0] b,input  [0:0] cin,output  [7:0] sum,output  [0:0] cout);")
    custom_reformat_verilog(name, ref_file, in_file, io_list)

if __name__ == "__main__":
    main()
