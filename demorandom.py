import gym
import argparse
import gym_quoridor.quoridorvars
import gym_quoridor.enums

parser = argparse.ArgumentParser(description='Demo Quoridor Environment')
parser.add_argument('--boardsize', type=int, default=9)
args = parser.parse_args()

quoridor_env = gym.make('gym_quoridor:quoridor-v0', size=args.boardsize)

statelist = []

done = False
tau = 0
while not done:
    print(f"-----{tau}------")

    action = quoridor_env.render(mode="terminal")
    if action is None or action == -1:
        state, reward, done, info = quoridor_env.step(quoridor_env.action_space.sample())
    else:
        print(action)
        state, reward, done, info = quoridor_env.step(action)
    
    #statelist.append(state)
    
    tau += 1
    if tau == 100:
        break

quoridor_env.render(mode="human")
image_array = quoridor_env.render(mode="rgbarray")


  