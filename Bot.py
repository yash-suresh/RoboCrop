import tkinter as tk
import random
import math
import numpy as np
from Grass import *

class Bot:

    def __init__(self,namep,canvasp):
    #AUTHORS: Dept of Computer Sci @ UoN + Yash Suresh , 2023
    
    
    #constructor method
        
        self.x = random.randint(100,1100)
        self.y = random.randint(100,400)
        #we have to initialise the bot within canvas constraints

        self.theta = random.uniform(0.0,2.0*math.pi)
        #self.theta = 0
        
        self.name = namep
        self.ll = 60 #axle width


        self.vl = 0.0
        #speed of left wheel
        self.vr = 0.0
        #speed of right wheel

        self.turning = 0
        self.moving = random.randrange(50,100)
        self.currentlyTurning = False
        self.canvas = canvasp

        self.isCollision = False
        self.formationCode = None

        self.dangerThreshold = 75.0
        
        if random.randint(1,2) == 3:
            self.isFaulty = True
        else:
            self.isFaulty = False
        

    
    def draw(self,canvas):
    #AUTHORS: Dept of Computer Sci @ UoN , 2023
    #function which draws the bot and all its different parts
        
        points = [ (self.x + 30*math.sin(self.theta)) - 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y - 30*math.cos(self.theta)) - 30*math.cos((math.pi/2.0)-self.theta), \
                   (self.x - 30*math.sin(self.theta)) - 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y + 30*math.cos(self.theta)) - 30*math.cos((math.pi/2.0)-self.theta), \
                   (self.x - 30*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y + 30*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta), \
                   (self.x + 30*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y - 30*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta)  \
                ]
        canvas.create_polygon(points, fill="blue", tags=self.name)

        self.sensorPositions = [ (self.x + 20*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                                 (self.y - 20*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta), \
                                 (self.x - 20*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                                 (self.y + 20*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta)  \
                            ]
    
        centre1PosX = self.x 
        centre1PosY = self.y
        canvas.create_oval(centre1PosX-15,centre1PosY-15,\
                           centre1PosX+15,centre1PosY+15,\
                           fill="gold",tags=self.name)

        wheel1PosX = self.x - 30*math.sin(self.theta)
        wheel1PosY = self.y + 30*math.cos(self.theta)
        canvas.create_oval(wheel1PosX-3,wheel1PosY-3,\
                                         wheel1PosX+3,wheel1PosY+3,\
                                         fill="red",tags=self.name)

        wheel2PosX = self.x + 30*math.sin(self.theta)
        wheel2PosY = self.y - 30*math.cos(self.theta)
        canvas.create_oval(wheel2PosX-3,wheel2PosY-3,\
                                         wheel2PosX+3,wheel2PosY+3,\
                                         fill="green",tags=self.name)

        sensor1PosX = self.sensorPositions[0]
        sensor1PosY = self.sensorPositions[1]
        sensor2PosX = self.sensorPositions[2]
        sensor2PosY = self.sensorPositions[3]
        canvas.create_oval(sensor1PosX-3,sensor1PosY-3, \
                           sensor1PosX+3,sensor1PosY+3, \
                           fill="yellow",tags=self.name)
        canvas.create_oval(sensor2PosX-3,sensor2PosY-3, \
                           sensor2PosX+3,sensor2PosY+3, \
                           fill="yellow",tags=self.name)
        
    # cf. Dudek and Jenkin, Computational Principles of Mobile Robotics
    def move(self,canvas,registryPassives,dt):
    #AUTHORS: Dept of Computer Sci @ UoN , 2023
        
        if self.vl==self.vr:
            R = 0

        else:
            R = (self.ll/2.0)*((self.vr+self.vl)/(self.vl-self.vr))

        omega = (self.vl-self.vr)/self.ll
        ICCx = self.x-R*math.sin(self.theta) #instantaneous centre of curvature
        ICCy = self.y+R*math.cos(self.theta)
        m = np.matrix( [ [math.cos(omega*dt), -math.sin(omega*dt), 0], \
                        [math.sin(omega*dt), math.cos(omega*dt), 0],  \
                        [0,0,1] ] )
        v1 = np.matrix([[self.x-ICCx],[self.y-ICCy],[self.theta]])
        v2 = np.matrix([[ICCx],[ICCy],[omega*dt]])
        newv = np.add(np.dot(m,v1),v2)
        newX = newv.item(0)
        newY = newv.item(1)
        newTheta = newv.item(2)
        newTheta = newTheta%(2.0*math.pi) #make sure angle doesn't go outside [0.0,2*pi)
        self.x = newX
        self.y = newY
        self.theta = newTheta        
        if self.vl==self.vr: # straight line movement
            self.x += self.vr*math.cos(self.theta) #vr wlog
            self.y += self.vr*math.sin(self.theta)
        
        
        
        canvas.delete(self.name)
        self.draw(canvas)
        
    def distanceTo(self,obj):
    
        xx,yy = obj.getLocation()
        return math.sqrt( math.pow(self.x-xx,2) + math.pow(self.y-yy,2) )
    
    def distanceToRightSensor(self,lx,ly):
        return math.sqrt( (lx-self.sensorPositions[0])*(lx-self.sensorPositions[0]) + \
                          (ly-self.sensorPositions[1])*(ly-self.sensorPositions[1]) )

    def distanceToLeftSensor(self,lx,ly):
        return math.sqrt( (lx-self.sensorPositions[2])*(lx-self.sensorPositions[2]) + \
                            (ly-self.sensorPositions[3])*(ly-self.sensorPositions[3]) )

    def MowGrass(self, canvas, registryPassives, count):
        toDelete = []
        for idx,rr in enumerate(registryPassives):
            if isinstance(rr, Grass):
                if self.distanceTo(rr)<30:
                    canvas.delete(rr.name)
                    toDelete.append(idx)
                    count.GrassMowed(canvas)
        for ii in sorted(toDelete,reverse=True):
            del registryPassives[ii]
        return registryPassives
    
    def getLocation(self):
        return self.x, self.y

    


    def brain(self, bots, code):
    #AUTHORS: Dept of Computer Sci @ UoN + Yash Suresh , 2023
        
        if self.isFaulty == False:

            self.formationCode = code
            
            if(self.formationCode == 'lw'):

                self.FormationLinearWander(bots)
            
            elif(self.formationCode == 'rw'):
                
                self.FormationRandomWander(bots)

            elif(self.formationCode == 'b'):
                self.BisectorSearch(bots)

            elif(self.formationCode == 'q'):
                self.QuadrantSearch(bots)
            
            elif(self.formationCode == 'r'):
                
                self.Repel(bots)

        else:
            pass

        

    def WallCollision(self):
    #AUTHOR: Yash Suresh , 2023
        
        if self.x <= 45 or self.x >= 1155 or self.y <= 45 or self.y >= 455:
        # we are assuming that the bot has some kind of cushioning which bounces of the wall ..
        #.. after collision, hence the simulation of slight backwards movement to reduce wall scratches
            if self.x <= 45:
                self.x = 46
            if self.x >= 1155:
                self.x = 1154
            if self.y <= 45:
                self.y = 46
            if self.y >= 455:
                self.y = 454
            #the above was done to prevent the bot from rotating on the edge indefinitely
             
            
            self.turning = 30 
            self.currentlyTurning = True
        

    def IsBotColliding(self,bots):
    #AUTHOR: Yash Suresh , 2023
        
        for bot in bots:
            if bot != self:
                #print(self.distanceTo(bot))
                if self.distanceTo(bot) < self.dangerThreshold:
                    self.isCollision = True

                    break
                    #if theres a collision, then no point of checking other bots we need to act
                
                else:
                    self.isCollision = False

            else:
                pass
        
        return self.isCollision


    def CollisionMechanics(self):
    #AUTHOR: Yash Suresh , 2023
        
        if random.choice([True, False]):
                self.x -= random.randint(10, 50)
        
        else:
                self.x += random.randint(10, 50)
            
        if random.choice([True, False]):
                self.y -= random.randint(10, 50)
        else:
                self.y += random.randint(10, 50)
            
        self.turning = random.randint(10, 50)

        self.currentlyTurning = True
        

    def FormationRandomWander(self, bots):
    #AUTHOR: Yash Suresh , 2023
        
        if self.currentlyTurning == True:
        #if the bot is in the process of turning
            
            self.vl = -2.0
            self.vr = 2.0
            #turns to the left
            
            self.turning -= 1
            #keep track of how many turns


        else:
        #bot in linear motion
            self.vl = 5.0
            self.vr = 5.0
            self.moving -= 1
            #keeps track of forward movement


        self.WallCollision()
        # checks for wall collision and takes necessary action

        
        if self.IsBotColliding(bots):
            self.CollisionMechanics()
           
  
        if self.moving == 0 and not self.currentlyTurning:
        #if the bot has come to end of its movement spell
        
        #the idea is that we set a high enough counter which runs itself down to 0..
        #..to mark the end of the movement spell, and triggers the bot change direction
            
            self.turning = random.randrange(20,60)
            self.currentlyTurning = True
        
        if self.turning == 0 and self.currentlyTurning:
        #if the bot is still turning, it should stop turning and begin its linear path

            self.moving = random.randrange(40,100)
            self.currentlyTurning = False
        
    
    def FormationLinearWander(self, bots):
        if self.currentlyTurning == True:
        #if the bot is in the process of turning
            
            self.vl = -2.0
            self.vr = 2.0
            #turns to the left
            
            
            self.turning -= 1
            #keep track of how many turns

        else:
            #bot in linear motion
            self.vl = 5.0
            self.vr = 5.0
            #the difference between this and 'Random Wander' is that bot doesn't randomly turn;..
            #..it only turns where there an obstacle is met


        self.WallCollision()
        # checks for wall collision and takes necessary action

        
        if self.IsBotColliding(bots):
            self.CollisionMechanics()


        if self.turning == 0 and self.currentlyTurning:
        #if the bot is still turning, it should stop turning and begin its linear path

            self.moving = random.randrange(100,200)
            self.currentlyTurning = False


    def BisectorSearch(self, bots):
    #AUTHOR: Yash Suresh , 2023
        if self.currentlyTurning == True:
        #if the bot is in the process of turning
            
            self.vl = -2.0
            self.vr = 2.0
            #turns to the left
            
            
            self.turning -= 1
            #keep track of how many turns

        else:
            #bot in linear motion
            self.vl = 5.0
            self.vr = 5.0
            #the difference between this and 'Random Wander' is that bot doesn't randomly turn;..
            #..it only turns where there an obstacle is met


        self.WallCollision()
        # checks for wall collision and takes necessary action

        if self.x <= 600 and self.x >= 595:
            self.x = 594
                
            self.turning = 30 
            self.currentlyTurning = True

        elif self.x > 600 and self.x <= 605:
            self.x = 606

            self.turning = 30
            self.currentlyTurning = True

        if self.IsBotColliding(bots):
            self.CollisionMechanics()


        if self.turning == 0 and self.currentlyTurning:
        #if the bot is still turning, it should stop turning and begin its linear path

            self.moving = random.randrange(100,200)
            self.currentlyTurning = False

    def QuadrantSearch(self, bots):
    #AUTHOR: Yash Suresh , 2023

        if self.currentlyTurning == True:
        #if the bot is in the process of turning
            
            self.vl = -2.0
            self.vr = 2.0
            #turns to the left
            
            
            self.turning -= 1
            #keep track of how many turns

        else:
            #bot in linear motion
            self.vl = 5.0
            self.vr = 5.0
            #the difference between this and 'Random Wander' is that bot doesn't randomly turn;..
            #..it only turns where there an obstacle is met


        self.WallCollision()
        # checks for wall collision and takes necessary action
        
        if self.x <= 600 and self.x >= 595:
            self.x = 594
                
            self.turning = 30 
            self.currentlyTurning = True

        elif self.x > 600 and self.x <= 605:
            self.x = 606

            self.turning = 30
            self.currentlyTurning = True
        
        if self.y <=250 and self.y >= 245:
            self.y = 244

            self.turning = 30 
            self.currentlyTurning = True

        elif self.y > 250 and self.y <= 255:
            self.y = 256

            self.turning = 30 
            self.currentlyTurning = True

        if self.IsBotColliding(bots):
            self.CollisionMechanics()


        if self.turning == 0 and self.currentlyTurning:
        #if the bot is still turning, it should stop turning and begin its linear path

            self.moving = random.randrange(100,200)
            self.currentlyTurning = False


    def Repel(self, bots):
    #AUTHOR: Yash Suresh , 2023

        if self.currentlyTurning == True:
        #if the bot is in the process of turning
            
            self.vl = -2.0
            self.vr = 2.0
            #turns to the left
            
            
            self.turning -= 1
            #keep track of how many turns

        else:
            #bot in linear motion
            self.vl = 5.0
            self.vr = 5.0
            #the difference between this and 'Random Wander' is that bot doesn't randomly turn;..
            #..it only turns where there an obstacle is met


        self.WallCollision()
        # checks for wall collision and takes necessary action
        
        if self.IsRepel(bots):
            self.CollisionMechanics()

        if self.turning == 0 and self.currentlyTurning:
        #if the bot is still turning, it should stop turning and begin its linear path

            self.moving = random.randrange(100,200)
            self.currentlyTurning = False

        
    def IsRepel(self, bots):
    #AUTHOR: Yash Suresh , 2023
        
        repelThreshold = 200
        tooClose = False
        
        for bot in bots:
            if bot != self:
                #print(self.distanceTo(bot))
                if self.distanceTo(bot) <= repelThreshold:
                    tooClose = True

                    
                
                else:
                    tooClose = False

            else:
                pass

        return tooClose
