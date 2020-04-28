import gym                      #Nödvändiga imports av bibliotek. 
from random import randint
import numpy as np
import pandas as pd

env = gym.make('gym_mouse.envs:mouse-v0')   #Ladda in miljön.  

Q = np.zeros([env.observation_space.n, env.action_space.n]) #Skapar ett Q-table

gamma = 0.7             #Gamma (greed) värde mellan 0 och 1 som bestämmer hur mycket nutida belöningar ska värderas kontra framtida belöningar. 
alpha = 0.5             #Alpha (learning rate) värde mellan 0 och 1 som bestämmer hur fort AI:n ska lära sig. Fortare inte alltid bättre
epsilon = 0.8           #Epsilon (random) värde mellan 0 och 1 som bestämmer hur ofta ett slumpmässigt val ska göras för att potentiellt lära sig mera eller hitta ett bättre alternativ. 
epsilon_decay = 0.99    #Epsilon_decay värde mellan 0 och 1 som bestämmer hur mycket epsilon ska minskas över tid. 

episodes = 5000        #Antal gånger som AI:n ska spela spelet

done = False            #Variabel so mhåller koll på ifall spelet är över. 
cheesearray = []        #Samling av antalet insamlade ostar för varje omgång för att kunna göra jämförelser. 
rewardarray = []        #Samling av belöningar från varje omgång för att kunna göra jämförelser. 


for episode in range(episodes): 
    reward = 0                          #Återställ belöningen till 0.
    epsilon = epsilon*epsilon_decay     #Räkna ut det nya värdet på epsilon.

    state, done = env.reset()           #Startar om miljön och tar in de första värdena. 
    while not done:
        if np.random.rand() < epsilon:          #Kollar om en slumpmässig action ska genomföras
            action = env.action_space.sample()  #Väljer ett slumpmässigt nummer av 0, 1, 2 eller 3 som action. 
        else: 
            action = np.argmax(Q[state])        #Väljer den action som borde ge bäst resultat från Q-tablet
        next_state, reward, done, info = env.step(action)   #Utför vald action och sparar resultatet i variablerna. 
        Q[state, action] = Q[state, action] + alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action]) #Uppdaterar Q-tablet utifrån de nya värdena, de gamla värdena samt hyperparametrarna med hjälp av Bellmanformeln. 
        state = next_state  #Uppdaterar state
    rewardarray.append(reward)  #Sparar ner belöningsresultatet. 
    cheesearray.append(info)    #Sparar ner antalet insamlade ostar. 
    print(cheesearray)
    print(episode)
    if episode % 500 == 0:      #If sats som utför var 500:e episod. Sparar ner Q-tablet till ett excelblad så det går att använda senare. 
        df = pd.DataFrame(Q)
        filepath = r"C:\Users\s9gabcal\OneDrive - ABB Industrigymnasium\Teknik\Code\Python\AI-lek\Musen\Excel.xls"
        df.to_excel(f"{episode}_episodes.xlsx")

df = pd.DataFrame(Q)        #Sparar ner det slutgiltiga resultatet i ett excelblad. 
df.to_excel(f"{episodes}_episodes.xlsx")

print(f"Average cheese eaten: {np.mean(cheesearray)}")
print(f"Average reward: {np.mean(rewardarray)}")



env.render()

