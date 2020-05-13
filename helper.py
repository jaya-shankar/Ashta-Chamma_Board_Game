import random
from classes import Player

redPath=[(0,4), (1,4), (1,3), (1,2), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7), (6,7), (5,7), (4,7), (3,7), (2,7), (1,7), (1,6), (1,5), 
            (2,6), (3,6), (4,6), (5,6), (6,6), (6,5), (6,4), (6,3), (6,2), (5,2), (4,2), (3,2), (2,2), (2,3), (2,4), (2,5), 
                (3,5), (4,5), (5,5), (5,4), (5,3), (4,3), (3,3),(3,4), 
                    (4,4)]


bluePath=[(4,0), (4,1), (5,1), (6,1), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7), (6,7), (5,7), (4,7), (3,7), (2,7), (1,7), (1,6), (1,5), (1,4), (1,3), (1,2), (1,1), (2,1), (3,1), 
             (2,2), (2,3), (2,4), (2,5), (2,6), (3,6), (4,6), (5,6), (6,6), (6,5), (6,4), (6,3), (6,2), (5,2), (4,2), (3,2), 
                 (3,3),(3,4), (3,5), (4,5), (5,5), (5,4), (5,3), (4,3),
                    (4,4)]


yellowPath=[(8,4), (7,4), (7,5), (7,6), (7,7), (6,7), (5,7), (4,7), (3,7), (2,7), (1,7), (1,6), (1,5), (1,4), (1,3), (1,2), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (7,2), (7,3), 
             (6,2), (5,2), (4,2), (3,2), (2,2), (2,3), (2,4), (2,5), (2,6), (3,6), (4,6), (5,6), (6,6), (6,5), (6,4), (6,3), 
                 (5,3), (4,3),(3,3),(3,4), (3,5), (4,5), (5,5), (5,4), 
                    (4,4)]


greenPath=[(4,8), (4,7), (3,7), (2,7), (1,7), (1,6), (1,5), (1,4), (1,3), (1,2), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7), (6,7), (5,7),
              (6,6), (6,5), (6,4), (6,3), (6,2), (5,2), (4,2), (3,2), (2,2), (2,3), (2,4), (2,5), (2,6), (3,6), (4,6), (5,6), 
                (5,5), (5,4), (5,3), (4,3), (3,3),(3,4), (3,5), (4,5), 
                    (4,4)]

safe_places=[ (1,4), (2,2), (2,6), (4,1), (4,4), (4,7), (6,2), (6,6), (7,4) ]

home_places=[(4,8), (8,4), (4,0), (0,4)]


board_overview={}
for i in range(0,9):
    for j in range(0,9):
        key=(i,j)
        if(key in safe_places):
            board_overview[key]="X"
        else:
            board_overview[key]=None


def diceRoll():

    """Generates a random number from the possbile numbers based on the chances of each outcome"""
    possibleNumbers=[]
    for i in range(1,5):
        possibleNumbers.append(i)
    possibleNumbers.append(8)
    prob=[1/4, 3/8, 1/4, 1/16, 1/16]
    number=random.choices(population=possibleNumbers, weights=prob, k=1)

    return number

def move(N,currentPos,color,isKill):
    k=0
    newPosition=0
    path=selectPath(color)
    N=int(N)
    
    k=path.index(currentPos)
   
    if(k+N>24 and not isKill):
        newPosition=k
    elif(k+N>len(path)-1 or currentPos==path[-1]):
        newPosition=k
    else:
        newPosition=(k+N)

    return path[newPosition]


def possibleMoves(N,pawns,kill):
    allMoves=[]
    for pawn in pawns:
        currentPos=pawn.Tup
        newPos=move(N,currentPos,pawn.color,kill)
        if(currentPos!=newPos ):
            allMoves.append(pawn)
    return allMoves


def checkEnemy(position,color):
    if position not in safe_places:
        if board_overview[position]!=None:
            enemy=board_overview[position]
            board_overview[position]=color
            return enemy


def gameDone(pawns):
    for pawn in pawns:
        if(pawn.Tup!=(4,4)):
            return False
    return True


def selectPath(color):
    if(color==0):
        return redPath
    elif(color==1):
        return bluePath
    elif(color==2):
        return yellowPath
    elif(color==3):
        return greenPath
    

def adjustDisplay(disNum):
    arr=disNum.split(" ")
    arr.pop(0)
    disNum=""
    for i in arr:
        disNum=disNum+str(i)
    return disNum