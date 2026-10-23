import pygame
from .panels import Panel
from .theme import Colors



class MapView:
	def __init__(self):
		self.mapImage= pygame.image.load("assets/earth.png")

		



	def draw(self, surface, pos: tuple[int, int], size: tuple[int, int]):
		mapPanel = Panel(pos, size)
		mapPanel.draw(surface)

		surface.blit(self.mapImage, mapPanel.getRect())
		


