import pygame
import asyncio
import sys

# The current state of the board
state = [' ' for i in range(9)]

WIDTH, HEIGHT = 800, 600
BOARD_SIZE = 480
CELL_SIZE = BOARD_SIZE // 3
BOARD_X = (WIDTH - BOARD_SIZE) // 2
BOARD_Y = (HEIGHT - BOARD_SIZE) // 2


# Draws the tic-tac-toe grid
def draw_grid(screen):
    # Draw 2 vertical lines
    for i in range(1, 3):
        x = BOARD_X + i * CELL_SIZE
        pygame.draw.line(screen, (255, 255, 255), (x, BOARD_Y), (x, BOARD_Y + BOARD_SIZE), 5)

    # Draw 2 horizontal lines
    for i in range(1, 3):
        y = BOARD_Y + i * CELL_SIZE
        pygame.draw.line(screen, (255, 255, 255), (BOARD_X, y), (BOARD_X + BOARD_SIZE, y), 5)


# Makes cells inside each square
def make_cells():
    cells = []

    for i in range(3):
        for j in range(3):
            x = BOARD_X + j * CELL_SIZE
            y = BOARD_Y + i * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            cells.append(rect)

    return cells

def draw_o(screen, rect, color, width):
    center = rect.center
    radius = rect.width // 3
    pygame.draw.circle(screen, color, center, radius, width)


def draw_x(screen, rect, color, width):
    padding = rect.width // 4

    pygame.draw.line(
        screen,
        color,
        (rect.left + padding, rect.top + padding),
        (rect.right - padding, rect.bottom - padding),
        width
    )

    pygame.draw.line(
        screen,
        color,
        (rect.right - padding, rect.top + padding),
        (rect.left + padding, rect.bottom - padding),
        width
    )



# Returns if the game has ended
def is_terminal(state):
    # These are all the winning combos
    WINNING_COMBOS = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]

    for i in WINNING_COMBOS:
        if state[i[0]] == state[i[1]] == state[i[2]] and state[i[1]] != ' ':
            return True

    if ' ' not in state:
        return True

    return False


# Checks who won. Returns 1(won), 0(tie), -1(loss)
def utility(state):
    WINNING_COMBOS = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]

    for i in WINNING_COMBOS:
        if state[i[0]] == state[i[1]] == state[i[2]] and state[i[1]] != ' ':
            if state[i[0]] == 'X':
                return 1
            elif state[i[0]] == 'O':
                return -1

    return 0


# Returns all legal moves
def actions(state):
    legal = []
    for i in range(len(state)):
        if state[i] == ' ':
            legal.append(i)

    return legal


# Returns the result of a hypothetical move
def result(state, action, player):
    new_board = state.copy()
    if new_board[action] == ' ':
        new_board[action] = player
    return new_board



def minmax(state, depth, alpha, beta, maximizing_player):
    if is_terminal(state) or depth == 0:
        return utility(state)

    # The bot, or 'X'
    if maximizing_player:
        max_eval = float("-inf")

        # Loops through all the possible actions
        for i in actions(state):
            new_state = result(state, i, 'X')

            # Next turn
            eval = minmax(new_state, depth-1, alpha, beta, False)
            max_eval = max(eval, max_eval)
            alpha = max(alpha, eval)

            # Stop checking this branch because it cannot give a better score then another move that's checked
            if beta <= alpha:
                break

        return max_eval

    # The minimizing player, 'O', or the player
    else:
        min_eval = float("inf")

        # Loops through all the possible actions
        for i in actions(state):
            new_state = result(state, i, 'O')

            # Next turn
            eval = minmax(new_state, depth - 1, alpha, beta, True)
            min_eval = min(eval, min_eval)
            beta = min(beta, eval)

            if beta <= alpha:
                break

        return min_eval


# Finds the best move
def best_move(state):
    best_score = float("-inf")
    move = None

    for i in actions(state):
        new_state = result(state, i, 'X')
        score = minmax(new_state, 9, float("-inf"), float("inf"), False)

        if score > best_score:
            best_score = score
            move = i

    return move

# Runs the GUI
async def play_ttt(screen):
    global state

    font = pygame.font.SysFont(None, 40)
    big_font = pygame.font.SysFont(None, 90)
    button_font = pygame.font.SysFont(None, 45)
    restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 60)

    cells = make_cells()
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        hover_index = None

        # Find which empty square the mouse is hovering over
        for i in range(len(cells)):
            if cells[i].collidepoint(mouse_pos) and state[i] == ' ':
                hover_index = i

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # Restart button click
                if is_terminal(state) and restart_button.collidepoint(event.pos):
                    state = [' ' for i in range(9)]

                    bot_move = best_move(state)
                    if bot_move is not None:
                        state[bot_move] = 'X'

                    continue

                # Normal board click
                if not is_terminal(state):
                    for i in range(len(cells)):
                        if cells[i].collidepoint(event.pos) and state[i] == ' ':
                            state[i] = 'O'

                            if not is_terminal(state):
                                bot_move = best_move(state)
                                if bot_move is not None:
                                    state[bot_move] = 'X'

                for i in range(len(cells)):
                    if cells[i].collidepoint(event.pos) and state[i] == ' ' and not is_terminal(state):
                        # Player places O
                        state[i] = 'O'

                        # If the game is over and restart button is clicked
                        if is_terminal(state) and restart_button.collidepoint(event.pos):
                            state = [' ' for i in range(9)]

                            # Bot starts again
                            bot_move = best_move(state)
                            if bot_move is not None:
                                state[bot_move] = 'X'

                        # Bot places X after player, if game is not over
                        if not is_terminal(state):
                            bot_move = best_move(state)
                            if bot_move is not None:
                                state[bot_move] = 'X'

        screen.fill((20, 30, 40))
        draw_grid(screen)

        X_COLOR = (255, 80, 80)
        O_COLOR = (80, 180, 255)
        HOVER_COLOR = (30, 130, 205)

        # Draw Xs and Os
        for i in range(9):
            if state[i] == 'O':
                draw_o(screen, cells[i], O_COLOR, 8)

            elif state[i] == 'X':
                draw_x(screen, cells[i], X_COLOR, 8)

            elif i == hover_index:
                # Faint O when hovering
                draw_o(screen, cells[i], HOVER_COLOR, 5)

            if is_terminal(state):
                result_after = utility(state)

                if result_after == 0:
                    text_ttt = big_font.render("Tie", True, (255, 215, 0))
                elif result_after == 1:
                    text_ttt = big_font.render("You Lost!", True, (255, 0, 0))
                elif result_after == -1:
                    text_ttt = big_font.render("You Won!", True, (0, 255, 0))

                # Text position
                text_rect = text_ttt.get_rect(center=(WIDTH // 2, HEIGHT // 2))

                # Rectangle behind text
                box_rect = text_rect.inflate(60, 40)
                pygame.draw.rect(screen, (0, 0, 0), box_rect)

                # Draw game over text
                screen.blit(text_ttt, text_rect)

                # Restart button
                pygame.draw.rect(screen, (255, 255, 255), restart_button)
                pygame.draw.rect(screen, (0, 0, 0), restart_button, 4)

                restart_text = button_font.render("Restart", True, (0, 0, 0))
                restart_text_rect = restart_text.get_rect(center=restart_button.center)
                screen.blit(restart_text, restart_text_rect)

        pygame.display.flip()
        await asyncio.sleep(0)