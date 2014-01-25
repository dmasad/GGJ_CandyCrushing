'''

Crushing candy into jam

'''

import random as rnd
from pygame import *
from game import Game
#from Candy import *


##### NEED SYSTEM TIME FOR ANIMATION RATE TIMING


'''
MAIN GAME LOOP
==================================================

'''

def menu_loop(): ## need to somehow stop animation clocks when this is active
    pass #######################################

def game_loop(game):
    '''
    Run a main loop using the game object
    '''

    # get all mouse clicks and pygame events
    already_got_click = False # I'm only going to get one mouse click
    for ev in event.get():
        if ev.type == MOUSEBUTTONUP and already_got_click == False:
            already_got_click = True
            mouse_pos = mouse.get_pos()
            print mouse_pos ###
            for game_object in game.game_objects.values(): 
                game_object.check_click(mouse_pos)    
        if ev.type == QUIT:
            return False
    
    # progress internal event queues for all objects
    dead_object_idents = []
    for game_object in game.game_objects.values():
        object_status = game_object.update_and_get_status()
        if object_status == "dead":
            dead_object_idents.append(game_object.ident)
        ######### Have a way to activate menu here ######
            
    # replenish dead game objects
    
    for ident in dead_object_idents:
        del game.game_objects[ident]
        game.game_objects[ident] = game.spawn(ident)
        # redraw and display everything
    
    screen.blit(background, (0,0))
    for game_object in game.game_objects.values():
        game_object.blit(screen)

    screen.blit(game.scorekeeper.draw_beaker(), (1100, 150))
    
    display.flip()
    return True

if __name__ == "__main__":

    # start pygame mixer
    mixer.pre_init()

    # start pygame
    init()
    
    # Create things you want in the global scope
    game = Game()
    screen = display.set_mode(game.DISPLAY_SIZE)
    background = Surface(game.DISPLAY_SIZE, SRCALPHA)
    background.fill(game.BACKGROUND_COLOR)
    display.set_caption(game.GAME_TITLE)
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

