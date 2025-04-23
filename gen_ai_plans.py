import json
import random
from itertools import product
from tqdm import tqdm
import math
import copy

# Game constants
GRID_SIZE = 5  # 5x5 grid
DAYS = 10  # Total days
BUDGETS = [150]  # Budget options for configurations
DIVERSITY_BONUS = 20  # Bonus for harvesting all crop types
MAX_ACTIONS = 10  # Limit actions to match bot's 1 action/day (10 days)
NUM_WEATHER_SCENARIOS = 100  # Number of weather scenarios to simulate

# Crop data (base values before weather effects or market prices)
BASE_CROPS = {
    "rice": {"cost": 10, "time": 2, "profit": 25},
    "corn": {"cost": 15, "time": 2, "profit": 35},
    "tomato": {"cost": 20, "time": 4, "profit": 50},
}

# Weather types and probabilities
WEATHER_TYPES = ["Sunny", "Rainy", "Dry"]
WEATHER_PROB = 1/3  # 33.3% chance for each weather type

def generate_weather_scenario():
    return [random.choice(WEATHER_TYPES) for _ in range(DAYS)]

def apply_weather_effects(crop, weather, day, remaining_days):
    base_time = BASE_CROPS[crop]["time"]
    time_reduction = 0
    fail_chance = 0
    
    if crop == "rice":
        if weather == "Rainy":
            time_reduction = 1
        elif weather == "Dry":
            fail_chance = 0.5
    elif crop == "corn":
        if weather == "Dry":
            time_reduction = 1
    elif crop == "tomato":
        if weather == "Sunny":
            time_reduction = 1
        elif weather == "Rainy":
            fail_chance = 0.5
    
    effective_time = max(1, base_time - time_reduction)
    if remaining_days < effective_time:
        return 0, effective_time, fail_chance
    return effective_time, effective_time, fail_chance

def apply_crop_abilities(crop, grid, i, j, weather, day, weather_history, profit):
    bonus = 0
    if crop == "rice":
        adjacent_rice = 0
        for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE and grid[ni][nj] == "rice":
                adjacent_rice += 1
        if adjacent_rice >= 2:
            bonus += 10
    
    elif crop == "corn":
        if day >= 2 and weather_history[day-1] == "Dry" and weather_history[day-2] == "Dry":
            bonus += 15
    
    elif crop == "tomato":
        if weather == "Sunny":
            bonus += 20
    
    return profit + bonus

def apply_market_prices(crop, day, harvest_history):
    market_multiplier = random.uniform(0.8, 1.2)
    if day > 0:
        prev_day_harvest = harvest_history[day-1]
        crop_count = prev_day_harvest.get(crop, 0)
        supply_factor = 1.0 - 0.05 * crop_count
        supply_factor = max(0.7, min(1.3, supply_factor))
        market_multiplier *= supply_factor
    
    profit = BASE_CROPS[crop]["profit"]
    return profit * market_multiplier

def score_position(grid, i, j, crop, weather_scenarios, t):
    score = 0
    if crop == "rice":
        # Prioritize positions with many empty or rice-filled adjacent cells
        adjacent_empty_or_rice = 0
        for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                if grid[ni][nj] is None or grid[ni][nj] == "rice":
                    adjacent_empty_or_rice += 1
        score += adjacent_empty_or_rice * 10  # Encourage clustering for rice
    
    elif crop == "tomato":
        # Prioritize positions where harvest might occur on a Sunny day
        expected_harvest_day = t + BASE_CROPS[crop]["time"]
        if expected_harvest_day < DAYS:
            sunny_count = sum(1 for scenario in weather_scenarios if scenario[expected_harvest_day] == "Sunny")
            sunny_prob = sunny_count / len(weather_scenarios)
            score += sunny_prob * 20  # Bonus for likely Sunny harvest
    
    elif crop == "corn":
        # Prioritize positions where harvest might occur after consecutive Dry days
        expected_harvest_day = t + BASE_CROPS[crop]["time"]
        if expected_harvest_day < DAYS and expected_harvest_day >= 2:
            dry_streak_count = 0
            for scenario in weather_scenarios:
                if scenario[expected_harvest_day-1] == "Dry" and scenario[expected_harvest_day-2] == "Dry":
                    dry_streak_count += 1
            dry_prob = dry_streak_count / len(weather_scenarios)
            score += dry_prob * 15  # Bonus for likely Dry streak
    
    # Add a distribution factor: prefer positions far from other planted crops
    min_dist = float('inf')
    for pi in range(GRID_SIZE):
        for pj in range(GRID_SIZE):
            if grid[pi][pj] is not None:
                dist = math.sqrt((i - pi)**2 + (j - pj)**2)
                min_dist = min(min_dist, dist)
    score += min_dist  # Encourage spreading out
    
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
                if grid[i][j]:
                    timers[i][j] = max(0, timers[i][j] - 1)
        
        # Process plan actions for this day
        for action in plan:
            if action[1] == "plant":
                i, j = action[0]
                crop = action[2]
                if grid[i][j] is None:
                    cost = BASE_CROPS[crop]["cost"]
                    if budget >= cost:
                        effective_time, _, fail_chance = apply_weather_effects(crop, weather_scenario[t], t, DAYS - t)
                        grid[i][j] = crop
                        timers[i][j] = effective_time
                        budget -= cost
        
        # Harvest where possible
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if grid[i][j] and timers[i][j] <= 0:
                    crop = grid[i][j]
                    _, _, fail_chance = apply_weather_effects(crop, weather_scenario[t], t, DAYS - t)
                    if random.random() < fail_chance:
                        grid[i][j] = None
                        timers[i][j] = 0
                        continue
                    
                    profit = apply_market_prices(crop, t, harvest_history)
                    final_profit = apply_crop_abilities(crop, grid, i, j, weather_scenario[t], t, weather_scenario[:t+1], profit)
                    
                    profit += final_profit
                    budget += final_profit
                    harvested_crops.add(crop)
                    harvest_history[t][crop] = harvest_history[t].get(crop, 0) + 1
                    grid[i][j] = None
                    timers[i][j] = 0
    
    if len(harvested_crops) == len(BASE_CROPS):
        profit += DIVERSITY_BONUS
    
    return profit

def adjust_time(crop, base_time, weather):
    """
    Điều chỉnh thời gian sinh trưởng của cây trồng dựa trên thời tiết.
    - Sunny: Tăng tốc độ sinh trưởng của tomato (+1 speed, giảm 1 ngày).
    - Rainy: Tăng tốc độ sinh trưởng của rice (+1 speed, giảm 1 ngày).
    - Dry: Tăng tốc độ sinh trưởng của corn (+1 speed, giảm 1 ngày).
    """
    time_reduction = 0
    if weather == "Sunny" and crop == "tomato":
        time_reduction = 1
    elif weather == "Rainy" and crop == "rice":
        time_reduction = 1
    elif weather == "Dry" and crop == "corn":
        time_reduction = 1
    
    # Đảm bảo thời gian không giảm xuống dưới 1
    adjusted_time = max(1, base_time - time_reduction)
    return adjusted_time

def estimate_upper_bound(t, grid, harvested_crops, remaining_budget, scenario):
    # Tính lợi nhuận hiện tại từ các cây đã trồng và đang chờ thu hoạch
    current_profit = 0
    temp_grid = [row[:] for row in grid]
    temp_timers = [[0 for _ in range(len(grid))] for _ in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid)):
            if temp_grid[i][j]:
                temp_timers[i][j] = BASE_CROPS[temp_grid[i][j]]["time"]

    for current_t in range(t, len(scenario)):
        weather = scenario[current_t % len(scenario)]
        for i in range(len(grid)):
            for j in range(len(grid)):
                if temp_grid[i][j]:
                    time_reduction = 0
                    fail_chance = 0
                    crop = temp_grid[i][j]
                    if weather == "Sunny" and crop == "tomato":
                        time_reduction = 1
                    elif weather == "Rainy":
                        if crop == "rice":
                            time_reduction = 1
                        elif crop == "tomato":
                            fail_chance = 0.5
                    elif weather == "Dry":
                        if crop == "corn":
                            time_reduction = 1
                        elif crop == "rice":
                            fail_chance = 0.5

                    if fail_chance > 0 and random.random() < fail_chance:
                        temp_grid[i][j] = None
                        temp_timers[i][j] = 0
                        continue

                    if time_reduction > 0 and temp_timers[i][j] > 0:
                        temp_timers[i][j] = max(1, temp_timers[i][j] - time_reduction)

                    temp_timers[i][j] -= 1
                    if temp_timers[i][j] <= 0 and temp_grid[i][j]:
                        current_profit += BASE_CROPS[temp_grid[i][j]]["profit"]
                        temp_grid[i][j] = None

    # Đếm số ô trống còn lại
    empty_cells = sum(row.count(None) for row in grid)

    # Tìm cây trồng tốt nhất (có lợi nhuận cao nhất) trong điều kiện thời tiết hiện tại
    weather = scenario[t % len(scenario)]
    best_crop = None
    best_profit_per_day = 0
    for crop, data in BASE_CROPS.items():
        cost = data["cost"]
        if remaining_budget < cost:
            continue
        time = adjust_time(crop, data["time"], weather)  # Sử dụng hàm adjust_time
        profit = data["profit"] / time  # Lợi nhuận trên mỗi ngày
        if profit > best_profit_per_day:
            best_profit_per_day = profit
            best_crop = crop

    # Nếu không tìm thấy cây trồng nào (ngân sách không đủ), trả về lợi nhuận hiện tại
    if best_crop is None:
        # Thêm bonus đa dạng nếu đã thu hoạch đủ loại cây
        if len(harvested_crops) == len(BASE_CROPS):
            current_profit += DIVERSITY_BONUS
        return current_profit

    # Tính chi phí và lợi nhuận tối đa giả định
    cost_per_cell = BASE_CROPS[best_crop]["cost"]
    profit_per_cell = BASE_CROPS[best_crop]["profit"]

    # Tính số ô có thể trồng với ngân sách còn lại
    max_cells_can_plant = min(empty_cells, remaining_budget // cost_per_cell)

    # Ước tính lợi nhuận tối đa
    optimistic_profit = current_profit + max_cells_can_plant * profit_per_cell

    # Thêm bonus đa dạng nếu có thể thu hoạch đủ loại cây
    potential_crops = set(harvested_crops)
    if best_crop not in potential_crops:
        potential_crops.add(best_crop)
    if len(potential_crops) == len(BASE_CROPS):
        optimistic_profit += DIVERSITY_BONUS

    return optimistic_profit

def generate_greedy_plan(budget, weather_scenarios):
    best_plan = []
    best_avg_profit = float('-inf')
    
    for initial_crop_order in [["rice", "corn", "tomato"], ["corn", "tomato", "rice"], ["tomato", "rice", "corn"]]:
        plan = []
        remaining_budget = budget
        grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        timers = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        harvested_crops = set()
        action_count = 0
        
        # Step 1: Plant one of each crop to ensure diversity bonus
        positions = list(product(range(GRID_SIZE), range(GRID_SIZE)))
        random.shuffle(positions)  # Shuffle to distribute crops
        pos_idx = 0
        for crop in initial_crop_order:
            if pos_idx >= len(positions) or action_count >= MAX_ACTIONS:
                break
            i, j = positions[pos_idx]
            cost = BASE_CROPS[crop]["cost"]
            if remaining_budget >= cost:
                plan.append([[i, j], "plant", crop])
                grid[i][j] = crop
                timers[i][j] = BASE_CROPS[crop]["time"]
                remaining_budget -= cost
                pos_idx += 1
                action_count += 1
        
        # Step 2: Fill remaining spots with the most profitable crops
        for t in range(DAYS):
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    if grid[i][j] and timers[i][j] <= t and action_count < MAX_ACTIONS:
                        plan.append([[i, j], "harvest"])
                        harvested_crops.add(grid[i][j])
                        grid[i][j] = None
                        timers[i][j] = 0
                        action_count += 1
            
            # Plant in empty spots
            available_positions = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] is None]
            if available_positions and action_count < MAX_ACTIONS:
                # Choose the best crop based on expected profit
                best_crop = max(BASE_CROPS.keys(), key=lambda c: BASE_CROPS[c]["profit"] / BASE_CROPS[c]["time"])
                cost = BASE_CROPS[best_crop]["cost"]
                if remaining_budget >= cost and t + BASE_CROPS[best_crop]["time"] <= DAYS:
                    # Score each position
                    scored_positions = [(score_position(grid, i, j, best_crop, weather_scenarios, t), (i, j)) for i, j in available_positions]
                    scored_positions.sort(reverse=True)  # Sort by score, highest first
                    i, j = scored_positions[0][1]  # Pick the best position
                    plan.append([[i, j], "plant", best_crop])
                    grid[i][j] = best_crop
                    timers[i][j] = BASE_CROPS[best_crop]["time"]
                    remaining_budget -= cost
                    action_count += 1
        
        # Simulate the plan
        total_profit = 0
        for scenario in weather_scenarios:
            total_profit += simulate_plan(plan, scenario)
        avg_profit = total_profit / len(weather_scenarios)
        
        if avg_profit > best_avg_profit:
            best_avg_profit = avg_profit
            best_plan = plan
    
    return best_plan, best_avg_profit

def generate_backtracking_plan(budget, weather_scenarios):
    best_plan = []
    best_avg_profit = float('-inf')
    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    timers = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    harvested_crops = set()
    action_count = [0]
    
    progress_bar = tqdm(total=DAYS, desc="Backtracking", leave=False)
    
    def backtrack(t, remaining_budget, plan, profit_per_scenario):
        nonlocal best_plan, best_avg_profit
        if t >= DAYS or action_count[0] >= MAX_ACTIONS:
            avg_profit = sum(profit_per_scenario) / len(profit_per_scenario)
            if avg_profit > best_avg_profit:
                best_avg_profit = avg_profit
                best_plan = plan[:]
            return
        
        upper_bounds = []
        for scenario in weather_scenarios:
            upper_bound = profit_per_scenario[weather_scenarios.index(scenario)] + \
                          estimate_upper_bound(t, grid, harvested_crops, remaining_budget, scenario)
            upper_bounds.append(upper_bound)
        avg_upper_bound = sum(upper_bounds) / len(upper_bounds)
        
        if avg_upper_bound <= best_avg_profit:
            return
        
        progress_bar.update(1)
        
        new_plan = plan[:]
        current_harvested = harvested_crops.copy()
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if grid[i][j] and timers[i][j] <= t and action_count[0] < MAX_ACTIONS:
                    new_plan.append([[i, j], "harvest"])
                    current_harvested.add(grid[i][j])
                    grid[i][j] = None
                    timers[i][j] = 0
                    action_count[0] += 1
        
        # Try planting in the best position for each crop
        available_positions = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] is None]
        if available_positions and action_count[0] < MAX_ACTIONS:
            for crop in BASE_CROPS:
                cost = BASE_CROPS[crop]["cost"]
                if remaining_budget >= cost and t + BASE_CROPS[crop]["time"] <= DAYS:
                    # Score positions for this crop
                    scored_positions = [(score_position(grid, i, j, crop, weather_scenarios, t), (i, j)) for i, j in available_positions]
                    scored_positions.sort(reverse=True)
                    i, j = scored_positions[0][1]  # Pick the best position
                    new_plan_with_plant = new_plan + [[[i, j], "plant", crop]]
                    grid[i][j] = crop
                    timers[i][j] = BASE_CROPS[crop]["time"]
                    action_count[0] += 1
                    backtrack(t + 1, remaining_budget - cost, new_plan_with_plant, profit_per_scenario)
                    grid[i][j] = None
                    timers[i][j] = 0
                    action_count[0] -= 1
        
        if action_count[0] < MAX_ACTIONS:
            backtrack(t + 1, remaining_budget, new_plan, profit_per_scenario)
    
    profit_per_scenario = [0] * len(weather_scenarios)
    backtrack(0, budget, [], profit_per_scenario)
    progress_bar.close()
    
    if best_plan:
        total_profit = 0
        for scenario in weather_scenarios:
            total_profit += simulate_plan(best_plan, scenario)
        best_avg_profit = total_profit / len(weather_scenarios)
    
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
    for crop in BASE_CROPS.keys():
        if pos_idx >= len(positions) or action_count[0] >= MAX_ACTIONS:
            break
        i, j = positions[pos_idx]
        cost = BASE_CROPS[crop]["cost"]
        if remaining_budget >= cost:
            plan.append([[i, j], "plant", crop])
            grid[i][j] = crop
            timers[i][j] = BASE_CROPS[crop]["time"]
            remaining_budget -= cost
            pos_idx += 1
            action_count[0] += 1
    
    dp = {}
    progress_bar = tqdm(total=DAYS, desc="DP", leave=False)
    
    def dp_solve(t, budget_left):
        if t >= DAYS or action_count[0] >= MAX_ACTIONS:
            total_profit = 0
            for scenario in weather_scenarios:
                total_profit += simulate_plan(plan, scenario)
            avg_profit = total_profit / len(weather_scenarios)
            return avg_profit, []
        
        progress_bar.update(1)
        
        state = (t, budget_left)
        if state in dp:
            return dp[state]
        
        best_profit = float('-inf')
        best_subplan = []
        
        current_grid = [[grid[i][j] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
        current_timers = [[timers[i][j] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
        current_harvested = harvested_crops.copy()
        subplan = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if grid[i][j] and timers[i][j] <= t and action_count[0] < MAX_ACTIONS:
                    subplan.append([[i, j], "harvest"])
                    current_harvested.add(grid[i][j])
                    grid[i][j] = None
                    timers[i][j] = 0
                    action_count[0] += 1
        
        available_positions = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] is None]
        if available_positions and action_count[0] < MAX_ACTIONS:
            for crop in BASE_CROPS:
                cost = BASE_CROPS[crop]["cost"]
                if budget_left >= cost and t + BASE_CROPS[crop]["time"] <= DAYS:
                    scored_positions = [(score_position(grid, i, j, crop, weather_scenarios, t), (i, j)) for i, j in available_positions]
                    scored_positions.sort(reverse=True)
                    i, j = scored_positions[0][1]
                    grid[i][j] = crop
                    timers[i][j] = BASE_CROPS[crop]["time"]
                    action_count[0] += 1
                    subplan_with_plant = subplan + [[[i, j], "plant", crop]]
                    future_profit, future_plan = dp_solve(t + 1, budget_left - cost)
                    if future_profit > best_profit:
                        best_profit = future_profit
                        best_subplan = subplan_with_plant + future_plan
                    grid[i][j] = None
                    timers[i][j] = 0
                    action_count[0] -= 1
        
        future_profit, future_plan = dp_solve(t + 1, budget_left)
        if future_profit > best_profit:
            best_profit = future_profit
            best_subplan = subplan + future_plan
        
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                grid[i][j] = current_grid[i][j]
                timers[i][j] = current_timers[i][j]
        
        dp[state] = (best_profit, best_subplan)
        return dp[state]
    
    total_profit, additional_plan = dp_solve(0, remaining_budget)
    plan.extend(additional_plan)
    
    for step in plan:
        if step[1] == "harvest":
            i, j = step[0]
            for prev_step in plan:
                if prev_step[1] == "plant" and prev_step[0] == [i, j]:
                    harvested_crops.add(prev_step[2])
                    break
    
    progress_bar.close()
    return plan, total_profit

def generate_config():
    budget = random.choice(BUDGETS)
    weather_scenarios = [generate_weather_scenario() for _ in range(NUM_WEATHER_SCENARIOS)]
    greedy_plan, greedy_profit = generate_greedy_plan(budget, weather_scenarios)
    backtracking_plan, backtracking_profit = generate_backtracking_plan(budget, weather_scenarios)
    dp_plan, dp_profit = generate_dp_plan(budget, weather_scenarios)
    
    config = {
        "budget": budget,
        "ai_plans": {
            "greedy": greedy_plan,
            "backtracking": backtracking_plan,
            "dp": dp_plan,
        },
        "ai_profits": {
            "greedy": greedy_profit,
            "backtracking": backtracking_profit,
            "dp": dp_profit,
        }
    }
    return config

def main():
    num_configs = int(input("Nhập số lượng cấu hình cần tạo: "))
    configs = []
    
    for _ in tqdm(range(num_configs), desc="Đang tạo cấu hình"):
        config = generate_config()
        configs.append(config)
    
    with open("ai_plans.json", "w") as f:
        json.dump(configs, f, indent=4)
    print(f"Đã tạo {num_configs} cấu hình và lưu vào ai_plans.json")

if __name__ == "__main__":
    main()