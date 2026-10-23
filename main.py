import pygame
from ui.theme import Colors
from ui.map_view import MapView
from ui.panels import Panel

pygame.init()
pygame.display.set_caption("DEFCON: Last Resort")

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


isRunning = True
while isRunning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: isRunning = False


	
	screen.fill(Colors.BACKGROUND_COLOR)


	tacMap = MapView().draw(screen, (22, 22), (480, 360))






	pygame.display.flip()
