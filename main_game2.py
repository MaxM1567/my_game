import random
import pygame
import os
import sys

# КОНСТАНТЫ
FPS = 60  # fps
W = 1000  # ширина экрана
H = 700  # высота экрана

WHITE = (255, 255, 255)  # белый цыет
GREEN = (25, 225, 25)  # зелёный цыет

font_name = pygame.font.match_font('arial')  # шрифт "arial"

tile_width = tile_height = 48  # размер одного блока карты

# Положение относительно карты
x_map_player = 1  # игрок x
y_map_player = 1  # игрок y

x_map_opponent = 1  # противник x
y_map_opponent = 1  # противник y


# ПАРАМЕТРЫ
sc = pygame.display.set_mode((W, H))  # разсер окна
clock = pygame.time.Clock()  # какие-то часы (связанно с FPS)
score = 0  # счёт

# ВЕРСИЯ ПРОГРАММЫ
version = 'BETA 0.6.0'  # версия
# 1. Создал ящики на карте осуществляющие функцию препядствий
# 2. Добавил взаимодействие сущностей и препядствий на карте (требует доработки)
# 3. Незначительная оптимизация кода

# TEST---TEST---TEST---TEST---TEST---TEST---TEST---TEST
x_last = 1
y_last = 1

x_last_opponent = 1
y_last_opponent = 1
# TEST---TEST---TEST---TEST---TEST---TEST---TEST---TEST


# ЗАГРУЗКА КАРТИНОК
def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# РИСОВАЛКА ТЕКСТА
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


# ЗАГРУЗКА УРОВНЯ
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('@')
    return list(map(lambda x: x.ljust(max_width, '@'), level_map))


# СПИСОК КАРТИНОК ДЛЯ ОТРИСОВКИ УРОВНЯ
tile_images = {'wall': load_image('concrete_brick.png'),
               'empty': load_image('concrete_brick_2.png'),
               'border': load_image('border.png')}


# ОБЪЕКТ ЕДИНИЧНАЯ ПЛИТКА
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


# ОБЪЕКТ ЯЩИК
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, filename):
        super().__init__(obstacle_group, all_sprites)
        self.image = pygame.image.load(os.path.join('data', filename)).convert_alpha()
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


# ОБЪЕКТ КАМЕРА
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


# ОБЪЕКТ ПЕРСООНАЖ
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        super().__init__(player_group, all_sprites)
        self.image = pygame.image.load(os.path.join('data', filename)).convert_alpha()
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)


# ОБЪЕКТ ПРОТИВНИК
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self, mobs_group, all_sprites)
        self.image = pygame.image.load(os.path.join('data', filename)).convert_alpha()
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)
        self.x_map = 1
        self.y_map = 1

    def update(self):
        if self.rect.x != player.rect.x:
            if self.rect.x < player.rect.x:
                self.image = pygame.image.load('data/enemy_right.png').convert_alpha()
                # ПОЗИЦИЯ
                self.x_map += 1.5  # относительно карты
                self.rect.x += 1.5  # относительно окна игры
            else:
                self.image = pygame.image.load('data/enemy_left.png').convert_alpha()
                self.x_map -= 1.5  # относительно карты
                self.rect.x -= 1.5  # относительно окна игры

        if self.rect.y != player.rect.y:
            if self.rect.y < player.rect.y:
                self.y_map += 1.5  # относительно карты
                self.rect.y += 1.5  # относительно окна игры
            else:
                self.y_map -= 1.5  # относительно карты
                self.rect.y -= 1.5  # относительно окна игры


# ОБЪЕКТ ВЫХОД
class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        super().__init__(all_sprites, exits_group)
        self.image = pygame.image.load(os.path.join('data', filename)).convert_alpha()
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)


# ОБЪЕКТ МОЕТА
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        super().__init__(coin_group, all_sprites)
        self.image = pygame.image.load(os.path.join('data', filename)).convert_alpha()
        self.rect = self.image.get_rect().move(x, y)


# ГРУППЫ СПРАЙТОВ
exits_group = pygame.sprite.Group()  # exit
coin_group = pygame.sprite.Group()  # coin
mobs_group = pygame.sprite.Group()  # mobs
obstacle_group = pygame.sprite.Group()  # obstacle
tiles_group = pygame.sprite.Group()  # tiles
player_group = pygame.sprite.Group()  # player
all_sprites = pygame.sprite.Group()  # all sprite


# ГЕНЕРАЦИЯ КАРТЫ
def generate_level(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            if level[y][x] == '#':
                Tile('wall', x, y)
            if level[y][x] == '@':
                Tile('border', x, y)
    return x, y


# СОЗДАНИЕ СПРАЙТОВ(ОБЪЕКТОВ)
player = Player(30, 15, 'character_right.png')  # создание глвного героя
opponent = Enemy(random.randint(14, 80), random.randint(8, 25), 'enemy_left.png')  # создание врага
exit_1 = Exit(21, 28.98, 'Exit_open_2.png')  # Выход 1
camera = Camera()  # создал камеру

for i in range(5):  # генерация монеток
    money = Coin(random.randint(630, 3650), random.randint(200, 1200), 'money.png')

for i in range(15):  # генерация ящиков
    obstacle = Obstacle(random.randint(14, 80), random.randint(8, 25), 'obstacle_2.png')

# НАЧАЛО ПРОГРАММЫ
if __name__ == '__main__':
    pygame.init()
    level_x, level_y = generate_level(load_level('map.txt'))
    keys = pygame.key.get_pressed()

    # МУЗЫКА
    # pygame.mixer.music.load('data/music.mp3')  # музыка
    # pygame.mixer.music.play()

    # НАЧАЛО ОСНОВНОГО ЦИКЛА ПРОГРАММЫ
    while True:
        # ОБНАРУЖЕНИЕ ИВЕНТОВ PYGAME
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()

        # ОБНАРУЖЕНИЕ СТОЛКНОВЕНИЙ
        if pygame.sprite.spritecollide(player, obstacle_group, False):  # персоонаж
            player.rect.x += (x_last - x_map_player)
            player.rect.y += (y_last - y_map_player)

        x_last = x_map_player  # x персоонажа до столкновения
        y_last = y_map_player  # y персоонажа до столкновения

        if pygame.sprite.spritecollide(opponent, obstacle_group, False):  # противник
            opponent.rect.x += (x_last_opponent - opponent.x_map)
            opponent.rect.y += (y_last_opponent - opponent.y_map)

        x_last_opponent = opponent.x_map  # x врага до столкновения
        y_last_opponent = opponent.y_map  # y врага до столкновения

        # ПРОВЕРКИ РАЗНЫХ СОБЫТИЙ ВНУТРИ ИГРЫ
        if pygame.sprite.spritecollide(player, mobs_group, True):  # смерть персоонажа
            exit(0)

        if pygame.sprite.spritecollide(player, coin_group, True):  # начисление счёта за нахождение монетки
            score += 1

        if pygame.sprite.spritecollide(player, exits_group, False) and score == 5:  # активация выхода
            exit(0)

        # ОБНОВЛЕНИЕ КАМЕРЫ
        camera.update(player)  # сама камера

        for sprite in all_sprites:  # остальные спрайты
            camera.apply(sprite)

        # ОТРИСОВАКА ВСЕХ СПРАЙТОВ НА ЭКРАНЕ
        tiles_group.draw(sc)     # карта
        obstacle_group.draw(sc)  # ящики
        coin_group.draw(sc)      # монетки
        exits_group.draw(sc)     # выходы
        mobs_group.draw(sc)      # противник
        player_group.draw(sc)    # игрок
        draw_text(sc, str(score), 40, 950, 10)  # счёт

        # КАКИЕ-ТО ВАЖНЫЙ ШТУКИ
        pygame.display.flip()  # флип
        keys = pygame.key.get_pressed()  # список нажимаемых клавишь

        # ПЕРЕМЕЩЕНИЕ СУЩНОСТЕЙ
        opponent.update()  # враг

        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:  # игрок
            player.image = load_image('character_right.png')

            y_map_player -= 3
            x_map_player += 3

            player.rect.y -= 3
            player.rect.x += 3

        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            player.image = load_image('character_left.png')

            y_map_player -= 3
            x_map_player -= 3

            player.rect.y -= 3
            player.rect.x -= 3

        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            player.image = load_image('character_right.png')

            y_map_player += 3
            x_map_player += 3

            player.rect.y += 3
            player.rect.x += 3

        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            player.image = load_image('character_left.png')

            y_map_player += 3
            x_map_player -= 3

            player.rect.y += 3
            player.rect.x -= 3

        elif keys[pygame.K_LEFT]:
            player.image = load_image('character_left.png')
            x_map_player -= 3
            player.rect.x -= 3

        elif keys[pygame.K_RIGHT]:
            player.image = load_image('character_right.png')
            x_map_player += 3
            player.rect.x += 3

        elif keys[pygame.K_DOWN]:
            y_map_player += 3
            player.rect.y += 3

        elif keys[pygame.K_UP]:
            y_map_player -= 3
            player.rect.y -= 3

        clock.tick(FPS)  # опять часы
