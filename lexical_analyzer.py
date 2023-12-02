import re

kw = {"int" : "DT", "flt" : "DT", "chr" : "DT", "text" : "DT", "logic" : "DT", "void": "DT", "list_of" : "list", "dict_of" : "map", "bring_back" : "return", "while_so" : "conditional", "given" : "conditional", "otherwise" : "else", "else_if" : "elif", "for_each" : "for", "stop" : "flow control","$":"$", "go_on" : "flow control", "doing" : "def", "display" : "print", "take" : "input", "bring" : "import", "extract" : "extract", "as" : "as", "classy" : "class", "is_a" : "inheritance", "has" : "has", "init" : "init","self":"self", "base" : "base", "this" : "this", "priv" : "AM", "pro" : "AM","virtual":"AM" , "range":"range", "try":"try", "except":"except", "sealed":"sealed"}
opr = {"+" : "AO", "-" : "AO", "*" : "AO", "/" : "AO", "%" : "AO", "**" : "AO", "==" : "RO", "!=" : "RO", "<=" : "RO", ">=" : "RO", "<" : "RO", ">" : "RO", "and" : "and", "or" : "or", "!" : "not", "=" : "SAO", "+=" : "CAO", "-=" : "CAO", "in" : "RO", "is" : "RO",}
punc = {";" : ";", ":" : "colon", "," : "comma", "." : "dot", "(" : "ORB", ")" : "CRB", "{" : "OCB", "}" : "CCB", "[" : "OSB", "]" : "CSB", "#/" : "comment"}

def isID(word):
    # Regular expression pattern for a valid identifier
    pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'

    if re.match(pattern, word):
        return True
    else:
        return False
    
def isIntConst(word):
    # Regular expression pattern for a valid identifier
    pattern = r'^[+-]?\d+$'

    if re.match(pattern, word):
        return True
    else:
        return False
    
def isFltConst(word):
    # Regular expression pattern for a valid identifier
    pattern = r'^[+-]?\d+(\.\d+)?$'

    if re.match(pattern, word):
        return True
    else:
        return False
    
def isChrConst(word):
    # Regular expression pattern for a valid identifier
    pattern = r'^\'[^\']\'$'

    if re.match(pattern, word):
        return True
    else:
        return False
    
def isTextConst(word):
    # Regular expression pattern for a valid identifier
    pattern = r'^\"[^\"]*\"$'

    if re.match(pattern, word):
        return True
    else:
        return False
    
def isKW(word):
    temp = kw.get(word)
    if (temp):
        return True
    else:
        return False
    
def isOpr(word):
    temp = opr.get(word)
    if (temp):
        return True
    else:
        return False
    
def isPunc(word):
    temp = punc.get(word)
    if (temp):
        return True
    else:
        return False
    
def isStringEnd(word):
    temp = kw.get(word)
    if (temp):
        return True
    else:
        return False

def generateToken(word, line, i):
    CP = None
    token_str = []
    if(isID(word)):
        CP=kw.get(word)
        if(CP == None):
            CP='ID'
    elif(isIntConst(word)):
        CP ='INTCONST'
    elif(isFltConst(word)):
        CP ="FLTCONST"
    elif(isChrConst(word)):
        CP ="CHRCONST"
    elif(isTextConst(word)):
        CP ="TEXTCONST"
    elif(isOpr(word)):
        CP = opr.get(word)
    elif(isPunc(word)):
        CP = punc.get(word)
    elif(isStringEnd(word)):
        CP="$"
    else:
        CP = "Invalid_Lexeme"

    token_str = [CP, word, line]
    #token_str = CP + ", " + word + ", " + str(line)
    return "", i, token_str


def breakWords(code):
    word = ""
    line = 1
    tokenList = []
    singleSymb = [",", ";", ":", "(", ")", "{", "}", "[", "]",
                   "-", "+", "*", "/", "%", "=", ">", "<", "!", ".", "$"]
    doubleSymb = [">=", "<=", "!=","+=", "-=","==", "**"]

    i = 0
    while (i < len(code)):
        temp = code[i]

        # checking for \n, return
        if (temp == "\n" or temp == "\r"):
            if (word != ""):
                word, i, current_token = generateToken(word, line, i)
                tokenList.append(current_token)
            else:
                i += 1
            line += 1
            continue

        # checking for space character and tab
        if (temp == " " or temp == "\t"):
            if (word != ""):
                word, i, current_token = generateToken(word, line, i)
                tokenList.append(current_token)
            else:
                i += 1
            continue

        # checking for dot and generating token based on the type of value
        if (code[i] == "."):
            if (word != ""):
                # If the current word contains only numbers then dot is treated as a decimal
                if (word.isnumeric()):
                    word = word + code[i]
                    i += 1
                # If not then the word and dot are separate
                else:
                    word, i, current_token = generateToken(word, line, i)
                    tokenList.append(current_token)

            if (i <= len(code)):
                # If the character succeeding dot is a number then dot is included in word
                checking = code[i]
                if (code[i].isnumeric()):
                    word = word + code[i]
                    i += 1
                # If character following dot is not a number then the dot is a separate word
                else:
                    word = word + code[i]
                    word, i, current_token = generateToken(word, line, i)
                    tokenList.append(current_token)
                    i+=1

            continue
        # checking for string
        if (code[i] == "\""):
            if (word != ""):
                word, i, current_token = generateToken(word, line, i)
                tokenList.append(current_token)
                i -= 1

            word = code[i]
            i = i + 1

            # string continues till the file ends or next double quote or new line character
            while (i < len(code)):
                checking = code[i]
                if (i+1 < len(code)):
                    if (code[i] == "\\"):
                        checking = f"{code[i]}{code[i+1]}"
                        word = word + checking
                        i += 1
                        if (i+1 < len(code)):
                            i += 1
                            continue
                        else:
                            break

                if (code[i] != "\"" and code[i] != "\n"):
                    word = word + code[i]
                    i += 1
                else:
                    break

            # ending the string when a double quote is found
            if (i < len(code) and code[i] == "\""):
                word = word + code[i]
                i+=1

            word, i, current_token = generateToken(word, line, i)
            tokenList.append(current_token)
            continue

        # double symbol word
        if (i + 1 < len(code)):
            checking = f"{code[i]}{code[i+1]}"
        if (i + 1 < len(code) and f"{code[i]}{code[i+1]}" in doubleSymb):
            if (word != ""):
                word, i, current_token = generateToken(word, line, i)
                tokenList.append(current_token)
                i -= 1

            word = f"{code[i]}{code[i+1]}"
            word, i, current_token = generateToken(word, line, i)
            tokenList.append(current_token)
            i += 2  
            continue

        # single symbol word
        if code[i] in singleSymb:
            if word != "":
                word, i, current_token = generateToken(word, line, i)
                tokenList.append(current_token)
            word = code[i]
            word, i, current_token = generateToken(word, line, i)
            tokenList.append(current_token)
            i += 1
            continue

        # comment
        if (code[i] == "~"):
            if (word != ""):
                word, i, current_token = generateToken(word, line, i)
                tokenList.append(current_token)
            else:
                i += 1

            if (i < len(code)):
                checking = code[i]
                # multi comment
                if (code[i] == "~"):
                    i += 1
                    # iterating till the code ends or the comment charachter appears
                    while (i < len(code)):
                        checking = code[i]
                        if (code[i] == "\n"):
                            line += 1
                        if (code[i] == "~" and code[i+1] == "~"):
                            i += 1
                            break
                        i += 1
                    i += 1
                    continue

                # single comment charachter
                else:
                    # iteration till the line or file ends
                    while (i < len(code)):
                        checking = code[i]
                        if (code[i] == "\n"):
                            line += 1
                            break
                        i += 1
                    i += 1
                    continue

        # characters are added to the 'word' if no breaks occur
        word = word + code[i]
        i = i + 1

    # at the end of the file, if the last word has not been broken down into tokens
    if (word != ""):
        word, i, current_token = generateToken(word, line, i)
        tokenList.append(current_token)

    return tokenList

f = open('D:\\Shaheer\\Compiler Construction\\Compiler-Construction\\code.txt', 'r')
code = f.read()
tokens = breakWords(code)
print(tokens)
# with open('D:\\Shaheer\\Syntax Analyzer\\output.txt', 'w') as txt_file:
#     for line in tokens:
#         txt_file.write(" ".join(line) + "\n")
#     print("Token's generated successfully!")