'''

Crushing candy into jam

'''

import random as rnd
from pygame import *

##### NEED SYSTEM TIME FOR ANIMATION RATE TIMING

DISPLAY_SIZE = (600,600)
BACKGROUND_COLOR = (10, 200, 10)
GAME_TITLE = "Crushing Candy Into Jam"
NUM_CANDIES = 30
MUTATE_CHANCE = 0.01
GRID_DIM = (6, 10) # (width, height) in cells of candy grid
CELL_SIZE = 58 # pixels that a cell is wide and tell (assuming square cells)
GRID_POS = (0, 0)

## ORDER THESE IN DRAW ORDER (back-to-front)
ATTRIBUTES = ["eyebrows",
              "eyes",
              "mouth",
              "nose", #?
              "color",
              "sparkles",
              "shape",
              "noise",
              "speed",
              "flee"]

GRAPHICS_DICT = {}
# attribute name : attribute value: graphical object
####### Placeholder #######:
for attribute in ATTRIBUTES:
    GRAPHICS_DICT[attribute] = {0: "imagetest/images/face.png", 1: "imagetest/images/face.png"}



class Candy(object):

    def __init__(self, genome, grid_spot, ident):
        self.ident = ident
        self.genome = genome # dict of attribute: attribute value
        self.grid_spot = grid_spot
            #### Could lazy type and stick in multiple spots, but that would break other stuff
        grid_to_object[self.grid_spot] = self
        
        self.image = image.load("imagetest/images/face.png").convert()
            ### WILL BE WAY DIFFERENT self.assemble_image()
        self.alive = True
    
    def get_pos(self):
        return grid_to_position[self.grid_spot] ### need to account for offset during animations

    def assemble_image(self):
        for attribute in ATTRIBUTES:
            graphic = GRAPHICS_DICT[attribute][self.genome[attribute]]
            draw(graphic, self.position) ######3 NOPE NOPE, SOMETHING WITH BLIT INSTEAD ##############

    def update_and_get_status(self): # This will handle ongoing animations
        if self.alive == False:
            grid_to_object[self.grid_spot] = None
            return "dead"
        else:
            return "alive"

    def check_click(self, mouse_pos):
        if self.image.get_rect( topleft=self.get_pos() ).collidepoint(mouse_pos):
            print "Mouse clicked on", self.ident #####
            self.alive = False

    def blit(self, screen):
        screen.blit(self.image, self.get_pos())



def getBabyGenome(Candy1, Candy2):
    genome1 = Candy1.genome
    genome2 = Candy2.genome

    new_genome = {}

    # get from parents
    for attribute in ATTRIBUTES:
        new_genome[attribute] = rnd.choice([genome1[attribute], genome2[attribute]])
    
    # randomly mutate
    for attribute in ATTRIBUTES:
        if rnd.random() < MUTATE_CHANCE:
            new_genome[attribute] = rnd.choice(GRAPHICS_DICT[attribute].keys())

    return new_genome

def get_init_genome():
    #### WILL NEED TO REWRITE TO MANUALLY RESTRICT INITIALLY SUPPRESSED ATTRIBUTES ###
    new_genome = {} # dict of attribute: position value
    for attribute in ATTRIBUTES:
        new_genome[attribute] = rnd.choice(GRAPHICS_DICT[attribute].keys())
    return new_genome

def get_empty_grid_spot():
    empty_spots = [spot for spot in grid_to_object if grid_to_object[spot]==None]
    return rnd.choice(empty_spots)

def spawn(ident, initial=False): # determines what to do about genome
    ### If ident not a number, follow special procedure for non-candy game object ######
    grid_spot = get_empty_grid_spot()
    if initial == True:
        genome = get_init_genome()
    elif initial == False:
        parent1, parent2 = rnd.sample(game_objects.values(), 2) #### BADLY ASSUMES ALL SUCH OBJECTS ARE CANDIES ######
            # (also problem if less than 2 candies)
        genome = getBabyGenome(parent1, parent2)
    return Candy(genome, grid_spot, ident)

def initialize():

    # show loading screen for at least 2.25 seconds

    # populate grid to pixel coordinates dictionary
    cells_wide, cells_tall = GRID_DIM
    for x_cell in range(cells_wide):
        for y_cell in range(cells_tall):
            x = GRID_POS[0] + x_cell*CELL_SIZE
            y = GRID_POS[1] + y_cell*CELL_SIZE
            grid_to_position[(x_cell, y_cell)] = (x, y)
            grid_to_object[(x_cell, y_cell)] = None
                # game_objects will put selves in appropriate spot ##########
    
    # create game objects and populate grid to game_object dictionary
                                            ###(objects will take care of) ####
    for ident in range(NUM_CANDIES):
        game_objects[ident] = spawn(ident, initial=True)
    ### create other game objects with spawn too    


def menu_loop(): ## need to somehow stop animation clocks when this is active
    pass #######################################

def game_loop():

    # get all mouse clicks and pygame events
    already_got_click = False # I'm only going to get one mouse click
    for ev in event.get():
        if ev.type == MOUSEBUTTONUP and already_got_click == False:
            already_got_click = True
            mouse_pos = mouse.get_pos()
            print mouse_pos ###
            for game_object in game_objects.values(): 
                game_object.check_click(mouse_pos)    
        if ev.type == QUIT:
            running = False

    # progress internal event queues for all objects
    dead_object_idents = []
    for game_object in game_objects.values():
        object_status = game_object.update_and_get_status()
        if object_status == "dead":
            dead_object_idents.append(game_object.ident)
        ######### Have a way to activate menu here ######
            
    # replenish dead game objects
    for ident in dead_object_idents:
        grid_to_object[game_objects[ident].grid_spot] = None
        del game_objects[ident]
        game_objects[ident] = spawn(ident)

    # redraw and display everything
    screen.blit(background, (0,0))
    for game_object in game_objects.values():
        game_object.blit(screen)
        display.flip()


if __name__ == "__main__":

    # start pygame
    init()
    
    # Create things you want in the global scope
    screen = display.set_mode(DISPLAY_SIZE)
    background = Surface(DISPLAY_SIZE, SRCALPHA)
    background.fill(BACKGROUND_COLOR)
    display.set_caption(GAME_TITLE)
    grid_to_position = {}
    game_objects = {}
    # all game objects need
    #   ident
    #   check_click method
    #   update_and_get_status method
    #   blit method
    grid_to_object = {}
    
    initialize()

    running = True
    while running:
        game_loop()

