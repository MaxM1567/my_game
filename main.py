import random
import pygame
import os
import sys
import datetime
import time


FPS = 60
W = 1000  # ширина экрана
H = 700  # высота экрана
WHITE = (255, 255, 255)
GREEN = (25, 225, 25)

sc = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
score = 0

version = '0.6.1'


# 1. создал камеру для персоонажа
# 2. расширил карту и сделал края
# 3. подогнал все спрайты под ноаую карту


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    if text == '5':
        text_surface = font.render('ВЫХОД ОТКРЫТ', True, GREEN)
        x -= 100
    else:
        text_surface = font.render(text + '/5', True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_seconds(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {'wall': load_image('concrete_brick.png'),
               'empty': load_image('concrete_brick_2.png'),
               'border': load_image('border.png')}

tile_width = tile_height = 48


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - W // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - H // 2)


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
        self.walk_right_enemy = [pygame.transform.scale(pygame.image.load(f'data/enemy/walk{i}_e.png'),
                                                        (50, 100)) for i in range(1, 5)]

        self.walk_left_enemy = [pygame.transform.flip(self.walk_right_enemy[i], True, False) for i in range(4)]

        self.enemy_stand = pygame.transform.scale(pygame.image.load(f'data/enemy/stand_e.png'), (50, 100))

        self.animation = 0
        self.count = 0

    def update(self):
        if self.rect.x == test_p1.rect.x and self.rect.y != test_p1.rect.y:
            pass
        elif self.rect.x < test_p1.rect.x:
            self.image = self.walk_right_enemy[self.animation % 4]
            if self.count == 6:
                self.animation += 1
                self.count = 0
            self.count += 1
            self.rect.x += 1.5
        else:
            self.image = self.walk_left_enemy[self.animation % 4]
            if self.count == 6:
                self.animation += 1
                self.count = 0
            self.count += 1
            self.rect.x -= 1.5
        if self.rect.y < test_p1.rect.y:
            self.rect.y += 1.5
        else:
            self.rect.y -= 1.5


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        super().__init__(all_sprites, exits_group)
        self.image = pygame.image.load(os.path.join('data', filename)).convert_alpha()
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        super().__init__(coin_group, all_sprites)
        self.image = pygame.image.load(os.path.join('data', filename)).convert_alpha()
        self.rect = self.image.get_rect().move(x, y)


# группы спрайтов
exits_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
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
                Tile('border', x, y)
    return x, y


# Создание монеток
for i in range(5):
    money = Coin(random.randint(630, 3650), random.randint(200, 1200), 'money.png')

opponent = Enemy(random.randint(14, 80), random.randint(8, 25), 'enemy_left.png')
test_p1 = Player(24, 14, 'character_right.png')

# ТЕСТ
exit_1 = Exit(21, 28.98, 'Exit_open_2.png')
camera = Camera()

if __name__ == '__main__':
    pygame.init()

    pygame.mixer.music.load('data/music.mp3')  # музыка
    pygame.mixer.music.play()

    level_x, level_y = generate_level(load_level('map.txt'))
    keys = pygame.key.get_pressed()
    count = 0
    animation = 0

    walk_right = [pygame.transform.scale(pygame.image.load(f'data/sprites-3/walk{i}.png'),
                                         (50, 100)) for i in range(1, 7)]
    walk_left = [pygame.transform.flip(walk_right[i], True, False) for i in range(6)]

    start_time = time.time()

    while 1:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()

        # Смерть главного персоонажа (разкоментить)
        if pygame.sprite.spritecollide(test_p1, mobs_group, True):
            exit(0)

        if pygame.sprite.spritecollide(test_p1, coin_group, True):
            score += 1

        if pygame.sprite.spritecollide(test_p1, exits_group, False) and score == 5:
            exit(0)

        camera.update(test_p1)

        for sprite in all_sprites:
            camera.apply(sprite)

        tiles_group.draw(sc)
        coin_group.draw(sc)
        exits_group.draw(sc)
        mobs_group.draw(sc)
        player_group.draw(sc)

        draw_text(sc, str(score), 40, 950, 10)
        #  draw_seconds(sc, f'{datetime.datetime.min.minute}:{datetime.datetime.now().second}', 40, 950, 60)
        draw_seconds(sc, f'время: {(time.time() - start_time) // 1}', 40, 950, 60)
        pygame.display.flip()
        keys = pygame.key.get_pressed()

        opponent.update()

        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            test_p1.image = walk_right[animation % 6]
            test_p1.rect.x += 3
            test_p1.rect.y -= 3
            if count == 6:  # скорость изменения шагов (если 12 то медленнее)
                animation += 1
                count = 0
            count += 1

        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            test_p1.image = walk_left[animation % 6]
            test_p1.rect.x -= 3
            test_p1.rect.y -= 3
            if count == 6:  # скорость изменения шагов (если 12 то медленнее)
                animation += 1
                count = 0
            count += 1

        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            test_p1.image = walk_right[animation % 6]
            test_p1.rect.x += 3
            test_p1.rect.y += 3
            if count == 6:  # скорость изменения шагов (если 12 то медленнее)
                animation += 1
                count = 0
            count += 1

        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            test_p1.image = walk_left[animation % 6]
            test_p1.rect.x -= 3
            test_p1.rect.y += 3
            if count == 6:  # скорость изменения шагов (если 12 то медленнее)
                animation += 1
                count = 0
            count += 1
            # test_p1.rect.y += 3
            # test_p1.rect.x -= 3

        elif keys[pygame.K_LEFT]:
            test_p1.image = walk_left[animation % 6]
            test_p1.rect.x -= 3
            if count == 6:  # скорость изменения шагов (если 12 то медленнее)
                animation += 1
                count = 0
            count += 1


        elif keys[pygame.K_RIGHT]:
            test_p1.image = walk_right[animation % 6]
            test_p1.rect.x += 3
            if count == 6:  # скорость изменения шагов (если 12 то медленнее)
                animation += 1
                count = 0
            count += 1

        elif keys[pygame.K_DOWN]:
            test_p1.rect.y += 3

        elif keys[pygame.K_UP]:
            test_p1.rect.y -= 3

        else:
            test_p1.image = walk_right[0]

        clock.tick(FPS)
