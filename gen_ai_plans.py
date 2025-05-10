import json
import random
import copy  # Thêm import copy để sử dụng deepcopy
from itertools import product
from tqdm import tqdm
import math

# Game constants
GRID_SIZE = 5
DAYS = 7  # Giảm từ 10 xuống 5
BUDGETS = [150]
DIVERSITY_BONUS = 20
MAX_ACTIONS = 10
NUM_WEATHER_SCENARIOS = 100  # Giảm từ 100 xuống 10

# Crop data
BASE_CROPS = {
    "rice": {"cost": 10, "time": 2, "profit": 25},
    "corn": {"cost": 15, "time": 2, "profit": 35},
    "tomato": {"cost": 20, "time": 4, "profit": 50},
}

WEATHER_TYPES = ["Sunny", "Rainy", "Dry"]
WEATHER_PROB = 1/3

def generate_weather_scenario():
    return [random.choice(WEATHER_TYPES) for _ in range(DAYS)]

def apply_weather_effects(crop, weather, day, remaining_days):
    base_time = BASE_CROPS[crop]["time"]
    time_reduction = 0
    fail_chance = 0
    if crop == "rice":
        if weather == "Rainy": time_reduction = 1
        elif weather == "Dry": fail_chance = 0.5
    elif crop == "corn":
        if weather == "Dry": time_reduction = 1
    elif crop == "tomato":
        if weather == "Sunny": time_reduction = 1
        elif weather == "Rainy": fail_chance = 0.5
    effective_time = max(1, base_time - time_reduction)
    if remaining_days < effective_time: return 0, effective_time, fail_chance
    return effective_time, effective_time, fail_chance

def apply_crop_abilities(crop, grid, i, j, weather, day, weather_history, profit):
    bonus = 0
    if crop == "rice":
        adjacent_rice = sum(1 for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]
                           if 0 <= i + di < GRID_SIZE and 0 <= j + dj < GRID_SIZE and grid[i + di][j + dj] == "rice")
        if adjacent_rice >= 2: bonus += 10
    elif crop == "corn":
        if day >= 2 and weather_history[day-1] == "Dry" and weather_history[day-2] == "Dry": bonus += 15
    elif crop == "tomato":
        if weather == "Sunny": bonus += 20
    return profit + bonus

def apply_market_prices(crop, day, harvest_history):
    market_multiplier = random.uniform(0.8, 1.2)
    if day > 0:
        crop_count = harvest_history[day-1].get(crop, 0)
        supply_factor = max(0.7, min(1.3, 1.0 - 0.05 * crop_count))
        market_multiplier *= supply_factor
    return BASE_CROPS[crop]["profit"] * market_multiplier

def score_position(grid, i, j, crop, weather_scenarios, t):
    score = 0
    if crop == "rice":
        score += sum(1 for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]
                    if 0 <= i + di < GRID_SIZE and 0 <= j + dj < GRID_SIZE and
                    (grid[i + di][j + dj] is None or grid[i + di][j + dj] == "rice")) * 10
    elif crop == "tomato":
        expected_harvest_day = t + BASE_CROPS[crop]["time"]
        if expected_harvest_day < DAYS:
            score += (sum(1 for scenario in weather_scenarios if scenario[expected_harvest_day] == "Sunny") / len(weather_scenarios)) * 20
    elif crop == "corn":
        expected_harvest_day = t + BASE_CROPS[crop]["time"]
        if expected_harvest_day < DAYS and expected_harvest_day >= 2:
            score += (sum(1 for scenario in weather_scenarios if scenario[expected_harvest_day-1] == "Dry" and scenario[expected_harvest_day-2] == "Dry") / len(weather_scenarios)) * 15
    min_dist = min((math.sqrt((i - pi)**2 + (j - pj)**2) for pi in range(GRID_SIZE) for pj in range(GRID_SIZE) if grid[pi][pj] is not None), default=float('inf'))
    score += min_dist
    return score

def simulate_plan(plan, weather_scenario):
    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    timers = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    harvested_crops = set()
    profit = 0
    harvest_history = [{} for _ in range(DAYS)]
    budget = BUDGETS[0]
    for t in range(DAYS):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if grid[i][j]: timers[i][j] = max(0, timers[i][j] - 1)
        for action in plan:
            if action[1] == "plant":
                i, j = action[0]
                crop = action[2]
                if grid[i][j] is None and budget >= BASE_CROPS[crop]["cost"]:
                    effective_time, _, fail_chance = apply_weather_effects(crop, weather_scenario[t], t, DAYS - t)
                    grid[i][j] = crop
                    timers[i][j] = effective_time
                    budget -= BASE_CROPS[crop]["cost"]
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if grid[i][j] and timers[i][j] <= 0:
                    crop = grid[i][j]
                    _, _, fail_chance = apply_weather_effects(crop, weather_scenario[t], t, DAYS - t)
                    if random.random() < fail_chance: continue
                    profit += apply_crop_abilities(crop, grid, i, j, weather_scenario[t], t, weather_scenario[:t+1], apply_market_prices(crop, t, harvest_history))
                    harvested_crops.add(crop)
                    harvest_history[t][crop] = harvest_history[t].get(crop, 0) + 1
                    grid[i][j] = None
                    timers[i][j] = 0
    if len(harvested_crops) == len(BASE_CROPS): profit += DIVERSITY_BONUS
    return profit

def estimate_upper_bound(t, grid, harvested_crops, remaining_budget, scenario):
    current_profit = 0
    temp_grid, temp_timers = copy.deepcopy(grid), [[BASE_CROPS[g]["time"] if g else 0 for g in row] for row in grid]
    for day in range(t, DAYS):
        weather = scenario[day]
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if temp_grid[i][j]:
                    if weather in [("Sunny", "tomato"), ("Rainy", "rice"), ("Dry", "corn")][{"Sunny": 0, "Rainy": 1, "Dry": 2}[weather] % 3]:
                        temp_timers[i][j] -= 1
                    temp_timers[i][j] = max(0, temp_timers[i][j] - 1)
                    if temp_timers[i][j] <= 0:
                        current_profit += BASE_CROPS[temp_grid[i][j]]["profit"]
                        temp_grid[i][j] = None
    empty_cells = sum(row.count(None) for row in grid)
    best_crop = max(BASE_CROPS, key=lambda c: BASE_CROPS[c]["profit"] / BASE_CROPS[c]["time"] if remaining_budget >= BASE_CROPS[c]["cost"] else 0)
    if best_crop:
        max_plants = min(empty_cells, remaining_budget // BASE_CROPS[best_crop]["cost"])
        current_profit += max_plants * BASE_CROPS[best_crop]["profit"]
    if len(harvested_crops) + (1 if best_crop else 0) >= len(BASE_CROPS): current_profit += DIVERSITY_BONUS
    return current_profit

def generate_greedy_plan(budget, weather_scenarios):
    plan = []
    remaining_budget = budget
    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    timers = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    harvested_crops = set()
    action_count = 0
    positions = list(product(range(GRID_SIZE), range(GRID_SIZE)))
    random.shuffle(positions)
    pos_idx = 0
    for crop in BASE_CROPS:
        if pos_idx >= len(positions) or action_count >= MAX_ACTIONS: break
        i, j = positions[pos_idx]
        if remaining_budget >= BASE_CROPS[crop]["cost"]:
            plan.append([[i, j], "plant", crop])
            grid[i][j] = crop
            timers[i][j] = BASE_CROPS[crop]["time"]
            remaining_budget -= BASE_CROPS[crop]["cost"]
            pos_idx += 1
            action_count += 1
    for t in range(DAYS):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if grid[i][j] and timers[i][j] <= 0 and action_count < MAX_ACTIONS:
                    plan.append([[i, j], "harvest"])
                    harvested_crops.add(grid[i][j])
                    grid[i][j] = None
                    timers[i][j] = 0
                    action_count += 1
        available_positions = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] is None]
        if available_positions and action_count < MAX_ACTIONS:
            best_crop = max(BASE_CROPS, key=lambda c: BASE_CROPS[c]["profit"] / BASE_CROPS[c]["time"] if remaining_budget >= BASE_CROPS[c]["cost"] else 0)
            if remaining_budget >= BASE_CROPS[best_crop]["cost"] and t + BASE_CROPS[best_crop]["time"] <= DAYS:
                i, j = max(available_positions, key=lambda pos: score_position(grid, pos[0], pos[1], best_crop, weather_scenarios, t))
                plan.append([[i, j], "plant", best_crop])
                grid[i][j] = best_crop
                timers[i][j] = BASE_CROPS[best_crop]["time"]
                remaining_budget -= BASE_CROPS[best_crop]["cost"]
                action_count += 1
    return plan, sum(simulate_plan(plan, scenario) for scenario in weather_scenarios) / len(weather_scenarios)

def generate_backtracking_plan(budget, weather_scenarios):
    best_plan, best_avg_profit = [], float('-inf')
    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    timers = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    harvested_crops = set()
    action_count = [0]
    def backtrack(t, budget_left, plan):
        nonlocal best_plan, best_avg_profit
        if t >= DAYS or action_count[0] >= MAX_ACTIONS:
            avg_profit = sum(simulate_plan(plan, scenario) for scenario in weather_scenarios) / len(weather_scenarios)
            if avg_profit > best_avg_profit: best_plan, best_avg_profit = plan[:], avg_profit
            return
        upper_bound = estimate_upper_bound(t, grid, harvested_crops, budget_left, weather_scenarios[0])
        if upper_bound <= best_avg_profit: return
        current_plan, current_grid, current_timers, current_harvested = plan[:], [row[:] for row in grid], [row[:] for row in timers], harvested_crops.copy()
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if current_grid[i][j] and current_timers[i][j] <= t and action_count[0] < MAX_ACTIONS:
                    current_plan.append([[i, j], "harvest"])
                    current_harvested.add(current_grid[i][j])
                    current_grid[i][j] = None
                    current_timers[i][j] = 0
                    action_count[0] += 1
        available_positions = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if current_grid[i][j] is None]
        if available_positions and action_count[0] < MAX_ACTIONS:
            for crop in BASE_CROPS:
                cost = BASE_CROPS[crop]["cost"]
                if budget_left >= cost and t + BASE_CROPS[crop]["time"] <= DAYS:
                    i, j = max(available_positions, key=lambda pos: score_position(current_grid, pos[0], pos[1], crop, weather_scenarios, t))
                    current_plan.append([[i, j], "plant", crop])
                    current_grid[i][j] = crop
                    current_timers[i][j] = BASE_CROPS[crop]["time"]
                    action_count[0] += 1
                    backtrack(t + 1, budget_left - cost, current_plan)
                    current_grid[i][j] = None
                    current_timers[i][j] = 0
                    action_count[0] -= 1
        backtrack(t + 1, budget_left, current_plan)
    backtrack(0, budget, [])
    return best_plan, best_avg_profit

def generate_dp_plan(budget, weather_scenarios):
    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    timers = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    plan = []
    remaining_budget = budget
    harvested_crops = set()
    action_count = [0]
    positions = list(product(range(GRID_SIZE), range(GRID_SIZE)))
    random.shuffle(positions)
    pos_idx = 0
    for crop in BASE_CROPS:
        if pos_idx >= len(positions) or action_count[0] >= MAX_ACTIONS: break
        i, j = positions[pos_idx]
        if remaining_budget >= BASE_CROPS[crop]["cost"]:
            plan.append([[i, j], "plant", crop])
            grid[i][j] = crop
            timers[i][j] = BASE_CROPS[crop]["time"]
            remaining_budget -= BASE_CROPS[crop]["cost"]
            pos_idx += 1
            action_count[0] += 1
    dp = {}
    def dp_solve(t, budget_left):
        if t >= DAYS or action_count[0] >= MAX_ACTIONS:
            return sum(simulate_plan(plan, scenario) for scenario in weather_scenarios) / len(weather_scenarios), []
        state = (t, budget_left)
        if state in dp: return dp[state]
        best_profit, best_subplan = float('-inf'), []
        current_grid, current_timers, current_harvested = [row[:] for row in grid], [row[:] for row in timers], harvested_crops.copy()
        subplan = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if current_grid[i][j] and current_timers[i][j] <= t and action_count[0] < MAX_ACTIONS:
                    subplan.append([[i, j], "harvest"])
                    current_harvested.add(current_grid[i][j])
                    current_grid[i][j] = None
                    current_timers[i][j] = 0
                    action_count[0] += 1
        available_positions = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if current_grid[i][j] is None]
        if available_positions and action_count[0] < MAX_ACTIONS:
            for crop in BASE_CROPS:
                cost = BASE_CROPS[crop]["cost"]
                if budget_left >= cost and t + BASE_CROPS[crop]["time"] <= DAYS:
                    i, j = max(available_positions, key=lambda pos: score_position(current_grid, pos[0], pos[1], crop, weather_scenarios, t))
                    current_grid[i][j] = crop
                    current_timers[i][j] = BASE_CROPS[crop]["time"]
                    action_count[0] += 1
                    subplan_with_plant = subplan + [[[i, j], "plant", crop]]
                    future_profit, future_plan = dp_solve(t + 1, budget_left - cost)
                    if future_profit > best_profit:
                        best_profit, best_subplan = future_profit, subplan_with_plant + future_plan
                    current_grid[i][j] = None
                    current_timers[i][j] = 0
                    action_count[0] -= 1
        future_profit, future_plan = dp_solve(t + 1, budget_left)
        if future_profit > best_profit: best_profit, best_subplan = future_profit, subplan + future_plan
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                grid[i][j], timers[i][j] = current_grid[i][j], current_timers[i][j]
        dp[state] = (best_profit, best_subplan)
        return dp[state]
    _, additional_plan = dp_solve(0, remaining_budget)
    plan.extend(additional_plan)
    for step in plan:
        if step[1] == "harvest":
            i, j = step[0]
            for prev_step in plan:
                if prev_step[1] == "plant" and prev_step[0] == [i, j]:
                    harvested_crops.add(prev_step[2])
                    break
    return plan, sum(simulate_plan(plan, scenario) for scenario in weather_scenarios) / len(weather_scenarios)

def generate_config():
    budget = random.choice(BUDGETS)
    weather_scenarios = [generate_weather_scenario() for _ in range(NUM_WEATHER_SCENARIOS)]
    greedy_plan, greedy_profit = generate_greedy_plan(budget, weather_scenarios)
    backtracking_plan, backtracking_profit = generate_backtracking_plan(budget, weather_scenarios)
    dp_plan, dp_profit = generate_dp_plan(budget, weather_scenarios)
    return {"budget": budget, "ai_plans": {"greedy": greedy_plan, "backtracking": backtracking_plan, "dp": dp_plan}, "ai_profits": {"greedy": greedy_profit, "backtracking": backtracking_profit, "dp": dp_profit}}

def main():
    num_configs = int(input("Nhập số lượng cấu hình cần tạo: "))
    configs = [generate_config() for _ in tqdm(range(num_configs), desc="Đang tạo cấu hình")]
    with open("ai_plans.json", "w") as f: json.dump(configs, f, indent=4)
    print(f"Đã tạo {num_configs} cấu hình và lưu vào ai_plans.json")

if __name__ == "__main__":
    main()