from gym_quoridor import quoridorvars

def get_board_size(state):
  assert state.shape[1] == state.shape[2] #X == Y
  return (state.shape[1], state.shape[2])

def get_wall_size(state):
  assert state.shape[1] == state.shape[2] #X == Y
  return (state.shape[1]-1, state.shape[2]-1)


def get_turn(state):
    """
    Returns who's turn it is (quoridorvars.BLACK/quoridorvars.WHITE)
    :param state:
    :return:
    """
    return int(state[quoridorvars.TURN_CHNL, 0, 0])

def set_turn(state):
    """
    Swaps turn
    :param state:
    :return:
    """
    state[quoridorvars.TURN_CHNL] = 1 - state[quoridorvars.TURN_CHNL]