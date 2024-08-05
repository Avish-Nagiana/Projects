import pygame
import sys
from settings import *
from level import Level

class Game:
	def __init__(self):

		# general setup of the game window
		pygame.init()
		# Creating the screen
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		# Giving the window a name - Name of the game
		pygame.display.set_caption('Loki')
		self.clock = pygame.time.Clock()

		self.level = Level()

		# sound
		# Getting the sound file, setting its volume and then playing it
		main_sound = pygame.mixer.Sound('../audio/main.ogg')
		main_sound.set_volume(0.5)
		main_sound.play(loops = -1)
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				# Creating the upgrade menu
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_m:
						self.level.toggle_menu()

			# Filling the screen outside of map with water color
			self.screen.fill(WATER_COLOR)
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()