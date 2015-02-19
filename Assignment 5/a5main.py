import sys
import tpg

################################
#ASSIGNMENT 5, Due Date: May.02#
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

# subclasses of Node for expressions

class Var(Node):
    """Class of nodes representing accesses of variable."""
    fields = ['name']
    
class Int(Node):
    """Class of nodes representing integer literals."""
    fields = ['value']
    
class String(Node):
    """Class of nodes representing string literals."""
    fields = ['value']
    
class Array(Node):
    """Class of nodes representing array literals."""
    fields = ['elements']

class Index(Node):
    """Class of nodes representing indexed accesses of arrays or strings."""
    fields = ['indexable', 'index']

class BinOpExp(Node):
    """Class of nodes representing binary-operation expressions."""
    fields = ['left', 'op', 'right']
    
class UniOpExp(Node):
    """Class of nodes representing unary-operation expressions."""
    fields = ['op', 'arg']

# subclasses of Node for statements

class Print(Node):
    """Class of nodes representing print statements."""
    fields = ['exp']

class Assign(Node):
    """Class of nodes representing assignment statements."""
    fields = ['left', 'right']
    
class Block(Node):
    """Class of nodes representing block statements."""
    fields = ['stmts']

class If(Node):
    """Class of nodes representing if statements."""
    fields = ['exp', 'stmt']

class While(Node):
    """Class of nodes representing while statements."""
    fields = ['exp', 'stmt']

class Def(Node):
    """Class of nodes representing procedure definitions."""
    fields = ['name', 'params', 'body']

class Call(Node):
    """Class of nodes representing precedure calls."""
    fields = ['name', 'args']

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


def anlz_procs_imp(node):
    """Analyze procedure definitions and calls."""
    if isinstance(node, (Print, Assign)): pass
    elif isinstance(node, Block):
        for s in node.stmts: anlz_procs_imp(s)
    elif isinstance(node, (If, While)):
        anlz_procs_imp(node.stmt)
    elif isinstance(node, Def):
        if node.name in proc_defined: raise AnalError()
        print('Definition of procedure', node.name)
        proc_defined.add(node.name)
        anlz_procs_imp(node.body)
    elif isinstance(node, Call):
        print('Call of procedure', node.name)
        proc_called.add(node.name)
    else: raise Exception("Not implemented.")


def anlz_vars_imp(node, local_var_env, is_global):
    """Analyze variable definitions and uses."""
    if isinstance(node, Var):
        if node.name not in local_var_env | global_var_env: raise AnalError()
        print('Use of variable', node.name)
    elif isinstance(node, (Int, String)): pass
    elif isinstance(node, Array):
        for e in node.elements: anlz_vars_imp(e, local_var_env, is_global)
    elif isinstance(node, Index):
        anlz_vars_imp(node.indexable, local_var_env, is_global)
        anlz_vars_imp(node.index, local_var_env, is_global)
    elif isinstance(node, BinOpExp):
        anlz_vars_imp(node.left, local_var_env, is_global)
        anlz_vars_imp(node.right, local_var_env, is_global)
    elif isinstance(node, UniOpExp):
        anlz_vars_imp(node.arg, local_var_env, is_global)
    elif isinstance(node, Print):
        anlz_vars_imp(node.exp, local_var_env, is_global)
    elif isinstance(node, Assign):
        anlz_vars_imp(node.right, local_var_env, is_global)
        if isinstance(node.left, Var):
            if is_global: global_var_env.add(node.left.name)
            else: local_var_env.add(node.left.name)
            print('Definition of variable', node.left.name)
            if not is_global and node.left.name in global_var_env:
                print('Shadowing of global variable', node.left.name)
        if isinstance(node.left, Index):
            anlz_vars_imp(node.left, local_var_env, is_global)
    elif isinstance(node, Block):
        for s in node.stmts: anlz_vars_imp(s, local_var_env, is_global)
    elif isinstance(node, (If, While)):
        anlz_vars_imp(node.exp, local_var_env, is_global)
        anlz_vars_imp(node.stmt, local_var_env, is_global)
    elif isinstance(node, Def):
        new_local_var_env = set(node.params)
        print('Locals of procedure', node.name+':', ', '.join(node.params))
        for v in new_local_var_env & global_var_env:
            print('Shadowing of global variable', v)
        anlz_vars_imp(node.body, new_local_var_env, False)
    elif isinstance(node, Call):
        for a in node.args: anlz_vars_imp(a, local_var_env, is_global)
    else: raise Exception("Not implemented.")

#Functional
def anlz_procs_fun(node,proc_defined,proc_called):
    
    if isinstance(node, (Print, Assign)): pass
    elif isinstance(node, Block):
        t=anlz_procs_block_fun(node, 1, proc_defined,proc_called)
        proc_defined = proc_defined|t[0]
        proc_called = proc_called|t[1]
    elif isinstance(node, (If, While)):
        t=anlz_procs_fun(node.stmt,proc_defined,proc_called)
        proc_defined = proc_defined|t[0]
        proc_called = proc_called|t[1]
    elif isinstance(node, Def):
        try:
            if node.name in proc_defined: raise AnalError()
            print('Definition of procedure', node.name)
            proc_defined = proc_defined|set([node.name])
            t=anlz_procs_fun(node.body,proc_defined,proc_called)
            proc_defined = proc_defined|t[0]
            proc_called = proc_called|t[1]
        except AnalError:
            print('Analysis Error')
            pass
    elif isinstance(node, Call):
        print('Call of procedure', node.name)
        proc_called = proc_called|set([node.name])
    else: raise Exception("Not implemented.")

    return (proc_defined ,proc_called)

#Calls 2 functions to check for undefined procedure calls and uncalled procedures.
def anlz_procs_errors(tup):
    anlz_undef_procs(tup)
    anlz_uncall_procs(tup)

#The 2 functions below checks set 'a' to see if it exists in set 'b', if not raise error.
def anlz_undef_procs(tup):
    temp=tup[0]|set()
    if not len(temp)<1:
        t = temp.pop()
        try:
            if (t not in tup[1]): raise AnalError()
        except AnalError:
            print('Analysis Error')
            pass
        anlz_undef_procs((temp,tup[1]))
        
def anlz_uncall_procs(tup):
    temp=tup[1]|set()
    if not len(temp)<1:
        t = temp.pop()
        try:
            if (t not in tup[0]): raise AnalError()
        except AnalError:
            print('Analysis Error')
            pass
        anlz_uncall_procs((tup[0],temp))

#Helper function to recursively call information within a block of code.
def anlz_procs_block_fun(block, num, proc_defined ,proc_called):
    if not len(block.stmts)<num:
        t1=anlz_procs_fun(block.stmts[num-1], proc_defined,proc_called)
        proc_defined=proc_defined|t1[0]
        proc_called=proc_called|t1[1]
        t2=anlz_procs_block_fun(block, num+1, proc_defined,proc_called)
        proc_defined=proc_defined|t2[0]
        proc_called=proc_called|t2[1]
    return (proc_defined ,proc_called)

#Helper function to iterate through a set and call analyze variable on it and finally returning a set of the results.
def anlz_lst_fun(lst ,num ,local_var_env ,is_global, glbal):
    if not len(lst)<num:
        local_var_env=anlz_vars_fun(lst[num-1],local_var_env,is_global, glbal)
        local_var_env=anlz_lst_fun(lst ,num+1 ,local_var_env ,is_global, glbal)
    return local_var_env

#Similar to the function above but for global variables.
def anlz_lstz_fun(lst ,num ,local_var_env ,is_global):
    global_var_env=set()
    if not len(lst)<num:
        global_var_env=global_var_env|anlz_global_fun(lst[num-1],local_var_env,is_global)
        global_var_env=global_var_env|anlz_lstz_fun(lst ,num+1 ,local_var_env ,is_global)
    return global_var_env

#The variable analyzing function.
def anlz_vars_fun(node, local_var_env, is_global, global_var_env):
    
    if isinstance(node, Var):
        try:
            if node.name not in local_var_env | global_var_env: raise AnalError()
            print('Use of variable', node.name)
        except AnalError:
            print('Analysis Error')
            pass
    elif isinstance(node, (Int, String)): pass
    elif isinstance(node, Array):
        local_var_env=local_var_env|anlz_lst_fun(node.elements, 1, local_var_env, is_global, global_var_env)
    elif isinstance(node, Index):
        local_var_env=local_var_env|anlz_vars_fun(node.indexable, local_var_env, is_global, global_var_env)
        local_var_env=local_var_env|anlz_vars_fun(node.index, local_var_env, is_global, global_var_env)
    elif isinstance(node, BinOpExp):
        local_var_env=local_var_env|anlz_vars_fun(node.left, local_var_env, is_global, global_var_env)
        local_var_env=local_var_env|anlz_vars_fun(node.right, local_var_env, is_global, global_var_env)
    elif isinstance(node, UniOpExp):
        local_var_env=local_var_env|anlz_vars_fun(node.arg, local_var_env, is_global, global_var_env)
    elif isinstance(node, Print):
        local_var_env=local_var_env|anlz_vars_fun(node.exp, local_var_env, is_global, global_var_env)
    elif isinstance(node, Assign):
        local_var_env=local_var_env|anlz_vars_fun(node.right, local_var_env, is_global, global_var_env)
        if isinstance(node.left, Var):
            if is_global:
                print('Definition of variable', node.left.name)
            else:
                local_var_env=local_var_env|set([node.left.name])
                print('Definition of variable', node.left.name)
            if not is_global and node.left.name in global_var_env:
                print('Shadowing of global variable', node.left.name)
        if isinstance(node.left, Index):
            local_var_env=local_var_env|anlz_vars_fun(node.left, local_var_env, is_global, global_var_env)
    elif isinstance(node, Block):
        local_var_env=local_var_env|anlz_lst_fun(node.stmts,1,local_var_env,is_global, global_var_env)
    elif isinstance(node, (If, While)):
        local_var_env=local_var_env|anlz_vars_fun(node.exp, local_var_env, is_global, global_var_env)
        local_var_env=local_var_env|anlz_vars_fun(node.stmt, local_var_env, is_global, global_var_env)
    elif isinstance(node, Def):
        new_local_var_env = set(node.params)
        print('Locals of procedure', node.name+':', ', '.join(node.params))
        anlz_shadowing_fun(new_local_var_env, global_var_env)
        anlz_vars_fun(node.body, new_local_var_env, False, global_var_env)
    elif isinstance(node, Call):
        local_var_env=local_var_env|anlz_lst_fun(node.args,1,local_var_env,is_global, global_var_env)#
    else: raise Exception("Not implemented.")

    return local_var_env

#Helper method to check for shadowing.
def anlz_shadowing_fun(local, glbal):
    localtemp=local|set()
    if len(localtemp)>0:
        t = localtemp.pop()
        if t in glbal: print('Shadowing of global variable', t)
        anlz_shadowing_fun(localtemp,glbal)

#Method that first looks through all the nodes to create a set of global variables.
def anlz_global_fun(node, local_var_env, is_global):
    global_var_env=set()
    
    if isinstance(node, Var): pass
    elif isinstance(node, (Int, String)): pass
    elif isinstance(node, Array):
        global_var_env=global_var_env|anlz_lstz_fun(node.elements, 1, local_var_env, is_global)
    elif isinstance(node, Index):
        global_var_env=global_var_env|anlz_global_fun(node.indexable, local_var_env, is_global)
        global_var_env=global_var_env|anlz_global_fun(node.index, local_var_env, is_global)
    elif isinstance(node, BinOpExp):
        global_var_env=global_var_env|anlz_global_fun(node.left, local_var_env, is_global)
        global_var_env=global_var_env|anlz_global_fun(node.right, local_var_env, is_global)
    elif isinstance(node, UniOpExp):
        global_var_env=global_var_env|anlz_global_fun(node.arg, local_var_env, is_global)
    elif isinstance(node, Print):
        global_var_env=global_var_env|anlz_global_fun(node.exp, local_var_env, is_global)
    elif isinstance(node, Assign):
        global_var_env=global_var_env|anlz_global_fun(node.right, local_var_env, is_global)
        if isinstance(node.left, Var):
            if is_global:
                global_var_env=global_var_env|set([node.left.name])
        if isinstance(node.left, Index):
            global_var_env=global_var_env|anlz_global_fun(node.left, local_var_env, is_global)
    elif isinstance(node, Block):
        global_var_env=global_var_env|anlz_lstz_fun(node.stmts,1,local_var_env,is_global)
    elif isinstance(node, (If, While)):
        global_var_env=global_var_env|anlz_global_fun(node.exp, local_var_env, is_global)
        global_var_env=global_var_env|anlz_global_fun(node.stmt, local_var_env, is_global)
    elif isinstance(node, Def):
        new_local_var_env = set(node.params)
        global_var_env=global_var_env|anlz_global_fun(node.body, new_local_var_env, False)
    elif isinstance(node, Call):
        global_var_env=global_var_env|anlz_lstz_fun(node.args,1,local_var_env,is_global)
    else: raise Exception("Not implemented.")
    
    return global_var_env

# Below is the driver code, which parses a given MustScript program
# and analyzes the definitions and uses of procedures and variables

# Open the input file, and read in the input program.
#prog = open(sys.argv[1]).read()
prog = open('a5input3.txt').read()

try:
    # Try to parse the program.
    print('Parsing...')
    node = parse(prog)

    # Try to analyze the program.
    print('Analyzing...')

    # set up and call method for analyzing procedures (imperative)
    #proc_defined, proc_called = set(), set()
    #anlz_procs_imp(node)
    #if {p for p in proc_called if p not in proc_defined}:
    #    raise AnalError('containing call to undefined procedure')
    #if {p for p in proc_defined if p not in proc_called}: # bonus dead code
    #    raise AnalError('containing definition of not-called procedure')
    
    # set up and call method for analyzing variables (imperative)
    #global_var_env, local_var_env, is_global = set(), set(), True
    #anlz_vars_imp(node, local_var_env, is_global)

    # set up and call method for analyzing procedures (functional)
    proc_defined,proc_called = set(), set()
    anlz_procs_errors(anlz_procs_fun(node,proc_defined,proc_called))
    # set up and call method for analyzing variables (functional)
    local_var_env = set()
    anlz_vars_fun(node, local_var_env, True, anlz_global_fun(node, local_var_env,True))
    # your methods could be named anlz_procs_fun and anlz_vars_fun

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

    #raise
