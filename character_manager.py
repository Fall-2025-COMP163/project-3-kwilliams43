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
        with open(filename, "w") as f:
            f.write(f"NAME: {character.get('name','')}\n")
            f.write(f"CLASS: {character.get('class','')}\n")
            f.write(f"LEVEL: {character.get('level',1)}\n")
            f.write(f"HEALTH: {character.get('health',0)}\n")
            f.write(f"MAX_HEALTH: {character.get('max_health',0)}\n")
            f.write(f"STRENGTH: {character.get('strength',0)}\n")
            f.write(f"MAGIC: {character.get('magic',0)}\n")
            f.write(f"EXPERIENCE: {character.get('experience',0)}\n")
            f.write(f"GOLD: {character.get('gold',0)}\n")
            f.write("INV: " + ",".join(character.get("inventory", [])) + "\n")
            f.write("ACTIVE: " + ",".join(character.get("active_quests", [])) + "\n")
            f.write("COMPLETE: " + ",".join(character.get("completed_quests", [])) + "\n")
        return True
    except Exception:
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
        with open(filename, "r") as f:
            lines = [ln.strip() for ln in f.readlines() if ln.strip()]
    except Exception:
        raise SaveFileCorruptedError("Could not read save file.")
    try:
        data = {}
        for line in lines:
            if ": " not in line:
                continue
            k, v = line.split(": ", 1)
            data[k] = v
        character = {
            "name": data.get("NAME", ""),
            "class": data.get("CLASS", ""),
            "level": int(data.get("LEVEL", "1")),
            "health": int(data.get("HEALTH", "0")),
            "max_health": int(data.get("MAX_HEALTH", "0")),
            "strength": int(data.get("STRENGTH", "0")),
            "magic": int(data.get("MAGIC", "0")),
            "experience": int(data.get("EXPERIENCE", "0")),
            "gold": int(data.get("GOLD", "0")),
            "inventory": data.get("INV", "").split(",") if data.get("INV", "") else [],
            "active_quests": data.get("ACTIVE", "").split(",") if data.get("ACTIVE", "") else [],
            "completed_quests": data.get("COMPLETE", "").split(",") if data.get("COMPLETE", "") else []
        }
        validate_character_data(character)
        return character
    except CharacterNotFoundError:
        raise
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
    return [f.replace("_save.txt", "") for f in files if f.endswith("_save.txt")]

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
    if character.get("health", 0) <= 0:
        raise CharacterDeadError("Cannot gain XP when dead.")
    character["experience"] = character.get("experience", 0) + int(xp_amount)
    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1
        character["max_health"] = character.get("max_health", 0) + 10
        character["strength"] = character.get("strength", 0) + 2
        character["magic"] = character.get("magic", 0) + 2
        character["health"] = character["max_health"]
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
     new_total = character.get("gold", 0) + int(amount)
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
     old = character.get("health", 0)
    character["health"] = min(character.get("health", 0) + int(amount), character.get("max_health", 0))
    return character["health"] - old  # actual healed

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    return character.get("health", 0) <= 0

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    if character.get("health", 0) > 0:
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
    required = ["name","class","level","health","max_health","strength","magic","experience","gold","inventory","active_quests","completed_quests"]
    for k in required:
        if k not in character:
            raise InvalidSaveDataError(f"Missing field: {k}")
    if not isinstance(character.get("inventory", []), list):
        raise InvalidSaveDataError("Inventory must be a list.")
    if not isinstance(character.get("active_quests", []), list):
        raise InvalidSaveDataError("Active quests must be a list.")
    if not isinstance(character.get("completed_quests", []), list):
        raise InvalidSaveDataError("Completed quests must be a list.")
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

