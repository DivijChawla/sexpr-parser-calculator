
def skip_space(s, idx):
    while idx<len(s) and s[idx].isspace():
        idx+=1
    return idx


#a placeholder for now
def parse_atom(s):
    # TODO: actually implement this
    import json
    try:
        return ['val', json.loads(s)]  #checks if valid json datatype and adds val tag to it... '""' also works - valid json string
    except json.JSONDecodeError:
        return s


'''
parse_expr takes a string input (s) and an offset index (idx). It iterates over the input, advancing the index until encountering an error or the end of the S-expression.

It distinguishes between an atom and a list by examining the first non-whitespace character.
'''


def parse_expr(s: str, idx: int):
    idx = skip_space(s, idx)
    if s[idx]=="(":
        #a list... parse recursively until a closing paranthesis is found
        idx +=1 #else will keep detecting ( over and over again as s[idx].isspace() wont work and wil keep returning index of the first opening paranthesis
        l = []
        while True:   #runs till s[idx]=")" is reached
            idx = skip_space(s,idx)
            if idx > len(s):
                raise Exception("unbalanced paranthesis")
            
            if s[idx] == ")":   
                idx +=1  #why?
                break

            idx, v = parse_expr(s,idx)  #  calls the parse_expr function with the arguments s and idx, and it expects that the function returns a tuple with two elements. The returned tuple is then unpacked into the variables idx and v.

            l.append(v)

        return idx, l

    elif s[idx]==")":
        raise Exception("bad paranthesis,  ')' without matching '(' ")
    else:
        #an atom...
        start = idx
        while idx<len(s) and (not s[idx].isspace()) and s[idx] not in '()':
            idx+=1
        if start == idx:
            raise Exception("empty program")
        
        return idx, parse_atom(s[start:idx])


#we need to check that the input is fully exhausted:
def pl_parse(s):
    idx, node = parse_expr(s,0)
    idx = skip_space(s, idx)
    if idx < len(s):
        raise ValueError('trailing garbage')
    return node

    
def pl_eval(node):
    if len(node) == 0:
        raise ValueError("empty list")

    if len(node) == 2 and node[0] == "val":
        return node[1]
    
    #binary operators
    import operator
    binops = {
        '+':operator.add,
        '-':operator.sub,
        '*':operator.mul,
        '/':operator.truediv,
        'eq':operator.eq,
        'ne':operator.ne,
        'ge':operator.ge,
        'gt':operator.gt,
        'le':operator.le,
        'lt':operator.lt,
        'and':operator.and_,
        'or':operator.or_
    }

    if len(node)==3 and node[0] in binops:
        op = binops[node[0]]
        return op(pl_eval(node[1]), pl_eval(node[2]))
    
    #unary operators (single oprand)
    unops = {
        '-': operator.neg,
        'not': operator.not_,
    }


    if len(node)==2 and node[0] in unops:
        op = unops[node[0]]
        return op(pl_eval(node[1]))
    
    if len(node) == 4 and node[0] == '?':
        _, cond, yes, no = node         #unpacks the four elements of node into variables
        if pl_eval(cond):
            return pl_eval(yes)
        else:
            return pl_eval(no)

    # print
    if node[0] == 'print':
        return print(*(pl_eval(val) for val in node[1:]))

    raise ValueError('unknown expression')


def test_eval():
    def f(s):
        return pl_eval(pl_parse(s))
    print(f('1'))
    print(f('(+ 1 3)') )
    print(f('(? (lt 1 3) "yes" "no")'))
    f('(print  "divij" 21 1)')

test_eval()
