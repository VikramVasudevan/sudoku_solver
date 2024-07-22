debug = False

SUDOKU_PUZZLE_SIZE = 9

SUBCUBE_CONFIG = [
    [(0, 2), (0, 2)],
    [(0, 2), (3, 5)],
    [(0, 2), (6, 8)],
    [(3, 5), (0, 2)],
    [(3, 5), (3, 5)],
    [(3, 5), (6, 8)],
    [(6, 8), (0, 2)],
    [(6, 8), (3, 5)],
    [(6, 8), (6, 8)],
]

### SIMPLE PUZZLE
simple_puzzle = [[0, 0, 2, 0, 8, 0, 0, 6, 0],
            [0, 5, 6, 9, 1, 7, 0, 3, 0],
            [0, 4, 0, 0, 5, 0, 8, 7, 1],
            [0, 9, 0, 0, 0, 0, 6, 0, 0],
            [6, 7, 1, 0, 9, 5, 2, 0, 0],
            [0, 0, 0, 0, 2, 0, 1, 0, 0],
            [1, 6, 7, 0, 3, 0, 5, 9, 0],
            [4, 8, 0, 0, 7, 0, 3, 0, 0],
            [0, 2, 5, 4, 6, 0, 0, 0, 0]
            ]

expert_puzzle = [[0, 0, 0, 6, 0, 0, 0, 4, 0],
          [0, 0, 0, 0, 4, 0, 1, 0, 0],
          [3, 0, 1, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 3, 0, 6, 0, 0],
          [0, 0, 0, 7, 0, 0, 0, 0, 0],
          [1, 0, 2, 0, 0, 6, 9, 3, 0],
          [0, 7, 0, 0, 0, 8, 0, 0, 4],
          [0, 0, 0, 9, 0, 7, 0, 2, 0],
          [0, 6, 8, 2, 0, 0, 7, 0, 0]
          ]

expert_puzzle_2 = [
    [0,5,0,0,2,0,0,0,0],
    [0,6,0,0,0,4,8,9,0],
    [0,1,0,0,0,0,2,7,0],
    [0,0,6,9,0,0,0,3,0],
    [0,0,0,0,0,0,0,0,1],
    [9,8,0,0,1,3,0,4,0],
    [0,7,0,2,0,5,4,6,0],
    [0,0,5,6,0,1,0,0,0],
    [0,0,0,8,0,0,0,0,0]
]

expert_puzzle_3 = [
    [0,0,5,0,0,0,0,0,0],
    [1,6,0,0,2,0,0,4,0],
    [3,7,0,0,0,0,0,0,0],
    [0,0,0,2,5,0,1,0,0],
    [0,9,0,0,0,0,0,0,0],
    [0,4,0,7,0,0,6,0,3],
    [0,0,0,0,0,8,2,0,0],
    [0,0,4,0,1,0,0,0,9],
    [0,8,2,9,0,0,0,0,6]
]

expert_puzzle_4_unsolved = [
    [0,0,0,8,0,0,6,0,0],
    [0,3,0,0,2,0,0,1,0],
    [0,4,0,0,7,0,0,3,0],
    [0,8,0,9,0,3,2,5,0],
    [0,0,5,0,0,0,0,7,0],
    [0,0,0,0,0,0,9,0,4],
    [6,0,0,0,0,0,3,8,0],
    [0,2,0,0,1,0,0,0,0],
    [4,0,0,2,8,0,0,0,0]
]

expert_puzzle_5 = [
    [5,0,0,0,0,0,9,0,0],
    [0,0,0,5,2,1,0,0,0],
    [0,0,0,6,0,7,2,0,0],
    [0,8,0,0,0,0,0,3,9],
    [0,0,7,0,6,0,0,0,0],
    [4,2,0,1,0,0,8,0,5],
    [8,0,0,0,0,4,0,0,1],
    [0,0,9,0,0,0,0,0,8],
    [0,3,0,0,0,0,0,0,0]
]

all_zero_puzzle = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
]

DISABLE_AUDIO = True
MAX_ATTEMPTS = 20
SELECTED_PUZZLE = expert_puzzle_5