# Made by Dan Barkhorn

operators = ['not', 'implies', 'and', 'or', 'biconditional']
def resolve(A, B):
    vars = dict()

    addToResolve(vars, A, 1)
    addToResolve(vars, B, 1)

    # Creating the entailed sentence
    ans = []
    for i in vars:
        if(vars[i] != 0):
            ans.append(i) if vars[i] else ans.append(str('not ' + i))
    if(len(ans) == len(vars)):
        print(ans, vars)
        return False
    if(len(ans) > 1):
        ans.insert(0, 'or')
    return ans

def addToResolve(vars, A, sign):
    if(isinstance(A, str)):
        if(A in vars.keys()):
            if(vars[A]!=sign):
                vars[A] = 0
        else:
            vars[A] = sign
    else:
        for i in A:
            if(i != 'or'):
                if(isinstance(i, str)):
                    if(i == 'not'):
                        sign *= -1
                    elif(i in vars.keys()):
                        if(vars[i]!=sign):
                            vars[i] = 0
                    else:
                        vars[i] = sign
                elif(not isinstance(i, str)):
                    addToResolve(vars, i, sign)
        sign = 1
