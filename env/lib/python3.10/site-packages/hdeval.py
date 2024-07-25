import os
import subprocess
import json


class HDEvalInterface:
    def __init__(self, repo_url='git@github.com:masc-ucsc/hdeval.git'):
        self.repo_url = repo_url
        self.cache_dir = os.path.expanduser('~/.cache/hdeval')

    def download_benchmark(self, benchmark_name, version=None):
        os.makedirs(self.cache_dir, exist_ok=True)
        benchmark_path = os.path.join(self.cache_dir, benchmark_name)

        if os.path.exists(benchmark_path):
            # If benchmark directory already exists, do a git pull to update it
            subprocess.run(['git', '-C', benchmark_path, 'pull'])
        else:
            subprocess.run(['git', 'clone', self.repo_url, benchmark_path])

        if version:
            subprocess.run(['cd', benchmark_path], shell=True)
            subprocess.run(['../decrypt', version], shell=True)
        else:
            subprocess.run(['cd', benchmark_path], shell=True)
            subprocess.run(['./decrypt'], shell=True)

    def get_benchmark_json(self, benchmark_name, version=None):
        benchmark_path = os.path.join(self.cache_dir, benchmark_name)
        if not os.path.exists(benchmark_path):
            self.download_benchmark(benchmark_name, version)

        json_path = os.path.join(benchmark_path, f'{benchmark_name}.json')
        if os.path.exists(json_path):
            with open(json_path, 'r') as file:
                return json.load(file)
        else:
            print(f"Error: JSON file for benchmark '{benchmark_name}' not found.")
            exit(1)

    def hdeval_open(self, benchmark_name, version=None):
        return self.get_benchmark_json(benchmark_name, version)
