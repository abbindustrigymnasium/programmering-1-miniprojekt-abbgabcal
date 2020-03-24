import gym
from random import randint

env = gym.make('gym_mouse.envs:mouse-v0')

Hej = 0

while Hej < 10:
    for x in range(10):
        env.step(3)
    env.reset()
    Hej +=1





env.render()
