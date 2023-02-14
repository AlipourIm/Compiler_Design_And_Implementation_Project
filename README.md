# Compiler_Design_And_Implementation_Project
In this project, we design a compiler for C- language using python 3.8. this project consists of 3 phases, in each phase we design and implement one part of the compiler.


Computer Engineering Department / Sharif Uni. of Technology

## Authors

* Ali Mahdavifar - Student ID: 98106072
* Iman Alipour - Student ID: 98102024

## Usage

Write your C- code in the `input.txt` file. A sample is already provided, and you can also use samples available in the `tests` folder.

This project eventually converts C- codes into three-address machine codes as described in `interpreter/tester_readme.pdf`.

Run the following command to compile the code in `input.txt` and generate the three-address code into `output.txt`:
```
python3 compiler.py
```
Besides the three-address machine code, you also get the parse tree of the code at `parse_tree.txt`, and possible lexical, syntax, and semantic errors respectively at `lexical_errors.txt`, `syntax_errors.txt` and `semantic_errors.txt`.

If there exist no errors, use the following command to execute the three-address code and get the result:
```
./interpreter/tester_Linux.out > reslut.txt
```

## Test
You can automatically test if the results for tests match the expected results for the final phase of the project by running the command below:
```
cd tests/Test_Area && ./run_tests_phase3.sh 
```
Then check `tests/Test_Area/log.txt` for possible differences between the expected and the actual outputs.
