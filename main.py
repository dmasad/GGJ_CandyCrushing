'''

Crushing candy into jam

'''

import random as rnd
from pygame import *
from Game import Game
#from Candy import *


##### NEED SYSTEM TIME FOR ANIMATION RATE TIMING

DISPLAY_SIZE = (600,600)
BACKGROUND_COLOR = (10, 200, 10)
GAME_TITLE = "Crushing Candy Into Jam"
NUM_CANDIES = 30
MUTATE_CHANCE = 0.01
GRID_DIM = (6, 10) # (width, height) in cells of candy grid
CELL_SIZE = 58 # pixels that a cell is wide and tall (assuming square cells)
GRID_POS = (0, 0)



'''
UTILITY FUNCTIONS
================================================
'''

def get_empty_grid_spot(rect_size, obj_list):
    '''
    Return a random position where a rectangle of size rect_size avoids collisions
    with 

    Args:
        rect_size: The height and width (assume a square) to check
        obj_list: A list of objects to avoid collisions with
    '''
    checking = True
    rect_list = [obj.get_rect() for obj in obj_list]
    while checking:
        x = rnd.randint(0, DISPLAY_SIZE[0]-1)
        y = rnd.randint(0, DISPLAY_SIZE[1]-1)
        r = Rect(x, y, rect_size, rect_size)
        i = r.collidelist(rect_list)
        if i == -1: 
            checking = False
    return (x, y)




def spawn(ident, initial=False): # determines what to do about genome
    ### If ident not a number, follow special procedure for non-candy game object ######
    grid_spot = get_empty_grid_spot(58, game_objects.values())
    if initial == True:
        genome = get_init_genome()
    elif initial == False:
        parent1, parent2 = rnd.sample(game_objects.values(), 2) #### BADLY ASSUMES ALL SUCH OBJECTS ARE CANDIES ######
            # (also problem if less than 2 candies)
        genome = getBabyGenome(parent1, parent2)
    return Candy(genome, grid_spot, ident)


'''
MAIN GAME LOOP
==================================================

'''

def initialize():

    # show loading screen for at least 2.25 seconds

    for ident in range(NUM_CANDIES):
        game_objects[ident] = spawn(ident, initial=True)
    ### create other game objects with spawn too    


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
    
    display.flip()
    return True

if __name__ == "__main__":

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

    running = True
    while game_loop(game):
        pass

