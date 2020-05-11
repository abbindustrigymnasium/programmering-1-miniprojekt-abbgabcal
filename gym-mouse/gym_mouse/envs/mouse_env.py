import gym                                                  #imports av nödvändiga bibliotek. 
from gym import spaces
import time
from random import randint

from tkinter import *
master = Tk()

class MouseEnv(gym.Env):                                    #Skapa klassen som innehåller hela miljön. 
    metadata = {'render.modes': ['human']}

    def __init__(self):                                     #Funktion som körs igång när klassen startar. I gym.make() i Q-learningagenten
        
        self.action_space = spaces.Discrete(4)              #Action space. Antalet olika "actions" som AI:n kan göra. Upp, ner, höger och vänster. 
        self.observation_space = spaces.Discrete(1100)      #Antal observationer som AI:n kan göra. Hundra musplaceringar för varje möjlig ostplacering (11*100). 
        self.reward = 0                                     #Belöning
        self.episode_over = False                           #Håller koll på om omgången är över. Om den är över är episode_over = True

        self.energi=50                                      #Energi
        self.mouse= [5,5]                                   #Musens ursprungliga position
        self.cheeseeaten=0                                  #Antal ätna ostar
        self.cheeseamount=1                                 #Antal ostar på planen, går att ändra men då krävs det att observation_space ändras. 
        self.currentcheeses=0                               #Antal ostar på planen just nu. 
        self.cheeseplaces=[[3,3],[2,1],[4,5],[7,3],[2,8],[9,1],[5,7],[8,3],[4,1],[2,7],[5,4]]   #Alla olika placeringar som en ost kan skapas på. 
        self.speed= 1/30                                    #Uppdaterngshastighet, för inlärning rekommenderas 0 (snabbast möjliga), för testning 0.2 (möjligt att se vad som händer). 

        self.w = 10     #Planens bredd.
        self.h = 10     #Planens höjd.
        self.Map = [[0 for x in range(self.w)] for y in range(self.h)]      #2d-Array 

        self.C = Canvas(master, bg="green", height=600, width=600)          #Skapa en yta (Canvas) som planen kan byggas på. Nedastående kod ritar ut ett rutnät på ytan. 
        self.C.pack()
        self.distanceY=0
        self.distanceX=0
        self.sizevalue=50
        for row in range(0,self.w): 
            for col in range(0,self.h):
                coord = self.distanceX, self.distanceY, self.distanceX+self.sizevalue, self.distanceY+self.sizevalue 
                self.distanceX+=self.sizevalue
                self.C.create_rectangle(coord, fill="white")
            self.distanceY+=self.sizevalue
            self.distanceX=0

        self.text = Text(master, height=2, width=30)                    #Skapar textrutan under planen. 
        self.text.pack()

        self.Mouse=self.C.create_rectangle(self.getcoord(self.mouse[0],self.mouse[1]), fill="brown")    #Skapar musen på Getcoord hämtar koordinaterna för musen position. 
        self.CreateCheese()

        print("Environment Init")

    def rs(self, inputval, sizevalue):
        return inputval*sizevalue

    def getcoord(self, x,y):            #Funktion som hittar koordinaterna på planen utifrån koordinaterna i 2d-arrayen. 
        sizevalue = 50
        x = self.rs(x, sizevalue)
        y = self.rs(y, sizevalue)
        return x, y, x+sizevalue, y+sizevalue

    def CreateCheese(self):                                     #Funktion som skapar den första osten
            ptpc = randint(0, len(self.cheeseplaces)-1)
            self.cheeseX = self.cheeseplaces[ptpc][0]
            self.cheeseY = self.cheeseplaces[ptpc][1]
            self.cheesesprite = self.C.create_rectangle(self.getcoord(self.cheeseX,self.cheeseY), fill="yellow")
            self.currentcheeses += 1
            self.Map[self.cheeseX][self.cheeseY] = 1

    def NewCheese(self):                                                #Funktion som skapar en ny ost när musen har hittat en gammal. 
        if self.cheeseamount > self.currentcheeses:
            ptpc = randint(0, len(self.cheeseplaces)-1)
            self.cheeseX = self.cheeseplaces[ptpc][0]
            self.cheeseY = self.cheeseplaces[ptpc][1]
            self.C.coords(self.cheesesprite, self.getcoord(self.cheeseX, self.cheeseY))
            self.currentcheeses += 1
            self.Map[self.cheeseX][self.cheeseY] = 1

    def FoundCheese(self):                                              #Funktion som kollar ommusen hittar en ost och delar ut poäng och energi.  
        if self.Map[self.mouse[0]][self.mouse[1]] == 1: 
            outputtext = f"Found Cheese at {self.mouse[0]} X {self.mouse[1]} Y"
            self.cheeseeaten += 1
            self.text.insert(INSERT, outputtext)
            self.Map[self.mouse[0]][self.mouse[1]] = 0
            self.energi += 15
            self.currentcheeses-=1
            self.reward += 10
    
    def step(self, action):                                             #Funktionen som kommunicerar med AI:n. 
        self.takeAction(action)                                         #Kör takeAction() och skickar in den action som AI:n sa skulle användas. 

        mouse_pos = self.mouse[0] + self.mouse[1]*10                                 #Skriver ut musens position som ett tal mellan 0 och 100. Tiotalet motsvarar y-koordinaten i 2d-arrayen och entalet motsvarar x-koordinaten. 
        cheese_pos = self.cheeseplaces.index([self.cheeseX, self.cheeseY])           #Tar den nuvarande ostens position genom att hitta dens index i cheeseplaces arrayen. 
        observation = cheese_pos*100 + mouse_pos                                     #Skapar en observation som AI:n kan använda. Hundratalet motsvarar ostens position, tiotalet musens y-koordinat och entalet musens x-koordniat 

        return observation, self.reward, self.episode_over, self.cheeseeaten         #Skickar iväg all information till AI:n

    def takeAction(self, action):       #Funktion som styr musen utifrån vad AI:n skickar in för action. 
        time.sleep(self.speed)
        steps = [0,0]                   #Variabel som håller koll på hur musen förflyttar sig. 
        if action == 0:
            if self.mouse[1] > 0:       #Kollar om musen är för nära väggen för att gå åt det hållet. Är musen för nära kan den inte gå men förlorar ändå poäng och energi för att AI:n skalära sig att inte gå in i väggen. 
                self.mouse[1] = self.mouse[1]-1 #Uppåt, Förflyttar musens position i 2d-arrayen. 
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
        self.C.move(self.Mouse, dx, dy) #Förflyttar musens position i det visuella. 
        self.NewCheese()                #Kollar om det behövs en ny ost och skapar en ifal det behövs. 
        self.C.update()
        self.FoundCheese()              #Kollar om musen har hittat en ost. 
        
        if self.cheeseeaten == 50:     #Om musen har samlat ihop 50 ostar avbryts omgången. Belöningen kan variera beroende på hur effektiv musen var. 
            self.episode_over = True

        if self.energi == 0:           #Om musen får slut på energi avslutas omgången och ett straff på -50 poäng delas ut. 
            self.reward -= 50
            print(f"Episode over. You collected {self.cheeseeaten} cheeses")
            self.episode_over = True

    def render(self, mode="human"):
        print("Environment render")
        mainloop()
    
    def reset(self):                #Funktion som återställer spelplanen till det utrspurngliga läget när en ny ongång ska påbörjas. 0
        self.reward = 0             #Sätter belöningen till 0. 
        self.episode_over = False   #Visar att spelet är igång. 

        self.energi=50              #Sätter energi till 50
        self.mouse= [5,5]           #Sätter musens position till 5,5
        self.cheeseeaten=0
        self.cheeseamount=1
        self.currentcheeses=0

        self.C.coords(self.Mouse, self.getcoord(self.mouse[0],self.mouse[1])) #Förflyttar musen till den ursprungliga positionen
        self.NewCheese()                                                      #Skapar den första osten

        print("Env reset")
        
        mouse_pos = self.mouse[0] + self.mouse[1]*10                         #Skriver ut musens position som ett tal mellan 0 och 100. Tiotalet motsvarar y-koordinaten i 2d-arrayen och entalet motsvarar x-koordinaten. 
        cheese_pos = self.cheeseplaces.index([self.cheeseX, self.cheeseY])   #Tar den nuvarande ostens position genom att hitta dens index i cheeseplaces arrayen.
        observation = cheese_pos*100 + mouse_pos                             #Skapar en observation som AI:n kan använda. Hundratalet motsvarar ostens position, tiotalet musens y-koordinat och entalet musens x-koordniat 

        return observation, self.episode_over                                #Skickar iväg all ny information till AI:n
