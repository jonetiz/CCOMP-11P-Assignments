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

# Item that modifies an instigator's CharacterStatistics
@dataclass
class Consumable(Item):
    # CharacterStatistics, representing the effect (ie. -10 HP, +50 mana)
    affected_stats: CharacterStatistics
    # The effects this applies on the instigator
    effects: dict[Effect]
    # Use this consumable
    def action(self, instigator: Character):
        stats = instigator.stats
        # For each of the affected_stats, if there are any affected_stats
        if len(self.affected_stats) > 0:
            for affected_stat in self.affected_stats:
                # For each of the instigator's stats
                for stat in stats:
                    # If the affected_stat matches the instigator's stat
                    if stat.name == affected_stat.name:
                        # Apply the affected_stat's value to the instigator's stat
                        stat.apply(affected_stat.value)

        # For each of the effects, if there are any effects
        if len(self.effects) > 0:
            for effect in self.effects:
                # Add the effect to 
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
    test_char = Character("Jon", None, None, CharacterStatistics(500, 500, 250, 100), [test_effect])
    while True:
        asd = input("Test?\n")
        if asd == "y":
            test_char.tick()
            print(test_char)

# PEP 299 Adherence
if __name__ == "__main__":
    main()