import tkinter
import pygame
import os, sys
import threading
import configparser
import ctypes
import random
import time
import fuckit

from tkinter import filedialog as fd


# --- variables ---
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

online = False

filename = 'Nothing Loaded'

parser = configparser.ConfigParser()
parser.read(root_dir + r'\configuration.cfg')



# --- initialization ---
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()


# screen
screen = pygame.display.set_mode((600, 300))
caption = pygame.display.set_caption('Vibe Looper')
icon = pygame.display.set_icon(pygame.image.load(root_dir + r'\icon.png'))



# --- functions ---
def select_file():
    def thread():

        TKwindow = tkinter.Tk()
        TKwindow.withdraw()

        filetypes = (
            ('.mp3', '*.mp3'),
            ('.wav', '*.wav'),
            ('All Files', '*.*'),
        )

        global filename
        filename = fd.askopenfilename(title='Please select a file', filetypes=filetypes, initialdir=root_dir + r'\local_music')
        try:
            pygame.mixer.music.load(filename)
            global song_text_pos
            song_text_pos = 15, 30
        except:
            pass

        TKwindow.destroy()
        TKwindow.mainloop()

    threading.Thread(target=(thread)).start()

def play():
    def thread():
        if online == False:

            try:
                pygame.mixer.music.play(-1)
                pygame.mixer.music
            except:
                ctypes.windll.user32.MessageBoxW(0, 'Failed to play music. Maybe try importing it first?', 'Sorry')
        
        elif online == True:
            ctypes.windll.user32.MessageBoxW(0, 'Online mode not working right now', 'Sorry')

    threading.Thread(target=(thread)).start()

def stop():
    pygame.mixer.music.stop()

def go_online():
    global online
    online = True

    while online:
        screen.fill('white')


        #HERE


        pygame.display.update()


# main loop
running = True
while running:

    #### BACKGROUND ###################################################################
    try:
        background = pygame.image.load(parser.get('general', 'custom_bg'))
    except:
        background = pygame.image.load(root_dir + r'\background.png').convert()
        background = pygame.transform.scale(background, (600, 300))

    screen.blit(background, (0, 0))
    ###################################################################################


    # --- blitting and drawing ---
    class play_button():
        font = pygame.font.SysFont('calibri bold', 40)
        text = font.render('Play', True, [0, 0, 0])

        pos = 320, 250
        geo = 70, 40

        rectangle = pygame.Rect(pos, geo)
        pygame.draw.rect(screen, [255, 255, 255], rectangle)

        screen.blit(text, (325, 258))

        # mouse hover
        if rectangle.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, [240, 240, 240], rectangle)

            text = font.render('Play', True, [250, 125, 57])
            screen.blit(text, (325, 258))
    class stop_button():
        font = pygame.font.SysFont('calibri bold', 40)
        text = font.render('Stop', True, [0, 0, 0])

        pos = 220, 250
        geo = 70, 40

        rectangle = pygame.Rect(pos, geo)
        pygame.draw.rect(screen, [255, 255, 255], rectangle)

        screen.blit(text, (225, 258))

        # mouse hover
        if rectangle.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, [240, 240, 240], rectangle)

            text = font.render('Stop', True, [250, 125, 57])
            screen.blit(text, (225, 258))
    class import_button():
        font = pygame.font.SysFont('calibri bold', 20)
        text = font.render('Import', True, [0, 0, 0])

        pos = 0, 0
        geo = 50, 15

        rectangle = pygame.Rect(pos, geo)
        pygame.draw.rect(screen, [255, 255, 255], rectangle)

        screen.blit(text, (4, 0))

        # mouse hover
        if rectangle.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, [240, 240, 240], rectangle)

            text = font.render('Import', True, [255, 0, 0])
            screen.blit(text, (4, 0))
    class online_button():
        font = pygame.font.SysFont('calibri bold', 20)
        text = font.render('Online', True, [0, 0, 0])

        pos = 50, 0
        geo = 50, 15

        rectangle = pygame.Rect(pos, geo)
        pygame.draw.rect(screen, [255, 255, 255], rectangle)

        screen.blit(text, (54, 0))

        # mouse hover
        if rectangle.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, [240, 240, 240], rectangle)

            text = font.render('Online', True, 'blue violet')
            screen.blit(text, (54, 0))
    class song_display():
        font = pygame.font.SysFont('cosmic sans ms', 20)
        text = font.render(os.path.basename(filename), True, [0, 0, 0])

        pos = 10, 27.5
        geo = 580, 20

        rectangle = pygame.Rect(pos, geo)
        pygame.draw.rect(screen, [0, 0, 0], rectangle, 1)

        screen.blit(text, (250, 30))



    # main event check
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if play_button.rectangle.collidepoint(pygame.mouse.get_pos()):
                play()
            
            if import_button.rectangle.collidepoint(pygame.mouse.get_pos()):
                select_file()
            
            if stop_button.rectangle.collidepoint(pygame.mouse.get_pos()):
                stop()
            
            if online_button.rectangle.collidepoint(pygame.mouse.get_pos()):
                go_online()


    clock.tick(120)
    pygame.display.update()