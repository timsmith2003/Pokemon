class Pokemon:
    def __init__(self, id, name, type, hp, attack, defense, spAttack, spDefense, speed):
        self.id = id
        self.name = name
        self.type = type
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.spAttack = spAttack
        self.spDefense = spDefense
        self.speed = speed


    @staticmethod
    def from_dict(source):
        return Pokemon(source.get("id"),
                       source.get("name"),
                       source.get("type"),
                       source.get("hp"),
                       source.get("Attack"),
                       source.get("Defense"),
                       source.get("spAttack"),
                       source.get("spDefense"),
                       source.get("Speed"))

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
            "speed" : self.speed
        }
