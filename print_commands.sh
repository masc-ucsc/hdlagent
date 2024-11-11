#!/bin/bash

# Lists of LLMs, languages, benchmarks, and labels
llms=("gpt-4-1106-preview" "gpt-3.5-turbo-0125" "gpt-3.5-turbo-1106" "gemini-1.0-pro-002" "gemini-1.5-flash-002" "llama3-405b")
languages=("Verilog" "Chisel" "PyRTL" "DSLX")
benchmarks=("HDLEval-comb" "HDLEval-pipe" "VerilogEval2-comb" "VerilogEval2-pipe")
labels=("init" "simple" "supp" "desc")

declare -A init_context_paths
init_context_paths["Verilog"]="hdlagent/resources/Verilog/Verilog_context_1.md"
init_context_paths["Chisel"]="hdlagent/resources/Chisel/chisel_reference_sum1_gpt.md"
init_context_paths["PyRTL"]="hdlagent/resources/PyRTL/pyrtl_reference_sum1_gpt.md"
init_context_paths["DSLX"]="hdlagent/resources/DSLX/dslx_reference_sum2_gemini.md"

declare -A desc_context_paths
desc_context_paths["Verilog"]="hdlagent/resources/Verilog/Verilog_context_1.md"
desc_context_paths["Chisel"]="hdlagent/resources/Chisel/chisel_reference_sum1_gpt.md"
desc_context_paths["PyRTL"]="hdlagent/resources/PyRTL/pyrtl_reference_sum1_gpt.md"
desc_context_paths["DSLX"]="hdlagent/resources/DSLX/dslx_reference_sum2_gemini.md"

declare -A fewshot_context_paths
fewshot_context_paths["Verilog"]="hdlagent/resources/Verilog/Verilog_examples.md"
fewshot_context_paths["Chisel"]="hdlagent/resources/Chisel/Chisel_examples.md"
fewshot_context_paths["PyRTL"]="hdlagent/resources/PyRTL/PyRTL_examples.md"
fewshot_context_paths["DSLX"]="hdlagent/resources/DSLX/DSLX_examples.md"

for lang in "${languages[@]}"; do
    rm -f "DAC_${lang}_auto.sh"
    echo "#!/bin/bash" > "DAC_${lang}_auto.sh"
done

# Function to map benchmarks to arguments
get_benchmark_argument() {
  local bench=$1
  case $bench in
    "HDLEval-comb")
      echo "24a"
      ;;
    "HDLEval-pipe")
      echo "24a_pipe"
      ;;
    "VerilogEval2-comb")
      echo "VerilogEval2-comb"
      ;;
    "VerilogEval2-pipe")
      echo "VerilogEval2-pipe"
      ;;
    *)
      echo ""
      ;;
  esac
}

#base:
simple_command_fmt="timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=%s --skip_successful --skip_completed --lang=%s --w_dir=%s/simple --lec_limit=1 --comp_limit=1 hdeval:%s%s"
#Desc:
desc_command_fmt="timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=%s --skip_successful --skip_completed --lang=%s --w_dir=%s/desc --lec_limit=1 --comp_limit=1 --init_context %s hdeval:%s%s"
#few-shot:
fewshot_command_fmt="timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=%s --skip_successful --skip_completed --lang=%s --w_dir=%s/few_shot --lec_limit=1 --comp_limit=1 --init_context %s hdeval:%s%s"
#compile:
init_command_fmt="timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=%s --skip_successful --skip_completed --lang=%s --w_dir=%s/init --lec_limit=1 --comp_limit=8 --init_context %s hdeval:%s%s"
#Fixes:
supp_command_fmt="timeout 4000 poetry run hdlagent/cli_agent.py bench --llm=%s --skip_successful --skip_completed --lang=%s --w_dir=%s/supp --lec_limit=1 --comp_limit=8 --init_context %s --supp_context hdeval:%s%s"


# Generate the commands and append to the scripts
for llm in "${llms[@]}"; do
  for lang in "${languages[@]}"; do
    init_context_path="${init_context_paths[$lang]}"
    desc_context_path="${desc_context_paths[$lang]}"
    fewshot_context_path="${fewshot_context_paths[$lang]}"
    for bench in "${benchmarks[@]}"; do
      bench_arg=$(get_benchmark_argument "$bench")
      if [[ "$bench_arg" == "" ]]; then
        continue
      fi

      # Adjust the benchmark name for DSLX if needed
      if [[ "$lang" == "DSLX" ]]; then
        if [[ "$bench" == "VerilogEval-Human" ]]; then
          bench="VerilogEval-Human_comb"
        elif [[ "$bench" == "VerilogEval-Machine" ]]; then
          bench="VerilogEval-Machine_comb"
        elif [[ "$bench" == "HDLEval-pipe" ]]; then
          continue
        fi
      fi

      # Determine w_dir (adjust the path as needed)
      w_dir="../DAC_results/${llm}/${bench}/${lang}"

      # Determine the script file
      script_file="DAC_${lang}_auto.sh"

      # Adjust supp_end based on benchmark
      if [[ "$bench" == "HDLEval-comb" ]]; then
        supp_end=" --top_k=10"
      else
        supp_end=""
      fi

      # Append the commands to the script file
      printf "$simple_command_fmt\n" "$llm" "$lang" "$w_dir" "$bench_arg" "$supp_end" >> "$script_file"

      printf "$fewshot_command_fmt\n" "$llm" "$lang" "$w_dir" "$fewshot_context_path" "$bench_arg" "$supp_end" >> "$script_file"

      printf "$init_command_fmt\n" "$llm" "$lang" "$w_dir" "$init_context_path" "$bench_arg" "$supp_end" >> "$script_file"

      printf "$supp_command_fmt\n" "$llm" "$lang" "$w_dir" "$init_context_path" "$bench_arg" "$supp_end" >> "$script_file"

    done
  done
done

# Make scripts executable
for lang in "${languages[@]}"; do
    chmod +x "DAC_${lang}_auto.sh"
done
# # Loop over each combination and print the command
# for llm in "${llms[@]}"; do
#   for bench in "${benchmarks[@]}"; do
#     # Get the benchmark argument
#     bench_arg=$(get_benchmark_argument "$bench")
#     for lang in "${languages[@]}"; do
#       for label in "${labels[@]}"; do
#         # Construct the working directory path with the new order
#         w_dir="${llm}/${bench}/${lang}/${label}"
#         # Construct the command, adding the benchmark argument at the end
#         cmd="poetry run hdlagent/cli_agent.py bench --w_dir ${w_dir} --lang ${lang} --llm ${llm} hdeval:${bench_arg}"
#         # Print the command
#         echo "${cmd}"
#       done
#     done
#   done
# done
