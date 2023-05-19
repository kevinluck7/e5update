import pygame, sys
import time
import datetime
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

def draw_chess_board():
    for row in range(15):
        pygame.draw.line(screen, BLACK, [40, 40 + row * 40], [600, 40 + row * 40], 1)
        pygame.draw.line(screen, BLACK, [40 + row * 40, 40], [40 + row * 40, 600], 1)

def draw_chess_piece(x, y, player):
    if player == 'black':
        pygame.draw.circle(screen, BLACK, [x, y], 20, 0)
    else:
        pygame.draw.circle(screen, WHITE, [x, y], 20, 0)

def check_win(board, x, y, player):
    count = 1
    # check row
    i = 1
    while x-i >= 0 and board[x-i][y]==player:
        i += 1
        count += 1
    i = 1
    while x+i < 15 and board[x+i][y]==player:
        i += 1
        count += 1
    if count >= 5:
        return True

    # check column
    count = 1
    i = 1
    while y-i >= 0 and board[x][y-i]==player:
        i += 1
        count += 1
    i = 1
    while y+i < 15 and board[x][y+i]==player:
        i += 1
        count += 1
    if count >= 5:
        return True

    # check diagonal
    count = 1
    i = 1
    while x-i>=0 and y-i>=0 and board[x-i][y-i]==player:
        i += 1
        count += 1
    i = 1
    while x+i<15 and y+i<15 and board[x+i][y+i]==player:
        i += 1
        count += 1
    if count >= 5:
        return True

    # check anti-diagonal
    count = 1
    i = 1
    while x-i>=0 and y+i<15 and board[x-i][y+i]==player:
        i += 1
        count += 1
    i = 1
    while x+i<15 and y-i>=0 and board[x+i][y-i]==player:
        i += 1
        count += 1
    if count >= 5:
        return True

    return False

def is_valid_move(board, x, y):
    if x<0 or x>=15 or y<0 or y>=15:
        return False
    elif board[x][y] != '':
        return False
    else:
        return True

def get_available_moves(board):
    available_moves = []
    for i in range(15):
        for j in range(15):
            if board[i][j] == '':
                available_moves.append((i, j))
    return available_moves

def get_ai_move(board, ai_player):
    available_moves = get_available_moves(board)
    for move in available_moves:
        # check if ai_player wins with this move
        x, y = move
        board[x][y] = ai_player
        if check_win(board, x, y, ai_player):
            board[x][y] = ''
            return x, y
        board[x][y] = ''

    for move in available_moves:
        # check if opponent wins with this move
        x, y = move
        opponent = 'white' if ai_player == 'black' else 'black'
        board[x][y] = opponent
        if check_win(board, x, y, opponent):
            board[x][y] = ''
            return x, y
        board[x][y] = ''

    return random.choice(available_moves)

def show_game_result(winner):
    font = pygame.font.Font(None, 36)
    text = font.render(winner.capitalize() + " wins!", 1, BLACK)
    screen.blit(text, (40, 630))

pygame.init()

SCREEN_SIZE = (660, 680)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("五子棋")

board = [['' for j in range(15)] for i in range(15)]
player = 'black'
game_over = False
winner = ''

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if player == 'black':
                x, y = event.pos
                row = round((y - 40) / 40)
                col = round((x - 40) / 40)
                if is_valid_move(board, row, col):
                    board[row][col] = player
                    draw_chess_piece((col * 40) + 40, (row * 40) + 40, player)
                    if check_win(board, row, col, player):
                        winner = player
                        game_over = True
                    player = 'white'
            else:
                x, y = get_ai_move(board, 'white')
                board[x][y] = 'white'
                draw_chess_piece((y * 40) + 40, (x * 40) + 40, 'white')
                if check_win(board, x, y, 'white'):
                    winner = 'white'
                    game_over = True
                player = 'black'

    draw_chess_board()
    for i in range(15):
        for j in range(15):
            if board[i][j] != '':
                draw_chess_piece((j * 40) + 40, (i * 40) + 40, board[i][j])
    pygame.display.update()

if winner != '':
    show_game_result(winner)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

pygame.quit()
