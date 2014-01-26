'''

GGJ GMU 2014, Candy Herder / Crushing Candy into Jam Team
Nathan McClain
Brendon Fuhs
David Masad



'''

# import pygame._view ## Necessary to make an exe with this?

import random as rnd
import sys

from pygame import *
from game import Game
from menu import Menu, SplashScreen

def game_loop(game):
    '''
    Run a main loop using the game object
    '''

    # get all mouse clicks and pygame events
    already_got_click = False # I'm only going to get one mouse click
    for ev in event.get():
        # If the mouse was clicked, find who it was clicked on
        if ev.type == MOUSEBUTTONUP and already_got_click == False:
            already_got_click = True
            mouse_pos = mouse.get_pos()
            for game_object in game.game_objects.values(): 
                game_object.check_click(mouse_pos)    
        if ev.type == QUIT:
            return False
        # Any key brinsg up the Pause menu
        if ev.type == KEYDOWN: # should get any key I think
            #menu = Menu(screen)
            menu = SplashScreen(screen, "graphics/splashes/Pause-Screen.png")
            menu.menu_loop()
            #while menu_loop(menu):
            #    deltat = clock.tick(FPS) # or something like this
    
    # progress internal event queues for all objects
    dead_object_idents = []
    mouse_pos = mouse.get_pos()
    for game_object in game.game_objects.values():
        object_status = game_object.update_and_get_status(mouse_pos)
        if object_status == "dead":
            dead_object_idents.append(game_object.ident)
    for spatter in game.spatter_list:
        spatter_status = spatter.update_status()
        if spatter_status == False: # (dead)
            game.spatter_list.remove(spatter)
            del spatter
            
    # remove dead game objects and create splatters
    for ident in dead_object_idents:
        game.create_spatter(game.game_objects[ident].get_pos())
        del game.game_objects[ident]
        
    game.check_spawn() # Randomly spawn more candies

    # redraw and display everything
    screen.blit(background, (0,0))
    for spatter in game.spatter_list:
        spatter.blit(screen)
    for game_object in game.game_objects.values():
        game_object.blit(screen)
    
    screen.blit(game.scorekeeper.draw_beaker(), (1100, 0))
    
    display.flip()
    return True

if __name__ == "__main__":

    # start pygame mixer
    mixer.pre_init()
    #mixer.pre_init(frequency=22050, size=-8, channels=2, buffer=2048)
    # frequency=22050, size=-16, channels=2, buffersize=4096

    # start pygame
    init()
    
    # Create things you want in the global scope
    game = Game()
    screen = display.set_mode((game.DISPLAY_SIZE[0] + 100, game.DISPLAY_SIZE[1]))
    game.screen = screen
    background = Surface(game.DISPLAY_SIZE, SRCALPHA)
    background.fill(game.BACKGROUND_COLOR)
    bg_image = image.load("graphics/Game-Board.png").convert()
    background.blit(bg_image, (0,0))
    background.blit(bg_image, (800,0))
    display.set_caption(game.GAME_TITLE)
    splash = SplashScreen(screen, "graphics/splashes/Cover3.png")
    splash.menu_loop()

    menu = SplashScreen(screen, "graphics/splashes/Open-Text.png")
    menu.menu_loop()


    #game_objects = {}
    # all game objects need
    #   ident
    #   check_click method
    #   update_and_get_status method
    #   blit method    
    game.initialize()
    clock = time.Clock()
    FPS = 60
    while game_loop(game):
        deltat = clock.tick(FPS)

