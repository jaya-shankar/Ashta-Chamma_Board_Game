import pygame
import time

from helper import diceRoll, move, checkEnemy, possibleMoves, board_overview, adjustDisplay
from player import Player

#---------------------------------------------------------------------------------------------------
pygame.init()
SIZE=(width,height)=(800,600)
screen=pygame.display.set_mode((width,height))

#---------------------------------------------------------------------------------------------------
# Caption & icon
pygame.display.set_caption("Ashta Chamma")
icon=pygame.image.load("assets/icons/game_icon.png")
pygame.display.set_icon(icon)

#-------------------------------------------------------------------------
# Colours
WHITE = (255, 255, 255)
GRAY  = (180, 180, 180)
BLACK = (0, 0, 0)

# Turn colours R->B->Y->G
colors=[(250, 39, 55), (42, 122, 218), (58, 154, 26), (220, 160, 20)]

home_colors=[WHITE, WHITE, WHITE, WHITE]
#---------------------------------------------------------------------------------------------------
# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)


#---------------------------------------------------------------------------------------------------
# Board setup
HEIGHT = 9
WIDTH = 9
BOARD_PADDING = 20												  
board_height = ((7/8) * height) - (BOARD_PADDING * 2)	
board_width = width - (BOARD_PADDING * 2)
cell_size = int(min(board_height / WIDTH, board_width / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

#----------------------------------------------------------------------------------------------------------
# Intialization
START=True
isBoardDrawn=True
running=True
changeTurn=True
mainPage=True
helpPage=False
rollDone=False
calculateNow=False
moveDone=True
disNum=""
moves=[]
k=[]
for i in range(4):
	k.append(False)
allPawns=[]

turn=-1
safe_places=[ (1,4), (2,2), (2,6), (4,1), (4,4), (4,7), (6,2), (6,6), (7,4) ]
home_places=[(4,8), (8,4), (4,0), (0,4)]

#----------------------------------------------------------------------------------------
# Importing and Resizing Images
cross=pygame.image.load("assets/icons/cross.png")
cross=pygame.transform.scale(cross,(53,53))

game_name=pygame.image.load("assets/icons/logo.gif")
game_name=pygame.transform.scale(game_name,(600,100))

instructions=pygame.image.load("assets/icons/instruction.png")
instructions=pygame.transform.scale(instructions, (790,350))
#------------------------------------------------------------------------------------------------------------------------

def drawPawn(pawn,position):
	""" Takes Pawn and Postion as input and renders the pawn at the given postion"""

	screen.blit(pawn,position)

def drawBoard():
	""" Draws the board on to the screen and return a 2D list representing each positon of the square """

	cells = []
	h_color=0
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
				if((i,j) in safe_places):
					pygame.draw.rect(screen, (240, 207, 174), rect)
					pygame.draw.rect(screen, WHITE, rect, 2)
					screen.blit(cross,(board_origin[0] + j * cell_size,board_origin[1] + i * cell_size))
				else:
					pygame.draw.rect(screen, (240, 207, 174), rect)
					pygame.draw.rect(screen, WHITE, rect, 2)
			else:
				if((i,j) in home_places):
					pygame.draw.rect(screen,home_colors[h_color], rect)
					pygame.draw.rect(screen, WHITE, rect, 2)
					h_color=(h_color+1)%4
					
				else:
					pygame.draw.rect(screen, BLACK, rect)
					pygame.draw.rect(screen, BLACK, rect, 2)
			row.append(rect)
		cells.append(row)
	return cells

def drawEverything():
	""" Renders all the pawns on to the board """

	cells=drawBoard()
	for j in range(4):
		for i in range(4):
			drawPawn(allPawns[i][j].image,allPawns[i][j].Position)

while running:
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			running=False


	#-----------------------------------------------Main Menu Page-------------------------------------------------------
	if(mainPage):
		screen.blit(game_name,(100,200))
		#-----------------------------------------Rendering Play Button-------------------------------------------------
		playButton = pygame.Rect((3 * width)//8, (5 * height)//8, (height // 3) - BOARD_PADDING * 2, 50)
		playText = mediumFont.render("Play", True, BLACK)
		playRect = playText.get_rect()
		playRect.center = playButton.center
		pygame.draw.rect(screen, WHITE, playButton)
		screen.blit(playText, playRect)

		#-----------------------------------------------Rendering Help Button--------------------------------------------
		helpButton = pygame.Rect((3 * width)//8 , (13 * height)//16, (height // 3) - BOARD_PADDING * 2, 50)
		helpText = mediumFont.render("Rules", True, BLACK)
		helpRect = helpText.get_rect()
		helpRect.center = helpButton.center
		pygame.draw.rect(screen, WHITE, helpButton)
		screen.blit(helpText, helpRect)
		
		#---------------------------------------------------------------------------------------------------------------
		# Check if play button clicked
		click, _, _ = pygame.mouse.get_pressed()
		if click == 1:
			mouse = pygame.mouse.get_pos()

			#If Play button is clicked
			if playRect.collidepoint(mouse):
				mainPage = False
				screen.fill(BLACK)
				pygame.display.flip()

			#If Help button is clicked
			if helpRect.collidepoint(mouse):
				mainPage = False
				helpPage=True
				screen.fill(BLACK)
				pygame.display.flip()
		pygame.display.update()
	#----------------------------------------------------------------------------------------------------
	elif(helpPage):
		screen.blit(instructions,(5,10))
		backButton = pygame.Rect((3 * width)//8, (13 * height)//16, (height // 3) - BOARD_PADDING * 2, 50)
		
		#-------------------------------------------Rendering Back Button----------------------------------
		backText = mediumFont.render("Back", True, BLACK)
		backRect = backText.get_rect()
		backRect.center = backButton.center
		pygame.draw.rect(screen, WHITE, backButton)
		screen.blit(backText, backRect)
		#-------------------------------------------------------------------------------------------------------

		click, _, _ = pygame.mouse.get_pressed()
		if click == 1:
			mouse = pygame.mouse.get_pos()

			#If Back button is clicked
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

		#------------------------------------Display the number on the die-------------------------------------
		displayBox = pygame.Rect((7 * height)//8 + BOARD_PADDING, (4 * width)//8 + BOARD_PADDING, (height//3) - BOARD_PADDING * 2, 50)
		pygame.draw.rect(screen, WHITE, displayBox)
		#-----------------------------------------------------------------------------------------------------
		
		N = mediumFont.render(str(disNum), True, BLACK)
		textRect = N.get_rect()
		textRect.center = displayBox.center
		screen.blit(N, textRect)
		
		#---------------------------------------Box shows who's turn it is-------------------------------------
		turnBox = pygame.Rect((7 * height)//8 + BOARD_PADDING, (2 * width)//8 + BOARD_PADDING, (height//3) - BOARD_PADDING * 2, 50)
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

		#-----------------------------------------Roll Button-----------------------------------
		rollButton = pygame.Rect((7 * height)//8 + BOARD_PADDING, (5 * width)//8 + 20, (height//3) - BOARD_PADDING * 2, 50)
		buttonText = mediumFont.render("Roll", True, BLACK)
		buttonRect = buttonText.get_rect()
		buttonRect.center = rollButton.center
		pygame.draw.rect(screen, WHITE, rollButton)
		screen.blit(buttonText, buttonRect)
		
	   #-----------------------------------------Exit Button-----------------------------------
		exitButton = pygame.Rect((7 * height)//8 + BOARD_PADDING, (1 * width)//8 , (height//3) - BOARD_PADDING * 2, 50)
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
				if(int(Num)%4==0):  #if the dice roll is 4 or 8 then give another chance
					diceNumbers.append(Num)
					disNum=disNum+Num+" "
					calculateNow=False
					changeTurn=False
					rollDone=False
				else:
					disNum=disNum+Num+" "
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
						

						disNum=adjustDisplay(disNum)
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
		

			drawEverything()
			if(exitButton.collidepoint(mouse)):
				mainPage=True
				START=True
				isBoardDrawn=True
				moves=[]
				screen.fill(BLACK)
				pygame.display.flip()
		
		pygame.display.update()
	



