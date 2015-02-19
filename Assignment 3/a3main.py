import sys
import tpg

################################
#ASSIGNMENT 3, Due Date: Mar.28#
#CSE 307-01: Prof. Annie Liu   #
#Name: Sam Wang, ID: 108107971 #  
################################

class AnalError(Exception):
    """Class of exceptions raised when an error occurs during analysis."""

# These are the classes of nodes of our abstract syntax trees (ASTs).

class Node(object):
    """Base class of AST nodes."""

    # For each class of nodes, store names of the fields for children nodes.
    fields = []

    def __init__(self, *args):
        """Populate fields named in "fields" with values in *args."""
        assert(len(self.fields) == len(args))
        for f, a in zip(self.fields, args): setattr(self, f, a)

    def eval(self, num):
        """Evaluate the AST node, called on nodes of subclasses of Node."""
    
# subclasses of Node for expressions

#List of var Names
glbNames=list()
class Var(Node):
    """Class of nodes representing accesses of variable."""
    fields = ['name']

    def __init__(self, value):
        self.value = value
        glbNames.append(self.value)
    
    def eval(self, num):
        if num==2:
            return self.value
    
class Int(Node):
    """Class of nodes representing integer literals."""
    fields = ['value']

    def __init__(self, value):
        self.value = value
    
    def eval(self, num):
        if num==2:
            return self.value
        
class String(Node):
    """Class of nodes representing string literals."""
    fields = ['value']

    def __init__(self, value):
        self.value = value
    
    def eval(self,num):
        if num==2:
            return self.value
    
class Array(Node):
    """Class of nodes representing array literals."""
    fields = ['elements']

    def __init__(self,param):
        self.param=param

    def eval(self, num):
        if num==2:
            for l in self.param:
                if l.eval(2) in glbNames: print('Use of variable '+str(l.eval(2)))
    
class Index(Node):
    """Class of nodes representing indexed accesses of arrays or strings."""
    fields = ['indexable','index']
    
    def __init__(self, e, e2):
        self.e=e
        
    def eval(self, num):
        if num==2:
            if self.e.eval(2) in glbNames: print('Use of variable '+str(self.e.eval(2)))
                              
class BinOpExp(Node):
    """Class of nodes representing binary-operation expressions."""
    fields = ['left', 'op', 'right']

    def __init__(self, left, op, right):
        self.left=left
        self.right=right
        
    def eval(self, num):
        if num==2:
            if self.left.eval(2) in glbNames: print('Use of variable '+str(self.left.eval(2)))
            if self.right.eval(2) in glbNames and not isinstance(self.right, Int): print('Use of variable '+str(self.right.eval(2)))
        
class UniOpExp(Node):
    """Class of nodes representing unary-operation expressions."""
    fields = ['op', 'arg']

    def __init__(self, op,e):
        self.e=e
        self.op=op
        
    def eval(self, num):
        if num==2:
            self.e.eval(2)
    
# subclasses of Node for statements

class Print(Node):
    """Class of nodes representing print statements."""
    fields = ['exp']

    def __init__(self, param):
        self.param=param

    def eval(self, num):
        if num==2:
            if isinstance(self.param,Array) or isinstance(self.param,BinOpExp): return self.param.eval(2)
            elif self.param.eval(2) in glbNames: print('Use of variable '+str(self.param.eval(2)))
            
class Assign(Node):
    """Class of nodes representing assignment statements."""
    fields = ['left', 'right']

    def __init__(self, name, value):
        self.value=value
        self.name=name

    def eval(self, num):
        if num==2:
            self.value.eval(2)
            print('Definition of variable '+str(self.name.eval(2)))
        
class Block(Node):
    """Class of nodes representing block statements."""
    fields = ['stmts']

    def __init__(self, value):
        self.value = value
    
    def eval(self, num):
        for l in self.value:
            l.eval(num)
    
class If(Node):
    """Class of nodes representing if statements."""
    fields = ['exp', 'stmt']

    def __init__(self, e,s):
        self.e=e
        self.s=s
        
    def eval(self, num):
        if num==2:
            self.e.eval(2)
            self.s.eval(2)
    
class While(Node):
    """Class of nodes representing while statements."""
    fields = ['exp', 'stmt']

    def __init__(self, e,s):
        self.e=e
        self.s=s
        
    def eval(self, num):
        if num==2:
            self.e.eval(2)
            self.s.eval(2)

#List of Procedure Names
defNames=list()
class Def(Node):
    """Class of nodes representing procedure definitions."""
    fields = ['name', 'params', 'body']

    def __init__(self, name, param, body):
        self.name = name
        self.param=param
        self.body=body
        if self.name in defNames:
            raise AnalError
        else:
            defNames.append(self.name)
            
    def eval(self,num):
        if num==1:
            print("Definition of procedure "+self.name)

        if num==2:
            print('Locals of procedure '+self.name+': '+str(self.param)[1:-1])
            return self.body.eval(2)
            
class Call(Node):
    """Class of nodes representing procedure calls."""
    fields = ['name', 'args']

    def __init__(self, name, param):
        self.name = name
        self.param=param

    def eval(self, num):
        if num==1:
            if self.name in defNames:
                print('Call of procedure '+self.name)
            else:
                raise AnalError
        if num==2:
            for l in self.param:
                if isinstance(l,Var):
                    if l.eval(2) in glbNames:
                        print('Use of variable '+str(l.eval(2)))
            
class Parser(tpg.Parser):
    r"""
    token int:         '\d+' ;
    token string:      '\"[^\"]*\"' ;
    token ident:       '[a-zA-Z_][\w]*' ;
    separator spaces:  '\s+' ;
    separator comment: '#.*' ;

    START/s -> Stmt/s ;

    Stmt/s ->
    ( 'print' Exp/e ';'  $s = Print(e)$
    | Exp/l '=(?!=)' Exp/r ';'  $ s = Assign(l, r) $
    | '\{'  $ s=[] $  ( Stmt/s2  $ s.append(s2) $  )* '\}'  $s = Block(s)$
    | 'if' '\(' Exp/e '\)' Stmt/s  $ s = If(e, s) $
    | 'while' '\(' Exp/e '\)' Stmt/s  $ s = While(e, s) $
    | 'def' ident/f '\('  $l=[]$  ( ident/i  $l.append(i)$
                                    ( ',' ident/i  $l.append(i)$  )*)? '\)'
      Stmt/s2  $s=Def(f,l,s2)$
    | ident/f '\('  $l=[]$  ( Exp/e  $l.append(e)$
                              ( ',' Exp/e  $l.append(e)$  )*)? '\)' ';'
      $s=Call(f,l)$
    ) ;

    Exp/e -> Or/e ;
    Or/e  -> And/e ( 'or'  And/e2  $e=BinOpExp(e,'or', e2)$  )* ;
    And/e -> Not/e ( 'and' Not/e2  $e=BinOpExp(e,'and',e2)$  )* ;
    Not/e -> 'not' Not/e  $e=UniOpExp('not', e)$  | Cmp/e ;
    Cmp/e -> Add/e ( CmpOp Add/e2  $e=BinOpExp(e,CmpOp,e2)$  )* ;
    Add/e -> Mul/e ( AddOp Mul/e2  $e=BinOpExp(e,AddOp,e2)$  )* ; 
    Mul/e -> Index/e ( MulOp Index/e2  $e=BinOpExp(e,MulOp,e2)$  )* ;
    Index/e -> Atom/e ( '\[' Exp/e2 '\]'  $e=Index(e,e2)$  )* ;
    Atom/e -> '\(' Exp/e '\)'
    | int/i     $e=Int(int(i))$
    | string/s  $e=String(s[1:-1])$
    | '\['  $e=[]$  ( Exp  $e.append(Exp)$  ( ',' Exp  $e.append(Exp)$  )*)?
      '\]'  $e=Array(e)$
    | ident     $e=Var(ident)$
    ;
    CmpOp/r -> '=='/r | '<'/r | '>'/r ;
    AddOp/r -> '\+'/r | '-'/r ;
    MulOp/r -> '\*'/r | '/'/r ;
    """

def parse(code):
    # This makes a parser object, which acts as a parsing function.
    parser = Parser()
    return parser(code)

##MY METHODS

def AnalProcedures(node):
    node.eval(1)

def AnalVariables(node):
    node.eval(2)

# Below is the driver code, which parses a given MustScript program
# and analyzes the definitions and uses of procedures and variables

# Open the input file, and read in the input program.
prog = open(sys.argv[1]).read()
#Below for easy Testing Only!
#prog = open('a3input4.txt').read()

try:
    # Try to parse the program.
    print('Parsing...')
    node = parse(prog)

    # Try to analyze the program.
    print('Analyzing...')

    # ... set up and call method for analyzing procedures here
    AnalProcedures(node)
    
    # ... set up and call method for analyzing variables here
    AnalVariables(node)

# If an exception is rasied, print the appropriate error.
except tpg.Error:
    print('Parsing Error')

    # Uncomment the next line to re-raise the parsing error,
    # displaying where the error occurs.  Comment it for submission.

    # raise

except AnalError as e:
    print('Analysis Error')

    # Uncomment the next line to re-raise the evaluation error, 
    # displaying where the error occurs.  Comment it for submission.

    # raise
