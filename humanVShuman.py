
from sys import exit
from pygame.locals import *
import sys 
import pygame
from global_vars import *

STARTING_NUMBER_OF_STONES = 4 

class State:

    def __init__(self):
        pass

    def getNewBoard(self):
        s = STARTING_NUMBER_OF_STONES
        return {'1': 0, '2': 0, 'A': s, 'B': s, 'C': s, 'D': s, 'E': s,
                'F': s, 'G': s, 'H': s, 'I': s, 'J': s, 'K': s, 'L': s}  # initial board

    def displayBoard(self, board):

        # Prepare stone amounts for each pit
        stoneAmounts = []

        for pit in 'GHIJKL21ABCDEF':
            numStonesInThisPit = str(board[pit])
            stoneAmounts.append(numStonesInThisPit)

         # Define position constants
        posicao_mancala = 436
        posicao_1y = 557
        posicao_2y = 315

        # Load and display the board image
        tabuleiro_img = pygame.image.load("tabuleiro_3.png")
        tabuleiro_x = (largura - tabuleiro_img.get_width()) // 2
        tabuleiro_y = (altura - tabuleiro_img.get_height()) // 2
        tela.blit(tabuleiro_img, (tabuleiro_x, tabuleiro_y))
        pygame.display.flip()

        # Display stone amounts for each pit on the board
        texta = fonte1.render(str(stoneAmounts[8]), True, cor_texto)
        tela.blit(texta, (368, posicao_1y))

        textb = fonte1.render(str(stoneAmounts[9]), True, cor_texto)
        tela.blit(textb, (493, posicao_1y))

        textc = fonte1.render(str(stoneAmounts[10]), True, cor_texto)
        tela.blit(textc, (618, posicao_1y))

        textd = fonte1.render(str(stoneAmounts[11]), True, cor_texto)
        tela.blit(textd, (743, posicao_1y))

        texte = fonte1.render(str(stoneAmounts[12]), True, cor_texto)
        tela.blit(texte, (868, posicao_1y))

        textf = fonte1.render(str(stoneAmounts[13]), True, cor_texto)
        tela.blit(textf, (993, posicao_1y))

        textg = fonte1.render(str(stoneAmounts[5]), True, cor_texto)
        tela.blit(textg, (993, posicao_2y))

        texth = fonte1.render(str(stoneAmounts[4]), True, cor_texto)
        tela.blit(texth, (868, posicao_2y))

        texti = fonte1.render(str(stoneAmounts[3]), True, cor_texto)
        tela.blit(texti, (743, posicao_2y))

        textj = fonte1.render(str(stoneAmounts[2]), True, cor_texto)
        tela.blit(textj, (618, posicao_2y))

        textk = fonte1.render(str(stoneAmounts[1]), True, cor_texto)
        tela.blit(textk, (493, posicao_2y))

        textl = fonte1.render(str(stoneAmounts[0]), True, cor_texto)
        tela.blit(textl, (368, posicao_2y))

        # Display stone amounts for mancala pits
        text1 = fonte1.render(str(stoneAmounts[7]), True, cor_texto)
        tela.blit(text1, (1118, posicao_mancala))

        text2 = fonte1.render(str(stoneAmounts[6]), True, cor_texto)
        tela.blit(text2, (243, posicao_mancala))

        # Add a delay to make it better to visualize moves and update the display
        pygame.time.delay(200)
        pygame.display.update()
        

    def askForPlayerMove(self, pTurn, board):

        while True:
            # Display instructions based on the current player's turn
            if pTurn == '1':
                textMove1a = fonte1.render(
                    '1                                   A - F', True, cor_texto)
                tela.blit(textMove1a, (493, 50))
                pygame.display.update()
            elif pTurn == '2':
                textMove2 = fonte1.render(
                    '2                                   G - L', True, cor_texto)
                tela.blit(textMove2, (493, 50))
                pygame.display.update()
                

            # Wait for the player's input
            letter = None
            while letter is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        elif event.unicode.isalpha():
                            letter = event.unicode.upper()

            # Validate the player's input
            if (pTurn == '1' and letter not in PLAYER_1_PITS) or (
                pTurn == '2' and letter not in PLAYER_2_PITS):
                textj1 = fonte2.render(
                    'Please pick a letter on your side of the board.', True, cor_texto)
                tela.blit(textj1, (400, 100))
                pygame.display.update()
                continue

            # Check if the chosen pit is not empty
            if board.get(letter) == 0:
                textj2 = fonte2.render(
                    'Please pick a non-empty pit.', True, cor_texto)
                tela.blit(textj2, (520, 100))
                pygame.display.update()
                continue  # ask for another move if the player clicked on an empty pit
            return letter

    def makeMove(self, board, pTurn, pit):
        # Get the number of stones in the selected pit and empty it
        stonesToSow = board[pit]  
        board[pit] = 0  

        # Distribute the stones to the next pits
        while stonesToSow > 0:
            pit = NEXT_PIT[pit]
            # Skip opponent's Mancala
            if (pTurn == '1' and pit == '2') or (
                    pTurn == '2' and pit == '1'):
                continue
            board[pit] += 1
            stonesToSow -= 1

        # Apply the opposite pit rule
        if pTurn == '1' and pit in PLAYER_1_PITS and board[pit] == 1:
            oppositePit = OPPOSITE_PIT[pit]
            if board[oppositePit] > 0:
                board['1'] += board[oppositePit] + 1
                board[oppositePit] = 0
                board[pit] = 0
        elif pTurn == '2' and pit in PLAYER_2_PITS and board[pit] == 1:
            oppositePit = OPPOSITE_PIT[pit]
            if board[oppositePit] > 0:
                board['2'] += board[oppositePit] + 1
                board[oppositePit] = 0
                board[pit] = 0

        # Switch player's turn
        if pTurn == '1':
            return '2'
        elif pTurn == '2':
            return '1'

    def checkForWinner(self, board):

        # Calculate the total number of stones for each player
        player1Total = board['A'] + board['B'] + board['C']
        player1Total += board['D'] + board['E'] + board['F']
        player2Total = board['G'] + board['H'] + board['I']
        player2Total += board['J'] + board['K'] + board['L']

        # Check if any player has no stones left in their pits
        if player1Total == 0:
            board['2'] += player2Total
            for pit in PLAYER_2_PITS:
                board[pit] = 0
        elif player2Total == 0:
            board['1'] += player1Total
            for pit in PLAYER_1_PITS:
                board[pit] = 0
        else:
            return 'no winner'

         # Determine the winner based on the number of stones in their Mancala
        if board['1'] > board['2']: 
            return '1'
        elif board['2'] > board['1']:
            return '2'
        else:
            return '0'
        
    def get_mancala_stones(self, board):
        # Used later to display the results
        return board['1'], board['2']
    
class MancalaGame:

    def __init__(self):
        # Initialize the game state
        self.state = State()
        # Set up the game window
        pygame.display.set_caption("Mancala Game")
        self.tela = pygame.display.set_mode((1400, 788))
        # Set the current player
        self.player_turn = '1'

        # Initialize the game loop variables
        self.running = True

    def instructions(self):

        # Display intructions of how to play the game
        tabuleiro_img = pygame.image.load("instrucoes.png")
        tabuleiro_x = (largura - tabuleiro_img.get_width()) // 2
        tabuleiro_y = (altura - tabuleiro_img.get_height()) // 2
        tela.blit(tabuleiro_img, (tabuleiro_x, tabuleiro_y))
        pygame.display.flip()

        # Wait the player to press the space key after readimg intructions
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        return 

    def main(self):
        # Initializes the board
        gameBoard = State().getNewBoard()

        # Initializes the game state
        running = True

        # Shows game instructions
        MancalaGame().instructions()

        # Main loop until the game is over    
        while running:  
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

            # Displays the game board
            State().displayBoard(gameBoard)

            # Asks for the player move
            playerMove = State().askForPlayerMove(self.player_turn, gameBoard)

            # Executes the player move and updates the turn
            self.player_turn = State().makeMove(gameBoard, self.player_turn, playerMove)

            # Checks if the game is over and declares the winner
            winner = self.state.checkForWinner(gameBoard)

            if winner == '1':
                # Display winner 1 image and the final score
                tabuleiro_img = pygame.image.load("winner1.png")
                tabuleiro_x = (largura - tabuleiro_img.get_width()) // 2
                tabuleiro_y = (altura - tabuleiro_img.get_height()) // 2
                tela.blit(tabuleiro_img, (tabuleiro_x, tabuleiro_y))
                pygame.display.flip()
                mancala1, mancala2 = self.state.get_mancala_stones(gameBoard)
                textwin = fonte1.render(str(f"{mancala2} X {mancala1}"), True, cor_texto)
                tela.blit(textwin, (615, 500))
                pygame.display.update()
                running = False
                pygame.time.wait(5000)

            elif winner == '2':  
                # Display winner 2 image and the final score
                tabuleiro_img = pygame.image.load("winner2.png")
                tabuleiro_x = (largura - tabuleiro_img.get_width()) // 2
                tabuleiro_y = (altura - tabuleiro_img.get_height()) // 2
                tela.blit(tabuleiro_img, (tabuleiro_x, tabuleiro_y))
                pygame.display.flip()
                mancala1, mancala2 = self.state.get_mancala_stones(gameBoard)
                textwin = fonte1.render(str(f"{mancala2} X {mancala1}"), True, cor_texto)
                tela.blit(textwin, (615, 500))
                pygame.display.update()
                running = False
                pygame.time.wait(5000)

            elif winner == '0':  
                # Display tie image and the final score
                tabuleiro_img = pygame.image.load("tie.png")
                tabuleiro_x = (largura - tabuleiro_img.get_width()) // 2
                tabuleiro_y = (altura - tabuleiro_img.get_height()) // 2
                tela.blit(tabuleiro_img, (tabuleiro_x, tabuleiro_y))
                pygame.display.flip()
                mancala1, mancala2 = self.state.get_mancala_stones(gameBoard)
                textwin = fonte1.render(str(f"{mancala2} X {mancala1}"), True, cor_texto)
                tela.blit(textwin, (615, 500))
                pygame.display.update()
                running = False
                pygame.time.wait(5000)

        self.state.displayBoard(gameBoard)

# start the game
if __name__ == '__main__':
    game = MancalaGame()
    game.main()
