import random
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'   # отключает приветствие от создателей пайгейма
import pygame
import pygame.freetype              # использование других шрифтов
import json
import tfg
from win32api import GetSystemMetrics
from tkinter import *
from tkinter import ttk
from game import main

def first_menu_function():
    difficulty_list = ['Легко', 'Средняя сложность', 'Pro уровень']
    computer_performance_list = ['Низкие', 'Средние', 'Высокие']

    root = Tk()

    def btn_confirm_function():
        difficulty_transport_dictionary = {difficulty_list[0]: 0, difficulty_list[1]: 1, difficulty_list[2]: 2}
        computer_performance_transport_dictionary = {computer_performance_list[0]: 0, computer_performance_list[1]: 1, computer_performance_list[2]: 2}
        difficulty = difficulty_list_vidget.get()
        computer_performance = computer_performance_list_vidget.get()
        # print(difficulty_transport_dictionary[difficulty], computer_performance_transport_dictionary[computer_performance])
        return difficulty_transport_dictionary[difficulty], computer_performance_transport_dictionary[computer_performance]

    # exec(open('game.pyw').read())

    root.minsize(300, 400)
    root['bg'] = 'White'
    root.title('Game menu')
    root.wm_attributes('-alpha', 1)
    root.geometry('300x400')

    title = Label(root, text='Free to play Game', bg='white', font='Times 25')
    title.place(relx=.5, rely=.15, anchor='center')

    difficulty_text = Label(root, text='Выберите сложность: ', bg='white', font='Times 16')
    difficulty_text.place(relx=.5, rely=.3, anchor='center')

    difficulty_list_vidget = ttk.Combobox(values=difficulty_list)
    difficulty_list_vidget.place(width = 200, relx=.5, rely=.40, anchor='center')
    difficulty_list_vidget.current(1)

    computer_performance_text = Label(root, text='Выберите настройки\nграфики: ', bg='white', font='Times 16')
    computer_performance_text.place(relx=.5, rely=.55, anchor='center')

    computer_performance_list_vidget = ttk.Combobox(values=computer_performance_list)
    computer_performance_list_vidget.place(width = 200, relx=.5, rely=.67, anchor='center')
    computer_performance_list_vidget.current(2)

    btn_confirm = Button(root, text = 'Подтвердить', bg = '#ff1400', command = btn_confirm_function, font = 'Times 18')
    btn_confirm.place(relx=0.5, rely=0.85, anchor='center')

    root.mainloop()