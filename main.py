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
    print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")
    choice = input("Choose an option (1-3): ")
    if choice.isdigit() and int(choice) in (1, 2, 3):
        return int(choice)
    else:
        print("Invalid choice.")
        return main_menu()

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character

    name = input("Enter your character's name: ")
    print("Choose a class: Warrior, Mage, Rogue, Cleric")
    cls = input("Class: ")
    try:
        current_character = character_manager.create_character(name, cls)
        print(f"Character {name} the {cls} created!")
        game_loop()
    except CharacterCreationError as e:
        print(f"Error creating character: {e}")

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    try:
        current_character = character_manager.load_character("slot1")
        print(f"Loaded character {current_character['name']}")
        game_loop()
    except (CharacterNotFoundError, SaveFileCorruptedError) as e:
        print(f"Error loading game: {e}")

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    while game_running:
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
            print("Game saved. Exiting...")
            game_running = False

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
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")
    choice = input("Choose an option (1-6): ")
    if choice.isdigit() and int(choice) in range(1, 7):
        return int(choice)
    else:
        print("Invalid choice.")
        return game_menu()

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    print("\n=== CHARACTER STATS ===")
    for k, v in current_character.items():
        if k != "inventory" and k != "equipment":
            print(f"{k}: {v}")
    quest_handler.display_character_quest_progress(current_character, all_quests)

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
     print("\n=== INVENTORY ===")
    for item in current_character["inventory"]:
        print(f"- {item['name']} ({item['type']})")

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    print("\n=== QUEST MENU ===")
    print("1. View Active Quests")
    print("2. View Available Quests")
    print("3. View Completed Quests")
    print("4. Accept Quest")
    print("5. Abandon Quest")
    print("6. Complete Quest (test)")
    print("7. Back")
    choice = input("Choose option: ")
    if choice == "1":
        quests = quest_handler.get_active_quests(current_character, all_quests)
        quest_handler.display_quest_list(quests)
    elif choice == "2":
        quests = quest_handler.get_available_quests(current_character, all_quests)
        quest_handler.display_quest_list(quests)
    elif choice == "3":
        quests = quest_handler.get_completed_quests(current_character, all_quests)
        quest_handler.display_quest_list(quests)
    elif choice == "4":
        qid = input("Enter quest id to accept: ")
        try:
            quest_handler.accept_quest(current_character, qid, all_quests)
            print("Quest accepted!")
        except Exception as e:
            print(f"Error: {e}")
    elif choice == "5":
        qid = input("Enter quest id to abandon: ")
        try:
            quest_handler.abandon_quest(current_character, qid)
            print("Quest abandoned.")
        except Exception as e:
            print(f"Error: {e}")
    elif choice == "6":
        qid = input("Enter quest id to complete: ")
        try:
            rewards = quest_handler.complete_quest(current_character, qid, all_quests)
            print(f"Quest completed! Rewards: {rewards}")
        except Exception as e:
            print(f"Error: {e}")

def explore():
    """Find and fight random enemies"""
    global current_character
    
    enemy = combat_system.get_random_enemy_for_level(current_character["level"])
    battle = combat_system.SimpleBattle(current_character, enemy)
    try:
        result = battle.start_battle()
        print(f"Battle result: {result}")
        if result["winner"] == "enemy":
            handle_character_death()
    except CharacterDeadError:
        handle_character_death()

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    global current_character, all_items
    print("\n=== SHOP ===")
    print(f"Gold: {current_character['gold']}")
    for iid, item in all_items.items():
        print(f"{iid}: {item['name']} ({item['cost']} gold)")
    

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    try:
        character_manager.save_character(current_character, "slot1")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except MissingDataFileError:
        print("Missing data files. Creating defaults...")
        game_data.create_default_data_files()
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except InvalidDataFormatError as e:
        print(f"Data format error: {e}")

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    print("\nYou have died!")
    choice = input("Revive for 50 gold? (y/n): ")
    if choice.lower() == "y" and current_character["gold"] >= 50:
        character_manager.revive_character(current_character, cost=50)
        print("You are revived!")
    else:
        print("Game over.")
        game_running = False

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

