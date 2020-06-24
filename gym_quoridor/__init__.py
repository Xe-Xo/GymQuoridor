from gym.envs.registration import register

register(
    id='quoridor-v0',
    entry_point='gym_quoridor.envs:QuoridorEnv',
)