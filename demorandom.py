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

    state, reward, done, info = quoridor_env.step(12)
    statelist.append(state)
    quoridor_env.render(mode="terminal")
    tau += 1
    if tau == 1:
        break

stateint = int(input("View which state?"))
for i in range(gym_quoridor.quoridorvars.NUM_CHNLS):
    print(statelist[stateint][i,:,:])

  