import re

def comment_filter_function(lec_feedback: str, limit: int = -1):
    # Deal with port mismatches
    if ("No matching port in gate module" in lec_feedback) or ("Can't match gold port" in lec_feedback):
        # Just return the name of the missing port, extract between '\\' and '!'
        pattern = r"\\(.*?)!"
        match = re.search(pattern, lec_feedback)
        if match:
            extracted  = match.group(1)
            res_string = extracted
        else:
            res_string = lec_feedback
        return str(-1) + "\n" + res_string
    # SAT Solver doesn't like latches
    if "Latch inferred for signal" in lec_feedback:
        res_string = ""
        lines      = lec_feedback.split('\n')
        for line in lines:
            # Return the line that idenfiies the latch
            pattern = r"^(.*?) from process"
            match   = re.search(pattern, line)
            if match:
                extracted   = match.group(1)
                res_string += extracted.replace('`','').replace('\'','')
            else:
                res_string += line
        return str(-2) + "\n" + res_string
    # Pipe misc. errors through directly
    if "ERROR:" in lec_feedback:
        return str(-3) + "\n" + lec_feedback

    # Split the string into separate sections for each table
    tables = lec_feedback.split(lec_feedback.split('\n')[0] + "\n")
    # Function to process each table
    def process_table(table):
        # Isolate the lines between "Signal Name" and "\trigger"
        table_lines = table.split("\\trigger")[0].split('\n')
        table_lines = table_lines[1:-1]
        gate_values = []
        gold_values = []
        input_values = []
        for line in table_lines:
            parts = line.split()
            if len(parts) == 0 or parts[0] == 'Signal' or parts[0] == ('-'*len(parts[0])):
                continue
            if parts:
                signal_name = parts[0][1:]  # Remove leading backslash
                bin_value = parts[-1]  # Binary representation
                if signal_name.startswith("\\gate_"):
                    gate_values.append(f"{signal_name[6:]} = 'b{bin_value}")
                elif signal_name.startswith("\\gold_"):
                    gold_values.append(f"{signal_name[6:]} = 'b{bin_value}")
                else:
                    input_values.append(f"{signal_name[4:]} = 'b{bin_value}")
        reduced_gold = []
        reduced_gate = []
        for i in range(len(gold_values)):
            if gold_values[i] != gate_values[i]:
                reduced_gold.append(gold_values[i])
                reduced_gate.append(gate_values[i])
        ret_string  = "Test input value(s):\n"
        ret_string += '\n'.join(input_values)
        ret_string += "\nDUT output value(s):\n"
        ret_string += '\n'.join(reduced_gate)
        ret_string += "\nExpected output value(s):\n"
        ret_string += '\n'.join(reduced_gold)
        return ret_string
    # Process each table
    ret_list = []
    for table in tables[1:]: # ignore blank first entry
        ret_list.append(process_table(table))
    ret_list.sort()
    if limit < 1:
        limit = len(ret_list)
    limited_list = ret_list[0:limit]
    res_string = ""
    i = 0
    test_count = 0
    if ret_list is not None:
        test_count = len(ret_list)
    if limit == 0:
        return str(test_count) + "\n "
    for entry in limited_list:
        i += 1
        res_string += ("Testcase failed:\n".format()) + entry + "\n\n"
    return str(test_count) + "\n" + res_string
