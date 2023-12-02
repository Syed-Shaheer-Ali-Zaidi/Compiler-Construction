global ST
global MT 
global DT

ST = []
MT = []
DT = []
stack = []

def insertST (N,T,S):
    if (len(T)>5):
        if(lookupST(N)==False):
            ST.append([N, T, S])
            return True
        else:
            print("ST Redeclaration at line ", TS[i][2])
            return False
    else:
        if(lookupFuncST(N)==False):
            ST.append([N, T, S])
            return True
        else:
            print("ST Function redeclaration at line",TS[i][2])
            return False
    
def insertDT (N, T, AM, CM, P):
    if(lookupDT(N)):
        DT.append(N, T, AM, CM, P)
        return True
    else:
        print("DT Redeclaration at line ", TS[i][2])
        return False
    
def insertMT (N, T, AM, TM, const, CN):
    if(lookupMT(N, CN)):
        MT.append(N, T, AM, TM, const, CN)
        return True
    else:
        print("MT Redeclaration at line ", TS[i][2])
        return False

def lookupST(N):
    for i in range(len(ST)):
        if(ST[i][0] == N):
            t = i
            temp = stack
            for j in range (len(stack)):
                if (ST[t][2]==temp.pop()):
                    return ST[t][1]
    return False
def lookupDT(N):
    return rowDT
def lookupMT(N, CN):
    return rowMT
def lookupFuncST(N, PL):
    for i in range(len(ST)):
        if(ST[i][0] == N and ST[i][1] == PL):
            t = i
            temp = stack
            ReTtype = []
            Ret = []
            for j in range (len(stack)):
                if (ST[t][2]==temp.pop()):
                    ReTtype = ST[t][1]
                    for i in range (len(ReTtype)):
                        if(ReTtype[i]==">"):
                            remaining = len(ReTtype) - i - 1
                            for j in remaining:
                                Ret.append(ReTtype[i+j+1])
                            return Ret
    return False

def lookupFuncMT(N, PL, CN):
    return rowDT
def Compatibility (left operand type, right operand type, operator):
    return type
def Compatibility (operand type, operator):
    return type