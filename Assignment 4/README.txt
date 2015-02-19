############################
#CSE 307-01 ASSIGNMENT 4   #
#  Prof. Annie Liu         #
#By Sam Wang, ID: 108107971#
############################
# Apr. 8, 2014 #
################

Included Files:
-a4main.py
-tpg.py
-a4input1.txt
-a4output1.txt
-a4input3.txt
-a4output3.txt
-a4input4.txt
-a4output4.png
-README.txt

How to Run:
- Extract files.
- Launch a4main.py via command line .
- Be sure to include your input filename as the argument.
(You can use the included 'a4input4.txt'.)
- An output should be printed on console.
(If you used the included txt file, the results should match the data in 'a4output4.png'.

What I did/Explanations:
A comment exists on top of all the methods I've written in the code.
I modified all the eval() methods to take in a local variable dict so I can pass a temporary dict that hold variables for recursive calls.
Implemented Var's eval() method to search for a variable and return its value from dictionaries.
Implemented exec() for Assign, Block, If, While, Def and Call. Most are self-explanatory except for Call which checks for correct length
of params/args and then execute the body code with a temporary dictionary for local variables.

Results:
My program prints the correct output for all example inputs.

Updated:
Def() updated to handle definitions with the same name.

Credits:
Code by Professor Liu

All information were learned from reading:
Previous knowledge
Google Q/A forum