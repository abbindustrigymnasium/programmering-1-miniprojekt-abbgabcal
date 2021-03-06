import gym                                                              #Nödvändiga imports av bibliotek. 
from random import randint
import numpy as np
import pandas as pd

env = gym.make('gym_mouse.envs:mouse-v0')                               #Ladda in miljön.

df = pd.read_excel(io=r'5000_episodes.xlsx', index_col=0)                #Ladda in Q-table från excel. Ändra siffrorna till den episod du önskar att testa. 
Q = df.to_numpy()

episodes = 100                                                          #Antal episoder. 

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

print(f"Average cheese eaten: {np.mean(cheesearray)}")              #Snitt på hur många ostar som musen lyckas äta. 
print(f"Average reward: {np.mean(rewardarray)}")                    #Snitt på belöning. Högre är bättre. 



env.render()

