import pygame

interfaceRunning = True
BACKGROUND_COLOR = (16, 23, 32)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("DEFCON: Last Resort")


screen.fill(BACKGROUND_COLOR)




## DISPLAY RENDERING CODE




pygame.display.flip()
while interfaceRunning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			interfaceRunning = False


