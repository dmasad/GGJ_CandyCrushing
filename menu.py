'''

menu class

'''
from pygame import *
import sys

class Menu(object):
    def __init__(self, screen, text = "paused", on_key=None):
        '''
        Create a new menu.

        Args:
            screen: Game main screen object to draw on
            text: Text to display; default is "paused"
            on_key: Optional function to call when any key is pressed while in
                    the menu. If None, just exits the menu
        '''

        self.screen = screen
        self.on_key = on_key
        self.text = text
        self.font = font.SysFont("monospace", 24)

    def menu_loop(self):
        self.screen.blit(self.display(), (300, 100))
        display.flip()

        while True:
            for ev in event.get():
                if ev.type == QUIT:
                    sys.exit(0)
                if ev.type == KEYDOWN:
                    if self.on_key == None:
                        return
                    else:
                        self.on_key()


    def display(self):
        base_img = Surface((600,600))
        
        menu_text = self.font.render(self.text, 1, (255,255,0))
        base_img.blit(menu_text, (100, 100))
        return base_img
    

