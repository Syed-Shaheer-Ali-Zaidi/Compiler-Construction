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
    print("Invalid Constant at ", TS[i][1], " in line number ", TS[i][2])
    return i, False 
    

def list2(i):
    if (TS[i][0] == ";"):
        return i, True
    if (TS[i][0] == "comma"):
        i+=1
        if (TS[i][0] == "ID"):
            i+=1
            if (TS[i][0] == "comma" or TS[i][0] == ";" or TS[i][0] == "SAO"):
                i, listLogic = list(i)
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

def init(i):
    if (TS[i][0] == "ID"):
        i+=1
        if (TS[i][0] == "comma" or TS[i][0] == ";" or TS[i][0] == "SAO"):
            i, listLogic = list(i)
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
            i+=1
            if (TS[i][0] == ";" or TS[i][0] == "comma"):
                i, list2Logic = list2(i)
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


def list(i):
    if (TS[i][0] == "comma"):
        i+=1
        if (TS[i][0] == "ID"):
            i+=1
            if (TS[i][0] == "comma" or TS[i][0] == ";" or TS[i][0] == "SAO"):
                i, listLogic = list(i)
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
        return i, True
    elif (TS[i][0] == "SAO"):
        i+=1
        if (TS[i][0] == "ID" or TS[i][0] == "INTCONST" or TS[i][0] == "FLTCONST" or TS[i][0] == "TEXTCONST" or TS[i][0] == "CHRCONST" or TS[i][0] == "LOGICCONST"):
            i, initLogic = init(i)
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
        i+=1
        if (TS[i][0] == "ID"):
            i+=1
            if (TS[i][0] == "comma" or TS[i][0] == ";" or TS[i][0] == "SAO"):
                i, listLogic = list(i)
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
                i+=1
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

def cond(i):
    i, OElogic = OE(i)
    if (OElogic):
        return i, True
    return i, True

def if_func(i):
    if (TS[i][0] == "conditional"):
        i+=1
        if (TS[i][0] == "ORB"):
            i+=1
            i, OElogic = OE(i)
            if (OElogic):
                i+=1
                if (TS[i][0] == "CRB"):
                    i+=1
                    if (TS[i][0] == "OCB"):
                        i+=1
                        i, bodylogic = Body(i)
                        if (bodylogic):
                            i+=1
                            if (TS[i][0] == "CCB"):
                                return i, True
    return i, False

def if_else(i):
    i, iflogic = if_func(i)
    if (iflogic):
        i+=1
        if (TS[i][0] == "else"):
            i+=1
            if (TS[i][0] == "ORB"):
                i+=1
                i, condLogic = cond(i)
                if(condLogic):
                    i+=1
                    if (TS[i][0] == "CRB"):
                        i+=1
                        if (TS[i][0] == "OCB"):
                            i+=1
                            i, bodylogic = Body(i)
                            if (bodylogic):
                                i+=1
                                if (TS[i][0] == "CCB"):
                                    i+=1
    return i, False

def else_if(i):
    i, iflogic = if_func(i)
    if (iflogic):
        i+=1
        i, elselogic = else_st(i)
        if (elselogic):
            return i, True
    return i, False

def else_st(i):
    if (TS[i][0] == "else"):
            i+=1
            if (TS[i][0] == "ORB"):
                i+=1
                i, condLogic = cond(i)
                if(condLogic):
                    i+=1
                    if (TS[i][0] == "CRB"):
                        i+=1
                        if (TS[i][0] == "OCB"):
                            i+=1
                            i, bodylogic = Body(i)
                            if (bodylogic):
                                i+=1
                                if (TS[i][0] == "CCB"):
                                    i+=1
                                    i, elselogic = else_st(i)
                                    if (elselogic):
                                        return i, True
    elif(TS[i][0]=="elif"):
        i+=1
        if (TS[i][0] == "ORB"):
            i+=1
            i, condLogic = cond(i)
            if(condLogic):
                i+=1
                if (TS[i][0] == "CRB"):
                    i+=1
                    if (TS[i][0] == "OCB"):
                        i+=1
                        i, bodylogic = Body(i)
                        if (bodylogic):
                            i+=1
                            if (TS[i][0] == "CCB"):
                                i+=1
                                i, elselogic = else_st(i)
                                if (elselogic):
                                    return i, True
    return i, True

def NT(i):
    i, IDlogic = ID(i)
    if (IDlogic):
        return i, True
    if (TS[i][0] == "range"):
        i+=1
        if (TS[i][0] == "INTCONST"):
            return i, True
    return i, False

def for_func(i):
    if (TS[i][0] == "for"):
        i+=1
        i, idlogic = ID(i)
        if(idlogic):
            i+=1
            if (TS[i][1] == "in"):
                i+=1
                i, NTlogic = NT(i)
                if (NTlogic):
                    i+=1
                    if (TS[i][0] == "OCB"):
                        i+=1
                        i, bodylogic = Body(i)
                        if (bodylogic):
                            i+=1
                            if (TS[i][0] == "CCB"):
                                return i, True
    return i, False

def A(i):
    if(TS[i][0] == "SAO"):
        return i, True
    elif (TS[i][0] == "CAO"):
        return i, True
    return i, False

def assign(i):
    i, IDlogic = ID(i)
    if(IDlogic):
        i+=1
        i, Alogic = A(i)
        if (Alogic):
            i, OElogic = OE(i)
            if (OElogic):
                i+=1
                if (TS[i][0] == ";"):
                    return i, True
    return i, False

def obj_dec(i):
    if (TS[i][0] == "ID"):
        i+=1
        if (TS[i][0] == "SAO"):
            i+=1
            if(TS[i][0] == "ID"):
                i+=1
                if (TS[i][0] == "ORB"):
                    i += 1  
                    i, argsLogic = args(i)
                    if (argsLogic):
                        i+=1
                        if (TS[i][0] == "CRB"):
                            i+=1
                            if (TS[i][0] == ";"):
                                return i, True
    return i, False

def exp(i):
    i, constLogic = const(i)
    if (constLogic):
        return i, True
    i , IDlogic = ID(i)
    if (IDlogic):
        return i-1, True
    return False

def ret(i):
    if (TS[i][0] == "return"):
        i+=1
        i, expLogic = exp(i)
        if (expLogic):
            print(TS[i][0])
            i+=1
            if (TS[i][0] == ";"):
                return i, True
    return i, False

def try_catch(i):
    if (TS[i][0] == "try"):
        i+=1
        if (TS[i][0] == "OCB"):
            i+=1
            i, bodyLogic = Body(i)
            if (bodyLogic):
                i+=1
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
                                        i, bodyLogic = Body(i)
                                        if (bodyLogic):
                                            i+=1
                                            if (TS[i][0] == "CCB"):
                                                return i, True
    return i, False

def while_st(i):
    if (TS[i][0] == "conditional"):
        i+=1
        if (TS[i][0] == "ORB"):
            i+=1
            i, OElogic = OE(i)
            if (OElogic):
                i+=2
                if (TS[i][0] == "CRB"):
                    i+=1
                    if (TS[i][0] == "OCB"):
                        i+=1
                        i, bodylogic = Body(i)
                        if (bodylogic):
                            i+=1
                            if (TS[i][0] == "CCB"):
                                return i, True
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
                        return i, True
    return i, False

def ip(i):
    if (TS[i][0] == "TEXTCONST"):
        return i, True
    return i, True

def take(i):
    i, IDlogic = ID(i)
    if (IDlogic):
        i+=1
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
                                i+=1
                                if (TS[i][0] == "CRB"):
                                    i+=1
                                    if (TS[i][0] == "CRB"):
                                        i+=1
                                        if (TS[i][0] == ";"):
                                            return i, True
    return i, False

def arg3(i):
    i, IDlogic = ID(i)
    if (IDlogic):
        i+=1
        i, arg2logic = arg2(i)
        if (arg2logic):
            return i, True
        
    i, constlogic = const(i)
    if (constlogic):
        i+=1
        i, arg2logic = arg2(i)
        if (arg2logic):
            return i, True
    
    return i, False

def arg2(i):
    if (TS[i][0] == "comma"):
        i+=1
        i, arg3logic = arg3(i)
        if (arg3logic):
            return i, True
    return i, True


def arg(i):
    i, IDlogic = ID(i)
    if (IDlogic):
        i+=1
        i, arg2logic = arg2(i)
        if (arg2logic):
            return i, True
    
    i, constlogic = const(i)
    if (constlogic):
        i+=1
        i, arg2logic = arg2(i)
        if (arg2logic):
            return i, True
    return i-1, True        

def display(i):
    if (TS[i][0] == "print"):
        i+=1
        if (TS[i][0] == "ORB"):
            i+=1
            i, arglogic = arg(i)
            if (arglogic):
                i+=1
                if (TS[i][0] == "CRB"):
                    i+=1
                    if (TS[i][0] == ";"):
                        return i, True
    return i, False

def var_list2(i):
    if (TS[i][0] == "comma"):
                i+=1
                if (TS[i][0] == "ID"):
                    i+=1
                    i, var2logic = var_list2(i)
                    if (var2logic):
                        return i, True
    return i, True

def var_list(i):
    if (TS[i][0] == "ID"):
        i+=1
        i, var2logic = var_list2(i)
        if (var2logic):
            return i, True
    return i, False

def extract(i):
    if (TS[i][0] == "DT"):
        i+=1
        i, varlogic = var_list(i)
        if (varlogic):
            i+=1
            if (TS[i][0] == "SAO"):
                i+=1
                if (TS[i][0] == "extract"):
                    i+=1
                    if (TS[i][0] == "ID"):
                        i+=1
                        if (TS[i][0] == ";"):
                            return i, True
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
    return i, True

def argscomp(i):
    if (TS[i][0] == "DT"):
        i+=1
        if (TS[i][0] == "ID"):
            i+=1
            i, args2logic = args2(i)
            if (args2logic):
                return i, True
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
                        i+=1
                        if (TS[i][0] == "CRB"):
                            i+=1
                            if (TS[i][0] == "OCB"):
                                i+=1
                                i, bodylogic = Body(i)
                                if (bodylogic):
                                    i+=1
                                    if (TS[i][0] == "CCB"):
                                        return i, True
    return i, False

def SST(i):
    i, Decl_logic = Decl(i)
    if (Decl_logic):
        return i, True
    
    i, mapdecl_logic = map_decl(i)
    if (mapdecl_logic):
        return i, True
    
    i, listdecl_logic = list_decl(i)
    if (listdecl_logic):
        return i, True
    
    i, whilest_logic = while_st(i)
    if (whilest_logic):
        return i, True
    
    i, if_logic = if_func(i)
    if (if_logic):
        return i, True
    
    i, ifelse_logic = if_else(i)
    if (ifelse_logic):
        return i, True
    
    i, elif_logic = else_if(i)
    if (elif_logic):
        return i, True
    
    i, for_logic = for_func(i)
    if (for_logic):
        return i, True
    
    i, assign_logic = assign(i)
    if (assign_logic):
        return i, True
    
    i, obj_logic = obj_dec(i)
    if (obj_logic):
        return i, True
    
    i, fc_logic = fn_call(i)
    if (fc_logic):
        return i, True
    
    i, ret_logic = ret(i)
    if (ret_logic):
        return i, True
    
    i, tc_logic = try_catch(i)
    if (tc_logic):
        return i, True
    
    i, fd_logic = func_def(i)
    if (fd_logic):
        return i, True
    
    i, ex_logic = extract(i)
    if (ex_logic):
        return i, True
    
    i, dis_logic = display(i)
    if (dis_logic):
        return i, True
    
    i, take_logic = take(i)
    if (take_logic):
        return i, True
    
    i, bring_logic = bring_st(i)
    if (bring_logic):
        return i, True
    return i, False
    

def MST(i):
    i, SSTlogic = SST(i)
    if (SSTlogic):
        i+=1
        i, MSTlogic = MST(i)
        if (MSTlogic):
            return i, True
    return i-1, True

def Body(i):
    i, SSTlogic = SST(i)
    if (SSTlogic):
        return i, True
    
    i, MSTlogic = MST(i)
    if (MSTlogic):
        return i, True

    return i, False

def acc_mod(i):
    if (TS[i][0] == "AM"):
        return i+1 , True
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
                        i+=1
                        if (TS[i][0] == "CRB"):
                            i+=1
                            if (TS[i][0] == "OCB"):
                                i+=1
                                i, MSTlogic = MST(i)
                                if (MSTlogic):
                                    i+=1
                                    if (TS[i][0] == "CCB"):
                                        return i, True
        return i, False

def AOM(i):
    i, accmodlogic = acc_mod(i)
    if (accmodlogic):
        if (TS[i][0] == "DT"):
            i+=1
            i, declLogic = Decl(i)
            if (declLogic):
                i+=1
                i, AOMlogic = AOM(i)
                if (AOMlogic):
                    return i, True
        if (TS[i][0] == "def"):
            i+=1
            i, funcLogic = func_def(i)
            if(funcLogic):
                i+=1
                i, AOMlogic = AOM(i)
                if(AOMlogic):
                    return i, True
        if (TS[i][0] == "init"):
            i+=1
            i, constrLogic = constr(i)
            if (constrLogic):
                i+=1
                i, AOMlogic = AOM(i)
                if(AOMlogic):
                    return i, True
        return i-1, True


def class_decl(i):
    if (TS[i][0] == "class"):
        i+=1
        if (TS[i][0] == "ID"):
            i+=1
            if (TS[i][0] == "OCB"):
                i+=1
                i, AOMlogic = AOM(i)
                if(AOMlogic):
                    i+=1
                    if (TS[i][0] == "CCB"):
                        return i+2, True
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
                                        i += 1
                                        if (TS[i][0] == "CCB"):
                                            return i+2, True
    return i, False

def S(i):
    if (TS[i][0] == "$"):
        return i, True
    if (TS[i][0] == "class"):
        i+=1
        if (TS[i][0] == "ID"):
            i+=1
            i, classLogic = class_decl(i-2)
            i, inhertLogic = inhert(i-2)
            if (inhertLogic or classLogic):
                i+=1
                i, Slogic = S(i)
                return i, Slogic
            else:
                return i, False
        else:
            return i, False
    else:
        i, SSTlogic = SST(i)
        if (SSTlogic):
            i+=1
            i, Slogic = S(i)
            return i, Slogic
        else:
            return i, False

i, logic = S(0)
print (logic)