import pygame
import asyncio
import sys

# 0 = empty, -1 = player, 1 = bot
state = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

ROWS = 6
COLS = 7
CELL_SIZE = 80

PLAYER = -1
BOT = 1
EMPTY = 0




def reset_board():
    new_board = []

    for row in range(ROWS):
        new_row = []

        for col in range(COLS):
            new_row.append(0)

        new_board.append(new_row)

    return new_board


def valid_column(col, state):
    return state[0][col] == 0



def valid_board(state):
    for i in state:
        for j in i:
            if j == 0:
                return True
    return False


def actions(state):
    if not valid_board(state):
        return []

    legal = []

    for col in range(7):
        if valid_column(col, state):
            legal.append(col)

    return legal


def ordered_actions(state):
    moves = actions(state)
    preferred_order = [3, 2, 4, 1, 5, 0, 6]
    ordered_moves = []

    for i in preferred_order:
        if i in moves:
            ordered_moves.append(i)

    return ordered_moves



def copy_state(state):
    new_state = []

    for row in state:
        new_state.append(row.copy())

    return new_state



def result(state, action, player):
    if not valid_column(action, state):
        return None

    new_state = copy_state(state)

    for i in range(5, -1, -1):
        if state[i][action] == 0:
            new_state[i][action] = player
            return new_state

    return None


def is_terminal(state):
    # Horizontal win
    for i in range(6):
        last_player = 0
        count = 1
        for j in range(7):
            if state[i][j] == last_player and last_player != 0:
                count += 1
            elif state[i][j] != last_player:
                count = 1

            if count == 4:
                return True

            last_player = state[i][j]

    # Vertical win
    for i in range(7):
        last_player = 0
        count = 1
        for j in range(6):
            if state[j][i] == last_player and last_player != 0:
                count += 1
            elif state[j][i] != last_player:
                count = 1

            if count == 4:
                return True

            last_player = state[j][i]

    # Up-right diagonal win
    for i in range(6):
        for j in range(7):
            if i >= 3 and j <= 3 :
                pos1 = state[i][j]
                pos2 = state[i-1][j+1]
                pos3 = state[i-2][j+2]
                pos4 = state[i-3][j+3]

                if pos4 == pos3 == pos2 == pos1 and pos1 != 0:
                    return True

    # Down-right diagonal win
    for i in range(6):
        for j in range(7):
            if i <= 2 and j <= 3:
                pos1 = state[i][j]
                pos2 = state[i + 1][j + 1]
                pos3 = state[i + 2][j + 2]
                pos4 = state[i + 3][j + 3]

                if pos4 == pos3 == pos2 == pos1 and pos1 != 0:
                    return True

    if not valid_board(state):
        return True

    return False


def utility(state):
    # Horizontal win
    for i in range(6):
        last_player = 0
        count = 1
        for j in range(7):
            if state[i][j] == last_player and last_player != 0:
                count += 1
            elif state[i][j] != last_player:
                count = 1

            if count == 4:
                return last_player

            last_player = state[i][j]

    # Vertical win
    for i in range(7):
        last_player = 0
        count = 1
        for j in range(6):
            if state[j][i] == last_player and last_player != 0:
                count += 1
            elif state[j][i] != last_player:
                count = 1

            if count == 4:
                return last_player

            last_player = state[j][i]

    # Up-right diagonal win
    for i in range(6):
        for j in range(7):
            if i >= 3 and j <= 3:
                pos1 = state[i][j]
                pos2 = state[i - 1][j + 1]
                pos3 = state[i - 2][j + 2]
                pos4 = state[i - 3][j + 3]

                if pos4 == pos3 == pos2 == pos1 and pos1 != 0:
                    return pos1

    # Down-right diagonal win
    for i in range(6):
        for j in range(7):
            if i <= 2 and j <= 3:
                pos1 = state[i][j]
                pos2 = state[i + 1][j + 1]
                pos3 = state[i + 2][j + 2]
                pos4 = state[i + 3][j + 3]

                if pos4 == pos3 == pos2 == pos1 and pos1 != 0:
                    return pos1

    return 0



def win_next_turn(state, player):
    moves = ordered_actions(state)

    for i in moves:
        new_state = result(state, i, player)
        if utility(new_state) == player:
            return i

    return -1


def count_winning_moves(state, player):
    count = 0
    moves = ordered_actions(state)

    for i in moves:
        new_state = result(state, i, player)
        if utility(new_state) == player:
            count += 1

    return count



# Gives context to the bot for how good position is when depth is reached
def score_window(window):
    score = 0

    bot_count = window.count(1)
    player_count = window.count(-1)
    empty_count = window.count(0)

    if bot_count == 4:
        score += 100000

    elif bot_count == 3 and empty_count == 1:
        score += 100

    elif bot_count == 2 and empty_count == 2:
        score += 10

    if player_count == 3 and empty_count == 1:
        score -= 120

    elif player_count == 2 and empty_count == 2:
        score -= 10

    if player_count == 4:
        score -= 100000

    return score



def evaluate(state):
    score = 0

    # Center column is strong in Connect 4
    center_count = 0

    for row in range(ROWS):
        if state[row][3] == BOT:
            center_count += 1

    score += center_count * 8

    # Horizontal windows
    for row in range(ROWS):
        for col in range(COLS - 3):
            window = [
                state[row][col],
                state[row][col + 1],
                state[row][col + 2],
                state[row][col + 3]
            ]

            score += score_window(window)

    # Vertical windows
    for col in range(COLS):
        for row in range(ROWS - 3):
            window = [
                state[row][col],
                state[row + 1][col],
                state[row + 2][col],
                state[row + 3][col]
            ]

            score += score_window(window)

    # Down-right diagonal windows
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [
                state[row][col],
                state[row + 1][col + 1],
                state[row + 2][col + 2],
                state[row + 3][col + 3]
            ]

            score += score_window(window)

    # Up-right diagonal windows
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [
                state[row][col],
                state[row - 1][col + 1],
                state[row - 2][col + 2],
                state[row - 3][col + 3]
            ]

            score += score_window(window)

    return score


def negamax(state, depth, alpha, beta, player):
    # Base cases
    if is_terminal(state):
        return utility(state) * 100000 * player

    if depth == 0:
        return evaluate(state) * player

    max_eval = float('-inf')

    for i in ordered_actions(state):
        new_state = result(state, i, player)
        score = -negamax(new_state, depth - 1, -beta, -alpha, -player)
        max_eval = max(score, max_eval)
        alpha = max(alpha, score)

        if alpha >= beta:
            break

    return max_eval


def best_move(state):
    # If bot can win now, play that move
    bot_win = win_next_turn(state, BOT)

    if bot_win != -1:
        return bot_win

    # If player can win next turn, block it
    player_win = win_next_turn(state, PLAYER)

    if player_win != -1:
        return player_win

    best_score = float("-inf")
    move = None

    for col in ordered_actions(state):
        new_state = result(state, col, BOT)

        # Avoid moves that let the player make a fork
        if count_winning_moves(new_state, PLAYER) >= 2:
            score = -100000

        else:
            score = -negamax(new_state, 6, float("-inf"), float("inf"), PLAYER)

        # Like moves that create a bot fork
        if count_winning_moves(new_state, BOT) >= 2:
            score += 5000

        if score > best_score:
            best_score = score
            move = col

    return move

def get_clicked_column(mouse_x, board_x):
    col = (mouse_x - board_x) // CELL_SIZE
    return col


def draw_board(screen, state, message, current_turn):
    screen_width = screen.get_width()

    board_width = COLS * CELL_SIZE
    board_height = ROWS * CELL_SIZE

    board_x = (screen_width - board_width) // 2
    board_y = 100

    screen.fill((30, 30, 40))

    font = pygame.font.SysFont(None, 38)
    small_font = pygame.font.SysFont(None, 28)

    title = font.render(message, True, (255, 255, 255))
    screen.blit(title, (board_x, 35))

    help_text = small_font.render("Click a column to play. Press R to restart. Press ESC to exit.", True, (220, 220, 220))
    screen.blit(help_text, (board_x, 70))

    # Draw blue board background
    pygame.draw.rect(screen, (20, 80, 180), (board_x, board_y, board_width, board_height))

    # Draw circles
    for row in range(ROWS):
        for col in range(COLS):
            x = board_x + col * CELL_SIZE + CELL_SIZE // 2
            y = board_y + row * CELL_SIZE + CELL_SIZE // 2

            if state[row][col] == PLAYER:
                color = (230, 60, 60)

            elif state[row][col] == BOT:
                color = (240, 220, 60)

            else:
                color = (25, 25, 35)

            pygame.draw.circle(screen, color, (x, y), 32)

    return board_x, board_y, board_width, board_height


async def play_c4(screen):
    global state

    state = reset_board()

    running = True
    game_over = False
    current_turn = BOT
    message = "Bot goes first..."
    bot_wait = 20

    while running:
        board_x, board_y, board_width, board_height = draw_board(screen, state, message, current_turn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_r:
                    state = reset_board()
                    game_over = False
                    current_turn = BOT
                    message = "Bot goes first..."
                    bot_wait = 20

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                inside_x = board_x <= mouse_x <= board_x + board_width
                inside_y = board_y <= mouse_y <= board_y + board_height

                if inside_x and inside_y and current_turn == PLAYER:
                    col = get_clicked_column(mouse_x, board_x)

                    if valid_column(col, state):
                        state = result(state, col, PLAYER)

                        winner = utility(state)

                        if winner == PLAYER:
                            game_over = True
                            message = "You win! Press R to restart."

                        elif not valid_board(state):
                            game_over = True
                            message = "Draw! Press R to restart."

                        else:
                            current_turn = BOT
                            message = "Bot is thinking..."
                            bot_wait = 15

        # Bot move with a small delay
        if current_turn == BOT and not game_over:
            if bot_wait > 0:
                bot_wait -= 1

            else:
                bot_col = best_move(state)

                if bot_col != None:
                    state = result(state, bot_col, BOT)

                winner = utility(state)

                if winner == BOT:
                    game_over = True
                    message = "Bot wins! Press R to restart."

                elif not valid_board(state):
                    game_over = True
                    message = "Draw! Press R to restart."

                else:
                    current_turn = PLAYER
                    message = "Your turn"

        pygame.display.flip()
        await asyncio.sleep(0)