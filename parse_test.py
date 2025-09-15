from pyparsing import Word, alphas, nums, Literal, ParseException

#Grammar Elements
text = Word(alphas)
integer = Word(nums)
equals = Literal('=') 

#POSSIBLE INPUTS
# 1) Help, Quit - text
# 2) Name, Type - text = text
# 3) Number, HP - text = int
# 4) CURRENTLY UNACCOUNTED FOR : Mega (text text)
# 5) Name and/or Type - text = text and/or text = text
# 6) Name and/or Number - text = text and/or text = int
# 7) Number and/or Name - text = int and/or text = text
# 8) number and/or HP - text = int and/or text = int

#Grammars
t = text
tet = text + equals + text
tei = text + equals + integer



#TODO:
#mega support
#query functions




#taking user input
line = "Name = Charmander"



def parse(line):
    line = line.lower()
    line = line.strip()

    if ' and ' in line and len(line) > 3:
        for i in range(len(line) - 3):
            if line[i:i + 5] == ' and ':
                line1 = line[:i]
                line2 = line[i + 5:]
                result = parse(line1)
                result.append('and')
                result.extend(parse(line2))
                return result
    if ' or ' in line and len(line) > 2:
        for i in range(len(line) - 2):
            if line[i:i + 4] == ' or ':
                line1 = line[:i]
                line2 = line[i + 4:]
                result = parse(line1)
                result.append('or')
                result.extend(parse(line2))
                return result
            
    try:
        result = tei.parseString(line)
        print("tei")
        #2 possibilities - num, hp 
    except ParseException:
        try:
            result = tet.parseString(line)
            print("tet")
            #2 possibilities - name, type
        except ParseException:
            try:
                result = t.parseString(line)
                print("t")
                #2 possibilities - help, quit
            except ParseException:
                raise SyntaxError("Invalid Query Syntax: query doesn't match possible grammars")
    
    last_word = ""
    curr_char = line[-1]
    index = len(line) - 1
    while curr_char:
        if line[index] == ' ':
            curr_char = ''
        else:
            last_word = line[index] + last_word
        index -= 1
    if last_word == result[-1]:
        return result
    else:
        raise SyntaxError("Invalid Query Syntax: query holds too many arguments")





print(parse(line))




#What is the structure of a query call?

def query():
    0

def t(parsed_input):
    return query([parsed_input[0], parsed_input[1]])