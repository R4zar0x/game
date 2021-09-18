import random
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import pygame.freetype
import json
import tfg

pygame.init()

pygame.font.init()
width, height = 1366, 768  # 924, 693; 1366, 768; 1920, 1080
size_py = (width, height)
screen = pygame.display.set_mode(size_py, pygame.FULLSCREEN)
clock = pygame.time.Clock()
f1 = pygame.font.Font("Cony Light.otf", 21)               # Cony Light.otf; Caviar Dreams.ttf
font = pygame.freetype.Font("Cony Light.otf", 20)

fps = 60
move = 11

map_arr = []
lx, ly = 0, 0
x_cap, y_cap = 0, 0
menu = 0
index = 0
inf_pos = 0
zone = True
lb = False
rb_info = False


def menu_num():
    global menu
    if event.pos[1] < 44:
        if event.pos[0] < 44:
            menu = 0
        elif 44 < event.pos[0] < 87:
            menu = 1
        elif 88 < event.pos[0] < 131:
            menu = 2
        elif 132 < event.pos[0] < 175:
            menu = 3
        elif 176 < event.pos[0] < 219:
            menu = 4
        elif width - 90 < event.pos[0] < width - 47:  # -90 = 2 * 44 - 2; -47 = - 44 - 2 - 1
            menu = 29
        elif width - 46 < event.pos[0] < width - 3:  # -46 = - 44 - 2; -3 =  - 2 - 1
            global run
            run = False


def add():
    global menu
    if zone:
        jj = int(lx / move)
        ii = int(ly / move) - 4
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
        elif menu == 29 and (12 >= map_arr[ii][jj] >= 8):
            map_arr[ii][jj] = 0


def greed():
    """отрисовка сетки мира"""
    for xg in range(0, width, move):
        pygame.draw.aaline(screen, pygame.Color("gray"), (xg, move * 4), (xg, height))
    for yg in range(move * 4, height, move):
        pygame.draw.aaline(screen, pygame.Color("gray"), (0, yg), (width, yg))
    pygame.draw.aaline(screen, pygame.Color("dimgray"), (0, 44), (width, 44), 1)


def mouse_rect(mx, my):
    """квадрат, котрый занимает курсор"""
    if zone:
        pygame.draw.rect(screen, pygame.Color("dimgray"), (mx, my, move + 1, move + 1), 1)  # dimgray


def gui():
    """ интерфейс"""
    screen.blit(menu_surf, (0, 0))
    screen.blit(delete, (width - 90, 0))  # width - 88 - 2
    screen.blit(esc_surf, (width - 46, 0))  # width - 44 - 2
    screen.blit(rec, (menu * 44, 0))
    # date = f1.render()


def word_wrap(surf, text, fon, color=pygame.Color("dimgray")):
    fon.origin = True
    words = text.split(' ')
    wid, heig = surf.get_size()     # 264, 308
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


def info(inf, n_txt):
    if inf:
        pygame.draw.rect(screen, pygame.Color("white"), (width - 255, height - 724, 254, 308))
        pygame.draw.rect(screen, pygame.Color("dimgray"), (width - 255, height - 724, 254, 308), 2)
        txt = f1.render(str(tfg.text[n_txt]), True, pygame.Color("dimgray"))
        screen.blit(txt, (width - 154, height - 721))
        txt1 = str(tfg.inf_tx[n_txt])
        word_wrap(screen, txt1, font)


while y_cap < 43:
    x_cap = random.randint(0, width - move * 5)
    y_cap = random.randint(move * 5, height - move * 5)
    x_cap = x_cap - (x_cap % move) - 1
    y_cap = y_cap - (y_cap % move) - 1

tx = int(width / move)
ty = int((height - move * 4) / move)
for i in range(ty):
    map_arr.append([])
    for j in range(tx):
        fir_count = 0
        sw = 0
        c = random.randint(0, 400)
        if 50 >= c >= 45:
            map_arr[i].append(1)
        elif c == 1:
            map_arr[i].append(2)
        elif c == 2 and fir_count < 10:
            map_arr[i].append(3)
            fir_count += 1
        elif c == 3:
            map_arr[i].append(4)
        elif c == 4:
            map_arr[i].append(5)
        elif c == 5 and sw < 4:
            map_arr[i].append(6)
            sw += 1
        elif c == 6:
            map_arr[i].append(7)
        elif 13 <= c <= 33:
            map_arr[i].append(13)
        else:
            map_arr[i].append(0)

with open('seed.txt', 'w') as fw:
    json.dump(pygame.font.get_fonts(), fw)

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

"""GUI"""
menu_surf = pygame.image.load("GUI/menu.png")
esc_surf = pygame.image.load("GUI/esc.png")
rec = pygame.image.load("GUI/yrect.png")
delete = pygame.image.load("GUI/trash.png")

run = True
while run:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEMOTION:
            lx = event.pos[0] - (event.pos[0] % move)
            ly = event.pos[1] - (event.pos[1] % move)
            if ly > 43:
                zone = True
            else:
                zone = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            lb = True
            menu_num()
            if x_cap < event.pos[0] < x_cap + move * 5 + 1 and y_cap < event.pos[1] < y_cap + move * 5 + 1:
                add()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            rb_info = not rb_info
            inf_pos = map_arr[int(ly / move) - 4][int(lx / move)]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        menu = 0
    if keys[pygame.K_2]:
        menu = 1
    if keys[pygame.K_3]:
        menu = 2
    if keys[pygame.K_4]:
        menu = 3
    if keys[pygame.K_5]:
        menu = 4
    if keys[pygame.K_DELETE]:
        menu = 29
    if keys[pygame.K_ESCAPE]:
        run = False

    screen.fill(pygame.Color('white'))
    greed()
    gui()

    for i in range(ty):
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

    mouse_rect(lx, ly)
    pygame.draw.rect(screen, pygame.Color("red"), (x_cap, y_cap, move * 5 + 3, move * 5 + 3), 1)

    info(rb_info, inf_pos)

    clock.tick(fps)
    pygame.display.flip()

pygame.quit()
