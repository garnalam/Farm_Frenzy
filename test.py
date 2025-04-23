import pygame
import json
import os
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 5  # 5x5 grid for farm
CELL_SIZE = 50  # Size of each cell in the grid
GRID_OFFSET_X = 50
GRID_OFFSET_Y = 100
BOT_GRID_OFFSET_X = WIDTH // 2 + 50  # Bot's farm on the right

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
DAY_DURATION = 11 * 1000  # 11 seconds per day
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
BOT_ACTION_INTERVAL = 10000  # 10 seconds per bot action
bot_messages = []
BOT_MESSAGE_DURATION = 5000  # Display each message for 5 seconds

# Weather system
WEATHER_TYPES = ["Sunny", "Rainy", "Dry"]
current_weather = "Sunny"  # Default weather

# Crop diversity tracking
harvested_crops = set()  # Track which crops have been harvested
DIVERSITY_BONUS = 20  # Bonus for harvesting all crop types

# Crops data (balanced)
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
        "time": 2,  # Reduced from 3 to make it more competitive
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
}

# Farm grid (5x5) for player
farm_grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
crop_timers = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Buttons
play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
guide_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
back_button_rect = pygame.Rect(50, HEIGHT - 70, 100, 50)
play_again_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
finish_button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 70, 100, 50)
remove_button_rect = pygame.Rect(50 + 3 * 120, 20, 100, 50)

# Crop selection and remove mode
selected_crop = None
remove_mode = False

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
    global all_configs, selected_config, budget, ai_plans, ai_profits, selected_bot, bot_plan_steps, bot_step_index
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
    global farm_grid, crop_timers, selected_crop, remove_mode
    global bot_profit, bot_grid, bot_timers, bot_step_index, last_bot_action, previous_config, bot_messages
    global current_weather, harvested_crops
    username = ""
    high_score = 0
    budget = 100
    day = 1
    profit = 0
    day_timer = 0
    last_day_update = 0
    farm_grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    crop_timers = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    selected_crop = None
    remove_mode = False
    bot_profit = 0
    bot_grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    bot_timers = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    bot_step_index = 0
    last_bot_action = 0
    bot_messages = []
    current_weather = "Sunny"
    harvested_crops = set()
    previous_config = selected_config
    setup()

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
        "1. Click on a grid cell to select it.",
        "2. Choose a crop to plant: Rice (10 cost, 2 days, 25 profit),",
        "   Corn (15 cost, 2 days, 35 profit), Tomato (20 cost, 4 days, 50 profit).",
        f"3. You have {budget} budget and 10 days to maximize profit.",
        "4. Each day lasts 11 seconds.",
        "5. Weather affects crops: Sunny (Tomato +1 speed),",
        "   Rainy (Rice +1 speed, Tomato 50% fail), Dry (Corn +1 speed, Rice 50% fail).",
        "6. Harvest all crop types for a +20 profit bonus.",
        "7. You can remove planted crops to get a refund.",
        "8. Compete against a bot (Backtracking, DP, or Greedy).",
        "9. Bot's actions are shown every 10 seconds.",
        "10. Click Finish to end early and see results."
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

def apply_weather_effects(grid, timers):
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
                    elif crop == "tomato":
                        fail_chance = 0.5
                elif current_weather == "Dry":
                    if crop == "corn":
                        time_reduction = 1
                    elif crop == "rice":
                        fail_chance = 0.5
                
                # Apply crop failure
                if fail_chance > 0 and random.random() < fail_chance:
                    grid[i][j] = None
                    timers[i][j] = 0
                    message = f"{'Bot' if grid is bot_grid else 'Player'}'s {crop} at ({i}, {j}) failed due to {current_weather} weather!"
                    print(message)
                    bot_messages.append((message, pygame.time.get_ticks()))
                    continue
                
                # Apply time reduction
                if time_reduction > 0 and timers[i][j] > 0:
                    timers[i][j] = max(1, timers[i][j] - time_reduction)  # Ensure timer doesn't go below 1

def draw_grid(grid, timers, offset_x, hide_crops=False):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell_rect = pygame.Rect(
                offset_x + j * CELL_SIZE,
                GRID_OFFSET_Y + i * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
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

# Ở phần khai báo biến toàn cục (gần đầu file test.py)
# Các khai báo khác như WIDTH, HEIGHT, GRID_OFFSET_X, v.v. đã có sẵn
finish_button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 210, 100, 50)  # Đã sửa trước đó
weather_rect = pygame.Rect((50 + 700) // 2 - 80, 360, 160, 40)  # Thêm khai báo weather_rect: căn giữa và dưới bản đồ

# Hàm draw_play() đã được sửa
def draw_play():
    print("Drawing play screen...")
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(GREEN)
    
    # Draw farms
    draw_grid(farm_grid, crop_timers, GRID_OFFSET_X, hide_crops=False)
    draw_grid(bot_grid, bot_timers, BOT_GRID_OFFSET_X, hide_crops=False)
    
    # Farm labels
    player_label = font.render("Your Farm", True, BLACK)
    bot_label = font.render(f"Bot ({selected_bot.capitalize()})", True, BLACK)
    screen.blit(player_label, (GRID_OFFSET_X, GRID_OFFSET_Y - 30))
    screen.blit(bot_label, (BOT_GRID_OFFSET_X, GRID_OFFSET_Y - 30))
    
    # Calculate time
    remaining_time = max(0, (DAY_DURATION - day_timer) // 1000)
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    timer_display = f"Time: {minutes:02d}:{seconds:02d}"
    
    # Day and Time (Top-right)
    day_rect = pygame.Rect(WIDTH - 180, 20, 160, 60)
    screen.blit(stats_panel, (day_rect.x, day_rect.y), (0, 0, 160, 60))
    day_text = font.render(f"Day: {day}/{MAX_DAYS}", True, BLACK)
    time_text = font.render(timer_display, True, BLACK)
    screen.blit(day_text, (day_rect.x + 10, day_rect.y + 10))
    screen.blit(time_text, (day_rect.x + 10, day_rect.y + 35))
    
    # Budget, Profit, High Score, Bot Profit (Bottom-right)
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
    
    # Weather (Now using global weather_rect, positioned below and centered)
    screen.blit(stats_panel, (weather_rect.x, weather_rect.y), (0, 0, 160, 40))
    weather_text = font.render(f"Weather: {current_weather}", True, BLACK)
    # Căn giữa văn bản trong khung
    text_rect = weather_text.get_rect(center=(weather_rect.x + weather_rect.width // 2, weather_rect.y + weather_rect.height // 2))
    screen.blit(weather_text, text_rect)
    
    # Diversity (Bottom-left, near "Your Farm")
    diversity_rect = pygame.Rect(50, HEIGHT - 100, 160, 30)
    screen.blit(stats_panel, (diversity_rect.x, diversity_rect.y), (0, 0, 160, 30))
    diversity_text = font.render(f"Diversity: {len(harvested_crops)}/3", True, BLACK)
    screen.blit(diversity_text, (diversity_rect.x + 10, diversity_rect.y + 5))
    
    # Crop buttons
    mouse_pos = pygame.mouse.get_pos()
    for idx, (crop_name, _) in enumerate(CROPS.items()):
        button_rect = pygame.Rect(50 + idx * 120, 20, 100, 50)
        if button_rect.collidepoint(mouse_pos):
            screen.blit(button_square_beige_pressed, (button_rect.x, button_rect.y))
        else:
            if selected_crop == crop_name and not remove_mode:
                screen.blit(button_square_beige_pressed, (button_rect.x, button_rect.y))
            else:
                screen.blit(button_square_beige, (button_rect.x, button_rect.y))
        text = font.render(crop_name.capitalize(), True, BLACK)
        screen.blit(text, (button_rect.x + 10, button_rect.y + 10))
    
    # Remove button
    if remove_button_rect.collidepoint(mouse_pos):
        screen.blit(button_square_beige_pressed, (remove_button_rect.x, remove_button_rect.y))
    else:
        if remove_mode:
            screen.blit(button_square_beige_pressed, (remove_button_rect.x, remove_button_rect.y))
        else:
            screen.blit(button_square_beige, (remove_button_rect.x, remove_button_rect.y))
    remove_text = font.render("Remove", True, BLACK)
    screen.blit(remove_text, (remove_button_rect.x + 10, remove_button_rect.y + 10))
    
    # Finish button
    if finish_button_rect.collidepoint(mouse_pos):
        screen.blit(button_square_beige_pressed, (finish_button_rect.x, finish_button_rect.y))
    else:
        screen.blit(button_square_beige, (finish_button_rect.x, finish_button_rect.y))
    finish_text = font.render("Finish", True, BLACK)
    screen.blit(finish_text, (finish_button_rect.x + 20, finish_button_rect.y + 10))
    
    # Bot messages
    current_time = pygame.time.get_ticks()
    bot_messages[:] = [msg for msg in bot_messages if current_time - msg[1] < BOT_MESSAGE_DURATION]
    for i, (message, _) in enumerate(bot_messages[-3:]):
        text = font.render(message, True, BLACK)
        screen.blit(text, (50, HEIGHT - 150 + i * 30))

def draw_game_over():
    print("Drawing game over screen...")
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(GREEN)

    # Game Over panel
    panel_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 200)
    screen.blit(stats_panel, (panel_rect.x, panel_rect.y), (0, 0, 300, 200))

    # Game Over text
    game_over_text = font.render("Game Over!", True, BLACK)
    profit_text = font.render(f"Your Profit: {profit}", True, BLACK)
    high_score_text = font.render(f"Your High Score: {high_score}", True, BLACK)
    bot_profit_text = font.render(f"Bot Profit: {bot_profit}", True, BLACK)
    bot_plan_text = font.render(f"Bot Plan: {selected_bot.capitalize()}", True, BLACK)

    # Thêm thông báo thắng/thua
    if profit > bot_profit:
        result_text = font.render("You Win!", True, BLACK)
    elif profit < bot_profit:
        result_text = font.render("You Lose!", True, BLACK)
    else:
        result_text = font.render("It's a Tie!", True, BLACK)

    # Vị trí các dòng văn bản
    screen.blit(game_over_text, (panel_rect.x + 90, panel_rect.y + 20))
    screen.blit(profit_text, (panel_rect.x + 20, panel_rect.y + 50))
    screen.blit(high_score_text, (panel_rect.x + 20, panel_rect.y + 80))
    screen.blit(bot_profit_text, (panel_rect.x + 20, panel_rect.y + 110))
    screen.blit(bot_plan_text, (panel_rect.x + 20, panel_rect.y + 140))
    screen.blit(result_text, (panel_rect.x + 90, panel_rect.y + 170))  # Thêm dòng kết quả

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
        print(f"Position: {position}")
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
            print(message)
            bot_messages.append((message, current_time))
        elif action == "harvest" and bot_grid[i][j] is not None:
            crop = bot_grid[i][j]
            bot_profit += CROPS[crop]["profit"]
            bot_grid[i][j] = None
            bot_timers[i][j] = 0
            harvested_crops.add(crop)  # Track harvested crop type
            message = f"Bot harvested at ({i}, {j}), profit now: {bot_profit}"
            print(message)
            bot_messages.append((message, current_time))
        
        bot_step_index += 1
        last_bot_action = current_time

def main():
    global game_state, budget, day, profit, selected_crop, username, high_score
    global username_input, username_input_active, day_timer, last_day_update, remove_mode
    global farm_grid, crop_timers, bot_profit, bot_grid, bot_timers, bot_step_index, last_bot_action
    global current_weather, harvested_crops
    
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
                            print(f"Selected crop: {selected_crop}")
                            break
                    
                    if remove_button_rect.collidepoint(mouse_pos):
                        remove_mode = not remove_mode
                        if remove_mode:
                            selected_crop = None
                            print("Remove mode activated")
                        else:
                            print("Remove mode deactivated")
                        continue
                    
                    if finish_button_rect.collidepoint(mouse_pos):
                        # Apply diversity bonus if all crops harvested
                        if len(harvested_crops) == len(CROPS):
                            profit += DIVERSITY_BONUS
                            bot_profit += DIVERSITY_BONUS
                            print(f"Diversity bonus applied! Player profit: {profit}, Bot profit: {bot_profit}")
                        game_state = GAME_OVER
                        print("Player clicked Finish, game over")
                        if profit > high_score:
                            high_score = profit
                            high_scores[username]["high_score"] = high_score
                            save_high_scores()
                        continue
                    
                    for i in range(GRID_SIZE):
                        for j in range(GRID_SIZE):
                            cell_rect = pygame.Rect(
                                GRID_OFFSET_X + j * CELL_SIZE,
                                GRID_OFFSET_Y + i * CELL_SIZE,
                                CELL_SIZE,
                                CELL_SIZE
                            )
                            if cell_rect.collidepoint(mouse_pos):
                                if remove_mode and farm_grid[i][j] is not None:
                                    crop_data = CROPS[farm_grid[i][j]]
                                    budget += crop_data["cost"]
                                    farm_grid[i][j] = None
                                    crop_timers[i][j] = 0
                                    print(f"Removed crop at ({i}, {j}), refunded {crop_data['cost']}")
                                elif selected_crop and farm_grid[i][j] is None:
                                    crop_data = CROPS[selected_crop]
                                    if budget >= crop_data["cost"]:
                                        budget -= crop_data["cost"]
                                        farm_grid[i][j] = selected_crop
                                        crop_timers[i][j] = crop_data["time"]
                                        print(f"Planted {selected_crop} at ({i}, {j})")
                elif game_state == GAME_OVER:
                    if play_again_button_rect.collidepoint(mouse_pos):
                        game_state = MENU
                        print("Switched to MENU state")
                        reset_game()
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
                # Update weather at the start of the day
                current_weather = random.choice(WEATHER_TYPES)
                print(f"Day {day}: Weather is {current_weather}")
                
                # Apply weather effects
                apply_weather_effects(farm_grid, crop_timers)
                apply_weather_effects(bot_grid, bot_timers)
                
                # Update crop timers
                for i in range(GRID_SIZE):
                    for j in range(GRID_SIZE):
                        if farm_grid[i][j] and crop_timers[i][j] > 0:
                            crop_timers[i][j] -= 1
                            if crop_timers[i][j] == 0:
                                crop = farm_grid[i][j]
                                profit += CROPS[crop]["profit"]
                                harvested_crops.add(crop)  # Track harvested crop type
                                farm_grid[i][j] = None
                                print(f"Player harvested at ({i}, {j}), profit now: {profit}")
                        if bot_grid[i][j] and bot_timers[i][j] > 0:
                            bot_timers[i][j] -= 1
                            if bot_timers[i][j] == 0:
                                crop = bot_grid[i][j]
                                bot_profit += CROPS[crop]["profit"]
                                harvested_crops.add(crop)  # Track harvested crop type
                                bot_grid[i][j] = None
                                print(f"Bot harvested at ({i}, {j}), profit now: {bot_profit}")
                
                if day < MAX_DAYS:
                    day += 1
                    last_day_update = current_time
                    day_timer = 0
                    print(f"Day updated to: {day}")
                else:
                    # Apply diversity bonus if all crops harvested
                    if len(harvested_crops) == len(CROPS):
                        profit += DIVERSITY_BONUS
                        bot_profit += DIVERSITY_BONUS
                        print(f"Diversity bonus applied! Player profit: {profit}, Bot profit: {bot_profit}")
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
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()