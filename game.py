import random as rnd

from pygame import *

import Candy

class Game(object):
    '''
    God class to monitoring the game, holding all game variables, etc.
    '''

    def __init__(self):
        '''
        Create a new game
        '''

        # Game constants
        self.DISPLAY_SIZE = (600,600)
        #self.BACKGROUND_COLOR = (10, 200, 10) # Green
        self.BACKGROUND_COLOR = (180, 180, 180) # Gray

        self.GAME_TITLE = "Crushing Candy Into Jam"
        self.NUM_CANDIES = 10
        self.MUTATE_CHANCE = 0.01
        self.GRID_DIM = (6, 10) # (width, height) in cells of candy grid
        self.CELL_SIZE = 100 # pixels that a cell is wide and tall (assuming square cells)
        self.GRID_POS = (0, 0)
        self.SOUNDTRACK = "audio/348504_Riding_on_the_edge_.mp3"

        self.game_objects = {} # Objects in the game

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

        
        for ident in range(self.NUM_CANDIES):
            self.game_objects[ident] = self.spawn(ident, initial=True)

    def get_empty_grid_spot(self, rect_size):
        '''
        Return a random position where a rectangle of size rect_size avoids collisions
        with 

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




