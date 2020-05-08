import pygame


class Player():
    def __init__(self,cells,i,j):
        self.image=pygame.image.load("assets/icons/"+str(i)+".gif")
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
        c=self.color
        i=self.number

        self.Tup=newPostion
        self.Position=cells[self.Tup[0]][self.Tup[1]].center
        self.Position=(self.Position[0]-(int(c/2)*25),self.Position[1]-((c%2)*25))
        self.Position=(self.Position[0],self.Position[1]-(3*i)+(9*(c%2)))
        self.Button=pygame.Rect(self.Position, self.image.get_size())

    def goToStart(self,cells):
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
        self.image=pygame.image.load("assets/icons/b.gif")

    def decreaseSize(self):
        i=self.color
        self.image=pygame.image.load("assets/icons/"+str(i)+".gif")
        
