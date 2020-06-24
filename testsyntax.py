import numpy as np
from gym_quoridor.quoridorgame import QuoridorGame
from gym_quoridor.envs import QuoridorEnv

env = QuoridorEnv()
env.step(env.action_space.sample())
# gamestate = QuoridorGame.get_init_board(5)

# gamestate = QuoridorGame.set_wall_location(gamestate,1,1,2,1) #Vertical wall by White at 0,2
# gamestate = QuoridorGame.set_path(gamestate,0)
# gamestate = QuoridorGame.set_path(gamestate,1)
# gamestate = QuoridorGame.set_invalid_placement(gamestate,1)
# gamestate = QuoridorGame.set_invalid_placement(gamestate,2)

# def print_array(array,axis=None):
#   orig = array.copy()
#   try:
#     array = np.rot90(array,axes=[1,2])
#     array = np.flip(array,axis=1)
#     print(array)
#   except:
#     array = np.rot90(array,axes=[0,1])
#     array = np.flip(array,axis=0)
#     print(array)


# #newarray = np.zeros((11,9,9))
# #for m in range(9):
# #  for n in range(9):
# #    newarray[0,m,n] = m
# #    newarray[1,m,n] = n+1 * 16

# #print(newarray)
# #print("---")
# #print_array(newarray)

# print("Player Loc")
# print_array(gamestate[0,:,:]+gamestate[1,:,:]*2)
# print("Player Path")
# print_array(gamestate[11,:,:]+gamestate[12,:,:]*2)
# print("----")
# vertwallarray = gamestate[5,:-1,:-1] + gamestate[7,:-1,:-1]
# horiwallarray = gamestate[6,:-1,:-1] + gamestate[8,:-1,:-1]

# print_array(vertwallarray+horiwallarray*2)

# invalidwall = gamestate[9,:-1,:-1] + gamestate[10,:-1,:-1]*2

# print_array(invalidwall)

# print("--")
# gamestate[2,0,1] = 9
# print_array(gamestate[2])
# #print(QuoridorGame.walls_around_walls(gamestate,0,1))

