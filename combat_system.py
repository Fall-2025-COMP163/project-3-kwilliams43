"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    enemies  = {"goblin": {"name": "Goblin", "health": 50, "max_health": 50,"strength": 8, "magic": 2, "xp_reward": 25, "gold_reward": 10},
        "orc": {"name": "Orc", "health": 80, "max_health": 80,"strength": 12, "magic": 5, "xp_reward": 50, "gold_reward": 25},
        "dragon": {"name": "Dragon", "health": 200, "max_health": 200,"strength": 25, "magic": 15, "xp_reward": 200, "gold_reward": 100}}
    if enemy_type not in enemies:
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")
    return enemies[enemy_type].copy()

def get_random_enemy_for_level(character_level):
    """Select enemy type based on level"""
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")
    

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_count = 0

    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        if self.character["health"] <= 0:
            raise CharacterDeadError("Character is already dead.")
        while self.combat_active:
            self.turn_count += 1
            self.player_turn()
            if self.check_battle_end():
                break
            self.enemy_turn()
            if self.check_battle_end():
                break
        winner = self.check_battle_end()
        if winner == "player":
            rewards = get_victory_rewards(self.enemy)
            return {"winner": "player", "xp_gained": rewards["xp"], "gold_gained": rewards["gold"]}
        else:
            return {"winner": "enemy", "xp_gained": 0, "gold_gained": 0}

    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError("Battle not active.")
        # For simplicity, always basic attack
        dmg = self.calculate_damage(self.character, self.enemy)
        self.apply_damage(self.enemy, dmg)
        display_battle_log(f"{self.character['name']} attacks for {dmg} damage.")
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
         if not self.combat_active:
            raise CombatNotActiveError("Battle not active.")
        dmg = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, dmg)
        display_battle_log(f"{self.enemy['name']} attacks for {dmg} damage.")
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        dmg = attacker["strength"] - (defender["strength"] // 4)
        return max(1, dmg)
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        target["health"] = max(0, target["health"] - damage)
        
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        if self.enemy["health"] <= 0:
            self.combat_active = False
            return "player"
        if self.character["health"] <= 0:
            self.combat_active = False
            return "enemy"
        return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        if random.random() < 0.5:
            self.combat_active = False
            return True
        return False

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    cls = character["class"]
    if cls == "Warrior":
        return warrior_power_strike(character, enemy)
    elif cls == "Mage":
        return mage_fireball(character, enemy)
    elif cls == "Rogue":
        return rogue_critical_strike(character, enemy)
    elif cls == "Cleric":
        return cleric_heal(character)
    else:
        raise InvalidTargetError(f"No special ability for class {cls}")

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    dmg = character["strength"] * 2
    enemy["health"] = max(0, enemy["health"] - dmg)
    return f"{character['name']} uses Power Strike for {dmg} damage!"

def mage_fireball(character, enemy):
    """Mage special ability"""
    dmg = character["magic"] * 2
    enemy["health"] = max(0, enemy["health"] - dmg)
    return f"{character['name']} casts Fireball for {dmg} damage!"

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    if random.random() < 0.5:
        dmg = character["strength"] * 3
        enemy["health"] = max(0, enemy["health"] - dmg)
        return f"{character['name']} lands a Critical Strike for {dmg} damage!"
    else:
        dmg = character["strength"]
        enemy["health"] = max(0, enemy["health"] - dmg)
        return f"{character['name']} attacks for {dmg} damage (no crit)."

def cleric_heal(character):
    """Cleric special ability"""
    heal = 30
    character["health"] = min(character["max_health"], character["health"] + heal)
    return f"{character['name']} heals for {heal} HP."

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
   return character["health"] > 0

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    return {"xp": enemy["xp_reward"], "gold": enemy["gold_reward"]}

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    pass

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    try:
        goblin = create_enemy("goblin")
        print(f"Created {goblin['name']}")
    except InvalidTargetError as e:
        print(f"Invalid enemy: {e}")

    test_char = {'name': 'Hero', 'class': 'Warrior','health': 120,'max_health': 120,'strength': 15,'magic': 5}

    battle = SimpleBattle(test_char, goblin)
    try:
        result = battle.start_battle()
        print(f"Battle result: {result}")
    except CharacterDeadError:
        print("Character is dead!")

