import gym
from random import randint
import numpy as np
import pandas as pd

env = gym.make('gym_mouse.envs:mouse-v0')

Q = np.zeros([env.observation_space.n, env.action_space.n])

gamma = 0.1
alpha = 0.1
epsilon = 0.1
epsilon_decay = 0.999

total_epochs = 0
episodes = 10000


for episode in range(episodes): 
    epochs = 0
    reward = 0
    epsilon = epsilon*epsilon_decay

    state = env.reset()
    while reward != 20:
        if np.random.rand() < epsilon:
            action = env.action_space.sample()
        else: 
            action = np.argmax(Q[state])
        next_state, reward, done = env.step(action)
        Q[state, action] = Q[state, action] + alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action])
        state = next_state
        epochs += 1
    total_epochs += epochs
    print(total_epochs)

df = pd.DataFrame(Q)

filepath = r"C:\Users\s9gabcal\OneDrive - ABB Industrigymnasium\Teknik\Code\Python\AI-lek\Musen\Excel.xls"
df.to_excel("pd.xlsx")

env.render()
print("Average timesteps taken {}".format(total_epochs/episodes))

