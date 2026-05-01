import pygame
import random

pygame.init()

# -------------------- COLORS --------------------
colorWHITE = (255, 255, 255)
colorGRAY = (200, 200, 200)
colorBLACK = (0, 0, 0)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorYELLOW = (255, 255, 0)
colorPURPLE = (200, 0, 200)

# -------------------- SCREEN --------------------
WIDTH = 600
HEIGHT = 600
CELL = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# -------------------- FONTS --------------------
font = pygame.font.SysFont("Verdana", 20)
game_over_font = pygame.font.SysFont("Verdana", 50)

# -------------------- GAME VARIABLES --------------------
FPS = 5
score = 0
level = 1

# -------------------- GRID --------------------
def draw_grid():
    """Draw background grid"""
    for i in range(WIDTH // CELL):
        for j in range(HEIGHT // CELL):
            pygame.draw.rect(
                screen,
                colorGRAY,
                (i * CELL, j * CELL, CELL, CELL),
                1
            )

# -------------------- BASIC STRUCT --------------------
class Point:
    """Simple point class for coordinates"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

# =========================================================
# ======================== SNAKE ===========================
# =========================================================

class Snake:
    """Main snake object"""

    def __init__(self):
        self.body = [
            Point(10, 10),
            Point(9, 10),
            Point(8, 10)
        ]
        self.dx = 1
        self.dy = 0

    def move(self):
        """Move snake body forward"""
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def draw(self):
        """Draw snake on screen"""
        head = self.body[0]
        pygame.draw.rect(screen, colorRED,
                         (head.x * CELL, head.y * CELL, CELL, CELL))

        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW,
                             (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_wall_collision(self):
        """Check collision with walls"""
        head = self.body[0]
        return (
            head.x < 0 or
            head.x >= WIDTH // CELL or
            head.y < 0 or
            head.y >= HEIGHT // CELL
        )

    def check_self_collision(self):
        """Check collision with itself"""
        head = self.body[0]
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

    def check_food_collision(self, food):
        """Handle eating food"""
        global score, level, FPS

        head = self.body[0]

        if head.x == food.pos.x and head.y == food.pos.y:

            # add score based on food value
            score += food.value

            # grow snake
            self.body.append(Point(self.body[-1].x, self.body[-1].y))

            # generate new food
            food.generate_random_position(self)

            # level up every 5 points
            if score % 5 == 0:
                level += 1
                FPS += 1


# =========================================================
# ========================= FOOD ===========================
# =========================================================

class Food:
    """Food with value and lifetime"""

    def __init__(self):
        self.pos = Point(5, 5)

        # possible food values
        self.values = [1, 2, 3]
        self.value = 1

        # timer (milliseconds)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 5000  # 5 seconds

    def draw(self):
        """Draw food with color based on value"""

        if self.value == 1:
            color = colorGREEN
        elif self.value == 2:
            color = colorYELLOW
        else:
            color = colorPURPLE

        pygame.draw.rect(
            screen,
            color,
            (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL)
        )

    def generate_random_position(self, snake):
        """Generate new position and random value"""

        self.value = random.choice(self.values)
        self.spawn_time = pygame.time.get_ticks()

        while True:
            x = random.randint(0, WIDTH // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)

            good = True
            for segment in snake.body:
                if segment.x == x and segment.y == y:
                    good = False

            if good:
                self.pos = Point(x, y)
                break

    def update_timer(self, snake):
        """Remove food if time expired"""

        current_time = pygame.time.get_ticks()

        if current_time - self.spawn_time > self.lifetime:
            self.generate_random_position(snake)


# =========================================================
# ======================= RESET ============================
# =========================================================

def reset_game():
    """Reset all game values"""
    global snake, food, score, level, FPS, game_over

    score = 0
    level = 1
    FPS = 5
    game_over = False

    snake = Snake()
    food = Food()
    food.generate_random_position(snake)


# =========================================================
# ======================= MAIN =============================
# =========================================================

clock = pygame.time.Clock()

snake = Snake()
food = Food()
food.generate_random_position(snake)

running = True
game_over = False

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # restart
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()

        if event.type == pygame.KEYDOWN and not game_over:

            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx, snake.dy = 0, 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx, snake.dy = 0, -1

    if not game_over:
        screen.fill(colorBLACK)

        draw_grid()

        snake.move()
        snake.check_food_collision(food)

        # update food timer (disappearing food)
        food.update_timer(snake)

        # lose conditions
        if snake.check_wall_collision() or snake.check_self_collision():
            game_over = True

        snake.draw()
        food.draw()

        # UI
        score_text = font.render("Score: " + str(score), True, colorWHITE)
        level_text = font.render("Level: " + str(level), True, colorWHITE)

        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (450, 10))

    else:
        screen.fill(colorRED)

        over_text = game_over_font.render("Game Over", True, colorBLACK)
        restart_text = font.render("Press R to restart", True, colorWHITE)

        screen.blit(over_text, (170, 250))
        screen.blit(restart_text, (180, 320))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()