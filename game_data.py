"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    try:
        with open(filename, 'r', encoding ='utf-8-') as f:
            content = f.read()
    except FileNotFoundError:
        raise MissingDataFileError(f"Quest file not found: {filename}")
    except UnicodeDecodeError as e:
        raise CorruptedDataError(f"Quest file encoding error: {e}")
    except OSError as e:
        raise CorruptedDataError(f"Quest file unreadable: {e}")
        
    blocks = _split_blocks(content)
    quests = {}

    try:
        for block in blocks:
            quest = parse_quest_block(block)
            validate_quest_data(quest)
            qid = quest["quest_id"]
            if qid in quests:
                raise InvalidDataFormatError(f"Duplicate quest_id: {qid}")
            quests[qid] = quest
    except InvalidDataFormatError:
        # re-raise as is for clarity
        raise
    except Exception as e:
        # Any unexpected parsing issues are considered corruption
        raise CorruptedDataError(f"Failed to parse quests: {e}")

    return quests

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        raise MissingDataFileError(f"Item file not found: {filename}")
    except UnicodeDecodeError as e:
        raise CorruptedDataError(f"Item file encoding error: {e}")
    except OSError as e:
        raise CorruptedDataError(f"Item file unreadable: {e}")

    blocks = _split_blocks(content)
    items = {}

    try:
        for block in blocks:
            item = parse_item_block(block)
            validate_item_data(item)
            iid = item["item_id"]
            if iid in items:
                raise InvalidDataFormatError(f"Duplicate item_id: {iid}")
            items[iid] = item
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Failed to parse items: {e}")

    return items

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    required = {"quest_id", "title", "description","reward_xp", "reward_gold", "required_level", "prerequisite"}
    missing = required - set(quest_dict.keys())
    if missing:
        raise InvalidDataFormatError(f"Quest missing fields: {sorted(missing)}")

    # Numeric validations
    for key in ("reward_xp", "reward_gold", "required_level"):
        val = quest_dict.get(key)
        if not isinstance(val, int):
            raise InvalidDataFormatError(f"Quest field '{key}' must be an integer, got {type(val).__name__}")

    # prerequisite can be None or string
    prereq = quest_dict.get("prerequisite")
    if not (prereq is None or isinstance(prereq, str)):
        raise InvalidDataFormatError("Quest field 'prerequisite' must be a string or None")

    return True

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    required = {"item_id", "name", "type", "effect", "cost", "description"}
    missing = required - set(item_dict.keys())
    if missing:
        raise InvalidDataFormatError(f"Item missing fields: {sorted(missing)}")

    typ = item_dict.get("type")
    if typ not in {"weapon", "armor", "consumable"}:
        raise InvalidDataFormatError(f"Invalid item type: {typ}")

    cost = item_dict.get("cost")
    if not isinstance(cost, int):
        raise InvalidDataFormatError("Item field 'cost' must be an integer")

    # effect must be dict with a single stat:value int
    effect = item_dict.get("effect")
    if not isinstance(effect, dict) or len(effect) != 1:
        raise InvalidDataFormatError("Item 'effect' must be a single-key dict like {'strength': 5}")
    stat, value = next(iter(effect.items()))
    if not isinstance(stat, str) or not stat:
        raise InvalidDataFormatError("Item effect stat name must be a non-empty string")
    if not isinstance(value, int):
        raise InvalidDataFormatError("Item effect value must be an integer")

    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
     data_dir = os.path.join(os.path.dirname(__file__), "data")
    quests_path = os.path.join(data_dir, "quests.txt")
    items_path = os.path.join(data_dir, "items.txt")

    try:
        os.makedirs(data_dir, exist_ok=True)
    except OSError as e:
        raise CorruptedDataError(f"Failed to create data directory: {e}")

    # Default quests
    if not os.path.isfile(quests_path):
        default_quests = (
            "QUEST_ID: goblin_hunt\n"
            "TITLE: Goblin Hunt\n"
            "DESCRIPTION: Clear the nearby cave of goblins.\n"
            "REWARD_XP: 100\n"
            "REWARD_GOLD: 50\n"
            "REQUIRED_LEVEL: 1\n"
            "PREREQUISITE: NONE\n"
            "\n"
            "QUEST_ID: orc_camp\n"
            "TITLE: Orc Camp\n"
            "DESCRIPTION: Drive back the orcs raiding local farms.\n"
            "REWARD_XP: 200\n"
            "REWARD_GOLD: 100\n"
            "REQUIRED_LEVEL: 2\n"
            "PREREQUISITE: goblin_hunt\n"
        )
        try:
            with open(quests_path, "w", encoding="utf-8") as f:
                f.write(default_quests)
        except OSError as e:
            raise CorruptedDataError(f"Failed to write default quests: {e}")

    # Default items
    if not os.path.isfile(items_path):
        default_items = (
            "ITEM_ID: w_rusty_sword\n"
            "NAME: Rusty Sword\n"
            "TYPE: weapon\n"
            "EFFECT: strength:3\n"
            "COST: 10\n"
            "DESCRIPTION: An old sword with a dull edge.\n"
            "\n"
            "ITEM_ID: a_leather_armor\n"
            "NAME: Leather Armor\n"
            "TYPE: armor\n"
            "EFFECT: health:5\n"
            "COST: 12\n"
            "DESCRIPTION: Basic protection made from tanned hide.\n"
            "\n"
            "ITEM_ID: c_small_potion\n"
            "NAME: Small Potion\n"
            "TYPE: consumable\n"
            "EFFECT: health:20\n"
            "COST: 5\n"
            "DESCRIPTION: Restores a small amount of health.\n"
        )
        try:
            with open(items_path, "w", encoding="utf-8") as f:
                f.write(default_items)
        except OSError as e:
            raise CorruptedDataError(f"Failed to write default items: {e}")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    data = {}
    for raw in lines:
        if ": " not in raw:
            raise InvalidDataFormatError(f"Malformed quest line (missing ': '): {raw}")
        key, val = raw.split(": ", 1)
        key = key.strip().upper()
        val = val.strip()
        data[key] = val

    required_keys = {"QUEST_ID", "TITLE", "DESCRIPTION","REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL", "PREREQUISITE"}
    missing = required_keys - set(data.keys())
    if missing:
        raise InvalidDataFormatError(f"Quest block missing keys: {sorted(missing)}")

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    data = {}
    for raw in lines:
        if ": " not in raw:
            raise InvalidDataFormatError(f"Malformed item line (missing ': '): {raw}")
        key, val = raw.split(": ", 1)
        key = key.strip().upper()
        val = val.strip()
        data[key] = val

    required_keys = {"ITEM_ID", "NAME", "TYPE", "EFFECT", "COST", "DESCRIPTION"}
    missing = required_keys - set(data.keys())
    if missing:
        raise InvalidDataFormatError(f"Item block missing keys: {sorted(missing)}")

    # Parse EFFECT: "stat_name:value"
    effect_raw = data["EFFECT"]
    if ":" not in effect_raw:
        raise InvalidDataFormatError("Item EFFECT must be 'stat:value'")
    stat, val = effect_raw.split(":", 1)
    stat = stat.strip()
    val = val.strip()
    try:
        effect_val = _to_int(val, "EFFECT value")
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise InvalidDataFormatError(f"Item effect conversion failed: {e}")

    try:
        cost = _to_int(data["COST"], "COST")
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise InvalidDataFormatError(f"Item cost conversion failed: {e}")

    item = {"item_id": data["ITEM_ID"],"name": data["NAME"],"type": data["TYPE"].lower(),"effect": {stat: effect_val},"cost": cost,"description": data["DESCRIPTION"],}
    return item


def _to_int(raw, field_name):
    """Convert a string to int, raising InvalidDataFormatError on failure."""
    try:
        return int(raw)
    except ValueError:
        raise InvalidDataFormatError(f"Field '{field_name}' must be an integer, got: {raw!r}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    )
    
    # Test creating default files
    try:
        create_default_data_files()
        print("Default data files ensured.")
    except CorruptedDataError as e:
        print("Error creating default files:", e)

    # Test loading quests
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests")
    except MissingDataFileError:
        print("Quest file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid quest format: {e}")
    except CorruptedDataError as e:
        print(f"Corrupted quest file: {e}")
    
    # Test loading items
    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
    except MissingDataFileError:
        print("Item file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid item format: {e}")
    except CorruptedDataError as e:
        print(f"Corrupted item file: {e}")tems)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

