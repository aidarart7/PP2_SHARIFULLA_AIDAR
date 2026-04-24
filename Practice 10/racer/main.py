import pygame
import sys
from pygame.locals import *
import random

# Initializing pygame
pygame.init()

# background music
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)  # infinite loop

# crash sound
crash_sound = pygame.mixer.Sound("crash.wav")

# FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)

# Screen settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Game values
SPEED = 5
SCORE = 0
COINS = 0
game_over_state = False

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
restart_font = pygame.font.SysFont("Verdana", 18)

game_over_text = font.render("Game Over", True, BLACK)

# Images
background = pygame.image.load("AnimatedStreet.png")

# Main screen
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.enemy_images = [
            "Enemy.png",
            "mbappe.jpg",
            "messi.jpg"
            
        ]

        self.image = None
        self.rect = None
        self.reset()

    def reset(self):
        self.image = pygame.image.load(random.choice(self.enemy_images))
        self.image = pygame.transform.scale(self.image, (50, 90))

        self.rect = self.image.get_rect()
        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            random.randint(-200, -100)
        )

    def move(self):
        global SCORE

        self.rect.move_ip(0, SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.reset()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("ronaldo.jpg")
        self.image = pygame.transform.scale(self.image, (50, 90))

        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def reset(self):
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (15, 15), 15)

        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        while True:
            self.rect.center = (
                random.randint(50, SCREEN_WIDTH - 50),
                random.randint(-300, -100)
            )

            if not self.rect.colliderect(E1.rect):
                break

    def move(self):
        self.rect.move_ip(0, SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()


def reset_game():
    global SCORE, COINS, SPEED, game_over_state

    SCORE = 0
    COINS = 0
    SPEED = 5
    game_over_state = False

    P1.reset()
    E1.reset()
    C1.reset_position()


# Creating sprites
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Speed increase event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game Loop
while True:

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # restart game with R
        if event.type == KEYDOWN:
            if event.key == K_r and game_over_state:
                reset_game()

        if event.type == INC_SPEED and not game_over_state:
            SPEED += 0.5

    DISPLAYSURF.blit(background, (0, 0))

    # score
    score_text = font_small.render(
        "Score: " + str(SCORE),
        True,
        BLACK
    )
    DISPLAYSURF.blit(score_text, (10, 10))

    # coins
    coin_text = font_small.render(
        "Coins: " + str(COINS),
        True,
        BLACK
    )
    DISPLAYSURF.blit(coin_text, (270, 10))

    if not game_over_state:
        # normal game
        P1.move()
        E1.move()
        C1.move()

        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)

        # enemy collision
        if pygame.sprite.spritecollideany(P1, enemies):
            crash_sound.play()
            game_over_state = True

        # coin collision
        if pygame.sprite.spritecollideany(P1, coins):
            COINS += 1
            C1.reset_position()

    else:
        # freeze scene
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)

        # game over text
        DISPLAYSURF.blit(game_over_text, (30, 230))

        restart_text = restart_font.render(
            "Press R to restart",
            True,
            WHITE
        )
        DISPLAYSURF.blit(restart_text, (110, 320))

    pygame.display.update()
    FramePerSec.tick(FPS)