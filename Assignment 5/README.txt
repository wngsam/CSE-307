############################
#CSE 307-01 ASSIGNMENT 5   #
#  Prof. Annie Liu         #
#By Sam Wang, ID: 108107971#
############################
# May. 2, 2014 #
################

Included Files:
-a5main.py
-tpg.py
-a5input1.txt
-a5input2.txt
-a5input3.txt
-a5input4.txt
-README.txt

How to Run:
- Extract files.
- Launch a5main.py via command line .
- Be sure to include your input filename as the argument.
(You can use the included 'a5input1.txt'.)
- An output should be printed on console.

What I did/Explanations:
The analyzing procedures method is written to return a tuple of procedures defined and called. Within this method the two sets
proc_defined and proc_called are merged with the return of each recursive call. The block objects are sent to a helper function that returns a tuple as well
and calls the analyzingh function and itself. Afterwards the error checking for procedures is done using a method that sends the tuple to two other methods that recursively check for errors.
The analyzing variable function returns a set of local variables which is used to keep track of the local variables upon recursive calls. Shadowing test is outsoured to another method that 
calls itself to check. Lastly a separate function is there to read in and made into a set of global variables available in the program. More information in code comments.

Results:
All 4 test inputs produce the correct/identical output provided by Prof. Liu.

Credits:
Code by Professor Liu

All information were learned from reading:
Previous knowledge
Google Q/A forum