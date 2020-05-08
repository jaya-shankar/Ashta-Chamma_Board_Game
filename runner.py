import pygame
import time

from helper import diceRoll,move,checkEnemy,safe_places,possibleMoves,board_overview
from classes import Player

HEIGHT = 9
WIDTH = 9

pygame.init()
SIZE=(width,height)=(800,600)
screen=pygame.display.set_mode((width,height))

pygame.display.set_caption("Ashta Chamma")

icon=pygame.image.load("assets/icons/game_icon.png")
pygame.display.set_icon(icon)


# Colours
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)
LIGHT_BLUE = (102, 204, 255)

RED = (255, 0, 0)
BLUE = (30, 144, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

colors=[RED, BLUE,YELLOW,GREEN]
turn=-1

# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)

BOARD_PADDING = 20
board_height = ((7/8) * height) - (BOARD_PADDING * 2)
board_width = width - (BOARD_PADDING * 2)
cell_size = int(min(board_height / WIDTH, board_width / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)
print("width=        "+str(width))
print("height=         "+str(height))
print("board_height=  "+str(board_width))
print("board_width=   "+str(board_height))
print("board_origin=  "+str(board_origin))
print("cell_size=     "+str(cell_size))

START=True
isBoardDrawn=True
running=True
changeTurn=True
mainPage=True
helpPage=False
rollDone=False
calculateNow=False
moveDone=True
disNum=" "
moves=[]
k=[]
for i in range(4):
    k.append(False)


allPawns=[]
cross=pygame.image.load("assets/icons/cross.gif")
cross=pygame.transform.scale(cross,(53,53))
game_name=pygame.image.load("assets/icons/logo.gif")
game_name=pygame.transform.scale(game_name,(600,100))
instructions=pygame.image.load("assets/icons/instruction.gif")
instructions=pygame.transform.scale(instructions,(790,350))

def drawPawn(pawn,position):
    screen.blit(pawn,position)

def drawBoard():
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

                # Draw rectangle for cell
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            if(i!=0 and i!=HEIGHT-1 and j!=0 and j!=WIDTH-1):
                if((i==1 and j==4) or (i==2 and j==2) or (i==2 and j==6) or (i==4 and j==1) or
                    (i==4 and j==4) or (i==4 and j==7) or (i==6 and j==2) or (i==6 and j==6) or (i==7 and j==4)):
                    pygame.draw.rect(screen, GRAY, rect)
                    pygame.draw.rect(screen, WHITE, rect, 3)
                    screen.blit(cross,(board_origin[0] + j * cell_size,board_origin[1] + i * cell_size))
                else:
                    pygame.draw.rect(screen, GRAY, rect)
                    pygame.draw.rect(screen, WHITE, rect, 3)
            else:
                if((i==0 and j==4) or (i==4 and j==0) or (i==8 and j==4) or (i==4 and j==8) ):
                    pygame.draw.rect(screen, LIGHT_BLUE, rect)
                    pygame.draw.rect(screen, WHITE, rect, 3)
                else:
                    pygame.draw.rect(screen, BLACK, rect)
                    pygame.draw.rect(screen, BLACK, rect, 3)
            row.append(rect)
        cells.append(row)
    return cells

def drawEverything():
    cells=drawBoard()
    for j in range(4):
        for i in range(4):
            drawPawn(allPawns[i][j].image,allPawns[i][j].Position)

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False


    # Play Button
    if(mainPage):
        screen.blit(game_name,(100,200))
        playButton = pygame.Rect(
            (3 / 8) * width , (5/8) * height,
            (height / 3) - BOARD_PADDING * 2, 50
        )
        playText = mediumFont.render("Play", True, BLACK)
        playRect = playText.get_rect()
        playRect.center = playButton.center
        pygame.draw.rect(screen, WHITE, playButton)
        screen.blit(playText, playRect)

        helpButton = pygame.Rect(
            (3 / 8) * width , (13/16) * height,
            (height / 3) - BOARD_PADDING * 2, 50
        )
        helpText = mediumFont.render("Rules", True, BLACK)
        helpRect = helpText.get_rect()
        helpRect.center = helpButton.center
        pygame.draw.rect(screen, WHITE, helpButton)
        screen.blit(helpText, helpRect)

        # Check if play button clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playRect.collidepoint(mouse):
                mainPage = False
                screen.fill(BLACK)
                pygame.display.flip()
            if helpRect.collidepoint(mouse):
                mainPage = False
                helpPage=True
                screen.fill(BLACK)
                pygame.display.flip()
        pygame.display.update()
    elif(helpPage):
        screen.blit(instructions,(5,10))
        backButton = pygame.Rect(
            (3 / 8) * width , (13/16) * height,
            (height / 3) - BOARD_PADDING * 2, 50
        )
        backText = mediumFont.render("Back", True, BLACK)
        backRect = backText.get_rect()
        backRect.center = backButton.center
        pygame.draw.rect(screen, WHITE, backButton)
        screen.blit(backText, backRect)

        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if backRect.collidepoint(mouse):
                mainPage = True
                helpPage=False
                screen.fill(BLACK)
                pygame.display.flip()
        pygame.display.update()
    else:
        left, _, right = pygame.mouse.get_pressed()
            
        #Place paws on board
        if(START):
            isBoardDrawn=False
            cells=drawBoard()
            for i in range(4):
                pawns=[]
                for j in range(4):

                    pawn=Player(cells,i,j)
                    pawns.append(pawn)

                allPawns.append(pawns)
            drawEverything()
            START=False

        # Display Number
        displayBox = pygame.Rect(
            (7 / 8) * height+ BOARD_PADDING, (4 / 8) * width + BOARD_PADDING,
            (height / 3) - BOARD_PADDING * 2, 50
        )
        pygame.draw.rect(screen, WHITE, displayBox)
        
        N = mediumFont.render(str(disNum), True, BLACK)
        textRect = N.get_rect()
        textRect.center = displayBox.center
        screen.blit(N, textRect)

        # who's Turn
        turnBox = pygame.Rect(
            (7 / 8) * height+ BOARD_PADDING, (2 / 8) * width + BOARD_PADDING,
            (height / 3) - BOARD_PADDING * 2, 50
        )
        if(changeTurn):  #decides whether to change the color or not
            turn=(turn+1)%4
            color = colors[turn]
            diceNumbers=[]
            changeTurn=False
            

        pygame.draw.rect(screen, color, turnBox)
        text = "Who's turn"
        text = mediumFont.render(text, True, BLACK)
        textRect = text.get_rect()
        textRect.center = turnBox.center
        screen.blit(text, textRect)

        # Roll Button
        rollButton = pygame.Rect(
            (7 / 8) *height + BOARD_PADDING, (5/8) * width + 20,
            (height / 3) - BOARD_PADDING * 2, 50
        )
        buttonText = mediumFont.render("Roll", True, BLACK)
        buttonRect = buttonText.get_rect()
        buttonRect.center = rollButton.center
        pygame.draw.rect(screen, WHITE, rollButton)
        screen.blit(buttonText, buttonRect)
        
       # Exit Button
        exitButton = pygame.Rect(
            (7 / 8) *height + BOARD_PADDING, (1/8) * width ,
            (height / 3) - BOARD_PADDING * 2, 50
        )
        exitText = mediumFont.render("Exit", True, BLACK)
        exitRect = buttonText.get_rect()
        exitRect.center = exitButton.center
        pygame.draw.rect(screen, WHITE, exitButton)
        screen.blit(exitText, exitRect)

        if(left==1):
            mouse = pygame.mouse.get_pos()

            if rollButton.collidepoint(mouse) and not changeTurn and not rollDone:
                number=diceRoll()
                Num=str(number[0])
                disNum=Num
                if(int(Num)%4==0):  #if the dice roll is 4 or 8 then give another chance
                    diceNumbers.append(Num)
                    calculateNow=False
                    changeTurn=False
                    rollDone=False
                else:
                    diceNumbers.append(Num)
                    calculateNow=True
                    rollDone=True

            
            if(calculateNow):
                for i in diceNumbers:
                    if(moveDone):
                        moves=possibleMoves(i,allPawns[turn],k[turn])
                        Num=i
                        diceNumbers.remove(i)
                        moveDone=False
                        calculateNow=False
                    if(len(moves)==0):
                        rollDone=False
                        changeTurn=True
                        moveDone=True
                        calculateNow=True
                        
                        Num=0
                if((rollDone and not moveDone)) or len(diceNumbers)!=0:
                    for pawn in moves:
                        pawn.increaseSize()
                        drawPawn(pawn.image,pawn.Position)
                    pygame.display.update()
                    
            else:
                for pawn in moves:
                    if(pawn.Button.collidepoint(mouse)):
                        newPostion=move(Num, pawn.Tup, pawn.color, k[pawn.color])
                        
                        board_overview[pawn.Tup]=None
                        pawn.changePosition(newPostion,cells)
                        if(newPostion==(4,4)):
                            if(gameDone(allPawns[pawn.color])):
                                winnerText = mediumFont.render("Winner is "+str(pawn.color)+" Player", True, colors[pawn.color])
                                screen.blit(winnerText,(width/2,height/2))
                                rollDone=True
                                drawEverything()
                        enemy=checkEnemy(pawn.Tup,pawn.color)

                        if(enemy!=None):   #if enemy is present kill the enemy 
                            enemy.goToStart(cells)
                            k[pawn.color]=True
                            changeTurn=False
                        elif (len(diceNumbers)==0):
                            changeTurn=True

                        if(board_overview[newPostion]!="X"):
                            board_overview[pawn.Tup]=pawn
                        disNum=" "
                        Num=0
                        
                        rollDone=False
                        moveDone=True
                        calculateNow=True
                        break
                if(not rollDone and moveDone and len(diceNumbers)==0):
                    for pawn in allPawns[turn]:
                        pawn.decreaseSize()
                        drawPawn(pawn.image,pawn.Position)
                    pygame.display.update()
        

            drawEverything() # this function redraws the board with 
            if(exitButton.collidepoint(mouse)):
                mainPage=True
                START=True
                isBoardDrawn=True
                moves=[]
                screen.fill(BLACK)
                pygame.display.flip()
        pygame.display.update()
    



