import pygame
import sys
from pygame.locals import *
import random
import time

pygame.init()


FPS = 60
FramePerSec = pygame.time.Clock()
width, height = 400, 600

#Colors
BLUE = (0, 0, 255)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
GREY = pygame.Color(128, 128, 128)
RED = pygame.Color(255, 0, 0)

SPEED = 5
SCORE = 0

#For the text
font = pygame.font.SysFont("Verdana", 25)
font_small = pygame.font.SysFont("Verdana", 20)

background = pygame.image.load("Images/AnimatedStreet.png")
icon = pygame.image.load("Images/sport-car.png")

DISPLAYSURF = pygame.display.set_mode((width, height))
pygame.display.set_caption("Race")
pygame.display.set_icon(icon)

#in order to get random coins
def rand_coin_type():
    return random.randint(1, 3)

#Class for enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/cthulhu.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, width - 40), 0)
    
    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > height:
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

#class for Players
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/car.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT] and self.rect.right < width:
            self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.relocate()

    def relocate(self):
        self.coin_type = rand_coin_type() 
        if self.coin_type == 1: #Depending on value we get certain money type
            self.image = pygame.image.load("Images/dollar.png")
            self.value = 1
        elif self.coin_type == 2:
            self.image = pygame.image.load("Images/money.png")
            self.value = 2
        elif self.coin_type == 3:
            self.image = pygame.image.load("Images/money-bag.png")
            self.value = 3

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, width - 40), 0)

    def move(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > height:
            self.relocate()

P1 = Player()
E1 = Enemy()
C1 = Coin()
C2 = Coin()
#Assining groups so in future it would be easier to manipulate with multiple 
#enemy,coins and etc
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)
coins.add(C2)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1, C2)

running = True

#Changing the spedd relying on a score
def inc_speed():
    global SCORE, SPEED
    SPEED = 5 + SCORE // 4

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    inc_speed()
    DISPLAYSURF.blit(background, (0, 0))

    #Score update
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    DISPLAYSURF.blit(scores, (width - 130, 10))

    
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('Sounds/crash.wav').play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)

        game_over_text = font.render(f"Game Over, Score: {SCORE}", True, BLACK)
        DISPLAYSURF.blit(game_over_text, (50, 250))
        pygame.display.update()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    collected_coins = pygame.sprite.spritecollide(P1, coins, False)
    for coin in collected_coins:
        pygame.mixer.Sound('Sounds/getCoin.wav').play()
        SCORE += coin.value
        coin.relocate()

    pygame.display.update()
    FramePerSec.tick(FPS)
