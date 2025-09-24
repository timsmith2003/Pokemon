class Pokemon:
    def __init__(self, id, name, type, hp, attack, defense, spAttack, spDefense, speed, hasMega):
        self.id = id
        self.name = name
        self.type = type
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.spAttack = spAttack
        self.spDefense = spDefense
        self.speed = speed
        try:
            self.hasMega = hasMega
        except KeyError:
            self.hasMega = None





    @staticmethod
    def from_dict(source):
        try:
            hasMega = source.get("hasMega")
        except KeyError:
            hasMega = None
        return Pokemon(source.get("id"),
                       source.get("name"),
                       source.get("type"),
                       source.get("hp"),
                       source.get("Attack"),
                       source.get("Defense"),
                       source.get("spAttack"),
                       source.get("spDefense"),
                       source.get("Speed"),
                       hasMega)

    def to_dict(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "type" : self.type,
            "hp" : self.hp,
            "attack" : self.attack,
            "defense" : self.defense,
            "spAttack" : self.spAttack,
            "spDefense" : self.spDefense,
            "speed" : self.speed,
            "hasMega" : self.hasMega
        }
    def print_poke(self):
        print("Name:" , self.name,"\n"
              "Type:" , self.type,"\n"
              "HP:" , self.hp,"\n"
              "Attack:" , self.attack,"\n"
              "Defense:" , self.defense,"\n"
              "Special Attack:" , self.spAttack,"\n"
              "Special Defense:" , self.spDefense,"\n"
              "Speed:" , self.speed,"\n"
              "Has Mega:" , self.hasMega,"\n")
    def get_types(self):
        return self.type
