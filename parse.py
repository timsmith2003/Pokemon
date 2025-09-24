# parse.py

from google.cloud.firestore_v1 import FieldFilter, Or, And
from pyparsing import Word, alphas, nums, Literal, ParseException
import admin
from poke_class import Pokemon

_db = admin.db
pokemon_ref = _db


#Grammar Elements
text = Word(alphas)
integer = Word(nums)
equals = Literal('=')
_is = Literal('is')
greater_than = Literal('>')
less_than = Literal('<')

#Grammars
t = text
tet = text + equals + text
tei = text + equals + integer
is_tet = text + _is + text
is_tei = text + _is + integer
greater_tei = text + greater_than + integer
less_tei = text + less_than + integer
tett = text + equals + text + text
tistt = text + _is + text + text


mega_list = ['Venusaur', 'Blastoise', 'Charizard', 'Gyarados', 'Pidgeot', 'Beedrill', 'Gengar', 'Alakazam',
             'Slowbro', 'Kangaskhan', 'Pinsir', 'Aerodactyl', 'Mewtwo']

#POSSIBLE INPUTS
# 1) Help, Quit - text
# 2) Name, Type - text = text
# 3) Number, HP - text = int
# 4) CURRENTLY UNACCOUNTED FOR : Mega (text text)
# 5) Name and/or Type - text = text and/or text = text
# 6) Name and/or Number - text = text and/or text = int
# 7) Number and/or Name - text = int and/or text = text
# 8) number and/or HP - text = int and/or text = int


def parse(line: str):
    # Normalize
    line = line.lower().strip()

    # split on ' and '
    if ' and ' in line and len(line) > 3:
        # -4 due to five characters in ' and '
        for i in range(len(line) - 4):
            # parse to left and right of the and
            if line[i:i+5] == ' and ':
                left  = parse(line[:i])
                right = parse(line[i+5:])
                return left + ['and'] + right

    # split on ' or '
    if ' or ' in line and len(line) > 2:
        # -3 due to four characters in ' or '
        for i in range(len(line) - 3):
            # parse to the left and right of the or
            if line[i:i+4] == ' or ':
                left  = parse(line[:i])
                right = parse(line[i+4:])
                return left + ['or'] + right

    # try tei
    try:
        # Use asList to convert parseList into regular python list for consistency
        val = tei.parseString(line).asList()
        # normalize operator and cast integer for firestore
        val[1] = '=='
        val[2] = int(val[2])
        return val
    except ParseException:
        pass

    # try tei with 'is'
    try:
        # Use asList to convert parseList into regular python list for consistency
        val = is_tei.parseString(line).asList()
        # normalize operator and cast integer for firestore
        val[1] = '=='
        val[2] = int(val[2])
        return val
    except ParseException:
        pass

    # Try tei with greater than
    try:
        # Use asList to convert parseList into regular python list for consistency
        val = greater_tei.parseString(line).asList()
        # normalize operator and cast integer for firestore
        val[1] = '>'
        val[2] = int(val[2])
        return val
    except ParseException:
        pass

    # Try tei with less than
    try:
        # Use asList to convert parseList into regular python list for consistency
        val = less_tei.parseString(line).asList()
        # normalize operator and cast integer for firestore
        val[1] = '<'
        val[2] = int(val[2])
        return val
    except ParseException:
        pass

    # Multi-word handle Mr Mime
    try:
        res = tett.parseString(line).asList()
        # convert user input operator to firestore operator
        if res[2] == 'mr':
            res[2] = res[2] + ' ' + res[3].title()
            res.pop()
        res[1] = '=='
        print(res)
        return res

    except ParseException:
        pass

    try:
        res = tistt.parseString(line).asList()
        # convert user input operator to firestore operator
        if res[2] == 'mr':
            res[2] = res[2] + ' ' + res[3].title()
            res.pop()
        res[1] = '=='
        return res

    except ParseException:
        pass

    # try tet
    try:
        res = tet.parseString(line).asList()
        # convert user input operator to firestore operator
        res[1] = '=='
        return res
    except ParseException:
        pass

    # try tet with 'is'
    try:
        res = is_tet.parseString(line).asList()
        # convert user input operator to firestore operator
        res[1] = '=='
        return res
    except ParseException:
        pass

    # try t
    try:
        res = t.parseString(line).asList()
        return res
    except ParseException:
        pass

    raise SyntaxError("Invalid Query Syntax: query doesn't match possible grammars. \n"
                      "Possible grammars include: \n 'text =/is text', 'text =/is integer, "
                      "'text > integer', \n 'text < integer', or 'text =/is text text' ")



#What is the structure of a query call?

def single_query(field, op, value):
    # Map each token to its corresponding firestore names
    path, operator, val = map_field_value(field, op, value)
    q = pokemon_ref.where(filter=FieldFilter(path, operator, val)).get()
    for doc in q:
        p = Pokemon.from_dict(source=doc)
        p.print_poke()

def and_query(lhs, rhs):
    # Map each token to its corresponding firestore name
    # l is everything to the left of the and and r is everything to the right of it
    lfield, lop, lval = map_field_value(*lhs)
    rfield, rop, rval = map_field_value(*rhs)
    if lfield == 'type' and rfield == 'type':
        q = pokemon_ref.where(filter=FieldFilter(lfield, lop, lval)).get()
        for doc in q:
            p = Pokemon.from_dict(source=doc)
            if rval in p.get_types():
                p.print_poke()
    else:
        q = pokemon_ref.where(filter=FieldFilter(lfield, lop, lval)) \
            .where(filter=FieldFilter(rfield, rop, rval)).get()
        for doc in q:
            p = Pokemon.from_dict(source=doc)
            p.print_poke()


def or_query(lhs, rhs):
    # Map each token to its corresponding firestore name
    # l is everything to the left of the or and r is everything to the right of it
    lfield, lop, lval = map_field_value(*lhs)
    rfield, rop, rval = map_field_value(*rhs)
    q = pokemon_ref.where(filter=Or([
        FieldFilter(lfield, lop, lval),
        FieldFilter(rfield, rop, rval),
    ])).get()
    for doc in q:
        p = Pokemon.from_dict(source=doc)
        p.print_poke()


def query():
    print("Type 'help' for examples, 'quit' to exit.")
    # Loop for querying
    while True:
        try:
            user = input("Enter a query: ").strip()
            tokens = parse(user)

            # Handles help or quit tokens
            if len(tokens) == 1:
                val = tokens[0]
                if val == 'help':
                    print("Options you can query:\n" \
                          "Name - Input name of pokemon\n" \
                          "   Example: Name = Charizard\n" \
                          "   Will return Charizard's Name, Number, and stats\n" \
                          "Number - Input ID number of pokemon\n" \
                          "   Example: Number = 6\n" \
                          "   Will return Pokemon No. 6's Name, Number, and Types\n" \
                          "Type - Input Pokemon's type\n" \
                          "   Example: Type = Fire\n" \
                          "   Will return all names, numbers and types of pokemon with that type\n" \
                          "Stat - Input value corresponding to a pokemon's stat\n" \
                          "   Example: HP > 90\n" \
                          "   Example: Attack = 130\n" \
                          "   Example: Defense = 165\n" \
                          "   Example: SpAttack = 80\n" \
                          "   Example: SpDefense < 85\n" \
                          "   Example: Speed = 90\n" \
                          "   Will return Pokemon Name, Number, and Types that match the stat you input\n" \
                          "And/Or - Input multiple conditions to narrow query\n" \
                          "   Example: Type = Fire and Type = Flying\n" \
                          "   Example: Type = Bug or HP > 90\n" \
                          "Help - Will show this help menu\n" \
                          "Quit - Will end the program")

                    continue
                elif val == 'quit':
                    print("See you later alligator. ")
                    break
                else:
                    print(f"Unknown command: {val}")
                    print("Follow the rules of the grammar: \n"
                          "'X =/is Y', 'X =/is Y and/or W =/is Z'")
                continue
            # Handles simple tokens like name = charmander -> [name, =, charmander]
            if len(tokens) == 3:
                single_query(tokens[0], tokens[1], tokens[2])
                continue

            # Handles compound and | or tokens like name = charmander or type = grass
            if len(tokens) == 7 and tokens[3] in ('and', 'or'):
                # Split the query in half excluding where the and/or will be
                lhs = tokens[0:3]
                rhs = tokens[4:7]

                # If middle token is an and go to and_query
                if tokens[3] == 'and':
                    and_query(lhs, rhs)
                # If middle token is an or go to or_query
                else:
                    or_query(lhs, rhs)
                continue

            # If input doesn't match defined grammar
            raise SyntaxError("Unsupported query form.")

        # Catch any errors
        except Exception as e:
            print(f"Error: {e}")

# Mapping for firestore
def map_field_value(field, op, value):
    # Normalize field key
    f = field.strip()

    # Normalize string values
    if isinstance(value, str):
        v = value.strip().title()
    else:
        v = value
    try:
        if f == 'name':
            # firestore name
            return ('name', op, v)
        elif f == 'type':
            # Types are held in an array
            return ('type', 'array_contains', v)
        # Enables searching for pokedex number by 'number' or 'id'
        elif f in ('number', 'id'):
            return ('id', op, v)
        # Enables search by hp
        elif f == 'hp':
            # firestore hp
            return ('hp', op, v)
        elif f == 'attack':
            # firestore attack
            return ('Attack', op, v)
        elif f == 'defense':
            # firestore defense
            return ('Defense', op, v)
        elif f == 'speed':
            # firestore speed
            return ('Speed', op, v)
        elif f == 'spAttack':
            # firestore spAttack
            return ('spAttack', op, v)
        elif f == 'spDefense':
            # firestore spDefense
            return ('spDefense', op, v)
        else:
            print("Unknown field:", f)
            print('Use "Name", "Number", "Type", "HP", "Defense",  \n',
                  '"Attack", "Speed", "spAttack", or "spDefense" ')

        # fallback
        return (f, op, v)

    except Exception as e:
        print(f"Error: {e}")

# Run program
if __name__ == '__main__':
    query()
