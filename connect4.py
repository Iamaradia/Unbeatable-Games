import pygame
import asyncio
import sys

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
