import pygame
from .theme import Colors

class Panel:
	def __init__(self, pos: tuple[int, int], size: tuple[int, int]):
		self.size = size
		self.pos = pos

		self.panel_color = Colors.PANEL_COLOR
		self.border_color = Colors.BORDER_COLOR



	def draw(self, surface, border_radius: int=8):
		panel_Rect = pygame.Rect(self.pos, self.size)


		pygame.draw.rect(surface, self.panel_color, panel_Rect, border_radius=border_radius)
		pygame.draw.rect(surface, self.border_color, panel_Rect, width=3, border_radius=border_radius)
		

	def addText(self, text: str, textPos: tuple[int, int], fontType: pygame.font, color=Colors.TEXT_COLOR):
		panelSurface = pygame.Surface(self.size)
		panelRect = pygame.Rect(self.pos, self.size)


		label = fontType.render(text, True, color)
		panelSurface.blit(label, panelRect)

		



	def getRect(self) -> pygame.Rect:
		return pygame.Rect(self.pos, self.size)

	def getSurface(self) -> pygame.Surface:
		return pygame.Surface(self.size)
