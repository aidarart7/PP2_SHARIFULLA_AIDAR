import json
from datetime import datetime
from pathlib import Path

import pygame

from db import get_best_score, get_or_create_player, get_top10, save_game
from game import Game

BASE_DIR = Path(__file__).resolve().parent
SETTINGS_PATH = BASE_DIR / "settings.json"


def load_settings():
    defaults = {"grid": True, "sound": True, "snake_color": [255, 0, 0]}
    if SETTINGS_PATH.exists():
        with open(SETTINGS_PATH, encoding="utf-8") as f:
            data = json.load(f)
        for k, v in defaults.items():
            data.setdefault(k, v)
        return data
    return defaults.copy()


def write_settings(settings):
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)


pygame.init()
pygame.display.set_caption("Snake — TSIS 4")

screen = pygame.display.set_mode((600, 600))
font = pygame.font.SysFont("Verdana", 18)

settings = load_settings()

username = ""
player_id = None
menu_notice = ""

state = "menu"
game = None
leaderboard_rows = None


def draw_button(text, x, y, width=220, height=44):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, (212, 212, 212), rect)
    pygame.draw.rect(screen, (72, 72, 72), rect, 2)
    lbl = font.render(text, True, (0, 0, 0))
    screen.blit(
        lbl,
        (x + (width - lbl.get_width()) // 2, y + (height - lbl.get_height()) // 2),
    )
    return rect


def clamp_channel(value, delta):
    return max(0, min(255, value + delta))


def fmt_played_at(value):
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M")
    text = str(value)
    return text[:16] + ".." if len(text) > 16 else text


running = True
clock = pygame.time.Clock()

while running:
    screen.fill((20, 20, 26))

    if state == "menu":
        pygame.display.set_caption("Snake — TSIS 4 — Menu")

        prompt = font.render("Enter username, then Play:", True, (240, 240, 245))
        screen.blit(prompt, (130, 60))

        name_surface = font.render(username or "(empty)", True, (255, 220, 96))
        screen.blit(name_surface, (190, 100))

        if menu_notice:
            note = font.render(menu_notice, True, (255, 120, 120))
            screen.blit(note, (120, 130))

        play_btn = draw_button("Play", 190, 170)
        lead_btn = draw_button("Leaderboard", 190, 225)
        set_btn = draw_button("Settings", 190, 280)
        quit_btn = draw_button("Quit", 190, 335)

    elif state == "game":
        pygame.display.set_caption("Snake — TSIS 4 — Playing")

        game.update()
        game.draw(screen)

        if game.game_over:
            save_game(player_id, game.score, game.level)
            if player_id is not None:
                game.set_best_from_db(get_best_score(player_id))
            state = "gameover"

    elif state == "leaderboard":
        pygame.display.set_caption("Snake — TSIS 4 — Leaderboard")

        title = font.render("Top 10 scores", True, (255, 255, 255))
        screen.blit(title, (215, 40))

        hdr = font.render(
            f"{'#':>2}  {'User':22} {'Score':>6} {'Lv':>3}  Date",
            True,
            (200, 200, 210),
        )
        screen.blit(hdr, (40, 76))

        y = 110
        data = leaderboard_rows or []
        for i, row in enumerate(data[:10]):
            user, score, lvl, played = row
            line = (
                f"{i + 1:>2}.  "
                f"{str(user)[:18]:22} "
                f"{score:>6} {lvl:>3} "
                f" {fmt_played_at(played)}"
            )
            screen.blit(font.render(line, True, (238, 238, 244)), (40, y))
            y += 26

        if not data:
            screen.blit(
                font.render("No scores yet — play a round!", True, (170, 170, 176)),
                (120, y + 40),
            )

        back_btn = draw_button("Back", 190, 500)

    elif state == "settings":
        pygame.display.set_caption("Snake — TSIS 4 — Settings")

        screen.blit(font.render("Settings", True, (240, 240, 246)), (255, 24))

        grid_btn = draw_button(f"Grid: {'on' if settings['grid'] else 'off'}", 190, 70)
        sound_btn = draw_button(
            f"Sound: {'on' if settings['sound'] else 'off'}", 190, 125
        )

        col = tuple(settings["snake_color"])
        pygame.draw.rect(screen, col, (240, 192, 120, 60))
        screen.blit(
            font.render(f"Snake color RGB {col}", True, (230, 230, 238)),
            (168, 170),
        )

        rp = draw_button("R+", 118, 270, width=92, height=38)
        rm = draw_button("R-", 228, 270, width=92, height=38)
        gp = draw_button("G+", 338, 270, width=92, height=38)
        gm = draw_button("G-", 448, 270, width=92, height=38)
        bp = draw_button("B+", 118, 320, width=92, height=38)
        bm = draw_button("B-", 228, 320, width=92, height=38)

        reset_col = draw_button("Reset color", 338, 320, width=200, height=38)

        save_btn = draw_button("Save & Back", 190, 392)

    elif state == "gameover":
        pygame.display.set_caption("Snake — TSIS 4 — Game over")

        screen.blit(font.render("GAME OVER", True, (255, 86, 86)), (220, 80))

        best = getattr(game, "best_stored_on_start", 0) if game else 0

        ys = [
            ("Final score:", f"{game.score if game else 0}", (220, 200, 208)),
            ("Level reached:", f"{game.level if game else 0}", (220, 200, 208)),
            ("Personal best (DB):", f"{best}", (255, 230, 120)),
        ]
        yo = 150
        for label, val, color in ys:
            screen.blit(font.render(label, True, color), (80, yo))
            screen.blit(font.render(val, True, color), (360, yo))
            yo += 42

        retry_btn = draw_button("Retry", 190, 330)
        menu_btn = draw_button("Main menu", 190, 392)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "menu" and event.type == pygame.KEYDOWN:
            menu_notice = ""
            if event.key == pygame.K_BACKSPACE:
                username = username[:-1]
            elif event.unicode and len(username) < 48:
                if event.unicode.isprintable():
                    username += event.unicode

        if state == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            menu_notice = ""

            if play_btn.collidepoint(event.pos):
                pid = get_or_create_player(username)
                if pid is None:
                    menu_notice = "Please enter a non-empty username before Play."
                else:
                    player_id = pid
                    game = Game(settings, player_id)
                    state = "game"

            elif lead_btn.collidepoint(event.pos):
                leaderboard_rows = get_top10()
                state = "leaderboard"

            elif set_btn.collidepoint(event.pos):
                state = "settings"

            elif quit_btn.collidepoint(event.pos):
                running = False

        elif state == "leaderboard":
            if event.type == pygame.MOUSEBUTTONDOWN and back_btn.collidepoint(event.pos):
                state = "menu"

        elif state == "settings" and event.type == pygame.MOUSEBUTTONDOWN:
            c = settings["snake_color"]
            if grid_btn.collidepoint(event.pos):
                settings["grid"] = not settings["grid"]
            elif sound_btn.collidepoint(event.pos):
                settings["sound"] = not settings["sound"]
            elif rp.collidepoint(event.pos):
                c[0] = clamp_channel(c[0], +20)
            elif rm.collidepoint(event.pos):
                c[0] = clamp_channel(c[0], -20)
            elif gp.collidepoint(event.pos):
                c[1] = clamp_channel(c[1], +20)
            elif gm.collidepoint(event.pos):
                c[1] = clamp_channel(c[1], -20)
            elif bp.collidepoint(event.pos):
                c[2] = clamp_channel(c[2], +20)
            elif bm.collidepoint(event.pos):
                c[2] = clamp_channel(c[2], -20)
            elif reset_col.collidepoint(event.pos):
                settings["snake_color"] = [255, 0, 0]
            elif save_btn.collidepoint(event.pos):
                write_settings(settings)
                state = "menu"

        elif state == "gameover" and event.type == pygame.MOUSEBUTTONDOWN:
            if retry_btn.collidepoint(event.pos) and game is not None:
                game.reset()
                state = "game"
            elif menu_btn.collidepoint(event.pos):
                state = "menu"

        elif state == "game" and event.type == pygame.KEYDOWN:
            game.handle_keydown(event.key)

    pygame.display.flip()

    if state == "game" and game is not None:
        clock.tick(game.FPS)
    else:
        clock.tick(60)

pygame.quit()
