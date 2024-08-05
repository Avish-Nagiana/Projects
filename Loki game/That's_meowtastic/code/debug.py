import pygame
pygame.init()

# Setting the font of the game
font = pygame.font.Font(None,30)

# Creating a debug function
def debug(info,y = 10, x = 10):
	# Gets current display surface from pygame
	display_surface = pygame.display.get_surface()
	# Rendering the text representation of 'info'
	debug_surf = font.render(str(info),True,'White')
	# Gets the rectangular area that encloses the rendered text
	debug_rect = debug_surf.get_rect(topleft = (x,y))
	# Drawing a black rectangle on the surface
	pygame.draw.rect(display_surface, 'Black', debug_rect)
	# Drawing the rendered text onto the display surface
	display_surface.blit(debug_surf,debug_rect)
