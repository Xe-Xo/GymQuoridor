

#State is returned as a np.array 
NUM_CHNLS = 14
# Channels of the the Array
BLACKLOC_CHNL = 0 #Black Player Location on Board
WHITELOC_CHNL = 1 #White Player Location on Board
TURN_CHNL = 2 #Current Turn 0 - Black 1- White
BLACKMOVEVALID_CHNL = 3 #Locations where Black can move to 1=Valid Move
WHITEMOVEVALID_CHNL = 4 #Locations where White can move to 1=Valid Move
BLACK_V_WALL_CHNL = 5 
BLACK_H_WALL_CHNL = 6 
WHITE_V_WALL_CHNL = 7 
WHITE_H_WALL_CHNL = 8
INVALID_V_WALL_CHNL = 9
INVALID_H_WALL_CHNL = 10
BLACKASTAR_CHNL = 11 #Blacks Astar Path to End
WHITEASTAR_CHNL = 12 #Whites Astar Path to End
GAMEOVER_CHNL = 13 #Indicator whether Game is Over

#movement action int 
MOVE_UP = 0
MOVE_DOWN = 1
MOVE_LEFT = 2
MOVE_RIGHT = 3
MOVE_UPUP = 4
MOVE_UPLEFT = 5
MOVE_UPRIGHT = 6
MOVE_DOWNDOWN = 7
MOVE_DOWNLEFT = 8
MOVE_DOWNRIGHT = 9
MOVE_LEFTLEFT = 10
MOVE_RIGHTRIGHT = 11

#movement action tuple
MOVEMENT_DIR = [(0  ,-1 ),
                (0  ,1  ),
                (-1 ,0  ),
                (1  ,0  ),
                (0  ,-2 ),
                (-1 ,-1 ),
                (1  ,-1 ),
                (0  ,2  ),
                (-1 ,1  ),
                (1  ,1  ),
                (-2 ,0  ), 
                (2  ,0  )
]



