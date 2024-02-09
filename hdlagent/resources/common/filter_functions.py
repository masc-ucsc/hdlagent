def comment_filter_function(lec_feedback: str):
    # Split the string into separate sections for each table
    tables = lec_feedback.split("Signal Name             Dec       Hex           Bin\n")
    # Function to process each table
    def process_table(table):
        # Isolate the lines between "Signal Name" and "\trigger"
        table_lines = table.split("\\trigger")[0].split('\n')
        realized_result = []
        desired_result = []
        when_condition = []
        for line in table_lines:
            if line.strip() and "-------" not in line:
                parts = line.split()
                if len(parts) < 4:  # Skip lines that don't have the complete format
                    continue
                signal_name = parts[0][1:]  # Remove leading backslash
                bin_value = parts[-1]  # Binary representation
                if signal_name.startswith("\gate_"):
                    realized_result.append(f"({signal_name[6:]} = 'b{bin_value})")
                elif signal_name.startswith("\gold_"):
                    desired_result.append(f"({signal_name[6:]} = 'b{bin_value})")
                else:
                    when_condition.append(f"({signal_name[4:]} = 'b{bin_value})")
        return f"// when: {', '.join(when_condition)}\n// realized result: {', '.join(realized_result)}\n// desired result: {', '.join(desired_result)}\n\n"
    # Process and print each table
    ret_str = ""
    for table in tables[1:]:  # Skip the first empty section before the first table
        formatted_output = process_table(table)
        if formatted_output.strip():  # Skip empty outputs
            ret_str += formatted_output
    return ret_str
