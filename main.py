"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    while True:
        print("\n=== MAIN MENU ===")
        print("1) New Game")
        print("2) Load Game")
        print("3) Exit")
        choice = input("Choose an option (1-3): ").strip()
        if choice in ("1", "2", "3"):
            return int(choice)
        print("Invalid. Need to enter 1, 2, or 3.")
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice


def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character

    print("\n=== NEW GAME ===")
    name = input("Enter character name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    print("Choose a class: Warrior, Mage, Rogue, Cleric")
    cls = input("Enter class: ").strip()

    try:
        char = character_manager.create_character(name, cls)
    except InvalidCharacterClassError as e:
        print(f"Invalid class: {e}")
        return

    char.setdefault("equipped_weapon", None)
    char.setdefault("equipped_armor", None)
    char["item_data"] = all_items

    current_character = char

    try:
        character_manager.save_character(current_character)
        print(f"Character '{name}' created and saved.")
    except InvalidCharacterClassError as e:
        print(f"Warning: character was not saved: {e}")

    game_loop()

    
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop



def load_game():
    """
    Load an existing saved game

    Shows list of saved characters
    Prompts user to select one
    """
    global current_character, all_items, all_quests

    print("\n=== LOAD GAME ===")
    saves = character_manager.list_saved_characters()
    if not saves:
        print("No saved characters found.")
        return None

    print("Saved characters:")
    for idx, s in enumerate(saves, start=1):
        print(f"{idx}) {s}")

    while True:
        choice = input(f"Select character (1-{len(saves)}) or 'b' to go back: ").strip()
        if choice.lower() == "b":
            return None
        if not choice.isdigit():
            print("Enter a number.")
            continue

        idx = int(choice)
        if 1 <= idx <= len(saves):
            selected = saves[idx - 1]
            break
        print("Invalid")

    try:
        loaded = character_manager.load_character(selected)
    except CharacterNotFoundError:
        print("Save file not found.")
        return None
    except SaveFileCorruptedError:
        print("Save file corrupted.")
        return None
    except InvalidSaveDataError as e:
        print(f"Invalid save data: {e}")
        return None

    loaded.setdefault("equipped_weapon", None)
    loaded.setdefault("equipped_armor", None)
    loaded["item_data"] = all_items

    current_character = loaded
    print(f"Loaded character: {current_character['name']} (Level {current_character.get('level', 1)})")

    return current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop


# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character

    if current_character is None:
        print("No character loaded.")
        return

    game_running = True

    while game_running:
        try:
            choice = game_menu()
            if choice == 1:
                view_character_stats()
            elif choice == 2:
                view_inventory()
            elif choice == 3:
                quest_menu()
            elif choice == 4:
                explore()
            elif choice == 5:
                shop()
            elif choice == 6:
                save_game()
                print("Game saved. Returning to main menu.")
                game_running = False
            else:
                print("Invalid choice.")
        except CharacterDeadError:
            handle_character_death()
        except Exception as e:
            print(f"An error occurred: {e}")

        try:
            save_game()
        except Exception as e:
            print(f"Warning: failed to auto-save: {e}")

    # Removed stray re-assignment that would re-enable the loop after it ends

    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action


def game_menu():
    """
    Display game menu and get player choice

    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit

    Returns: Integer choice (1-6)
    """
    while True:
        print("\n=== GAME MENU ===")
        print("1) View Character Stats")
        print("2) View Inventory")
        print("3) Quest Menu")
        print("4) Explore (Find Battles)")
        print("5) Shop")
        print("6) Save and Quit")
        choice = input("Choose an option (1-6): ").strip()
        if choice in ("1", "2", "3", "4", "5", "6"):
            return int(choice)
        print("Enter a number between 1 and 6.")
    # TODO: Implement game menu


# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    if not current_character:
        print("No character loaded.")
        return

    c = current_character
    print("\n=== CHARACTER STATS ===")
    print(f"Name: {c.get('name')}")
    print(f"Class: {c.get('class')}")
    print(f"Level: {c.get('level')}")
    print(f"HP: {c.get('health')}/{c.get('max_health')}")
    print(f"Strength: {c.get('strength')}")
    print(f"Magic: {c.get('magic')}")
    print(f"Experience: {c.get('experience')}")
    print(f"Gold: {c.get('gold')}")
    print(f"Equipped Weapon: {c.get('equipped_weapon')}")
    print(f"Equipped Armor: {c.get('equipped_armor')}")
    try:
        quest_handler.display_character_quest_progress(c, all_quests)
    except Exception:
        print(f"Active Quests: {len(c.get('active_quests', []))}")
        print(f"Completed Quests: {len(c.get('completed_quests', []))}")

    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler


def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    if not current_character:
        print("No character loaded.")
        return

    while True:
        print("\n=== INVENTORY MENU ===")
        inventory_system.display_inventory(current_character, all_items)
        print("\nOptions:")
        print("1) Use item")
        print("2) Equip weapon")
        print("3) Equip armor")
        print("4) Drop item")
        print("5) Back")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            item_id = input("Enter item ID to use: ").strip()
            if item_id not in all_items:
                print("Unknown item ID.")
                continue
            try:
                result = inventory_system.use_item(current_character, item_id, all_items[item_id])
                print(result)
            except ItemNotFoundError:
                print("You don't have that item.")
            except InvalidItemTypeError as e:
                print(e)
            except Exception as e:
                print(f"Error using item: {e}")

        elif choice == "2":
            item_id = input("Enter weapon item ID to equip: ").strip()
            if item_id not in all_items:
                print("Unknown item ID.")
                continue
            try:
                result = inventory_system.equip_weapon(current_character, item_id, all_items[item_id])
                print(result)
            except ItemNotFoundError:
                print("You don't have that weapon.")
            except InvalidItemTypeError as e:
                print(e)
            except InventoryFullError as e:
                print(e)
            except Exception as e:
                print(f"Error equipping weapon: {e}")

        elif choice == "3":
            item_id = input("Enter armor item ID to equip: ").strip()
            if item_id not in all_items:
                print("Unknown item ID.")
                continue
            try:
                result = inventory_system.equip_armor(current_character, item_id, all_items[item_id])
                print(result)
            except ItemNotFoundError:
                print("You don't have that armor.")
            except InvalidItemTypeError as e:
                print(e)
            except InventoryFullError as e:
                print(e)
            except Exception as e:
                print(f"Error equipping armor: {e}")

        elif choice == "4":
            item_id = input("Enter item ID to drop: ").strip()
            try:
                inventory_system.remove_item_from_inventory(current_character, item_id)
                print(f"Dropped {item_id}.")
            except ItemNotFoundError:
                print("Item not in inventory.")
            except Exception as e:
                print(f"Error dropping item: {e}")

        elif choice == "5":
            break
        else:
            print("Invalid input. Choose 1-5.")


    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system


def quest_menu():
    """Quest management menu"""
    global current_character, all_quests

    if not current_character:
        print("No character loaded.")
        return

    while True:
        print("\n=== QUEST MENU ===")
        print("1) View Active Quests")
        print("2) View Available Quests")
        print("3) View Completed Quests")
        print("4) Accept Quest")
        print("5) Abandon Quest")
        print("6) Complete Quest (testing)")
        print("7) Back")
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            active = quest_handler.get_active_quests(current_character, all_quests)
            if not active:
                print("No active quests.")
            else:
                quest_handler.display_quest_list(active)

        elif choice == "2":
            available = quest_handler.get_available_quests(current_character, all_quests)
            if not available:
                print("No available quests at this time.")
            else:
                quest_handler.display_quest_list(available)

        elif choice == "3":
            completed = quest_handler.get_completed_quests(current_character, all_quests)
            if not completed:
                print("No completed quests.")
            else:
                quest_handler.display_quest_list(completed)

        elif choice == "4":
            qid = input("Enter quest ID to accept: ").strip()
            try:
                quest_handler.accept_quest(current_character, qid, all_quests)
                print(f"Accepted quest '{qid}'.")
            except QuestNotFoundError:
                print("Quest not found.")
            except InsufficientLevelError as e:
                print(e)
            except QuestRequirementsNotMetError as e:
                print(e)
            except QuestAlreadyCompletedError as e:
                print(e)
            except Exception as e:
                print(f"Error accepting quest: {e}")

        elif choice == "5":
            qid = input("Enter quest ID to abandon: ").strip()
            try:
                quest_handler.abandon_quest(current_character, qid)
                print(f"Abandoned quest '{qid}'.")
            except QuestNotActiveError:
                print("Quest is not active.")
            except Exception as e:
                print(f"Error abandoning quest: {e}")

        elif choice == "6":
            qid = input("Enter quest ID to complete: ").strip()
            try:
                rewards = quest_handler.complete_quest(current_character, qid, all_quests)
                print(f"Quest '{qid}' completed! Gained {rewards['xp']} XP and {rewards['gold']} gold.")
            except QuestNotFoundError:
                print("Quest not found.")
            except QuestNotActiveError:
                print("Quest is not active.")
            except Exception as e:
                print(f"Error completing quest: {e}")

        elif choice == "7":
            break
        else:
            print("Invalid input. Choose 1-7.")


    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler


def explore():
    """Find and fight random enemies"""
    global current_character
    if not current_character:
        print("No character loaded.")
        return

    level = int(current_character.get("level", 1))
    enemy = combat_system.get_random_enemy_for_level(level)
    print(f"You encounter a {enemy['name']}!")

    battle = combat_system.SimpleBattle(current_character, enemy)
    try:
        result = battle.start_battle()
    except CharacterDeadError:
        print("You have been defeated...")
        handle_character_death()
        return
    except Exception as e:
        print(f"Combat error: {e}")
        return

    if result["winner"] == "player":
        print(f"You defeated the {enemy['name']} and gained {result['xp_gained']} XP and {result['gold_gained']} gold.")
    elif result["winner"] == "escaped":
        print("You escaped from battle.")
    else:
        print("You were defeated in battle.")
        handle_character_death()


    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions


def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items

    if not current_character:
        print("No character loaded.")
        return

    while True:
        print("\n=== SHOP ===")
        print(f"Gold: {current_character.get('gold', 0)}")
        print("Available items:")
        ids = list(all_items.keys())
        for idx, iid in enumerate(ids, start=1):
            it = all_items[iid]
            print(f"{idx}) {it['name']} (id: {iid}) - Cost: {it.get('cost', 0)}")

        print("\nOptions:")
        print("1) Buy item")
        print("2) Sell item")
        print("3) Back")
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            sel = input("Enter item id to buy: ").strip()
            if sel not in all_items:
                print("Invalid item id.")
                continue
            try:
                inventory_system.purchase_item(current_character, sel, all_items[sel])
                print(f"Purchased {all_items[sel]['name']}.")
            except InsufficientResourcesError:
                print("Not enough gold.")
            except InventoryFullError:
                print("Inventory is full.")
            except Exception as e:
                print(f"Error purchasing item: {e}")

        elif choice == "2":
            sel = input("Enter item id to sell: ").strip()
            try:
                price = inventory_system.sell_item(current_character, sel, all_items.get(sel, {"cost": 0}))
                print(f"Sold {sel} for {price} gold.")
            except ItemNotFoundError:
                print("You don't have that item.")
            except Exception as e:
                print(f"Error selling item: {e}")

        elif choice == "3":
            break
        else:
            print("Invalid input. Choose 1-3.")


    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character

    if not current_character:
        return

    try:
        character_manager.save_character(current_character)
    except Exception as e:
        print(f"Warning: failed to save game: {e}")


    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions


def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items

    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
        return True  # REQUIRED by autograder
    except MissingDataFileError:
        raise
    except (InvalidDataFormatError, CorruptedDataError):
        raise
    except Exception as e:
        raise InvalidDataFormatError(f"Unexpected error loading data: {e}")

    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()


def handle_character_death():
    """Handle character death"""

    global current_character, game_running

    if not current_character:
        return

    print("\n=== YOU DIED ===")
    revive_cost = 50
    gold = int(current_character.get("gold", 0))
    print(f"You may revive for {revive_cost} gold, or quit to the main menu.")
    while True:
        choice = input("Revive for gold? (y/n): ").strip().lower()
        if choice == "y":
            if gold < revive_cost:
                print("Not enough gold to revive.")
                choice2 = input("Quit to main menu? (y/n): ").strip().lower()
                if choice2 == "y":
                    game_running = False
                    return
                else:
                    return
            else:
                try:
                    current_character["gold"] = gold - revive_cost
                    revived = character_manager.revive_character(current_character)
                    if revived:
                        print("You were revived!")
                        return
                    else:
                        print("Could not revive character.")
                        return
                except Exception as e:
                    print(f"Revive failed: {e}")
                    return
        elif choice == "n":
            print("Returning to main menu.")
            game_running = False
            return
        else:
            print("Answer 'y' or 'n'.")
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False


def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""

    # Display welcome message
    display_welcome()

    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return

    # Main menu loop
    while True:
        choice = main_menu()

        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()
