'''
Candy object and related methods

GGJ GMU 2014, Crushing Candy into Jam Team

'''

import random as rnd
from pygame import *

# Setting up some genome stuff
# ============================

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
    GRAPHICS_DICT[attribute] = {
        0: "imagetest/images/face.png", 
        1: "imagetest/images/face.png"
        }


MUTATE_CHANCE = 0.01



class Candy(object):

    def __init__(self, genome, position, ident):
        '''
        Create a new Candy

        Args:
            genome: The candy's genome
            position: Tuple of grid (not pixel) coordinates
            ident: 
        '''
        self.ident = ident
        self.genome = genome # dict of attribute: attribute value
        self.position = position
        self.image = image.load("imagetest/images/face.png").convert()
            ### WILL BE WAY DIFFERENT self.assemble_image()
        self.alive = True
    
    def get_pos(self):
        return self.position

    def assemble_image(self):
        for attribute in ATTRIBUTES:
            graphic = GRAPHICS_DICT[attribute][self.genome[attribute]]
            draw(graphic, self.position) ######3 NOPE NOPE, SOMETHING WITH BLIT INSTEAD ##############

    def update_and_get_status(self): # This will handle ongoing animations
        if self.alive == False:
            return "dead"
        else:
            return "alive"

    def get_rect(self):
        return self.image.get_rect(topleft=self.get_pos())

    def check_collision(self, coords):
        '''
        Check to see whether coordinates collide with this object
        '''
        if self.get_rect().collidepoint(coords):
            return True
        else:
            return False

    def check_click(self, mouse_pos):
        if self.check_collision(mouse_pos):
            print "Mouse clicked on", self.ident
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
