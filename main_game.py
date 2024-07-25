import random
from game_data import game_weapons, game_armor, game_monsters, Weapon, Armor, Enemy
from game_map import DungeonMap


class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.weapon = None
        self.armor = None
        self.inventory = []

    def take_damage(self, damage):
        if self.armor:
            damage -= self.armor.defense
            if damage < 0:
                damage = 0
        self.health -= damage
        if self.health < 0:
            self.health = 0
        print(f"You take {damage} damage! Your health is now {self.health}.")

    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100
        print(f"You healed for {amount} health points. Your health is now {self.health}.")

    def attack(self):
        if self.weapon:
            return self.weapon.damage
        else:
            return 10  # Unarmed attack damage

    def add_to_inventory(self, item):
        self.inventory.append(item)
        print(f"You added {item.name} to your inventory.")

    def display_inventory(self):
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(f"- {item.name}")

    def equip_weapon(self, weapon):
        self.weapon = weapon
        print(f"You equipped {weapon.name}.")

    def equip_armor(self, armor):
        self.armor = armor
        print(f"You equipped {armor.name}.")

    def drop_item(self, item_name):
        for i, item in enumerate(self.inventory):
            if item.name.lower().replace(" ", "_") == item_name:
                del self.inventory[i]
                print(f"You dropped {item.name}.")
                return
        print("You don't have that item in your inventory.")

    def display_equipment(self):
        print("Equipment:")
        print(f"- Weapon: {self.weapon.name if self.weapon else 'None'}")
        print(f"- Armor: {self.armor.name if self.armor else 'None'}")



def main():
    player_name = input("Enter your name: ")
    player = Player(player_name)
    dungeon_map = DungeonMap()

    print(f"Welcome, {player_name}, to the depths of the dungeon!")

    while player.health > 0:
        current_room = dungeon_map.current_room
        print(f"\nYou are in the {current_room.name}. {current_room.description}")

        available_directions = ", ".join(current_room.connections.keys())
        print(f"You can move in the following directions: {available_directions}")

        enemy = current_room.get_enemy()
        if enemy:
            print(f"You encounter a {enemy.name}!")
            while enemy.health > 0 and player.health > 0:
                action = input("What do you want to do? (attack/heal/flee): ").lower()

                if action == "attack":
                    player_damage = player.attack()
                    enemy.take_damage(player_damage)
                    print(f"You attack the {enemy.name} for {player_damage} damage!")
                    if enemy.health <= 0:
                        print(f"You defeated the {enemy.name}!")
                        break
                elif action == "heal":
                    player.heal(20)  # Heals 20 health points
                    print("You healed yourself for 20 health points.")
                elif action == "flee":
                    if random.random() < 0.5:  # 50% chance of successful flee
                        print("You successfully fled!")
                        break
                    else:
                        print("You failed to flee!")
                else:
                    print("Invalid action.")

                if enemy.health > 0:
                    enemy.attack(player)
                    print(f"The {enemy.name} attacks you for {enemy.damage} damage!")

                print(f"Your Health: {player.health}")
                print(f"{enemy.name}'s Health: {enemy.health}")

        # Item interaction
        if not enemy and current_room.item:
            print(f"You found a {current_room.item.name}!")
            player.add_to_inventory(current_room.item)
            current_room.item = None

        while True:  # Main action loop
            print("\nActions:")
            print("1. Move")
            print("2. Inventory")
            print("3. Search")
            print("4. Interact with NPCs")
            print("5. Quit")

            choice = input("Enter your choice: ")

            if choice == '1':
                directions = input("Which directions? (north/south/east/west, separated by spaces): ").lower()
                dungeon_map.move(directions)

                # Display available directions after moving
                current_room = dungeon_map.current_room  # Update current room after moving
                available_directions = ", ".join(current_room.connections.keys())
                print(f"\nYou are now in the {current_room.name}. {current_room.description}")
                print(f"You can move in the following directions: {available_directions}")

                break  # Exit the action loop after moving

            elif choice == '2':
                player.display_inventory()

                while True:  # Loop for inventory actions
                    inv_action = input("Do you want to (equip weapon/equip armor/drop/view equipped/back): ").lower()
                    if inv_action == "equip weapon":
                        if not any(isinstance(item, Weapon) for item in player.inventory):
                            print("You don't have any weapons in your inventory.")
                            continue

                        print("Available weapons:")
                        for i, item in enumerate(player.inventory):
                            if isinstance(item, Weapon):
                                print(f"{i+1}. {item.name}")

                        choice = int(input("Enter the number of the weapon to equip: ")) - 1
                        if 0 <= choice < len(player.inventory) and isinstance(player.inventory[choice], Weapon):
                            player.equip_weapon(player.inventory[choice])
                        else:
                            print("Invalid choice.")
                    elif inv_action == "equip armor":
                        if not any(isinstance(item, Armor) for item in player.inventory):
                            print("You don't have any armor in your inventory.")
                            continue

                        print("Available armor:")
                        for i, item in enumerate(player.inventory):
                            if isinstance(item, Armor):
                                print(f"{i+1}. {item.name}")

                        choice = int(input("Enter the number of the armor to equip: ")) - 1
                        if 0 <= choice < len(player.inventory) and isinstance(player.inventory[choice], Armor):
                            player.equip_armor(player.inventory[choice])
                        else:
                            print("Invalid choice.")
                    elif inv_action == "drop":
                        if not player.inventory:
                            print("Your inventory is empty.")
                            continue

                        print("Available items:")
                        for i, item in enumerate(player.inventory):
                            print(f"{i+1}. {item.name}")

                        choice = int(input("Enter the number of the item to drop: ")) - 1
                        if 0 <= choice < len(player.inventory):
                            dropped_item = player.inventory.pop(choice)
                            print(f"You dropped {dropped_item.name}.")
                        else:
                            print("Invalid choice.")
                    elif inv_action == "view equipped":
                        player.display_equipment()
                    elif inv_action == "back":
                        break
                    else:
                        print("Invalid action.")

            elif choice == '3':
                if not current_room.searched:
                    if random.random() < 0.2:  # 20% chance to find a hidden item
                        hidden_item = random.choice(list(game_weapons.values()) + list(game_armor.values()))
                        item_type = Weapon if "damage" in hidden_item else Armor
                        print(f"You found a hidden {hidden_item['name']}!")
                        player.add_to_inventory(item_type(**hidden_item))  
                    else:
                        print("You didn't find anything.")
                    current_room.searched = True
                else:
                    print("You have already searched this room.")
            elif choice == '4':
                if current_room.npcs:
                    print("NPCs in this room:")
                    for npc in current_room.npcs:
                        print(f"- {npc}")

                    while True:  # Loop for NPC interaction
                        npc_to_interact = input("Who do you want to interact with? (or type 'back' to cancel): ")
                        if npc_to_interact.lower() == "back":
                            break
                        elif npc_to_interact in current_room.npcs:
                            if npc_to_interact == "Bartender":
                                print("The bartender offers you a drink. (Accept/Decline)")
                                choice = input("> ").lower()
                                if choice == "accept":
                                    print("You feel refreshed.")
                                    player.heal(10)
                                else:
                                    print("You politely decline.")
                            elif npc_to_interact == "Merchant":
                                print("The merchant shows you their wares. (Buy/Sell/Back)")
                                choice = input("> ").lower()
                                if choice == "buy":
                                    # Implement buying logic here (not shown in this example)
                                    pass
                                elif choice == "sell":
                                    # Implement selling logic here (not shown in this example)
                                    pass
                            elif npc_to_interact == "Blacksmith":
                                print("The blacksmith offers to repair or upgrade your equipment. (Repair/Upgrade/Back)")
                                choice = input("> ").lower()
                                if choice == "repair":
                                    # Implement repair logic here (not shown in this example)
                                    pass
                                elif choice == "upgrade":
                                    # Implement upgrade logic here (not shown in this example)
                                    pass
                            # ... (Add interactions for other NPCs)
                        else:
                            print("That NPC is not here.")
                else:
                    print("There are no NPCs in this room.")

            elif choice == '5':
                print("Thanks for playing!")
                return  # Exit the main game loop

            else:
                print("Invalid action.")

    if player.health <= 0:
        print("You have been defeated. Game over.")


if __name__ == "__main__":
    main()
