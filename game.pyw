import random
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'   # отключает приветствие от создателей пайгейма
import pygame
import pygame.freetype              # использование других шрифтов
import json
import tfg
from win32api import GetSystemMetrics


pygame.init()  # инициализация пайгейма

pygame.font.init()

width, height = GetSystemMetrics(0), GetSystemMetrics(1)    # 924, 693; 1366, 768; 1920, 1080
size_py = (width, height)
screen = pygame.display.set_mode(size_py, pygame.FULLSCREEN)
clock = pygame.time.Clock()
f1 = pygame.font.Font("Cony Light.otf", 21)
f2 = pygame.font.Font("Cony Light.otf", 16)
font = pygame.freetype.Font("Cony Light.otf", 20)

fps = 60
move = 11  # ширина клетки

week = 1
month = 1
year = 0
map_arr = []
lx, ly = 0, 0           # округленные координаты
x_cap, y_cap = 0, 0            # координаты левого верхнего угла на поле работ
menu = 0  # выделенное меню
index = 0  # не помню что это
inf_pos = 0  # не помню что это
zone = True  # наличие курсора в зоне карты
lb = False  # не помню, вроде бесполезная херня
rb_info = False  # нажатие ПКМ


def menu_num():  # обработка меню выбора
    global menu
    if event.pos[1] < 44:
        if event.pos[0] < 44:
            menu = 0
        elif 44 <= event.pos[0] < 88:
            menu = 1
        elif 88 <= event.pos[0] < 132:
            menu = 2
        elif 132 <= event.pos[0] < 176:
            menu = 3
        elif 176 <= event.pos[0] < 220:
            menu = 4
        elif 220 <= event.pos[0] < 264:
            menu = 5
        elif 264 <= event.pos[0] < 308:
            menu = 6
        elif width - 90 <= event.pos[0] < width - 46:  # -90 = 2 * 44 - 2; -47 = - 44 - 2
            menu = 29
        elif width - 46 <= event.pos[0] < width - 2:  # -46 = - 44 - 2; -3 =  - 2
            global run
            run = False


def add():  # добавление на карту зданий
    global menu
    if zone:
        jj = int(lx / move)      # Номер клеточки в горизонтальном ряду
        ii = int(ly / move) - 4     # Номер клеточки в вертикальнои ряду (с учетом меню)
        if menu == 0 and map_arr[ii][jj] == 0:
            map_arr[ii][jj] = 8
        elif menu == 1 and map_arr[ii][jj] == 0:
            map_arr[ii][jj] = 9
        elif menu == 2 and map_arr[ii][jj] == 0:
            map_arr[ii][jj] = 10
        elif menu == 3 and map_arr[ii][jj] == 0:
            map_arr[ii][jj] = 11
        elif menu == 4 and (7 >= map_arr[ii][jj] > 0):
            map_arr[ii][jj] = 12
        elif menu == 5 and map_arr[ii][jj] == 0:
            map_arr[ii][jj] = 14
        elif menu == 6 and map_arr[ii][jj] == 0:
            map_arr[ii][jj] = 15
        elif menu == 29 and (12 >= map_arr[ii][jj] >= 8):
            map_arr[ii][jj] = 0


def greed():
    """отрисовка сетки мира"""
    for xg in range(0, width, move):
        pygame.draw.aaline(screen, pygame.Color("gray"), (xg, move * 4), (xg, height))  # вертикальные полосы
    for yg in range(move * 4, height, move):
        pygame.draw.aaline(screen, pygame.Color("gray"), (0, yg), (width, yg))  # горизонтальные полосы
    pygame.draw.aaline(screen, pygame.Color("dimgray"), (0, 44), (width, 44),
                       1)  # верхняя темная линия (под меню выбора)


def mouse_rect(mx, my):
    """квадрат, котрый занимает курсор"""
    if zone:
        pygame.draw.rect(screen, pygame.Color("dimgray"), (mx, my, move + 1, move + 1), 1)  # dimgray


def gui():
    """ интерфейс, его отрисовка"""
    screen.blit(menu_surf, (0, 0))
    screen.blit(delete, (width - 90, 0))  # width - 88 - 2
    screen.blit(esc_surf, (width - 46, 0))  # width - 44 - 2
    screen.blit(rec, (menu * 44, 0))
    date = f2.render(f"Неделя: {week}/{month}", True, pygame.Color("black"))
    d_year = f2.render(f"Месяц: {year}", True, pygame.Color("black"))
    screen.blit(date, (width - 160, 5))
    screen.blit(d_year, (width - 160, 25))


def word_wrap(surf, text, fon, color=pygame.Color("dimgray")):              # разбивает одну строку на нескоько чтобы поместилось в окно, вызываемое на ПКМ
    fon.origin = True
    words = text.split(' ')
    wid, heig = surf.get_size()     # 264, 308 (ширина, высота), эти значения на всякий случай, размер окна, вызываемого на ПКМ
    line_spacing = fon.get_sized_height() + 2
    x, y = 1127, 63 + line_spacing
    space = fon.get_rect(' ')
    for word in words:
        bounds = fon.get_rect(word)
        if x + bounds.width + bounds.x >= wid:
            x, y = 1117, y + line_spacing
        if x + bounds.width + bounds.x >= wid:
            raise ValueError("word too wide for the surface")
        if y + bounds.height - bounds.y >= heig:
            raise ValueError("text to long for the surface")
        fon.render_to(surf, (x, y), None, color)
        x += bounds.width + space.width
    return x, y


def info(inf, n_txt):               # меню вызываемое на ПКМ
    if inf:
        pygame.draw.rect(screen, pygame.Color("white"), (width - 255, 44, 254, 308))
        pygame.draw.rect(screen, pygame.Color("dimgray"), (width - 255, 44, 254, 308), 2)
        txt = f1.render(str(tfg.text[n_txt]), True, pygame.Color("dimgray"))
        screen.blit(txt, (width - 154, height - 721))
        txt1 = str(tfg.inf_tx[n_txt])
        word_wrap(screen, txt1, font)


while y_cap < 43:
    x_cap = random.randint(0, width - move * 5)
    y_cap = random.randint(move * 5, height - move * 5)
    x_cap = x_cap - (x_cap % move) - 1
    y_cap = y_cap - (y_cap % move) - 1


tx = int(width / move)              # определение колличества клеток по оси Х
ty = int((height - move * 4) / move)             # определение колличества клеток по оси У
for i in range(ty):                 # заполнение массива карты
    map_arr.append([])
    fir_count = 0
    sw = 0
    for j in range(tx):
        c = random.randint(0, 400)
        if 50 >= c >= 45:
            map_arr[i].append(1)        # Уголь
        elif c == 1:
            map_arr[i].append(2)        # Медь
        elif c == 2 and fir_count < 10:
            map_arr[i].append(3)        # Фируз
            fir_count += 1
        elif c == 3:
            map_arr[i].append(4)        # Золото
        elif c == 4:
            map_arr[i].append(5)        # Железо
        elif c == 5 and sw < 4:
            map_arr[i].append(6)        # Болотный камень
            sw += 1
        elif c == 6:
            map_arr[i].append(7)        # Олово
        elif 13 <= c <= 33:
            map_arr[i].append(13)       # Дерево
        else:
            map_arr[i].append(0)        # Пустое поле

with open('seed.txt', 'w') as fw:
    json.dump(map_arr, fw)

"""Копирование изображений в ОЗУ и присваивание им названий"""
""" Ресурсы"""
coal = pygame.image.load("resources/Coal.png")
copper = pygame.image.load("resources/Copper ore.png")
firuz = pygame.image.load("resources/Firuz.png")
gold = pygame.image.load("resources/Gold ore.png")
iron = pygame.image.load("resources/Iron ore.png")
swamp_st = pygame.image.load("resources/Swamp stone.png")
tin = pygame.image.load("resources/Tin ore.png")
tree = pygame.image.load("resources/tree.png")

"""Постройки"""
farm_surf = pygame.image.load("buildings/farm.png")
fac_surf = pygame.image.load("buildings/factory.png")
lab_surf = pygame.image.load("buildings/laboratory.png")
home_surf = pygame.image.load("buildings/home.png")
mine_surf = pygame.image.load("buildings/mine.png")
storage_surf = pygame.image.load("buildings/storage.png")
sawmill_surf = pygame.image.load("buildings/sawmill.png")

"""GUI"""
menu_surf = pygame.image.load("GUI/menu.png")
esc_surf = pygame.image.load("GUI/esc.png")
rec = pygame.image.load("GUI/yrect.png")
delete = pygame.image.load("GUI/trash.png")

run = True
while run:

    events = pygame.event.get()         # кортеж событий
    for event in events:
        if event.type == pygame.QUIT:       # событие нажатия крестика выхода
            run = False
        elif event.type == pygame.MOUSEMOTION:              # обработка движения мыши
            lx = event.pos[0] - (event.pos[0] % move)           # как я и обьяснял, вычисления координаты ячейки по оси Х (верхняя левая тчк квадратика)
            ly = event.pos[1] - (event.pos[1] % move)           # ровно то же, но и осью У
            if ly > 43:             # чтобы выделенный квадрат, который следует за курсором не залазил на менюшку
                zone = True
            else:
                zone = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # нажатие ЛКМ pygame.MOUSEBUTTONDOWN - событие нажатия клавиши, event.button == 1 - клавиша ЛКМ
            lb = True
            menu_num()      #
            if x_cap < event.pos[0] < x_cap + move * 5 + 1 and y_cap < event.pos[1] < y_cap + move * 5 + 1:         # курсор внутри красного квадрата
                add()         # вызов функции
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:        # проверка нажатия ПКМ
            rb_info = not rb_info               # включение меню
            inf_pos = map_arr[int(ly / move) - 4][int(lx / move)]       # запоминание ячейки, о которой нужно показать информацию

    keys = pygame.key.get_pressed()         # кортеж нажатых клавиш
    if keys[pygame.K_1]:        # если нажата клавиша 1 то выбано на панеле соответствующее значение
        menu = 0
    if keys[pygame.K_2]:
        menu = 1
    if keys[pygame.K_3]:
        menu = 2
    if keys[pygame.K_4]:
        menu = 3
    if keys[pygame.K_5]:
        menu = 4
    if keys[pygame.K_6]:
        menu = 5
    if keys[pygame.K_DELETE]:
        menu = 29
    if keys[pygame.K_ESCAPE]:
        run = False

    screen.fill(pygame.Color('white'))              # заполнения экрана белым
    greed()             # отрисовка сетки
    gui()               # менюшка

    for i in range(ty):                 # отрисовка значков на карте
        for j in range(tx):
            if map_arr[i][j] == 1:
                """отрисовка угля"""
                screen.blit(coal, (j * move, (i + 4) * move))
            elif map_arr[i][j] == 2:
                """отрисовка меди"""
                screen.blit(copper, (j * move, (i + 4) * move))
            elif map_arr[i][j] == 3:
                """отрисовка фируза"""
                screen.blit(firuz, (j * move, (i + 4) * move))
            elif map_arr[i][j] == 4:
                """отрисовка золота"""
                screen.blit(gold, (j * move, (i + 4) * move))
            elif map_arr[i][j] == 5:
                """отрисовка железа"""
                screen.blit(iron, (j * move, (i + 4) * move))
            elif map_arr[i][j] == 6:
                """отрисовка болотного камня"""
                screen.blit(swamp_st, (j * move, (i + 4) * move))
            elif map_arr[i][j] == 7:
                """отрисовка олова"""
                screen.blit(tin, (j * move, (i + 4) * move))
            elif map_arr[i][j] == 8:
                """отрисовка фермы"""
                screen.blit(farm_surf, (j * move, (i + 4) * move))
            elif map_arr[i][j] == 9:
                """отрисовка завода"""
                screen.blit(fac_surf, (j * move, (i + 4) * move))
            elif map_arr[i][j] == 10:
                """отрисовка лаборатории"""
                screen.blit(lab_surf, (j * move, (i + 4) * move))
            elif map_arr[i][j] == 11:
                """отрисовка дома"""
                screen.blit(home_surf, (j * move, (i + 4) * move))
            elif map_arr[i][j] == 12:
                """отрисовка шахты"""
                screen.blit(mine_surf, (j * move, (i + 4) * move))
            elif map_arr[i][j] == 13:
                """отрисовка дерева"""
                screen.blit(tree, (j * move, (i + 4) * move))
            elif map_arr[i][j] == 14:
                """отрисовка склада"""
                screen.blit(storage_surf, (j * move, (i + 4) * move))
            elif map_arr[i][j] == 15:
                """отрисовка лесопилки"""
                screen.blit(sawmill_surf, (j * move, (i + 4) * move))

    mouse_rect(lx, ly)
    pygame.draw.rect(screen, pygame.Color("red"), (x_cap, y_cap, move * 5 + 3, move * 5 + 3), 1)        # красный квадрат

    info(rb_info, inf_pos)

    clock.tick(fps)       # задержка на 1/fps секунды
    pygame.display.flip()           # обновление экрана

pygame.quit()           # выход из пайгейма
