
## Installation instructions

Install with python poetry:
```
poetry install
```

Set the required keys (depends on the model that you use)
```
export OPENAI_API_KEY=.....
export OCTOAI_TOKEN=....
```

Sample execution:
```
cd sample
poetry run python ../hdlagent/hdlagent.py --llm=codellama-34b-instruct-fp16 --lang=Verilog --json_path=./sample-test.json --lec_source=../../llm4pld/RTL/Verilog/HDLEval-comb/
```

