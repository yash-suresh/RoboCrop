import tkinter as tk
import random
import numpy as np
from Bot import *
from Counter import *
from TimeCounter import *



def buttonClicked(x,y,registryActives):
    #AUTHOR: Dept of Computer Sci @ UoN, 2023
    
    for rr in registryActives:
        if isinstance(rr,Bot):
            rr.x = x
            rr.y = y

def initialise(window):
    #AUTHOR: Dept of Computer Sci @ UoN, 2023
    #initialises the window in which the canvas will be built
    
    window.resizable(False,False)
    canvas = tk.Canvas(window,width=1200,height=500)
    canvas.pack()
    return canvas

def placeGrass(registryPassives,canvas):
    #AUTHORS: Dept of Computer Sci @ UoN + Yash Suresh , 2023
    #places grass in a specific configuration in the canvas
    
    map = np.zeros( (10,10), dtype=np.int16)
    #creates a grid of 10x10 zeros; the map will be split into a grid, each cell...
    #..will be populated by grass

    global totalGrassCount
    totalGrassCount = 0
    #this variable allows us to track the number of grass been placed on the canvas.

 


    for xx in range(10):
        for yy in range(10):
                map[xx][yy] = random.randrange(4,8)
    for yy in range(0,10):
        map[8][yy] = 10
    for xx in range(1,8):
        map[xx][0] = 10
    map[0][0] = 1
    map[9][9] = 0
    i = 0
    
    for xx in range(10):
        for yy in range(10):
            
            for _ in range(map[xx][yy]):
                grassX = xx*120 + random.randrange(0,199)
                grassY = yy*50 + random.randrange(0,49)

                grass = Grass("Grass"+str(i),grassX,grassY)
            
                totalGrassCount += 1
                registryPassives.append(grass)
                grass.draw(canvas)
                i += 1
    
    print(np.transpose(map))
    return map


def register(canvas, numberOfBots):
    #AUTHOR: Dept of Computer Sci @ UoN, 2023
    #each object on the canvas needs to be added to a 'register'. This function takes care of that
    
    registryActives = []
    # a store of all actve objects like the bot
    
    registryPassives = []
    # a store of passive objects like the grass
    
    noOfBots = numberOfBots
    #change as required

    for i in range(0,noOfBots):
    #drawing each bot on the canvas
        bot = Bot("Bot"+str(i),canvas)
        registryActives.append(bot)
        bot.draw(canvas)
    
    
    map = placeGrass(registryPassives,canvas)
    #placing and drawing all the grass on the map.
    
    
    count = Counter(canvas, totalGrassCount)
    #initialising the counter to keep a track of the percentage of grass cut
    
    timer = Timer(canvas)
    #initialising the timer.

    canvas.bind( "<Button-1>", lambda event: buttonClicked(event.x,event.y,registryActives) )
    #button click function
    
    return registryActives, registryPassives, count, map, timer


def moveIt(canvas,registryActives,registryPassives,count,moves,window, formationCode, timer):
    #AUTHORS: Dept of Computer Sci @ UoN + Yash Suresh , 2023
    #recrusive function keeps the bot moving until window closed.
    
    moves += 1
    #increment the move counter by 1 because its our first move

    
    code = formationCode
    

    for rr in registryActives:
    #for each bot

        rr.brain(registryActives, code)
        # 'brain' determines the next move.

        rr.move(canvas,registryPassives,1.0)
        # executes next move

        registryPassives = rr.MowGrass(canvas,registryPassives, count)

        #measured by moves
        numberOfMoves = 500
        if moves>numberOfMoves:
            window.destroy()

    

    canvas.after(1,moveIt,canvas,registryActives,registryPassives,count,moves,window, formationCode, timer)
    #keeps calling the function with a delay of 20 milliseconds; sets up an infinite loop
    #change the first arg for to speed up or slow down

def main():
    #AUTHORS: Dept of Computer Sci @ UoN + Yash Suresh , 2023
    
    formationCode = 'lw'
    numberOfBots = 4

    
    window = tk.Tk()
    canvas = initialise(window)
    registryActives, registryPassives, count, map, timer = register(canvas,numberOfBots)

    moves = 0

    #this function is called ONCE to get the bot moving, or else it stays stationary
    moveIt(canvas,registryActives,registryPassives, count, moves, window, formationCode, timer)
    
    window.mainloop()
    
    print(round(count.percentGrassCut, 2))

def runOneExperiment(noOfBots, formationCode):
    #AUTHORS: Dept of Computer Sci @ UoN + Yash Suresh , 2023
    
    window = tk.Tk()
    canvas = initialise(window)
    registryActives, registryPassives, count, map, timer = register(canvas,noOfBots)
    moves = 0
    moveIt(canvas,registryActives,registryPassives, count, moves,window, formationCode, timer)
    window.mainloop()
    return round(count.percentGrassCut, 2)

main()