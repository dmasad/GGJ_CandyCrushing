'''
Candy object and related methods

GGJ GMU 2014, Candy Herder / Crushing Candy into Jam Team
Nathan McClain
Brendon Fuhs
David Masad


'''

import random as rnd
import os
from pygame import *
import math

# Setting up some genome stuff
# ============================

MUTATE_CHANCE = 0.15

ATTRIBUTE_TYPES = ["body", "sound", "behavior"]
ATTRIBUTES = {"body": "graphics",
              "eyes": "graphics",
              "mouth": "graphics",
              "speed": "behavior",
              "fear": "behavior",
              "death": "sound",
              "squish": "sound"}
GRAPHICS_DICT = {}
SOUNDS_DICT = {}
BEHAVIORS_DICT = {}

# Populate:
for attribute in ATTRIBUTES:
    if ATTRIBUTES[attribute] == "graphics":
        GRAPHICS_DICT[attribute] = {} # attribute : value : image
        path = "graphics/" + attribute + "/"
        for f in os.listdir(path):
            if f[-3:] == "png": 
                i = int(f[0])
                img = image.load(path + f)
                GRAPHICS_DICT[attribute][i] = img
    if ATTRIBUTES[attribute] == "behavior":
        pass
    if ATTRIBUTES[attribute] == "sound":
        SOUNDS_DICT[attribute] = {}
        path = "audio/" + attribute + "/"
        for f in os.listdir(path):
            if f[-3:] == "mp3":  ##### supposed to be ogg / wav ? #####
                i = int(f[0])
                filename = path + f
                SOUNDS_DICT[attribute][filename] = [] #### POPULATE AUDIO OBJ LATER
                
BEHAVIORS_DICT["fear"] = ["friendly", "indifferent", "scared"]
BEHAVIORS_DICT["speed"] = [1, 2, 4]
    


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

        self.speed = self.genome["speed"]
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
        mouth = GRAPHICS_DICT["mouth"][self.genome["mouth"]].convert_alpha()

        body = transform.smoothscale(body, (self.game.CELL_SIZE, self.game.CELL_SIZE))
        eyes = transform.smoothscale(eyes, (self.game.CELL_SIZE, self.game.CELL_SIZE))
        mouth = transform.smoothscale(mouth, (self.game.CELL_SIZE, self.game.CELL_SIZE))
        

        self.image = body
        self.image.blit(eyes, (0,0))
        self.image.blit(mouth, (0,0))

    def change_direction(self):
        # random direction
        self.direction = rnd.random() * 2 * math.pi
        # set velocity
        x_vel = self.speed*math.sin(self.direction)
        y_vel = self.speed*math.cos(self.direction)
        self.velocity = (x_vel, y_vel)
    

    def move_random(self):
        '''
        Move around randomly
        '''
        rect_list = [obj.get_rect() for obj in self.game.game_objects.values() if obj is not self]
        # Try changing directions 8 times
        for i in range(8):
            new_x = (self.position[0] + self.velocity[0])
            new_y = (self.position[1] + self.velocity[1])
            cell_size = self.game.CELL_SIZE
            r = Rect(new_x, new_y, cell_size, cell_size)
            i = r.collidelist(rect_list)
            on_screen = 0 < new_x < (self.game.DISPLAY_SIZE[0]-cell_size) and 0 < new_y < (self.game.DISPLAY_SIZE[1]-cell_size)
            if i == -1 and on_screen: # no collision
                self.position = (new_x, new_y)
                return
            else:
                self.change_direction()

    def move_to_mouse(self, mouse_coords):
        dy = mouse_coords[1] - self.position[1]
        dx = mouse_coords[0] - self.position[0]
        v = math.sqrt(dy**2 + dx**2)

        x_vel = (dx / v) * self.speed
        y_vel = (dy / v) * self.speed
        self.velocity = (x_vel, y_vel)

        rect_list = [obj.get_rect() for obj in self.game.game_objects.values() if obj is not self]

        new_x = (self.position[0] + self.velocity[0])
        new_y = (self.position[1] + self.velocity[1])
        cell_size = self.game.CELL_SIZE
        r = Rect(new_x, new_y, cell_size, cell_size)
        i = r.collidelist(rect_list)
        on_screen = 0 < new_x < (self.game.DISPLAY_SIZE[0]-cell_size) and 0 < new_y < (self.game.DISPLAY_SIZE[1]-cell_size)
        if i == -1 and on_screen: # no collision
            self.position = (new_x, new_y)
            return
        else:
            self.move_random()

    def move_awayfrom_mouse(self, mouse_coords):
        dy = mouse_coords[1] - self.position[1]
        dx = mouse_coords[0] - self.position[0]
        v = math.sqrt(dy**2 + dx**2)

        x_vel = -(dx / v) * self.speed
        y_vel = -(dy / v) * self.speed
        self.velocity = (x_vel, y_vel)

        rect_list = [obj.get_rect() for obj in self.game.game_objects.values() if obj is not self]

        new_x = (self.position[0] + self.velocity[0])
        new_y = (self.position[1] + self.velocity[1])
        cell_size = self.game.CELL_SIZE
        r = Rect(new_x, new_y, cell_size, cell_size)
        i = r.collidelist(rect_list)
        on_screen = 0 < new_x < (self.game.DISPLAY_SIZE[0]-cell_size) and 0 < new_y < (self.game.DISPLAY_SIZE[1]-cell_size)
        if i == -1 and on_screen: # no collision
            self.position = (new_x, new_y)
            return
        else:
            self.move_random()

    def update_and_get_status(self, mouse_pos): # This will handle ongoing animations
        if self.genome["fear"] == "indifferent":
            self.move_random()
        elif self.genome["fear"] == "friendly":
            self.move_to_mouse(mouse_pos)
        elif self.genome["fear"] == "scared":
            self.move_awayfrom_mouse(mouse_pos)

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
            # do death and squish sounds simultaneously
            for sound_type in SOUNDS_DICT:
                SOUNDS_DICT[sound_type][self.genome[sound_type]].play()
                print self.genome[sound_type] ####
            self.alive = False
            self.game.scorekeeper.add_jam()

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
            if ATTRIBUTES[attribute] == "graphics":
                new_genome[attribute] = rnd.choice(GRAPHICS_DICT[attribute].keys())
            if ATTRIBUTES[attribute] == "behavior":
                new_genome[attribute] = rnd.choice(BEHAVIORS_DICT[attribute])
            if ATTRIBUTES[attribute] == "sound":
                new_genome[attribute] = rnd.choice(SOUNDS_DICT[attribute].keys())

    return new_genome

def get_init_genome():
    #### WILL NEED TO REWRITE TO MANUALLY RESTRICT INITIALLY SUPPRESSED ATTRIBUTES ###
    new_genome = {} # dict of attribute: position value
    for attribute in ATTRIBUTES:
        if ATTRIBUTES[attribute] == "graphics":
            new_genome[attribute] = rnd.choice(GRAPHICS_DICT[attribute].keys())
        if ATTRIBUTES[attribute] == "behavior":
            new_genome[attribute] = rnd.choice(BEHAVIORS_DICT[attribute])
        if ATTRIBUTES[attribute] == "sound":
            new_genome[attribute] = rnd.choice(SOUNDS_DICT[attribute].keys())
        
    return new_genome

class Spatter(object):
    def __init__(self, position):
        self.position = position
        self.ticks_left = 60
        self.alive= True
        img_list = ["graphics/spatter/purple-goo.png",
                    "graphics/spatter/green-goo.png",
                    "graphics/spatter/blue-goo.png"]
        self.img = image.load(rnd.choice(img_list)).convert_alpha()
    def blit(self, screen):
        screen.blit(self.img, self.position)
    def update_status(self):
        self.ticks_left -= 1
        if self.ticks_left <= 0:
            self.alive = False
        return self.alive


    
