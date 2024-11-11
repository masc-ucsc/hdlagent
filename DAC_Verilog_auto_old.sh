#!/bin/bash

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gpt-4-1106-preview --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gpt-4-1106-preview/HDLEval-comb/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:24a --top_k=10

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gpt-4-1106-preview --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gpt-4-1106-preview/HDLEval-pipe/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:24a_pipe

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gpt-4-1106-preview --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gpt-4-1106-preview/VerilogEval2-comb/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:VerilogEval2-comb

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gpt-4-1106-preview --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gpt-4-1106-preview/VerilogEval2-pipe/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:VerilogEval2-pipe

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gpt-3.5-turbo-0125 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gpt-3.5-turbo-0125/HDLEval-comb/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:24a --top_k=10

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gpt-3.5-turbo-0125 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gpt-3.5-turbo-0125/HDLEval-pipe/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:24a_pipe

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gpt-3.5-turbo-0125 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gpt-3.5-turbo-0125/VerilogEval2-comb/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:VerilogEval2-comb

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gpt-3.5-turbo-0125 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gpt-3.5-turbo-0125/VerilogEval2-pipe/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:VerilogEval2-pipe

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gpt-3.5-turbo-1106 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gpt-3.5-turbo-1106/HDLEval-comb/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:24a --top_k=10

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gpt-3.5-turbo-1106 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gpt-3.5-turbo-1106/HDLEval-pipe/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:24a_pipe

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gpt-3.5-turbo-1106 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gpt-3.5-turbo-1106/VerilogEval2-comb/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:VerilogEval2-comb

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gpt-3.5-turbo-1106 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gpt-3.5-turbo-1106/VerilogEval2-pipe/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:VerilogEval2-pipe
timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gemini-1.0-pro-002 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gemini-1.0-pro-002/HDLEval-comb/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:24a --top_k=10

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gemini-1.0-pro-002 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gemini-1.0-pro-002/HDLEval-pipe/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:24a_pipe

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gemini-1.0-pro-002 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gemini-1.0-pro-002/VerilogEval2-comb/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:VerilogEval2-comb

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gemini-1.0-pro-002 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gemini-1.0-pro-002/VerilogEval2-pipe/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:VerilogEval2-pipe

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gemini-1.5-flash-002 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gemini-1.5-flash-002/HDLEval-comb/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:24a --top_k=10

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gemini-1.5-flash-002 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gemini-1.5-flash-002/HDLEval-pipe/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:24a_pipe

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gemini-1.5-flash-002 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gemini-1.5-flash-002/VerilogEval2-comb/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:VerilogEval2-comb

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=gemini-1.5-flash-002 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/gemini-1.5-flash-002/VerilogEval2-pipe/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:VerilogEval2-pipe

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=Mixtral-8x7B-v0.1 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/Mixtral-8x7B-v0.1/HDLEval-comb/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:24a --top_k=10

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=Mixtral-8x7B-v0.1 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/Mixtral-8x7B-v0.1/HDLEval-pipe/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:24a_pipe

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=Mixtral-8x7B-v0.1 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/Mixtral-8x7B-v0.1/VerilogEval2-comb/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:VerilogEval2-comb

timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=Mixtral-8x7B-v0.1 --skip_successful --skip_completed --lang=Verilog --w_dir=../DAC_results/Mixtral-8x7B-v0.1/VerilogEval2-pipe/Verilog/few_shot --lec_limit=1 --comp_limit=1 --init_context hdlagent/resources/Verilog/Verilog_examples.md hdeval:VerilogEval2-pipe

