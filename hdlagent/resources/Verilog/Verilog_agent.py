
def custom_check_errors(compiler_output):
    res_string = (str(compiler_output.stdout))[2:-1].replace("\\n", "\n")
    if ("error" in res_string) or ("ERROR:" in res_string) or ("Warning:" in res_string):
        return res_string
    return None


def custom_reformat_verilog(name: str, ref_file: str, in_file: str, io_lines):
    # No need to reformat
    return (ref_file, in_file)
