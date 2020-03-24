import gym


env = gym.make('gym_mouse.envs:mouse-v0')

env.step(1)
env.reset()
env.render()