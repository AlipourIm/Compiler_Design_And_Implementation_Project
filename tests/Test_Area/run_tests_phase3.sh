#!/bin/sh
echo "" > log.txt
echo "" > brief_results.txt
#for dir in ../PA3_final_tests/*; do
for dir in ../PA3_input_output_samples/*; do
    cp "${dir}/input.txt" "../../input.txt"
    cd '../../'
    python3 ./compiler.py
    ./interpreter/tester_Linux.out > expected.txt
    cd 'tests/Test_Area/'

    printf "\n\n\n\n=====================================>>>>> Running Test ${dir}...\n" >> log.txt
    printf "\n\n=====================================>>>>> Running Test ${dir}...\n" >> brief_results.txt
    
    printf "\n\n              *** expected.txt diffrences ***\n" >> log.txt
    diff -y -B -W 250 -w  --suppress-common-lines "../../expected.txt" "${dir}/expected.txt" >> log.txt
    diff -y -B -W 250 -w -q "../../expected.txt" "${dir}/expected.txt" >> brief_results.txt
done


