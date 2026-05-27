import pygame
import asyncio
import sys


# Example imports from your other files
# Ensure these files have async functions defined inside them!
# from tictactoe import play_ttt
# from connect4 import play_c4

# Placeholder async game loops for demonstration purposes
async def play_ttt(screen):
    print("Starting Tic Tac Toe...")
    font = pygame.font.SysFont(None, 40)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # Return to main menu

        screen.fill((20, 30, 40))
        text = font.render("Tic Tac Toe Running! Press ESC to Exit", True, (255, 255, 255))
        screen.blit(text, (50, 250))

        pygame.display.flip()
        await asyncio.sleep(0)


async def play_c4(screen):
    print("Starting Connect 4...")
    font = pygame.font.SysFont(None, 40)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # Return to main menu

        screen.fill((40, 20, 30))
        text = font.render("Connect 4 Running! Press ESC to Exit", True, (255, 255, 255))
        screen.blit(text, (50, 250))

        pygame.display.flip()
        await asyncio.sleep(0)


async def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Launcher")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 50)

    # Define the two halves of the screen
    left_rect = pygame.Rect(0, 0, WIDTH // 2, HEIGHT)
    right_rect = pygame.Rect(WIDTH // 2, 0, WIDTH // 2, HEIGHT)

    # Color definitions (Normal and Hover states)
    COLOR_TTT = (52, 152, 219)  # Soft Blue
    COLOR_TTT_HOVER = (41, 128, 185)
    COLOR_C4 = (231, 76, 60)  # Soft Red
    COLOR_C4_HOVER = (192, 57, 43)

    running = True
    while running:
        # 1. Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # 2. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if Left Side (Tic Tac Toe) was clicked
                if left_rect.collidepoint(mouse_pos):
                    await play_ttt(screen)

                # Check if Right Side (Connect 4) was clicked
                elif right_rect.collidepoint(mouse_pos):
                    await play_c4(screen)

        # 3. Drawing Layout & Hover Logic
        # Left Side
        if left_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, COLOR_TTT_HOVER, left_rect)
        else:
            pygame.draw.rect(screen, COLOR_TTT, left_rect)

        # Right Side
        if right_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, COLOR_C4_HOVER, right_rect)
        else:
            pygame.draw.rect(screen, COLOR_C4, right_rect)

        # 4. Drawing Text labels
        text_ttt = font.render("Tic Tac Toe", True, (255, 255, 255))
        text_c4 = font.render("Connect 4", True, (255, 255, 255))

        # Center text inside their respective halves
        screen.blit(text_ttt,
                    (left_rect.centerx - text_ttt.get_width() // 2, left_rect.centery - text_ttt.get_height() // 2))
        screen.blit(text_c4,
                    (right_rect.centerx - text_c4.get_width() // 2, right_rect.centery - text_c4.get_height() // 2))

        # Draw a thin black dividing line down the middle
        pygame.draw.line(screen, (0, 0, 0), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 4)

        pygame.display.flip()

        # Gives control back to the browser / limits FPS
        await asyncio.sleep(0)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())