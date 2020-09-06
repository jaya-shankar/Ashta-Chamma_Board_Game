import pygame

class Player():
    def __init__(self,cells,i,j):
        self.image=pygame.image.load("assets/icons/"+str(i)+".png")
        if(i==3):
            self.Position=cells[4][8].center
            self.Tup=(4,8)
        else:
            self.Position=cells[i*4][((i+1)%2)*4].center
            self.Tup=((i*4),((i+1)%2)*4)
        self.Position=(self.Position[0]-(int(j/2)*25),self.Position[1]-((j%2)*25))
        self.color=i
        self.number=j
        self.Button=pygame.Rect(self.Position,self.image.get_size())

    def changePosition(self,newPostion,cells):
        """ Takes newPositon and position of all the pawns on board and changes the object's Positon to New Position"""

        c=self.color
        i=self.number

        self.Tup=newPostion
        self.Position=cells[self.Tup[0]][self.Tup[1]].center
        self.Position=(self.Position[0]-(int(c/2)*25),self.Position[1]-((c%2)*25))
        self.Position=(self.Position[0],self.Position[1]-(3*i)+(9*(c%2)))
        self.Button=pygame.Rect(self.Position, self.image.get_size())

    def goToStart(self,cells):
        """ Changes the object's position to it's Start Positon """
        
        i=self.color
        j=self.number
        if(i==3):
            self.Position=cells[4][8].center
            self.Tup=(4,8)
        else:
            self.Position=cells[i*4][((i+1)%2)*4].center
            self.Tup=((i*4),((i+1)%2)*4)
        self.Position=(self.Position[0]-(int(j/2)*25),self.Position[1]-((j%2)*25))
        self.Button=pygame.Rect(self.Position,self.image.get_size())

    def increaseSize(self):
        """ Increases the size of the object's Pawn Image """

        self.image=pygame.image.load("assets/icons/b.png")

    def decreaseSize(self):
        """ Decreases the size of the object's Pawn Image """
        
        i=self.color
        self.image=pygame.image.load("assets/icons/"+str(i)+".png")
        

