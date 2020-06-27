import random
import unittest

import gym
import numpy as np

from gym_quoridor import quoridorvars
from gym_quoridor.quoridorgame import QuoridorGame

class TestGoEnv(unittest.TestCase):

  def setUp(self) -> None:
    self.env = gym.make('gym_quoridor:quoridor-v0', size=9, reward_method='real')

  def tearDown(self):
    self.env.close()

  def test_get_init_board(self):

    """Check Initial Board"""

    state = self.env.reset()

    teststate = np.array([
      [       #CHANNEL 0
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ], [  #CHANNEL 1
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ], [  #CHANNEL 2
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ], [  #CHANNEL 3
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 1, 0, 0, 0, 0, 0, 0, 0], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ], [  #CHANNEL 4
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [0, 0, 0, 0, 0, 0, 0, 1, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ], [  #CHANNEL 5
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ], [  #CHANNEL 6
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ], [  #CHANNEL 7
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ], [  #CHANNEL 8
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ], [  #CHANNEL 9
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ], [  #CHANNEL 10
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ], [  #CHANNEL 11
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 1, 1, 1, 1, 1, 1, 1, 1], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ], [  #CHANNEL 12
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [1, 1, 1, 1, 1, 1, 1, 1, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ], [  #CHANNEL 13
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]])
    
    for chnl in range(quoridorvars.NUM_CHNLS):
      for x in range(self.env.size):
        for y in range(self.env.size):
          with self.subTest(f"{chnl,x,y}"):
            self.assertEqual(state[chnl,x,y],teststate[chnl,x,y])

  def test_start_turn(self):

    """Check Black Starts"""
  
    state = self.env.reset()
    self.assertEqual(QuoridorGame.get_player_turn(state),0)

  def test_next_turn(self):

    """Check Next Turn Works correctly"""

    state = self.env.reset()
    state, _, _,_ = self.env.step(1)
    self.assertEqual(QuoridorGame.get_player_turn(state),1)

  def test_place_v_wall(self):
    for x in range(self.env.size-1): #self.env.size-1
      for y in range(self.env.size-1): #self.env.size-1
        for turn in range(2):
          state = self.env.reset()
          if turn == 1:
            state,_,_,_ = self.env.step(1)
            action = QuoridorGame.placement_to_action(state,x,y,0)
            state, _, _, _ = self.env.step(action)
            with self.subTest(f"{quoridorvars.WHITE_V_WALL_CHNL,x,y}=1,{action},{turn}"):
              self.assertEqual(state[quoridorvars.WHITE_V_WALL_CHNL,x,y],1)
            pass
          else:
            action = QuoridorGame.placement_to_action(self.env.state,x,y,0)
            state, _, _, _ = self.env.step(action)
            with self.subTest(f"{quoridorvars.BLACK_V_WALL_CHNL,x,y}=1,{action}-->{x,y},{turn},{QuoridorGame.__str__(state)}"):
              self.assertEqual(state[quoridorvars.BLACK_V_WALL_CHNL,x,y],1)


  def test_place_h_wall(self):
    for x in range(self.env.size-1): #self.env.size-1
      for y in range(self.env.size-1): #self.env.size-1
        for turn in range(2):
          state = self.env.reset()
          if turn == 1:
            state, _, _, _ = self.env.step(1)
            action = QuoridorGame.placement_to_action(self.env.state,x,y,1)
            state, _, _, _ = self.env.step(action)
            with self.subTest(f"{quoridorvars.WHITE_H_WALL_CHNL,x,y}=1,{action},{turn}"):
              self.assertEqual(state[quoridorvars.WHITE_H_WALL_CHNL,x,y],1)
          else:
            action = QuoridorGame.placement_to_action(self.env.state,x,y,1)
            state, _, _, _ = self.env.step(action)
            with self.subTest(f"{quoridorvars.BLACK_H_WALL_CHNL,x,y}=1,{action},{turn}"):
              self.assertEqual(state[quoridorvars.BLACK_H_WALL_CHNL,x,y],1)

  def test_place_walls_on_existing_walls(self):
    for x in range(self.env.size-1):
      for y in range(self.env.size-1):
        for walltype1 in range(2):
          for walltype2 in range(2):
            state = self.env.reset()
            action = QuoridorGame.placement_to_action(state,x,y,walltype1)
            state, _, _, _ = self.env.step(action)
            action2 = QuoridorGame.placement_to_action(state,x,y,walltype2)
            state, _, _, _ = self.env.step(action2)
            total = 0
            for chnl in range(quoridorvars.BLACK_V_WALL_CHNL,quoridorvars.WHITE_H_WALL_CHNL+1):
              total += state[chnl,x,y]
            with self.subTest(f"{x,y,walltype1,walltype2}=>{total}==1,{action,action2},samewalls!{walltype1==walltype2}{state[quoridorvars.BLACK_V_WALL_CHNL,x,y]}{state[quoridorvars.BLACK_H_WALL_CHNL,x,y]}{state[quoridorvars.WHITE_V_WALL_CHNL,x,y]}{state[quoridorvars.WHITE_H_WALL_CHNL,x,y]}"):
              self.assertEqual(total,1)

  def test_invalid_placement_for_walls(self):
    for x in range(self.env.size-1):
      for y in range(self.env.size-1):
        for walltype1 in range(2):
          for walltype2 in range(2):
            state = self.env.reset()
            action = QuoridorGame.placement_to_action(state,x,y,walltype1)
            b,i,j,d = QuoridorGame.valid_placement(state,action)
            self.assertTrue(b)
            self.assertEqual(x,i)
            self.assertEqual(y,j)
            self.assertEqual(walltype1,d)
            state, _, _, _ = self.env.step(action)
            action2 = QuoridorGame.placement_to_action(state,x,y,walltype2)
            b,i,j,d = QuoridorGame.valid_placement(state,action2)
            self.assertFalse(b)
            self.assertEqual(x,i)
            self.assertEqual(y,j)
            self.assertEqual(walltype2,d)




            


          



if __name__ == '__main__':
  unittest.main()
