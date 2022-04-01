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

def gkern(l=10, sig=3., scale=10):
    """\
    creates gaussian kernel with side length `l` and a sigma of `sig`
    """
    ax = np.linspace(-(l - 1) / 2., (l - 1) / 2., l)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sig))
    kernel = np.outer(gauss, gauss)
    return scale * kernel / np.max(kernel)
  
def centre_grad(data: dict) -> np.array:
  board_w = data["board"]["width"] + 1
  board_h = data["board"]["height"] + 1
  gradient_board = gkern(max(board_w, board_h))
  populate_walls_on_grad(gradient_board, board_w, board_h)

  return gradient_board

def populate_walls_on_grad(board: np.array, board_w, board_h):
  for x in range(0, board_w): 
    board[x, 0] = -9
    board[x, board_h -1] = -9

  for y in range(0, board_h): 
    board[0, y] = -9
    board[board_w - 1, y] = -9

def populate_other_snakes(board: np.array, data: dict):
    for snake in data['board']['snakes']:        
        snake_body = snake['body']
        for ele in snake_body:
            if ele == snake['head']:
                if ele == data['you']['head']: 
                    board[ele['x'] + 1, ele['y'] + 1] = -9
                elif snake['length'] < data['you']['length']:
                    continue
                else:
                    board[ele['x'] + 1, ele['y'] + 1] = -9
                    # direction snake head can go are dangerous
                    board[ele['x'] + 1 + 1, ele['y'] + 1] += -2
                    board[ele['x'] - 1 + 1, ele['y'] + 1] += -2
                    board[ele['x'] + 1, ele['y'] + 1 + 1] += -2
                    board[ele['x'] + 1, ele['y'] - 1 + 1] += -2
            else:
                board[ele['x'] + 1, ele['y'] + 1] = -9

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
    array_of_arrays = centre_grad(data)
    # print(f'GRADIENT ARRAY: {array_of_arrays}')

    populate_other_snakes(array_of_arrays, data)

    direction = follow_grad(data['you']['head'], array_of_arrays)

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

# board = centre_grad(data)
# populate_other_snakes(board, data)

# plt.imshow(np.rot90(np.fliplr(board)), interpolation='none', origin="lower")
# plt.show()