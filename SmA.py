global ST
global MT 
global DT
global scope

ST = []
MT = []
DT = []
stack = []
scope = 0

def insertST (N,T,S):
    if (len(T)>5):
        if(lookupFuncST(N)==False):
            ST.append([N, T, S])
            return True
        else:
            print("ST Function redeclaration at line ", TS[i][2])
            return False
    else:
        if(lookupST(N)==False):
            ST.append([N, T, S])
            return True
        else:
            print("ST Redeclaration at line ", TS[i][2])
            return False
    
def insertDT (N, AM, CM, P):
    if(lookupDT(N)==False):
        DT.append([N, AM, CM, P])
        return True
    else:
        print("DT Redeclaration at line ", TS[i][2])
        return False
    
def insertMT (N, T, AM, const, CN):
    if(len(T)>5):
        if(lookupFuncMT(N, CN)==False):
            MT.append([N, T, AM, const, CN])
            return True
        else:
            print("MT Function Redeclaration at line ", TS[i][2])
            return False
    else:
        if(lookupMT(N, CN)==False):
            MT.append([N, T, AM, const, CN])
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
    for i in range(len(DT)):
        if(DT[i][0] == N):
            return DT[i]
    return False

def lookupMT(N, CN):
    for i in range(len(MT)):
        if((MT[i][0] == N and MT[i][5] == CN)):
            return MT[i]
    return False

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
    for i in range(len(MT)):
        if((MT[i][0] == N and MT[i][5] == CN and MT[i][1]== PL)):
            return MT[i]
    return False

# def Compatibility (LOT, ROT, OP):
#     if OP in ['+', '-', '*', '/', '%']:
#         if (OP == '+' and LOT is 'text' and ROT is 'text'):
#             T = "text"
#             return T
#         elif (OP == '+' and LOT is 'char' and ROT is 'char'):
#             T= "text"
#             return T
#         elif (OP == '-' and LOT is 'int' and ROT is 'int'):
#             T= "int"
#             return T

def Compatibility(OP, LOT, ROT):
    type_combinations = {

    ('+', 'text', 'text'): 'text',    # "abc" + "def"
    ('+', 'char', 'char'): 'text',    # 'a' + 'b'
    ('+', 'int', 'int'): 'int',        # 1 + 1
    ('+', 'flt', 'flt'): 'flt',        # 1.1 + 1.2
    ('+', 'int', 'flt'): 'flt',        # 1 + 2.1
    ('+', 'flt', 'int'): 'flt',        # 1.1 + 2
    ('+', 'logic', 'logic'): 'int',     # True + True
    ('+', 'logic', 'int'): 'int',       # True + 1
    ('+', 'int', 'logic'): 'int',       # 1 + True
    ('+', 'logic', 'flt'): 'flt',       # True + 1.1
    ('+', 'flt', 'logic'): 'flt',       # 1.1 + True

    ('-', 'int', 'int'): 'int',        # 1 - 1
    ('-', 'flt', 'flt'): 'flt',        # 1.1 - 1.2
    ('-', 'int', 'flt'): 'flt',        # 1 - 2.1
    ('-', 'flt', 'int'): 'flt',        # 1.1 - 2
    ('-', 'logic', 'logic'): 'int',     # True - True
    ('-', 'logic', 'int'): 'int',       # True - 1
    ('-', 'int', 'logic'): 'int',       # 1 - True
    ('-', 'logic', 'flt'): 'flt',       # True - 1.1
    ('-', 'flt', 'logic'): 'flt',       # 1.1 - True

    ('*', 'int', 'int'): 'int',        # 1 * 1
    ('*', 'flt', 'flt'): 'flt',        # 1.1 * 1.2
    ('*', 'int', 'flt'): 'flt',        # 1 * 2.1
    ('*', 'flt', 'int'): 'flt',        # 1.1 * 2
    ('*', 'logic', 'logic'): 'int',   # True * True
    ('*', 'logic', 'int'): 'int',       # True * 1
    ('*', 'int', 'logic'): 'int',       # 1 * True
    ('*', 'logic', 'flt'): 'flt',       # True * 1.1
    ('*', 'flt', 'logic'): 'flt',       # 1.1 * True

    ('/', 'int', 'int'): 'flt',        # 1 / 1
    ('/', 'flt', 'flt'): 'flt',        # 1.1 / 1.2
    ('/', 'int', 'flt'): 'flt',        # 1 / 2.1
    ('/', 'flt', 'int'): 'flt',        # 1.1 / 2
    ('/', 'logic', 'logic'): 'int',   # True / True
    ('/', 'logic', 'int'): 'int',       # True / 1
    ('/', 'int', 'logic'): 'int',       # 1 / True
    ('/', 'logic', 'flt'): 'flt',       # True / 1.1
    ('/', 'flt', 'logic'): 'flt',       # 1.1 / True

    ('**', 'int', 'int'): 'int',        # 2^2
    ('**', 'flt', 'flt'): 'flt',        # 2.2^1.1
    ('**', 'int', 'flt'): 'flt',        # 2^1.1
    ('**', 'flt', 'int'): 'flt',        # 1.1^2
    ('**', 'logic', 'logic'): 'int',   # True^True
    ('**', 'logic', 'int'): 'int',       # True^2
    ('**', 'int', 'logic'): 'int',       # 2^True
    ('**', 'logic', 'flt'): 'flt',       # True^1.1
    ('**', 'flt', 'logic'): 'flt',       # 1.1^True

    ('%', 'int', 'int'): 'flt',        # 1 % 1
    ('%', 'flt', 'flt'): 'flt',        # 1.1 % 1.2
    ('%', 'int', 'flt'): 'flt',        # 1 % 2.1
    ('%', 'flt', 'int'): 'flt',        # 1.1 % 2
    ('%', 'logic', 'logic'): 'flt',     # True % True
    ('%', 'logic', 'int'): 'flt',       # True % 1
    ('%', 'int', 'logic'): 'flt',       # 1 % True
    ('%', 'logic', 'flt'): 'flt',       # True % 1.1
    ('%', 'flt', 'logic'): 'flt',       # 1.1 % True

    ('<', 'int', 'int'): 'logic',       # 1 < 1
    ('<', 'flt', 'flt'): 'logic',       # 1.1 < 1.2
    ('<', 'int', 'flt'): 'logic',       # 1 < 2.1
    ('<', 'flt', 'int'): 'logic',       # 1.1 < 2
    ('<', 'logic', 'logic'): 'logic',   # True / True
    ('<', 'logic', 'int'): 'logic',       # True / 1
    ('<', 'int', 'logic'): 'logic',       # 1 / True
    ('<', 'logic', 'flt'): 'logic',       # True / 1.1
    ('<', 'flt', 'logic'): 'logic',       # 1.1 / True

    ('>', 'int', 'int'): 'logic',       # 1 > 1
    ('>', 'flt', 'flt'): 'logic',       # 1.1 > 1.2
    ('>', 'int', 'flt'): 'logic',       # 1 > 2.1
    ('>', 'flt', 'int'): 'logic',       # 1.1 > 2
    ('>', 'logic', 'logic'): 'logic',   # True / True
    ('>', 'logic', 'int'): 'logic',       # True / 1
    ('>', 'int', 'logic'): 'logic',       # 1 / True
    ('>', 'logic', 'flt'): 'logic',       # True / 1.1
    ('>', 'flt', 'logic'): 'logic',       # 1.1 / True

    ('<=', 'int', 'int'): 'logic',       # 1 < 1
    ('<=', 'flt', 'flt'): 'logic',       # 1.1 < 1.2
    ('<=', 'int', 'flt'): 'logic',       # 1 < 2.1
    ('<=', 'flt', 'int'): 'logic',       # 1.1 < 2
    ('<=', 'logic', 'logic'): 'logic',   # True / True
    ('<=', 'logic', 'int'): 'logic',       # True / 1
    ('<=', 'int', 'logic'): 'logic',       # 1 / True
    ('<=', 'logic', 'flt'): 'logic',       # True / 1.1
    ('<=', 'flt', 'logic'): 'logic',       # 1.1 / True

    ('>=', 'int', 'int'): 'logic',       # 1 > 1
    ('>=', 'flt', 'flt'): 'logic',       # 1.1 > 1.2
    ('>=', 'int', 'flt'): 'logic',       # 1 > 2.1
    ('>=', 'flt', 'int'): 'logic',       # 1.1 > 2
    ('>=', 'logic', 'logic'): 'logic',   # True / True
    ('>=', 'logic', 'int'): 'logic',       # True / 1
    ('>=', 'int', 'logic'): 'logic',       # 1 / True
    ('>=', 'logic', 'flt'): 'logic',       # True / 1.1
    ('>=', 'flt', 'logic'): 'logic',       # 1.1 / True

    ('==', 'int', 'int'): 'logic',      # 1 == 1
    ('==', 'flt', 'flt'): 'logic',      # 1.1 == 1.2
    ('==', 'int', 'flt'): 'logic',      # 1 == 2.1
    ('==', 'flt', 'int'): 'logic',      # 1.1 == 2
    ('==', 'logic', 'logic'): 'logic',   # True / True
    ('==', 'logic', 'int'): 'logic',       # True / 1
    ('==', 'int', 'logic'): 'logic',       # 1 / True
    ('==', 'logic', 'flt'): 'logic',       # True / 1.1
    ('==', 'flt', 'logic'): 'logic',       # 1.1 / True

    ('!=', 'int', 'int'): 'logic',      # 1 != 1
    ('!=', 'flt', 'flt'): 'logic',      # 1.1 != 1.2
    ('!=', 'int', 'flt'): 'logic',      # 1 != 2.1
    ('!=', 'flt', 'int'): 'logic',      # 1.1 != 2
    ('!=', 'logic', 'logic'): 'logic',   # True / True
    ('!=', 'logic', 'int'): 'logic',       # True / 1
    ('!=', 'int', 'logic'): 'logic',       # 1 / True
    ('!=', 'logic', 'flt'): 'logic',       # True / 1.1
    ('!=', 'flt', 'logic'): 'logic',       # 1.1 / True

    ('and', 'logic', 'logic'): 'logic',       # True and True

    ('or', 'logic', 'logic'): 'logic',       # True or True

    ('=', 'int', 'int'): 'logic',      # 1 == 1
    ('=', 'flt', 'flt'): 'logic',      # 1.1 == 1.2
    ('=', 'logic', 'logic'): 'logic',   # True / True
    ('=', 'char', 'char'): 'logic',       # 1.1 / True
    ('=', 'text', 'text'): 'logic',       # 1.1 / True
    
    }

    # Check if the combination is in the dictionary
    if (OP, LOT, ROT) in type_combinations:
        return type_combinations[(OP, LOT, ROT)]
    else:
        # Handle unsupported combinations
        print ("Type Mismatch")
        return False

def Compatibility (OP, OT):

    type_combinations = {
          ('not', 'logic'): 'logic'
    }

    # Check if the combination is in the dictionary
    if (OP, OT) in type_combinations:
        return type_combinations[(OP, OT)]
    else:
        # Handle unsupported combinations
        print ("Type Mismatch")
        return False

def CreateScope():
    stack.append(scope)
    scope+=1

def DestroyScope():
    stack.pop()