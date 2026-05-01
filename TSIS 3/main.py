import pygame
import sys
import os
from persistence import load_settings, save_settings, load_leaderboard, save_score
from ui import Button, TextInput
from racer import Player, Enemy, Obstacle, PowerUp

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3 Racer")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

settings = load_settings()

# ---------- SOUND ----------
pygame.mixer.music.load(os.path.join('assets','sounds','background.wav'))
pygame.mixer.music.play(-1)

# ---------- BACKGROUND ----------
bg = pygame.image.load(os.path.join('assets','images','AnimatedStreet.png'))
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
bg_y = 0

# ---------- STATE ----------
state = "MENU"
player_name = "Player"
score = 0
distance = 0

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = None

# ---------- EVENTS ----------
SPAWN_ENEMY = pygame.USEREVENT + 1
SPAWN_OBSTACLE = pygame.USEREVENT + 2
SPAWN_POWERUP = pygame.USEREVENT + 3

def apply_difficulty():
    if settings["difficulty"] == "easy":
        pygame.time.set_timer(SPAWN_ENEMY, 1600)
        pygame.time.set_timer(SPAWN_OBSTACLE, 2600)
        pygame.time.set_timer(SPAWN_POWERUP, 3000)

    elif settings["difficulty"] == "normal":
        pygame.time.set_timer(SPAWN_ENEMY, 1200)
        pygame.time.set_timer(SPAWN_OBSTACLE, 2000)
        pygame.time.set_timer(SPAWN_POWERUP, 2500)

    elif settings["difficulty"] == "hard":
        pygame.time.set_timer(SPAWN_ENEMY, 700)
        pygame.time.set_timer(SPAWN_OBSTACLE, 1200)
        pygame.time.set_timer(SPAWN_POWERUP, 2000)

apply_difficulty()

# ---------- GAME ----------
def reset_game():
    global player, score, distance
    all_sprites.empty()
    enemies.empty()
    obstacles.empty()
    powerups.empty()

    player = Player(settings["car_color"])
    all_sprites.add(player)

    score = 0
    distance = 0

def draw_hud():
    screen.blit(font.render(f"Score: {int(score)}", True, (255,255,255)), (10,10))
    screen.blit(font.render(f"Dist: {int(distance)}", True, (255,255,255)), (10,40))

    if player.nitro_active:
        t = (player.powerup_timer - pygame.time.get_ticks())//1000
        screen.blit(font.render(f"NITRO {max(0,t)}s", True, (0,255,255)), (10,80))

    elif player.shield_active:
        screen.blit(font.render("SHIELD", True, (255,255,0)), (10,80))

    elif player.crashes_allowed > 0:
        screen.blit(font.render("REPAIR", True, (255,0,255)), (10,80))

# ---------- UI ----------
btn_play = Button(200,150,200,50,"Play")
btn_settings = Button(200,220,200,50,"Settings")
btn_board = Button(200,290,200,50,"Leaderboard")
btn_quit = Button(200,360,200,50,"Quit")

btn_easy = Button(200,150,200,50,"Easy")
btn_normal = Button(200,220,200,50,"Normal")
btn_hard = Button(200,290,200,50,"Hard")
btn_back = Button(200,500,200,50,"Back")

btn_retry = Button(200,350,200,50,"Retry")
btn_menu = Button(200,420,200,50,"Menu")

name_input = TextInput(200,250,200,40)

# ---------- LOOP ----------
running = True
while running:

    bg_y += 6
    if bg_y >= HEIGHT:
        bg_y = 0

    screen.blit(bg, (0, bg_y))
    screen.blit(bg, (0, bg_y - HEIGHT))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ---------- MENU ----------
        if state == "MENU":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_play.rect.collidepoint(event.pos): state = "NAME"
                elif btn_settings.rect.collidepoint(event.pos): state = "SETTINGS"
                elif btn_board.rect.collidepoint(event.pos): state = "BOARD"
                elif btn_quit.rect.collidepoint(event.pos): running = False

        # ---------- SETTINGS ----------
        elif state == "SETTINGS":
            if event.type == pygame.MOUSEBUTTONDOWN:

                if btn_easy.rect.collidepoint(event.pos):
                    settings["difficulty"] = "easy"
                    save_settings(settings)
                    apply_difficulty()
                    reset_game()

                elif btn_normal.rect.collidepoint(event.pos):
                    settings["difficulty"] = "normal"
                    save_settings(settings)
                    apply_difficulty()
                    reset_game()

                elif btn_hard.rect.collidepoint(event.pos):
                    settings["difficulty"] = "hard"
                    save_settings(settings)
                    apply_difficulty()
                    reset_game()

                elif btn_back.rect.collidepoint(event.pos):
                    state = "MENU"

        # ---------- NAME ----------
        elif state == "NAME":
            name_input.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                player_name = name_input.text or "Player"
                reset_game()
                state = "PLAY"

        # ---------- PLAY ----------
        elif state == "PLAY":

            if event.type == SPAWN_ENEMY:
                e = Enemy(settings["difficulty"])
                all_sprites.add(e)
                enemies.add(e)

            if event.type == SPAWN_OBSTACLE:
                o = Obstacle()
                all_sprites.add(o)
                obstacles.add(o)

            if event.type == SPAWN_POWERUP:
                p = PowerUp()
                all_sprites.add(p)
                powerups.add(p)

        # ---------- BOARD ----------
        elif state == "BOARD":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.rect.collidepoint(event.pos):
                    state = "MENU"

        # ---------- GAME OVER ----------
        elif state == "GAMEOVER":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retry.rect.collidepoint(event.pos):
                    reset_game()
                    state = "PLAY"
                elif btn_menu.rect.collidepoint(event.pos):
                    state = "MENU"

    # ---------- GAME ----------
    if state == "PLAY":
        all_sprites.update()

        distance += 0.2
        score += 0.3

        hit_enemy = pygame.sprite.spritecollideany(player, enemies)
        hit_obstacle = pygame.sprite.spritecollideany(player, obstacles)

        if hit_enemy or hit_obstacle:

            if player.shield_active:
                player.shield_active = False
                if hit_enemy: hit_enemy.kill()
                if hit_obstacle: hit_obstacle.kill()

            elif player.crashes_allowed > 0:
                player.crashes_allowed -= 1
                if hit_enemy: hit_enemy.kill()
                if hit_obstacle: hit_obstacle.kill()

            else:
                save_score(player_name, int(score), int(distance))
                state = "GAMEOVER"

        hits = pygame.sprite.spritecollide(player, powerups, True)
        for h in hits:

            if player.nitro_active or player.shield_active:
                continue

            if h.type == "Nitro":
                player.nitro_active = True
                player.powerup_timer = pygame.time.get_ticks() + 4000

            elif h.type == "Shield":
                player.shield_active = True
                player.powerup_timer = pygame.time.get_ticks() + 4000

            elif h.type == "Repair":
                player.crashes_allowed = 1

        all_sprites.draw(screen)
        draw_hud()

    elif state == "MENU":
        btn_play.draw(screen)
        btn_settings.draw(screen)
        btn_board.draw(screen)
        btn_quit.draw(screen)

    elif state == "SETTINGS":
        screen.fill((40,40,40))
        btn_easy.draw(screen)
        btn_normal.draw(screen)
        btn_hard.draw(screen)
        btn_back.draw(screen)

    elif state == "NAME":
        screen.blit(font.render("Enter Name:", True,(255,255,255)), (200,200))
        name_input.draw(screen)

    elif state == "BOARD":
        screen.fill((30,30,30))
        board = load_leaderboard()
        for i,e in enumerate(board):
            txt = f"{i+1}. {e['name']} {e['score']} {e['distance']}"
            screen.blit(font.render(txt,True,(255,255,255)), (120,60+i*30))
        btn_back.draw(screen)

    elif state == "GAMEOVER":
        screen.fill((0,0,0))
        screen.blit(font.render("GAME OVER",True,(255,0,0)), (220,200))
        btn_retry.draw(screen)
        btn_menu.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()