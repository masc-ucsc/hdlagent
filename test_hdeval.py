import sys
import hdeval

print("Python executable:", sys.executable)
print("Python version:", sys.version)
print("Imported hdeval module from:", hdeval.__file__)

from hdeval import HDEvalInterface

def main():
    hdeval_interface = HDEvalInterface('/home/farzaneh/hdeval')
    benchmark_data = hdeval_interface.hdeval_open('24a')
    print("Benchmark Data:")
    print(benchmark_data)

if __name__ == "__main__":
    main()

