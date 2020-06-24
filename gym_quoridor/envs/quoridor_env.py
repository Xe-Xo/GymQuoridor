import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

from gym_quoridor import enums, quoridorvars
from gym_quoridor.quoridorgame import QuoridorGame

class QuoridorEnv(gym.Env):
  metadata = {'render.modes': ['terminal'] }
  quoridorgame = QuoridorGame()

  def __init__(self,size=9,reward_method='real'):
    '''
    @param reward_method: either 'heuristic' or 'real'
    heuristic: len of black path - len of white path.
    real: gives 0 for in-game move, 1 for winning, -1 for losing,
    0 for draw, all from black player's perspective
    '''

    self.size = size #default is 9
    self.state = QuoridorGame.get_init_board(size)
    self.reward_method = enums.RewardMethod(reward_method)
    self.observation_space = gym.spaces.Box(np.float32(0), np.float32(1),
                                                shape=(quoridorvars.NUM_CHNLS, size, size))
    self.action_space = spaces.Discrete(QuoridorGame.get_action_size(self.state))
    self.done = False

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

    self.state = QuoridorGame.get_next_state(self.state, action)
    self.done = QuoridorGame.get_game_ended(self.state)
    return np.copy(self.state), self.get_reward(), self.done, self.get_info()


  def game_ended(self):
    return self.done

  def turn(self):
    return QuoridorGame.get_turn(self.state)



  #TO DO

  def get_state(self):
    return np.copy(self.state)

  def get_reward(self):
    pass

  def get_info(self):
    pass

  def action_to_wall_movement(self):
    pass  

  def __str__(self):
    return QuoridorGame.str(self.state)

  def close(self):
    if hasattr(self, 'window'):
      assert hasattr(self, 'pyglet')
      self.window.close()
      self.pyglet.app.exit() 

  def render(self, mode='terminal'):
      if mode == 'terminal':
        print(self.__str__())
      #TO DO -- ADD PYGLET WINDOW