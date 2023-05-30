#AUTHORS: Dept of Computer Sci @ UoN + Yash Suresh , 2023

class Counter:

    def __init__(self,canvas, totalGrass):

        self.grassCut = 0
        self.percentGrassCut = 0.0
        self.canvas = canvas
        self.totalGrass = totalGrass
        self.canvas.create_text(90,50,text="Percent of Grass Mowed: "+ str(self.percentGrassCut),tags="counter")
    

           
    def GrassMowed(self, canvas):
        self.grassCut +=1
        self.percentGrassCut = self.grassCut / self.totalGrass * 100

        self.canvas.itemconfigure("counter",text="Percent of Grass Mowed: {:.2f}%".format(self.percentGrassCut))
        

