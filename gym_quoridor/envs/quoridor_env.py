import gym
from gym import error, spaces, utils
from gym.utils import seeding
import sys
import random
import copy

class QuoridorEnv(gym.Env):
    metadata = {'render.modes':['human']}
    
    #color tuples
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

    MOVEMENT = {"UP":(-1,0),"DOWN":(1,0),"LEFT":(0,-1),"RIGHT":(0,1)}
    WALL_DIR = {"HORIZONTAL":1, "VERTICAL": 2}
    WALLCHECK = {"UP":("HORIZONTAL",["NE","NW"]),
                "DOWN":("HORIZONTAL",["SE","SW"]),
                "LEFT":("VERTICAL",["NW","SW"]),
                "RIGHT":("VERTICAL",["NE","SE"])}
    WALL_COMPASS = {"NW":(-1,-1),"NE":(0,-1),"SE":(-1,0),"SW":(0,0)}

    def __init__(self,seed=None):
        self.seed = seed
        if seed is None:
            self.seed = random.randint(0, sys.maxsize)
        self.array_height = 9
        self.array_width = 9
        self.window_height = 100*self.array_height
        self.window_width = 100*self.array_width

        self.action_space = spaces.Discrete((self.array_height*self.array_width)+(self.array_height-1)*(self.array_width-1)*2) #81movement+64*2wallplacement = 209
        self.observation_space = spaces.Dict({"board": spaces.MultiDiscrete([3 for i in range(self.array_height * self.array_width)]),
                                              "walls": spaces.MultiDiscrete([2 for i in range((self.array_height-1) * (self.array_width-1))]),
                                              "player_walls": spaces.Discrete(5),
                                              "opponent_walls": spaces.Discrete(5)})

        self.reset()

    def step(self,action):

        action += 1 #add one due to Discrete action_space
        #check within actionspace
        if action <= 0 or action >= 210:
            raise Exception("Invalid action: {}".format(action))

        self.last_board = copy.deepcopy(self.board)
        self.last_walls = copy.deepcopy(self.walls)
        

        done = self._is_over()
        state = self._get_game_state()
        reward = 0
        
        return state,reward,done, {}

    def reset(self):
        self.board, self.walls = self._make_blank_board()
        self.player_walls = 5
        self.opponent_walls = 5
        
        #for rendering
        self.screen = None
        self.last_board = copy.deepcopy(self.board)
        self.last_walls = copy.deepcopy(self.walls)
        return self._get_game_state()

    def render(self, mode='human',close=False):
        """
        This function renders the current game state in the given mode.
        """
        if mode == 'console':
            print(self._get_game_state)
        elif mode == 'human':
            try:
                import pygame
                from pygame import gfxdraw
            except ImportError as e:
                raise error.DependencyNotInstalled(f"{e}.Install pygame using 'pip install pygame'")
            if close:
                pygame.quit()
            else:
                if self.screen is None:
                    pygame.init()
                    self.screen = pygame.display.set_mode(round(self.window_width),round(self.window_height))
                clock = pygame.time.Clock()

            self.screen.fill((255,255,255))

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
        return state

    def _get_reward(self):
        pass

    def _valid_actions(self,state):
        pass

    def _find_player_pos(self,state):
        for row in self.array_height:
            for col in self.array_width:
                if state["board"][row][col] == 1:
                    return row, col

    def _find_opponent_pos(self,state):
        for row in self.array_height:
            for col in self.array_width:
                if state["board"][row][col] == 2:
                    return row, col

    def _walls_around_pos(self,state,pos):
        midrow, midcol = pos
        walls_bool = [None,None,None,None]
        walls_pos = [None,None,None,None]
        walls_check = [(-1,-1),(0,-1),(-1,0),(0,0)]
        walls_angle = [None,None,None,None]
        
        for wallint in range(len(walls)): #TL, TR
            r_check, c_check = walls_check[wallint]
            r_check += midrow
            c_check += midcol
            try:
                if self.walls[r_check][c_check] != 0:
                    walls_bool[wallint] = True
                    walls_angle[wallint] = self.walls[r_check][c_check]
                else:
                    walls_bool[wallint] = False
                walls_pos[wallint] = (r_check,c_check)
            except:
                walls_bool[wallint] = None
        return walls_bool,walls_pos,walls_angle

    def _allowed_move(self,state):
        playerpos = self._find_player_pos(state)
        for row in self.array_height:
            for col in self.array_width:
                pass
                
    def _is_over(self):
        return False



if __name__ == "__main__":
    env = QuoridorEnv()
    act = 1
    env.step(1)
    