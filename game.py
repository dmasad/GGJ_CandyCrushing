'''
GGJ GMU 2014, Candy Herder / Crushing Candy into Jam Team
Nathan McClain
Brendon Fuhs
David Masad


'''

import random as rnd
import sys

from pygame import *

import Candy
from menu import *

class Game(object):
    '''
    God class to monitoring the game, holding all game variables, etc.
    '''

    def __init__(self):
        '''
        Create a new game
        '''

        # Game constants
        self.DISPLAY_SIZE = (1100,800)
        #self.BACKGROUND_COLOR = (10, 200, 10) # Green
        self.BACKGROUND_COLOR = (180, 180, 180) # Gray

        self.GAME_TITLE = "Candy Herder"
        self.START_CANDIES = 10
        self.MAX_CANDIES = 60
        self.MUTATE_CHANCE = 0.01
        self.CELL_SIZE = 60 # pixels that a cell is wide and tall (assuming square cells)
        #self.SOUNDTRACK = "audio/348504_Riding_on_the_edge_.mp3"
        self.SOUNDTRACK = "audio/bardy.MID"
        
        self.game_objects = {} # Objects in the game
        self.max_id = 0
        self.scorekeeper = Scorekeeper(self)

        self.spawn_prob = 1.0/(60*3)
        self.endgame = False # End-game

        self.spatter_list = []

    def initialize(self):
        '''
        Initialize the game
        '''

        # show loading screen for at least 2.25 seconds
        try:
            mixer.music.load(self.SOUNDTRACK)
            mixer.music.play(-1) # play FOREVER!!!
        
        except:
            print "Music-related error"

        # stick sounds in SOUNDS_DICT
        for attribute in Candy.SOUNDS_DICT:
            for filename in Candy.SOUNDS_DICT[attribute]:
                Candy.SOUNDS_DICT[attribute][filename] = mixer.Sound(filename)
        
        for ident in range(self.START_CANDIES):
            self.game_objects[ident] = self.spawn(ident, initial=True)
            self.max_id += 1

    def get_empty_grid_spot(self, rect_size):
        '''
        Return a random free position for a rectangle of size rect_size

        Args:
            rect_size: The height and width (assume a square) to check

        Returns:
            A random collision-free (x, y) tuple 
        '''
        checking = True
        rect_list = [obj.get_rect() for obj in self.game_objects.values()]
        while checking:
            x = rnd.randint(0, self.DISPLAY_SIZE[0]-rect_size)
            y = rnd.randint(0, self.DISPLAY_SIZE[1]-rect_size)
            r = Rect(x, y, rect_size, rect_size)
            i = r.collidelist(rect_list)
            if i == -1: 
                checking = False
        return (x, y)


    def check_spawn(self):
        '''
        Check to see whether to spawn a new candy
        '''
        if len(self.game_objects) < 2:
            if not self.endgame:
                # Game loss condition
                path = "graphics/splashes/loss1.png"
            else:
                # Game ending 1
                path = "graphics/splashes/end1.png"
            menu = SplashScreen(self.screen, path, on_key=lambda: sys.exit(0))
            menu.menu_loop()

        if len(self.game_objects) > self.MAX_CANDIES:
            if not self.endgame:
                path = "graphics/splashes/loss2.png"
            else:
                path = "graphics/splashes/end2.png"
            menu = SplashScreen(self.screen, path, on_key=lambda: sys.exit(0))
            menu.menu_loop()

        if rnd.random() < self.spawn_prob:
            self.max_id += 1
            new = self.spawn(self.max_id)
            #print "Spawning"
            self.game_objects[self.max_id] = new

    def spawn(self, ident, initial=False):
        '''
        Create a new Candy object
        '''
        ### If ident not a number, follow special procedure for non-candy game object ######
        grid_spot = self.get_empty_grid_spot(self.CELL_SIZE)
        if initial == True:
            genome = Candy.get_init_genome()
        elif initial == False:
            #### BADLY ASSUMES ALL SUCH OBJECTS ARE CANDIES ######
            parent1, parent2 = rnd.sample(self.game_objects.values(), 2) 
                # (also problem if less than 2 candies)
            genome = Candy.getBabyGenome(parent1, parent2)
        return Candy.Candy(genome, grid_spot, ident, self)

    def create_spatter(self, corpse_location):
        self.spatter_list.append(Candy.Spatter(corpse_location))
        



class Scorekeeper(object):
    '''
    Class to track score and draw the jamometer
    '''

    def __init__(self, game):
        self.game = game
        self.current_jam = 0
        self.level = 0
        self.LEVEL_MAX = [1, 5, 10, 20, 50] # Target jams per level
        self.max_jam = self.LEVEL_MAX[self.level]

        # Load image assets
        self.beaker_img = image.load("graphics/jam/beaker.png")
        self.jam_imgs = [image.load("graphics/jam/jam" + str(i) + ".png")
                                                        for i in range(1,4)]
        self.font = font.SysFont("monospace", 24)


    def add_jam(self):
        '''
        Add 1 candy to the jam
        '''
        self.current_jam += 1
        if self.current_jam >= self.max_jam:
            self.level += 1
            if self.level < len(self.LEVEL_MAX):
                self.max_jam = self.LEVEL_MAX[self.level]
                self.current_jam = 0
                self.game.spawn_prob *= 1.5
            elif not self.game.endgame: # End game scenario
                message = ["Good job, Candy Herder!",
                            "Now we're gonna need you",
                            "to go ahead and liquidate",
                            "your herd.",
                            "",
                            "Good job!"
                            ]
                menu = Menu(self.game.screen, text=message)
                menu.menu_loop()
                self.game.endgame = True
                self.game.spawn_prob = (1.0/120)



    def draw_beaker(self):
        base_img = Surface((100,800))
        base_img.blit(self.beaker_img, (0,150))
        count = int(self.current_jam / (self.max_jam / 12.0))
        start_y = 800 - (10 + 60) # Top-left of lowest jam bar
        for i in range(count):
            img = rnd.choice(self.jam_imgs)
            img = img.convert()
            base_img.blit(img, (10, start_y - i*50))

        score_text = str(self.current_jam) + "/" + str(self.max_jam)
        score = self.font.render(score_text, 1, (255,255,0))
        base_img.blit(score, (10, 100))
        return base_img








