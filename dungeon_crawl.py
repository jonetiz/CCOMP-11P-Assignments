# Dungeon Crawl
# Written by Jon Etiz
# Created on 22SEP2022

# MIDTERM OBJECTIVE: Procedurally Generated Rogue-lite Dungeon Crawler

from operator import invert
from subprocess import STARTF_USESTDHANDLES
from etizmodules import input_int # used to get and validate integer inputs
from dataclasses import dataclass # used to reduce boilerplate code
from random import randint, choice # random stuff
from os import system # used for controlling stdout
from itertools import zip_longest # used for extended zip() behavior

ROOM_NAMES = [ # A list of strings to be used as room names; move this out of file when
    "Hallway",
    "Armory",
    "Jail",
    "Quarters",
    "Library",
    "Forge",
    "Storeroom",
    "Chapel",
    "Shrine",
    "Kitchen",
    "Laboratory",
    "Study",
    "Latrine",
    "Barracks",
    "Pantry",
    "Office",
    "Empty Room",
    "Condemned Room"
] 

DUNGEON_NAMES = [ # similar to above, but for dungeon names
    "Ancient Ruins",
    "Fortress"
]

ENEMY_NAMES = [ # possible enemy names
    "Soldier"
]

# Base class for entities
@dataclass
class Entity:
    name: str # Entity Name

# Data class for CharacterStatistics, things such as HP, Armor, Mana, and Stamina
@dataclass
class CharacterStatistics:
    hp: int
    mana: int
    armor: int
    stamina: int
    def __repr__(self):
        return f"{self.hp} HP, {self.mana} Mana, {self.armor} Armor, {self.stamina} Stamina"

@dataclass
class Effect:
    # Name of the Effect
    name: str

    # The current duration
    duration = 0

    # How many turns the Effect lasts
    total_duration: int

    # The actual effects of the Effect on the CharacterStatistics
    effect_per_turn: CharacterStatistics

    def __repr__(self):
        effects = ""
        turns_remaining = f"{self.total_duration - self.duration} turns remaining" 
        for name, value in self.effect_per_turn.__dict__.items():
            if value != 0:
                effects += f"{'+' if value > 0 else '-'}{abs(value)} {name}, "
        return f"{self.name} ({effects + turns_remaining})"

    # Called every turn, does the effect of the Effect
    def do_effect(self, instigator):
        # Increment duration by one
        self.duration += 1

        # For each attribute of effect_per_turn of Effect, apply it to the instigator's stats
        for attr, value in self.effect_per_turn.__dict__.items():
            # Set instigator.stats.(attr) to instigator.stats.(attr) + value
            setattr(instigator.stats, attr, getattr(instigator.stats, attr) + value)

        # If this was the last turn of the effect, remove it from active effects
        if self.duration >= self.total_duration:
            instigator.active_effects.remove(self)

# Base class for items
@dataclass
class Item(Entity):
    # The weight of the item
    weight: int
    def action(self, instigator, target):
        pass

# Base class for characters
@dataclass
class Character(Entity):
    equipped: Item # Currently equipped item (typically weapon); should be reference to an item in inventory
    inventory: list[Item] # All of the character's items, including equipped.
    stats: CharacterStatistics # Character's stats
    active_effects: list[Effect] = None # List of active effects, default none
    alive: bool = True
    current_room: object = None # The character's current room

    def __repr__(self):
        return f"{self.name}; {self.stats}"

    # Run every turn of combat to do effects and check self.alive
    def tick(self):
        if self.active_effects:
            for effect in self.active_effects:
                effect.do_effect(self)
        if self.stats.hp <= 0:
            self.alive = False

    # Simple check if this Character has an effect; returns the Effect object or False if it's not found.
    def has_effect(self, effect_name):
        for effect in self.active_effects:
            if effect.name == effect_name:
                return effect
        return False

    # Attack with weapon
    def attack(self):
        target = self.get_target() # get a target
        self.equipped.action(self, target) # attack the target
    
    # Get a target; automatically selects the target with lowest health, or a specific target.
    def get_target(self, take_input = False):
        """Returns the Character object of the next available target; if self is the player character, it will prompt user for input. No input does auto-target."""
        if take_input:
            # Get input from user for which target to use // not implemented yet
            pass
        else:
            chars = self.current_room.characters.copy()
            if self in chars:
                chars.remove(self)
            if chars and len(chars) > 0:
                return chars[0]
            # Return the first available target
    
    def equip_weapon(self, weapon): # equip an item
        self.equipped = weapon

    def use_consumable(self, consumable): # use a consumable
        consumable.action(self)
        self.inventory.remove(consumable)

    def drop_item(self, item): # drop an item; remove from inventory and put in the room inventory
        if self.current_room.items:
            self.current_room.items.append(item)
        else:
            self.current_room.items = [item]
        self.inventory.remove(item)
        if self.equipped == item:
            self.equipped = None
    
    def pickup_item(self, item): # pick up an item; remove from room inventory and add to character inventory
        self.current_room.items.remove(item)
        self.inventory.append(item)

# Item that modifies an instigator's CharacterStatistics
@dataclass
class Consumable(Item):
    # CharacterStatistics, representing the effect (ie. -10 HP, +50 mana)
    affected_stats: CharacterStatistics = None
    # The effects this applies on the instigator
    applied_effects: list[Effect] = None

    def __repr__(self):
        stats_affected = ""
        effects = ""
        if self.affected_stats:
            for name, value in self.affected_stats.__dict__.items():
                if value != 0:
                    stats_affected += f"{'+' if value > 0 else '-'}{abs(value)} {name}, "
        
        if self.applied_effects:
            for name, value in self.applied_effects.__dict__.items():
                if value != 0:
                    effects += f"{'+' if value > 0 else '-'}{abs(value)} {name}, "

        return f"{self.name} {stats_affected}{' ' if stats_affected != '' else ''}{effects}"

    # Use this consumable
    def action(self, instigator: Character):

        # For each attribute of affected_stats of Consumable, apply it to the instigator's stats
        for attr, value in self.affected_stats.__dict__.items():
            # Set instigator.stats.(attr) to instigator.stats.(attr) + value
            setattr(instigator.stats, attr, getattr(instigator.stats, attr) + value)

        # For each of the effects, if there are any effects
        if self.applied_effects:
            for effect in self.applied_effects:
                # Add the effect to the character
                cur_effect = instigator.has_effect(effect.name)
                # If the character already has the effect, reset duration, else add the new effect.
                if cur_effect:
                    cur_effect.duration = 0
                else:
                    instigator.active_effects.append(effect)

@dataclass
class Weapon(Item):
    # The damage applied by the weapon
    attack_damage: int

    # CharacterStatistics, representing what is needed (ie. needs 30 mana)
    required_stats: CharacterStatistics

    # An optional list of effects that are applied to the target 
    applied_effects: list[Effect] = None

    def __repr__(self):
        stats_required = ""
        for name, value in self.required_stats.__dict__.items():
            if value != 0:
                stats_required += f"{value} {name}, "
        
        if stats_required != "":
            stats_required = f", requires {stats_required}per attack."

        return f"{self.name}, {self.attack_damage} DPT{stats_required}"

    # Attack using this weapon
    def action(self, instigator: Character, target: Character):
        # if target is valid
        if target:
            # if the instigator is able to use this weapon
            if self.can_attack(instigator):
                # set target hp
                target.stats.hp -= self.attack_damage
                if target.stats.hp <= 0:
                    target.alive = False # set alive to false if they should be dead
                # if there are any effects with this weapon, set them on the target
                if self.applied_effects:
                    for effect in self.applied_effects:
                        cur_effect = target.has_effect(effect.name)
                        # Only add the effect if the target doesn't have it, else reset duration
                        if cur_effect:
                            cur_effect.duration = 0
                        else:
                            target.active_effects.append(effect)
                return True # return true if the attack is successful
        return False # return false if the attack cannot proceed

    # check if instigator is eligible to use this weapon
    def can_attack(self, instigator: Character):
        stats = instigator.stats
        # if there are any required stats
        if self.required_stats:
            # foreach of the required stats
            for n1, v1 in self.required_stats.__dict__.items():
                # for each of the instigator's stats
                for n2, v2 in stats.__dict__.items():
                    # if the stat matches and the required value is greater than instigator's value, do not allow attack
                    if n1 == n2 and v1 > v2:
                        return False
            return True # else return true

# Class for control-flow of gameplay; holds a text variable and options as Entities with methods for displaying the options
@dataclass
class ActionMenu:
    text: str
    options: list

    def display_menu(self):
        system('cls') # clear console
        print(f"{self.text}") # print the menu title/header text
        out = ""
        # print up to four options per line
        for i, j, k, l, m in zip_longest(range(len(self.options)), self.options[0::4], self.options[1::4], self.options[2::4], self.options[3::4]):
            i *= 4
            if j:
                out += f"\n[{i+1}] {j.name}".ljust(20)
            if k:
                out += f"[{i+2}] {k.name}".ljust(20)
            if l:
                out += f"[{i+3}] {l.name}".ljust(20)
            if m:
                out += f"[{i+4}] {m.name}".ljust(20)
        print(f"{out}")
        selected_num = input_int("Select option from above:", 1, len(self.options)) # get an input from user
        try:
            selection = self.options[selected_num - 1] # try to see if selection is valid
        except: # input_int has error checking, but just in case something weird happens, don't let any out of range get through the cracks
            print(f"{selected_num} is out of range!")
            return self.options[0]
        else: # assuming selection is valid, return the selected option
            return selection

@dataclass
class Room:
    name: str # the name of the room
    position: list[list] # a (x, y) representation of the room's position to ensure no overlap
    characters: list[Character] = None # list of characters in the room
    items: list[Item] = None # a list of items in the room
    connections: list = None # list of connected rooms

class Dungeon:
    name: str # name of the dungeon
    rooms: list[Room] = [] # list of rooms in the dungeon
    def __init__(self, name, player_character, dungeon_size: int):
        self.name = name # todo: randomize
        dungeon_entrance = Room("Entry Hall", [0, 0], [player_character]) # generate a room for the dungeon entrance; should always be the northmost as y = -1 will kick to main menu
        self.rooms.append(dungeon_entrance) # place dungeon_entrance in the list of rooms
        
        used_positions = [] # list of positions that have been used by the dungeon generator
        used_positions.append(dungeon_entrance.position) # append the entrance coordinates to used_positions

        for i in range(dungeon_size): # generate i number of rooms, where i is the dungeon_size
            position = choice(used_positions).copy() # get position of a random room and use it to generate this room

            while position in used_positions: # keep trying to generate a unique position
                if position[1] <= 1: # ensure the room won't be y=0, only entry hall should be (y=-1 will exit dungeon)
                    position[1] += 1
                elif randint(0, 1): # 50/50 chance of x OR y being changed
                    if randint(0, 1): # 50/50 chance of x being incremented or decremented
                        position[0] += 1
                    else:
                        position[0] -= 1
                else: # if we don't change x, we need to change y so rooms don't overlap
                    if randint(0, 1): # 50/50 chance of y being incremented or decremented
                        position[1] += 1
                    else:
                        position[1] -= 1

            used_positions.append(position) # once we got out of the loop above, we must have a valid unused position, so now add this to the used_positions list

            room = Room(choice(ROOM_NAMES), position) # create the room with a random name and the position generated above
            
            characters_in_room = [] # generate random characters in the room
            if randint(0, 1): # 50/50 chance of a random enemy with random weapon being generated (need to flesh out for midterm)
                sword = Weapon("Ramshackle Sword", 5, 10, CharacterStatistics(0, 0, 0, 10)) # create a weapon
                char = Character(choice(ENEMY_NAMES), sword, [sword], CharacterStatistics(50, 0, 0, 100), current_room = room) # create character with random name and stuff
                characters_in_room.append(char) # add this character to characters_in_room

            room.characters = characters_in_room # set the room's characters to characters_in_room

            self.rooms.append(room) # append this room to the dungeon's rooms

        # set connections to other rooms
        for i in self.rooms: # for each room
            if i.connections: # if the room has connections, set con to the list of connections
                con = i.connections
            else: # else create a new list
                con = []

            for j in self.rooms: # for each room
                if j is not i: # only try to make connections on different rooms to prevent recursion; if this room is not the room we're trying to connect
                    if abs(i.position[0] - j.position[0]) <= 1 or abs(i.position[1] - j.position[1]) <= 1: # if the position's x OR y are within 1 value, it's eligible for connection
                        if con: # if there are connections, run a random check to see if a connection should be made
                            if randint(0, 1): # 50/50 chance of connection being made
                                con.append(j)
                        else: # if there are no connections, force the append so there's no chance of the room being detached
                            con.append(j)
            i.connections = con # save the original room's connections with the new connections made

# class for MenuOptions of ActionMenu; these are items that can be put in the Menu that will execute a function (do_action)
@dataclass
class MenuOption(Entity):
    do_action: any # the function to be executed when this option is selected
    def action(self, *args): # run the action with any potentially passed arguments
        self.do_action(*args)

# game object used to keep track of important things and so we dont need global variables
@dataclass
class Game:
    main_character: Character = None # the main character object
    current_dungeon: Dungeon = None # the current dungeon
    current_room: Room = None
    game_state: int = 0 # 0 = main menu, 1 = out of combat, 2 = in combat
    combat_log: str = "" # A string used to save combat log stuff in the text when console is cls'd

    def status_string(self):
        """Returns a string in following format: RoomName | CharacterName, Level 1 | 100 HP, 100 Mana, 25 Armor, 100 Stamina"""
        return f"{self.current_room.name} | {self.main_character.name}, Level 1 | {self.main_character.stats}\n{self.combat_log}" # todo: implement character levels

    def generate_dungeon(self): # generate the dungeon
        char_name = input("What is your name? ") # ask user for character name
        default_weapon = Weapon("Basic Sword", 10, 25, CharacterStatistics(0, 0, 0, 10)) # default weapon
        default_inventory = [default_weapon, Consumable("Basic Potion", 2, CharacterStatistics(50, 0, 0, 0)), Consumable("Basic Potion", 2, CharacterStatistics(50, 0, 0, 0))] # default inventory is weapon and 2 potions
        self.main_character = Character(char_name, default_inventory[0], default_inventory, CharacterStatistics(100, 100, 25, 100)) # create main character object
        dungeon = Dungeon(choice(DUNGEON_NAMES), self.main_character, 5) # generate the dungeon
        self.current_dungeon = dungeon # set the current dungeon
        self.game_state = 1 # set gameplay mode thing
        self.current_room = dungeon.rooms[0] # set current room to the Entry Hall
        self.main_character.current_room = self.current_room # set main character's current room to the current room (Entry Hall)

    def room_has_enemies(self, room: Room):
        """Returns True if the room has characters other than the main character, else will return False"""
        if room.characters:
            chars = room.characters.copy()
        else:
            return False
        if self.main_character in chars:
            chars.remove(self.main_character)
        if chars and len(chars) > 0:
            return True

        return False

    def travel(self):
        """Travel menu and functionality"""
        self.combat_log = "" # blank out combat_log
        menu = ActionMenu(f"{self.status_string()}\nYou see the following rooms to travel into.", self.current_room.connections + [MenuOption("Go Back", print)])
        option = menu.display_menu()
        if isinstance(option, MenuOption): # if the option is a MenuOption and not a Room, go back
            return
        if self.current_room.characters: # remove main character from original room
            self.current_room.characters.remove(self.main_character)

        self.current_room = option # set current room to the selected room
        if self.current_room.characters: # add main character to selected room's characters
            self.current_room.characters.append(self.main_character)
        else:
            self.current_room.characters = [self.main_character]
        self.main_character.current_room = self.current_room

        if self.room_has_enemies(self.current_room): # if the new room has enemies, go into combat
            self.game_state = 2

    def inventory(self):
        """Inventory menu and functionality"""
        self.combat_log = "" # blank out combat_log
        headerstr = f"{self.status_string()}\nCurrently equipped: {self.main_character.equipped}\n" # print the currently equipped item
        menu = ActionMenu(f"{headerstr}You have the following items in your inventory.", self.main_character.inventory + [MenuOption("Go Back", print)])
        item = menu.display_menu()
        if isinstance(item, MenuOption): # if the option is a MenuOption and not a Item, go back
            return
        iactions = []
        if isinstance(item, Weapon): # if the selected object is a Weapon, allow Equip, Drop, or Go Back
            iactions = [
                MenuOption("Equip", self.main_character.equip_weapon),
                MenuOption("Drop", self.main_character.drop_item),
                MenuOption("Go Back", print)
            ]
        elif isinstance(item, Consumable): # if the selected object is a Consumable, allow Use, Drop, or Go Back
            iactions = [
                MenuOption("Use", self.main_character.use_consumable),
                MenuOption("Drop", self.main_character.drop_item),
                MenuOption("Go Back", print)
            ]
        imenu = ActionMenu(f"{headerstr}Selected item: {item}", iactions) # show menu for selected item
        iaction = imenu.display_menu()
        iaction.action(item) # run selected item option when selected

    def search_room(self):
        """Loot from the room; open's room's inventory essentially same as inventory() method"""
        self.combat_log = ""
        searching = True
        while searching:
            if self.current_room.items:
                menu = ActionMenu(f"{self.status_string()}\nYou find the following items in the room.", self.current_room.items + [MenuOption("Go Back", print)])
                item = menu.display_menu()
                if isinstance(item, MenuOption):
                    return
                imenu = ActionMenu(f"{self.status_string()}\nSelected item: {item}", 
                    [
                    MenuOption("Pick Up", self.main_character.pickup_item),
                    MenuOption("Go Back", print)
                    ]
                )
                iaction = imenu.display_menu()
                if isinstance(item, MenuOption):
                    continue
                iaction.action(item)
            else:
                menu = ActionMenu(f"{self.status_string()}\nYou found nothing in the room.", [MenuOption("Go Back", print)])
                item = menu.display_menu()
                if isinstance(item, MenuOption):
                    return

    def combat_method(self):
        """Run all combat functionality and ticks. Each call represents one turn. Main character always goes first"""
        self.main_character.attack() # MC attack
        self.main_character.tick() # MC tick
        for character in self.current_room.characters: # foreach character in the room
            if character.alive and character is not self.main_character: # if it's not MC and it's alive, attack and tick
                character.attack()
                character.tick()
            if not character.alive: # if it's dead or just died, drop its items into the room and remove from room. also add to combat log that user defeated this character
                for item in character.inventory:
                    character.drop_item(item)
                self.current_room.characters.remove(character)
                self.combat_log = f"You have defeated a {character.name}."

# main function 
def main():
    game = Game() # new game object
    while True: # main loop
        if game.game_state == 0: # If user is in main menu
            main_menu = ActionMenu("Main Menu", [
                MenuOption("Begin Game", game.generate_dungeon),
                MenuOption("Quit", quit)
            ]
            )
            option = main_menu.display_menu()
            option.action()
        if game.game_state == 1: # If user is out of combat
            action_menu = ActionMenu(f"{game.status_string()}", [
                MenuOption("Travel", game.travel),
                MenuOption("Inventory", game.inventory),
                MenuOption("Search Room", game.search_room)
            ]
            )
            option = action_menu.display_menu()
            option.action()
        if game.game_state == 2: # If user is in combat
            game.combat_log = f"You are in combat with a {game.main_character.get_target()}"
            combat_menu = ActionMenu(f"{game.status_string()}", [
                MenuOption("Attack", game.combat_method)
            ]
            )
            option = combat_menu.display_menu()
            option.action()
            if not game.room_has_enemies(game.current_room): # if there are no enemies in the room, add to combat log that we're no longer in combat and set game.game_state = 1
                game.combat_log += "\nYou are no longer in combat."
                game.game_state = 1
            if not game.main_character.alive: # if MC dies, tell them they suck and quit program
                print("You have perished.")
                quit()

# PEP 299 Adherence; if this is imported for whatever reason main() will not run
if __name__ == "__main__":
    main()