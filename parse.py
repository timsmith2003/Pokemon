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
tt = text + text

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

#TODO:
#mega support

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

    try:
        res = tt.parseString(line).asList()
        return res
    except ParseException:
        pass

    # try t
    try:
        res = t.parseString(line).asList()
        return res
    except ParseException:
        pass

    raise SyntaxError("Invalid Query Syntax: query doesn't match possible grammars")


#What is the structure of a query call?

def single_query(field, op, value):
    # Map each token to its corresponding firestore names
    path, operator, val = map_field_value(field, op, value)
    q = pokemon_ref.where(filter=FieldFilter(path, operator, val)).get()
    for doc in q:
        p = Pokemon.from_dict(source=doc)
        print(p.to_dict())

def and_query(lhs, rhs):
    # Map each token to its corresponding firestore name
    # l is everything to the left of the and and r is everything to the right of it
    lfield, lop, lval = map_field_value(*lhs)
    rfield, rop, rval = map_field_value(*rhs)
    if lfield == 'type' and rfield == 'type':
        first_group = []
        q = pokemon_ref.where(filter=FieldFilter(lfield, lop, lval)).get()
        for doc in q:
            p = Pokemon.from_dict(source=doc)
            if rval in p.get_types():
                print(p.to_dict())
    else:
        q = pokemon_ref.where(filter=FieldFilter(lfield, lop, lval)) \
            .where(filter=FieldFilter(rfield, rop, rval)).get()
        for doc in q:
            p = Pokemon.from_dict(source=doc)
            print(p.to_dict())


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
        print(p.to_dict())

    

def mega_query(field, value):
    if field == 'mega':
        field = 'hasMega'
    q = pokemon_ref.where(filter = FieldFilter(field, value))
    print_docs(q.stream())


# Handles output of firestore data in the console
def print_docs(docs):
    flag = False
    for doc in docs:
        flag = True
        # necessary firestore thing I don't really understand but is probably obvious if I took the time to read
        d = doc.to_dict()
        name = (d['name'])
        types = d.get('type') or []
        hp = (d['hp'])
        if name in mega_list:
            has_mega = (d['hasMega'])
        else:
            has_mega = False
        type_str = "/".join(types) if types else ""
        print(f"{d.get('id')}: {name} [{type_str}], HP={hp}, mega={has_mega}")
    if not flag:
        print("No results.")

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
                    print("Try: Name = charmander | Number = 10 | Type = fire | "
                          "Name = charmander and Type = fire | Name = pikachu or Type = electric")
                    continue
                elif val == 'quit':
                    print("See you later alligator. ")
                    break
                else:
                    print(f"Unknown command: {val}")
                continue
            # Handles simple tokens like name = charmander -> [name, =, charmander]
            if len(tokens) == 3:
                single_query(tokens[0], tokens[1], tokens[2])
                continue

            # Handles mega tokens
            if len(tokens) == 2:
                mega_query(tokens[0], tokens[1])
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
    f = field.strip().lower()

    # Normalize string values
    if isinstance(value, str):
        v = value.strip().title()
    else:
        v = value

    if f == 'name':
        # firestore name
        return ('name', op, v)
    if f == 'type':
        # Types are held in an array
        return ('type', 'array_contains', v)
    # Enables searching for pokedex number by 'number' or 'id'
    if f in ('number', 'id'):
        return ('id', op, v)
    if f == 'hp':
        # firestore hp
        return ('hp', op, v)

    # fallback
    return (f, op, v)

# Run program
if __name__ == '__main__':
    query()
