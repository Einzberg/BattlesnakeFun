import random
from typing import List, Dict

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
    possible_moves = avoid_walls(data, possible_moves)
    possible_moves = avoid_myself(my_body, possible_moves)
    possible_moves = avoid_others(my_head, data, possible_moves)
    # TODO: Step 2 - Don't hit yourself.
    # Use information from `my_body` to avoid moves that would collide with yourself.

    # TODO: Step 3 - Don't collide with others.
    # Use information from `data` to prevent your Battlesnake from colliding with others.

    # TODO: Step 4 - Find food.
    # Use information in `data` to seek out and find food.
    # food = data['board']['food']

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    move = random.choice(list(possible_moves))
    last_move = move
    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")
    print(f"HEAD AT: {my_head}")
    print(last_move)

    return move


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

  board_height = data['board']['height']
  board_width = data['board']['width']
  print(f'board_height: {board_height}, board_width: {board_width}')
        
  my_head = data['you']['head']

  # Bottom left is 0,0
  # Top right is board_width, board_height
  if my_head['x'] == 0:
    possible_moves.discard('left')
  if my_head['y'] == 0:
    possible_moves.discard('down')
  if my_head['x'] == board_width - 1:  
    possible_moves.discard('right')
  if my_head['y'] == board_height - 1:      
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

  for direction in list(possible_moves):
    if direction == 'up':
      if {'x': head['x'], 'y': head['y'] + 1} in bodies:
        possible_moves.discard('up')
    elif direction == 'down':
      if {'x': head['x'], 'y': head['y'] - 1} in bodies:
        possible_moves.discard('down')
    elif direction == 'left':
      if {'x': head['x'] - 1, 'y': head['y']} in bodies:
        possible_moves.discard('left')
    elif direction == 'right':
      if {'x': head['x'] + 1, 'y': head['y']} in bodies:
        possible_moves.discard('right')
  return possible_moves