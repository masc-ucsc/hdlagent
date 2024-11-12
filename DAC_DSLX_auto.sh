#!/bin/bash

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gemini-1.0-pro-002 --skip_successful --skip_completed --lang=DSLX --w_dir=../DAC_results/gemini-1.0-pro-002/HDLEval-comb/DSLX/supp --lec_limit=1 --comp_limit=8 --init_context hdlagent/resources/DSLX/dslx_reference_sum2_gemini.md --supp_context hdeval:24a --top_k=10

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gemini-1.0-pro-002 --skip_successful --skip_completed --lang=DSLX --w_dir=../DAC_results/gemini-1.0-pro-002/VerilogEval2-comb/DSLX/supp --lec_limit=1 --comp_limit=8 --init_context hdlagent/resources/DSLX/dslx_reference_sum2_gemini.md --supp_context hdeval:VerilogEval2-comb

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gemini-1.5-flash-002 --skip_successful --skip_completed --lang=DSLX --w_dir=../DAC_results/gemini-1.5-flash-002/HDLEval-comb/DSLX/supp --lec_limit=1 --comp_limit=8 --init_context hdlagent/resources/DSLX/dslx_reference_sum2_gemini.md --supp_context hdeval:24a --top_k=10


timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gemini-1.5-flash-002 --skip_successful --skip_completed --lang=DSLX --w_dir=../DAC_results/gemini-1.5-flash-002/VerilogEval2-comb/DSLX/supp --lec_limit=1 --comp_limit=8 --init_context hdlagent/resources/DSLX/dslx_reference_sum2_gemini.md --supp_context hdeval:VerilogEval2-comb

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=llama3-405b --skip_successful --skip_completed --lang=DSLX --w_dir=../DAC_results/llama3-405b/HDLEval-comb/DSLX/supp --lec_limit=1 --comp_limit=8 --init_context hdlagent/resources/DSLX/dslx_reference_sum2_gemini.md --supp_context hdeval:24a --top_k=10

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=llama3-405b --skip_successful --skip_completed --lang=DSLX --w_dir=../DAC_results/llama3-405b/VerilogEval2-comb/DSLX/supp --lec_limit=1 --comp_limit=8 --init_context hdlagent/resources/DSLX/dslx_reference_sum2_gemini.md --supp_context hdeval:VerilogEval2-comb
