import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

from gym_quoridor import enums, quoridorvars, rendering
from gym_quoridor.quoridorgame import QuoridorGame

class QuoridorEnv(gym.Env):
  metadata = {'render.modes': ['terminal','human'] }
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
    self.last_state = self.state
    self.last_action = action
    self.state = QuoridorGame.get_next_state(self.state, action)
    self.done = QuoridorGame.get_game_ended(self.state)
    return self.state, self.get_reward(self.state,self.last_state), self.done, self.get_info()

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
    #---TO DO----
    # white path - As a list
    # black path - As a list
    # heuristic reward
    # real reward
    # invalid reward
    # invalid bool
    # move notation eg. MOVE A4,B4 and PLACE A4V

    return {}

  def __str__(self):
    string = QuoridorGame.__str__(self.state)+"\n"+QuoridorGame.__str__(self.last_state)+"\n Reward:"+str(self.get_reward(self.state,self.last_state))+"\nActionNum:"+str(self.last_action)
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

  #def close(self):
  #  if hasattr(self, 'window'):
  #    assert hasattr(self, 'pyglet')
  #    self.window.close()
  #    self.pyglet.app.exit() 

  def render(self, mode='terminal'):
    if mode == 'terminal':
      print(self.__str__())
    elif mode == 'human':

      window_width = 800
      window_height = 600

      import pyglet
      from pyglet.window import mouse
      from pyglet.window import key

      screen = pyglet.canvas.get_display().get_default_screen()

      window = pyglet.window.Window(window_width, window_height)
      self.window = window
      self.pyglet = pyglet

      self.action_state = "MOVE"
      
        # Set Cursor      
      cursor = self.window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
      self.window.set_mouse_cursor(cursor)

      self.user_action = None
      
      self.offset = 50


      @window.event
      def on_draw():
        pyglet.gl.glClearColor(0.7, 0.5, 0.3, 1)
        window.clear()

        pyglet.gl.glLineWidth(3)
        batch = pyglet.graphics.Batch()
        rendering.draw_grid(window_height/2, window_height/2, window_height, window_height, self.state,self.offset )
        rendering.draw_players(window_height/2, window_height/2, window_height, window_height, self.state, self.offset )
        rendering.draw_potential_move(window_height/2, window_height/2, window_height, window_height, self.state, self.offset )
        rendering.draw_path(window_height/2, window_height/2, window_height, window_height, self.state, self.offset)
        rendering.draw_action_state(window_height/2, window_height/2, window_height, window_height, self.state, self.offset ,self.action_state)
        rendering.draw_walls(window_height/2, window_height/2, window_height, window_height, self.state, self.offset)
        if self.action_state == "DEBUG":
          rendering.draw_invalid_walls(window_height/2, window_height/2, window_height, window_height, self.state, self.offset)
        batch.draw()

      @window.event
      def on_mouse_motion(x, y, dx, dy):
        #this is for debugging
        insidegrid = x >= 20 and x <= 571 and y >= 20 and y <= 571
        print(f"InsideGrid?{insidegrid},{x},{y}")
        if insidegrid:
          if self.action_state == "MOVE":
            #playermovement
            deltaw = (window_height-50)//self.size
            deltah = (window_height-50)//self.size
            grid_x = x - 50
            grid_y = y - 50
            x_coord = round(grid_x / deltaw)
            y_coord = round(grid_y / deltah)
            player = QuoridorGame.get_player_turn(self.state)
            dx_coord,dy_coord = QuoridorGame.movement_offset(self.state,x_coord,y_coord,player)
            print(f"PlayerMovement{dx_coord,dy_coord},{x_coord,y_coord},{QuoridorGame.movement_to_action(self.state,dx_coord,dy_coord)},{QuoridorGame.valid_move(self.state,QuoridorGame.movement_to_action(self.state,dx_coord,dy_coord))}",QuoridorGame.movement_around_pos(self.state,x_coord,y_coord),QuoridorGame.walls_around_pos(self.state,x_coord,y_coord))
          #wallplacement
          elif self.action_state == "PLACE_V" or self.action_state == "PLACE_H":
            deltaw = (window_height-50)//self.size
            deltah = (window_height-50)//self.size
            grid_x = x - 50-deltaw//2
            grid_y = y - 50-deltah//2
            x_coord = round(grid_x / deltaw)
            y_coord = round(grid_y / deltah)           
            if self.action_state == "PLACE_V":
              print(f"VWallPlacement{x_coord,y_coord,0},{QuoridorGame.placement_to_action(self.state,x_coord,y_coord,0)},{QuoridorGame.valid_placement(self.state,QuoridorGame.placement_to_action(self.state,x_coord,y_coord,0))}")
            else:
              print(f"HWallPlacement{x_coord,y_coord,1},{QuoridorGame.placement_to_action(self.state,x_coord,y_coord,1)},{QuoridorGame.valid_placement(self.state,QuoridorGame.placement_to_action(self.state,x_coord,y_coord,1))}")
          else:
            pass

      @window.event
      def on_mouse_press(x, y, button, modifiers):
        if button == mouse.LEFT:
          if x >= 25 and x <= window_height-50 and y >= 25 and y <= window_height-50:
            if self.action_state == "MOVE":
              deltaw = (window_height-50)//self.size
              deltah = (window_height-50)//self.size
              grid_x = x - 50
              grid_y = y - 50
              x_coord = round(grid_x / deltaw)
              y_coord = round(grid_y / deltah)
              player = QuoridorGame.get_player_turn(self.state)
              x_coord,y_coord = QuoridorGame.movement_offset(self.state,x_coord,y_coord,player)
              self.user_action = x_coord,y_coord
              self.user_action = QuoridorGame.movement_to_action(self.state,x_coord,y_coord)
              try:
                self.window.close()
                pyglet.app.exit()
              except:
                pass
            elif self.action_state == "PLACE_V":
              deltaw = (window_height-50)//self.size
              deltah = (window_height-50)//self.size
              grid_x = x - 25-deltaw//2
              grid_y = y - 25-deltah//2
              x_coord = round(grid_x / deltaw)
              y_coord = round(grid_y / deltah)           
              player = QuoridorGame.get_player_turn(self.state)
              self.user_action = x_coord,y_coord
              self.user_action = QuoridorGame.placement_to_action(self.state,x_coord,y_coord,0)
              try:
                self.window.close()
                pyglet.app.exit()
              except:
                pass
            elif self.action_state == "PLACE_H":
              deltaw = (window_height-50)//self.size
              deltah = (window_height-50)//self.size
              grid_x = x - 50-deltaw//2
              grid_y = y - 50-deltah//2
              x_coord = round(grid_x / deltaw)
              y_coord = round(grid_y / deltah)           
              player = QuoridorGame.get_player_turn(self.state)
              self.user_action = x_coord,y_coord
              self.user_action = QuoridorGame.placement_to_action(self.state,x_coord,y_coord,1)
              try:
                self.window.close()
                pyglet.app.exit()
              except:
                pass
            

              pass

      @window.event
      def on_mouse_scroll(x,y,scroll_x,scroll_y):
        if self.action_state == "MOVE":
          self.action_state = "PLACE_V"
        elif self.action_state == "PLACE_V":
          self.action_state = "PLACE_H"
        elif self.action_state == "PLACE_H":
          self.action_state = "DEBUG"
        else:
          self.action_state = "MOVE"
                
      @window.event
      def on_key_press(symbol, modifiers):
        if symbol == key.ESCAPE:
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
      
    elif mode == 'rgbarray':

      window_width = 600
      window_height = 600

      import pyglet
      from pyglet.window import mouse
      from pyglet.window import key

      screen = pyglet.canvas.get_display().get_default_screen()

      window = pyglet.window.Window(window_width, window_height)
      self.window = window
      self.pyglet = pyglet
  
        # Set Cursor      
      cursor = self.window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
      self.window.set_mouse_cursor(cursor)

      self.user_action = None
      
      self.offset = 50

      @window.event
      def on_draw():
        pyglet.gl.glClearColor(0.7, 0.5, 0.3, 1)
        window.clear()
        pyglet.gl.glLineWidth(3)
        batch = pyglet.graphics.Batch()
        rendering.draw_grid(window_height/2, window_height/2, window_height, window_height, self.state,self.offset )
        rendering.draw_players(window_height/2, window_height/2, window_height, window_height, self.state, self.offset )
        rendering.draw_potential_move(window_height/2, window_height/2, window_height, window_height, self.state, self.offset )
        rendering.draw_path(window_height/2, window_height/2, window_height, window_height, self.state, self.offset)
        rendering.draw_action_state(window_height/2, window_height/2, window_height, window_height, self.state, self.offset ,self.action_state)
        rendering.draw_walls(window_height/2, window_height/2, window_height, window_height, self.state, self.offset)
        batch.draw()

      buffer = pyglet.image.get_buffer_manager().get_color_buffer()
      image_data = buffer.get_image_data()
      arr = np.frombuffer(image_data.get_data(), dtype=np.uint8)
      arr = arr.reshape(buffer.height, buffer.width, 4)
      arr = arr[::-1,:,0:3]

      return arr

    else:
      pass