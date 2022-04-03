# import random
# from typing import List, Dict
import numpy as np
# import matplotlib.pyplot as plt

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
# Globals 
food_weight = 9
snake_weight = -9
snake_head_weight = -2
wall_weight = -9
board_centre = 1

board_x = None
board_y = None

def gkern(l=10, scale=4):
    """\
    creates gaussian kernel with side length `l` and a sigma of `sig`
    """
    sig = (l-1)/3
    ax = np.linspace(-(l - 1) / 2., (l - 1) / 2., l)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sig))
    kernel = np.outer(gauss, gauss)
    return scale * kernel / np.max(kernel)

def centre_grad(data: dict) -> np.array:
  board_w = data["board"]["width"]
  board_h = data["board"]["height"]
  gradient_board = gkern(max(board_w, board_h), board_centre)

  return gradient_board

def populate_food(board: np.array, data: dict):
  for food in data['board']['food']:
    food_x, food_y = food['x'], food['y']
    kern_size = max(board.shape[0], board.shape[1])
    kernel = gkern(kern_size*2 + 1, 1)
    mid = kern_size + 1
    x_min = mid - food_x
    x_max = mid + board.shape[0] - food_x
    y_min = mid - food_y
    y_max = mid + board.shape[0] - food_y
    board += kernel[x_min:x_max, y_min:y_max]*food_weight

def populate_other_snakes(board: np.array, data: dict):
    for snake in data['board']['snakes']:        
        snake_body = snake['body']
        for ele in snake_body:
            if ele == snake['head']:
                if ele == data['you']['head']: 
                    board[ele['x'], ele['y']] = snake_weight
                elif snake['length'] < data['you']['length']:
                    continue
                else:
                    board[ele['x'], ele['y']] = snake_weight
                    # direction snake head can go are dangerous
                    board[ele['x'] + 1, ele['y']] += snake_head_weight
                    board[ele['x'] - 1, ele['y']] += snake_head_weight
                    board[ele['x'], ele['y'] + 1] += snake_head_weight
                    board[ele['x'], ele['y'] - 1] += snake_head_weight
            else:
                board[ele['x'], ele['y']] = snake_weight

def follow_global_max(head: dict, board: np.array) -> str: 
  global_max = np.unravel_index(np.argmax(board), board.shape)
  directions = {
    "up": (0,1),
    "down": (0,-1),
    "left": (-1,0),
    "right": (1,0)
  }
  direction = ""
  distance = 10000
  for item in directions.items():
    curr_dist = (head['x'] + item[1][0] - global_max[0])**2 + (head['y'] + item[1][1] - global_max[1])**2
    print(curr_dist, item[0])
    if curr_dist < distance:
      distance = curr_dist
      direction = item[0]
  return direction

def follow_grad(head: dict, board: np.array) -> str:
    directions = {
        "up": (0,1),
        "down": (0,-1),
        "left": (-1,0),
        "right": (1,0)
    }
    direction = ""
    max_score = 0
  
    for item in directions.items():
        curr_score = board[head['x'] + item[1][0] + 1, head['y'] + item[1][1] + 1]
        if curr_score > max_score:
            max_score = curr_score
            direction = item[0]

    return direction

def choose_move(data: dict) -> str:
    board_y = data['board']['height']
    board_x = data['board']['width']

    board = centre_grad(data)
    # print(f'GRADIENT ARRAY: {array_of_arrays}')

    populate_other_snakes(board, data)
    board = np.pad(board, 1, 'constant', constant_values=wall_weight)
    populate_food(board, data)
    direction = follow_global_max(data['you']['head'], board)

    # direction = follow_grad(array_of_arrays)
    print(f'GOING THIS DIRECTION: {direction}')
    return direction


data = {
  "turn": 14,
  "board": {
    "height": 11,
    "width": 11,
    "food": [
      {"x": 5, "y": 5}, 
      {"x": 9, "y": 0}, 
      {"x": 2, "y": 6}
    ],
    "hazards": [
      {"x": 3, "y": 2}
    ],
    "snakes": [
      {
        "id": "snake-508e96ac-94ad-11ea-bb37",
        "name": "My Snake",
        "health": 54,
        "body": [
          {"x": 0, "y": 0}, 
          {"x": 1, "y": 0}, 
          {"x": 2, "y": 0}
        ],
        "latency": "111",
        "head": {"x": 0, "y": 0},
        "length": 3,
        "shout": "why are we shouting??",
        "squad": "",
        "customizations":{
          "color":"#FF0000",
          "head":"pixel",
          "tail":"pixel"
        }
      }, 
      {
        "id": "snake-b67f4906-94ae-11ea-bb37",
        "name": "Another Snake",
        "health": 16,
        "body": [
          {"x": 5, "y": 4}, 
          {"x": 5, "y": 3}, 
          {"x": 6, "y": 3},
          {"x": 6, "y": 2}
        ],
        "latency": "222",
        "head": {"x": 5, "y": 4},
        "length": 4,
        "shout": "I'm not really sure...",
        "squad": "",
        "customizations":{
          "color":"#26CF04",
          "head":"silly",
          "tail":"curled"
        }
      }
    ]
  },
      "you": {
      "id": "snake-508e96ac-94ad-11ea-bb37",
        "name": "My Snake",
        "health": 54,
        "body": [
        {"x": 0, "y": 0}, 
        {"x": 1, "y": 0}, 
        {"x": 2, "y": 0}
        ],
        "latency": "111",
        "head": {"x": 0, "y": 0},
        "length": 3,
        "shout": "why are we shouting??",
        "squad": "",
        "customizations":{
        "color":"#FF0000",
        "head":"pixel",
        "tail":"pixel"
        }
    }
}

if False:
  board = centre_grad(data)
  board_x, board_y = 11, 11
  populate_other_snakes(board, data)
  populate_food(board, data)
  board = np.pad(board, 1, 'constant', constant_values=snake_weight)

  # plt.imshow(np.rot90(np.fliplr(board)), interpolation='none', origin="lower")
  # plt.show()
