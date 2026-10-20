import pygame
from ui.theme import Colors
from ui.map_view import MapView

pygame.init()


WIDTH, HEIGHT = 1000, 600
isRunning = True


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DEFCON: Last Resort")
screen.fill(Colors.BACKGROUND_COLOR)



strategic_map = MapView((20, 95, 625, 425))
strategic_map.draw(screen)



pygame.display.flip()
while isRunning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: isRunning = False
