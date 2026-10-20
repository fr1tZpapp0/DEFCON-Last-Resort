import pygame
from pathlib import Path
from .theme import Colors



class MapView:
	def __init__(self, rect):
		self.rect = pygame.Rect(rect)
		project_root = Path(__file__).resolve().parent.parent
		map_path = project_root / "assets" / "earth.png"

		
		self.image = pygame.image.load(str(map_path)).convert_alpha()



		image_width, image_height = self.image.get_size()
		scale = min(self.rect.width / image_width, self.rect.height / image_height)
		scaled_size = (max(1, round(image_width * scale)), max(1, round(image_height * scale)))

		self.scaled_image = pygame.transform.smoothscale(self.image, scaled_size)
		self.image_rect = self.scaled_image.get_rect(center=self.rect.center)




	def draw(self, surface):
		pygame.draw.rect(surface, Colors.PANEL_COLOR, self.rect, border_radius=4)
		
		old_clip = surface.get_clip()
		surface.set_clip(self.rect)

		surface.blit(self.scaled_image, self.image_rect)
		surface.set_clip(old_clip)

		pygame.draw.rect(surface, Colors.BORDER_COLOR, self.rect, width=2, border_radius=4)


