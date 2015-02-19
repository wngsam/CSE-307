import sys
import operator

###############################
#ASSIGNMENT 1, Due Date: Feb.7#
#CSE 307-01: Prof. Annie Liu  #
#Name: Sam Wang, ID: 108107971#  
###############################

#Test command arg for valid filename.
try:
    fileName = sys.argv[1]
    f = open(sys.argv[1],'r')
    
except (IndexError, FileNotFoundError):
    
    print("No input filename or file not found.")
    sys.exit()

#Variables for columns, rows and a list for the headers separate from other cells.
columns, rows = 0,0
cellList = list()
headerList = list()

#Class for cells and their data. (Value of cell and its # of occurrences.) 
class Cell:
    
        def __init__(self, value):
            self.count = 1
            self.value = value

#Function for finding duplicate values.
#First checks whether mylist (the list of cells in that column)is empty.
#Then operates depending on whether types is 1 or 0.
#1 means value is a number while 0 means value is a string.
#Returns true to signify duplicate value, false for non-duplicate.
def searchValue(mylist, value, types):
    if len(mylist)==0:
        return False
    
    counter = 0
    while counter < len(mylist):
        
            if types==0 and mylist[counter].value.strip()==value.strip():
                mylist[counter].count=mylist[counter].count+1
                return True
            elif types==1 and mylist[counter].value==value:
                mylist[counter].count=mylist[counter].count+1
                return True
            
            counter=counter+1
            
    return False
            
#Starts reading txt file to the end and record cells in various lists according to columns.
for line in f:
    #Checks if row is empty, if not continue, else next line. (Ignoring empty spaces)
    if line.strip() != '':
        
        #Get line and split by tabs.
        tempLine = line.split('\t')
    
        #Increases rows count by 1.
        rows=rows+1

        #If first line, initialize column value and append the cell list to the appropriate size.
        #Also appends header data to header list.
        if columns == 0:
            
            columns = len(tempLine)
            counter = 0
            
            while counter<columns:
                cellList.append([])
                headerList.append("Column "+str(counter)+": "+tempLine[counter].strip())
                counter=counter+1
                
        else:
        #Checks if the # of columns on this line matches the initialized column # of headers if not exit.    
            if len(tempLine)!=columns:
                print("Number of rows: "+str(rows))
                print("Cannot determine number of columns")
                o = open("a1output.txt",'w')
                o.write("Number of rows: "+str(rows)+"\n")
                o.write("Cannot determine number of columns"+"\n")
                o.close()
                sys.exit()
                
            else:
                counter = 0
                #Get specific cell in the list of cells from the line.
                while counter<columns:
                    tempString = tempLine[counter]
                    #Check if cell is a number.
                    if tempString.isdigit()==True:
                            tempString=int(tempString)
                            #Check if num value has been recorded already.
                            if searchValue(cellList[counter],tempString,1)!=True:
                                #Create cell obj and append to list.
                                tempCell = Cell(tempString)
                                cellList[counter].append(tempCell)
                    else:
                        #Check if string value has been recorded already.
                        if searchValue(cellList[counter],tempString,0)!=True:
                            #Record string to cell obj and append to list.
                            tempString=tempString.strip()
                            tempCell = Cell(tempString)
                            cellList[counter].append(tempCell)
                    
                    counter=counter+1
                    
#End of txt reading, close file.
f.close()

#Open/Create an output file to be written with the data extracted from the lists.    
o = open("a1output.txt",'w')
o.write("Number of rows: "+str(rows)+"\n"+"Number of columns: "+str(columns)+"\n")
counter = 0
for x in headerList:
    #Writing Headers
    o.write(x+"\n")
    #Sort list by the attribute value of the cell obj.
    cellList[counter].sort(key=operator.attrgetter("value"))
    for y in cellList[counter]:
        #Writing cell value and occurrences.
        o.write(" "+str(y.count)+" "+str(y.value)+"\n")        
    counter=counter+1
o.close()

#Standard output for testing purposes, visual comparison, etc.
print("Number of rows: "+str(rows)+"\n"+"Number of columns: "+str(columns))
counter = 0
for x in headerList:
    #Print headers
    print(x)
    #Sort by obj attribute
    cellList[counter].sort(key=operator.attrgetter("value"))
    for y in cellList[counter]:
        #Print data
        print(" "+str(y.count)+" "+str(y.value))        
    counter=counter+1
#End of Program. Feb. 6, 2014. Sam Wang.
