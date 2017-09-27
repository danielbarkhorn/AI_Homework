import resolve

class engine(object):

    def __init__(self):
        self.vars = dict()

    def tell(self, A):
        a = self.convertToCNF(A)
        resolve.addToResolve(self.vars, a, 1)

    def ask(self, A):
        if(isinstance(A, str)):
            a = ['not', A]
        else:
            a = self.convertToCNF(A)
            a = a.insert(0, 'not')
        if(self.engineResolve(a) == []):
            return True
        else:
            return False

    def clear(self):
        self.vars.clear

    def convertToCNF(self, A):
        ans = []
        if(A[0] == 'implies'):
            ans.append('or')
            ans.append(['not', A[1]])
            ans.append(A[2])
            return ans
        elif(A[0] == 'and'):
            ans.append('or')
            ans.append(['not', A[1]])
            ans.append(['not', A[2]])
            return ans
        elif(A[0] == 'biconditional'):
            ans1 = self.convertToCNF(['implies', A[0], A[1]])
            ans2 = self.convertToCNF(['implies', A[1], A[0]])
            ans = self.convertToCNF(['and', ans1, ans2])
            return ans
        return A

    def engineResolve(self, A):
        resolve.addToResolve(self.vars, A, 1)
        # Creating the entailed sentence
        ans = []
        for i in self.vars:
            if(self.vars[i] != 0):
                ans.append(i) if self.vars[i] else ans.append(str('not ' + i))
        if(len(ans) == len(self.vars)):
            print(ans, self.vars)
            return False
        if(len(ans) > 1):
            ans.insert(0, 'or')
        return ans
