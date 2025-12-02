"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
   character_class = character_class.capitalize()
    valid_classes = ["Warrior", "Mage", "Rogue", "Cleric"]

    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"{character_class} is not a valid class.")

    # Base stats
    if character_class == "Warrior":
        health, strength, magic = 120,15,5
    elif character_class == "Mage":
        health, strength, magic = 80, 8, 20
    elif character_class == "Rogue":
        health, strength, magic = 90, 12, 10
    elif character_class == "Cleric":
        health, strength, magic = 100, 10, 15
    character = {"name": name, "class": character_class, "level": 1, "health": health, "max_health": health, "strength": strength, "magic": magic, "experience": 0, "gold": 100,"inventory": [], "active_quests": [],  "completed_quests": []}

    return character


def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
   if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    filename = os.path.join(save_directory, f"{character['name']}_save.txt")

    try:
        with open(filename, "w") as file:
            file.write(f"NAME: {character['name']}\n")
            file.write(f"CLASS: {character['class']}\n")
            file.write(f"LEVEL: {character['level']}\n")
            file.write(f"HEALTH: {character['health']}\n")
            file.write(f"MAX_HEALTH: {character['max_health']}\n")
            file.write(f"STRENGTH: {character['strength']}\n")
            file.write(f"MAGIC: {character['magic']}\n")
            file.write(f"EXPERIENCE: {character['experience']}\n")
            file.write(f"GOLD: {character['gold']}\n")
            file.write("INV: " + ",".join(character["inventory"]) + "\n")
            file.write("ACTIVE: " + ",".join(character["active_quests"]) + "\n")
            file.write("COMPLETE: " + ",".join(character["completed_quests"]) + "\n")
        return True

    except IOError:
        raise SaveFileCorruptedError("Unable to save file.")

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"{character_name} does not exist.")

    try:
        with open(filename, "r") as file:
            lines = file.readlines()

    except Exception:
        raise SaveFileCorruptedError("Could not read save file.")

    try:
        # Parse each line
        data = {}
        for line in lines:
            key, value = line.strip().split(": ")
            data[key] = value

        # Rebuild character dictionary
        character = {
            "name": data["NAME"],
            "class": data["CLASS"],
            "level": int(data["LEVEL"]),
            "health": int(data["HEALTH"]),
            "max_health": int(data["MAX_HEALTH"]),
            "strength": int(data["STRENGTH"]),
            "magic": int(data["MAGIC"]),
            "experience": int(data["EXPERIENCE"]),
            "gold": int(data["GOLD"]),
            "inventory": data["INV"].split(",") if data["INV"] else [],
            "active_quests": data["ACTIVE"].split(",") if data["ACTIVE"] else [],
            "completed_quests": data["COMPLETE"].split(",") if data["COMPLETE"] else []
        }

        validate_character_data(character)
        return character

    except Exception:
        raise InvalidSaveDataError("Save data format is invalid.")

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
   if not os.path.exists(save_directory):
        return []

    files = os.listdir(save_directory)
    character_names = []

    for f in files:
        if f.endswith("_save.txt"):
            name = f.replace("_save.txt", "")
            character_names.append(name)

    return character_names

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError("Character save file does not exist.")

    os.remove(filename)
    return True
# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    if character["health"] <= 0:
        raise CharacterDeadError("Cannot gain XP when dead.")

    character["experience"] += xp_amount

    # Level up check
    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1

        # Increase stats
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]  # Full restore

    return character

def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
     new_total = character["gold"] + amount
    if new_total < 0:
        raise ValueError("Gold cannot go negative.")

    character["gold"] = new_total
    return character["gold"]

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
     old_health = character["health"]
    new_health = old_health + amount

    if new_health > character["max_health"]:
        new_health = character["max_health"]

    character["health"] = new_health
    return new_health - old_health  # actual healed

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    return character["health"] <= 0

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    if character["health"] > 0:
        return False

    character["health"] = character["max_health"] // 2
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    required = ["name", "class", "level", "health", "max_health","strength", "magic", "experience", "gold","inventory", "active_quests", "completed_quests"]

    for key in required:
        if key not in character:
            raise InvalidSaveDataError(f"Missing field: {key}")

    if type(character["inventory"]) != list:
        raise InvalidSaveDataError("Inventory must be a list.")

    if type(character["active_quests"]) != list:
        raise InvalidSaveDataError("Active quests must be a list.")

    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    try:
        char = create_character("TestHero", "Warrior")
        print(f"Created: {char['name']} the {char['class']}")
        print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    except InvalidCharacterClassError as e:
        print(f"Invalid class: {e}")

    # ----------------------------------------------------
    # Test Saving Character
    # ----------------------------------------------------
    try:
        save_character(char)
        print("Character saved successfully.")
    except Exception as e:
        print(f"Save error: {e}")

    # ----------------------------------------------------
    # Test Loading Character
    # ----------------------------------------------------
    try:
        loaded = load_character("TestHero")
        print(f"Loaded: {loaded['name']}")
        print(f"HP={loaded['health']}  STR={loaded['strength']}  MAG={loaded['magic']}")
    except CharacterNotFoundError:
        print("Character not found.")
    except SaveFileCorruptedError:
        print("Save file corrupted.")
    except InvalidSaveDataError:
        print("Save file data invalid.")

