import random
from game_data import game_weapons, game_armor, game_monsters, Enemy, Weapon, Armor


class Room:
    def __init__(self, name, description, connections=None, enemy=None, item=None, npcs=None):
        self.name = name
        self.description = description
        self.connections = connections if connections else {}
        self.enemy = enemy
        self.item = item
        self.npcs = npcs if npcs else []
        self.searched = False

    def get_enemy(self):
        if self.enemy and random.random() < 0.3:  # 30% chance to encounter an enemy
            return self.enemy
        return None


class DungeonMap:
    def __init__(self):
        self.rooms = self.create_rooms()
        self.current_room = self.rooms["Entrance Hall"]  # Start in the Entrance Hall

    def create_rooms(self):
        return {
            "Entrance Hall": Room(
                "Entrance Hall",
                "The entrance hall is a grand, echoing chamber filled with flickering torches casting eerie shadows. "
                "Cobwebs drape from the high ceiling, and the air smells musty with a hint of decay. The stone walls are "
                "lined with ancient, faded tapestries depicting long-forgotten battles.",
                connections={"north": "Armory", "east": "Library", "south": "Hidden Alcove"}
            ),
            "Armory": Room(
                "Armory",
                "The armory is a cluttered space filled with rusty weapons and battered armor. Old wooden racks hold "
                "swords, axes, and spears in various states of disrepair. A large iron anvil sits in the center, covered "
                "in dust.",
                connections={"south": "Entrance Hall"},
                item=Weapon(**game_weapons["short_sword"])
            ),
            "Library": Room(
                "Library",
                "The library is a vast room filled with shelves that stretch to the ceiling, packed with ancient tomes and "
                "scrolls. Dust motes float in the air, disturbed by your presence. The scent of old paper and leather is "
                "overwhelming. A flickering candle illuminates a particularly "
                "large and old book that catches your eye.",
                connections={"west": "Entrance Hall", "north": "Dining Hall"}
            ),
            "Dining Hall": Room(
                "Dining Hall",
                "The dining hall is dominated by a long wooden table set for a feast that never happened. Plates, cups, and "
                "cutlery are neatly arranged, but covered in a thick layer of dust. Chairs are haphazardly pushed back as if "
                "the diners left in a hurry.",
                connections={"south": "Library", "east": "Treasure Room"}
            ),
            "Treasure Room": Room(
                "Treasure Room",
                "The treasure room is small but richly adorned. Golden candelabras line the walls, casting a soft glow over "
                "the treasure chest in the center of the room. The chest is locked with an intricate mechanism.",
                connections={"west": "Dining Hall", "north": "Guard Room", "west": "Collapsed Tunnel"}  
            ),
            "Guard Room": Room(
                "Guard Room",
                "The guard room is sparse, with simple beds and wooden chests at their feet. A large wooden table occupies the "
                "center, scattered with playing cards and tankards. The air is heavy with the scent of stale ale. You notice a skeleton warrior standing guard.",
                connections={"south": "Treasure Room", "east": "Alchemy Lab", "north": "Ancient Shrine"},
                enemy=Enemy(**game_monsters["skeleton_warrior"])
            ),
            "Alchemy Lab": Room(
                "Alchemy Lab",
                "The alchemy lab is a chaotic mess of bottles, jars, and strange apparatuses. The scent of various herbs and chemicals "
                "mingles in the air, creating a pungent aroma. The workbench is cluttered with notes and ingredients.",
                connections={"west": "Guard Room", "north": "Prison Cell"}
            ),
            "Prison Cell": Room(
                "Prison Cell",
                "The prison cell is dark and damp, with iron bars rusting away. A single torch flickers weakly on the wall, casting "
                "shadows that dance across the cold stone floor. There is an old prisoner here, looking at you with weary eyes.",
                connections={"south": "Alchemy Lab", "east": "Secret Passage"}
            ),
            "Secret Passage": Room(
                "Secret Passage",
                "The secret passage is narrow and dimly lit, with walls that seem to close in around you. It twists and turns in unexpected "
                "ways, making it easy to get lost. The air is cold and carries a faint whisper of past secrets.",
                connections={"west": "Prison Cell", "north": "Boss Chamber"}
            ),
            "Boss Chamber": Room(
                "Boss Chamber",
                "The boss chamber is a massive, echoing cavern filled with the sound of dripping water. Stalactites hang from the ceiling, "
                "and the floor is uneven and treacherous. At the far end of the chamber, a dragon sleeps atop a mountain of gold and jewels.",
                connections={"south": "Secret Passage"},
                enemy=Enemy(**game_monsters["dragon"])
            ),
            # New Dungeon Rooms
            "Hidden Alcove": Room(
                "Hidden Alcove",
                "You stumble upon a hidden alcove concealed behind a tapestry. A faint glow emanates from a small chest tucked away in the corner.",
                connections={"north": "Entrance Hall"},
                item=Weapon(**game_weapons["magic_staff"])
            ),
            "Collapsed Tunnel": Room(
                "Collapsed Tunnel",
                "The tunnel ahead is blocked by a massive cave-in. You'll need to find another way around.",
                connections={"east": "Treasure Room"}
            ),
            "Ancient Shrine": Room(
                "Ancient Shrine",
                "An ancient shrine stands in the center of the chamber, adorned with intricate carvings. The air is thick with an aura of forgotten power.",
                connections={"south": "Guard Room"}
            ),

            # Town Area
            "Town Square": Room(
                "Town Square",
                "The heart of the town, bustling with activity. You see a fountain in the center and various paths leading in different directions.",
                connections={"north": "Blacksmith", "south": "General Store", "east": "Inn", "west": "Town Gate"}
            ),
            "Blacksmith": Room(
                "Blacksmith",
                "The clang of hammer on steel fills the air. A burly blacksmith works diligently at his forge. The walls are lined with weapons and armor.",
                connections={"south": "Town Square"},
                npcs=["Blacksmith"]
            ),
            "General Store": Room(
                "General Store",
                "The shelves are stocked with a variety of goods: potions, torches, rations, and other adventuring essentials.",
                connections={"north": "Town Square"},
                npcs=["Shopkeeper"]
            ),
            "Inn": Room(
                "Inn",
                "A cozy tavern with a warm fire and the smell of roasting meat. Travelers and locals alike gather here to share stories and unwind.",
                connections={"west": "Town Square"},
                npcs=["Innkeeper", "Bard"]
            ),
            "Town Gate": Room(
                "Town Gate",
                "The imposing town gate stands tall, guarding the entrance to the settlement. Guards patrol the walls, ensuring the safety of those within.",
                connections={"east": "Town Square"},
                npcs=["Guard"]
            )
        }
  

    def move(self, directions):
        for direction in directions.split():
            if direction in self.current_room.connections:
                self.current_room = self.rooms[self.current_room.connections[direction]]
                print(f"You move {direction}.")
            else:
                print(f"You cannot move {direction}.")

        return self.current_room
