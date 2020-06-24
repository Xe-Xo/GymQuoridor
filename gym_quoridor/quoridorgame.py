import math
import numpy as np
from gym_quoridor import quoridorvars, state_utils, pathfinding


"""
The state of the game is a numpy array
* Are values are either 0 or 1
* Shape [NUM_CHNLS, SIZE, SIZE]
0 - Black Location (0 - False, 1 - True)
1 - White Location (0 - False, 1 - True)
2 - Turn (0 - black, 1 - white)
3 - Black Valid moves (0 - Invalid, 1 - Valid
4 - White Valid moves (0 - Invalid, 1 - Valid)
5 - Current Vertical Wall Location (0 - None, 1 - Placed)
6 - Current Horizontal Wall Location (0 - None, 1 - Placed)
7 - Valid Vertical Wall locations (0 - Invalid, 1 - Valid)
8 - Valid Horizontal Wall locations (0 - Invalid, 1 - Valid)
9 - Black Astar Path (0 - No Path, 1 - Path)
10 - White Astar Path (0 - No Path, 1 - Path)
11 - Game Over
12 - Black Walls (1 = +1 Wall available)
13 - White Walls (1 = +1 Wall available)
"""

class QuoridorGame():

  """Class manages states of the game to output new states"""

  @staticmethod
  def get_init_board(size):

    """
    Initializes the Board in its Starting State
    Players location at each end
    Black Players turn
    Valid Moves setup
    All Wall locations marked Valid
    Black_astar calculated
    White_astar calculated
    Gameover set to 0
    """

    # return initial board (numpy board) (12,9,9) (channel,x_loc,y_loc)

    state = np.zeros((quoridorvars.NUM_CHNLS, size, size),dtype=np.int32)

    #Layer 0 & 1
    state = QuoridorGame.set_player_location(state,size//2,0,0)
    state = QuoridorGame.set_player_location(state,size//2,size-1,1)

    #Layer 2 already correctly set to 0 -- BLACK TURN
    #Layers 5 & 6 already set to zero -- NO WALLS PLACED

    #Layer 3, 4, 7, 8, 9, 10
    state = QuoridorGame.set_valid_moves(state,0)
    state = QuoridorGame.set_valid_moves(state,1)
    state = QuoridorGame.set_invalid_placement(state,0)
    state = QuoridorGame.set_invalid_placement(state,1)
    state = QuoridorGame.set_path(state,0)
    state = QuoridorGame.set_path(state,1)

    #Layer 11 set to not GAME_OVER
    return state

  @staticmethod
  def get_action_size(state=None,board_size: int = None):
    if state is not None:
      m, n = state_utils.get_wall_size(state)
    elif board_size is not None:
      m, n = board_size -1, board_size-1
    else:
      raise RuntimeError('No argument passed')
    
    return 12 + m * n * 2

  @staticmethod
  def get_max_walls(state):
    m, n = state_utils.get_wall_size(state)
    return (math.sqrt(m * n) // 2) + 1

  @staticmethod
  def get_game_ended(state):
    return QuoridorGame.get_player_pos(state,0) in QuoridorGame.get_player_end_pos(state,0) or QuoridorGame.get_player_pos(state,1) in QuoridorGame.get_player_end_pos(state,1) 

#region Next State Methods

  @staticmethod
  def get_next_state(state, action):
    '''
    Action has not been checked whether valid or not
    if valid then return the updated state and set the turn, update info layers
    '''
    m, n = state_utils.get_board_size(state)

    if action < 12:
      valid, i, j = QuoridorGame.valid_move(state,action)
      if valid:
        state = QuoridorGame.set_player_location(state,i,j,QuoridorGame.get_player_turn(state))
        state = QuoridorGame.set_turn(state)
        state = QuoridorGame.set_info_layers(state)
    elif action >= 12 and action <= 12 + (m-1) * (n-1) * 2:
      valid, i, j, walldir = QuoridorGame.valid_placement(state,action)
      if valid:
        state = QuoridorGame.set_wall_location(state,i,j,walldir,QuoridorGame.get_player_turn(state))
        state = QuoridorGame.set_turn(state)
        state = QuoridorGame.set_info_layers(state)
    else:
      raise Exception(f"action int is outside the action space! {action}")

    return state

  @staticmethod
  def valid_move(state,moveaction):
    
    '''
    Check whether movementint translated to board coord is allowed
    '''
    o_i, o_j = QuoridorGame.action_to_movement(state,moveaction)
    p = QuoridorGame.get_player_turn(state)
    p_i, p_j = QuoridorGame.get_player_pos(state,p)
    if state[quoridorvars.BLACKMOVEVALID_CHNL+p,p_i + o_i,p_j + o_j] == 1:
      return True, p_i + o_i, p_j + o_j
    else:
      return False, p_i + o_i, p_j + o_j

  @staticmethod
  def valid_placement(state,placementaction):

    '''
    Check whether placementint translated to board coord is allowed
    '''
    i,j,d = QuoridorGame.action_to_placement(state,placementaction)
    p = QuoridorGame.get_player_turn(state)
    if QuoridorGame.get_player_walls(state,p) < 5:
      if state[quoridorvars.INVALID_V_WALL_CHNL+d-1,i,j] == 0:
        return True, i, j, d
      else:
        return False, i, j, d

    else:
      return False, i, j, d 

  @staticmethod
  def action_to_movement(state,action):
    if action < 12:
      return quoridorvars.MOVEMENT_DIR[action]
    else:
      raise Exception(f"Action is greater than 12?!!?! {action}")

  @staticmethod
  def action_to_placement(state,action):
    m,n = state_utils.get_wall_size(state)
    wallspace = m * n

    if action >= 12 and action <= 11 + wallspace * 2:

      action -= 12
      actionmod = action % wallspace
      walldir = action // wallspace
      x,y = actionmod % m, actionmod // m
      return x,y,walldir
    else:
      raise Exception(f"Action is outside wallactionspace? 12 <= {action} >= 11 + {wallspace * 2} = {11 + wallspace * 2}")

#endregion

#region Movement and Wall Placement

  @staticmethod
  def walls_around_pos(state,i,j):

    #return 1,0 whether a walll exists in NW,NE,SW,SE positions
    m,n = state_utils.get_wall_size(state)
    vwalls = [0,0,0,0]
    hwalls = [0,0,0,0]

    for coordindex,offset in enumerate([(-1,-1),(0,-1),(-1,0),(0,0)]): #Check around location
      o_i, o_j = offset
      c_i, c_j = i + o_i, j+ o_j #wall coords
      if c_i < 0 or c_i > m or c_j < 0 or c_j > n: #if wall out of range
        vwalls[coordindex] = 0
        hwalls[coordindex] = 0
      else:
        vwalls[coordindex] = state[quoridorvars.BLACK_V_WALL_CHNL,c_i,c_j] + state[quoridorvars.WHITE_V_WALL_CHNL,c_i,c_j]
        hwalls[coordindex] = state[quoridorvars.BLACK_H_WALL_CHNL,c_i,c_j] + state[quoridorvars.WHITE_H_WALL_CHNL,c_i,c_j]
    
    return vwalls, hwalls

  @staticmethod
  def walls_around_walls(state,i,j):

    #returns 1,0 whether a wall exists in N,S,W,E positions
    m,n = state_utils.get_wall_size(state)
    vwalls = [0,0,0,0]
    hwalls = [0,0,0,0]

    for coordindex, offset in enumerate([(0,-1),(0,1),(-1,0),(1,0)]):
      o_i, o_j = offset
      c_i, c_j = i + o_i, j+ o_j #wall coords
      if c_i < 0 or c_i > m or c_j < 0 or c_j > n: #if wall out of range
        vwalls[coordindex] = 0
        hwalls[coordindex] = 0
      else:
        vwalls[coordindex] = state[quoridorvars.BLACK_V_WALL_CHNL,c_i,c_j] + state[quoridorvars.WHITE_V_WALL_CHNL,c_i,c_j]
        hwalls[coordindex] = state[quoridorvars.BLACK_H_WALL_CHNL,c_i,c_j] + state[quoridorvars.WHITE_H_WALL_CHNL,c_i,c_j]
    
    return vwalls, hwalls      

  @staticmethod
  def invalid_wall_placement(state,i,j,d):

    #returns 0  or 1 to mark whether a wall location is invalid
    vwalls, hwalls = QuoridorGame.walls_around_walls(state,i,j)

    for index in range(len(vwalls)):
      if vwalls[index] == 1: #if wall is vertical
        if d == 1: #Vertical
          if index == 0 or index == 1: #if wall is up or down
            return 1
            
      elif hwalls[index] == 1:
        if d == 2: #Horizontal
          if index == 2 or index == 3:
            return 1

    #checks whether if placed will block paths to exit
    #complexity sucks but only needs to be refreshed when a wall is placed
    tempstate = state.copy()
    current_player = QuoridorGame.get_player_turn(tempstate)
    tempstate = QuoridorGame.set_wall_location(tempstate,i,j,d,current_player)
    black_i, black_j = QuoridorGame.get_player_pos(tempstate,0)
    white_i, white_j = QuoridorGame.get_player_pos(tempstate,1)
    blackpath = QuoridorGame.astar(tempstate,black_i,black_j,0)
    whitepath = QuoridorGame.astar(tempstate,white_i,white_j,1)

    if blackpath is None or whitepath is None:
      return 1

    return 0

  @staticmethod
  def movement_around_pos(state,i,j):

    """"
    Returns allowed movement around a position
    """
    m, n = state_utils.get_board_size(state)

    direction = []
    movement_allowed = [1,1,1,1]

    # check if location is outside board

    for moveid, movedir in enumerate([(0,-1),(0,1),(-1,0),(1,0)]):
      o_i, o_j = movedir
      c_i, c_j = o_i + i, o_j + j
      if c_i < 0 or c_i >= m or c_j < 0 or c_j >= n:
        movement_allowed[moveid] = 0
        
    # check if wall stops movement
    
    vwalls, hwalls = QuoridorGame.walls_around_pos(state,i,j)
    for index in range(len(vwalls)):
      if vwalls[index] == 1:
        if index == 0 or index == 2:
          movement_allowed[2] == 0
        if index == 1 or index == 3:
          movement_allowed[3] == 0 

      if hwalls[index] == 1:
        if index == 0 or index == 1:
          movement_allowed[0] = 0
        if index == 2 or index == 3:
          movement_allowed[1] = 0

    return movement_allowed

  @staticmethod
  def player_movement_around_pos(state,player):

    p_i, p_j = QuoridorGame.get_player_pos(state,player)
    p_movement = QuoridorGame.movement_around_pos(state,p_i,p_j) #[1,1,1,1] [U,D,L,R]
    opp_i, opp_j = QuoridorGame.get_player_pos(state,1-player)

    j_movement = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

    for offset_index, offset_pos in enumerate([(0,-1),(0,1),(-1,0),(1,0)]):
      o_i, o_j = offset_pos
      if p_movement[offset_index] == 1 and p_i + o_i == opp_i and p_j + o_j == opp_j:
        p_movement[offset_index] = 0
        j_movement[offset_index] = QuoridorGame.movement_around_pos(state,opp_i,opp_j)
        if offset_index == 0:
          j_movement[offset_index][0+1-offset_index] = 0
        elif offset_index == 1:
          j_movement[offset_index][0+1-offset_index] = 0
        elif offset_index == 2:
          j_movement[offset_index][2+3-offset_index] = 0
        elif offset_index == 3:
          j_movement[offset_index][2+3-offset_index] = 0
    return p_movement, j_movement

#endregion

#region Getting Player State Methods
  @staticmethod      
  def get_player_pos(state,player):
    m,n = state_utils.get_board_size(state)
    for i in range(m):
      for j in range(n):
        if state[player,i,j] == 1:
          return i,j
    raise KeyError("player not found on board!")    

  @staticmethod
  def get_player_end_pos(state,player):
    end_pos_list = []
    m, n = state_utils.get_board_size(state)
    for i in range(m):
      end_pos_list.append((i,(n-1)-player*(n-1)))
    return end_pos_list

  @staticmethod
  def astar(state,si,sj,p,error=False):
    
    #--TO DO--
    #OPTIMISE OPEN_LIST BY CONVERTING INTO A HEAP
    #ADD JUMPS INTO PATHFINDING BUT WILL PROBABLY REQUIRE STATE MANAGEMENT FOR EACH MOVE
    #PATH LENGTH IS CURRENTLY INACCURATE AS IT DOESNT REMOVE THE JUMP POS

    m, n = state_utils.get_board_size(state)

    end_list = []
    #create start Nodes
    start_node = pathfinding.GridNode(None,(si,sj))
    start_node.g = start_node.h = start_node.f = 0

    #multiple end positions so making multiple end Nodes
    for endpos in QuoridorGame.get_player_end_pos(state,p):
      end_node = pathfinding.GridNode(None,endpos)
      end_node.g = end_node.h = end_node.f = 0
      end_list.append(end_node)

    #Initialise the two lists (open (unseen) and closed (seen))
    open_list = []
    closed_list = []

    #Add start node

    open_list.append(start_node)

    while len(open_list) > 0:

      # get node with greatest f
      current_node = open_list[0]
      current_index = 0
      for index, item in enumerate(open_list):
          if item.f < current_node.f:
              current_node = item
              current_index = index

      open_list.pop(current_index)
      closed_list.append(current_node)

      #check if found a end_node

      for end_node in end_list:
          if current_node == end_node:
              path = []
              current = current_node
              while current is not None:
                  path.append(current.position)
                  current = current.parent
              #return path[::-1]
              return path[::-1][1:] #remove the first position

      #Not at end_node! check next nodes

      children = []
      i,j = current_node.position
      movement_allowed = QuoridorGame.movement_around_pos(state,i,j)
      offset_list = [(0,-1),(0,1),(-1,0),(1,0)]

      for index in range(len(movement_allowed)):
        if movement_allowed[index] == 1:            
          o_i, o_j = offset_list[index]
          c_i, c_j = i + o_i, j + o_j
          new_node = pathfinding.GridNode(current_node, (c_i, c_j))
          children.append(new_node)

      for child in children:
          if child in closed_list:
              continue
          else:
              child.g = current_node.g + 1

              #get lowest h value
              min_h_value = m ** 2 + n ** 2
              min_h_index = 0

              for end_index,end_node in enumerate(end_list):
                  hvalue = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                  if hvalue < min_h_value:
                      min_h_value = hvalue
                      min_h_index = end_index
                  
              #print(f"{child.position}--{end_list[min_h_index]}")
              child.h = min_h_value
              child.f = child.g + child.h

              append = True

              for open_node in open_list:
                  if child == open_node and child.f > open_node.f:
                      append = False
                  else:
                      append = True

              if append:
                  open_list.append(child)
    
    if error:
      raise Exception(f"Path not found! {(si,sj)} --> {QuoridorGame.get_player_end_pos(state,p)} {closed_list}")
  
  @staticmethod
  def get_player_walls(state,player):
    wallcount = np.count_nonzero(state[quoridorvars.BLACK_V_WALL_CHNL+player*2,:,:]) + np.count_nonzero(state[quoridorvars.BLACK_H_WALL_CHNL+player*2,:,:])
    return wallcount

  @staticmethod
  def get_path_len(state,player):
    """ Count non zeros on the layer to get the path"""
    pathlen = np.count_nonzero(state[quoridorvars.BLACKASTAR_CHNL+player])
    return pathlen

  @staticmethod
  def get_player_turn(state):
    turn = state[quoridorvars.TURN_CHNL,0,0]
    return int(turn)

#endregion

#region Setting State Methods

  @staticmethod
  def set_info_layers(state):
    """
    Setting Info Layers after a move has been made
    """

    state = QuoridorGame.set_valid_moves(state,0)
    state = QuoridorGame.set_valid_moves(state,1)
    state = QuoridorGame.set_invalid_placement(state,0)
    state = QuoridorGame.set_invalid_placement(state,1)
    state = QuoridorGame.set_path(state,0)
    state = QuoridorGame.set_path(state,1)
    state = QuoridorGame.set_gameover(state)
    return state

  @staticmethod
  def set_player_location(state,i,j,player):

    """For Player Location Layers (0 & 1)"""

    state = state.copy()
    state[player,:,:] = 0
    state[player,i,j] = 1
    return state
  
  @staticmethod
  def set_turn(state):

    """For Turn Layer (2)"""

    state = state.copy()
    state[quoridorvars.TURN_CHNL,:,:] = 1 - state[quoridorvars.TURN_CHNL,0,0]
    return state

  @staticmethod
  def set_valid_moves(state,player):

    """For Valid Move Layers (3 & 4)"""

    state = state.copy()
    state[3+player,:,:] = 0

    p_i, p_j = QuoridorGame.get_player_pos(state,player)
    p_movement, j_movement = QuoridorGame.player_movement_around_pos(state,player)

    for movementindex,offset in enumerate([(0,-1),(0,1),(-1,0),(1,0)]):
      
      o_i, o_j = offset
      c_i, c_j = p_i + o_i, p_j + o_j
      
      if p_movement[movementindex] == 1: #if movement allowed
        state[3+player,c_i,c_j] = 1 #set the state layer to allowed
      
      elif j_movement[movementindex] != [0,0,0,0]:
        for jumpindex,jumpoffset in enumerate([(0,-1),(0,1),(-1,0),(1,0)]):
          if j_movement[movementindex][jumpindex] == 1:
            jump_i, jump_j = jumpoffset
            j_i, j_j = c_i + jump_i, c_j + jump_j
            state[3+player,j_i,j_j] = 1
    
    return state

  @staticmethod
  def set_wall_location(state,i,j,walldir,player):

    """For Layers 5 and 6 """

    state = state.copy()
    state[quoridorvars.BLACK_V_WALL_CHNL+(player*2)+walldir-1,i,j] = 1
    return state

  @staticmethod
  def set_invalid_placement(state,walldir):

    """For Layers 7 and 8 """

    state = state.copy()
    state[quoridorvars.INVALID_V_WALL_CHNL-1+walldir,:,:] = 0
    m, n = state_utils.get_board_size(state)
    for i in range(m):
      for j in range(n):
        state[quoridorvars.INVALID_V_WALL_CHNL-1+walldir,i,j] = QuoridorGame.invalid_wall_placement(state,i,j,walldir)
    return state

  @staticmethod
  def set_path(state,player):

    """ For Layers 9 and 10 """

    state = state.copy()
    state[quoridorvars.BLACKASTAR_CHNL+player,:,:] = 0
    p_i, p_j = QuoridorGame.get_player_pos(state,player)
    for path_i,path_j in QuoridorGame.astar(state,p_i,p_j,player):
      state[quoridorvars.BLACKASTAR_CHNL+player,path_i,path_j] = 1
    return state

  @staticmethod
  def set_gameover(state):

    """ For Layer 11 """

    state = state.copy()
    if QuoridorGame.get_game_ended(state):
      state[quoridorvars.GAMEOVER_CHNL,:,:] = 1
    else:
      state[quoridorvars.GAMEOVER_CHNL,:,:] = 0
    
    return state

#endregion    















  

