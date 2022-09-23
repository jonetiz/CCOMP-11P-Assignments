# Dungeon Crawl
# Written by Jon Etiz
# Created on 22SEP2022

# KEY OBJECTIVE: Procedurally Generated Rogue-lite Dungeon Crawler

from dataclasses import dataclass
from random import randrange

# Base class for entities
@dataclass
class Entity:
    name: str

# Data class for CharacterStatistics, things such as HP, Armor, Mana, and Stamina
@dataclass
class CharacterStatistics:
    hp: int
    mana: int
    armor: int
    stamina: int

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
    equipped: Item
    inventory: list[Item]
    stats: CharacterStatistics
    active_effects: list[Effect]

    def tick(self):
        for effect in self.active_effects:
            effect.do_effect(self)

    # Simple check if this Character has an effect; returns the Effect object or False if it's not found.
    def has_effect(self, effect_name):
        for effect in self.active_effects:
            if effect.name == effect_name:
                return effect
        return False

    # Generic use the currently equipped item (use consumable or attack with weapon)
    def use(self):
        # If the equipped item is a weapon, get a target and pass, else just use the consumable.
        if isinstance(self.equipped, Weapon):
            self.get_target()
            self.equipped.action(self, target)
        else:
            self.equipped.action(self)
    
    # Get a target; automatically selects the target with lowest health, or a specific target.
    def get_target(self, take_input = False):
        """Returns the Character object of the next available target; if self is the player character, it will prompt user for input. No input does auto-target."""
        if take_input:
            # Get input from user for tager
        else:
            # Return the first available target

# Item that modifies an instigator's CharacterStatistics
@dataclass
class Consumable(Item):
    # CharacterStatistics, representing the effect (ie. -10 HP, +50 mana)
    affected_stats: CharacterStatistics
    # The effects this applies on the instigator
    effects: list[Effect]
    # Use this consumable
    def action(self, instigator: Character):

        # For each attribute of affected_stats of Consumable, apply it to the instigator's stats
        for attr, value in self.affected_stats.__dict__.items():
            # Set instigator.stats.(attr) to instigator.stats.(attr) + value
            setattr(instigator.stats, attr, getattr(instigator.stats, attr) + value)

        # For each of the effects, if there are any effects
        if len(self.effects) > 0:
            for effect in self.effects:
                # Add the effect to the character
                cur_effect = instigator.has_effect(effect.name)
                # If the character already has the effect, reset duration, else add the new effect.
                if cur_effect:
                    cur_effect.duration = 0
                else:
                    instigator.active_effects.append(effect)


@dataclass
class Weapon(Item):
    # CharacterStatistics, representing what is needed (ie. needs 30 mana)
    required_stats: CharacterStatistics

    # A list of effects that are applied to the target 
    applied_effects: list[Effect]

    # Attack using this weapon
    def action(self, instigator: Character, target: Character):
        if self.can_attack(instigator):
            target.stats.hp -= self.effective_value()
            for effect in self.applied_effects:
                cur_effect = target.has_effect(effect.name)
                # Only add the effect if the target doesn't have it, else reset duration
                if cur_effect:
                    cur_effect.duration = 0
                else:
                    target.active_effects.append(effect)
            return True
        else:
            return False

    def can_attack(self, instigator: Character):
        stats = instigator.stats
        if len(self.required_stats) > 0:
            for required_stat in self.required_stats:
                for stat in stats:
                    if required_stat.name == stat.name and required_stat.value < stat.value:
                        return False
                


def main():
    # generate_dungeon
    # do stuff
    test_effect = Effect("Test Effect", 5, CharacterStatistics(10, -10, 0, 0))
    test_consumable = Consumable("Test Potion", 5, CharacterStatistics(1000, 0, 0, -50), [test_effect])
    test_char = Character("Jon", None, None, CharacterStatistics(500, 500, 250, 100), [])
    print(test_char)
    test_consumable.action(test_char)
    print(test_char)
    while True:
        asd = input("Test?\n")
        if asd == "y":
            test_char.tick()
            print(test_char)
        if asd == "n":
            test_consumable.action(test_char)
            test_char.tick()
            print(test_char)

# PEP 299 Adherence
if __name__ == "__main__":
    main()