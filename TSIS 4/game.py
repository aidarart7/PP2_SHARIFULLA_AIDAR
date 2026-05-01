import pygame
import random
import sys
from collections import deque

from db import get_best_score

WIDTH = 600
HEIGHT = 600
CELL = 30

COLORS_GREEN = (0, 255, 0)
COLORS_YELLOW = (255, 255, 0)
COLORS_PURPLE = (200, 0, 200)
FOOD_VALUES = (1, 2, 3)
FOOD_LIFETIME_MS = 5000


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Game:
    def __init__(self, settings, player_id):
        self.settings = settings
        self.player_id = player_id
        self.reset()

    def reset(self):
        self.snake = [
            Point(10, 10),
            Point(9, 10),
            Point(8, 10),
        ]

        self.dx = 1
        self.dy = 0

        self.score = 0
        self.level = 1
        self.FPS = 5
        self.base_FPS = 5

        self.game_over = False

        self.obstacles = []

        self.food_point = None
        self.food_value = 1
        self.food_spawn_time = pygame.time.get_ticks()

        self.poison = None
        self.poison_spawn_time = 0

        self.power_cell = None
        self.power_field_kind = None
        self.power_spawn_time = 0

        self.speed_effect_until = 0
        self.shield_armed = False

        self.best_stored_on_start = get_best_score(self.player_id)

        self.spawn_fresh_food()

    def set_best_from_db(self, value):
        self.best_stored_on_start = max(self.best_stored_on_start, value or 0)

    # ---------------- HELPERS ----------------
    def obstacle_set(self):
        return {(x, y) for x, y in self.obstacles}

    def random_free_point(self, forbid=None):
        forbid = forbid or ()
        forbid_set = set(forbid)

        while True:
            x = random.randint(0, WIDTH // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)

            ok = True
            for p in self.snake:
                if p.x == x and p.y == y:
                    ok = False

            if (x, y) in self.obstacle_set() or (x, y) in forbid_set:
                ok = False

            if ok:
                return Point(x, y)

    def snake_head(self):
        return self.snake[0]

    def obstacles_fully_connected(self, obs_blocks):
        """Ensure every non-obstacle cell is reachable from the head (orthogonal)."""
        h = self.snake_head()
        obs_set = set(obs_blocks)
        if (h.x, h.y) in obs_set:
            return False

        playable = []
        for x in range(WIDTH // CELL):
            for y in range(HEIGHT // CELL):
                if (x, y) not in obs_set:
                    playable.append((x, y))

        if not playable:
            return False

        start = (h.x, h.y)
        if start not in playable:
            return False

        q = deque([start])
        seen = {start}
        while q:
            cx, cy = q.popleft()
            for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                n = (nx, ny)
                if n in playable and n not in seen:
                    seen.add(n)
                    q.append(n)

        return len(seen) == len(playable)

    def spawn_fresh_food(self):
        extra = []
        if self.power_cell:
            extra.append((self.power_cell.x, self.power_cell.y))
        if self.poison:
            extra.append((self.poison.x, self.poison.y))
        pt = self.random_free_point(tuple(extra))
        self.food_point = pt
        self.food_value = random.choice(FOOD_VALUES)
        self.food_spawn_time = pygame.time.get_ticks()

    def spawn_poison_cell(self):
        extra = []
        if self.food_point:
            extra.append((self.food_point.x, self.food_point.y))
        if self.power_cell:
            extra.append((self.power_cell.x, self.power_cell.y))
        self.poison = self.random_free_point(tuple(extra))
        self.poison_spawn_time = pygame.time.get_ticks()

    def spawn_power_cell(self):
        extra = []
        if self.food_point:
            extra.append((self.food_point.x, self.food_point.y))
        if self.poison:
            extra.append((self.poison.x, self.poison.y))
        self.power_cell = self.random_free_point(tuple(extra))
        self.power_field_kind = random.choice(["speed", "slow", "shield"])
        self.power_spawn_time = pygame.time.get_ticks()

    def apply_speed_pickup_kind(self, kind):
        now = pygame.time.get_ticks()
        self.speed_effect_until = now + 5000
        if kind == "speed":
            self.FPS = self.base_FPS + 5
        elif kind == "slow":
            self.FPS = max(2, self.base_FPS - 3)

    def clear_speed_effect_if_expired(self):
        now = pygame.time.get_ticks()
        if self.speed_effect_until and now >= self.speed_effect_until:
            self.FPS = self.base_FPS
            self.speed_effect_until = 0

    # ---------------- INPUT ----------------
    def handle_keydown(self, key):
        if self.game_over:
            return

        if key == pygame.K_RIGHT and self.dx != -1:
            self.dx, self.dy = 1, 0
        elif key == pygame.K_LEFT and self.dx != 1:
            self.dx, self.dy = -1, 0
        elif key == pygame.K_DOWN and self.dy != -1:
            self.dx, self.dy = 0, 1
        elif key == pygame.K_UP and self.dy != 1:
            self.dx, self.dy = 0, -1

    # ---------------- AUDIO (optional) ----------------
    def maybe_play_pickup_sound(self):
        if not self.settings.get("sound", True):
            return
        if sys.platform != "win32":
            return
        try:
            import winsound

            winsound.Beep(740, 30)
        except Exception:
            pass

    # ---------------- UPDATE ----------------
    def update(self):
        if self.game_over:
            return

        self.clear_speed_effect_if_expired()

        now = pygame.time.get_ticks()

        # Timed foods (Practice 11)
        if now - self.food_spawn_time > FOOD_LIFETIME_MS:
            self.spawn_fresh_food()

        if self.poison and now - self.poison_spawn_time > 8000:
            self.poison = None

        if self.power_cell and now - self.power_spawn_time > 8000:
            self.power_cell = None
            self.power_field_kind = None

        if self.poison is None and random.random() < 0.01:
            self.spawn_poison_cell()

        if self.power_cell is None and random.random() < 0.01:
            self.spawn_power_cell()

        h = self.snake_head()
        nh_x = h.x + self.dx
        nh_y = h.y + self.dy

        for ox, oy in self.obstacles:
            if nh_x == ox and nh_y == oy:
                self.game_over = True
                return

        oob = (
            nh_x < 0
            or nh_x >= WIDTH // CELL
            or nh_y < 0
            or nh_y >= HEIGHT // CELL
        )
        if oob:
            if self.shield_armed:
                self.shield_armed = False
                return
            self.game_over = True
            return

        occupied = {(p.x, p.y) for p in self.snake[:-1]}
        hits_self = (nh_x, nh_y) in occupied
        if hits_self:
            if self.shield_armed:
                self.shield_armed = False
                return
            self.game_over = True
            return

        # Safe move — body follows, head enters (nh_x, nh_y)
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i].x = self.snake[i - 1].x
            self.snake[i].y = self.snake[i - 1].y
        head = self.snake_head()
        head.x = nh_x
        head.y = nh_y

        # Normal food
        if (
            self.food_point
            and head.x == self.food_point.x
            and head.y == self.food_point.y
        ):
            self.score += self.food_value
            self.maybe_play_pickup_sound()
            self.snake.append(Point(self.snake[-1].x, self.snake[-1].y))
            self.spawn_fresh_food()

            if self.score % 5 == 0 and self.score > 0:
                self.level += 1
                self.base_FPS += 1
                self.FPS = self.base_FPS
                self.speed_effect_until = 0
                if self.level >= 3:
                    self.generate_obstacles_safe()

        if self.poison and head.x == self.poison.x and head.y == self.poison.y:
            self.poison = None
            self.snake = self.snake[:-2]
            if len(self.snake) <= 1:
                self.game_over = True

        head = self.snake_head()
        if (
            self.power_cell
            and self.power_field_kind
            and head.x == self.power_cell.x
            and head.y == self.power_cell.y
        ):
            kind = self.power_field_kind
            self.power_cell = None
            self.power_field_kind = None
            if kind == "shield":
                self.shield_armed = True
                self.maybe_play_pickup_sound()
            else:
                self.apply_speed_pickup_kind(kind)
                self.maybe_play_pickup_sound()

    # ---------------- DRAW ----------------
    def draw(self, screen):
        screen.fill((0, 0, 0))

        if self.settings.get("grid", True):
            for i in range(WIDTH // CELL):
                for j in range(HEIGHT // CELL):
                    pygame.draw.rect(
                        screen,
                        (50, 50, 50),
                        (i * CELL, j * CELL, CELL, CELL),
                        1,
                    )

        color = tuple(self.settings.get("snake_color", [255, 0, 0]))
        for p in self.snake:
            pygame.draw.rect(
                screen, color, (p.x * CELL, p.y * CELL, CELL, CELL)
            )

        if self.food_point:
            if self.food_value == 1:
                fc = COLORS_GREEN
            elif self.food_value == 2:
                fc = COLORS_YELLOW
            else:
                fc = COLORS_PURPLE
            pygame.draw.rect(
                screen,
                fc,
                (
                    self.food_point.x * CELL,
                    self.food_point.y * CELL,
                    CELL,
                    CELL,
                ),
            )

        if self.poison:
            pygame.draw.rect(
                screen,
                (139, 0, 0),
                (self.poison.x * CELL, self.poison.y * CELL, CELL, CELL),
            )

        if self.power_cell and self.power_field_kind:
            if self.power_field_kind == "shield":
                pc = (0, 200, 255)
            elif self.power_field_kind == "speed":
                pc = (255, 215, 0)
            else:
                pc = (150, 70, 255)
            pygame.draw.rect(
                screen,
                pc,
                (self.power_cell.x * CELL, self.power_cell.y * CELL, CELL, CELL),
            )

        for ox, oy in self.obstacles:
            pygame.draw.rect(
                screen,
                (100, 100, 100),
                (ox * CELL, oy * CELL, CELL, CELL),
            )

        font = pygame.font.SysFont("Verdana", 20)
        screen.blit(
            font.render(f"Score: {self.score}", True, (255, 255, 255)),
            (10, 10),
        )
        shield_lbl = "Shield: ready" if self.shield_armed else "Shield: none"
        screen.blit(
            font.render(shield_lbl, True, (200, 200, 200)),
            (175, 10),
        )
        screen.blit(
            font.render(f"Level: {self.level}", True, (255, 255, 255)),
            (420, 10),
        )

        pb = getattr(self, "best_stored_on_start", 0)
        screen.blit(
            font.render(f"Best: {pb}", True, (255, 255, 0)),
            (10, 36),
        )

    # ---------------- OBSTACES ----------------
    def generate_obstacles_safe(self, count=8, attempts=160):
        w = WIDTH // CELL
        h = HEIGHT // CELL

        for _ in range(attempts):
            blocks = []
            for __ in range(count):
                for ___ in range(40):
                    x = random.randint(0, w - 1)
                    y = random.randint(0, h - 1)
                    snake_hit = False
                    for p in self.snake:
                        if p.x == x and p.y == y:
                            snake_hit = True
                            break
                    if snake_hit:
                        continue
                    if any(b[0] == x and b[1] == y for b in blocks):
                        continue
                    blocks.append((x, y))
                    break

            if len(blocks) < count:
                continue
            if self.obstacles_fully_connected(blocks):
                self.obstacles = blocks
                return

        self.obstacles = []
