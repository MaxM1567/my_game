import random
import pygame
import os
import sys
import datetime

while True:
    # КОНСТАНТЫ
    FPS = 60  # fps
    W = 1000  # ширина экрана
    H = 700  # высота экрана

    WHITE = (255, 255, 255)  # белый цвет
    GREEN = (25, 225, 25)  # зелёный цвет
    BLACK = (0, 0, 0)  # чёрный цвет

    font_name = pygame.font.match_font('arial')  # шрифт "arial"

    tile_width = tile_height = 48  # размер одного блока карты

    # ПАРАМЕТРЫ
    sc = pygame.display.set_mode((W, H))  # разсер окна
    clock = pygame.time.Clock()  # какие-то часы (связанно с FPS)
    score = 0  # счёт
    counter_interface = 0  # счётчик интерфейса
    side_character = 'r'
    tile_images = {}  # список плиток для карты
    initial_time = datetime.datetime.now()  # время начала игры

    # ВЕРСИЯ ПРОГРАММЫ
    version = '1.0.2 '  # версия

    # 1. На экране окончания время показывается точнее
    # 2. Незначительная оптимизация кода

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
            text_surface = font.render('EXIT ON', True, WHITE)
            x -= 26
        else:
            text_surface = font.render(text + '/5', True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    # РИМОВАЛКА ТАЙМЕРА
    def draw_seconds(surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
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

    # ОТОБРАЖЕНИЕ ИНТЕРФЕЙСА
    def display_interface(k):
        if k % 3 == 0:
            # РИСОВКА ТАЙМЕРА
            pygame.draw.rect(sc, BLACK, (850, 0, 950, 40))

            # РАСЧЁТ ВРЕМЕНИ
            seconds = (datetime.datetime.now() - start_time).seconds
            minutes = seconds // 60
            seconds = seconds - minutes * 60

            draw_seconds(sc, 'time: ' + f'{minutes}:{seconds}', 30, 922, 2)

            # РИСОВКА СЧЁТА
            pygame.draw.rect(sc, GREEN, (850, 40, 950, 60))
            draw_text(sc, str(score), 40, 950, 50)

        if k % 3 == 1:
            draw_text(sc, str(score), 40, 950, 10)  # счёт

        if k % 3 == 2:
            pass

    # ОТРИСОВКА СПРАЙТОВ НА ЭКРАНЕ
    def draw_sprite_group():
        tiles_group.draw(sc)  # карта
        wall_border_group.draw(sc)  # граници стен
        wall_group.draw(sc)  # стены
        obstacle_group.draw(sc)  # ящики
        coin_group.draw(sc)  # монетки
        picture_group.draw(sc)  # картинки
        exits_group.draw(sc)  # выходы
        mobs_group.draw(sc)  # противник
        player_group.draw(sc)  # игрок

    # КОНЕЦ ИГРЫ
    def end_game():  # проверка: надо ли заканчивать игру
        global run

        if pygame.sprite.spritecollide(player, exits_group, False) and score == 5:  # активация выхода
            f = open('data/result.txt', 'r')
            text = f.read()
            f.close()

            os.remove('data/result.txt')

            f = open('data/result.txt', 'w')
            f.write(f'{str(datetime.datetime.now())[:16]}/{score}/Win\n{text}')
            f.close()

            show_end_menu(1)
            run = False

        elif pygame.sprite.spritecollide(player, mobs_group, True):  # смерть персоонажа
            f = open('data/result.txt', 'r')
            text = f.read()
            f.close()
            os.remove('data/result.txt')
            f = open('data/result.txt', 'w')
            f.write(f'{str(datetime.datetime.now())[:16]}/{(str(datetime.datetime.now() - initial_time))[2:7]}'
                    f'/{score}/Fail\n{text}')

            f.close()

            show_end_menu(0)
            run = False

    # ГЛАВНОЕ МЕНЮ
    def show_menu():
        # ПАРАМЕТРЫ
        show = True
        image = pygame.image.load('data/start_menu/main_menu_test.png')
        rect = image.get_rect(bottomright=(W, H))
        sc.blit(image, rect)
        global tile_images

        pygame.display.update()

        # ЗАПУСТИЛ ГЛАВНОЕ МЕНЮ
        while show:
            for event_1 in pygame.event.get():
                # ОБНАРУЖЕНИЕ ИВЕНТОВ PYGAME
                if event_1.type == pygame.QUIT:
                    sys.exit()
                if event_1.type == pygame.KEYDOWN:
                    if event_1.key == pygame.K_s:  # меню старт

                        image = pygame.image.load('data/start_menu/main_menu_levels.png')
                        rect = image.get_rect(bottomright=(W, H))
                        sc.blit(image, rect)
                        pygame.display.update()

                        show_1 = True

                        # ЗАПУСК МЕНЮ ВЫБОРА УРОВНЯ
                        while show_1:
                            for event_2 in pygame.event.get():
                                # ОБНАРУЖЕНИЕ ИВЕНТОВ PYGAME
                                if event_2.type == pygame.QUIT:
                                    sys.exit()
                                if event_2.type == pygame.KEYDOWN:
                                    if event_2.key == pygame.K_1:
                                        tile_images = {'wall': load_image('concrete_brick.png'),
                                                       'empty': load_image('concrete_brick_2.png'),
                                                       'border': load_image('border.png')}

                                        show_1 = False
                                        show = False

                                    elif event_2.key == pygame.K_2:
                                        tile_images = {'wall': load_image('wood_boards.png'),
                                                       'empty': load_image('wood_boards.png'),
                                                       'border': load_image('border.png')}

                                        show_1 = False
                                        show = False

                                    elif event_2.key == pygame.K_ESCAPE:
                                        show = True
                                        image = pygame.image.load('data/start_menu/main_menu_test.png')
                                        rect = image.get_rect(bottomright=(W, H))
                                        sc.blit(image, rect)

                                        pygame.display.update()
                                        show_1 = False

                    elif event_1.key == pygame.K_h:  # меню правила
                        image = pygame.image.load('data/start_menu/main_menu_rules.png')
                        rect = image.get_rect(bottomright=(W, H))
                        sc.blit(image, rect)
                        pygame.display.update()

                        show_1 = True

                        # ЗАПУСК ГЛАВНОГО МЕНЮ
                        while show_1:
                            for event_2 in pygame.event.get():
                                # ОБНАРУЖЕНИЕ ИВЕНТОВ PYGAME
                                if event_2.type == pygame.QUIT:
                                    sys.exit()
                                if event_2.type == pygame.KEYDOWN:
                                    if event_2.key == pygame.K_ESCAPE:
                                        show = True
                                        image = pygame.image.load('data/start_menu/main_menu_test.png')
                                        rect = image.get_rect(bottomright=(W, H))
                                        sc.blit(image, rect)

                                        pygame.display.update()
                                        show_1 = False

                    elif event_1.key == pygame.K_ESCAPE:
                        exit(0)

    # ФИНАЛЬНОЕ МЕНЮ
    def show_end_menu(result):
        show = True  # показ меню
        image = None  # наличие картинки

        if result == 1:  # выиигрышь или поражение
            image = pygame.image.load('data/end_menu/end_menu_win.png')
        elif result == 0:
            image = pygame.image.load('data/end_menu/end_menu_fail.png')

        rect = image.get_rect(bottomright=(W, H))
        sc.blit(image, rect)  # нарисовал финальный мнтерфейс

        # ОТРИСОВКА РЕЗУЛЬТАТОВ
        font = pygame.font.Font(font_name, 40)  # счёт
        text_surface = font.render(str(score), True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (518, 290)
        sc.blit(text_surface, text_rect)

        font = pygame.font.Font(font_name, 40)  # время
        text_surface = font.render((str(datetime.datetime.now() - initial_time))[2:7], True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (588, 340)
        sc.blit(text_surface, text_rect)

        pygame.display.update()  # обновил дисплей

        # ЗАПУСТИЛ ФИНАЛЬНОЕ МЕНЮ
        while show:
            for event_1 in pygame.event.get():
                if event_1.type == pygame.QUIT:
                    sys.exit()
                if event_1.type == pygame.KEYDOWN:
                    if event_1.key == pygame.K_ESCAPE:
                        show = False

    # ОБЪЕКТ ГРАНИЦА СТНЕЫ
    class Wall_border(pygame.sprite.Sprite):
        def __init__(self, x, y, filename):
            super().__init__(wall_border_group, all_sprites)
            self.image = pygame.image.load(os.path.join('data', filename)).convert_alpha()
            self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)

    # ОБЪЕКТ КАРТИНКА
    class Picture(pygame.sprite.Sprite):
        def __init__(self, x, y, filename):
            super().__init__(picture_group, all_sprites)
            self.image = pygame.image.load(os.path.join('data', filename)).convert_alpha()
            self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)

    # ОБЪЕКТ СТЕНА
    class Wall(pygame.sprite.Sprite):
        def __init__(self, x, y, filename):
            super().__init__(wall_group, all_sprites)
            self.image = pygame.image.load(os.path.join('data', filename)).convert_alpha()
            self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)

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
            # ПОЗИЦИЯ ОТНОСИТЕЛЬНА КАРТЫ

            # актуальная
            self.x_map_player = 1
            self.y_map_player = 1

            # предидущая
            self.x_last = 1
            self.y_last = 1

    # ОБЪЕКТ ПРОТИВНИК
    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y, filename):
            pygame.sprite.Sprite.__init__(self, mobs_group, all_sprites)
            self.image = pygame.image.load(os.path.join('data', filename)).convert_alpha()
            self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)
            # ПОЗИЦИЯ ОТНОСИТЕЛЬНА КАРТЫ
            self.x_map_enemy = 1
            self.y_map_enemy = 1

        def animation(self):  # анимация ходьбы
            if not pygame.sprite.spritecollide(opponent, obstacle_group, False):  # не столкнулся ли с ящиком
                if self.rect.x < player.rect.x:  # если цель справа
                    self.image = walk_right_enemy[animation_enemy % quantity_images_enemy]
                elif self.rect.x > player.rect.x:  # если цель слева
                    self.image = walk_left_enemy[animation_enemy % quantity_images_enemy]
                else:
                    pass

        def update(self):  # перемещение противника на карте
            if self.rect.x not in range(player.rect.x - 2, player.rect.x + 2):
                if pygame.sprite.spritecollide(opponent, obstacle_group, False):  # столкновение с ящиком: True
                    if self.rect.x < player.rect.x:
                        # ИЗОБРАЖЕНИЕ
                        self.image = pygame.image.load('data/enemy_right_tackle.png').convert_alpha()

                        # ПОЗИЦИЯ
                        self.x_map_enemy += 3  # относительно карты
                        self.rect.x += 3  # относительно окна игры
                    else:
                        # ИЗОБРАЖЕНИЕ
                        self.image = pygame.image.load('data/enemy_left_tackle.png').convert_alpha()

                        # ПОЗИЦИЯ
                        self.x_map_enemy -= 3  # относительно карты
                        self.rect.x -= 3  # относительно окна игры
                else:  # столкновение с ящиком: False
                    if self.rect.x < player.rect.x:
                        # ИЗОБРАЖЕНИЕ
                        self.image = pygame.image.load('data/enemy_right.png').convert_alpha()

                        # ПОЗИЦИЯ
                        self.x_map_enemy += 2  # относительно карты
                        self.rect.x += 2  # относительно окна игры
                    else:
                        # ИЗОБРАЖЕНИЕ
                        self.image = pygame.image.load('data/enemy_left.png').convert_alpha()

                        # ПОЗИЦИЯ
                        self.x_map_enemy -= 2  # относительно карты
                        self.rect.x -= 2  # относительно окна игры
            else:
                pass

            if self.rect.y not in range(player.rect.y - 2, player.rect.y + 2):
                if pygame.sprite.spritecollide(opponent, obstacle_group, False):  # столкновение с ящиком: True
                    if self.rect.y < player.rect.y:
                        # ПОЗИЦИЯ
                        self.y_map_enemy += 3  # относительно карты
                        self.rect.y += 3  # относительно окна игры
                    else:
                        # ПОЗИЦИЯ
                        self.y_map_enemy -= 3  # относительно карты
                        self.rect.y -= 3  # относительно окна игры
                else:  # столкновение с ящиком: False
                    if self.rect.y < player.rect.y:
                        # ПОЗИЦИЯ
                        self.y_map_enemy += 2  # относительно карты
                        self.rect.y += 2  # относительно окна игры
                    else:
                        # ПОЗИЦИЯ
                        self.y_map_enemy -= 2  # относительно карты
                        self.rect.y -= 2  # относительно окна игры
            else:
                pass

    # ОБЪЕКТ ВЫХОД
    class Exit(pygame.sprite.Sprite):
        def __init__(self, x, y, filename):
            super().__init__(all_sprites, exits_group)
            self.image = pygame.image.load(os.path.join('data', filename)).convert_alpha()
            self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)

    # ОБЪЕКТ МОНЕТА
    class Coin(pygame.sprite.Sprite):
        def __init__(self, x, y, filename):
            super().__init__(coin_group, all_sprites)
            self.image = pygame.image.load(os.path.join('data', filename)).convert_alpha()
            self.rect = self.image.get_rect().move(x, y)


    # ГРУППЫ СПРАЙТОВ
    picture_group = pygame.sprite.Group()  # picture
    wall_border_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()  # wall
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

    show_menu()

    # СОЗДАНИЕ СПРАЙТОВ
    wall_top = Wall(12.7, 0.9, 'wall_top_2.png')  # верхняя стена
    exit_door_border = Wall_border(12.7, 3, 'wall_top_border.png')  # граница верхней стены

    wall_right = Wall_border(11.7, 0.9, 'wall_right.png')  # правая стена
    wall_left = Wall_border(90.7, 0.9, 'wall_right.png')  # левая стена
    wall_bot = Wall_border(12.7, 48.9, 'wall_bot.png')  # нижняя стена

    for i in range(5):  # генерация монеток
        money = Coin(random.randint(630, 3650), random.randint(200, 2300), 'money.png')
        while pygame.sprite.spritecollide(money, obstacle_group, True):
            money = Coin(random.randint(630, 3650), random.randint(200, 2300), 'money.png')

    for i in range(50):  # генерация ящиков
        n = random.randint(1, 3)
        if n == 1:
            obstacle = Obstacle(random.randint(14, 85), random.randint(8, 47), 'obstacle_2_2.png')
        else:
            obstacle = Obstacle(random.randint(14, 85), random.randint(8, 47), 'obstacle_2.png')

    player = Player(30, 15, 'character_right.png')  # создание главного героя
    if pygame.sprite.spritecollide(player, obstacle_group, False):  # заспавнился ли игрок в ящике
        while pygame.sprite.spritecollide(player, obstacle_group, False):
            new_x = random.randint(100, 500)  # новый x
            new_y = random.randint(100, 300)  # новый y

            player.rect.x += new_x
            player.rect.y += new_y

    opponent = Enemy(random.randint(14, 80), random.randint(8, 25), 'enemy_left.png')  # создание врага

    x_exit = random.randint(15, 85)  # x выхода 1
    exit_1 = Exit(x_exit + 0.35, 3.2, 'door_exit_tablet.png')  # выход 1
    exit_door = Picture(x_exit, 2.3, 'door_exit.png')  # дверь выхода 1

    camera = Camera()  # создал камеру

    # НАЧАЛО ПРОГРАММЫ
    if __name__ == '__main__':
        pygame.init()
        level_x, level_y = generate_level(load_level('map.txt'))
        keys = pygame.key.get_pressed()

        # ПАРАМЕТРЫ АНИМАЦИИ ПЕРСООНАЖЕЙ

        # персоонаж
        quantity_images = 4  # количество картинок
        count = 0  # ход анимации
        animation = 0  # номер картинки в анимации
        speed_animation = 6  # скорость обновления картинок (чем больше тем медленнее)

        walk_right = [pygame.transform.scale(pygame.image.load(f'data/walk/character_walk_{i}.png'),
                                             (76, 86)) for i in range(quantity_images)]  # список картинок

        walk_left = [pygame.transform.flip(walk_right[i], True, False) for i in range(quantity_images)]

        # противник
        quantity_images_enemy = 4  # количество картинок
        count_enemy = 0  # ход анимации
        animation_enemy = 0  # номер картинки в анимации
        speed_animation_enemy = 10  # скорость обновления картинок (чем больше тем медленнее)

        walk_right_enemy = [pygame.transform.scale(pygame.image.load(f'data/walk_enemy/enemy_walk_{i}.png'),
                                                   (76, 86)) for i in range(quantity_images_enemy)]  # список картинок

        walk_left_enemy = [pygame.transform.flip(walk_right_enemy[i], True, False)
                           for i in range(quantity_images_enemy)]

        # НАЧАЛО ВРЕМЕНИ
        start_time = datetime.datetime.now()

        # МУЗЫКА
        pygame.mixer.music.load('data/music.mp3')  # музыка
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(15)

        # НАЧАЛО ОСНОВНОГО ЦИКЛА ПРОГРАММЫ
        run = True
        while run:
            # ОБНАРУЖЕНИЕ ИВЕНТОВ PYGAME
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_o:  # вид интерфейса
                        counter_interface += 1
                    if event.key == pygame.K_MINUS:  # нажатие "-" ставит музыку на паузу
                        pygame.mixer.music.pause()
                    if event.key == pygame.K_EQUALS:  # нажатие "=" продолжает играть музыка
                        pygame.mixer.music.unpause()
                    if event.key == pygame.K_h:  # помощь
                        score = 5

            # ОБНАРУЖЕНИЕ СТОЛКНОВЕНИЙ
            if pygame.sprite.spritecollide(player, wall_border_group, False):  # персоонаж
                player.rect.x += (player.x_last - player.x_map_player)
                player.rect.y += (player.y_last - player.y_map_player)

            if pygame.sprite.spritecollide(player, obstacle_group, False):  # персоонаж
                player.rect.x += (player.x_last - player.x_map_player)
                player.rect.y += (player.y_last - player.y_map_player)

            player.x_last = player.x_map_player  # x персоонажа до столкновения
            player.y_last = player.y_map_player  # y персоонажа до столкновения

            # ПРОВЕРКИ РАЗНЫХ СОБЫТИЙ ВНУТРИ ИГРЫ
            if pygame.sprite.spritecollide(player, coin_group, True):  # начисление счёта за нахождение монетки
                score += 1

            # ОБНОВЛЕНИЕ КАМЕРЫ
            camera.update(player)  # сама камера

            for sprite in all_sprites:  # остальные спрайты
                camera.apply(sprite)

            # ОТРИСОВАКА ВСЕХ СПРАЙТОВ НА ЭКРАНЕ
            draw_sprite_group()  # отрисовка спрайтов
            display_interface(counter_interface)  # отрисовка интерфейса

            # КАКИЕ-ТО ВАЖНЫЙ ШТУКИ
            pygame.display.flip()  # флип
            keys = pygame.key.get_pressed()  # список нажимаемых клавишь

            # ПЕРЕМЕЩЕНИЕ СУЩНОСТЕЙ
            opponent.update()  # враг

            opponent.animation()
            if count_enemy == speed_animation_enemy:
                animation_enemy += 1
                count_enemy = 0
            count_enemy += 1

            if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:  # игрок
                side_character = 'r'
                player.image = walk_right[animation % quantity_images]

                player.y_map_player -= 3
                player.x_map_player += 3

                player.rect.y -= 3
                player.rect.x += 3

                if count == speed_animation:
                    animation += 1
                    count = 0
                count += 1

            elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
                side_character = 'l'
                player.image = walk_left[animation % quantity_images]

                player.y_map_player -= 3
                player.x_map_player -= 3

                player.rect.y -= 3
                player.rect.x -= 3

                if count == speed_animation:
                    animation += 1
                    count = 0
                count += 1

            elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
                side_character = 'r'
                player.image = walk_right[animation % quantity_images]

                player.y_map_player += 3
                player.x_map_player += 3

                player.rect.y += 3
                player.rect.x += 3

                if count == speed_animation:
                    animation += 1
                    count = 0
                count += 1

            elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
                side_character = 'l'
                player.image = walk_left[animation % quantity_images]

                player.y_map_player += 3
                player.x_map_player -= 3

                player.rect.y += 3
                player.rect.x -= 3

                if count == speed_animation:
                    animation += 1
                    count = 0
                count += 1

            elif keys[pygame.K_LEFT]:
                side_character = 'l'
                player.image = walk_left[animation % quantity_images]

                player.x_map_player -= 3
                player.rect.x -= 3

                if count == speed_animation:
                    animation += 1
                    count = 0
                count += 1

            elif keys[pygame.K_RIGHT]:
                side_character = 'r'
                player.image = walk_right[animation % quantity_images]

                player.x_map_player += 3
                player.rect.x += 3

                if count == speed_animation:
                    animation += 1
                    count = 0
                count += 1

            elif keys[pygame.K_DOWN]:
                if side_character == 'r':
                    player.image = walk_right[animation % quantity_images]
                else:
                    player.image = walk_left[animation % quantity_images]

                player.y_map_player += 3
                player.rect.y += 3

                if count == speed_animation:
                    animation += 1
                    count = 0
                count += 1

            elif keys[pygame.K_UP]:
                if side_character == 'r':
                    player.image = walk_right[animation % quantity_images]
                else:
                    player.image = walk_left[animation % quantity_images]

                player.y_map_player -= 3
                player.rect.y -= 3

                if count == speed_animation:
                    animation += 1
                    count = 0
                count += 1

            else:
                if side_character == 'r':
                    player.image = walk_right[0]
                else:
                    player.image = walk_left[0]

            end_game()  # проверка окончания игры

            clock.tick(FPS)  # опять часы
