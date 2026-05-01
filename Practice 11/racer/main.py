import pygame
import sys
from pygame.locals import *
import random

# -------------------- INIT --------------------
pygame.init()

# background music
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)

# crash sound
crash_sound = pygame.mixer.Sound("crash.wav")

# FPS controller
FPS = 60
FramePerSec = pygame.time.Clock()

# -------------------- COLORS --------------------
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)

# -------------------- SCREEN --------------------
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# -------------------- GAME VARIABLES --------------------
SPEED = 5          # movement speed of all objects
SCORE = 0          # score for dodging enemies
COINS = 0          # collected coins
COINS_FOR_SPEED = 5  # every N coins → increase speed
game_over_state = False

# -------------------- FONTS --------------------
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
restart_font = pygame.font.SysFont("Verdana", 18)

game_over_text = font.render("Game Over", True, BLACK)

# -------------------- ASSETS --------------------
background = pygame.image.load("AnimatedStreet.png")

# -------------------- DISPLAY --------------------
DISPLAYSURF = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Racer Game")

# =========================================================
# ====================== CLASSES ===========================
# =========================================================

class Enemy(pygame.sprite.Sprite):
    """Enemy car that moves downward"""

    def __init__(self):
        super().__init__()

        # different enemy images
        self.enemy_images = [
            "Enemy.png",
            "mbappe.jpg",
            "messi.jpg"
        ]

        self.image = None
        self.rect = None
        self.reset()

    def reset(self):
        """Reset enemy position and image"""
        self.image = pygame.image.load(random.choice(self.enemy_images))
        self.image = pygame.transform.scale(self.image, (50, 90))

        self.rect = self.image.get_rect()
        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            random.randint(-200, -100)
        )

    def move(self):
        """Move enemy downward"""
        global SCORE

        self.rect.move_ip(0, SPEED)

        # if enemy leaves screen → increase score
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.reset()


class Player(pygame.sprite.Sprite):
    """Player controlled car"""

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("ronaldo.jpg")
        self.image = pygame.transform.scale(self.image, (50, 90))

        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def reset(self):
        """Reset player position"""
        self.rect.center = (160, 520)

    def move(self):
        """Handle player movement using keyboard"""
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):
    """Coin with different values (weights)"""

    def __init__(self):
        super().__init__()

        self.values = [1, 3, 5]  # possible coin values
        self.value = 1
        self.image = None
        self.rect = None

        self.reset_position()

    def reset_position(self):
        """Generate coin with random value and position"""

        # choose random value
        self.value = random.choice(self.values)

        # change color based on value
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)

        if self.value == 1:
            color = YELLOW
        elif self.value == 3:
            color = (0, 255, 0)  # green coin
        else:
            color = (255, 0, 255)  # purple coin

        pygame.draw.circle(self.image, color, (15, 15), 15)

        self.rect = self.image.get_rect()

        # avoid spawning on enemy
        while True:
            self.rect.center = (
                random.randint(50, SCREEN_WIDTH - 50),
                random.randint(-300, -100)
            )
            if not self.rect.colliderect(E1.rect):
                break

    def move(self):
        """Move coin downward"""
        self.rect.move_ip(0, SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()


# =========================================================
# ===================== GAME RESET =========================
# =========================================================

def reset_game():
    """Reset all game variables and positions"""
    global SCORE, COINS, SPEED, game_over_state

    SCORE = 0
    COINS = 0
    SPEED = 5
    game_over_state = False

    P1.reset()
    E1.reset()
    C1.reset_position()


# =========================================================
# ===================== OBJECTS ============================
# =========================================================

P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group(E1)
coins = pygame.sprite.Group(C1)
all_sprites = pygame.sprite.Group(P1, E1, C1)

# =========================================================
# ===================== EVENTS =============================
# =========================================================

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# =========================================================
# ===================== GAME LOOP ==========================
# =========================================================

while True:

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # restart game
        if event.type == KEYDOWN:
            if event.key == K_r and game_over_state:
                reset_game()

        # passive speed increase over time
        if event.type == INC_SPEED and not game_over_state:
            SPEED += 0.5

    # draw background
    DISPLAYSURF.blit(background, (0, 0))

    # draw score
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))

    # draw coins
    coin_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(coin_text, (270, 10))

    if not game_over_state:

        # update movement
        P1.move()
        E1.move()
        C1.move()

        # draw all objects
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)

        # enemy collision → game over
        if pygame.sprite.spritecollideany(P1, enemies):
            crash_sound.play()
            game_over_state = True

        # coin collision
        if pygame.sprite.spritecollideany(P1, coins):
            COINS += C1.value  # add coin value

            # increase speed every N coins
            if COINS % COINS_FOR_SPEED == 0:
                SPEED += 1

            C1.reset_position()

    else:
        # freeze game screen
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)

        # game over UI
        DISPLAYSURF.blit(game_over_text, (30, 230))

        restart_text = restart_font.render(
            "Press R to restart",
            True,
            WHITE
        )
        DISPLAYSURF.blit(restart_text, (110, 320))

    pygame.display.update()
    FramePerSec.tick(FPS)