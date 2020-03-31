import gym
from random import randint
import numpy as np
import pandas as pd

env = gym.make('gym_mouse.envs:mouse-v0')

Q = np.zeros([env.observation_space.n, env.action_space.n])

gamma = 0.7
alpha = 0.5
epsilon = 0.8
epsilon_decay = 0.99

total_epochs = 0
episodes = 10000

done = False
cheesearray = []
rewardarray = []


for episode in range(episodes): 
    reward = 0
    epsilon = epsilon*epsilon_decay

    state, done = env.reset()
    while not done:
        if np.random.rand() < epsilon:
            action = env.action_space.sample()
        else: 
            action = np.argmax(Q[state])
        next_state, reward, done, info = env.step(action)
        Q[state, action] = Q[state, action] + alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action])
        state = next_state
    rewardarray.append(reward)
    cheesearray.append(info)
    print(cheesearray)
    print(episode)
    if episode % 500 == 0:
        df = pd.DataFrame(Q)
        filepath = r"C:\Users\s9gabcal\OneDrive - ABB Industrigymnasium\Teknik\Code\Python\AI-lek\Musen\Excel.xls"
        df.to_excel(f"{episode}_episodes.xlsx")

df = pd.DataFrame(Q)
df.to_excel(f"{episodes}_episodes.xlsx")

print(f"Average cheese eaten: {np.mean(cheesearray)}")
print(f"Average reward: {np.mean(rewardarray)}")



env.render()

