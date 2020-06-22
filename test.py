
from gym_quoridor.envs.quoridor_env import QuoridorEnv
from gym_quoridor.envs.enums import PlayerState, WallDir

if __name__ == "__main__":
    env = QuoridorEnv()
    
    #player placement
#    env.board[0][2] = PlayerState.NONE.value
#    env.board[4][2] = PlayerState.NONE.value
#    env.board[1][2] = PlayerState.PLAYER.value
#    env.board[2][2] = PlayerState.OPPONENT.value

    #wall placement
#    env.walls[3][2] = WallDir.HORIZONTAL.value
#    env.walls[2][1] = WallDir.VERTICAL.value
#    env.walls[1][2] = WallDir.VERTICAL.value

    #env.render()

    #print(env._walls_around_pos(env._get_game_state(),(2,4)))
    #print(env._allowed_jump(env._get_game_state(),(2,3)))
    #print(env._walls_around_walls(env._get_game_state(),(3,3)))
    #print(env._allowed_placement(env._get_game_state(),(3,3),1))
    #print(env._allowed_placement(env._get_game_state(),(3,3),2))
    #print(env._allowed_movement(env._get_game_state(),(0,1)))
    #print(f"Path:{env.current_path(env._get_game_state(),1)}")
    #print(f"Path:{env.current_path(env._get_game_state(),2)}")
    #print(env.no_maze(env._get_game_state()))
    #print(env.path_len_dif(env._get_game_state()))
    env.walls[3][1] = WallDir.HORIZONTAL.value
    #print(f"Path:{env.current_path(env._get_game_state(),1)}")
    #print(f"Path:{env.current_path(env._get_game_state(),2)}")
    #print(env.no_maze(env._get_game_state()))
    #print(env.path_len_dif(env._get_game_state()))
    env.walls[2][3] = WallDir.HORIZONTAL.value
    #print(f"Path:{env.current_path(env._get_game_state(),1)}")
    #print(f"Path:{env.current_path(env._get_game_state(),2)}")
    #print(env.no_maze(env._get_game_state()))
    #print(env.path_len_dif(env._get_game_state()))
    env.walls[2][0] = WallDir.HORIZONTAL.value
    #print(f"Path:{env.current_path(env._get_game_state(),1)}")
    #print(f"Path:{env.current_path(env._get_game_state(),2)}")
    #print(env.no_maze(env._get_game_state()))
    #print(env.path_len_dif(env._get_game_state()))
    env.walls[3][3] = WallDir.HORIZONTAL.value
    #print(f"Path:{env.current_path(env._get_game_state(),1)}")
    #print(f"Path:{env.current_path(env._get_game_state(),2)}")
    #print(env.no_maze(env._get_game_state()))
    #print(env.path_len_dif(env._get_game_state()))
    #print("------")
    #print(f"Path:{env.current_path(env._get_game_state(),1)}")
    #print(f"Path:{env.current_path(env._get_game_state(),2)}")
    #print(env._blocked_exit_wall(env._get_game_state(),(1,2),WallDir.VERTICAL.value))
    #print("-----")
    #env.walls[2][1] = WallDir.VERTICAL.value
    #print(f"Path:{env.current_path(env._get_game_state(),1)}")
    #print(f"Path:{env.current_path(env._get_game_state(),2)}")
    #env.render()
    #print("--state not copied--")
    #print(env._allowed_movement(env._get_game_state(),(2,3)))

    #print(env.placement_to_action((2,3),2))
    #posx, posy = env._find_player_pos(env._get_game_state(),1)
    #print(env.movement_to_action((posx,posy),(posx-1,posy-1)))
    
    #Testing that placement methods agree#
    for action in range(0,12):
      _,(x,y,d) = env.action_to_movementplacement(action)
      actionint = env.placement_to_action((x,y),d)
      print(action,actionint,action==actionint)



    for action in range(12,(env.array_width-1) * (env.array_height-1) * 2 +12):
      _,(x,y,d) = env.action_to_movementplacement(action)
      actionint = env.placement_to_action((x,y),d)
      print(action,actionint,action==actionint)