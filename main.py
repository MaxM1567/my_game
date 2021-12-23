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

version = '0.4.2'  # было 0.3.1 поставил 0.3.2 (исправил бег)


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

tile_width = tile_height = 48


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        super().__init__(player_group, all_sprites)
        self.image = pygame.image.load(os.path.join('data', filename)).convert_alpha()
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self, mobs_group, all_sprites)
        self.image = pygame.image.load(os.path.join('data', filename)).convert_alpha()
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)

    def update(self):
        if self.rect.x == test_p1.rect.x and self.rect.y != test_p1.rect.y:
            pass
        elif self.rect.x < test_p1.rect.x:
            self.image = pygame.image.load('data/enemy_right.png').convert_alpha()
            self.rect.x += 1
        else:
            self.image = pygame.image.load('data/enemy_left.png').convert_alpha()
            self.rect.x -= 1
        if self.rect.y < test_p1.rect.y:
            self.rect.y += 1
        else:
            self.rect.y -= 1


# группы спрайтов
all_sprites = pygame.sprite.Group()
mobs_group = pygame.sprite.Group()
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
    return x, y


opponent = Enemy(1, 1, 'enemy_left.png')
test_p1 = Player(3, 3, 'character_right.png')

if __name__ == '__main__':
    pygame.init()
    level_x, level_y = generate_level(load_level('map.txt'))
    keys = pygame.key.get_pressed()

    while 1:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()

        if pygame.sprite.spritecollide(test_p1, mobs_group, True):
            exit(0)

        tiles_group.draw(sc)
        mobs_group.draw(sc)
        player_group.draw(sc)
        pygame.display.flip()
        keys = pygame.key.get_pressed()

        opponent.update()

        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            test_p1.image = load_image('character_right.png')
            test_p1.rect.y -= 3
            test_p1.rect.x += 3

        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            test_p1.image = load_image('character_left.png')
            test_p1.rect.y -= 3
            test_p1.rect.x -= 3

        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            test_p1.image = load_image('character_right.png')
            test_p1.rect.y += 3
            test_p1.rect.x += 3

        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            test_p1.image = load_image('character_left.png')
            test_p1.rect.y += 3
            test_p1.rect.x -= 3

        elif keys[pygame.K_LEFT]:
            test_p1.image = load_image('character_left.png')
            test_p1.rect.x -= 3

        elif keys[pygame.K_RIGHT]:
            test_p1.image = load_image('character_right.png')
            test_p1.rect.x += 3

        elif keys[pygame.K_DOWN]:
            test_p1.rect.y += 3

        elif keys[pygame.K_UP]:
            test_p1.rect.y -= 3

        clock.tick(FPS)
