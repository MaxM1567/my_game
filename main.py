import pygame
import os
import sys
import random

FPS = 60
W = 1000  # ширина экрана
H = 700  # высота экрана
WHITE = (255, 255, 255)
BLUE = (0, 70, 225)
RIGHT = "to the right"
LEFT = "to the left"
UP = "to the up"
DOWN = "to the down"
STOP = "stop"

version = '0.3.2'

pygame.init()

sc = pygame.display.set_mode((W, H))
background = pygame.image.load('data/background.png')
sc.blit(background, (0, 0))


class Character(pygame.sprite.Sprite):
    def __init__(self, x, filename):
        pygame.sprite.Sprite.__init__(self)
        fullname = os.path.join('data', filename)
        self.image = pygame.image.load(fullname).convert_alpha()
        self.rect = self.image.get_rect(center=(x, 100))

    def update(self, motion):
        # ПЕРЕМЕЩЕНИЕ
        if motion == LEFT:
            self.rect.x -= 3
        elif motion == RIGHT:
            self.rect.x += 3
        elif motion == UP:
            self.rect.y -= 3
        elif motion == DOWN:
            self.rect.y += 3


class Point(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        fullname = os.path.join('data', filename)
        self.image = pygame.image.load(fullname).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))


# Создание монеток
moneys = pygame.sprite.Group()

for i in range(5):
    moneys.add(Point(random.randint(100, 900), random.randint(100, 600),  'money.png'))

character = Character(100, 'character_right.png')
enemy = Character(10, 'enemy_right.png')

clock = pygame.time.Clock()
motion = STOP

while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_LEFT:
                motion = LEFT
            elif i.key == pygame.K_RIGHT:
                motion = RIGHT
            elif i.key == pygame.K_UP:
                motion = UP
            elif i.key == pygame.K_DOWN:
                motion = DOWN
        elif i.type == pygame.KEYUP:
            if i.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                motion = STOP

    # нарисовал фон
    sc.blit(background, (0, 0))

    # НАРИСОВАЛ СЕБЯ
    sc.blit(character.image, character.rect)

    # НАРИСОВАЛ ВРАГА
    sc.blit(enemy.image, enemy.rect)

    # Нарисовал монетки
    moneys.draw(sc)

    # обновил дисплей
    pygame.display.update()

    # ОБНОВИЛ СЕБЯ
    if motion == LEFT:
        character.image = pygame.image.load('data/character_left.png').convert_alpha()

    elif motion == RIGHT:
        character.image = pygame.image.load('data/character_right.png').convert_alpha()

    character.update(motion)

    # КРАСНЫЙ ДОГНАЛ
    if character.rect.x == enemy.rect.x and character.rect.y == enemy.rect.y:
        print('Поражение!')
        exit(0)

    # КРАСНЫЙ ДОГОНЯЕТ
    if enemy.rect.x == character.rect.x and enemy.rect.y != character.rect.y:
        pass
    elif enemy.rect.x < character.rect.x:
        enemy.image = pygame.image.load('data/enemy_right.png').convert_alpha()
        enemy.rect.x += 1
    else:
        enemy.image = pygame.image.load('data/enemy_left.png').convert_alpha()
        enemy.rect.x -= 1

    if enemy.rect.y < character.rect.y:
        enemy.rect.y += 1
    else:
        enemy.rect.y -= 1

    clock.tick(FPS)
