'''

menu class

'''
from pygame import *

class Menu(object):
    def __init__(self, text = "paused"):
        self.text = text

    def display(self):
        base_img = Surface((600,600))
        
        menu_text = self.font.render(self.text, 1, (255,255,0))
        base_img.blit(menu_text, (100, 100))
        return base_img
    

