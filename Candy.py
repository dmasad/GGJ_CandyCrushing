'''
Candy object and related methods

GGJ GMU 2014, Crushing Candy into Jam Team

'''

import random as rnd
import os
from pygame import *
import math

# Setting up some genome stuff
# ============================

MUTATE_CHANCE = 0.25
## ORDER THESE IN DRAW ORDER (back-to-front)
'''
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

'''

ATTRIBUTES = ["body",
              "eyes"]
              #"mouth"]

GRAPHICS_DICT = {}
# Populate:
for attribute in ATTRIBUTES:
    GRAPHICS_DICT[attribute] = {}
    path = "graphics/" + attribute + "/"
    for f in os.listdir(path):
        if f[-3:] == "png": 
            i = int(f[0])
            img = image.load(path + f)
            GRAPHICS_DICT[attribute][i] = img

class Candy(object):

    def __init__(self, genome, position, ident, game):
        '''
        Create a new Candy

        Args:
            genome: The candy's genome
            position: Tuple of grid (not pixel) coordinates
            ident: 
        '''
        self.game = game
        self.ident = ident
        self.genome = genome # dict of attribute: attribute value
        self.position = position
        self.assemble_image()
        #self.image = image.load("imagetest/images/face.png").convert()
            ### WILL BE WAY DIFFERENT self.assemble_image()
        self.alive = True

        self.speed = 1.0 ##### BASE THIS ON GENOME
        self.velocity = (0,0)
        self.direction = 0 # radians
        self.change_direction() # and direction
        
        
    
    def get_pos(self):
        return self.position

    def assemble_image(self):
        '''
        Composite an image based on the genome
        '''
        # Get graphics
        body = GRAPHICS_DICT["body"][self.genome["body"]].convert_alpha()
        eyes = GRAPHICS_DICT["eyes"][self.genome["eyes"]].convert_alpha()
        #mouth = GRAPHICS_DICT["mouth"][self.genome["mouth"]].convert_alpha()

        self.image = body
        #self.image.blit(body, (0,0))
        self.image.blit(eyes, (0,0))
        #self.image.blit(mouth, (80, 30))

    def change_direction(self):
        # random direction
        self.direction = rnd.random() * 2 * math.pi
        # set velocity
        x_vel = self.speed*math.sin(self.direction)
        y_vel = self.speed*math.cos(self.direction)
        self.velocity = (x_vel, y_vel)
        
    def update_and_get_status(self): # This will handle ongoing animations

        for i in range(10):
        
            # check if collision
            rect_list = [obj.get_rect() for obj in self.game.game_objects.values() if obj is not self]
            x = self.position[0]
            y = self.position[1]
            r = Rect(x, y, self.game.CELL_SIZE, self.game.CELL_SIZE)
            i = r.collidelist(rect_list)
            if i == -1: # no collision
                break

            # change velocity until no collision # set to zero if too much
            self.change_direction()

            if i > 8: # if too long without finding a good velocity, just stay put
                self.velocity = (0,0)
                break

        # if no collision move in accordance with velocity
        new_x = self.position[0] + self.velocity[0]
        new_y = self.position[1] + self.velocity[1]
        self.position = (new_x, new_y)

        # check if alive and return status        
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
