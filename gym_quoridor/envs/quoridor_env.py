import gym
from gym import error, spaces, utils
from gym.utils import seeding
import sys
import random
import copy
from gym_quoridor.envs.enums import Color, WallDir, MovementDir,MovementIndex, CompassDir, PlayerState, CompassIndex

class QuoridorEnv(gym.Env):
    metadata = {'render.modes':['human']}
    
    def __init__(self,seed=None):
        self.array_height = 9
        self.array_width = 9
        self.turn = 1
        self.reset()
        self.player_endpos_list = []
        self.opponent_endpos_list = []
        for x in range(self.array_width):
            self.player_endpos_list.append((x,self.array_height-1))
            self.opponent_endpos_list.append((x,0))

    def step(self,action):

        
        #last_state = copy.deepcopy(self.get_game_state())
        
        done = self._is_over()
        state = self._get_game_state()
        reward = 0
        
        return state,reward,done, {}

    def next_turn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

    def reset(self):
        self.board, self.walls = self._make_blank_board()
        self.player_walls = 5
        self.opponent_walls = 5
        self.last_board = copy.deepcopy(self.board)
        self.last_walls = copy.deepcopy(self.walls)
        return self._get_game_state()

    def render(self):
        """
        This function renders the current game state in the given mode.
        """

        print("   "+" - ".join(str(num) for num in range(5)))

        for y,board_line in enumerate(self.board):
            print(str(y)+"| "+ " | ".join(str(item) for item in board_line)+ " |")
            try:
                print("     "+ "   ".join(str(item) for item in self.walls[y]))
            except:
                pass

    def render_state(self,state):
        print("Rendering State")
        print("   "+" - ".join(str(num) for num in range(5)))

        for y,board_line in enumerate(state['board']):
            print(str(y)+"| "+ " | ".join(str(item) for item in board_line)+ " |")
            try:
                print("     "+ "   ".join(str(item) for item in state['walls'][y]))
            except:
                pass

    def state_eq(self,state,other):
        return state == other

    def _make_blank_board(self):
        boardarray = []
        wallsarray = []
        
        for _ in range(self.array_height):
            column = []
            for _ in range(self.array_width):
                column.append(0)
            boardarray.append(column)
        
        for _ in range(self.array_height-1):
            column = []
            for _ in range(self.array_width-1):
                column.append(0)
            wallsarray.append(column)
        
        midcol = round(self.array_width/2)
        boardarray[0][midcol] = 1
        boardarray[self.array_height-1][midcol] = 2

        return boardarray, wallsarray

    def _get_game_state(self):
        """
        This function returns the current game state.
        """
        state = {}
        state["board"] = self.board
        state["walls"] = self.walls
        state["player_walls"] = self.player_walls
        state["opponent_walls"] = self.opponent_walls
        state["turn"] = self.turn
        return state

    def _get_reward(self,state,laststate):
        try:
            return self.path_len_dif(state) - self.path_len_dif(laststate)
        except:
            return -15 #Pathing Broke

    def _valid_action(self,state,player,action):
        pass

    def _find_player_pos(self,state,player):
        for row in range(self.array_height):
            for col in range(self.array_width):
                if state["board"][col][row] == player:
                    return row, col

    def _player_movement(self,state,player):
        playerpos = self._find_player_pos(state,player)      
        movement_bool,movementpos,_ = self._allowed_movement(state,playerpos)

        player_movement_pos = []

        for moveid, move_bool in enumerate(movement_bool):
            if move_bool:
                player_movement_pos.append(movementpos[moveid])

        jumpbool, jumppos_start = self._allowed_jump(state,playerpos)
        if jumpbool:
            player_movement_pos.remove(jumppos_start)
            movement_bool,jumppos,_ = self._allowed_movement(state,jumppos_start)
            for moveid, move_bool in enumerate(movement_bool):
                if move_bool:
                    if jumppos[moveid] != playerpos:
                        player_movement_pos.append(jumppos[moveid])

        return player_movement_pos

    def _player_placement(self,state,player):
        """ Return the Valid Placement Locations """
        wallplacements = []        

        if player == 1 and state['player_walls'] == 0:
            return []
        elif player == 2 and state['opponent_walls'] == 0:
            return []
        else:
            pass

        return wallplacements

    def _walls_around_walls(self,state,wallpos):
        walls_check = [MovementDir['UP'].value,MovementDir['DOWN'].value,MovementDir['LEFT'].value,MovementDir['RIGHT'].value]
        walls_bool = [None,None,None,None]
        walls_pos = [None,None,None,None]
        walls_angle = [None,None,None,None]

        for wallint in range(len(walls_check)): #TL, TR
            r_check, c_check = walls_check[wallint]
            r_check += wallpos[0]
            c_check += wallpos[1]
            try:
                if state['walls'][c_check][r_check] != 0:
                    walls_bool[wallint] = True
                    walls_angle[wallint] = self.walls[c_check][r_check]
                else:
                    walls_bool[wallint] = False
                walls_pos[wallint] = (r_check,c_check)
            except IndexError:
                walls_bool[wallint] = None
        return walls_bool,walls_pos,walls_angle
        
    def _walls_around_pos(self,state,pos):
        midrow, midcol = pos
        walls_bool = [None,None,None,None]
        walls_pos = [None,None,None,None]
        walls_check = [(-1,-1),(0,-1),(-1,0),(0,0)] #NW, NE, SW, SE
        walls_angle = [None,None,None,None]
        
        for wallint in range(len(walls_check)): #TL, TR
            r_check, c_check = walls_check[wallint]
            r_check += midrow
            c_check += midcol
            if r_check < 0 or r_check >= self.array_width -1 or c_check < 0 or c_check >= self.array_height -1:
                walls_bool[wallint] = None
            else:
                if state['walls'][c_check][r_check] != 0:
                    walls_bool[wallint] = True
                    walls_angle[wallint] = state['walls'][c_check][r_check]
                else:
                    walls_bool[wallint] = False
                walls_pos[wallint] = (r_check,c_check)

        return walls_bool,walls_pos,walls_angle

    def _board_around_pos(self,state,pos):
        boards_bool = [False,False,False,False]
        boards_pos = [None,None,None,None]
        boards_check = [MovementDir.UP,MovementDir.DOWN,MovementDir.LEFT,MovementDir.RIGHT]
        boards_value = [None,None,None,None]
        posx, posy = pos
        for moveidx, movedir in enumerate(boards_check):
            move_x, move_y = movedir.value
            new_x, new_y = posx+move_x, posy+move_y
            if new_x < 0 or new_x >= self.array_width or new_y < 0 or new_y >= self.array_height:
                boards_value[moveidx] = None
                boards_bool[moveidx] = False
                boards_pos[moveidx] = (new_x, new_y)
            else:
                boards_value[moveidx] = state['board'][new_y][new_x]
                boards_bool[moveidx] = True
                boards_pos[moveidx] = (new_x, new_y)
            
        return boards_bool, boards_pos, boards_value

    def _allowed_movement(self,state,pos):

        """ Method to return whether movement in direction is allowed from a position"""
        # ["UP","DOWN","LEFT","RIGHT"]
        # ["NW","NE","SW","SE"]

        
        walls_bool,walls_pos,walls_angle = self._walls_around_pos(state,pos)
        boards_bool, boards_pos, boards_value = self._board_around_pos(state,pos)
        movement_allowed = boards_bool

        #Check if a Wall blocks movement

        for wall_id, wall_bool in enumerate(walls_bool):
            if wall_bool:
                if walls_angle[wall_id] == WallDir['HORIZONTAL']: #HORIZONTAL
                    #print(wall_id)
                    if wall_id == CompassIndex['NW'] or wall_id == CompassIndex['NE']: #if wall is in the NW or NE pos
                        movement_allowed[MovementIndex['UP']] = False #stop movement up
                    elif wall_id == CompassIndex['SW'] or wall_id == CompassIndex['SE']: #if wall is in SW or SE pos
                        movement_allowed[MovementIndex['DOWN']] = False #stop movement down
                    else:
                        pass
                elif walls_angle[wall_id] == WallDir['VERTICAL']: #VERTICAL
                    if wall_id == CompassIndex['NW'] or wall_id == CompassIndex['SW']: #if wall is in NW or SW pos
                        movement_allowed[MovementIndex['LEFT']] = False #stop movement leftto sen
                    elif wall_id == CompassIndex['NE'] or wall_id == CompassIndex['SE']: #if wall is in NE or SE pos
                        movement_allowed[MovementIndex['RIGHT']] = False
       
        #print(f"pos{pos}->{boards_pos,movement_allowed}")
        return movement_allowed, boards_pos, boards_value

    def _allowed_jump(self,state,pos):

        jump_bool = False
        jumpfrom_pos = None
        
        posx, posy = pos
        if state['board'][posy][posx] == PlayerState.NONE:
            return jump_bool, jump_bool
        playerindex = state['board'][posy][posx]
        if playerindex == PlayerState.PLAYER:
            otherplayerindex = PlayerState.OPPONENT.value
        else:
            otherplayerindex = PlayerState.PLAYER.value

        movement_allowed, board_pos, board_value = self._allowed_movement(state,pos)
        for movementindex, movement_bool in enumerate(movement_allowed):
            if movement_bool:
                if board_value[movementindex] == otherplayerindex:
                    return True, board_pos[movementindex]
        
        return jump_bool, jumpfrom_pos

    def _allowed_placement(self,state,wallpos,walldir):
        walls_bool, walls_pos, walls_dir = self._walls_around_walls(state,wallpos)
        if walldir in walls_dir:
            if walldir == WallDir['HORIZONTAL']:
                if walls_dir[MovementIndex['LEFT'].value] == walldir or walls_dir[MovementIndex['RIGHT'].value] == walldir:
                    return False
            elif walldir == WallDir['VERTICAL']:
                if walls_dir[MovementIndex['UP'].value] == walldir or walls_dir[MovementIndex['DOWN'].value] == walldir:
                    return False
        return True

    def _blocked_exit_wall(self,state,wallpos,walldir):
        newstate = self.copy_state(state)
        newstate['walls'][wallpos[1]][wallpos[0]] = walldir
        #self.render_state(newstate)
        return self.no_maze(newstate)
        
    def copy_state(self,state):
        return copy.deepcopy(state)

    def astar(self,state,startpos,endpos_list):
        
        #create start Nodes
        start_node = GridNode(None,startpos)
        start_node.g = start_node.h = start_node.f = 0

        #multiple end positions so making multiple end Nodes
        end_list = []
        for endpos in endpos_list:
            end_node = GridNode(None,endpos)
            end_node.g = end_node.h = end_node.f = 0
            end_list.append(end_node)

        #Initialise the two lists (open (unseen) and closed (seen))
        open_list = []
        closed_list = []

        #Add start node

        open_list.append(start_node)

        while len(open_list) > 0:
            #print(open_list)
            
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
                    return path[::-1]

            #Not at end_node! check next nodes

            children = []
            movement_allowed, boards_pos, boards_value = self._allowed_movement(state,current_node.position)
            for index, pos in enumerate(boards_pos):
                if movement_allowed[index]:
                    
                    new_node = GridNode(current_node, pos)
                    children.append(new_node)

            for child in children:
                if child in closed_list:
                    continue
                else:
                    child.g = current_node.g + 1

                    #get lowest h value
                    min_h_value = self.array_height ** 2 + self.array_width ** 2
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

    def current_path(self,state,player):
        if player == 1:
            return self.astar(state,self._find_player_pos(state,player),self.player_endpos_list)
        elif player == 2:
            return self.astar(state,self._find_player_pos(state,player),self.opponent_endpos_list)
        else:
            return None

    def no_maze(self,state):
        # returns True if there is no path to finish
        #print(self.current_path(state,1))
        #print(self.current_path(state,2))
        return self.current_path(state,1) is None or self.current_path(state,2) is None

    def _is_over(self,state):
        return self.no_maze(state) or self.loc_at_finish(state,1) or self.loc_at_finish(state,2)

    def loc_at_finish(self,state,player):
        if player == 1:
            return self._find_player_pos(state,player) in self.player_end_pos
        else:
            return self._find_player_pos(state,player) in self.opponent_end_pos

    def path_len_dif(self,state):
        try:
            return len(self.current_path(state,1)) - len(self.current_path(state,2))
        except TypeError:
            return None

    def placement_to_action(self,wallpos,walldir):
        #Action is a Discrete!
        #First 4 is movement Second 8 is Jump Movements, remaining self.height-1 x self.width-1 = Wallpos locations
        return (wallpos[1] * self.array_width-1 + wallpos[0])*walldir + 12

    def movement_to_action(self,startpos,endpos):
        sx,sy = startpos
        ex,ey = endpos
        try:
            return MovementIndex[MovementDir((ex - sx, ey - sy)).name].value
        except Exception as e:
            print(e)
            return None

    def action_to_movementplacement(self,action):
        if action < 12:
            return MovementDir[MovementIndex(action).name].value, None
        else:
            return None, ((action-12) % (self.array_width-1), (action-12-((action-12) % (self.array_width-1)))//(self.array_width-1))


class GridNode():
    def __init__(self,parent=None,position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self,other):
        return self.position == other.position

    def __repr__(self):
        return f"{self.position}"

