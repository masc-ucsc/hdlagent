#!/usr/bin/env python3

import sys
import os
import re

def main():
    if len(sys.argv) != 2:
        print("Usage: python scriptname.py filename.scala")
        sys.exit(1)

    filename = sys.argv[1]
    if not filename.endswith('.scala'):
        print("Error: file must be a .scala file")
        sys.exit(1)

    with open(filename, 'r') as f:
        lines = f.readlines()

    modified = False

    file_basename = os.path.basename(filename)
    classname = os.path.splitext(file_basename)[0]

    # Create a new list to store the modified lines
    new_lines = []
    pattern = r'\b{}\b'.format(re.escape(classname))
    for line in lines:
        new_line = re.sub(pattern, classname, line, flags=re.IGNORECASE)
        new_lines.append(new_line)

    lines = new_lines

    # Check for the import statement chisel3.util._
    import_line = 'import chisel3.util._\n'
    import_exists = any('import chisel3.util._' in line for line in lines)

    if not import_exists:
        # Find the last import statement
        last_import_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('import '):
                last_import_index = i

        # Insert the import after the last import or at the beginning
        insert_index = last_import_index + 1 if last_import_index != -1 else 0
        lines.insert(insert_index, import_line)
        modified = True

    # Check for the import statement ChiselStage
    import_line = 'import _root_.circt.stage.ChiselStage\n'
    import_exists = any('import _root_.circt.stage.ChiselStage' in line for line in lines)

    if not import_exists:
        # Find the last import statement
        last_import_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('import '):
                last_import_index = i

        # Insert the import after the last import or at the beginning
        insert_index = last_import_index + 1 if last_import_index != -1 else 0
        lines.insert(insert_index, import_line)
        modified = True

    # Check for an object that extends App
    object_extends_app_pattern = re.compile(r'\bobject\s+\w+\s+extends\s+App\b')
    object_exists = any(object_extends_app_pattern.search(line) for line in lines)

    if not object_exists:
        # Prepare the snippet, replacing XXXXXX with the file name without .scala

        snippet = f"""
object Top extends App {{
  ChiselStage.emitSystemVerilogFile(
    new {classname},
    firtoolOpts = Array("-disable-all-randomization", "-strip-debug-info")
  )
}}
"""
        # Add the snippet at the end
        lines.append(snippet)
        modified = True

    if modified:
        # Write back to the file
        with open(filename, 'w') as f:
            f.writelines(lines)
        print(f"File {filename} has been modified.")
    else:
        print(f"No changes needed for file {filename}.")

if __name__ == '__main__':
    main()

