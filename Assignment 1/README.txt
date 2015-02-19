############################
#CSE 307-01 ASSIGNMENT 1   #
#  Prof. Annie Liu         #
#By Sam Wang, ID: 108107971#
############################
# Feb. 6, 2014 #
################

Included Files:
-a1main.py
-a1input0.txt
-a1output0.txt
-README.txt
-a1test.png

How to Run:
- Extract files.
- Launch a1main.py via command line .
- Be sure to include your input filename as the argument.
(You can use the included 'a1input0.txt'.)
- An output table should be printed on console and a 'a1output.txt' file should also be created with the same data.
(If you used the included txt file, the results should match the data in 'a1output0.txt'.
- Data with an unequal number of columns will be rejected gracefully.
- Failure to provide a filename or providing an invalid filename will also cause the program to terminate gracefully.

What I did/Explanations:
- The program first take in the command line argument and attempts to open it. I use exception handling and the sys module for this.
- I also make a class called 'Cell' for easy data storage of each cell that will be recorded from the input.
Each Cell object holds the value of the cell and the occurrences of it.
- I also designed a searchValue function that will search the given value attribute in the given list of Cells.
This function acts differently depending on whether the value is a string or int signified by another variable.
- The main program is a for loop that loops through the input file and records the lines one at a time, splitting them into a list of strings, separated by tabs using .split('\t').
The line is also checked to see whether it's empty beforehand.
- The 'rows' variable is repeatedly increased by one for each successful line intake to signify an additional row.
- If 'columns' has not been initialized (still 0) then it signifies the line is the first line which represents the header.
The header cells are appended into the headerList.
- Else the lines must be actual data and is checked whether they're digits. The # of columns is also checked to see whether it matches
the number of headers.
- Next the program calls 'searchValue' to check whether the current value in a particular position of the line has appeared before.
A Cell object is made and appended if the value has not appeared before, otherwise the # of occurrences of that cell is increased.
- Lastly we write the output in the required format onto a text file named 'a1output.txt'. 
The lists are also sorted during this time using .sort() with a key using the operator module to get the attributes of the cell objects for sorting.
The same information is also printed on the console.

Results:
The program have been tested with all the example inputs provided by the handout and returns desired results.
There was a little bug during the process when sorting a column made of floats and ints however that bug was not reproducible.
(Hopefully it won't happen again.)

Credits:
All information were learned from reading:
 The Python Tutorial (http://docs.python.org/3.3/tutorial/)
 The Python Library (http://docs.python.org/3.3/library/)
No discussions were made with any third-party.