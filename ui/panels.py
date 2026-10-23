import pygame
from .theme import Colors

class Panel:
	def __init__(self, size: tuple[int, int], pos: tuple[int, int]):
		self.size = size
		self.pos = pos

		self.panel_color = Colors.PANEL_COLOR
		self.border_color = Colors.BORDER_COLOR



	def draw(self, surface):
		panel_Rect = pygame.Rect()

	




