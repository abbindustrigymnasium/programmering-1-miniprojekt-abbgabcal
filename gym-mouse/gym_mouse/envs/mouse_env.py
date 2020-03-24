import gym
from gym import error, spaces, utils
from gym.utils import seeding

from tkinter import *
master = Tk()

class MouseEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    


    def __init__(self):
        self.energi=50
        self.mouse= [1,2] 
        self.cheeseeaten=0
        self.cheeseamount=10
        self.currentcheeses=0
        self.cheeseplaces=[[3,3],[2,1],[4,5],[7,3],[2,8],[9,1],[5,7],[8,3],[4,1],[2,7],[5,4]]
        self.speed=0.2

        self.w = 10
        self.h = 10
        self.Map = [[0 for x in range(w)] for y in range(h)] 
        self.food= 1
        self.wall=2
        self.Map[2][2]= self.food
        self.Map[0][1]= self.wall
        print("Environment Init")
        
        
    
    def step(self, action): 
        print("Step taken")

    def render(self, mode="human"):
        print("Environment render")
        C = Canvas(master, bg="green", height=600, width=600)
        C.pack()
        mainloop()
        self.distanceY=0
        self.distanceX=0
        self.sizevalue=50
        for row in range(0,self.w): 
            for col in range(0,self.h):
                coord = self.distanceX, self.distanceY, self.distanceX+self.sizevalue, self.distanceY+self.sizevalue #y,x, w, h
                self.distanceX+=self.sizevalue
                if col%2==0:
                        C.create_rectangle(coord, fill="white")
                elif col%2==1:
                        C.create_rectangle(coord, fill="gray")
        self.distanceY+=self.sizevalue
        self.distanceX=0
    
    def reset(self):
        print("Reset")

    # def render(self, mode='human'):
    #     code
    