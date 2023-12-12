import lexical_analyzer as LA
f = open('D:\\Shaheer\\Compiler Construction\\Compiler-Construction\\code.txt', 'r')
code = f.read()
TS = LA.breakWords(code)

global ST
global MT 
global DT
global scope
global stack
global CCN

ST = []
MT = []
DT = []
stack = []
scope = 0
CCN = None

def insertST (N,T,S, i):
    if (len(T)>5):
        if(lookupFuncST(N, T)==False):
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
    
def insertDT (N, AM, CM, P, i):
    if(lookupDT(N)==False):
        DT.append([N, AM, CM, P])
        return True
    else:
        print("DT Redeclaration at line ", TS[i][2])
        return False
    
def insertMT (N, T, TM, AM, constructor, CN, i):
    if(len(T)>5):
        if(lookupFuncMT(N, T, CN)==False):
            MT.append([N, T, TM ,AM, constructor, CN])
            return True
        else:
            print("MT Function Redeclaration at line ", TS[i][2])
            return False
    else:
        if(lookupMT(N, CN)==False):
            MT.append([N, T, TM, AM, constructor, CN])
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
                            for j in range(remaining):
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

def BCompatibility (OP, OT):

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
        T = TS[i][1]
        return i + 1, "int", True
    if (TS[i][0] == "FLTCONST"):
        T = TS[i][1]
        return i + 1, "flt", True
    if (TS[i][0] == "CHRCONST"):
        T = TS[i][1]
        return i + 1, "char", True
    if (TS[i][0] == "TEXTCONST"):
        T = TS[i][1]
        return i + 1, "text", True
    if (TS[i][0] == "LOGICCONST"):
        T = TS[i][1]
        return i + 1, "logic", True
    print("Invalid Constant at ", TS[i][1], " in line number ", TS[i][2])
    return i, None, False 
    

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
        T1 = lookupST(N)
        if(T1==False):
            print("Undeclared variable ", N, " at line number ", TS[i][2])
        Compatibility("=", T, T1)
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
        i, T1, const_logic = const(i)
        Compatibility("=", T, T1)
        if (const_logic):
            if (TS[i][0] == ";" or TS[i][0] == "comma"):
                i, list2Logic = list2(i, T)
                if(list2Logic):
                    return i, True
                else:
                    return i, False
            else:
                print("Error, expected a , or ; at ", TS[i][1], " in line number ", TS[i][2])
                return i, False
        else:
            return i, False
    else:
        print("Error, expected an identifier or constant at ", TS[i][1], " in line number ", TS[i][2])
        return i, False


def list(i, T, AM=None, TM=None):
    if (TS[i][0] == "comma"):
        i+=1
        if (TS[i][0] == "ID"):
            N = TS[i][1]
            global CCN 
            CN = CCN 
            if (CN == None):
                insertST(N, T, stack[-1], i)
            if (CN!=None):
                insertMT(N, T, TM, AM, None, CN)
            i+=1
            if (TS[i][0] == "comma" or TS[i][0] == ";" or TS[i][0] == "SAO"):
                i, listLogic = list(i, T, AM)
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

def Decl(i, AM=None, TM=None):
    if (TS[i][0] == "DT"):
        T = TS[i][1]
        i+=1
        if (TS[i][0] == "ID"):
            N = TS[i][1]
            global CCN 
            CN = CCN 
            if (CN == None):
                insertST(N, T, stack[-1], i)
            if (CN!=None):
                insertMT(N, T, AM, None, None, CN)
            i+=1
            if (TS[i][0] == "comma" or TS[i][0] == ";" or TS[i][0] == "SAO"):
                i, listLogic = list(i, T, AM)
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


def new(i, PL):
    if (TS[i][0] == "comma"):
        i+=1
        if (TS[i][0]=="ID" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST" or TS[i][0] == "ORB" or TS[i][0] == "not"):
            i, T, OElogic = OE(i)
            PL += "," + T
            if (OElogic):
                i, newlogic = new(i, PL)
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
        i, T, OElogic = OE(i)
        PL = T
        if (OElogic):
            i, newlogic = new(i, PL)
            if (newlogic):
                return i, PL, True
            else:
                return i, None, False
        else:
            return i, None, False
    else:
        return i, None, True

def fn_call(i, N, N1):
    RDT = lookupDT(N1)
    i, T, IDcomplogic = IDcomp(i, N1)
    if (IDcomplogic):
        if (TS[i][0] == "ORB"):
            i+=1
            if (RDT!=None):
                insertST(N, N1, 0, i)
            elif (T!=None):
                S = lookupST(N)
                if (S!=None):
                    global CCN 
                    CN = CCN 
                    M = lookupMT(N, CN)
                    if (M!=None):
                        print ("Undeclared variable ", N)
            i, PL, argslogic = args(i)
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


def IDcomp(i, N):
    if (TS[i][0] == "dot"):
                i+=1
                T = lookupST(N)
                if(T==False):
                    print("Variable ", N, " is undeclared")
                if (T=="INTCONST" or T=="FLTCONST" or T=="LOGICCONST" or T=="TEXTCONST" or T=="CHRCONST"):
                    print("Identifier ", N, " has a primitive data type")
                if (TS[i][0] == "ID"):
                    N = TS[i][1]
                    T1 = lookupMT(N, T)
                    if (T1!=False):
                        if (T1[2]=="priv"):
                            print("Identifier ", N, " is private")
                    i+=1
                    i, T1, IDcomplogic = IDcomp(i, N)
                    if (IDcomplogic):
                        return i, T1, True
                    else:
                        return i, None, False
                else:
                    print("Error, invalid identifier at ", TS[i][1], " in line number ", TS[i][2])
                    return i, None, False               
    elif (TS[i][0] == "OSB"):
        i+=1
        T = lookupST(N)
        if(T==False):
            print("List ", N, " is undeclared")
        if (TS[i][0]=="ID" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST" or TS[i][0] == "ORB" or TS[i][0] == "not"):
            i, T1, OElogic = OE(i)
            if (OElogic):
                global dim
                dim = 1
                if (TS[i][0] == "CSB"):
                    i+=1
                    i, twoDlogic = twoD(i)
                    if (T=="list1d"):
                        if (T!=dim):
                            print("Declared list is one dimensional")
                    if (T=="list2d"):
                        if (T!=dim):
                            print("Declared list is two dimensional")
                    if (twoDlogic):
                        i, T, IDcomplogic = IDcomp(i, None)
                        if (IDcomplogic):
                            return i, T, True
                        else:
                            return i, T, False
                else:
                    print("Error, expected a ] at ", TS[i][1], " in line number ", TS[i][2])
                    return i, None, False
            else:
                return i, None, False
        else:
            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
            return i, None, False
    # elif (TS[i][0]=="ORB"):
    #     i+=1
    #     i, argslogic = args(i)
    #     if (argslogic):
    #         if (TS[i][0]=="CRB"):
    #             i+=1
    #             i, idcomplogic = IDcomp(i)
    #             if (idcomplogic):
    #                 return i, True
    else:
        global CCN 
        CN = CCN
        if (CN == None):  
            T = lookupST(N)
        if (CN != None):
            RMT = lookupMT(N, CN)
            T = RMT [1]
        return i, T, True

def ID(i):
    if (TS[i][0] == "ID"):
        N = TS[i][1]
        i+=1
        i, T, IDcomplogic = IDcomp(i, N)
        if (IDcomplogic):
            return i,T, True
        else:
            return i,None, False
    else:
        print("Error, invalid identifier at ", TS[i][1], " in line number ", TS[i][2])
        return i, None, False

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

def ID2(i, N):

    i, T, IDclogic = IDcomp(i, N)
    if (IDclogic):
        return i, T, True
    
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
    
def TyS(i):
    if (TS[i][0]=="this"):
        global CCN
        CR = CCN
        i+=1
        if (TS[i][0]=="dot"):
            return i+1, CR, True
        else:
            print("Error, expected a . at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    elif (TS[i][0]=="base"):
        CR = TS[i][1]
        i+=1
        if (TS[i][0]=="dot"):
            return i+1, CR, True
        else:
            print("Error, expected a . at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        CR = None
        return i, CR, True

def opts(i):
    if(TS[i][0]=="dot"):
        i+=1
        if (TS[i][0]=="ID"):
            i+=1
            i, optsLogic = opts(i)
            if (optsLogic):
                return i, True
            else:
                return i, False
        else:
            print("Error, expected an identifier at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    elif(TS[i][0]=="ORB"):
        i, argsLogic = args(i)
        if (argsLogic):
            if (TS[i][0]=="CRB"):
                i+=1
                i, op2logic = op2(i)
                if (op2logic):
                    return i, True
                else:
                    return i, False
            else:
                print("Error, expected a ) at ", TS[i][1], " in line number ", TS[i][2])
                return i, False
        else:
            return i, False
    else:
        return i, True
    
def op2(i):
    if(TS[i][0]=="dot"):
        i+=1
        if (TS[i][0]=="ID"):
            i+=1
            i, optsLogic = opts(i)
            if (optsLogic):
                return i, True
            else:
                return i, False
        else:
            print("Error, expected an identifier at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    
def F(i):
    if (TS[i][0]=="ID"):
        N = TS[i][1]
        i+=1
        i, T, ID2logic = ID2(i, N)
        if(ID2logic):
            return i, T, True
        else:
            return i, None, False 
                
    if (TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
        i, T, constlogic = const(i)
        if (constlogic):
            return i, T, True
        else:
            return i, None, False                
    if (TS[i][0] == "ORB"):
        i+=1
        if (TS[i][0]=="ID" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST" or TS[i][0] == "ORB" or TS[i][0] == "not"):
            i, T, OElogic = OE(i)
            if (OElogic):
                if (TS[i][0] == "CRB"):
                    return i + 1, T, True
                else:
                    print("Error, expected a ] at ", TS[i][1], " in line number ", TS[i][2])
                    return i, None, False
            else:
                return i, None, False
        else:
            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
            return i, None, False
        
    if (TS[i][0] == "not"):
        i+=1
        if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, T, flogic = F(i)
            if (flogic):
                return i, T, True
            else:
                return i, None, False
        else:
            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
            return i, None, False
    i, TySlogic = TyS(i)
    if(TySlogic):
        if(TS[i][0]=="ID"):
            i+=1
            i, optsLogic = opts(i)
            if(optsLogic):
                return i, True
            else:
                return i, False
        else:
            print("Error, expected an identifier at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
        return i, False
    
    
def MDM(i):
    if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
        i, T1, Flogic = F(i)
        if (Flogic):
            i, T, MDMcomp_logic = MDMcomp(i, T1)
            if (MDMcomp_logic):
                return i, T, True
            else:
                return i, None, False
        else:
            i, None, False
    else:
        print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
        return i, None, False

def PM(i):
    if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
        i, T1, MDMlogic = MDM(i)
        if (MDMlogic):
            i, T, PMcomp_logic = PMcomp(i, T1)
            if (PMcomp_logic):
                return i, T, True
            else:
                return i, None, False
        else:
            return i, None, False
    else:
        print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
        return i, None, False

def RE(i):
    if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
        i, T1, PMlogic = PM(i)
        if (PMlogic):
            i, T, REcomp_logic = REcomp(i, T1)
            if (REcomp_logic):
                return i, T, True
            else:
                return i, None, False
        else:
            return i, None, False
    else:
        print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
        return i, None, False

def AE(i):
    if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
        i, T1, RElogic = RE(i)
        if (RElogic):
            i, T, AEcomp_logic = AEcomp(i, T1)
            if (AEcomp_logic):
                return i, T, True
            else:
                return i, None, False
        else:
            return i, None, False
    else:
        print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
        return i, None, False

def OE(i):
    if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
        i, T1, AElogic = AE(i)
        if (AElogic):
            i, T, OEcomp_logic = OEcomp(i, T1)
            if (OEcomp_logic):
                return i, T, True
            else:
                return i, None, False
        else:
            return i, None, False
    else:
        print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
        return i, None, False

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

def PMcomp(i, T1):
    if (TS[i][0] == "PM"):
        OP = TS[i][1]
        i+=1
        if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, T, MDMlogic = MDM(i)
            if (MDMlogic):
                Compatibility (OP, T1, T)
                i, PMcomplogic = PMcomp(i, T1)
                if (PMcomplogic):
                    return i, T, True
                else:
                    return i, None, False
            else:
                return i, None, False
        else:
            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
            return i, None, False 
    else:
        T = T1
        return i, T, True

def MDMcomp(i, T1):
    if (TS[i][0] == "MDM"):
        OP = TS[i][1]
        i+=1
        if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, T, flogic = F(i)
            if (flogic):
                Compatibility (OP, T1, T)
                i, MDMcomplogic = MDMcomp(i, T1)
                if (MDMcomplogic):
                    return i, T, True
                else:
                    return i, None, False
            else:
                return i, None, False
        else:
            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
            return i, None, False 
    else:
        T = T1
        return i, T, True

def REcomp(i, T1):
    if (TS[i][0] == "RO"):
        OP = TS[i][1]
        i+=1
        if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, T, PMlogic = PM(i)
            if (PMlogic):
                Compatibility (OP, T1, T)
                i, REcomplogic = REcomp(i, T1)
                if (REcomplogic):
                    return i, T, True
                else:
                    return i, None, False
            else:
                return i, None, False
        else:
            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
            return i, None, False
    else:
        T = T1
        return i, T, True            

def AEcomp(i, T1):
    if (TS[i][0] == "and"):
        OP = TS[i][1]
        i+=1
        if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, T, RElogic = RE(i)
            if (RElogic):
                Compatibility (OP, T1, T)
                i, AEcomplogic = AEcomp(i, T1)
                if (AEcomplogic):
                    return i, T, True
                else:
                    return i, None, False
            else:
                return i, None, False
        else:
            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
            return i, None, False
    else:
        T = T1
        return i, T, True

def OEcomp(i, T1):
    if (TS[i][0] == "or"):
        OP = TS[i][1]
        i+=1
        if(TS[i][0] == "not" or TS[i][0] == "ID" or TS[i][0] == "ORB" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, T, AElogic = AE(i)
            if (AElogic):
                Compatibility(OP, T1, T)
                i, OEcomplogic = OEcomp(i, T1)
                if (OEcomplogic):
                    return i, T, True
                else:
                    return i, None, False
            else:
                return i, None, False
        else:
            print("Error, expected an identifier or a constant or ( or ! at ", TS[i][1], " in line number ", TS[i][2])
            return i, None, False
    else:
        T=T1
        return i, T, True


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
            i, T, OElogic = OE(i)
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
                global dim; dim += 1
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
        i , T, OElogic = OE(i)
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

def list_decl(i, N, TM=None):
    if (TS[i][0] == "OSB"):
        i+=1
        if (TS[i][0] == "ID" or TS[i][0]=="INTCONST"):
            i, indlogic = ind(i)
            if (indlogic):
                global dim;dim = 1
                if (TS[i][0] == "CSB"):
                    i+=1
                    i, twoDlogic = twoD(i)
                    if (twoDlogic):
                        if (dim==1):
                            T = "list1d"
                        elif (dim==2):
                            T = "list2d"
                        AM = None
                        global CCN 
                        CN = CCN 
                        S = insertST(N, T, stack[-1], i)
                        if (S == False):
                            M = insertMT(N, T, TM, AM, None, CN)
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

def assign(i, N):
    i, T, IDcomplogic = IDcomp(i, N)
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

def exp(i, T):
    if(TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"): 
        i, T1, constLogic = const(i)
        Compatibility("=", T, T1)
        if (constLogic):
            return i, True
        else:
            return i, False
    if (TS[i][0]=="ID"):
        i , T1, IDlogic = ID(i)
        Compatibility("=", T, T1)
        if (IDlogic):
            return i, True
        else:
            return i, False
    else:
        print("Error, expected an identifier or constant at ", TS[i][1], " in line number ", TS[i][2])
        return False

def ret(i, T):
    if (TS[i][0] == "return"):
        i+=1
        if(TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST" or TS[i][0] == "ID" ): 
            i, expLogic = exp(i, T)
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

def var_list2(i, T):
    if (TS[i][0] == "comma"):
        i+=1
        if (TS[i][0] == "ID"):
            N = TS[i][1]
            insertST(N, T, stack[-1], i)
            i+=1
            i, var2logic = var_list2(i, T)
            if (var2logic):
                return i, True
            else:
                return i, False
        else:
            print("Error, expected an identifer at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        return i, True

def var_list(i, T):
    if (TS[i][0] == "ID"):
        N = TS[i][1]
        insertST(N, T, stack[-1], i)
        i+=1
        i, var2logic = var_list2(i, T)
        if (var2logic):
            return i, True
        else:
            return i, False
    else:
        print("Error, expected an identifer at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def extract(i):
    if (TS[i][0] == "DT"):
        T = TS[i][1]
        i+=1
        if (TS[i][0] == "ID"):
            i, varlogic = var_list(i, T)
            if (varlogic):
                if (TS[i][0] == "SAO"):
                    i+=1
                    if (TS[i][0] == "extract"):
                        i+=1
                        if (TS[i][0] == "ID"):
                            N = TS[i][1]
                            if(lookupST(N)==False):
                                print("Variable", N, "undeclared at line ", TS[i][2])
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

def args2(i, RT, PL):
    if (TS[i][0] == "comma"):
        i+=1
        if (TS[i][0] == "DT"):
            T = TS[i][1]
            PL += "," + T
            i+=1
            if (TS[i][0] == "ID"):
                N = TS[i][1]
                AM = None
                global CCN 
                CN = CCN 
                if (CN == None):
                    S = insertST(N, T, stack[-1], i)
                if (CN != None):
                    M = insertMT(N, T,None, AM, None, CN, i)
                i+=1
                i, PL, args2logic = args2(i, RT, PL)
                if (args2logic):
                    return i, PL, True
                else:
                    return i, None, False
            else:
                print("Error, expected an identifer at ", TS[i][1], " in line number ", TS[i][2])
                return i, None, False
        else:
            print("Error, expected a data type at ", TS[i][1], " in line number ", TS[i][2])
            return i, None, False
    else:
        PL += "->" + RT 
        return i, PL, True

def argscomp(i, RT):
    PL = None
    if (TS[i][0] == "DT"):
        T = TS[i][1]
        PL = T
        i+=1
        if (TS[i][0] == "ID"):
            N = TS[i][1]
            AM = None
            global CCN 
            CN = CCN 
            if (CN==None):    
                S = insertST(N, T, stack[-1], i)
            if (CN != None):
                M = insertMT(N, T, None, AM, None, CN, i)
            i+=1
            i, PL, args2logic = args2(i, RT, PL)
            if (args2logic):
                return i, PL, True
            else:
                return i, None, False
        else:
            print("Error, expected an identifer at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    else:
        if(PL==None):
            return i, None, True
        else:
            PL += "->" + RT
            return i, PL, True

def func_def(i, AM=None, TM=None):
    if (TS[i][0] == "def"):
        i+=1
        if (TS[i][0] == "DT"):
            RT = TS[i][1]
            i+=1
            if (TS[i][0] == "ID"):
                N = TS[i][1]
                i+=1
                if (TS[i][0] == "ORB"):
                    i+=1
                    scope = stack[-1]
                    CreateScope()
                    i, PL, argscomp_logic = argscomp(i, RT)
                    global CCN 
                    CN = CCN
                    if (N == CN):
                        constructor = "Yes"
                    else:
                        constructor = None
                    if (CN==None):
                        S = insertST(N, PL, scope, i)
                    if (CN!=None):
                        RDT = lookupDT(CN)
                        P = RDT[3]
                        if (P!=None):
                            RMT = lookupFuncMT(N, PL, P)
                            if (RMT!=False):
                                if (RMT[2]=="virtual"):
                                    M = insertMT(N, PL, TM, AM, constructor, CN, i)
                                else:
                                    print("Cannot override non-virtual function")
                            else:
                                M = insertMT(N, PL, TM, AM, constructor, CN, i)
                        else:
                            M = insertMT(N, PL, TM, AM, constructor, CN, i)
                    if (argscomp_logic):
                        if (TS[i][0] == "CRB"):
                            i+=1
                            if (TS[i][0] == "OCB"):
                                i+=1
                                i, bodylogic = Body(i, RT)
                                if (bodylogic):
                                    if (TS[i][0] == "CCB"):
                                        DestroyScope()
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

def F2(i, N):

    i, ID2logic = ID2(i, N)
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
        #print("Error, expected ! or ( or valid constant at ", TS[i][1], " in line number ", TS[i][2])
        return i, True


def MDM2comp(i, T1):
    if (TS[i][0] == "MDM"):
        i+=1
        i, T1, F2logic = F2(i)
        if(F2logic):
            i, T, MDM2Clogic = MDM2comp(i, T1)
            if (MDM2Clogic):
                return i, T, True
            else:
                return i, None, False
        else:
            return i, None, False
    else:
        return i, T, True

def MDM2(i, N):
    i, T1, F2logic = F2(i, N)
    if (F2logic):
        i, T, MDM2Clogic = MDM2comp(i, T1)
        if (MDM2Clogic):
            return i, T, True
        else: 
            return i, None, False
    else:
        return i, None, False

def PM2comp(i, T1):
    if (TS[i][0] == "PM"):
        i+=1
        i, T1, MDM2logic = MDM2(i)
        if (MDM2logic):
            i, T, PM2Clogic = PM2comp(i, T1)
            if (PM2Clogic):
                return i, T, True
            else:
                return i, None, False
        else:
            return i, None, False
    else:
        return i, T, True

def PM2(i, N):
    i, T1, MDM2logic = MDM2(i, N)
    if (MDM2logic):
        i, T, PM2Clogic = PM2comp(i, T1)
        if (PM2Clogic):
            return i, T, True
        else:
            return i, None, False
    else:
        return i, None, False

def RE2comp(i, T1):
    if (TS[i][0] == "RO"):
        i+=1
        i, T, PM2logic = PM2(i)
        if (PM2logic):
            i, T, RE2Clogic = RE2comp(i, T1)
            if (RE2Clogic):
                return i, T1, True
            else:
                return i,None, False
        else:
            return i,None, False
    return i, T1, True

def RE2(i, N):
    i, T1, PM2logic = PM2(i, N)
    if (PM2logic):
        i, T, RE2Clogic = RE2comp(i, T1)
        if (RE2Clogic):
            return i, T, True
        else:
            return i,None, False
    else:
        return i, None, False

def AE2comp(i, T1):
    if (TS[i][0] == "and"):
        OP = TS[i][1]
        i+=1
        i, T, RE2logic = RE2(i)
        if (RE2logic):
            Compatibility(OP, T1, T)
            i, T, AE2Clogic = AE2comp(i, T1)
            if (AE2Clogic):
                return i, T, True
            else:
                return i, None, False
        else:
            return i, None, False
    return i, T, True

def AE2(i, N):
    i, T1, RE2logic = RE2(i, N)
    if (RE2logic):
        i, T, AE2Clogic = AE2comp(i, T1)
        if (AE2Clogic):
            return i, T, True
        else:
            return i, None, False
    else:
        return i, None, False

def OE2comp(i, T1):
    if (TS[i][0] == "or"):
        OP = TS[i][1]
        i+=1
        i, T, AE2logic = AE2(i)
        if (AE2logic):
            Compatibility (OP, T1, T)
            i, T, OE2Clogic = OE2comp(i, T1)
            if (OE2Clogic):
                return i, T, True
            else:
                return i, None, False
        else:
            return i, None, False
    return i, T, True

def OE2(i,N):
    i, T1, AE2logic = AE2(i, N)
    if (AE2logic):
        i, T, OE2Clogic = OE2comp(i, T1)
        if (OE2Clogic):
            return i, T, True
        else:
            return i, None, False
    else:
        return i, None, False

def decl3(i, N, N1):
    if (TS[i][0] == "ORB"):
        i, funcCalllogic = fn_call(i, N, N1)
        if (funcCalllogic):
            return i, True
        else:
            return i, False
    if(lookupST(N)==False):
        print("Variable ", N, " undeclared")
    if(lookupST(N1)==False):
        print("Variable ", N1, " undeclared")
    i, OE2logic = OE2(i, N)
    if (OE2logic):
        if (TS[i][0] == ";"):
            return i+1, True
        else:
            print("Error, expected ; at ", TS[i][1], " in line number ", TS[i][2]) 
            return i, False
    else:
        return i, False

def decl2(i, N):
    if (TS[i][0] == "map"):
        i, maplogic = map_decl(i, N)
        if (maplogic):
            return i, True
        else:
            return i, False
    elif(TS[i][0]=="input"):
        i, takeClogic = takeComp(i, N)
        if(takeClogic):
            return i, True
        else:
            return i, False
    elif (TS[i][0]=="ID"):
        N1 = TS[i][1]
        i+=1
        i, decl3logic = decl3(i, N, N1)
        if(decl3logic):
            return i, True
        else:
            return i, False
    else:
        print("Error, expected \"dict_of\" or \"take\" or an identifier at ", TS[i][1], " in line number ", TS[i][2])
        return i, False

def ID3(i, N):
    if(TS[i][0]=="SAO"):
        i+=1
        if (TS[i][0] == "map" or TS[i][0]=="input" or TS[i][0]=="ID"):
            i, decl2logic = decl2(i, N)
            if (decl2logic):
                return i, True
            else:
                return i, False
        else:
            print("Error, expected \"dict_of\" or \"take\" or an identifier at ", TS[i][1], " in line number ", TS[i][2])
            return i, False
    try:
        if(TS[i][0]=="OSB" and (TS[i+3][0]=="SAO" or TS[i+6][0]=="SAO")):
            i, listlogic = list_decl(i, N)
            if (listlogic):
                return i, True
            else:
                return i, False
    except:
        if(TS[i][0]=="dot" or TS[i][0]=="OSB" or TS[i][0]=="SAO" or TS[i][0]=="CAO"):
        #print(TS[i][0])
            i, assignlogic = assign(i, N)
            if (assignlogic):
                return i, True
            else:
                return i, False
        if (TS[i][0]=="input"):
            i, takelogic = take(i, N)
            if (takelogic):
                return i, True
            else:
                return i, False
        if(TS[i][0]=="ID"):
            i, fclogic = fn_call(i, N, N1 = None)
            if(fclogic):
                return i, True
            else:
                return i, False
        else:
            print("Error, expected a = or [ or . or += / -= or \"take\" or an identifier at ", TS[i][1], " in line number ", TS[i][2])
            return i, False

def SST(i, T=None):

    if (TS[i][0]=="ID"):
        N = TS[i][1]
        i+=1
        if (TS[i][0]=="SAO" or TS[i][0]=="dot" or TS[i][0]=="OSB" or TS[i][0]=="SAO" or TS[i][0]=="CAO" or TS[i][0]=="input" or TS[i][0]=="ID"):
            i, ID3logic = ID3(i, N)
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
        i, ret_logic = ret(i, T)
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

def Body(i, RT):
    if (TS[i][0]=="ID" or TS[i][0]=="DT" or TS[i][0]=="conditional" or TS[i][0]=="for" or TS[i][0]=="return" or TS[i][0]=="try" or TS[i][0]=="def" or TS[i][0]=="extract" or TS[i][0]=="print" or TS[i][0]=="import"):
        i, SSTlogic = SST(i, RT)
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
        AM = TS[i][1]
        return i+1 , AM, True
    else:
        AM = None
        return i, AM, True

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
    i, AM, accmodlogic = acc_mod(i)
    if (accmodlogic):
        if (TS[i][0] == "DT"):
            i, declLogic = Decl(i, AM)
            if (declLogic):
                i, AOMlogic = AOM(i)
                if (AOMlogic):
                    return i, True
                else:
                    return i, False
            else:
                return i, False
        elif (TS[i][0] == "def" or TS[i][0]=="virtual"):
            i, TM, virLogic = vir(i)
            if (virLogic):
                i, funcLogic = func_def(i, AM, TM)
                if(funcLogic):
                    i, AOMlogic = AOM(i)
                    if(AOMlogic):
                        return i, True
                    else:
                        return i, False
                else:
                    return i, False
            else:
                return i , False
        elif (TS[i][0] == "init"):
            i, constrLogic = constr(i, AM)
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

def vir(i):
    if(TS[i][0]=="virtual"):
        TM = TS[i][1]
        return i+1, TM, True
    else:
        return i, None, True

def seal(i):
    if (TS[i][0] == "sealed"):
        CM = TS[i][1]
        return i+1, CM, True
    else:
        CM = None
        return i, CM, True
        
def class_decl(i):
    global CCN 
    i, CM, seallogic = seal(i)
    if (seallogic):
        i, AM, accmodlogic = acc_mod(i)
        if (accmodlogic):
            if (TS[i][0] == "class"):
                i+=1
                if (TS[i][0] == "ID"):
                    N = TS[i][1]
                    CCN = N
                    i+=1
                    i, P, inhertLogic = inhert(i)
                    if (inhertLogic):
                        insertDT(N, AM, CM, P ,i)
                        if (TS[i][0] == "OCB"):
                            i+=1
                            i, AOMlogic = AOM(i)
                            if(AOMlogic):
                                if (TS[i][0] == "CCB"):
                                    CCN = None
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
                        return i, False
                else:
                    print("Error, expected an identifier at ", TS[i][1], " in line number ", TS[i][2])
                    return i, False
            else:
                print("Error, expected \"classy\" at ", TS[i][1], " in line number ", TS[i][2])
                return i, False
        else:
            return i, False
    else:
        return i, False

def inhert(i):
    if (TS[i][0] == "ORB"):
        i+=1
        if (TS[i][0] == "inheritance"):
            i+=1
            if (TS[i][0] == "SAO"):
                 i+=1
                 if (TS[i][0] == "ID"):
                    P = TS[i][1]
                    RDT = lookupDT(P)
                    if (RDT==False):
                        P = None
                        print ("Parent class undeclared")
                    if (RDT[2] == "sealed"):
                        print ("Cannot inherit from sealed class")
                        P = None
                    i+=1
                    if (TS[i][0] == "CRB"):
                        return i+1, P, True
                    else:
                        print("Error, expected ) at ", TS[i][1], " in line number ", TS[i][2])
                        return i, None, False
                 else:
                    print("Error, expected an identifier at ", TS[i][1], " in line number ", TS[i][2])
                    return i, None, False
            else:
                print("Error, expected = at ", TS[i][1], " in line number ", TS[i][2])
                return i, None, False
        else:
            print("Error, expected \"is_a\" at ", TS[i][1], " in line number ", TS[i][2])
            return i, None, False
    else:
        P = None
        return i, P, True

def S(i):
    if (TS[i][0] == "$"):
        return i+1, True

    if (TS[i][0] == "sealed" or TS[i][0] == "AM" or TS[i][0] == "class"):
        i, class_decllogic = class_decl(i)
        if (class_decllogic):
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
    print ("\nSyntax Parsed Successfully !")

print("\nScope Table : ", ST)
print("\nDefinition Table : ", DT)
print("\nMember Table : ", MT)