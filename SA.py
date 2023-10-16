import lexical_analyzer as LA
f = open('D:\\Shaheer\\Compiler Construction\\Compiler-Construction\\code.txt', 'r')
code = f.read()
TS = LA.breakWords(code)

def const(i):
    if (TS[i][0] == "INTCONST"):
        return i, True
    if (TS[i][0] == "FLTCONST"):
        return i, True
    if (TS[i][0] == "CHRCONST"):
        return i, True
    if (TS[i][0] == "TEXTCONST"):
        return i, True
    if (TS[i][0] == "LOGICCONST"):
        return i, True
    return i, False
    

def list2(i):
    if (TS[i][0] == ";"):
        return True
    if (TS[i][0] == ","):
        i+=1
        if (TS[i][0] == "ID"):
            i+=1
            if (list(i)):
                return True
    return False

def init(i):
    if (TS[i][0] == "ID"):
        i+=1
        if(list(i)):
            return True
    i, const_logic = const(i)
    if (const_logic):
        i+=1
        if(list2(i)):
            return True
    return False


def list(i):
    if (TS[i][0] == ","):
        i+=1
        if (TS[i][0] == "ID"):
            i+=1
            if(list(i)):
                return True
    elif (TS[i][0] == ";"):
        return True
    elif (TS[i][0] == "SAO"):
        i+=1
        if(init(i)):
            return True
    return False

def Decl(i):
    if (TS[i][0] == "DT"):
        i+=1
        if (TS[i][0] == "ID"):
            i+=1
            if(list(i)):
                return True
    return False


def new(i):
    if (TS[i][0] == "comma"):
        i+=1
        i, OElogic = OE(i)
        if (OElogic):
            i+=1
            i, newlogic = new(i)
            if (newlogic):
                return i, True
    return i, True

def args(i):
    i, OElogic = OE(i)
    if (OElogic):
        i+=1
        i, newlogic = new(i)
        if (newlogic):
            return i, True
    return i-1, True

def fn_call(i):
    i, IDlogic = ID(i)
    if (IDlogic):
        i+=1
        if (TS[i][0] == "ORB"):
            i+=1
            i, argslogic = args(i)
            if (argslogic):
                i+=1
                if (TS[i][0] == "CRB"):
                    i+=1
                    if (TS[i][0] == ";"):
                        return i, argslogic
    return i, False


def IDcomp(i):
    if (TS[i][0] == "dot"):
                i+=1
                if (TS[i][0] == "ID"):
                    i+=1
                    i, IDcomplogic = IDcomp(i)
                    if (IDcomplogic):
                        return i, True
    elif (TS[i][0] == "OSB"):
        i+=1
        i, OElogic = OE(i)
        if (OElogic):
            i+=1
            if (TS[i][0] == "CSB"):
                i+=1
                i, IDcomplogic = IDcomp(i)
                if (IDcomplogic):
                    return i, True
    return i, True

def ID(i):
    if (TS[i][0] == "ID"):
        i+=1
        i, IDcomplogic = IDcomp(i)
        if (IDcomplogic):
            return i, True
    return i, False

def ind(i):
    if (TS[i][0] == "ID"):
        return i, True
    
    i, constlogic = const(i)
    if (constlogic):
        return i, True
    
    return i, False

def Dim(i):
    if (TS[i][0] == "OSB"):
        i+=1
        i, indlogic = ind(i)
        if (indlogic):
            i+=1
            if (TS[i][0] == "CSB"):
                return i, True
    elif (TS[i][0] == None):
        return i, True
    return i, False

def inc_dec(i):
    i, IDlogic = ID(i)
    if (IDlogic): 
        i+=1
        if (TS[i][0] == "CAO"):
            i+=1
            i, dcilogic = dci(i)
            if (dcilogic):
                return i, True
    return i, False

def dci(i):
    if (TS[i][0] == "ID"):
        return i, True
    elif (TS[i][0] == "INTCONST"):
        return i, True
    elif (TS[i][0] == "FLTCONST"):
        return i, True
    return i, False

def P(i):
    if (TS[i][0] == "ID"):
        return i, True
    elif (TS[i][0] == "INTCONST"):
        return i, True
    elif (TS[i][0] == "FLTCONST"):
        return i, True
    elif (TS[i][0] == "LOGICCONST"):
        return i, True
    return i, False
            

def F(i):  
    i, IDlogic = ID(i)
    if (IDlogic): 
        return i, True
    
    i, constlogic = const(i)
    if (constlogic):
        return i, True
    
    i, fc_logic = fn_call(i)
    if (fc_logic):
        return i, True
    
    if (TS[i][0] == "ID"):
        i+=1
        if (TS[i][0] == "OSB"):
            i+=1
            i, indlogic = ind(i)
            if (indlogic):
                i+=1
                if (TS[i][0] == "CSB"):
                    i+=1
                    i, dimlogic = Dim(i)
                    if (dimlogic):
                        return i, True
                    
    if (TS[i][0] == "ORB"):
        i+=1
        i, OElogic = OE(i)
        if (OElogic):
            i+=1
            if (TS[i][0] == "CRB"):
                return i, True
    
    if (TS[i][0] == "not"):
        i+=1
        i, flogic = F(i)
        if (flogic):
            return i, True
    
    i, icdclogic = inc_dec(i)
    if (icdclogic):
        return i, True
    
    i, plogic = P(i)
    if (plogic):
        i+=1
        if (TS[i][1] == "**"):
            i+=1
            i, plogic = P(i)
            if (plogic):
                return i, True
    return i, False
    
    
def MDM(i):
    i, Flogic = F(i)
    if (Flogic):
        i+=1
        i, MDMcomp_logic = MDMcomp(i)
        if (MDMcomp_logic):
            return i, True
    return i, False

def PM(i):
    i, MDMlogic = MDM(i)
    if (MDMlogic):
        i+=1
        i, PMcomp_logic = PMcomp(i)
        if (PMcomp_logic):
            return i, True
    return i, False

def RE(i):
    i, PMlogic = PM(i)
    if (PMlogic):
        i+=1
    i, REcomp_logic = REcomp(i)
    if (REcomp_logic):
        return i, True
    return i, False

def AE(i):
    i, RElogic = RE(i)
    if (RElogic):
        i+=1
        i, AEcomp_logic = AEcomp(i)
        if (AEcomp_logic):
            return i, True
    return i, False


def OE(i):
    i, AElogic = AE(i)
    if (AElogic):
        i+=1
        i, OEcomp_logic = OEcomp(i)
        if (OEcomp_logic):
            return i, True
    return i, False

def cont(i):
    if (TS[i][0] == "comma"):
        i+=1
        i, OElogic = OE(i)
        if (OElogic):
            i+=1
            if (TS[i][0] == "colon"):
                i+=1
                i, OElogic = OE(i)
                if (OElogic):
                    i+=1
                    i, contlogic = cont(i)
                    if (contlogic):
                        return i, True  
    return i-1  , True

def PMcomp(i):
    if (TS[i][0] == "PM"):
        i+=1
        i, MDMlogic = MDM(i)
        if (MDMlogic):
            i+=1
            i, PMcomplogic = PMcomp(i)
            if (PMcomplogic):
                return i, True
    return i-1, True

def MDMcomp(i):
    if (TS[i][0] == "MDM"):
        i+=1
        i, flogic = F(i)
        if (flogic):
            i+=1
            i, MDMcomplogic = MDMcomp(i)
            if (MDMcomplogic):
                return i, True
    return i-1, True

def REcomp(i):
    if (TS[i][0] == "RO"):
        i+=1
        i, PMlogic = PM(i)
        if (PMlogic):
            i+=1
            i, REcomplogic = REcomp(i)
            if (REcomplogic):
                return i, True
    return i-1, True            

def AEcomp(i):
    if (TS[i][0] == "and"):
        i+=1
        i, RElogic = RE(i)
        if (RElogic):
            i+=1
            i, AEcomplogic = AEcomp(i)
            if (AEcomplogic):
                return i, True
    return i-1, True

def OEcomp(i):
    if (TS[i][0] == "or"):
        i+=1
        i, AElogic = AE(i)
        if (AElogic):
            i+=1
            i, OEcomplogic = OEcomp(i)
            if (OEcomplogic):
                return i, True
    return i-1, True


def map_decl(i):
    if (TS[i][0] == "ID"):
        i+=1
        if (TS[i][0] == "SAO"):
            i+=1
            if (TS[i][0] == "map"):
                i+=1
                if (TS[i][0] == "OCB"):
                    i+=1
                    i, OElogic = OE(i)
                    if (OElogic):
                        i+=1
                        if (TS[i][0] == "colon"):
                            i+=1
                            i, OElogic = OE(i)
                            if (OElogic):
                                i+=1
                                i, contlogic = cont(i)
                                if (contlogic):
                                    i+=1
                                    if (TS[i][0] == "CCB"):
                                        i+=1
                                        if (TS[i][0] == ";"):
                                            return i, True
    return i, False

def L(i):
    i, listClogic = listComp(i)
    if (listClogic):
        return i, True
    i, OElogic = OE(i)
    if (OElogic):
        return i, True
    return i, False
    

def contComp(i):
    if (TS[i][0] == "comma"):
        i+=1
        i, Llogic = L(i)
        if (Llogic):
            i+=1
            i, contClogic = contComp(i)
            if (contClogic):
                return i, True
    return i, True

def listComp(i):
    if (TS[i][0] == "list"):
        i+=1
        if (TS[i][0] == "OSB"):
            i+=1
            i, Llogic = L(i)
            if (Llogic):
                i+=1
                i, contClogic = contComp(i)
                if (contClogic):
                    if (TS[i][0] == "CSB"):
                        return i, True
    return i, False

def list_decl(i):
    if (TS[i][0] == "ID"):
        i+=1
        if (TS[i][0] == "OSB"):
            i+=1
            i, indlogic = ind(i)
            if (indlogic):
                i+=1
                if (TS[i][0] == "CSB"):
                    i+=1
                    if (TS[i][0] == "SAO"):
                        i+=1
                        i, listcomp_logic = listComp(i)
                        if (listcomp_logic):
                            i+=1
                            if (TS[i][0] == ";"):
                                return i, True
    return i, False
