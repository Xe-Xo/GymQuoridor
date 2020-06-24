import gym
import argparse


parser = argparse.ArgumentParser(description='Demo Quoridor Environment')
parser.add_argument('--boardsize', type=int, default=9)
args = parser.parse_args()

quoridor_env = gym.make('gym_quoridor:quoridor-v0', size=args.boardsize)

done = False
action = 0
while not done and action < 140:
    state, _, done, _ = quoridor_env.step(action)
    action += 1



  