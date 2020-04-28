import gym
from gym import spaces

import time
from random import randint

from tkinter import *
master = Tk()

class MouseEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Discrete(1100)
        self.reward = 0
        self.episode_over = False

        self.energi=50
        self.mouse= [5,5] 
        self.cheeseeaten=0
        self.cheeseamount=1
        self.currentcheeses=0
        self.cheeseplaces=[[3,3],[2,1],[4,5],[7,3],[2,8],[9,1],[5,7],[8,3],[4,1],[2,7],[5,4]]
        self.speed= 0.2

        self.w = 10
        self.h = 10
        self.Map = [[0 for x in range(self.w)] for y in range(self.h)] 

        self.C = Canvas(master, bg="green", height=600, width=600)
        self.C.pack()
        self.distanceY=0
        self.distanceX=0
        self.sizevalue=50
        for row in range(0,self.w): 
            for col in range(0,self.h):
                coord = self.distanceX, self.distanceY, self.distanceX+self.sizevalue, self.distanceY+self.sizevalue #y,x, w, h
                self.distanceX+=self.sizevalue
                self.C.create_rectangle(coord, fill="white")
            self.distanceY+=self.sizevalue
            self.distanceX=0

        self.text = Text(master, height=2, width=30)
        self.text.pack()

        self.Mouse=self.C.create_rectangle(self.getcoord(self.mouse[0],self.mouse[1]), fill="brown")
        self.CreateCheese()

        print("Environment Init")

    def rs(self, inputval, sizevalue):
        return inputval*sizevalue

    def getcoord(self, x,y):
        sizevalue = 50
        x = self.rs(x, sizevalue)
        y = self.rs(y, sizevalue)
        return x, y, x+sizevalue, y+sizevalue

    def CreateCheese(self):
            ptpc = randint(0, len(self.cheeseplaces)-1)
            self.cheeseX = self.cheeseplaces[ptpc][0]
            self.cheeseY = self.cheeseplaces[ptpc][1]
            self.cheesesprite = self.C.create_rectangle(self.getcoord(self.cheeseX,self.cheeseY), fill="yellow")
            self.currentcheeses += 1
            self.Map[self.cheeseX][self.cheeseY] = 1

    def NewCheese(self):
        if self.cheeseamount > self.currentcheeses:
            ptpc = randint(0, len(self.cheeseplaces)-1)
            self.cheeseX = self.cheeseplaces[ptpc][0]
            self.cheeseY = self.cheeseplaces[ptpc][1]
            self.C.coords(self.cheesesprite, self.getcoord(self.cheeseX, self.cheeseY))
            self.currentcheeses += 1
            self.Map[self.cheeseX][self.cheeseY] = 1

    def FoundCheese(self):
        if self.Map[self.mouse[0]][self.mouse[1]] == 1: 
            outputtext = f"Found Cheese at {self.mouse[0]} X {self.mouse[1]} Y"
            self.cheeseeaten += 1
            self.text.insert(INSERT, outputtext)
            self.Map[self.mouse[0]][self.mouse[1]] = 0
            self.energi += 10
            self.currentcheeses-=1
            self.reward += 10
    
    def step(self, action):
        self.takeAction(action)

        mouse_pos = self.mouse[0] + self.mouse[1]*10
        cheese_pos = self.cheeseplaces.index([self.cheeseX, self.cheeseY])
        observation = cheese_pos*100 + mouse_pos

        return observation, self.reward, self.episode_over, self.cheeseeaten

    def takeAction(self, action):
        time.sleep(self.speed)
        steps = [0,0]
        if action == 0:
            if self.mouse[1] > 0:
                self.mouse[1] = self.mouse[1]-1 #Uppåt
                steps = [0,-1]
            self.reward -=1
            self.energi -=1
        elif action == 1:
            if self.mouse[1] < self.h-1:
                self.mouse[1] = self.mouse[1]+1 #Nedåt
                steps = [0,1]
            self.reward -=1
            self.energi -=1
        elif action == 2:
            if self.mouse[0] > 0:
                self.mouse[0] = self.mouse[0]-1 #Vänster
                steps = [-1,0]
            self.reward -=1
            self.energi -=1
        elif action == 3: 
            if self.mouse[0] < self.w-1:
                self.mouse[0] = self.mouse[0]+1 #Höger  
                steps = [1,0]
            self.reward -=1
            self.energi -=1

        dx = steps[0] * self.sizevalue
        dy = steps[1] * self.sizevalue
        self.C.move(self.Mouse, dx, dy)
        self.NewCheese()
        self.C.update()
        self.FoundCheese()
        

        if self.cheeseeaten == 50:
            self.episode_over = True

        if self.energi == 0: 
            self.reward -= 50
            print(f"Episode over. You collected {self.cheeseeaten} cheeses")
            self.episode_over = True

    def render(self, mode="human"):
        print("Environment render")
        mainloop()
    
    def reset(self):
        self.reward = 0
        self.episode_over = False

        self.energi=50
        self.mouse= [5,5] 
        self.cheeseeaten=0
        self.cheeseamount=1
        self.currentcheeses=0

        self.C.coords(self.Mouse, self.getcoord(self.mouse[0],self.mouse[1]))
        self.NewCheese()

        print("Env reset")
        
        mouse_pos = self.mouse[0] + self.mouse[1]*10
        cheese_pos = self.cheeseplaces.index([self.cheeseX, self.cheeseY])
        observation = cheese_pos*100 + mouse_pos

        return observation, self.episode_over
