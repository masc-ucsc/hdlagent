#!/usr/bin/env python3
import os
import sys
import yaml

def add_bench_stage(directory):
    file_count = 0
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                file_path = os.path.join(subdir, file)
                try:
                    with open(file_path, 'r') as f:
                        data = yaml.safe_load(f)
                    
                    data['bench_stage'] = 0

                    with open(file_path, 'w') as f:
                        yaml.safe_dump(data, f, default_flow_style=False)
                    
                    file_count += 1
                    print(f"Processed {file_path}")
                except Exception as e:
                    print(f"Failed to process {file_path}: {e}")

    print(f"Total files processed: {file_count}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./add_stage.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    add_bench_stage(directory)
    print(f"Completed adding 'bench_stage: 0' to all YAML files in {directory}")

