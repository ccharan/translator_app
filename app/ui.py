#!/usr/bin/env python
import queue
from backend import translate_text
import PySimpleGUI as sg
import threading


sg.theme('Dark')
gui_queue = queue.Queue()

languages = ('Auto', 'Bengali', 'English (UK)', 'English (US)', 'Gujarati', 'Hindi', 'Kannada', 'Malayalam', 'Marathi', 'Tamil', 'Telugu', 'Urdu')
languages_code = ('auto', 'bn', 'en-GB', 'en', 'gu', 'hi', 'kn', 'ml', 'mr', 'ta', 'te', 'ur')
dict_languages = dict(zip(languages, languages_code))


left_element = [
    [sg.Text()],
    [sg.Text("Translate From", pad=((10, 10), (0, 0)))],
    [sg.Combo(values=languages, default_value='Auto', readonly=False, k='TRANSLATE_FROM',
              expand_x=True, pad=((10, 10), (0, 0)))],
    [sg.Text()],
    [sg.Text("Enter Text", pad=((10, 10), (0, 0)))],
    [sg.Multiline(expand_y=True, expand_x=True, pad=((10, 10), (0, 0)), no_scrollbar=True, key='INPUT_TEXT')],
    [sg.Text()]
]

right_element = [
    [sg.Text()],
    [sg.Text("Translate To", pad=((10, 10), (0, 0)))],
    [sg.Combo(values=languages, default_value='Auto', readonly=False, k='TRANSLATE_TO',
              expand_x=True, pad=((10, 10), (0, 0)))],
    [sg.Text()],
    [sg.Text("Translation", pad=((10, 10), (0, 0)))],
    [sg.Multiline(expand_y=True, expand_x=True, pad=((10, 10), (0, 0)), no_scrollbar=True, key='OUTPUT_TEXT')],
    [sg.Text()]
]


layout=[[sg.Column(left_element, expand_x=True, expand_y=True), sg.Column(right_element, expand_x=True, expand_y=True)],
        [sg.Push(), sg.Button("Translate", key='TRANSLATE', expand_x=True), sg.Push()]]


window = sg.Window("Translator", layout,
                   finalize=True, size=(500, 500), resizable=True)


def long_operation_thread(source, target, text, gui_queue):
    translated_text = translate_text(source, target, text)
    window['OUTPUT_TEXT'].update(*translated_text)
    gui_queue.put(None)


while True:
    event, values = window.Read(timeout=100)
    if event == sg.WIN_CLOSED:
        break

    if event == 'TRANSLATE':
        source = dict_languages[values['TRANSLATE_FROM']]
        target = dict_languages[values['TRANSLATE_TO']]
        text = values['INPUT_TEXT']
        threading.Thread(target=long_operation_thread, args=(source, target, text, gui_queue,), daemon=True).start()
    try:
        message = gui_queue.get_nowait()
    except queue.Empty:
        message = None

    if message:
        print('Got a message back from the thread: ', message)

window.close()
