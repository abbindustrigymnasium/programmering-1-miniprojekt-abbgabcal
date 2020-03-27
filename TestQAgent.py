import gym
from random import randint
import numpy as np
import pandas as pd

env = gym.make('gym_mouse.envs:mouse-v0')

df = pd.read_excel(io=r'1_episodes.xlsx', index_col=0)
Q = df.to_numpy()

episodes = 100

done = False
cheesearray = []
rewardarray = []


for episode in range(episodes): 
    reward = 0

    state, done = env.reset()
    while not done:
        action = np.argmax(Q[state])
        next_state, reward, done, info = env.step(action)
        state = next_state
    rewardarray.append(reward)
    cheesearray.append(info)
    print(cheesearray)
    print(episode)

print(f"Average cheese eaten: {np.mean(cheesearray)}")
print(f"Average reward: {np.mean(rewardarray)}")



env.render()

