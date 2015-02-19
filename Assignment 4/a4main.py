import sys
import tpg

################################
#ASSIGNMENT 4, Due Date: Apr.11#
#CSE 307-01: Prof. Annie Liu   #
#Name: Sam Wang, ID: 108107971 #  
################################

class EvalError(Exception):
    """Class of exceptions raised when an error occurs during evaluation."""

# These are the classes of nodes of our abstract syntax trees (ASTs).

class Node(object):
    """Base class of AST nodes."""

    # For each class of nodes, store names of the fields for children nodes.
    fields = []

    def __init__(self, *args):
        """Populate fields named in "fields" with values in *args."""
        assert(len(self.fields) == len(args))
        for f, a in zip(self.fields, args): setattr(self, f, a)

    def anlz_procs(self):
        """Collect procedure definitions, called on statements."""
        raise Exception("Not implemented.")

    def eval(self):
        """Evaluate the AST node, called on nodes of expression subclasses."""
        raise Exception("Not implemented.")

    def exec(self, local_var_env, is_global):
        """Evaluate the AST node, called on nodes of statement subclasses.
        local_var_env: mapping of local variables to values.
        is_global: whether the current scope is global
        """
        raise Exception("Not implemented.")

# subclasses of Node for expressions

class Var(Node):
    """Class of nodes representing accesses of variable."""
    fields = ['name']

    ##SW- Checks if variable name exists in local or global dictionary
    def eval(self, local_var_env):
        if (self.name in local_var_env):
            return local_var_env[self.name]
        elif(self.name in global_var_env):
            return global_var_env[self.name]
        else: raise EvalError()
    
class Int(Node):
    """Class of nodes representing integer literals."""
    fields = ['value']
    
    def eval(self, local_var_env): return self.value

class String(Node):
    """Class of nodes representing string literals."""
    fields = ['value']
    
    def eval(self, local_var_env): return self.value

class Array(Node):
    """Class of nodes representing array literals."""
    fields = ['elements']

    def eval(self, local_var_env): return [e.eval(local_var_env) for e in self.elements]
        
class Index(Node):
    """Class of nodes representing indexed accesses of arrays or strings."""
    fields = ['indexable', 'index']
    
    def eval(self, local_var_env):
        v1 = self.indexable.eval(local_var_env)
        v2 = self.index.eval(local_var_env)

        if not isinstance(v1,(str,list)): raise EvalError()
        if not isinstance(v2,int): raise EvalError()
        if v2 >= len(v1): raise EvalError()

        return v1[v2]

class BinOpExp(Node):
    """Class of nodes representing binary-operation expressions."""
    fields = ['left', 'op', 'right']
    
    def eval(self, local_var_env):
        v1 = self.left.eval(local_var_env)
        v2 = self.right.eval(local_var_env)
        
        if self.op == '+': 
            if isinstance(v1,int) and isinstance(v2,int): return v1 + v2
            if isinstance(v1,str) and isinstance(v2,str): return v1 + v2
            raise EvalError()
        
        if not isinstance(v1,int): raise EvalError()
        if not isinstance(v2,int): raise EvalError()

        if self.op == '-': return v1 - v2
        if self.op == '*': return v1 * v2

        if self.op == '/': 
            if v2 ==0: raise EvalError()
            return int(v1 / v2)

        if self.op == '==': return 1 if v1 == v2 else 0
        if self.op == '<':  return 1 if v1 < v2 else 0
        if self.op == '>':  return 1 if v1 > v2 else 0

        if self.op == 'and': return 1 if v1 and v2 else 0
        if self.op == 'or':  return 1 if v1 or v2 else 0

class UniOpExp(Node):
    """Class of nodes representing unary-operation expressions."""
    fields = ['op', 'arg']

    def eval(self, local_var_env):
        v = self.arg.eval(local_var_env)
        if not isinstance(v,int): raise EvalError()

        if self.op == 'not': return 0 if v else 1

# subclasses of Node for statements

class Print(Node):
    """Class of nodes representing print statements."""
    fields = ['exp']

    def anlz_procs(self): pass

    def exec(self, local_var_env, is_global):
        print(repr(self.exp.eval(local_var_env)))

class Assign(Node):
    """Class of nodes representing assignment statements."""
    fields = ['left', 'right']
    
    def anlz_procs(self): pass

    ##SW- Checks if global then whether left is an index or variable
    def exec(self, local_var_env, is_global):
        if not (is_global) and isinstance(self.left,Var):
                local_var_env[self.left.name]=self.right.eval(local_var_env)
        elif not (is_global) and isinstance(self.left,Index) and (self.left.indexable.name in local_var_env):
                local_var_env[self.left.indexable.name][self.left.index.eval(local_var_env)]=self.right.eval(local_var_env)
        else:
            if isinstance(self.left,Var):
                global_var_env[self.left.name]=self.right.eval(local_var_env)
            if isinstance(self.left,Index):
                global_var_env[self.left.indexable.name][self.left.index.eval(local_var_env)]=self.right.eval(local_var_env)
            
    
class Block(Node):
    """Class of nodes representing block statements."""
    fields = ['stmts']

    def anlz_procs(self):
        for s in self.stmts: s.anlz_procs()

    ##SW- For each stmts, calls exec
    def exec(self, local_var_env, is_global):
        for e in self.stmts:
            e.exec(local_var_env, is_global)

class If(Node):
    """Class of nodes representing if statements."""
    fields = ['exp', 'stmt']

    def anlz_procs(self): self.stmt.anlz_procs()

    ##SW- If condition is not 0 calls stmt.exec
    def exec(self, local_var_env, is_global):
        if(self.exp.eval(local_var_env)!=0): self.stmt.exec(local_var_env, is_global) 

class While(Node):
    """Class of nodes representing while statements."""
    fields = ['exp', 'stmt']

    def anlz_procs(self): self.stmt.anlz_procs()

    ##SW- If condition is not 0 calls exec on stmt then calls exec on itself
    def exec(self, local_var_env, is_global):
        if(self.exp.eval(local_var_env)!=0):
            self.stmt.exec(local_var_env, is_global)
            self.exec(local_var_env, is_global)

class Def(Node):
    """Class of nodes representing procedure definitions."""
    fields = ['name', 'params', 'body']

    def anlz_procs(self):
        if not self.name in proc_env:
            proc_env[self.name] = (self.params, self.body)
            self.body.anlz_procs()
        else: raise EvalError()

    ##SW- No work here
    def exec(self, local_var_env, is_global): pass
        

class Call(Node):
    """Class of nodes representing precedure calls."""
    fields = ['name', 'args']

    def anlz_procs(self): pass

    ##SW- Checks if length of args and param match, make a dict for local variables, assign params and run exec on body
    def exec(self, local_var_env, is_global):
        if(self.name in proc_env):
            if(len(self.args)!=len(proc_env[self.name][0])):
                raise EvalError()
            else:
                temp={}
                for x,y in zip(proc_env[self.name][0], self.args):
                    temp[x]=y.eval(local_var_env)
                proc_env[self.name][1].exec(temp, False)
        else: raise EvalError()
        
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


# Below is the driver code, which parses a given MustScript program,
# collects procedure definitions in the program, and executes the program.

# Open the input file, and read in the input program.
prog = open(sys.argv[1]).read()
##SW- prog = open('a4input2.txt').read()

try:
    # Try to parse the program.
    print('Parsing...')
    node = parse(prog)

    # Try to collect procedure definitions in the program.
    print('Collecting...')
    # proc_env: map from procedure names to their parameters and body
    proc_env = {}
    node.anlz_procs()

    # Try to execute the program.
    print('Executing...')
    # global_var_env: map from global variable names to their values
    # local_var_env: map from local variable names to their values
    # is_global: whether the current scope is global
    global_var_env, local_var_env, is_global = {}, {}, True
    node.exec(local_var_env, is_global)

# If an exception is rasied, print the appropriate error.
except tpg.Error:
    print('Parsing Error')

    # Uncomment the next line to re-raise the parsing error,
    # displaying where the error occurs.  Comment it for submission.

    # raise

except EvalError:
    print('Evaluation Error')

    # Uncomment the next line to re-raise the evaluation error, 
    # displaying where the error occurs.  Comment it for submission.

    # raise
