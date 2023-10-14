import lexical_analyzer as LA
f = open('D:\\Shaheer\\Syntax Analyzer\\code.txt', 'r')
code = f.read()
TS = LA.breakWords(code)

def const(i):
    if (TS[i][0] == "INTCONST"):
        return True
    if (TS[i][0] == "FLTCONST"):
        return True
    if (TS[i][0] == "CHRCONST"):
        return True
    if (TS[i][0] == "TEXTCONST"):
        return True

def list2(i):
    if (TS[i][0] == ";"):
        return True
    if (TS[i][0] == ","):
        i+=1
        if (TS[i][0] == "ID"):
            i+=1
            if (list(i)):
                return True

def init(i):
    if (TS[i][0] == "ID"):
        i+=1
        if(list(i)):
            return True
    elif (const(i)):
        i+=1
        if(list2(i)):
            return True


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

def Decl(i):
    if (TS[i][0] == "DT"):
        i+=1
        if (TS[i][0] == "ID"):
            i+=1
            if(list(i)):
                return True
    return False

print(Decl(0))