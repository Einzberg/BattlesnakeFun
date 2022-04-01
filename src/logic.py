import random
from typing import List, Dict
import numpy as np
"""
This file can be a nice home for your Battlesnake's logic and helper functions.

We have started this for you, and included some logic to remove your Battlesnake's 'neck'
from the list of possible moves!
"""

def get_info() -> dict:
    """
    This controls your Battlesnake appearance and author permissions.
    For customization options, see https://docs.battlesnake.com/references/personalization

    TIP: If you open your Battlesnake URL in browser you should see this data.
    """
    return {
        "apiversion": "1",
        "author": "Mex",  # TODO: Your Battlesnake Username
        "color": "#888889",  # TODO: Personalize
        "head": "silly",  # TODO: Personalize
        "tail": "curled",  # TODO: Personalize
    }


def populate_board(data: dict):
  board = data["board"]
  snakes = board["snakes"]
  # empty grid
  occ_grid = np.zeros((board["height"], board["width"]))
  for snake in snakes:
    for loc in snake['body']:
      occ_grid[loc["x"], loc["y"]] = 1
  return occ_grid

  
def get_nearest_food(data: dict) -> dict:
  all_foods = data["board"]["food"]
  closest_food = None
  closest_dist = 100000
  curr_x, curr_y = data["you"]["head"]["x"], data["you"]["head"]["y"]
  for food in all_foods:
    dist = (curr_x - food["x"])**2 + (curr_y - food["y"])**2
    if dist < closest_dist:
      closest_dist = dist
      closest_food = food

  print(f'CLOSEST FOOD: {closest_food}')
  return closest_food

def food_direction(data: dict) -> set:
  head = data["you"]["head"]
  food = get_nearest_food(data)
  
  head_x, head_y = head["x"], head["y"]
  food_x, food_y = food["x"], food["y"]
  
  x_dir = food_x - head_x
  y_dir = food_y - head_y
  
  dirs = set()
  
  if x_dir > 0:
    dirs.add("right")
  if x_dir < 0:
    dirs.add("left")
  if y_dir > 0: 
   dirs.add("up")
  if y_dir < 0:
    dirs.add("down")
    
  return dirs
  
# Sample Move Request: https://docs.battlesnake.com/references/api/sample-move-request
def get_direction(data, possible_moves) -> set:
  suggested_moves = set()
  hash_scores = {}
  max_score = 0
  for move in possible_moves:
    score = get_flood_fill(move, data)
    if score > max_score: max_score = score
    hash_scores[move] = score
    print(f'MOVE: {move}, SCORE: {score}')

  for key, score in hash_scores.items():
    if score > max_score - 10: suggested_moves.add(key)

  print(f'FLOOD DIRECTIONS DEEMED OK {suggested_moves}')
  food_moves = food_direction(data)
  print(f'FOOD DIRECTIONS DEEMED OK {food_moves}')
  if food_moves:
    if suggested_moves.intersection(food_moves):
      return suggested_moves.intersection(food_moves)
    else:
      return suggested_moves
  else:
    return suggested_moves

"""
input: str: move (up, down, left, right)
output: int: score (non-occupied squares in that direction)
"""
def get_flood_fill(move: str, data: dict) -> dict:
  board = populate_board(data)
  visited = np.array(board)
  head = data["you"]["head"]
  y_max = data['board']['height']
  x_max = data['board']['width']
  
  dir = {"up": (0,1),
         "down": (0,-1),
         "left": (-1,0),
         "right": (1,0)}

  def r_visit(x: int, y: int, acc: int) -> int:
    

    
    if visited[x, y] != 1:
      acc += 1
      visited[x, y] = 1
    if x+1 < x_max and not visited[x + 1, y]: acc += r_visit(x + 1, y, 0) 
    if y+1 < y_max and not visited[x, y + 1]: acc += r_visit(x, y + 1, 0)
    if 0 <= x-1 and not visited[x - 1, y]: acc += r_visit(x - 1, y, 0)
    if 0 <= y-1 and not visited[x, y - 1]: acc += r_visit(x, y - 1, 0)
    
    return acc
  
  score = r_visit(head["x"] + dir[move][0], head["y"] + dir[move][1], 0)
  return score

def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    last_move = "idk"
    my_snake = data["you"]      # A dictionary describing your snake's position on the board
    my_head = my_snake["head"]  # A dictionary of coordinates like {"x": 0, "y": 0}
    my_body = my_snake["body"]  # A list of coordinate dictionaries like [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]

    # Uncomment the lines below to see what this data looks like in your output!
    # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    # print(f"All board data this turn: {data}")
    # print(f"My Battlesnake this turn is: {my_snake}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = { "up", "down", "left", "right" } 

    # Step 0: Don't allow your Battlesnake to move back on it's own neck.
    possible_moves = _avoid_my_neck(my_body, possible_moves)
    print(f'FINISHED AVOIDING NECK - POSSIBLE_MOVES {possible_moves}')
    possible_moves = avoid_walls(data, possible_moves)
    print(f'FINISHED AVOIDING WALLS - POSSIBLE_MOVES {possible_moves}')
    possible_moves = avoid_myself(my_body, possible_moves)
    print(f'FINSIHED AVOIDING MYSELF - POSSIBLE_MOVES {possible_moves}')
    possible_moves = avoid_others(my_head, data, possible_moves)
    print(f'FINSIHED AVOIDING OTHERS - POSSIBLE_MOVES {possible_moves}')
    possible_moves = avoid_face_to_face_if_weak(data, possible_moves)
    print(f'FINSIHED AVOIDING IF WEEEAAKK - POSSIBLE_MOVES {possible_moves}')

    possible_moves = get_direction(data, possible_moves)
    print(f'FINSIHED GETTING DIRECTIONS - POSSIBLE_MOVES {possible_moves}')
    # TODO: Step 2 - Don't hit yourself.
    # Use information from `my_body` to avoid moves that would collide with yourself.

    # TODO: Step 3 - Don't collide with others.
    # Use information from `data` to prevent your Battlesnake from colliding with others.

    # TODO: Step 4 - Find food.
    # Use information in `data` to seek out and find food.
    # food = data['board']['food']

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    move = random.choice(list(possible_moves))
    # last_move = move
    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")
    print(f"HEAD AT: {my_head}")
    # print(last_move)

    return move

def generate_possible_head_moves(head: dict) -> []:
  x, y = head['x'], head['y']

  return [{"x": x+1, "y": y}, {"x": x-1, "y": y}, {"x": x, "y": y+1}, {"x": x, "y": y-1}]

def avoid_face_to_face_if_weak(data: dict, possible_moves: set) -> set:
  other_snakes = data['board']['snakes']
  head = data['you']['head']
  
  for snake in other_snakes:
    if snake['name'] == data['you']['name']: continue
    if snake['length'] < data['you']['length']: continue
    flat_list = generate_possible_head_moves(snake['head'])

    print(f'LIST OF OTHER SNAKE{flat_list}')
    print(f'ME{head}')
      
    for direction in list(possible_moves):
      if direction == 'up':
        if {'x': head['x'], 'y': head['y'] + 1} in flat_list:
          possible_moves.discard('up')
      elif direction == 'down':
        if {'x': head['x'], 'y': head['y'] - 1} in flat_list:
          possible_moves.discard('down')
      elif direction == 'left':
        if {'x': head['x'] - 1, 'y': head['y']} in flat_list:
          possible_moves.discard('left')
      elif direction == 'right':
        if {'x': head['x'] + 1, 'y': head['y']} in flat_list:
          possible_moves.discard('right')

  return possible_moves

def _avoid_my_neck(my_body: dict, possible_moves: set) -> set:
    """
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_head = my_body[0]  # The first body coordinate is always the head
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.discard("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.discard("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.discard("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.discard("up")

    return possible_moves


def avoid_walls(data: dict, possible_moves: set) -> set:
  print("Avoiding the Walls")

  y_max = data['board']['height']
  x_max = data['board']['width']
  print(f'y_max: {y_max}, x_max: {x_max}')
        
  my_head = data['you']['head']

  # Bottom left is 0,0
  # Top right is x_max, y_max
  if my_head['x'] == 0:
    possible_moves.discard('left')
  if my_head['y'] == 0:
    possible_moves.discard('down')
  if my_head['x'] == x_max - 1:  
    possible_moves.discard('right')
  if my_head['y'] == y_max - 1:      
    possible_moves.discard('up')

  return possible_moves

def avoid_myself(my_body: dict, possible_moves: set) -> set:
  head = my_body[0]

  for direction in list(possible_moves):
    if direction == 'up':
      if {'x': head['x'], 'y': head['y'] + 1} in my_body:
        possible_moves.discard('up')
    elif direction == 'down':
      if {'x': head['x'], 'y': head['y'] - 1} in my_body:
        possible_moves.discard('down')
    elif direction == 'left':
      if {'x': head['x'] - 1, 'y': head['y']} in my_body:
        possible_moves.discard('left')
    elif direction == 'right':
      if {'x': head['x'] + 1, 'y': head['y']} in my_body:
        possible_moves.discard('right')
  return possible_moves

def avoid_others(head: dict, others: dict, possible_moves:set) -> set:
  bodies = []
  for snakes in others['board']['snakes']:
    bodies.append(snakes['body'])

  flat_list = [item for sublist in bodies for item in sublist]

  for direction in list(possible_moves):
    if direction == 'up':
      if {'x': head['x'], 'y': head['y'] + 1} in flat_list:
        possible_moves.discard('up')
    elif direction == 'down':
      if {'x': head['x'], 'y': head['y'] - 1} in flat_list:
        possible_moves.discard('down')
    elif direction == 'left':
      if {'x': head['x'] - 1, 'y': head['y']} in flat_list:
        possible_moves.discard('left')
    elif direction == 'right':
      if {'x': head['x'] + 1, 'y': head['y']} in flat_list:
        possible_moves.discard('right')
  return possible_moves