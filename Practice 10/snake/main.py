import pygame
import random

pygame.init()

# colors
colorWHITE = (255, 255, 255)
colorGRAY = (200, 200, 200)
colorBLACK = (0, 0, 0)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorYELLOW = (255, 255, 0)

# screen settings
WIDTH = 600
HEIGHT = 600
CELL = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# fonts
font = pygame.font.SysFont("Verdana", 20)
game_over_font = pygame.font.SysFont("Verdana", 50)

# game values
FPS = 5
score = 0
level = 1


def draw_grid():
    # draw simple grid
    for i in range(WIDTH // CELL):
        for j in range(HEIGHT // CELL):
            pygame.draw.rect(
                screen,
                colorGRAY,
                (i * CELL, j * CELL, CELL, CELL),
                1
            )


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Snake:
    def __init__(self):
        # starting snake body
        self.body = [
            Point(10, 10),
            Point(9, 10),
            Point(8, 10)
        ]

        self.dx = 1
        self.dy = 0

    def move(self):
        # move body from tail to head
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        # move head
        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def draw(self):
        # draw head
        head = self.body[0]
        pygame.draw.rect(
            screen,
            colorRED,
            (head.x * CELL, head.y * CELL, CELL, CELL)
        )

        # draw body
        for segment in self.body[1:]:
            pygame.draw.rect(
                screen,
                colorYELLOW,
                (segment.x * CELL, segment.y * CELL, CELL, CELL)
            )

    def check_wall_collision(self):
        head = self.body[0]

        # check if snake leaves screen
        if (
            head.x < 0 or
            head.x >= WIDTH // CELL or
            head.y < 0 or
            head.y >= HEIGHT // CELL
        ):
            return True

        return False

    def check_self_collision(self):
        head = self.body[0]

        # check collision with own body
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True

        return False

    def check_food_collision(self, food):
        global score
        global level
        global FPS

        head = self.body[0]

        if head.x == food.pos.x and head.y == food.pos.y:
            score += 1

            # increase snake length
            self.body.append(
                Point(
                    self.body[-1].x,
                    self.body[-1].y
                )
            )

            # generate new food
            food.generate_random_position(self)

            # next level every 4 foods
            if score % 4 == 0:
                level += 1
                FPS += 1


class Food:
    def __init__(self):
        self.pos = Point(5, 5)

    def draw(self):
        pygame.draw.rect(
            screen,
            colorGREEN,
            (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL)
        )

    def generate_random_position(self, snake):
        while True:
            x = random.randint(0, WIDTH // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)

            good_position = True

            # food should not be on snake
            for segment in snake.body:
                if segment.x == x and segment.y == y:
                    good_position = False

            if good_position:
                self.pos = Point(x, y)
                break


def reset_game():
    global snake
    global food
    global score
    global level
    global FPS
    global game_over

    # reset values
    score = 0
    level = 1
    FPS = 5
    game_over = False

    # create new snake and food
    snake = Snake()
    food = Food()
    food.generate_random_position(snake)


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

        # restart game with R
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()

        if event.type == pygame.KEYDOWN and not game_over:

            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx = 1
                snake.dy = 0

            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx = -1
                snake.dy = 0

            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx = 0
                snake.dy = 1

            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx = 0
                snake.dy = -1

    if not game_over:
        screen.fill(colorBLACK)

        draw_grid()

        snake.move()
        snake.check_food_collision(food)

        # lose conditions
        if snake.check_wall_collision() or snake.check_self_collision():
            game_over = True

        snake.draw()
        food.draw()

        # score text
        score_text = font.render(
            "Score: " + str(score),
            True,
            colorWHITE
        )
        screen.blit(score_text, (10, 10))

        # level text
        level_text = font.render(
            "Level: " + str(level),
            True,
            colorWHITE
        )
        screen.blit(level_text, (450, 10))

    else:
        screen.fill(colorRED)

        over_text = game_over_font.render(
            "Game Over",
            True,
            colorBLACK
        )

        screen.blit(over_text, (170, 250))

        restart_text = font.render(
            "Press R to restart",
            True,
            colorWHITE
        )

        screen.blit(restart_text, (180, 320))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()