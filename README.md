
AI Coding Agent for specification to hardware code.

It uses self-reflection, context, and grounding with EDA tools.


## Installation instructions

Install with python poetry:
```
poetry install
```

If updating hdlagent, you may need to update poetry dependencies too:
```
poetry lock
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

