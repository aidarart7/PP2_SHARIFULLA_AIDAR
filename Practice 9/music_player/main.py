import pygame
import sys
from player import MusicPlayer


def main():
    pygame.init()

    screen = pygame.display.set_mode((600, 300))
    pygame.display.set_caption("Music Player")

    player = MusicPlayer()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()

                elif event.key == pygame.K_s:
                    player.stop()

                elif event.key == pygame.K_n:
                    player.next()

                elif event.key == pygame.K_b:
                    player.prev()

                elif event.key == pygame.K_q:
                    running = False

        player.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()