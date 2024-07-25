game_weapons = {
    "rusty_dagger": {"name": "Rusty Dagger", "damage": 5},
    "short_sword": {"name": "Short Sword", "damage": 10},
    "long_sword": {"name": "Long Sword", "damage": 15},
    "battle_axe": {"name": "Battle Axe", "damage": 20},
    "war_hammer": {"name": "War Hammer", "damage": 25},
    "magic_staff": {"name": "Magic Staff", "damage": 30},
    "flaming_sword": {"name": "Flaming Sword", "damage": 35},
    "ice_spear": {"name": "Ice Spear", "damage": 40},
    "thunder_bow": {"name": "Thunder Bow", "damage": 45},
    "dragon_slayer": {"name": "Dragon Slayer", "damage": 50}
}

game_armor = {
    "leather_armor": {"name": "Leather Armor", "defense": 5},
    "chainmail_armor": {"name": "Chainmail Armor", "defense": 10},
    "iron_armor": {"name": "Iron Armor", "defense": 15},
    "steel_armor": {"name": "Steel Armor", "defense": 20},
    "mithril_armor": {"name": "Mithril Armor", "defense": 25},
    "dragon_scale_armor": {"name": "Dragon Scale Armor", "defense": 30},
    "magic_robes": {"name": "Magic Robes", "defense": 35},
    "shadow_cloak": {"name": "Shadow Cloak", "defense": 40},
    "holy_armor": {"name": "Holy Armor", "defense": 45},
    "titanium_armor": {"name": "Titanium Armor", "defense": 50}
}

game_monsters = {
    "goblin": {"name": "Goblin", "health": 50, "damage": 10},
    "skeleton_warrior": {"name": "Skeleton Warrior", "health": 30, "damage": 5},
    "orc": {"name": "Orc", "health": 70, "damage": 15},
    "troll": {"name": "Troll", "health": 100, "damage": 20},
    "vampire": {"name": "Vampire", "health": 60, "damage": 25},
    "werewolf": {"name": "Werewolf", "health": 80, "damage": 30},
    "dragon": {"name": "Dragon", "health": 150, "damage": 40},
    "lich": {"name": "Lich", "health": 90, "damage": 35},
    "giant_spider": {"name": "Giant Spider", "health": 40, "damage": 10},
    "dark_knight": {"name": "Dark Knight", "health": 120, "damage": 50}
}


class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage


class Armor:
    def __init__(self, name, defense):
        self.name = name
        self.defense = defense


class Enemy:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def attack(self, target):
        target.take_damage(self.damage)

# Expose classes and game data for import
__all__ = ["game_weapons", "game_armor", "game_monsters", "Weapon", "Armor", "Enemy"]
