import sys
import tpg

################################
#ASSIGNMENT 2, Due Date: Feb.28#
#CSE 307-01: Prof. Annie Liu   #
#Name: Sam Wang, ID: 108107971 #  
################################

class EvalError(Exception):
    """Class of exceptions raised when an error occurs during evaluation."""

# These are the classes of nodes of our abstract syntax trees (ASTs).

class Node(object):
    """Base class of AST nodes.  May come in handy in the future."""
    
    def eval(self):
        """Evaluate the AST node, called on nodes of subclasses of Node."""
        raise Exception("Not implemented.")

class Int(Node):
    """Class of nodes representing integer literals."""

    def __init__(self, value):
        self.value = int(value)
    
    def eval(self):
        return self.value

class Multiply(Node):
    """Class of nodes representing integer multiplications."""

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this operation.
        self.left = left
        self.right = right

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if not isinstance(left,int): raise EvalError()
        if not isinstance(right,int): raise EvalError()
        return left * right

class Divide(Node):
    """Class of nodes representing integer divisions."""

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this operation.
        self.left = left
        self.right = right

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if not isinstance(left, int): raise EvalError()
        if not isinstance(right, int): raise EvalError()
        if right == 0: raise EvalError()
        return int(left / right)

#My CLASSES
class Str(Node):

    def __init__(self, value):
        self.value = str(value)[1:-1]
    
    def eval(self):
        return self.value

class Array(Node):

    def __init__(self, value):
        self.value = value
    
    def eval(self):
        return self.value

class Add(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if (isinstance(left,int) and isinstance(right,int)) or (isinstance(left,str) and isinstance(right,str)):
            return left + right
        else: raise EvalError()

class Subtract(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if not isinstance(left,int): raise EvalError()
        if not isinstance(right,int): raise EvalError()
        return left - right

class Equal(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if not isinstance(left,int): raise EvalError()
        if not isinstance(right,int): raise EvalError()
        if left == right: return 1
        else: return 0

class Greater(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if not isinstance(left,int): raise EvalError()
        if not isinstance(right,int): raise EvalError()
        if left > right: return 1
        else: return 0
        
class Less(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if not isinstance(left,int): raise EvalError()
        if not isinstance(right,int): raise EvalError()
        if left < right: return 1
        else: return 0

class Or(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if not isinstance(left,int): raise EvalError()
        if not isinstance(right,int): raise EvalError()
        if left or right: return 1
        else: return 0

class And(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if not isinstance(left,int): raise EvalError()
        if not isinstance(right,int): raise EvalError()
        if left and right: return 1
        else: return 0

class Index(Node):

    def __init__(self, a, b):
        self.lst = a
        self.pos = b
        
    def eval(self):
        lst = self.lst.eval()
        pos = self.pos.eval()
        if not isinstance(pos,int): raise EvalError()
        if (not isinstance(lst,str))and(not isinstance(lst,list)): raise EvalError()
        if (len(lst)<=(pos)): raise EvalError()
        else: return lst[pos]

class Not(Node):

    def __init__(self, value):
        self.value = value

    def eval(self):
        value = self.value.eval()
        if not isinstance(value,int): raise EvalError()
        if not value: return 1
        else: return 0

#END

# This is the parser using TPG for parsing expressions and building an AST.
class Parser(tpg.Parser):
    r"""
    token int:         '\d+' ;
    token string:      '\"[^\"]*\"' ;
    separator spaces:  '\s+' ;

    START/s -> Exp/s ;
    Exp/e -> Dis/e ;
    Dis/e -> Con/e ('or' Con/e2 $e=Or(e,e2)$)* ;
    Con/e -> Not/e ('and' Not/e2 $e=And(e,e2)$)* ;
    Not/e -> 'not' Not/e $e=Not(e)$ | Comp/e ;
    Comp/e -> Add/e ( '\==' Add/e2 $e=Equal(e,e2)$
                    | '\>' Add/e2 $e=Greater(e,e2)$
                    | '\<' Add/e2 $e=Less(e,e2)$)* ;
    Add/e -> Mul/e ( '\+' Mul/e2 $e=Add(e,e2)$
                   | '\-' Mul/e2 $e=Subtract(e,e2)$)* ;
    Mul/e -> Index/e ( '\*' Index/e2  $e=Multiply(e,e2)$
                    | '/'  Index/e2  $e=Divide(e,e2)$)* ;
    Index/e -> Atom/e ( '\[' Exp/e2 '\]' $e=Index(e,e2)$)*
              | Atom/e ;
    Atom/e -> '\[' $lst=[]$ Exp/e $lst.append(e.eval())$ (',' Exp/e $lst.append(e.eval())$)* '\]' $e=Array(lst)$
              | '\[' $e=Array([])$ '\]'
              | '\(' Exp/e '\)'
              | int/i  $e=Int(int(i))$
              | string/s $e=Str(s)$; 
    """

# This makes a parser object, which acts as a parsing function.
parser = Parser()


# Below is the driver code, which reads in lines, deals with errors, and
# prints the evaluation result if no error occurs.

# Open the input file, and read in lines of the file.
lines = open(sys.argv[1], 'r').readlines()
#Next line for easy testing only
#lines = open("a2input0.txt", 'r').readlines() 

# For each line in the input file
for l in lines:
    # Uncomment the next line to help testing.  Comment it for submission.
    # print(l, end="")
    try:
        # Try to parse the expression.
        node = parser(l)

        # Try to evaluate the expression.
        result = node.eval()

        # Print the representation of the result.
        print(repr(result))

    # If an exception is rasied, print the appropriate error.
    except tpg.Error:
        print('Parsing Error')

        # Uncomment the next line to re-raise the parsing error,
        # displaying where the error occurs.  Comment it for submission.

        #raise

    except EvalError:
        print('Evaluation Error')

        # Uncomment the next line to re-raise the evaluation error, 
        # displaying where the error occurs.  Comment it for submission.

        #raise
