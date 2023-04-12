
from copy import deepcopy
from sys import exit
from pygame.locals import *
import sys 
import pygame
from global_vars import *

STARTING_NUMBER_OF_STONES = 4

# Set the depths of the AI for each player to run simulations 
global profundidade1 
profundidade1 = 1

global profundidade2 
profundidade2 = 1

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

    def available_moves(self, board, player):
        # Determine which pits to consider based on the player
        if player == '1':
            pits = PLAYER_1_PITS
        else:
            pits = PLAYER_2_PITS

        # Create a list of available moves (pits with stones)
        moves = [pit for pit in pits if board[pit] > 0]
        return moves
    
    def simulate_move(self, board, player, move):
        new_board = board.copy()
        new_player = '1' if player == '2' else '2'
        self.makeMove(new_board, player, move)
        return new_board, new_player
    
    def evaluate_board(self, board):
            #Heuristic used for the minimax algorithm
            return board['2'] - board['1']
        
    def minimax(self, board, player, depth, alpha, beta, is_maximizing):
        if depth == 0 or self.checkForWinner(board) != 'no winner':
            return self.evaluate_board(board, player)

  
        # Get the available moves for the current player
        moves = self.available_moves(board, player)

        # If the current player is maximizing their score
        if is_maximizing:
            max_eval = float('-inf')
            for move in moves:
                # Simulate the move and get the resulting board and player
                new_board, new_player = self.simulate_move(board, player, move)
                # Recursively call the minimax function
                eval = self.minimax(new_board, new_player, depth - 1, alpha, beta, False)
                # Update the maximum evaluation and alpha values
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                # Perform alpha-beta pruning if necessary
                if beta <= alpha:
                    break
            return max_eval
        
        # If the current player is minimizing their score
        else:
            min_eval = float('inf')
            for move in moves:
                # Simulate the move and get the resulting board and player
                new_board, new_player = self.simulate_move(board, player, move)
                # Recursively call the minimax function
                eval = self.minimax(new_board, new_player, depth - 1, alpha, beta, True)
                # Update the minimum evaluation and beta values
                min_eval = min(min_eval, eval)
                 # Perform alpha-beta pruning if necessary
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def find_best_move(self, board, player, depth):
        best_move = None
        best_eval = float('-inf')
        # Get the available moves for the current player
        moves = self.available_moves(board, player)

        # For each move, simulate the move and call the minimax function to evaluate the move
        for move in moves:
            new_board, new_player = self.simulate_move(board, player, move)
            eval = self.minimax(new_board, new_player, depth - 1, float('-inf'), float('inf'), False)
            
            # If the evaluation is better than the previous best evaluation, update the best evaluation and best move
            if eval > best_eval:
                best_eval = eval
                best_move = move

        return best_move

    def execute_minimax_move(self, evaluate_func, depth):
        def execute_minimax_move_aux():
            state = State()
            best_move = None
            best_eval = float('-inf')

            for move in state.available_moves():
                new_mancala_game = state.makeMove(move)
                new_state_eval = self.minimax(new_mancala_game, depth - 1, float('-inf'), float('+inf'), False, state.current_player(), evaluate_func)
                if new_state_eval > best_eval:
                    best_move = move
                    best_eval = new_state_eval
            state.apply_move(best_move)

        return execute_minimax_move_aux

class MancalaGame:

    def __init__(self, player_1, player_2):
        # Initialize the game state
        self.state = State()
        # Set the players
        self.player_1 = player_1
        self.player_2 = player_2
        # Set up the game window
        pygame.display.set_caption("Mancala Game")
        self.tela = pygame.display.set_mode((1400, 788))
        # Set the current player turn and difficulty level
        self.player_turn = '1'

        # Initialize the game loop variables
        self.running = True

    def main(self):
        gameBoard = self.state.getNewBoard()

        running = True

        # Loop until game is over    
        while running:  
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

            # Display the current game board
            self.state.displayBoard(gameBoard)

            # If it's the computer's turn, choose the best move using minimax algorithm
            if self.player_turn == self.player_2:
                move = self.state.find_best_move(gameBoard, self.player_2, depth=self.difficulty)
                self.player_turn = self.state.makeMove(gameBoard, self.player_2, move)
            # If it's the player's turn, ask for their move and update the game board
            else:
                player_move = self.state.askForPlayerMove(self.player_turn, gameBoard)
                self.player_turn = self.state.makeMove(gameBoard, self.player_turn, player_move)

            # Check if the game has ended and display the winner
            self.winner = self.state.checkForWinner(gameBoard)
            if self.winner == '1':
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
                pygame.time.wait(1000)

            elif self.winner == '2':  
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
                pygame.time.wait(1000)

            elif self.winner == '0':  
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
                pygame.time.wait(1000)

        self.state.displayBoard(gameBoard)

    def get_winner(self):
        return self.winner

def play_multiple_games(num_games, player_1, player_2):
    global profundidade1 
    global profundidade2 
    results = {"player_1": 0, "player_2": 0, "draws": 0}
    # Play the chosen number of games
    for i in range(num_games):
        game = MancalaGame(player_1, player_2)
        # Play the game
        game.main()

        # Determine the winner of the game and update results
        winner = game.get_winner()
        if winner == '1':
            results["player_1"] += 1
        elif winner == '2':
            results["player_2"] += 1
        elif winner == '0':
            results["draws"] += 1

        # Print the results for the current game
        print("Player 1 depth: " + str(profundidade1))
        print("Player 2 depth: " + str(profundidade2))
        if winner == '1':
            print("Game number "+ str(i+1) + " - winner: player 1")
        elif winner == '2':
            print("Game number "+ str(i+1) + " - winner: player 2")
        elif winner == '0':
            print("Game number "+ str(i+1) + " - Tie")
        print("-------------------------")

        # Increment the difficulty level for the player you choose
        profundidade2 +=1 # Change to profundidade1 if you want player 2 to be the same every time the game runs

    return results


if __name__ == "__main__":
    player_1 = '1'
    player_2 = '2'
    num_games = 1  # Set this number to the desired number of games to run
    results = play_multiple_games(num_games, player_1, player_2)
    print(f"Results after {num_games} games:")
    print(f"Player 1 wins: {results['player_1']}")
    print(f"Player 2 wins: {results['player_2']}")
    print(f"Ties: {results['draws']}")
