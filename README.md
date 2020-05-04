# AI-mus med Q-learning -- Miniprojekt

## Kom igång 
###  Förberedelser
För att komma igång och prova AI-musen krävs några enkla förberedelser. Börja med att klona eller ladda ner repositoriet.<br/> 
Skriv sedan i terminalen för `gym-mouse`:
```sh
pip install -e .
```
### Testfiler
För att ni ska kunna se resultatet av att Q-learningalgoritemen har kört programmet och försökt att lära sig har jag inkluderat excelfiler som motsvarar Q-tables för var femhundrade generation upp till 5000.<br/>
För att testa någon av de här generationerna öppna `TestQAgent.py` och ändra i följande rad till det som du önskar att testa.  
```python
df = pd.read_excel(io=r'5000_episodes.xlsx', index_col=0)
```

### Testa Q-learning själv
Om ni själva vill testa att lära upp en egen Q-learningagent kan ni använda `LearnQAgent.py` för att lära upp. Ni kan prova runt och ändra hyperparametrarna för att se vad som händer samt ändra antalet episoder som agenten ska träna. 
```python
gamma = 0.7
alpha = 0.5 
epsilon = 0.8 
epsilon_decay = 0.99

episodes = 5000
```
Någonting att tänka på är att lära upp en Q-learningagent tar tid. För att minimera tiden det tar finns det några åtgärder som kan göras. Den enklaste är att minimera fönstret med musen som letar efter ost för att minska last på framförallt GPU. <br/>
Det gär även att ändra följande rad i `gym-mouse/gym_mouse/envs/mouse_env.py` till: 
```python
#Rad nummer 25
self.speed= 0.2 #Från det här

self.speed= 0 #Till det här
```
Nu kommer den att uppdatera så fort datorn klarar av istället för 5 gånger i sekunden. Ni kommer dock inte kunna uppfatta vad AI:n gör men det kommer att gå snabbare. 

## Projektet
Det här projektet går ut på att vidareutveckla Joakims AI-mus till att använda sig utav Q-learning. Till Q-learningalgoritmen har jag använt mig av openai-gym och numpy. För att kunna använda Q-learning på musprojektet var jag tvungen att skriva om det till ett openai-gym environement. Det här visade sig vara en utav de svårare stegen i projektet dels eftersom jag behövde ändra om i koden en hel del vilket mestadels var jobbigt men även att jag inte kunde komma på ett lämligt sätt att skapa ett observation_space. Ett observation_space är det som en Q-learningalgoritm använder för att ha koll på vad som händer och det svåraste under hela projektet var att komma på en lämplig metod att ta fram detta. Eter att jag hade skissat på diverse olika alternativ kom jag tillslut på en lösning som fungerade hyfsat men med nackdelen att det innebar att jag endast skulle kunna ha en ost som musn letade efter på planen åt gången. <br/>

Under projektet har jag lärt mig väldigt mycket om hur machine learning fungerar i allmänhet och Q-learning i synnerhet. Jag har även lär mig en del om hur man kan skapa grafiska saker i python med tkinter och även en del om hur klasser fungerar i python. För att bygga vidare på projektet hade man kunnat försöka skapa ett program där Ai:n fortfarande hade kunnat köras men med flera ostar samtidigt som i Joakims ursprungliga program. Det går även att ändra på machine learning-delen i projektet genom att prova något annat än Q-learning eller genom att kombinera Q-learning med till exempel Tensorflow. 

## AI in action
![Alt Text](https://media.giphy.com/media/chKLhZbas6WxWspKdK/giphy.gif)