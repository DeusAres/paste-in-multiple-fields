import time

from pynput.keyboard import Key, Controller
from pynput import keyboard
from pyperclip import copy

import PySimpleGUI as sg

def main():
    layout =  [
        [sg.Text('Number of fields'), sg.Input(key='N')],
        [sg.Button('OK')]
    ]
    window = sg.Window('Fields', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'OK':
            window.close()
            break

    if event == 'OK':
        paster(int(values['N'])+1)


def paster(N):
    layout = [
        [[sg.Text(f'Field {i}'), sg.Multiline(key=f'field{i}')] for i in range(1, N, 1)],
        [sg.Text('Press "-" to paste and tab, Esc to stop'), sg.Push(), sg.Button('Start'), sg.Button('Stop', disabled=True)]
    ]

    window = sg.Window(f'{N-1} times paster', layout)

    while True:
        event, values = window.read(1000)
        #on_press_func = lambda key: on_press(key, values)
        if event == sg.WINDOW_CLOSED:
            break
        
        def pasteDatas():
            datas = [values[f'field{i}'].strip('\n') for i in range(1, N, 1)]
            index = 0
            keyboard = Controller()
            for i in range(index, 3, 1):
                with keyboard.pressed(Key.ctrl):
                    keyboard.press('a')
                keyboard.release('a')
                copy(datas[index])
                time.sleep(0.5)
                
                with keyboard.pressed(Key.ctrl):
                    keyboard.press('v')
                keyboard.release('v')

                time.sleep(0.5)

                keyboard.press(Key.tab)
                keyboard.release(Key.tab)

                index += 1
                if index >= len(datas):     
                    index = len(datas) - 1

        def on_press(key):

            if key == keyboard.Key.esc:
                return False  # stop listener
            try:
                k = key.char  # single-char keys
            except:
                k = key.name  # other keys

            if k in ['-']:
                index = pasteDatas()
                return index

        if event == 'Start':
            listener = keyboard.Listener(on_press=on_press)
            listener.start()
            window['Start'].Update(disabled=True)
            window['Stop'].Update(disabled=False)

        try:
            if event == 'Stop' or not listener.is_alive():
                if event == 'Stop':
                    listener.stop()
                window['Start'].Update(disabled=False)
                window['Stop'].Update(disabled=True)
        except:
            pass

    window.close()

if __name__ == '__main__':
    main()