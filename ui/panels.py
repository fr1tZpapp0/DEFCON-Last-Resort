import pygame
from .theme import Colors

class Panel:
	def __init__(self, size: tuple[int, int], pos: tuple[int, int]):
		self.size = size
		self.pos = pos

		self.panel_color = Colors.PANEL_COLOR
		self.border_color = Colors.BORDER_COLOR



	def draw(self, surface, border_radius: int=8):
		panel_Rect = pygame.Rect(self.pos, self.size)


		pygame.draw.rect(surface, self.panel_color, panel_Rect, border_radius=border_radius)
		pygame.draw.rect(surface, self.border_color, panel_Rect, width=3, border_radius=border_radius)










