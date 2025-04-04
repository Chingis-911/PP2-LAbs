import pygame
import random
from pygame.locals import *

pygame.init()

width, height = 600, 600
CELL_SIZE = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PINK = (255, 0, 255)

DISPLAYSURF = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")
ICON = pygame.image.load("Images/snake.png")
pygame.display.set_icon(ICON)

snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

food_pos = [random.randrange(1, width // 10) * 10, random.randrange(1, height // 10) * 10]
food_spawn = True

banana_pos = [random.randrange(1, width // 10) * 10, random.randrange(1, height // 10) * 10]
banana_spawn = True
banana_timer = pygame.time.get_ticks()

cherry_pos = [random.randrange(1, width // 10) * 10, random.randrange(1, height // 10) * 10]
cherry_spawn = True
cherry_timer = pygame.time.get_ticks()

clock = pygame.time.Clock()
speed = 10
SCORE = 0
LEVEL = 0





direction = "RIGHT"
change_to = direction

def handle_events():
    global change_to, direction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                change_to = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                change_to = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                change_to = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                change_to = "RIGHT"
    direction = change_to

def move_snake():
    global direction, snake_pos, food_spawn, banana_spawn, cherry_spawn
    global food_pos, banana_pos, cherry_pos, banana_timer, cherry_timer

    if direction == "UP":
        snake_pos[1] -= CELL_SIZE
    elif direction == "DOWN":
        snake_pos[1] += CELL_SIZE
    elif direction == "LEFT":
        snake_pos[0] -= CELL_SIZE
    elif direction == "RIGHT":
        snake_pos[0] += CELL_SIZE

    snake_body.insert(0, list(snake_pos))

    global SCORE  #if we got certain fruit then 
    if snake_pos == food_pos:
        food_spawn = False
        SCORE += 1
    elif snake_pos == banana_pos and banana_spawn:
        banana_spawn = False
        SCORE += 2
    elif snake_pos == cherry_pos and cherry_spawn:
        cherry_spawn = False
        SCORE += 3
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos[:] = [random.randrange(1, width // 10) * 10, random.randrange(1, height // 10) * 10]
        food_spawn = True

    if not banana_spawn:
        banana_pos[:] = [random.randrange(1, width // 10) * 10, random.randrange(1, height // 10) * 10]
        banana_timer = pygame.time.get_ticks()
        banana_spawn = True

    if not cherry_spawn:
        cherry_pos[:] = [random.randrange(1, width // 10) * 10, random.randrange(1, height // 10) * 10]
        cherry_timer = pygame.time.get_ticks()
        cherry_spawn = True

def show_lev():
    global SCORE, speed, LEVEL
    LEVEL = int(SCORE / 4)
    speed = LEVEL + 10

rect = pygame.Surface((180, 30))
rect.fill(GREEN)

def show_sc():
    global SCORE, LEVEL
    DISPLAYSURF.blit(rect, (30, 30))
    font1 = pygame.font.SysFont('Verdana', 20)
    txt = font1.render(f'Your score : {SCORE}  Level : {LEVEL}', True, WHITE)
    DISPLAYSURF.blit(txt, (30, 30))

def draw():
    for pos in snake_body:
        pygame.draw.rect(DISPLAYSURF, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(DISPLAYSURF, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    if banana_spawn:
        pygame.draw.rect(DISPLAYSURF, YELLOW, pygame.Rect(banana_pos[0], banana_pos[1], 10, 10))

    if cherry_spawn:
        pygame.draw.rect(DISPLAYSURF, PINK, pygame.Rect(cherry_pos[0], cherry_pos[1], 10, 10))

def check_game_over():
    if snake_pos[0] < 0 or snake_pos[0] > width - 10 or snake_pos[1] < 0 or snake_pos[1] > height - 10:
        game_over_screen()

    for block in snake_body[1:]:
        if snake_pos == block:
            game_over_screen()

def game_over_screen():
    DISPLAYSURF.fill(RED)
    font = pygame.font.SysFont('Verdana', 40)
    game_over_text = font.render(f'Game Over! Score: {SCORE}', True, WHITE)
    DISPLAYSURF.blit(game_over_text, (width // 6, height // 3))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    quit()

running = True
while running:
    DISPLAYSURF.fill(BLACK)
    handle_events()
    move_snake()
    check_game_over()
    show_sc()
    show_lev()
    draw()

    current_time = pygame.time.get_ticks()
    if banana_spawn and current_time - banana_timer > 5000:
        banana_spawn = False
    if cherry_spawn and current_time - cherry_timer > 3000:
        cherry_spawn = False

    pygame.display.flip()
    clock.tick(speed)
