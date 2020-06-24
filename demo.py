import gym
import argparse


parser = argparse.ArgumentParser(description='Demo Quoridor Environment')
parser.add_argument('--boardsize', type=int, default=9)
args = parser.parse_args()

quoridor_env = gym.make('gym_quoridor', size=args.boardsize)
done = False
while not done:
  action = quoridor_env.render(mode="human")
  if action == -1:
    exit()
  try:
    _, _, done, _ = quoridor_env.step(action)
  except Exception as e:
    print(e)
    continue

  