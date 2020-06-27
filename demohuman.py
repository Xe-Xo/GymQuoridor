import gym
import argparse


parser = argparse.ArgumentParser(description='Demo Quoridor Environment')
parser.add_argument('--boardsize', type=int, default=9)
args = parser.parse_args()

quoridor_env = gym.make('gym_quoridor:quoridor-v0', size=args.boardsize)
done = False
while not done:
  #break #to stop infinite loop until human setup
  action = quoridor_env.render(mode="human")
  #print(f"RETURNED ACTION! {action}")
  if action == -1:
    exit()
  elif type(action) == tuple:
    print(action)
  elif action is None:
    pass
  else:
    try:
      _, _, done, _ = quoridor_env.step(action)
    except Exception as e:
        print(e)
        break



  