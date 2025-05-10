import pygame
import json
import os
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 1200
HEIGHT = 800
GRID_SIZE = 5
CELL_SIZE = 50
GRID_OFFSET_X = 50
GRID_OFFSET_Y = 100
BOT_GRID_OFFSET_X = WIDTH // 2 + 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game states
MENU = 0
USERNAME_INPUT = 1
GUIDE = 2
PLAY = 3
GAME_OVER = 4
VIEW_PLANS = 5
game_state = MENU

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Farm Frenzy")

# Load background image
try:
    background_img = pygame.image.load("background.png")
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
except pygame.error as e:
    print(f"Error loading background.png: {e}")
    print("Falling back to default background color.")
    background_img = None

# Load assets
soil_tile = pygame.image.load(os.path.join("Tiles", "tile_0014.png"))
soil_tile = pygame.transform.scale(soil_tile, (CELL_SIZE, CELL_SIZE))

panel_beige = pygame.image.load(os.path.join("UI", "panel_beige.png"))
panel_beige = pygame.transform.scale(panel_beige, (600, 400))
stats_panel = pygame.image.load(os.path.join("UI", "panel_beige.png"))
stats_panel = pygame.transform.scale(stats_panel, (180, 200))
button_long_beige = pygame.image.load(os.path.join("UI", "buttonLong_beige.png"))
button_long_beige = pygame.transform.scale(button_long_beige, (200, 50))
button_long_beige_pressed = pygame.image.load(os.path.join("UI", "buttonLong_beige_pressed.png"))
button_long_beige_pressed = pygame.transform.scale(button_long_beige_pressed, (200, 50))
button_square_beige = pygame.image.load(os.path.join("UI", "buttonSquare_beige.png"))
button_square_beige = pygame.transform.scale(button_square_beige, (100, 50))
button_square_beige_pressed = pygame.image.load(os.path.join("UI", "buttonSquare_beige_pressed.png"))
button_square_beige_pressed = pygame.transform.scale(button_square_beige_pressed, (100, 50))

sprites = {
    "house_large_1": pygame.image.load(os.path.join("sprites", "sprite_0544.png")),
    "house_large_2": pygame.image.load(os.path.join("sprites", "sprite_0545.png")),
    "house_large_3": pygame.image.load(os.path.join("sprites", "sprite_0604.png")),
    "house_large_4": pygame.image.load(os.path.join("sprites", "sprite_0605.png")),
    "lake_1": pygame.image.load(os.path.join("sprites", "sprite_1440.png")),
    "lake_2": pygame.image.load(os.path.join("sprites", "sprite_1441.png")),
    "lake_3": pygame.image.load(os.path.join("sprites", "sprite_1442.png")),
    "lake_4": pygame.image.load(os.path.join("sprites", "sprite_1443.png")),
    "lake_5": pygame.image.load(os.path.join("sprites", "sprite_1500.png")),
    "lake_6": pygame.image.load(os.path.join("sprites", "sprite_1501.png")),
    "lake_7": pygame.image.load(os.path.join("sprites", "sprite_1502.png")),
    "lake_8": pygame.image.load(os.path.join("sprites", "sprite_1503.png")),
    "lake_9": pygame.image.load(os.path.join("sprites", "sprite_1560.png")),
    "lake_10": pygame.image.load(os.path.join("sprites", "sprite_1561.png")),
    "lake_11": pygame.image.load(os.path.join("sprites", "sprite_1562.png")),
    "lake_12": pygame.image.load(os.path.join("sprites", "sprite_1563.png")),
    "lake_13": pygame.image.load(os.path.join("sprites", "sprite_1620.png")),
    "lake_14": pygame.image.load(os.path.join("sprites", "sprite_1621.png")),
    "lake_15": pygame.image.load(os.path.join("sprites", "sprite_1622.png")),
    "lake_16": pygame.image.load(os.path.join("sprites", "sprite_1623.png")),
    "tree_large_1": pygame.image.load(os.path.join("sprites", "sprite_0008.png")),
    "tree_large_2": pygame.image.load(os.path.join("sprites", "sprite_0068.png")),
    "greenhouse_1": pygame.image.load(os.path.join("Tiles", "tile_0032.png")),
    "greenhouse_2": pygame.image.load(os.path.join("Tiles", "tile_0033.png")),
    "greenhouse_3": pygame.image.load(os.path.join("Tiles", "tile_0034.png")),
    "greenhouse_4": pygame.image.load(os.path.join("Tiles", "tile_0035.png")),
    "greenhouse_5": pygame.image.load(os.path.join("Tiles", "tile_0048.png")),
    "greenhouse_6": pygame.image.load(os.path.join("Tiles", "tile_0049.png")),
    "greenhouse_7": pygame.image.load(os.path.join("Tiles", "tile_0050.png")),
    "greenhouse_8": pygame.image.load(os.path.join("Tiles", "tile_0051.png")),
    "fence": pygame.image.load(os.path.join("Tiles", "tile_0006.png")),
    "flower": pygame.image.load(os.path.join("Tiles", "tile_0020.png")),
}

SPRITE_SCALE_ROGUE = 2
rogue_keys = ["house_large_1", "house_large_2", "house_large_3", "house_large_4",
              "lake_1", "lake_2", "lake_3", "lake_4", "lake_5", "lake_6", "lake_7", "lake_8",
              "lake_9", "lake_10", "lake_11", "lake_12", "lake_13", "lake_14", "lake_15", "lake_16",
              "tree_large_1", "tree_large_2"]
for key in rogue_keys:
    sprites[key] = pygame.transform.scale(sprites[key], (sprites[key].get_width() * SPRITE_SCALE_ROGUE, sprites[key].get_height() * SPRITE_SCALE_ROGUE))

SPRITE_SCALE_FARM = 2
farm_keys = ["greenhouse_1", "greenhouse_2", "greenhouse_3", "greenhouse_4",
             "greenhouse_5", "greenhouse_6", "greenhouse_7", "greenhouse_8",
             "fence", "flower"]
for key in farm_keys:
    sprites[key] = pygame.transform.scale(sprites[key], (sprites[key].get_width() * SPRITE_SCALE_FARM, sprites[key].get_height() * SPRITE_SCALE_FARM))

# Fonts
font = pygame.font.Font(None, 36)

# Player stats
username = ""
high_score = 0
budget = 150
day = 1
MAX_DAYS = 10
profit = 0
DAY_DURATION = 8 * 1000
day_timer = 0
last_day_update = 0

# Bot stats
bot_profit = 0
selected_bot = None
BOT_TYPES = ["backtracking", "dp", "greedy"]
bot_grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
bot_timers = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
bot_plan_steps = []
bot_step_index = 0
last_bot_action = 0
BOT_ACTION_INTERVAL = 8000
bot_messages = []
BOT_MESSAGE_DURATION = 5000
last_disrupt_time = 0
DISRUPT_COOLDOWN = 15000

# Player plan tracking
player_plan = []

# Weather system
WEATHER_TYPES = ["Sunny", "Rainy", "Dry"]
current_weather = "Sunny"
next_weather = "Sunny"

# Crop diversity tracking
harvested_crops = set()
DIVERSITY_BONUS = 30

# Market prices
market_prices = {"rice": 25, "corn": 35, "tomato": 50, "carrot": 40}
original_profits = {"rice": 25, "corn": 35, "tomato": 50, "carrot": 40}

# Crops data
CROPS = {
    "rice": {
        "cost": 10,
        "time": 2,
        "profit": 25,
        "sprite": pygame.transform.scale(pygame.image.load(os.path.join("Tiles", "tile_0059.png")), (CELL_SIZE - 10, CELL_SIZE - 10)),
        "color": GREEN
    },
    "corn": {
        "cost": 15,
        "time": 2,
        "profit": 35,
        "sprite": pygame.transform.scale(pygame.image.load(os.path.join("Tiles", "tile_0058.png")), (CELL_SIZE - 10, CELL_SIZE - 10)),
        "color": YELLOW
    },
    "tomato": {
        "cost": 20,
        "time": 4,
        "profit": 50,
        "sprite": pygame.transform.scale(pygame.image.load(os.path.join("Tiles", "tile_0057.png")), (CELL_SIZE - 10, CELL_SIZE - 10)),
        "color": RED
    },
    "carrot": {
        "cost": 12,
        "time": 3,
        "profit": 40,
        "sprite": pygame.transform.scale(pygame.image.load(os.path.join("Tiles", "tile_0056.png")), (CELL_SIZE - 10, CELL_SIZE - 10)),
        "color": BROWN
    },
}

# Farm grid
farm_grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
crop_timers = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
crop_protected = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Buttons
play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
guide_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
back_button_rect = pygame.Rect(50, HEIGHT - 70, 100, 50)
play_again_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
finish_button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 70, 100, 50)
remove_button_rect = pygame.Rect(50 + 3 * 120, GRID_OFFSET_Y + GRID_SIZE * CELL_SIZE + 20, 100, 50)
water_button_rect = pygame.Rect(50 + 4 * 120, GRID_OFFSET_Y + GRID_SIZE * CELL_SIZE + 20, 100, 50)
protect_button_rect = pygame.Rect(50 + 5 * 120, GRID_OFFSET_Y + GRID_SIZE * CELL_SIZE + 20, 100, 50)
disrupt_button_rect = pygame.Rect(50 + 6 * 120, GRID_OFFSET_Y + GRID_SIZE * CELL_SIZE + 20, 100, 50)
back_to_menu_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 150, 100, 50)
view_plans_button_rect = pygame.Rect(WIDTH // 2 + 50, HEIGHT - 150, 100, 50)
weather_rect = pygame.Rect((50 + 700) // 2 - 80, GRID_OFFSET_Y + GRID_SIZE * CELL_SIZE + 70, 160, 40)
next_weather_rect = pygame.Rect((50 + 700) // 2 - 80, GRID_OFFSET_Y + GRID_SIZE * CELL_SIZE + 120, 160, 40)

# Modes
selected_crop = None
remove_mode = False
water_mode = False
protect_mode = False
disrupt_mode = False

# Username input
username_input = ""
username_input_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 25, 300, 50)
username_input_active = False

# High scores
high_scores = {}

# AI plans
all_configs = []
selected_config = None
previous_config = None
ai_plans = {}
ai_profits = {}

# --- Game Functions ---

def load_high_scores():
    global high_scores
    try:
        with open("high_scores.json", "r") as f:
            high_scores = json.load(f)
    except FileNotFoundError:
        high_scores = {}
    except json.JSONDecodeError:
        high_scores = {}

def save_high_scores():
    with open("high_scores.json", "w") as f:
        json.dump(high_scores, f, indent=4)

def setup():
    global all_configs, selected_config, budget, ai_plans, ai_profits, selected_bot, bot_plan_steps, bot_step_index, next_weather
    print("Loading AI plans from file...")
    try:
        with open("ai_plans.json", "r") as f:
            all_configs = json.load(f)
        if not all_configs:
            raise ValueError("No configurations found in ai_plans.json")
        
        available_configs = [cfg for cfg in all_configs if cfg != previous_config]
        if not available_configs:
            available_configs = all_configs
        selected_config = random.choice(available_configs)
        
        budget = selected_config["budget"]
        ai_plans = selected_config["ai_plans"]
        ai_profits = selected_config["ai_profits"]
        
        selected_bot = random.choice(BOT_TYPES)
        bot_plan_steps = ai_plans[selected_bot]
        bot_step_index = 0
        
        next_weather = random.choice(WEATHER_TYPES)
        
        print(f"Selected configuration with budget {budget}")
        print(f"Selected bot: {selected_bot}")
        print(f"Bot plan steps: {bot_plan_steps}")
    except FileNotFoundError:
        print("Error: ai_plans.json not found. Please run generate_ai_plans.py first.")
        exit(1)
    except ValueError as e:
        print(f"Error: {e}. Please run generate_ai_plans.py to generate valid plans.")
        exit(1)

def reset_game():
    global username, high_score, budget, day, profit, day_timer, last_day_update
    global farm_grid, crop_timers, crop_protected, selected_crop, remove_mode, water_mode, protect_mode, disrupt_mode
    global bot_profit, bot_grid, bot_timers, bot_step_index, last_bot_action, previous_config, bot_messages
    global current_weather, next_weather, harvested_crops, player_plan, market_prices, last_disrupt_time
    username = ""
    high_score = 0
    budget = 150
    day = 1
    profit = 0
    day_timer = 0
    last_day_update = 0
    farm_grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    crop_timers = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    crop_protected = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    selected_crop = None
    remove_mode = False
    water_mode = False
    protect_mode = False
    disrupt_mode = False
    bot_profit = 0
    bot_grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    bot_timers = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    bot_step_index = 0
    last_bot_action = 0
    bot_messages = []
    current_weather = "Sunny"
    next_weather = random.choice(WEATHER_TYPES)
    harvested_crops = set()
    player_plan = []
    market_prices = original_profits.copy()
    last_disrupt_time = 0
    previous_config = selected_config
    setup()

def update_market_prices():
    global market_prices
    for crop in market_prices:
        fluctuation = random.uniform(-0.3, 0.3)
        market_prices[crop] = max(0.5 * original_profits[crop], original_profits[crop] * (1 + fluctuation))

def apply_weather_effects(grid, timers, protected_grid):
    global profit, bot_profit, harvested_crops
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j]:
                crop = grid[i][j]
                crop_data = CROPS[crop]
                time_reduction = 0
                fail_chance = 0
                if current_weather == "Sunny" and crop == "tomato":
                    time_reduction = 1
                elif current_weather == "Rainy":
                    if crop == "rice":
                        time_reduction = 1
                    elif crop == "tomato" and not protected_grid[i][j]:
                        fail_chance = 0.5
                elif current_weather == "Dry":
                    if crop == "corn":
                        time_reduction = 1
                    elif crop == "rice" and not protected_grid[i][j]:
                        fail_chance = 0.5
                
                if fail_chance > 0 and random.random() < fail_chance:
                    grid[i][j] = None
                    timers[i][j] = 0
                    message = f"{'Bot' if grid is bot_grid else 'Player'}'s {crop} at ({i}, {j}) failed due to {current_weather} weather!"
                    bot_messages.append((message, pygame.time.get_ticks()))
                    continue
                
                if time_reduction > 0 and timers[i][j] > 0:
                    timers[i][j] = max(1, timers[i][j] - time_reduction)

def draw_grid(grid, timers, offset_x, protected_grid, hide_crops=False):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell_rect = pygame.Rect(offset_x + j * CELL_SIZE, GRID_OFFSET_Y + i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            screen.blit(soil_tile, (cell_rect.x, cell_rect.y))
            if grid[i][j]:
                if hide_crops:
                    pygame.draw.rect(screen, GRAY, cell_rect)
                else:
                    crop_data = CROPS[grid[i][j]]
                    screen.blit(crop_data["sprite"], (cell_rect.x + 5, cell_rect.y + 5))
                    if timers[i][j] > 0:
                        timer_text = font.render(str(timers[i][j]), True, BLACK)
                        screen.blit(timer_text, (cell_rect.x + 15, cell_rect.y + 15))
                if protected_grid[i][j]:
                    pygame.draw.rect(screen, BLUE, cell_rect, 2)
                if water_mode and grid[i][j] and cell_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, GREEN, cell_rect, 2)
                if protect_mode and grid[i][j] and not protected_grid[i][j] and cell_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, BLUE, cell_rect, 2)
                if disrupt_mode and bot_grid[i][j] and cell_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, RED, cell_rect, 2)

def draw_play():
    print("Drawing play screen...")
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(GREEN)
    
    draw_grid(farm_grid, crop_timers, GRID_OFFSET_X, crop_protected, hide_crops=False)
    draw_grid(bot_grid, bot_timers, BOT_GRID_OFFSET_X, [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)], hide_crops=False)
    
    player_label = font.render("Your Farm", True, BLACK)
    bot_label = font.render(f"Bot ({selected_bot.capitalize()})", True, BLACK)
    screen.blit(player_label, (GRID_OFFSET_X, GRID_OFFSET_Y - 30))
    screen.blit(bot_label, (BOT_GRID_OFFSET_X, GRID_OFFSET_Y - 30))
    
    remaining_time = max(0, (DAY_DURATION - day_timer) // 1000)
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    timer_display = f"Time: {minutes:02d}:{seconds:02d}"
    
    day_rect = pygame.Rect(WIDTH - 180, 20, 160, 100)
    screen.blit(stats_panel, (day_rect.x, day_rect.y), (0, 0, 160, 100))
    day_text = font.render(f"Day: {day}/{MAX_DAYS}", True, BLACK)
    time_text = font.render(timer_display, True, BLACK)
    screen.blit(day_text, (day_rect.x + 10, day_rect.y + 10))
    screen.blit(time_text, (day_rect.x + 10, day_rect.y + 35))
    
    stats_rect = pygame.Rect(WIDTH - 180, HEIGHT - 150, 160, 120)
    screen.blit(stats_panel, (stats_rect.x, stats_rect.y), (0, 0, 160, 120))
    budget_text = font.render(f"Budget: {budget}", True, BLACK)
    profit_text = font.render(f"Profit: {profit}", True, BLACK)
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    bot_profit_text = font.render(f"Bot Profit: {'???' if day <= MAX_DAYS else bot_profit}", True, BLACK)
    screen.blit(budget_text, (stats_rect.x + 10, stats_rect.y + 10))
    screen.blit(profit_text, (stats_rect.x + 10, stats_rect.y + 35))
    screen.blit(high_score_text, (stats_rect.x + 10, stats_rect.y + 60))
    screen.blit(bot_profit_text, (stats_rect.x + 10, stats_rect.y + 85))
    
    screen.blit(stats_panel, (weather_rect.x, weather_rect.y), (0, 0, 160, 40))
    weather_text = font.render(f"Weather: {current_weather}", True, BLACK)
    text_rect = weather_text.get_rect(center=(weather_rect.x + weather_rect.width // 2, weather_rect.y + weather_rect.height // 2))
    screen.blit(weather_text, text_rect)
    
    screen.blit(stats_panel, (next_weather_rect.x, next_weather_rect.y), (0, 0, 160, 40))
    next_weather_text = font.render(f"Tomorrow: {next_weather}", True, BLACK)
    next_text_rect = next_weather_text.get_rect(center=(next_weather_rect.x + next_weather_rect.width // 2, next_weather_rect.y + next_weather_rect.height // 2))
    screen.blit(next_weather_text, next_text_rect)
    
    diversity_rect = pygame.Rect(50, HEIGHT - 100, 160, 30)
    screen.blit(stats_panel, (diversity_rect.x, diversity_rect.y), (0, 0, 160, 30))
    diversity_text = font.render(f"Diversity: {len(harvested_crops)}/4", True, BLACK)
    screen.blit(diversity_text, (diversity_rect.x + 10, diversity_rect.y + 5))
    
    mouse_pos = pygame.mouse.get_pos()
    for idx, (crop_name, _) in enumerate(CROPS.items()):
        button_rect = pygame.Rect(50 + idx * 120, 20, 100, 50)
        if button_rect.collidepoint(mouse_pos):
            screen.blit(button_square_beige_pressed, (button_rect.x, button_rect.y))
        else:
            if selected_crop == crop_name and not remove_mode and not water_mode and not protect_mode and not disrupt_mode:
                screen.blit(button_square_beige_pressed, (button_rect.x, button_rect.y))
            else:
                screen.blit(button_square_beige, (button_rect.x, button_rect.y))
        text = font.render(f"{crop_name.capitalize()}: {int(market_prices[crop_name])}", True, BLACK)
        screen.blit(text, (button_rect.x + 10, button_rect.y + 10))
    
    if water_button_rect.collidepoint(mouse_pos):
        screen.blit(button_square_beige_pressed, (water_button_rect.x, water_button_rect.y))
    else:
        if water_mode:
            screen.blit(button_square_beige_pressed, (water_button_rect.x, water_button_rect.y))
        else:
            screen.blit(button_square_beige, (water_button_rect.x, water_button_rect.y))
    water_text = font.render("Water (5)", True, BLACK)
    screen.blit(water_text, (water_button_rect.x + 10, water_button_rect.y + 10))
    
    if remove_button_rect.collidepoint(mouse_pos):
        screen.blit(button_square_beige_pressed, (remove_button_rect.x, remove_button_rect.y))
    else:
        if remove_mode:
            screen.blit(button_square_beige_pressed, (remove_button_rect.x, remove_button_rect.y))
        else:
            screen.blit(button_square_beige, (remove_button_rect.x, remove_button_rect.y))
    remove_text = font.render("Remove", True, BLACK)
    screen.blit(remove_text, (remove_button_rect.x + 10, remove_button_rect.y + 10))
    
    if protect_button_rect.collidepoint(mouse_pos):
        screen.blit(button_square_beige_pressed, (protect_button_rect.x, protect_button_rect.y))
    else:
        if protect_mode:
            screen.blit(button_square_beige_pressed, (protect_button_rect.x, protect_button_rect.y))
        else:
            screen.blit(button_square_beige, (protect_button_rect.x, protect_button_rect.y))
    protect_text = font.render("Protect (10)", True, BLACK)
    screen.blit(protect_text, (protect_button_rect.x + 10, protect_button_rect.y + 10))
    
    if disrupt_button_rect.collidepoint(mouse_pos):
        screen.blit(button_square_beige_pressed, (disrupt_button_rect.x, disrupt_button_rect.y))
    else:
        if disrupt_mode:
            screen.blit(button_square_beige_pressed, (disrupt_button_rect.x, disrupt_button_rect.y))
        else:
            screen.blit(button_square_beige, (disrupt_button_rect.x, disrupt_button_rect.y))
    disrupt_text = font.render("Disrupt (20)", True, BLACK)
    screen.blit(disrupt_text, (disrupt_button_rect.x + 10, disrupt_button_rect.y + 10))
    
    if finish_button_rect.collidepoint(mouse_pos):
        screen.blit(button_square_beige_pressed, (finish_button_rect.x, finish_button_rect.y))
    else:
        screen.blit(button_square_beige, (finish_button_rect.x, finish_button_rect.y))
    finish_text = font.render("Finish", True, BLACK)
    screen.blit(finish_text, (finish_button_rect.x + 20, finish_button_rect.y + 10))
    
    current_time = pygame.time.get_ticks()
    bot_messages[:] = [msg for msg in bot_messages if current_time - msg[1] < BOT_MESSAGE_DURATION]
    for i, (message, _) in enumerate(bot_messages[-3:]):
        text = font.render(message, True, BLACK)
        screen.blit(text, (50, 50 + i * 30))

def draw_menu():
    print("Drawing menu screen...")
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(GREEN)
    
    lake_x, lake_y = WIDTH // 2 - 64, HEIGHT // 4
    screen.blit(sprites["lake_1"], (lake_x, lake_y))
    screen.blit(sprites["lake_2"], (lake_x + 32, lake_y))
    screen.blit(sprites["lake_3"], (lake_x + 64, lake_y))
    screen.blit(sprites["lake_4"], (lake_x + 96, lake_y))
    screen.blit(sprites["lake_5"], (lake_x, lake_y + 32))
    screen.blit(sprites["lake_6"], (lake_x + 32, lake_y + 32))
    screen.blit(sprites["lake_7"], (lake_x + 64, lake_y + 32))
    screen.blit(sprites["lake_8"], (lake_x + 96, lake_y + 32))
    screen.blit(sprites["lake_9"], (lake_x, lake_y + 64))
    screen.blit(sprites["lake_10"], (lake_x + 32, lake_y + 64))
    screen.blit(sprites["lake_11"], (lake_x + 64, lake_y + 64))
    screen.blit(sprites["lake_12"], (lake_x + 96, lake_y + 64))
    screen.blit(sprites["lake_13"], (lake_x, lake_y + 96))
    screen.blit(sprites["lake_14"], (lake_x + 32, lake_y + 96))
    screen.blit(sprites["lake_15"], (lake_x + 64, lake_y + 96))
    screen.blit(sprites["lake_16"], (lake_x + 96, lake_y + 96))
    house_x, house_y = 50, HEIGHT - 150
    screen.blit(sprites["house_large_1"], (house_x, house_y))
    screen.blit(sprites["house_large_2"], (house_x + 32, house_y))
    screen.blit(sprites["house_large_3"], (house_x, house_y + 32))
    screen.blit(sprites["house_large_4"], (house_x + 32, house_y + 32))
    for pos in [(50, 50), (100, 80), (150, 30)]:
        screen.blit(sprites["tree_large_1"], (pos[0], pos[1]))
        screen.blit(sprites["tree_large_2"], (pos[0], pos[1] + 32))
    greenhouse_x, greenhouse_y = WIDTH - 200, 50
    screen.blit(sprites["greenhouse_1"], (greenhouse_x, greenhouse_y))
    screen.blit(sprites["greenhouse_2"], (greenhouse_x + 36, greenhouse_y))
    screen.blit(sprites["greenhouse_3"], (greenhouse_x + 72, greenhouse_y))
    screen.blit(sprites["greenhouse_4"], (greenhouse_x + 108, greenhouse_y))
    screen.blit(sprites["greenhouse_5"], (greenhouse_x, greenhouse_y + 36))
    screen.blit(sprites["greenhouse_6"], (greenhouse_x + 36, greenhouse_y + 36))
    screen.blit(sprites["greenhouse_7"], (greenhouse_x + 72, greenhouse_y + 36))
    screen.blit(sprites["greenhouse_8"], (greenhouse_x + 108, greenhouse_y + 36))
    for x in range(50, WIDTH - 50, 36):
        screen.blit(sprites["fence"], (x, HEIGHT // 2 - 50))
    for pos in [(50, HEIGHT - 100), (100, HEIGHT - 100), (400, HEIGHT - 100)]:
        screen.blit(sprites["flower"], pos)
    
    mouse_pos = pygame.mouse.get_pos()
    if play_button_rect.collidepoint(mouse_pos):
        screen.blit(button_long_beige_pressed, (play_button_rect.x, play_button_rect.y))
    else:
        screen.blit(button_long_beige, (play_button_rect.x, play_button_rect.y))
    if guide_button_rect.collidepoint(mouse_pos):
        screen.blit(button_long_beige_pressed, (guide_button_rect.x, guide_button_rect.y))
    else:
        screen.blit(button_long_beige, (guide_button_rect.x, guide_button_rect.y))
    
    play_text = font.render("Play", True, BLACK)
    guide_text = font.render("Guide", True, BLACK)
    screen.blit(play_text, (play_button_rect.x + 70, play_button_rect.y + 10))
    screen.blit(guide_text, (guide_button_rect.x + 60, guide_button_rect.y + 10))

def draw_username_input():
    print("Drawing username input screen...")
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(GREEN)
    
    pygame.draw.rect(screen, WHITE, username_input_rect)
    if username_input_active:
        pygame.draw.rect(screen, BLACK, username_input_rect, 2)
    else:
        pygame.draw.rect(screen, GRAY, username_input_rect, 2)
    
    input_text = font.render(username_input, True, BLACK)
    screen.blit(input_text, (username_input_rect.x + 10, username_input_rect.y + 10))
    
    prompt_text = font.render("Enter your username and press Enter", True, BLACK)
    screen.blit(prompt_text, (WIDTH // 2 - 150, HEIGHT // 2 - 80))

def draw_guide():
    print("Drawing guide screen...")
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(GREEN)
    
    panel_rect = pygame.Rect(100, 100, 600, 400)
    screen.blit(panel_beige, (panel_rect.x, panel_rect.y))
    
    guide_lines = [
        "Farm Frenzy Guide",
        "1. Click a cell to plant crops.",
        "2. Crops: Rice (10, 2d, 25), Corn (15, 2d, 35),",
        "   Tomato (20, 4d, 50), Carrot (12, 3d, 40).",
        f"3. Budget: {budget}, {MAX_DAYS} days to maximize profit.",
        "4. Each day lasts 8 seconds.",
        "5. Weather: Sunny (Tomato +1), Rainy (Rice +1, Tomato 50% fail),",
        "   Dry (Corn +1, Rice 50% fail).",
        "6. Diversity bonus: +30 profit for all 4 crops.",
        "7. Actions: Water (-1 day, 5), Protect (no fail, 10),",
        "   Disrupt bot (+1 day, 20).",
        "8. Compete with bot (Backtracking, DP, Greedy).",
        "9. Click Finish to end early."
    ]
    for i, line in enumerate(guide_lines):
        text = font.render(line, True, BLACK)
        screen.blit(text, (120, 120 + i * 40))
    
    mouse_pos = pygame.mouse.get_pos()
    if back_button_rect.collidepoint(mouse_pos):
        screen.blit(button_square_beige_pressed, (back_button_rect.x, back_button_rect.y))
    else:
        screen.blit(button_square_beige, (back_button_rect.x, back_button_rect.y))
    back_text = font.render("Back", True, BLACK)
    screen.blit(back_text, (back_button_rect.x + 20, back_button_rect.y + 10))

def draw_game_over():
    print("Drawing game over screen...")
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(GREEN)

    panel_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 200)
    screen.blit(stats_panel, (panel_rect.x, panel_rect.y), (0, 0, 300, 200))

    game_over_text = font.render("Game Over!", True, BLACK)
    profit_text = font.render(f"Your Profit: {profit}", True, BLACK)
    high_score_text = font.render(f"Your High Score: {high_score}", True, BLACK)
    bot_profit_text = font.render(f"Bot Profit: {bot_profit}", True, BLACK)
    bot_plan_text = font.render(f"Bot Plan: {selected_bot.capitalize()}", True, BLACK)

    if profit > bot_profit:
        result_text = font.render("You Win!", True, BLACK)
    elif profit < bot_profit:
        result_text = font.render("You Lose!", True, BLACK)
    else:
        result_text = font.render("It's a Tie!", True, BLACK)

    screen.blit(game_over_text, (panel_rect.x + 90, panel_rect.y + 20))
    screen.blit(profit_text, (panel_rect.x + 20, panel_rect.y + 50))
    screen.blit(high_score_text, (panel_rect.x + 20, panel_rect.y + 80))
    screen.blit(bot_profit_text, (panel_rect.x + 20, panel_rect.y + 110))
    screen.blit(bot_plan_text, (panel_rect.x + 20, panel_rect.y + 140))
    screen.blit(result_text, (panel_rect.x + 90, panel_rect.y + 170))

    mouse_pos = pygame.mouse.get_pos()
    if back_to_menu_button_rect.collidepoint(mouse_pos):
        screen.blit(button_square_beige_pressed, (back_to_menu_button_rect.x, back_to_menu_button_rect.y))
    else:
        screen.blit(button_square_beige, (back_to_menu_button_rect.x, back_to_menu_button_rect.y))
    back_to_menu_text = font.render("Back to Menu", True, BLACK)
    screen.blit(back_to_menu_text, (back_to_menu_button_rect.x + 5, back_to_menu_button_rect.y + 10))

    if view_plans_button_rect.collidepoint(mouse_pos):
        screen.blit(button_square_beige_pressed, (view_plans_button_rect.x, view_plans_button_rect.y))
    else:
        screen.blit(button_square_beige, (view_plans_button_rect.x, view_plans_button_rect.y))
    view_plans_text = font.render("View Plans", True, BLACK)
    screen.blit(view_plans_text, (view_plans_button_rect.x + 10, view_plans_button_rect.y + 10))

def draw_view_plans():
    print("Drawing view plans screen...")
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(GREEN)

    panel_rect = pygame.Rect(50, 50, 700, 500)
    screen.blit(panel_beige, (panel_rect.x, panel_rect.y))

    player_plan_text = font.render("Your Plan:", True, BLACK)
    screen.blit(player_plan_text, (panel_rect.x + 20, panel_rect.y + 20))
    for i, action in enumerate(player_plan):
        action_text = font.render(f"Step {i+1}: {action[1]} at {action[0]} {'with ' + action[2] if action[1] == 'plant' else ''}", True, BLACK)
        screen.blit(action_text, (panel_rect.x + 40, panel_rect.y + 60 + i * 40))

    bot_plan_text = font.render(f"Bot ({selected_bot.capitalize()}) Plan:", True, BLACK)
    screen.blit(bot_plan_text, (panel_rect.x + 20, panel_rect.y + 160))
    for i, action in enumerate(bot_plan_steps):
        action_text = font.render(f"Step {i+1}: {action[1]} at {action[0]} {'with ' + action[2] if action[1] == 'plant' else ''}", True, BLACK)
        screen.blit(action_text, (panel_rect.x + 40, panel_rect.y + 200 + i * 40))

    mouse_pos = pygame.mouse.get_pos()
    if back_button_rect.collidepoint(mouse_pos):
        screen.blit(button_square_beige_pressed, (back_button_rect.x, back_button_rect.y))
    else:
        screen.blit(button_square_beige, (back_button_rect.x, back_button_rect.y))
    back_text = font.render("Back", True, BLACK)
    screen.blit(back_text, (back_button_rect.x + 20, back_button_rect.y + 10))

def update_bot():
    global bot_step_index, last_bot_action, bot_profit
    current_time = pygame.time.get_ticks()
    if bot_step_index < len(bot_plan_steps) and current_time - last_bot_action >= BOT_ACTION_INTERVAL:
        step = bot_plan_steps[bot_step_index]
        print(f"Step: {step}")
        
        if not isinstance(step, list) or len(step) < 2:
            print(f"Warning: Invalid step format {step}, skipping this step.")
            bot_step_index += 1
            last_bot_action = current_time
            return
        
        position = step[0]
        action = step[1]
        
        if not isinstance(position, (list, tuple)) or len(position) < 2:
            print(f"Warning: Invalid position format in step {step}, skipping this step.")
            bot_step_index += 1
            last_bot_action = current_time
            return
        
        i, j, *_ = position
        if action == "plant" and bot_grid[i][j] is None:
            if len(step) < 3:
                print(f"Warning: Invalid step format for 'plant' action {step}, skipping this step.")
                bot_step_index += 1
                last_bot_action = current_time
                return
            crop = step[2]
            if crop not in CROPS:
                print(f"Warning: Unknown crop {crop} in step {step}, skipping this step.")
                bot_step_index += 1
                last_bot_action = current_time
                return
            bot_grid[i][j] = crop
            bot_timers[i][j] = CROPS[crop]["time"]
            message = f"Bot planted {crop} at ({i}, {j})"
            bot_messages.append((message, current_time))
            pygame.draw.rect(screen, YELLOW, (BOT_GRID_OFFSET_X + j * CELL_SIZE, GRID_OFFSET_Y + i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
            pygame.display.flip()
            pygame.time.wait(200)
        elif action == "harvest" and bot_grid[i][j] is not None:
            crop = bot_grid[i][j]
            bot_profit += market_prices[crop]
            bot_grid[i][j] = None
            bot_timers[i][j] = 0
            harvested_crops.add(crop)
            message = f"Bot harvested at ({i}, {j}), profit now: {bot_profit}"
            bot_messages.append((message, current_time))
            pygame.draw.rect(screen, GREEN, (BOT_GRID_OFFSET_X + j * CELL_SIZE, GRID_OFFSET_Y + i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
            pygame.display.flip()
            pygame.time.wait(200)
        
        bot_step_index += 1
        last_bot_action = current_time

def update_market_prices():
    global market_prices
    for crop in market_prices:
        fluctuation = random.uniform(-0.3, 0.3)
        market_prices[crop] = max(0.5 * original_profits[crop], original_profits[crop] * (1 + fluctuation))

def main():
    global game_state, budget, day, profit, selected_crop, username, high_score
    global username_input, username_input_active, day_timer, last_day_update, remove_mode, water_mode, protect_mode, disrupt_mode
    global farm_grid, crop_timers, crop_protected, bot_profit, bot_grid, bot_timers, bot_step_index, last_bot_action
    global current_weather, next_weather, harvested_crops, player_plan, last_disrupt_time
    
    load_high_scores()
    reset_game()
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if game_state == MENU:
                    if play_button_rect.collidepoint(mouse_pos):
                        game_state = USERNAME_INPUT
                        username_input = ""
                        username_input_active = True
                        print("Switched to USERNAME_INPUT state")
                    elif guide_button_rect.collidepoint(mouse_pos):
                        game_state = GUIDE
                        print("Switched to GUIDE state")
                elif game_state == USERNAME_INPUT:
                    if username_input_rect.collidepoint(mouse_pos):
                        username_input_active = True
                    else:
                        username_input_active = False
                elif game_state == GUIDE:
                    if back_button_rect.collidepoint(mouse_pos):
                        game_state = MENU
                        print("Switched to MENU state")
                elif game_state == PLAY:
                    for idx, (crop_name, _) in enumerate(CROPS.items()):
                        button_rect = pygame.Rect(50 + idx * 120, 20, 100, 50)
                        if button_rect.collidepoint(mouse_pos):
                            selected_crop = crop_name
                            remove_mode = False
                            water_mode = False
                            protect_mode = False
                            disrupt_mode = False
                            print(f"Selected crop: {selected_crop}")
                            break
                    
                    if water_button_rect.collidepoint(mouse_pos):
                        water_mode = not water_mode
                        remove_mode = False
                        protect_mode = False
                        disrupt_mode = False
                        selected_crop = None
                        if water_mode:
                            print("Water mode activated")
                        else:
                            print("Water mode deactivated")
                        continue
                    
                    if remove_button_rect.collidepoint(mouse_pos):
                        remove_mode = not remove_mode
                        water_mode = False
                        protect_mode = False
                        disrupt_mode = False
                        selected_crop = None
                        if remove_mode:
                            print("Remove mode activated")
                        else:
                            print("Remove mode deactivated")
                        continue
                    
                    if protect_button_rect.collidepoint(mouse_pos):
                        protect_mode = not protect_mode
                        remove_mode = False
                        water_mode = False
                        disrupt_mode = False
                        selected_crop = None
                        if protect_mode:
                            print("Protect mode activated")
                        else:
                            print("Protect mode deactivated")
                        continue
                    
                    if disrupt_button_rect.collidepoint(mouse_pos):
                        current_time = pygame.time.get_ticks()
                        if current_time - last_disrupt_time >= DISRUPT_COOLDOWN:
                            disrupt_mode = not disrupt_mode
                            remove_mode = False
                            water_mode = False
                            protect_mode = False
                            selected_crop = None
                            if disrupt_mode:
                                print("Disrupt mode activated")
                            else:
                                print("Disrupt mode deactivated")
                            last_disrupt_time = current_time if disrupt_mode else 0
                        else:
                            message = f"Disrupt on cooldown! Wait {int((DISRUPT_COOLDOWN - (current_time - last_disrupt_time)) / 1000)}s"
                            bot_messages.append((message, current_time))
                        continue
                    
                    if finish_button_rect.collidepoint(mouse_pos):
                        if len(harvested_crops) == len(CROPS):
                            profit += DIVERSITY_BONUS
                            bot_profit += DIVERSITY_BONUS
                            message = f"Diversity bonus applied! +{DIVERSITY_BONUS} profit!"
                            bot_messages.append((message, pygame.time.get_ticks()))
                            pygame.draw.rect(screen, YELLOW, (WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50))
                            pygame.display.flip()
                            pygame.time.wait(500)
                        game_state = GAME_OVER
                        print("Player clicked Finish, game over")
                        if profit > high_score:
                            high_score = profit
                            high_scores[username]["high_score"] = high_score
                            save_high_scores()
                        continue
                    
                    for i in range(GRID_SIZE):
                        for j in range(GRID_SIZE):
                            cell_rect = pygame.Rect(GRID_OFFSET_X + j * CELL_SIZE, GRID_OFFSET_Y + i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                            if cell_rect.collidepoint(mouse_pos):
                                if remove_mode and farm_grid[i][j] is not None:
                                    crop_data = CROPS[farm_grid[i][j]]
                                    budget += crop_data["cost"]
                                    player_plan.append([[i, j], "remove", farm_grid[i][j]])
                                    farm_grid[i][j] = None
                                    crop_timers[i][j] = 0
                                    crop_protected[i][j] = False
                                    print(f"Removed crop at ({i}, {j}), refunded {crop_data['cost']}")
                                elif water_mode and farm_grid[i][j] is not None and budget >= 5:
                                    budget -= 5
                                    crop_timers[i][j] = max(1, crop_timers[i][j] - 1)
                                    player_plan.append([[i, j], "water"])
                                    print(f"Watered crop at ({i}, {j})")
                                elif protect_mode and farm_grid[i][j] is not None and not crop_protected[i][j] and budget >= 10:
                                    budget -= 10
                                    crop_protected[i][j] = True
                                    player_plan.append([[i, j], "protect"])
                                    print(f"Protected crop at ({i}, {j})")
                                elif selected_crop and farm_grid[i][j] is None:
                                    crop_data = CROPS[selected_crop]
                                    if budget >= crop_data["cost"]:
                                        budget -= crop_data["cost"]
                                        farm_grid[i][j] = selected_crop
                                        crop_timers[i][j] = crop_data["time"]
                                        player_plan.append([[i, j], "plant", selected_crop])
                                        print(f"Planted {selected_crop} at ({i}, {j})")
                            bot_cell_rect = pygame.Rect(BOT_GRID_OFFSET_X + j * CELL_SIZE, GRID_OFFSET_Y + i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                            if disrupt_mode and bot_cell_rect.collidepoint(mouse_pos) and bot_grid[i][j] is not None and budget >= 20:
                                budget -= 20
                                bot_timers[i][j] = min(10, bot_timers[i][j] + 1)
                                player_plan.append([[i, j], "disrupt"])
                                message = f"Player disrupted bot's crop at ({i}, {j})!"
                                bot_messages.append((message, pygame.time.get_ticks()))
                                print(message)
                elif game_state == GAME_OVER:
                    if back_to_menu_button_rect.collidepoint(mouse_pos):
                        game_state = MENU
                        print("Switched to MENU state")
                        reset_game()
                    elif view_plans_button_rect.collidepoint(mouse_pos):
                        game_state = VIEW_PLANS
                        print("Switched to VIEW_PLANS state")
                elif game_state == VIEW_PLANS:
                    if back_button_rect.collidepoint(mouse_pos):
                        game_state = GAME_OVER
                        print("Switched back to GAME_OVER state")
            if event.type == pygame.KEYDOWN:
                if game_state == USERNAME_INPUT and username_input_active:
                    if event.key == pygame.K_RETURN and username_input.strip():
                        username = username_input.strip()
                        if username in high_scores:
                            high_score = high_scores[username]["high_score"]
                        else:
                            high_score = 0
                            high_scores[username] = {"high_score": 0}
                        game_state = PLAY
                        last_day_update = pygame.time.get_ticks()
                        last_bot_action = pygame.time.get_ticks()
                        print(f"Switched to PLAY state with username: {username}")
                    elif event.key == pygame.K_BACKSPACE:
                        username_input = username_input[:-1]
                    elif event.unicode.isprintable():
                        username_input += event.unicode
        
        if game_state == PLAY:
            current_time = pygame.time.get_ticks()
            day_timer = current_time - last_day_update
            
            update_bot()
            
            if day_timer >= DAY_DURATION:
                current_weather = next_weather
                next_weather = random.choice(WEATHER_TYPES)
                print(f"Day {day}: Weather is {current_weather}, Tomorrow: {next_weather}")
                
                update_market_prices()
                print(f"Market prices updated: {market_prices}")
                
                apply_weather_effects(farm_grid, crop_timers, crop_protected)
                apply_weather_effects(bot_grid, bot_timers, [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)])
                
                for i in range(GRID_SIZE):
                    for j in range(GRID_SIZE):
                        if farm_grid[i][j] and crop_timers[i][j] > 0:
                            crop_timers[i][j] -= 1
                            if crop_timers[i][j] == 0:
                                crop = farm_grid[i][j]
                                profit += market_prices[crop]
                                if crop not in harvested_crops:
                                    budget += 5
                                    message = f"New crop harvested! +5 budget!"
                                    bot_messages.append((message, pygame.time.get_ticks()))
                                harvested_crops.add(crop)
                                player_plan.append([[i, j], "harvest"])
                                farm_grid[i][j] = None
                                crop_protected[i][j] = False
                                print(f"Player harvested at ({i}, {j}), profit now: {profit}")
                        if bot_grid[i][j] and bot_timers[i][j] > 0:
                            bot_timers[i][j] -= 1
                            if bot_timers[i][j] == 0:
                                crop = bot_grid[i][j]
                                bot_profit += market_prices[crop]
                                harvested_crops.add(crop)
                                bot_grid[i][j] = None
                                print(f"Bot harvested at ({i}, {j}), profit now: {bot_profit}")
                
                if day < MAX_DAYS:
                    day += 1
                    last_day_update = current_time
                    day_timer = 0
                    print(f"Day updated to: {day}")
                else:
                    if len(harvested_crops) == len(CROPS):
                        profit += DIVERSITY_BONUS
                        bot_profit += DIVERSITY_BONUS
                        message = f"Diversity bonus applied! +{DIVERSITY_BONUS} profit!"
                        bot_messages.append((message, pygame.time.get_ticks()))
                    if profit > high_score:
                        high_score = profit
                        high_scores[username]["high_score"] = high_score
                        save_high_scores()
                    game_state = GAME_OVER
                    print("Game Over")
        
        screen.fill(BLACK)
        if game_state == MENU:
            draw_menu()
        elif game_state == USERNAME_INPUT:
            draw_username_input()
        elif game_state == GUIDE:
            draw_guide()
        elif game_state == PLAY:
            draw_play()
        elif game_state == GAME_OVER:
            draw_game_over()
        elif game_state == VIEW_PLANS:
            draw_view_plans()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()