import pygame
import os
import sys

FPS = 60
W = 1000  # ширина экрана
H = 700  # высота экрана
WHITE = (255, 255, 255)
BLUE = (0, 70, 225)

sc = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

version = '0.3.2'  # было 0.3.1 поставил 0.3.2 (исправил бег)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {'wall': load_image('concrete_brick.png'), 'empty': load_image('concrete_brick_2.png')}
player_image = load_image('character_right.png')

tile_width = tile_height = 48


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)


'''
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, filename):
        pygame.sprite.Sprite.__init__(self, player_group, all_sprites)
        fullname = os.path.join('data', filename)
        self.image = pygame.image.load(fullname).convert_alpha()
        self.rect = self.image.get_rect(center=(x, 100))

    def update(self, motion):
        if enemy.rect.x == character.rect.x and enemy.rect.y != character.rect.y:
            pass
        elif enemy.rect.x < character.rect.x:
            self.image = pygame.image.load('data/enemy_right.png').convert_alpha()
            enemy.rect.x += 1
        else:
            self.image = pygame.image.load('data/enemy_left.png').convert_alpha()
            enemy.rect.x -= 1

        if enemy.rect.y < character.rect.y:
            enemy.rect.y += 1
        else:
            enemy.rect.y -= 1
'''

# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


test_p1 = Player(3, 3)

if __name__ == '__main__':
    pygame.init()
    player, level_x, level_y = generate_level(load_level('map.txt'))

    while 1:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()
            # elif i.type == pygame.KEYDOWN:
            #     if i.key == pygame.K_LEFT:
            #         motion = LEFT
            #     elif i.key == pygame.K_RIGHT:
            #         motion = RIGHT
            #     elif i.key == pygame.K_UP:
            #         motion = UP
            #     elif i.key == pygame.K_DOWN:
            #         motion = DOWN
            # elif i.type == pygame.KEYUP:
            #     if i.key in [pygame.K_LEFT,
            #                  pygame.K_RIGHT]:
            #         motion = STOP

        tiles_group.draw(sc)
        player_group.draw(sc)
        pygame.display.flip()
        keys = pygame.key.get_pressed()
        # if motion == LEFT:
        #     test_p1.rect.x -= 3
        # elif motion == RIGHT:
        #     test_p1.rect.x += 3
        # elif motion == DOWN:
        #     test_p1.rect.y += 3
        # elif motion == UP:
        #     test_p1.rect.y -= 3
        if keys[pygame.K_LEFT]:
            test_p1.rect.x -= 3
        elif keys[pygame.K_RIGHT]:
            test_p1.rect.x += 3
        elif keys[pygame.K_DOWN]:
            test_p1.rect.y += 3
        elif keys[pygame.K_UP]:
            test_p1.rect.y -= 3

        clock.tick(FPS)
