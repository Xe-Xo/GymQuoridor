from enum import Enum


class TupleEnum(tuple,Enum):
  pass

class IntEnum(int,Enum):
  pass


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
  HORIZONTAL = 1
  VERTICAL = 2

class MovementDir(TupleEnum):
  UP = (0,-1)
  DOWN = (0,1)
  LEFT = (-1,0)
  RIGHT = (1,0)

class MovementIndex(IntEnum):
  UP = 0
  DOWN = 1
  LEFT = 2
  RIGHT = 3

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

class PlayerState(IntEnum):
  PLAYER = 1
  OPPONENT = 2
  NONE = 0


