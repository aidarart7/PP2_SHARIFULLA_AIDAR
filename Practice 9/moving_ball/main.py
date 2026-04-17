import pygame
import sys
from ball import Ball

def main():
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball Game")

    clock = pygame.time.Clock()

    # создаем шар в центре
    ball = Ball(WIDTH // 2, HEIGHT // 2, 25, WIDTH, HEIGHT)

    running = True
    while running:
        screen.fill((255, 255, 255))  # белый фон

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move(0, -ball.speed)
                elif event.key == pygame.K_DOWN:
                    ball.move(0, ball.speed)
                elif event.key == pygame.K_LEFT:
                    ball.move(-ball.speed, 0)
                elif event.key == pygame.K_RIGHT:
                    ball.move(ball.speed, 0)

        ball.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()