from enum import Enum


class TupleEnum(tuple,Enum):
  pass

class IntEnum(int,Enum):
  pass

class Player(IntEnum):
  """
  BLACK: Player that starts first.
  WHITE: Player that starts second.
  """
  BLACK = 0
  WHITE = 1

class RewardMethod(Enum):
  """
  REAL: 0 = game is ongoing, +15 = Black won, -15 = White won"
  HEURISTIC: if the game is ongoing the reward is the movement steps between Black and White
  Otherwise the game has ended and if player 1 has won the reward is +15 and if player 2 has won the reward is -15
  INVALID: Heuristic reward however a -1 reward if action is invalid for current player
  """

  REAL = 'real'
  HEURISTIC = 'heuristic'
  INVALID = 'invalid'

class Color(TupleEnum):

  GRAY = (100, 100, 100)
  WHITE = (255, 255, 255)
  RED = (255, 0, 0)
  GREEN = (0, 255, 0)
  BLUE = (0, 0, 255)
  YELLOW = (255, 255, 0)
  ORANGE = (255, 128, 0)
  PURPLE = (255, 0, 255)
  CYAN = (0, 255, 255)
  BLACK = (0, 0, 0)

class WallDir(IntEnum):

  VERTICAL = 1
  HORIZONTAL = 2

class MovementDir(TupleEnum):

  UP = (0,-1)
  DOWN = (0,1)
  LEFT = (-1,0)
  RIGHT = (1,0)
  UPUP = (0,-2)
  UPLEFT = (-1,-1)
  UPRIGHT = (1,-1)
  DOWNDOWN = (0,2)
  DOWNLEFT = (-1,1)
  DOWNRIGHT = (1,1)
  LEFTLEFT = (-2,0)
  RIGHTRIGHT = (2,0)

class MovementIndex(IntEnum):

  UP = 0
  DOWN = 1
  LEFT = 2
  RIGHT = 3
  UPUP = 4
  UPLEFT = 5
  UPRIGHT = 6
  DOWNDOWN = 7
  DOWNLEFT = 8
  DOWNRIGHT = 9
  LEFTLEFT = 10
  RIGHTRIGHT = 11

class CompassDir(TupleEnum):

  NW = (-1,-1)
  NE = (0,-1)
  SW = (-1,0)
  SE = (0,0)

class CompassIndex(IntEnum):
  
  NW = 0
  NE = 1
  SW = 2
  SE = 3

  