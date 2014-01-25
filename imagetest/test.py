import random
from pygame import *


class Circle(object):
	'''
	Class to store a Circle object

	Attributes:
		id_num: A unique(?) identifier
		alive: Whether the circle is alive / should be drawn
		image: The image to draw
		pos_x, pos_y: X and Y coordinates, in pixels

	'''

	def __init__(self, id_num=None):
		if id_num is None: 
			self.id_num = random.randint(1,1000)
		else:
			self.id_num = id_num

		self.image = image.load("images/face.png").convert()
		self.image.set_colorkey((255,255,255))

		# Composite some eyes onto the image:
		eye = image.load("images/eye.png").convert()
		eye.set_colorkey((255,255,255))
		self.image.blit(eye, (10,10))
		self.image.blit(eye, (30, 10))

		self.pos_x = int(random.random() * 600)
		self.pos_y = int(random.random() * 600)
		self.alive = True

	def get_pos(self):
		return (self.pos_x, self.pos_y)

	def blit(self, screen):
		'''
		Blit this object onto the Screen object
		'''
		if self.alive:
			screen.blit(self.image, self.get_pos())

	def check_click(self, mouse_pos):
		center_x = self.pos_x + self.image.get_width()
		center_y = self.pos_y + self.image.get_height()

		if self.image.get_rect(topleft=self.get_pos()).collidepoint(mouse_pos):
			print "Mouse clicked on", self.id_num
			self.alive = False

		




if __name__ == "__main__":
	init()

	screen = display.set_mode((600,600))
	background = Surface((600, 600), SRCALPHA)
	background.fill((10, 200, 10))
	display.set_caption("Testing")
	running = True

	circles = [Circle(x) for x in range(30)]
	while running:
		for ev in event.get():
			if ev.type == MOUSEBUTTONUP:
				mouse_pos = mouse.get_pos()
				print mouse_pos
				for circle in circles:
					circle.check_click(mouse_pos)
			if ev.type == QUIT:
				running = False



		# Draw
		screen.blit(background, (0,0))
		for circle in circles:
			circle.blit(screen)
		display.flip()


