import gym
from gym import error, spaces, utils
from gym.utils import seeding

class MouseEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        print("Environment Init")
    
    def step(self, action): 
        print("Step taken")
    
    def reset(self):
        print("Reset")

    # def render(self, mode='human'):
    #     code
    