import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

from gym_quoridor import enums, quoridorvars, rendering
from gym_quoridor.quoridorgame import QuoridorGame

class QuoridorEnv(gym.Env):
  metadata = {'render.modes': ['terminal'] }
  quoridorgame = QuoridorGame()

  def __init__(self,size=9,reward_method='invalid'):
    '''
    @param reward_method: either 'heuristic' or 'real'
    heuristic: len of black path - len of white path.
    real: gives 0 for in-game move, 1 for winning, -1 for losing,
    0 for draw, all from black player's perspective
    '''

    self.size = size #default is 9
    self.state = QuoridorGame.get_init_board(size)
    self.last_state = np.copy(self.state)
    self.reward_method = enums.RewardMethod(reward_method)
    self.observation_space = gym.spaces.Box(np.float32(0), np.float32(1),
                                                shape=(quoridorvars.NUM_CHNLS, size, size))
    self.action_space = spaces.Discrete(QuoridorGame.get_action_size(self.state))
    self.done = False
    self.last_action = None
    self.window = None

  def reset(self):
    '''
    Reset state, quoridor board, current_player, done, return state
    '''
    self.state = QuoridorGame.get_init_board(self.size)
    self.done = False
    return np.copy(self.state)

  def step(self,action):
    '''
    Assumes the correct player is making a move. Black goes first
    return observation, reward, done, info
    '''

    assert not self.done

    self.last_state = np.copy(self.state)
    self.last_action = action
    self.state = QuoridorGame.get_next_state(self.state, action)
    self.done = QuoridorGame.get_game_ended(self.state)
    return np.copy(self.state), self.get_reward(self.state,self.last_state), self.done, self.get_info()


  def game_ended(self):
    return self.done

  def turn(self):
    return QuoridorGame.get_player_turn(self.state)

  def get_state(self):
    return np.copy(self.state)

  def get_reward(self,state=None,laststate=None):
    
    if state is None:
      state = self.state
    if laststate is None:
      laststate = self.last_state
    p = QuoridorGame.get_player_turn(laststate)

    #potentially rewrite this to be more efficient
    if self.reward_method == enums.RewardMethod.REAL:
      return QuoridorGame.get_game_winner(state,p) * 15
    elif self.reward_method == enums.RewardMethod.HEURISTIC:
      if QuoridorGame.get_game_ended(state):
        return QuoridorGame.get_game_winner(state,p) * 15
      else:
        currentpathdif = QuoridorGame.get_path_len(state,p)-QuoridorGame.get_path_len(state,1-p)
        lastpathdif = QuoridorGame.get_path_len(laststate,p)-QuoridorGame.get_path_len(laststate,1-p)
        return currentpathdif - lastpathdif
    elif self.reward_method == enums.RewardMethod.INVALID:
      if QuoridorGame.get_game_ended(state):
        return QuoridorGame.get_game_winner(state,p) * 15
      elif np.equal(state,laststate).all() == False:
        return -1 
      else:
        currentpathdif = QuoridorGame.get_path_len(state,p)-QuoridorGame.get_path_len(state,1-p)
        lastpathdif = QuoridorGame.get_path_len(laststate,p)-QuoridorGame.get_path_len(laststate,1-p)
        return currentpathdif - lastpathdif

  def get_info(self):

    #Diagnostic information useful for debugging
    #official evaluations of agent should not be using this for learning
    #TO DO
    # white path - As a list
    # black path - As a list
    # heuristic reward
    # real reward
    # invalid reward
    # invalid bool
    # move notation eg. MOVE A4,B4 and PLACE A4V

    return {}

  def __str__(self):
    string = QuoridorGame.__str__(self.state)+"\n Reward:"+str(self.get_reward(self.state,self.last_state))+"\nActionNum:"+str(self.last_action)
    try:
      string += "\nValidMove:"+str(QuoridorGame.valid_move(self.last_state,self.last_action))
    except:
      pass

    try:
      string += "\nValidPlacement:"+str(QuoridorGame.valid_placement(self.last_state,self.last_action))
    except:
      pass

    string += "\nGameOver:"+str(self.game_ended())

    return string

  def close(self):
    if hasattr(self, 'window'):
      assert hasattr(self, 'pyglet')
      self.window.close()
      self.pyglet.app.exit() 

  def render(self, mode='terminal'):
    if mode == 'terminal':
      print(self.__str__())
    elif mode == 'human':

      window_width = 800
      window_height = 600

      if self.window is None:
        import pyglet
        from pyglet.window import mouse
        from pyglet.window import key

        screen = pyglet.canvas.get_display().get_default_screen()

        window = pyglet.window.Window(window_width, window_height)
        self.window = window
        self.pyglet = pyglet
      
        # Set Cursor
        
      window = self.window
      pyglet = self.pyglet
      cursor = self.window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
      self.window.set_mouse_cursor(cursor)

      self.user_action = None

 

      # Outlines
      
      lower_grid_coord = window_width * 0.075
      board_size = window_width * 0.85
      upper_grid_coord = board_size + lower_grid_coord
      delta = board_size / (self.size)
      piece_r = delta / 3.3  # radius

      @window.event
      def on_draw():
          pyglet.gl.glClearColor(0.7, 0.5, 0.3, 1)
          window.clear()

          pyglet.gl.glLineWidth(3)
          batch = pyglet.graphics.Batch()

          #rendering.draw_rectangle(window_height//2,window_height//2,window_height,window_height,(0.5,0.5,0.5),batch=batch)
          rendering.draw_grid(window_height/2, window_height/2, window_height, window_height, self.state,50)
#          rendering.draw_v_walls(window_height/2, window_height/2, window_height, window_height, self.state, 50, batch=batch)
#          rendering.draw_h_walls(window_height/2, window_height/2, window_height, window_height, self.state, 50, batch=batch)
          rendering.draw_players(window_height/2, window_height/2, window_height, window_height, self.state, 50)
#          rendering.draw_potential_v_walls(window_height/2, window_height/2, window_height, window_height, self.state, 50, batch=batch)
#          rendering.draw_potential_h_walls(window_height/2, window_height/2, window_height, window_height, self.state, 50, batch=batch)
          rendering.draw_potential_move(window_height/2, window_height/2, window_height, window_height, self.state, 50)
          rendering.draw_path(window_height/2, window_height/2, window_height, window_height, self.state, 50)
          batch.draw()

          # draw the pieces
          #rendering.draw_pieces(batch, lower_grid_coord, delta, piece_r, self.size, self.state)

      @window.event
      def on_mouse_press(x, y, button, modifiers):
          if button == mouse.LEFT:
              grid_x = (x - lower_grid_coord)
              grid_y = (y - lower_grid_coord)
              x_coord = round(grid_x / delta)
              y_coord = round(grid_y / delta)
              try:
                self.user_action = (x_coord, y_coord)
              except:
                pass

      @window.event
      def on_key_press(symbol, modifiers):
        if symbol == key.P:
          self.window.close()
          pyglet.app.exit()
          self.user_action = None
        elif symbol == key.R:
          self.reset()
          self.window.close()
          pyglet.app.exit()
        elif symbol == key.E:
          self.window.close()
          pyglet.app.exit()
          self.user_action = -1

      @window.event
      def on_close():
        self.window.close()
        pyglet.app.exit()
        self.user_action = -1



      pyglet.app.run()

      return self.user_action