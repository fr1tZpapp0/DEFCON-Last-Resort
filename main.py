import pygame
from ui.theme import Colors
from ui.map_view import MapView
from ui.panels import Panel

pygame.init()
pygame.display.set_caption("DEFCON: Last Resort")

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

titleFont = pygame.font.SysFont("Black Ops One", 40)
textFont = pygame.font.SysFont("Black Ops One", 20)

isRunning = True
while isRunning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: isRunning = False


	
	screen.fill(Colors.BACKGROUND_COLOR)

	labelPanel = Panel((244, 244), (220, 120))
	labelPanel.draw(screen)

	testLabel = textFont.render("I'm a test!", True, Colors.TEXT_COLOR)
	labelPanel.getRect().blit(testLabel, labelPanel.getRect())

	tacMap = MapView().draw(screen, (22, 22), (180, 60))






	pygame.display.flip()
