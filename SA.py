import lexical_analyzer as LA
f = open('D:\\Shaheer\\Compiler Construction\\Compiler-Construction\\code.txt', 'r')
code = f.read()
TS = LA.breakWords(code)

global ST
global MT 
global DT
global scope
global stack

ST = []
MT = []
DT = []
stack = []
scope = 0

def insertST (N,T,S, i):
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
    
def insertDT (N, T, AM, CM, P, i):
    if(lookupDT(N)==False):
        DT.append([N, T, AM, CM, P])
        return True
    else:
        print("DT Redeclaration at line ", TS[i][2])
        return False
    
def insertMT (N, T, AM, TM, const, CN, i):
    if(len(T)>5):
        if(lookupFuncMT(N, CN)==False):
            MT.append([N, T, AM, TM, const, CN])
            return True
        else:
            print("MT Function Redeclaration at line ", TS[i][2])
            return False
    else:
        if(lookupMT(N, CN)==False):
            MT.append([N, T, AM, TM, const, CN])
            return True
        else:
            print("MT Redeclaration at line ", TS[i][2])
            return False

def lookupST(N):
    for i in range(len(ST)):
        if(ST[i][0] == N):
            t = i
            temp = stack
            counter = -1
            for j in range (len(stack)):
                if (ST[t][2]==temp[counter]):
                    return ST[t][1]
                counter -=1
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
            counter = -1
            for j in range (len(stack)):
                if (ST[t][2]==temp[counter]):
                    ReTtype = ST[t][1]
                    for i in range (len(ReTtype)):
                        if(ReTtype[i]==">"):
                            remaining = len(ReTtype) - i - 1
                            for j in remaining:
                                Ret.append(ReTtype[i+j+1])
                            return Ret
            counter -= 1
    return False

def lookupFuncMT(N, PL, CN):
    for i in range(len(MT)):
        if((MT[i][0] == N and MT[i][5] == CN and MT[i][1]== PL)):
            return MT[i]
    return False

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
    global scope
    stack.append(scope)
    scope+=1

def DestroyScope():
    stack.pop()

def const(i):
    if (TS[i][0] == "INTCONST"):
        return i + 1, True
    if (TS[i][0] == "FLTCONST"):
        return i + 1, True
    if (TS[i][0] == "CHRCONST"):
        return i + 1, True
    if (TS[i][0] == "TEXTCONST"):
        return i + 1, True
    if (TS[i][0] == "LOGICCONST"):
        return i + 1, True
    print("Invalid Constant at ", TS[i][1], " in line number ", TS[i][2])
    return i, False 
    

def list2(i, T):
    if (TS[i][0] == ";"):
        return i + 1, True
    if (TS[i][0] == "comma"):
        i+=1
        if (TS[i][0] == "ID"):
            N = TS[i][1]
            insertST(N, T, stack[-1], i)
            i+=1
            if (TS[i][0] == "comma" or TS[i][0] == ";" or TS[i][0] == "SAO"):
                i, listLogic = list(i, T)
                if (listLogic):
                    return i, True
                else:
                    return i, False
            else:
                print("Error, expected a , or ; or = at ", TS[i][1], " in line number ", TS[i][2])
                return i, False
        else:
            print("Error, expected an identifier at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        print("Error, expected a ; or , at ", TS[i][2], " in line number ", TS[i][2])
        return i, False

def init(i, T):
    if (TS[i][0] == "ID"):
        N = TS[i][1]
        if(lookupST(N)==False):
            print("Undeclared variable ", N, " at line number ", TS[i][2])
        i+=1
        if (TS[i][0] == "comma" or TS[i][0] == ";" or TS[i][0] == "SAO"):
            i, listLogic = list(i, T)
            if(listLogic):
                return i, True
            else:
                return i, False
        else:
            print("Error, expected a , or ; or = at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    if(TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
        i, const_logic = const(i)
        if (const_logic):
            if (TS[i][0] == ";" or TS[i][0] == "comma"):
                i, list2Logic = list2(i, T)
                if(list2Logic):
                    return i, True
                else:
                    return i, False
            else:
                print("Error, expected a , or ; at ", TS[i][1], " in line number ", TS[i][2])
        else:
            return i, False
    else:
        print("Error, expected an identifier or constant at ", TS[i][1], " in line number ", TS[i][2])
        return i, False


def list(i, T):
    if (TS[i][0] == "comma"):
        i+=1
        if (TS[i][0] == "ID"):
            N = TS[i][1]
            insertST(N, T, stack[-1], i)
            i+=1
            if (TS[i][0] == "comma" or TS[i][0] == ";" or TS[i][0] == "SAO"):
                i, listLogic = list(i, T)
                if(listLogic):
                    return i, True
                else:
                    return i, False
            else:
                print("Error, expected , or ; or = at ", TS[i][1], " in line number ", TS[i][2])
                return i, False
        else:
            print("Error, expected an identifier at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    elif (TS[i][0] == ";"):
        return i + 1, True
    elif (TS[i][0] == "SAO"):
        i+=1    
        if (TS[i][0] == "ID" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, initLogic = init(i, T)
            if(initLogic):
                return i, True
            else:
                return i, False
        else:
            print("Error, expected an identifier or constant at ", TS[i][1], " at line number ", TS[i][2])
            return i, False
    else:
        print("Error, expected a , or ; or = at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def Decl(i):
    if (TS[i][0] == "DT"):
        T = TS[i][1]
        i+=1
        if (TS[i][0] == "ID"):
            N = TS[i][1]
            insertST(N, T, stack[-1], i)
            i+=1
            if (TS[i][0] == "comma" or TS[i][0] == ";" or TS[i][0] == "SAO"):
                i, listLogic = list(i, T)
                if(listLogic):
                    return i, True
                else:
                    return i, False
            else:
                print("Error, expected , or ; or = at ", TS[i][1], " in line number ", TS[i][2])
                return i, False
        else:
            print ("Error, invalid Identifier at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        print ("Error, invalid DataType at ", TS[i][1], " in line number ", TS[i][2])
        return i, False


def new(i):
    if (TS[i][0] == "comma"):
        i+=1
        if (TS[i][0]=="ID" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST" or TS[i][0] == "ORB" or TS[i][0] == "not"):
            i, OElogic = OE(i)
            if (OElogic):
                i, newlogic = new(i)
                if (newlogic):
                    return i, True
                else:
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        return i, True

def args(i):
    if (TS[i][0]=="ID" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST" or TS[i][0] == "ORB" or TS[i][0] == "not"):
        i, OElogic = OE(i)
        if (OElogic):
            i, newlogic = new(i)
            if (newlogic):
                return i, True
            else:
                return i, False
        else:
            return i, False
    return i, True

def fn_call(i):
    i, IDcomplogic = IDcomp(i)
    if (IDcomplogic):
        if (TS[i][0] == "ORB"):
            i+=1
            i, argslogic = args(i)
            if (argslogic):
                if (TS[i][0] == "CRB"):
                    i+=1
                    if (TS[i][0] == ";"):
                        return i + 1, True
                    else:
                        print("Error, expected a ; at ", TS[i][1], " in line number ", TS[i][2])
                        return i, False
                else:
                    print("Error, expected a ) at ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected a ( at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        return i, False


def IDcomp(i):
    if (TS[i][0] == "dot"):
                i+=1
                if (TS[i][0] == "ID"):
                    i+=1
                    i, IDcomplogic = IDcomp(i)
                    if (IDcomplogic):
                        return i, True
                    else:
                        return i, False
                else:
                    print("Error, invalid identifier at ", TS[i][1], " in line number ", TS[i][2])
                    return i, False               
    elif (TS[i][0] == "OSB"):
        i+=1
        if (TS[i][0]=="ID" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST" or TS[i][0] == "ORB" or TS[i][0] == "not"):
            i, OElogic = OE(i)
            if (OElogic):
                if (TS[i][0] == "CSB"):
                    i+=1
                    i, IDcomplogic = IDcomp(i)
                    if (IDcomplogic):
                        return i, True
                    else:
                        return i, False
                else:
                    print("Error, expected a ] at ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    elif (TS[i][0]=="ORB"):
        i+=1
        i, argslogic = args(i)
        if (argslogic):
            if (TS[i][0]=="CRB"):
                i+=1
                i, idcomplogic = IDcomp(i)
                if (idcomplogic):
                    return i, True
    else:
        return i, True

def ID(i):
    if (TS[i][0] == "ID"):
        i+=1
        i, IDcomplogic = IDcomp(i)
        if (IDcomplogic):
            return i, True
        else:
            return i, False
    else:
        print("Error, invalid identifier at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def ind(i):
    if (TS[i][0] == "ID"):
        return i + 1, True
    
    if( TS[i][0] == "INTCONST"):
        return i + 1, True
    else:
        print("Error, expected an identifier or an integar constant at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

# def Dim(i):
#     if (TS[i][0] == "OSB"):
#         i+=1
#         if (TS[i][0]=="ID" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
#             i, indlogic = ind(i)
#             if (indlogic):
#                 i+=1
#                 if (TS[i][0] == "CSB"):
#                     return i, True
#                 else:
#                     print("Error, expected a ] at ", TS[i][1], " in line number ", TS[i][2])
#                     return i, False
#             else:
#                 return i, False
#         else:
#             print("Error, expected an identifier or constant at ", TS[i][1], " in line number ", TS[i][2])
#             return i, False
#     else:
#         print("Error, expected [ at ", TS[i][1], " in line number ", TS[i][2])
#         return i, False

def CAO(i):
    if (TS[i][0]=="CAO"):
        i+=1
        i, dcilogic = dci(i)
        if(dcilogic):
            return i, True
        else: 
            return i, False
    else:
        print("Error, expected a compound assignment operator at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def inc_dec(i):
    i, IDcomplogic = IDcomp(i)
    if (IDcomplogic): 
        if (TS[i][0]=="CAO"):
            i+=1
            i, CAOlogic = CAO(i)
            if (CAOlogic):
                return i, True
            else:
                return i, False
        else:
            print("Error, expected a compound assignment operator at ", TS[i][1], " in line number ", TS[i][2])
    else:
        return i, False

def dci(i):
    if (TS[i][0] == "ID"):
        return i + 1, True
    elif (TS[i][0] == "INTCONST"):
        return i + 1, True
    elif (TS[i][0] == "FLTCONST"):
        return i + 1, True
    else:
        print("Error, expected identifier or integer / float constant at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def P(i):
    if (TS[i][0] == "ID"):
        return i + 1, True
    elif (TS[i][0] == "INTCONST"):
        return i + 1, True
    elif (TS[i][0] == "FLTCONST"):
        return i + 1, True
    elif (TS[i][0] == "LOGICCONST"):
        return i + 1, True
    else:
        print("Error, expected expected identifier or integer / float / logic constant at ", TS[i][1], " in line number ", TS[i][2])
        return i, False
            
def Pcomp(i):
    if (TS[i][0]=="INTCONST"):
        return i + 1, True
    elif (TS[i][0]=="FLTCONST"):
        return i + 1, True
    elif (TS[i][0]=="LOGICCONST"):
        return i + 1, True
    else:
        print("Error, expected an integar, float or logic constant at ", TS[i][1], " in line number ", TS[i][2])

def ID2(i):

    i, IDclogic = IDcomp(i)
    if (IDclogic):
        return i, True
    
    if ((TS[i][0]=="dot" or TS[i][0]=="OSB" or TS[i][0]=="ORB") and TS[i+1][0]=="DT"):
        i, fncallLogic = fn_call(i)
        if (fncallLogic):
            return i, True
    if (TS[i][0]=="dot" or TS[i][0]=="OSB" or TS[i][0]=="CAO"):    
        i, incdecLogic = inc_dec(i)
        if (incdecLogic):
            return i, True
    
    if (TS[i][0]=="INTCONST" or TS[i][0]=="FLTCONST" or TS[i][0]=="LOGICCONST"):
        i, pcomplogic = Pcomp(i)
        if (pcomplogic):
            return i, True
    else:
        print("Error, expected a . or [ or ( or +=/-= or integer/float/logic constant at ", TS[i][1], " in line number ", TS[i][2])
        return i, False
    
def F(i):  
    if (TS[i][0]=="ID"):
        i+=1
        i, ID2logic = ID2(i)
        if(ID2logic):
            return i, True
        else:
            return i, False 
                
    if (TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
        i, constlogic = const(i)
        if (constlogic):
            return i, True
        else:
            return i, False                
    if (TS[i][0] == "ORB"):
        i+=1
        if (TS[i][0]=="ID" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST" or TS[i][0] == "ORB" or TS[i][0] == "not"):
            i, OElogic = OE(i)
            if (OElogic):
                if (TS[i][0] == "CRB"):
                    return i + 1, True
                else:
                    print("Error, expected a ] at ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
        
    if (TS[i][0] == "not"):
        i+=1
        if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, flogic = F(i)
            if (flogic):
                return i, True
            else:
                return i, False
        else:
            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    
    else:
        print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
        return i, False
    
    
def MDM(i):
    if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
        i, Flogic = F(i)
        if (Flogic):
            i, MDMcomp_logic = MDMcomp(i)
            if (MDMcomp_logic):
                return i, True
            else:
                return i, False
        else:
            i, False
    else:
        print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def PM(i):
    if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
        i, MDMlogic = MDM(i)
        if (MDMlogic):
            i, PMcomp_logic = PMcomp(i)
            if (PMcomp_logic):
                return i, True
            else:
                return i, False
        else:
            return i, False
    else:
        print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def RE(i):
    if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
        i, PMlogic = PM(i)
        if (PMlogic):
            i, REcomp_logic = REcomp(i)
            if (REcomp_logic):
                return i, True
            else:
                return i, False
        else:
            return i, False
    else:
        print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def AE(i):
    if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
        i, RElogic = RE(i)
        if (RElogic):
            i, AEcomp_logic = AEcomp(i)
            if (AEcomp_logic):
                return i, True
            else:
                return i, False
        else:
            return i, False
    else:
        print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def OE(i):
    if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
        i, AElogic = AE(i)
        if (AElogic):
            i, OEcomp_logic = OEcomp(i)
            if (OEcomp_logic):
                return i, True
            else:
                return i, False
        else:
            return i, False
    else:
        print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def cont(i):
    if (TS[i][0] == "comma"):
        i+=1
        if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, OElogic = OE(i)
            if (OElogic):
                if (TS[i][0] == "colon"):
                    i+=1
                    if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
                        i, OElogic = OE(i)
                        if (OElogic):
                            i, contlogic = cont(i)
                            if (contlogic):
                                return i, True
                            else:
                                return i, False
                        else:
                            return i, False
                    else:
                        print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
                        return i, False
                else:
                    print("Error, expected a : ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
            return i, False 
    else:
        return i  , True

def PMcomp(i):
    if (TS[i][0] == "PM"):
        i+=1
        if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, MDMlogic = MDM(i)
            if (MDMlogic):
                i, PMcomplogic = PMcomp(i)
                if (PMcomplogic):
                    return i, True
                else:
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
            return i, False 
    else:
        return i, True

def MDMcomp(i):
    if (TS[i][0] == "MDM"):
        i+=1
        if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, flogic = F(i)
            if (flogic):
                i, MDMcomplogic = MDMcomp(i)
                if (MDMcomplogic):
                    return i, True
                else:
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
            return i, False 
    else:
        return i, True

def REcomp(i):
    if (TS[i][0] == "RO"):
        i+=1
        if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, PMlogic = PM(i)
            if (PMlogic):
                i, REcomplogic = REcomp(i)
                if (REcomplogic):
                    return i, True
                else:
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        return i, True            

def AEcomp(i):
    if (TS[i][0] == "and"):
        i+=1
        if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, RElogic = RE(i)
            if (RElogic):
                i, AEcomplogic = AEcomp(i)
                if (AEcomplogic):
                    return i, True
                else:
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        return i, True

def OEcomp(i):
    if (TS[i][0] == "or"):
        i+=1
        if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, AElogic = AE(i)
            if (AElogic):
                i, OEcomplogic = OEcomp(i)
                if (OEcomplogic):
                    return i, True
                else:
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        return i, True


def map_decl(i, N):
    if (TS[i][0] == "map"):
        T = TS[i][0]
        insertST(N, T, stack[-1], i)
        i+=1
        if (TS[i][0] == "OCB"):
            i+=1
            if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
                i, OElogic = OE(i)
                if (OElogic):
                    if (TS[i][0] == "colon"):
                        i+=1
                        if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
                            i, OElogic = OE(i)
                            if (OElogic):
                                i, contlogic = cont(i)
                                if (contlogic):
                                    if (TS[i][0] == "CCB"):
                                        i+=1
                                        if (TS[i][0] == ";"):
                                            return i + 1, True
                                        else:
                                            print("Error, expected a ; at ", TS[i][1], " in line number ", TS[i][2])
                                            return i, False
                                    else:
                                        print("Error, expected a } at ", TS[i][1], " in line number ", TS[i][2])
                                        return i, False
                                else:
                                    return i, False
                            else:
                                return i, False
                        else:
                            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
                            return i, False
                    else:
                        print("Error, expected a : at ", TS[i][1], " in line number ", TS[i][2])
                        return i, False
                else:
                    return i, False
            else:
                print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
                return i, False
        else:
            print("Error, expected a { at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        print("Error, expected \"dict_of\" at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def contComp(i):
    if (TS[i][0]=="comma"):
        i+=1
        if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, OElogic = OE(i)
            if (OElogic):
                i , contComplogic = contComp(i)
                if (contComplogic):
                    return i, True
                else:
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
            return i, False  
    else:
        return i, True

def twoD(i):
    if (TS[i][0]=="OSB"):
        i+=1
        if (TS[i][0] == "ID" or TS[i][0]=="INTCONST"):
            i, indlogic = ind(i)
            if (indlogic):
                if(TS[i][0]=="CSB"):
                    return i + 1, True
                else:
                    print ("Error, expected a ] ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected an identifier or INTCONSTANT at", TS[i][1], "in line number", TS[i][2])
    else:
        return i, True
# def listComp(i):
#     if (TS[i][0] == "list"):
#         i+=1
#         if (TS[i][0] == "OSB"):
#             i+=1
#             if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST" or TS[i][0]=="list"):
#                 i, Llogic = L(i)
#                 if (Llogic):
#                     i, contClogic = contComp(i)
#                     if (contClogic):
#                         if (TS[i][0] == "CSB"):
#                             return i + 1, True
#                         else:
#                             print("Error, expected } at ", TS[i][1], " in line number ", TS[i][2])
#                     else:
#                         return i, False
#                 else:
#                     return i, False
#             else:
#                 print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
#                 return i, False
#         else:
#             print("Error, expected [ at ", TS[i][1], " in line number ", TS[i][2])
#     else:
#         print("Error, expected \"list_of\" at ", TS[i][1], " in line number ", TS[i][2])
#         return i, False

def Lcomp(i):
    if (TS[i][0]=="comma"):
        i+=1
        i , Llogic = L(i)
        if (Llogic):
            return i, True
        else:
            return i, False
    else:
        return i , True

def L(i):
    if (TS[i][0]=="OSB"):
        i+=1
        if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, OElogic = OE(i)
            if (OElogic):
                i, contCompLogic = contComp(i)
                if (contCompLogic):
                    if (TS[i][0]=="CSB"):
                        i+=1
                        i , Lcomplogic = Lcomp(i)
                        if (Lcomplogic):
                            return i , True
                        else:
                            return i, False
                    else:
                        print("Error, expected a ] at ", TS[i][1], " in line number ", TS[i][2])
                        return i, False
                else:
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected a \"not\" or \"ID\" or \"(\" or \"constant\" at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
        
    elif(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
        i , OElogic = OE(i)
        if(OElogic):
            i, contCompLogic = contComp(i)
            if (contCompLogic):
                i, Lcomplog = Lcomp(i)
                if (Lcomplog):
                    return i , True
                else:
                    return i, False
            else:
                return i, False
        else:
            return i, False     
                  
    else:
        return i , True

def list_decl(i):
    if (TS[i][0] == "OSB"):
        i+=1
        if (TS[i][0] == "ID" or TS[i][0]=="INTCONST"):
            i, indlogic = ind(i)
            if (indlogic):
                if (TS[i][0] == "CSB"):
                    i+=1
                    i, twoDlogic = twoD(i)
                    if (twoDlogic):
                        if (TS[i][0] == "SAO"):
                            i+=1
                            if (TS[i][0] == "OSB"):
                                i+=1
                                i, Llogic = L(i)
                                if (Llogic):
                                    if (TS[i][0]=="CSB"):
                                        i+=1
                                        if (TS[i][0]==";"):
                                            return i+1, True
                                        else:
                                            print("Error, expected a ; at ", TS[i][1], " in line number ", TS[i][2])
                                            return i, False
                                    else:
                                        print("Error, expected a ) at ", TS[i][1], " in line number ", TS[i][2])
                                        return i, False
                                else:
                                    return i, False
                            else:
                                print("Error, expected a ( at ", TS[i][1], " in line number ", TS[i][2])
                                return i, False
                        else:
                            print("Error, expected = at ", TS[i][1], " in line number ", TS[i][2])
                            return i, False
                    else:
                        return i, False
                else:
                    print("Error, expected ] at ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected an identifier or integer constant at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        print("Error, expected [ at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def cond(i):
    if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
        i, OElogic = OE(i)
        if (OElogic):
            return i, True
        else:
            return i, False
    else:
        return i, True

def if_func(i):
    if (TS[i][0] == "conditional"):
        i+=1
        if (TS[i][0] == "ORB"):
            i+=1
            if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
                i, OElogic = OE(i)
                if (OElogic):
                    if (TS[i][0] == "CRB"):
                        i+=1
                        if (TS[i][0] == "OCB"):
                            i+=1
                            i, bodylogic = Body(i)
                            if (bodylogic):
                                if (TS[i][0] == "CCB"):
                                    return i + 1, True
                                else:
                                    print("Error, expected } at ", TS[i][1], "in line number ", TS[i][2])
                                    return i, False
                            else:
                                return i, False
                        else:
                            print("Error, expected { at ", TS[i][1], "in line number ", TS[i][2])
                            return i, False
                    else:
                        print("Error, expected ) at ", TS[i][1], "in line number ", TS[i][2])
                        return i, False
                else:
                    return i, False
            else:
                print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
                return i, False
        else:
            print("Error, expected ( at ", TS[i][1], "in line number ", TS[i][2])
            return i, False
    else:
        print("Error, expected \"given\" at ", TS[i][1], "in line number ", TS[i][2])
        return i, False

# def if_else(i):
#     i, iflogic = if_func(i)
#     if (iflogic):
#         i+=1
#         if (TS[i][0] == "else"):
#             i+=1
#             if (TS[i][0] == "ORB"):
#                 i+=1
#                 i, condLogic = cond(i)
#                 if(condLogic):
#                     i+=1
#                     if (TS[i][0] == "CRB"):
#                         i+=1
#                         if (TS[i][0] == "OCB"):
#                             i+=1
#                             i, bodylogic = Body(i)
#                             if (bodylogic):
#                                 i+=1
#                                 if (TS[i][0] == "CCB"):
#                                     i+=1
#     return i, False

# def else_if(i):
#     i, iflogic = if_func(i)
#     if (iflogic):
#         i+=1
#         i, elselogic = else_st(i)
#         if (elselogic):
#             return i, True
#     return i, False

def else_st(i):
    if (TS[i][0] == "else"):
        i+=1
        if (TS[i][0] == "ORB"):
            i+=1
            i, condLogic = cond(i)
            if(condLogic):
                if (TS[i][0] == "CRB"):
                    i+=1
                    if (TS[i][0] == "OCB"):
                        i+=1
                        i, bodylogic = Body(i)
                        if (bodylogic):
                            if (TS[i][0] == "CCB"):
                                i+=1
                                i, elselogic = else_st(i)
                                if (elselogic):
                                    return i, True
                                else:
                                    return  i, False
                            else:
                                print("Error, expected } at ", TS[i][1], "in line number ", TS[i][2])
                                return i, False
                        else:
                            return i, False
                    else:
                        print("Error, expected { at ", TS[i][1], " in line number ", TS[i][2])
                        return i, False
                else:
                    print("Error, expected ) at ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected ( at ", TS[i][1], "in line number ", TS[i][2])
            return i, False

    elif(TS[i][0]=="elif"):
        i+=1
        if (TS[i][0] == "ORB"):
            i+=1
            i, condLogic = cond(i)
            if(condLogic):
                if (TS[i][0] == "CRB"):
                    i+=1
                    if (TS[i][0] == "OCB"):
                        i+=1
                        i, bodylogic = Body(i)
                        if (bodylogic):
                            if (TS[i][0] == "CCB"):
                                i+=1
                                i, elselogic = else_st(i)
                                if (elselogic):
                                    return i, True
                                else:
                                    return i, False
                            else:
                                print("Error, expected } at ", TS[i][1], "in line number ", TS[i][2])
                                return i, False
                        else:
                            return i, False
                    else:
                        print("Error, expected { at ", TS[i][1], " in line number ", TS[i][2])
                        return i, False
                else:
                    print("Error, expected ) at ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected ( at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        return i, True

def NT(i):
    if (TS[i][0]=="ID"):
        i, IDlogic = ID(i)
        if (IDlogic):
            return i, True
        else:
            return i, False
    elif (TS[i][0] == "range"):
        i+=1
        if (TS[i][0] == "INTCONST"):
            return i + 1, True
        else:
            return i, False
    else:
        print("Error, expected an identifier or integer constant at ", TS[i][1], " in line number ",TS[i][2])
        return i, False

def for_func(i):
    if (TS[i][0] == "for"):
        i+=1
        if (TS[i][0] == "ID"):
            i, idlogic = ID(i)
            if(idlogic):
                if (TS[i][1] == "in"):
                    i+=1
                    if(TS[i][0]=="ID" or TS[i][0]=="range"):
                        i, NTlogic = NT(i)
                        if (NTlogic):
                            if (TS[i][0] == "OCB"):
                                i+=1
                                i, bodylogic = Body(i)
                                if (bodylogic):
                                    if (TS[i][0] == "CCB"):
                                        return i + 1, True
                                    else:
                                        print("Error, expected a } at ", TS[i][1], " in line number ",TS[i][2])
                                        return i, False
                                else:
                                    return i, False
                            else:
                                print("Error, expected a { at ", TS[i][1], " in line number ",TS[i][2])
                                return i, False
                        else:
                            return i, False
                    else:
                        print("Error, expected an identifier or \"range\" at ", TS[i][1], " in line number ",TS[i][2])
                        return i, False
                else:
                    print("Error, expected \"in\" at ", TS[i][1], " in line number ",TS[i][2])
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected an identifier at ", TS[i][1], " in line number ",TS[i][2])
            return i, False
    else:
        print("Error, expected \"for_each\" at ", TS[i][1], " in line number ",TS[i][2])
        return i, False

def A(i):
    if(TS[i][0] == "SAO"):
        return i + 1, True
    elif (TS[i][0] == "CAO"):
        return i + 1, True
    else:
        print("Error, expected an = or += or -= at ", TS[i][1], " in line number ",TS[i][2])
        return i, False

def assign2(i):
    if (TS[i][0]=="SAO" or TS[i][0]=="CAO"):
        i, Alogic = A(i)
        if (Alogic):
            if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
                i, OElogic = OE(i)
                if (OElogic):
                    if (TS[i][0] == ";"):
                        return i + 1, True
                    else:
                        print("Error, expected ; at ", TS[i][1]," in line number", TS[i][2])
                        return i, False
                else:
                    return i, False
            else:
                print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
                return i, False
        else:
            return i, False
    else:
        #print("Error, expected a = or += or -= at ", TS[i][1]," in line number", TS[i][2])
        return i, True

def assign(i):
    i, IDcomplogic = IDcomp(i)
    if(IDcomplogic):
        i, assign2logic = assign2(i)
        if (assign2logic):
            return i, True
        else:
            return i, False
    else:
        return i, False

def obj_dec(i):
    if (TS[i][0] == "ORB"):
        i += 1  
        i, argsLogic = args(i)
        if (argsLogic):
            if (TS[i][0] == "CRB"):
                i+=1
                if (TS[i][0] == ";"):
                    return i + 1, True
                else:
                    print("Error, expected a ; at ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                print("Error, expected a ) at ", TS[i][1], " in line number ", TS[i][2])
                return i, False
        else:
            return i, False
    else:
        print("Error, expected a ( at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def exp(i):
    if(TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"): 
        i, constLogic = const(i)
        if (constLogic):
            return i, True
        else:
            return i, False
    if (TS[i][0]=="ID"):
        i , IDlogic = ID(i)
        if (IDlogic):
            return i, True
        else:
            return i, False
    else:
        print("Error, expected an identifier or constant at ", TS[i][1], " in line number ", TS[i][2])
        return False

def ret(i):
    if (TS[i][0] == "return"):
        i+=1
        if(TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST" or TS[i][0] == "ID" ): 
            i, expLogic = exp(i)
            if (expLogic):
                if (TS[i][0] == ";"):
                    return i + 1, True
                else:
                    print("Error, expected a ; at ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected an identifier or constant at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        print("Error, expected \"bring_back\" at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def try_catch(i):
    if (TS[i][0] == "try"):
        i+=1
        if (TS[i][0] == "OCB"):
            i+=1
            i, bodyLogic = Body(i)
            if (bodyLogic):
                if (TS[i][0] == "CCB"):
                    i+=1
                    if (TS[i][0] == "except"):
                        i+=1
                        if (TS[i][0] == "ID"):
                            i+=1
                            if (TS[i][0] == "as"):
                                i+=1
                                if (TS[i][0] == "ID"):
                                    i+=1
                                    if (TS[i][0] == "OCB"):
                                        i+=1
                                        i, bodyLogic = Body(i)
                                        if (bodyLogic):
                                            if (TS[i][0] == "CCB"):
                                                return i + 1, True
                                            else:
                                                print("Error, expected a } at ", TS[i][1], " in line number ", TS[i][2])
                                                return i, False
                                        else:
                                            return i, False
                                    else:
                                        print("Error, expected a { at ", TS[i][1], " in line number ", TS[i][2])
                                        return i, False
                                else:
                                    print("Error, expected an identifier at ", TS[i][1], " in line number ", TS[i][2])
                                    return i, False
                            else:
                                print("Error, expected \"as\" at ", TS[i][1], " in line number ", TS[i][2])
                                return i, False 
                        else:
                            print("Error, expected an identifier at ", TS[i][1], " in line number ", TS[i][2])
                            return i, False
                    else:
                         print("Error, expected \"except\" at ", TS[i][1], " in line number ", TS[i][2])
                         return i, False
                else:
                    print("Error, expected a } at ", TS[i][1], " in line number ", TS[i][2])  
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected a { at ", TS[i][1], " in line number ", TS[i][2])   
            return i, False                           
    else:
        print("Error, expected \"try\" at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def while_st(i):
    if (TS[i][0] == "conditional"):
        i+=1
        if (TS[i][0] == "ORB"):
            i+=1
            if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
                i, OElogic = OE(i)
                if (OElogic):
                    if (TS[i][0] == "CRB"):
                        i+=1
                        if (TS[i][0] == "OCB"):
                            i+=1
                            i, bodylogic = Body(i)
                            if (bodylogic):
                                if (TS[i][0] == "CCB"):
                                    return i + 1, True
                                else:
                                    print("Error, expected } at ", TS[i][1], " in line number ", TS[i][2])
                                    return i, False
                            else:
                                return i, False
                        else:
                            print("Error, expected { at ", TS[i][1], " in line number ", TS[i][2])
                            return i, False
                    else:
                        print("Error, expected ) at ", TS[i][1], " in line number ", TS[i][2])
                        return i, False
                else:
                    return i, False
            else:
                print("Error, expected \"not\" or ( or valid identifier or constant at ", TS[i][1], " in line number ", TS[i][2])
                return i, False
        else:
            print("Error, expected ( at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        print("Error, expected \"while_so\" at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def bring_st(i):
    if (TS[i][0] == "import"):
        i+=1
        if (TS[i][0] == "ID"):
            i+=1
            if (TS[i][0] == "as"):
                i+=1
                if (TS[i][0] == "ID"):
                    i+=1
                    if (TS[i][0] == ";"):
                        return i + 1, True
                    else:
                        print("Error, expected a ; at ", TS[i][1], " in line number ", TS[i][2])
                        return i, False
                else:
                    print("Error, expected an identifier at ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                print("Error, expected \"as\" at ", TS[i][1], " in line number ", TS[i][2])
                return i, False
        else:
            print("Error, expected an identifier at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        print("Error, expected \"bring\" at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def ip(i):
    if (TS[i][0] == "TEXTCONST"):
        return i + 1, True
    else:
        return i, True

def takeComp(i):
    if (TS[i][0] == "input"):
        i+=1
        if (TS[i][0] == "ORB"):
            i+=1
            if (TS[i][0] == "DT"):
                i+=1
                if (TS[i][0] == "ORB"):
                    i+=1
                    if (TS[i][0] == "TEXTCONST"):
                        i+=1
                        if (TS[i][0] == "CRB"):
                            i+=1
                            if (TS[i][0] == "CRB"):
                                i+=1
                                if (TS[i][0] == ";"):
                                    return i + 1, True
                                else:
                                    print("Error, expected a ; at ", TS[i][1], " in line number ", TS[i][2])
                                    return i, False
                            else:
                                print("Error, expected ) at ", TS[i][1], " in line number ", TS[i][2])
                                return i, False
                        else:
                            print("Error, expected ) at ", TS[i][1], " in line number ", TS[i][2])
                            return i, False
                    else:
                        print("Error, expected text constant at ", TS[i][1], " in line number ", TS[i][2])
                        return i, False
                else:
                    print ("Error, expected ( at ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                print("Error, expected DT at ", TS[i][1], " in line number ", TS[i][2])
                return i, False
        else:
            print("Error, expected ( at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        print("Error, expected \"take\" at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def take(i):
    i, IDcomplogic = IDcomp(i)
    if (IDcomplogic):
        if (TS[i][0] == "SAO"):
            i+=1
            if (TS[i][0] == "input"):
                i+=1
                if (TS[i][0] == "ORB"):
                    i+=1
                    if (TS[i][0] == "DT"):
                        i+=1
                        if (TS[i][0] == "ORB"):
                            i+=1
                            i, iplogic = ip(i)
                            if (iplogic):
                                if (TS[i][0] == "CRB"):
                                    i+=1
                                    if (TS[i][0] == "CRB"):
                                        i+=1
                                        if (TS[i][0] == ";"):
                                            return i + 1, True
                                        else:
                                            print("Error, expected a ; at ", TS[i][1], " in line number ", TS[i][2])
                                            return i, False
                                    else:
                                        print("Error, expected a ) at ", TS[i][1], " in line number ", TS[i][2])
                                        return i, False
                                else:
                                    print("Error, expected a ) at ", TS[i][1], " in line number ", TS[i][2])
                                    return i, False
                            else:
                                return i, False
                        else:
                            print("Error, expected a ( at ", TS[i][1], " in line number ", TS[i][2])
                            return i, False
                    else:
                        print("Error, expected a valid datatype at ", TS[i][1], " in line number ", TS[i][2])
                        return i, False
                else:
                    print("Error, expected a ( at ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                print("Error, expected \"take\" at ", TS[i][1], " in line number ", TS[i][2])
                return i, False
        else:
            print("Error, expected = at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        return i, False

def arg3(i):
    if (TS[i][0]=="ID"):
        i, IDlogic = ID(i)
        if (IDlogic):
            i, arg2logic = arg2(i)
            if (arg2logic):
                return i, True
            else:
                return i, False
        else:
            return i, False
    elif(TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):    
        i, constlogic = const(i)
        if (constlogic):
            i, arg2logic = arg2(i)
            if (arg2logic):
                return i, True
            else:
                return i, True
        else:
            return i, False
    else:
        print("Error, expected an identifer or constant at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def arg2(i):
    if (TS[i][0] == "comma"):
        i+=1
        if (TS[i][0]=="ID" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, arg3logic = arg3(i)
            if (arg3logic):
                return i, True
            else:
                return i, False
        else:
            print("Error, expected an identifer or constant at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        return i, True


def arg(i):
    if (TS[i][0] == "ID"):
        i, IDlogic = ID(i)
        if (IDlogic):
            i, arg2logic = arg2(i)
            if (arg2logic):
                return i, True
            else:
                return i, False
        else:
            return i, False
    elif(TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
        i, constlogic = const(i)
        if (constlogic):
            i, arg2logic = arg2(i)
            if (arg2logic):
                return i, True
            else:
                return i, False
        else:
            return i, False
    else:
        return i, True        

def display(i):
    if (TS[i][0] == "print"):
        i+=1
        if (TS[i][0] == "ORB"):
            i+=1
            i, arglogic = arg(i)
            if (arglogic):
                if (TS[i][0] == "CRB"):
                    i+=1
                    if (TS[i][0] == ";"):
                        return i+1, True
                    else:
                        print("Error, expected ; at ", TS[i][1], " in line number ", TS[i][2])
                        return i, False
                else:
                    print("Error, expected ) at ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected ( at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        print("Error, expected \"display\" at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def var_list2(i):
    if (TS[i][0] == "comma"):
        i+=1
        if (TS[i][0] == "ID"):
            i+=1
            i, var2logic = var_list2(i)
            if (var2logic):
                return i, True
            else:
                return i, False
        else:
            print("Error, expected an identifer at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        return i, True

def var_list(i):
    if (TS[i][0] == "ID"):
        i+=1
        i, var2logic = var_list2(i)
        if (var2logic):
            return i, True
        else:
            return i, False
    else:
        print("Error, expected an identifer at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def extract(i):
    if (TS[i][0] == "DT"):
        i+=1
        if (TS[i][0] == "ID"):
            i, varlogic = var_list(i)
            if (varlogic):
                if (TS[i][0] == "SAO"):
                    i+=1
                    if (TS[i][0] == "extract"):
                        i+=1
                        if (TS[i][0] == "ID"):
                            i+=1
                            if (TS[i][0] == ";"):
                                return i+1, True
                            else:
                                print("Error, expected a ; at ", TS[i][1], " in line number ", TS[i][2])
                                return i, False
                        else:
                            print("Error, expected an identifer at ", TS[i][1], " in line number ", TS[i][2])
                            return i, False
                    else:
                        print("Error, expected \"extract\" at ", TS[i][1], " in line number ", TS[i][2])
                        return i, False
                else:
                    print("Error, expected = at ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                return i, False
        else:
            print("Error, expected an identifer at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        print("Error, expected a valid datatype at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def args2(i):
    if (TS[i][0] == "comma"):
        i+=1
        if (TS[i][0] == "DT"):
            i+=1
            if (TS[i][0] == "ID"):
                i+=1
                i, args2logic = args2(i)
                if (args2logic):
                    return i, True
                else:
                    return i, False
            else:
                print("Error, expected an identifer at ", TS[i][1], " in line number ", TS[i][2])
                return i, False
        else:
            print("Error, expected a data type at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        return i, True

def argscomp(i):
    if (TS[i][0] == "DT"):
        i+=1
        if (TS[i][0] == "ID"):
            i+=1
            i, args2logic = args2(i)
            if (args2logic):
                return i, True
            else:
                return i, False
        else:
            print("Error, expected an identifer at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        return i, True

def func_def(i):
    if (TS[i][0] == "def"):
        i+=1
        if (TS[i][0] == "DT"):
            i+=1
            if (TS[i][0] == "ID"):
                i+=1
                if (TS[i][0] == "ORB"):
                    i+=1
                    i, argscomp_logic = argscomp(i)
                    if (argscomp_logic):
                        if (TS[i][0] == "CRB"):
                            i+=1
                            if (TS[i][0] == "OCB"):
                                i+=1
                                i, bodylogic = Body(i)
                                if (bodylogic):
                                    if (TS[i][0] == "CCB"):
                                        return i+1, True
                                    else:
                                        print("Error, expected a } at ", TS[i][1], " in line number ", TS[i][2])
                                        return i, False
                                else:
                                    return i, False
                            else:
                                print("Error, expected a { at ", TS[i][1], " in line number ", TS[i][2])
                                return i, False
                        else:
                            print("Error, expected a ) ", TS[i][1], " in line number ", TS[i][2])
                            return i, False
                    else:
                        return i, False
                else:
                    print("Error, expected a ( at ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                print("Error, expected an identifer at ", TS[i][1], " in line number ", TS[i][2])
                return i, False
        else:
            print("Error, expected a valid data type ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        print("Error, expected \"doing\" at ", TS[i][1], " in line number ", TS[i][2]) 
        return i, False

def F2(i):

    i, ID2logic = ID2(i)
    if (ID2logic):
        return i, True
    
    elif(TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
        i, constlogic = const(i)
        if (constlogic):
            return i, True
    elif (TS[i][0]=="ORB"):
        i+=1
        if (TS[i][0]=="ID" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST" or TS[i][0] == "ORB" or TS[i][0] == "not"):
            i, OElogic = OE(i)
            if(OElogic):
                if (TS[i][0]=="CRB"):
                    return i+1, True
    elif (TS[i][0]=="not"):
        i+=1
        if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, Flogic = F(i)
            if (Flogic):
                return i, True
            else:
                return i, False
        else:
            print("Error, expected ! or ( or valid identifier or constant at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        print("Error, expected ! or ( or valid constant at ", TS[i][1], " in line number ", TS[i][2])
        return i, False


def MDM2comp(i):
    if (TS[i][0] == "MDM"):
        i+=1
        i, F2logic = F2(i)
        if (F2logic):
            i, MDM2Clogic = MDM2comp(i)
            if (MDM2Clogic):
                return i, True
            else:
                return i, False
        else:
            return i, False
    else:
        return i, True

def MDM2(i):
    i, F2logic = F2(i)
    if (F2logic):
        i, MDM2Clogic = MDM2comp(i)
        if (MDM2Clogic):
            return i, True
        else: 
            return i, False
    else:
        return i, False

def PM2comp(i):
    if (TS[i][0] == "PM"):
        i+=1
        i, MDM2logic = MDM2(i)
        if (MDM2logic):
            i, PM2Clogic = PM2comp(i)
            if (PM2Clogic):
                return i, True
            else:
                return i, False
        else:
            return i, False
    else:
        return i, True

def PM2(i):
    i, MDM2logic = MDM2(i)
    if (MDM2logic):
        i, PM2Clogic = PM2comp(i)
        if (PM2Clogic):
            return i, True
        else:
            return i, False
    else:
        return i, False

def RE2comp(i):
    if (TS[i][0] == "RO"):
        i+=1
        i, PM2logic = PM2(i)
        if (PM2logic):
            i, RE2Clogic = RE2comp(i)
            if (RE2Clogic):
                return i, True
            else:
                return i, False
        else:
            return i, False
    return i, True

def RE2(i):
    i, PM2logic = PM2(i)
    if (PM2logic):
        i, RE2Clogic = RE2comp(i)
        if (RE2Clogic):
            return i, True
        else:
            return i, False
    else:
        return i, False

def AE2comp(i):
    if (TS[i][0] == "and"):
        i+=1
        i, RE2logic = RE2(i)
        if (RE2logic):
            i, AE2Clogic = AE2comp(i)
            if (AE2Clogic):
                return i, True
            else:
                return i, False
        else:
            return i, False
    return i, True

def AE2(i):
    i, RE2logic = RE2(i)
    if (RE2logic):
        i, AE2Clogic = AE2comp(i)
        if (AE2Clogic):
            return i, True
        else:
            return i, False
    else:
        return i, False

def OE2comp(i):
    if (TS[i][0] == "or"):
        i+=1
        i, AE2logic = AE2(i)
        if (AE2logic):
            i, OE2Clogic = OE2comp(i)
            if (OE2Clogic):
                return i, True
            else:
                return i, False
        else:
            return i, False
    return i, True

def OE2(i):
    i, AE2logic = AE2(i)
    if (AE2logic):
        i, OE2Clogic = OE2comp(i)
        if (OE2Clogic):
            return i, True
        else:
            return i, False
    else:
        return i, False

def decl3(i):
    if (TS[i][0] == "ORB"):
        i, objlogic = obj_dec(i)
        if (objlogic):
            return i, True
        else:
            return i, False
    i, OE2logic = OE2(i)
    if (OE2logic):
        if (TS[i][0] == ";"):
            return i+1, True
        else:
            print("Error, expected ; at ", TS[i][1], " in line number ", TS[i][2]) 
            return i, False
    else:
        return i, False

def decl2(i):
    if (TS[i][0] == "map"):
        i, maplogic = map_decl(i)
        if (maplogic):
            return i, True
        else:
            return i, False
    elif(TS[i][0]=="input"):
        i, takeClogic = takeComp(i)
        if(takeClogic):
            return i, True
        else:
            return i, False
    elif (TS[i][0]=="ID"):
        i+=1
        if (TS[i][0] == "ORB" or TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, decl3logic = decl3(i)
            if(decl3logic):
                return i, True
            else:
                return i, False
        else:
            print("Error, expected ( or ! or constant or an identifier at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        print("Error, expected \"dict_of\" or \"take\" or an identifier at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def ID3(i):

    # i, IDcomplogic = IDcomp(i)
    # if(IDcomplogic):
    #     return i, True
    
    if(TS[i][0]=="SAO"):
        i+=1
        if (TS[i][0] == "map" or TS[i][0]=="input" or TS[i][0]=="ID"):
            i, decl2logic = decl2(i)
            if (decl2logic):
                return i, True
            else:
                return i, False
        else:
            print("Error, expected \"dict_of\" or \"take\" or an identifier at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    if(TS[i][0]=="OSB" and (TS[i+3][0]=="SAO" or TS[i+6][0]=="SAO")):
        i, listlogic = list_decl(i)
        if (listlogic):
            return i, True
        else:
            return i, False
    if(TS[i][0]=="dot" or TS[i][0]=="OSB" or TS[i][0]=="SAO" or TS[i][0]=="CAO"):
        #print(TS[i][0])
        i, assignlogic = assign(i)
        if (assignlogic):
            return i, True
        else:
            return i, False
    if (TS[i][0]=="input"):
        i, takelogic = take(i)
        if (takelogic):
            return i, True
        else:
            return i, False
    if(TS[i][0]=="ID"):
        i, fclogic = fn_call(i)
        if(fclogic):
            return i, True
        else:
            return i, False
    else:
        print("Error, expected a = or [ or . or += / -= or \"take\" or an identifier at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def SST(i):

    if (TS[i][0]=="ID"):
        i+=1
        if (TS[i][0]=="SAO" or TS[i][0]=="dot" or TS[i][0]=="OSB" or TS[i][0]=="SAO" or TS[i][0]=="CAO" or TS[i][0]=="input" or TS[i][0]=="ID"):
            i, ID3logic = ID3(i)
            if (ID3logic):
                return i, True
            else:
                return i, False
        else:
            print("Error, expected a = or [ or . or += / -= or \"take\" or an identifier at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    
    elif(TS[i][0]=="DT"):
        i, Decl_logic = Decl(i)
        if (Decl_logic):
            return i, True
        else:
            return i, False
    
    elif(TS[i][1]=="while_so"):
        i, whilest_logic = while_st(i)
        if (whilest_logic):
            return i, True
        else:
            return i, False
    
    elif (TS[i][1]=="given"):
        i, if_logic = if_func(i)
        if (if_logic):
            i, elselogic = else_st(i)
            if (elselogic):
                return i, True
            else:
                return i, False
        else:
            return i, False
    
    elif(TS[i][0]=="for"):
        i, for_logic = for_func(i)
        if (for_logic):
            return i, True
        else:
            return i, False
    
    elif(TS[i][0]=="return"):
        i, ret_logic = ret(i)
        if (ret_logic):
            return i, True
        else:
            return i, False
    
    elif (TS[i][0]=="try"):
        i, tc_logic = try_catch(i)
        if (tc_logic):
            return i, True
        else:
            return i, False
    
    elif (TS[i][0]=="def"):
        i, fd_logic = func_def(i)
        if (fd_logic):
            return i, True
        else:
            return i, False
    
    elif (TS[i][0]=="extract"):
        i, ex_logic = extract(i)
        if (ex_logic):
            return i, True
        else:
            return i, False
    
    elif (TS[i][0]=="print"):
        i, dis_logic = display(i)
        if (dis_logic):
            return i, True
        else:
            return i, False
    
    elif (TS[i][0]=="import"):
        i, bring_logic = bring_st(i)
        if (bring_logic):
            return i, True
        else:
            return i, False
    
    else:
        print("Error, expected an identifier or valid data type or \"while_so\" or \"given\" or \"for_each\" or \"bring_back\" or \"try\" or \"doing\" or \"extract\" or \"display\" or \"bring\" at ", TS[i][1], " in line number ", TS[i][2])
        return i, False
    

def MST(i):
    if (TS[i][0]=="ID" or TS[i][0]=="DT" or TS[i][0]=="conditional" or TS[i][0]=="for" or TS[i][0]=="return" or TS[i][0]=="try" or TS[i][0]=="def" or TS[i][0]=="extract" or TS[i][0]=="print" or TS[i][0]=="import"):
        i, SSTlogic = SST(i)
        if (SSTlogic):
            i, MSTlogic = MST(i)
            if (MSTlogic):
                return i, True
            else:
                return i, False
        else:
            return i, False
    else:
        return i, True

def Body(i):
    if (TS[i][0]=="ID" or TS[i][0]=="DT" or TS[i][0]=="conditional" or TS[i][0]=="for" or TS[i][0]=="return" or TS[i][0]=="try" or TS[i][0]=="def" or TS[i][0]=="extract" or TS[i][0]=="print" or TS[i][0]=="import"):
        i, SSTlogic = SST(i)
        if (SSTlogic):
            return i, True
        else:
            return i, False
    
    i, MSTlogic = MST(i)
    if (MSTlogic):
        return i, True
    else:
        print("Error, expected an identifier or valid data type or \"while_so\" or \"given\" or \"for_each\" or \"bring_back\" or \"try\" or \"doing\" or \"extract\" or \"display\" or \"bring\" at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def acc_mod(i):
    if (TS[i][0] == "AM"):
        return i+1 , True
    else:
        return i, True

def constr(i):
        if (TS[i][0] == "init"):
            i+=1
            if (TS[i][0] == "ORB"):
                i+=1
                if (TS[i][0] == "self"):
                    i+=1
                    if (TS[i][0] == "comma"):
                        i+=1
                        i, argsClogic = argscomp(i)
                        if (argsClogic):
                            if (TS[i][0] == "CRB"):
                                i+=1
                                if (TS[i][0] == "OCB"):
                                    i+=1
                                    i, MSTlogic = MST(i)
                                    if (MSTlogic):
                                        if (TS[i][0] == "CCB"):
                                            return i+1, True
                                        else:
                                            print("Error, expected a } at ", TS[i][1], " in line number ", TS[i][2])
                                            return i, False
                                    else:
                                        return i, False
                                else:
                                    print("Error, expected a {  at ", TS[i][1], " in line number ", TS[i][2])
                                    return i, False
                            else:
                                print("Error, expected a )  at ", TS[i][1], " in line number ", TS[i][2])
                                return i, False
                        else:
                            return i, False
                    else:
                        print("Error, expected a ,  at ", TS[i][1], " in line number ", TS[i][2])
                        return i, False
                else:
                    print("Error, expected \"self\" at ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                print("Error, expected a (  at ", TS[i][1], " in line number ", TS[i][2])
                return i, False
        else:
            print("Error, expected \"init\" at ", TS[i][1], " in line number ", TS[i][2])
            return i, False

def AOM(i):
    i, accmodlogic = acc_mod(i)
    if (accmodlogic):
        if (TS[i][0] == "DT"):
            i, declLogic = Decl(i)
            if (declLogic):
                i, AOMlogic = AOM(i)
                if (AOMlogic):
                    return i, True
                else:
                    return i, False
            else:
                return i, False
        elif (TS[i][0] == "def"):
            i, funcLogic = func_def(i)
            if(funcLogic):
                i, AOMlogic = AOM(i)
                if(AOMlogic):
                    return i, True
                else:
                    return i, False
            else:
                return i, False
        elif (TS[i][0] == "init"):
            i, constrLogic = constr(i)
            if (constrLogic):
                i, AOMlogic = AOM(i)
                if(AOMlogic):
                    return i, True
                else:
                    return i, False
            else:
                return i, False
        else:
            return i, True
    else:
        return i, True

def seal(i):
    if (TS[i][0] == "sealed"):
        return i+1, True
    else:
        return i, True
        
def class_decl(i):
    i, seallogic = seal(i)
    if (seallogic):
        if (TS[i][0] == "class"):
            i+=1
            if (TS[i][0] == "ID"):
                i+=1
                if (TS[i][0] == "OCB"):
                    i+=1
                    i, AOMlogic = AOM(i)
                    if(AOMlogic):
                        if (TS[i][0] == "CCB"):
                            return i + 1, True
                        else:
                            print("Error, expected a }  at ", TS[i][1], " in line number ", TS[i][2])
                            return i, False
                    else:
                        return i, False
                else:
                    print("Error, expected a { at ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                print("Error, expected an identifier at ", TS[i][1], " in line number ", TS[i][2])
                return i, False
        else:
            print("Error, expected \"classy\" at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        return i, False

def inhert(i):
    if (TS[i][0] == "class"):
        i+=1
        if (TS[i][0] == "ID"):
            i+=1
            if (TS[i][0] == "ORB"):
                i+=1
                if (TS[i][0] == "inheritance"):
                    i+=1
                    if (TS[i][0] == "SAO"):
                        i+=1
                        if (TS[i][0] == "ID"):
                            i+=1
                            if (TS[i][0] == "CRB"):
                                i+=1
                                if (TS[i][0] == "OCB"):
                                    i+=1
                                    i, AOMlogic = AOM(i)
                                    if(AOMlogic):
                                        if (TS[i][0] == "CCB"):
                                            return i + 1, True
                                        else:
                                            print("Error, expected } at ", TS[i][1], " in line number ", TS[i][2])
                                            return i, False
                                    else:
                                        return i, False
                                else:
                                    print("Error, expected { at ", TS[i][1], " in line number ", TS[i][2])
                                    return i, False
                            else:
                                print("Error, expected ) at ", TS[i][1], " in line number ", TS[i][2])
                                return i, False
                        else:
                            print("Error, expected an identifier at ", TS[i][1], " in line number ", TS[i][2])
                            return i, False
                    else:
                        print("Error, expected = at ", TS[i][1], " in line number ", TS[i][2])
                        return i, False
                else:
                    print("Error, expected \"is_a\" at ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                print("Error, expected an ( at ", TS[i][1], " in line number ", TS[i][2])
                return i, False
        else:
            print("Error, expected an identifier at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        print("Error, expected \"classy\" at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def S(i):
    if (TS[i][0] == "$"):
        return i+1, True
    
    if (TS[i][0] == "class"):
        i+=1
        if (TS[i][0] == "ID"):
            i+=1
            if (TS[i][0] == "ORB"):
                i+=1
                i, inhertLogic = inhert(i-2)
                if (inhertLogic):
                    i, Slogic = S(i)
                    if (Slogic):
                        return i, True
                    else:
                        return i, False
                else:
                    return i, False
            else:
                i, classLogic = class_decl(i-2)
                if (classLogic):
                    i, Slogic = S(i)
                    if (Slogic):
                        return i, True
                    else:
                        return i, False
                else:
                    return i, False
        else:
            return i, False
    elif(TS[i][0] == "sealed"):
        i+=1
        i, classLogic = class_decl(i)
        if (classLogic):
            i, Slogic = S(i)
            if (Slogic):
                return i, True
            else:
                return i, False
        else:
            return i, False
        
    else:
        i, SSTlogic = SST(i)
        if (SSTlogic):
            i, Slogic = S(i)
            return i, Slogic
        else:
            return i, False

CreateScope()
i, logic = S(0)
DestroyScope()
if (logic):
    print ("Parsed Successfully !")