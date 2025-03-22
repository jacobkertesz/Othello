import pygame

pygame.init()

# Screen Size
WIDTH = 800
HEIGHT = 800

# Board Size
ROWS, COLS = 8, 8
SQUARESIZE = WIDTH//COLS

# Colors
GREEN = (0,100,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (128,128,128)
BOARDCOLOR = GREEN

# Other
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


# Classes
class Board:
    def __init__(self):
        self.board = [
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]
        ]
        self.pieces = 0
    
    def drawBoard(self, display):
        borders = 0
        c = 100

        while borders < COLS:
            pygame.draw.line(display, BLACK,
                             [c,0],[c,800],2)
            pygame.draw.line(display, BLACK,
                             [0,c],[800,c],2)
            c += 100
            borders += 1

    def addDisk(self, row, y, color):
        disk = Disk(row,y,color)
        self.board[row][y] = disk
        disk.findPose()
        disk.draw(SCREEN)
        self.pieces += 1
        
class Disk:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

        self.x = 0
        self.y = 0
    
    def findPose(self):
        self.x = SQUARESIZE * self.col + SQUARESIZE // 2
        self.y = SQUARESIZE * self.row + SQUARESIZE // 2

    def flipDisk(self):
        if self.color == WHITE:
            self.color = BLACK
        else:
            self.color = WHITE

    def draw(self, display):
        pygame.draw.circle(display, self.color, (self.x, self.y), 45)


# General Functions
def getMousePos(pos):
    x, y = pos
    row = y // SQUARESIZE
    col = x // SQUARESIZE
    return row, col

def collectDisks(row,col,board,turn):
    item = board.board[row][col]
    disksToFlip = []

    if item == 0: # if space is unoccupied
        mod = 0
        while mod < 8: # each direction
            catch = checkDirect(row,col,board,turn,mod,[])
            for disk in catch:
                disksToFlip.append(disk)
            mod +=1

    return disksToFlip
    
def checkDirect(row,col,board,turn,mod,currCatch):
    checkRowLow = row > 0
    checkColLow = col > 0
    checkRowHigh = row < 7
    checkColHigh = col < 7

    if mod == 0 and checkRowLow and checkColLow: #nw
        row-=1
        col-=1
    elif mod == 1 and checkColLow: #n
        col-=1
    elif mod == 2 and checkRowHigh and checkColLow: #ne
        row+=1
        col-=1
    elif mod == 3 and checkRowHigh: #e
        row+=1
    elif mod == 4 and checkRowHigh and checkColHigh: #se
        row+=1
        col+=1
    elif mod == 5 and checkColHigh: #s
        col+=1
    elif mod == 6 and checkRowLow and checkColHigh: #sw
        row-=1
        col+=1
    elif mod == 7 and checkRowLow: #w
        row-=1
    else:
        return []

    item = board.board[row][col]
    if item !=0:
        if item.color == turn:
            return currCatch
        else:     
            currCatch.append(item)
            return checkDirect(row,col,board,turn,mod,currCatch)
    else:
        return [] 
    
def startingSetup(gameBoard):
    gameBoard.addDisk(3,3,WHITE)
    gameBoard.addDisk(3,4,BLACK)
    gameBoard.addDisk(4,3,BLACK)
    gameBoard.addDisk(4,4,WHITE)
        
def changeTurn(turn):
    if turn == BLACK:
        turn = WHITE
    else:
        turn = BLACK
    return turn


# Display Setup
SCREEN.fill(BOARDCOLOR)
gameBoard = Board()
gameBoard.drawBoard(SCREEN)
startingSetup(gameBoard)
pygame.display.update()

def main():
    # Game Loop
    run = True
    clock = pygame.time.Clock()
    turn = BLACK # Black always starts
    winner = False

    while run:
        clock.tick(FPS)
        for event in pygame.event.get(): # Checks Events

            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN: # Reset Game 
                if event.key == pygame.K_r:
                    turn = BLACK
                    winner = False
                    gameBoard.board = [
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0]
                    ]
                    gameBoard.pieces = 0
                    SCREEN.fill(BOARDCOLOR)
                    startingSetup(gameBoard)
                    gameBoard.drawBoard(SCREEN)

            if gameBoard.pieces < 64: # When the board is full, the game is over

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        turn = changeTurn(turn)

                if event.type == pygame.MOUSEBUTTONDOWN:  

                    pos = pygame.mouse.get_pos()
                    row, col = getMousePos(pos)

                    disks = collectDisks(row,col,gameBoard,turn)
                    if len(disks) > 0:
                        gameBoard.addDisk(row,col,turn)
                        for disk in disks:
                            disk.flipDisk()
                            disk.draw(SCREEN)

                        turn = changeTurn(turn)
            
            else:
                if winner == False: # Determine winner

                    piecesW = []
                    piecesB = []

                    for row in gameBoard.board: # Organize Disks by color
                        for disk in row:
                            if disk.color == WHITE:
                                piecesW.append(disk)
                            elif disk.color == BLACK:
                                piecesB.append(disk)

                    countW = len(piecesW)
                    countB = len(piecesB)

                    if countW > countB: # Lower length is loser
                        loser = piecesB
                    elif countB > countW:
                        loser = piecesW
                    else: # tie
                        loser = piecesB
                        for disk in piecesW:
                            loser.append(disk)
                    
                    for disk in loser: # Loser turns gray
                        disk.color = GRAY
                        disk.draw(SCREEN)
                                
                    winner = True
                            
        pygame.display.update()

    pygame.quit()

main()