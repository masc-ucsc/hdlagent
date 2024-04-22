
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

### List available models

Running directly from the checkout repository
```
cd sample
 poetry run  ../hdlagent/hdlagent.py --list_models
```

### Run a Simple test from json

```
cd sample
poetry run ../hdlagent/hdlagent.py --supp_context  --llm gpt-4-turbo-preview --bench ./sample-test.json
```

