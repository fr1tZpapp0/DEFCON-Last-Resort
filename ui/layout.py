import pygame
from .theme import Colors

HEADER_RECT = pygame.Rect(20, 15, 960, 65)
MAP_RECT = pygame.Rect(20, 95, 625, 425)
STATUS_RECT = pygame.Rect(660, 95, 320, 290)
ALERT_RECT = pygame.Rect(660, 400, 320, 120)
STATIONS_RECT = pygame.Rect(20, 535, 960, 45)

WORLD_MAP = pygame.image.load("assets/world_map.png").convert()

contacts = [
	{
		"id": "c001",
		"pos_x": 0.62,
		"pos_y": 0.36,
		"kind": "unknown",
		"label": "UNKNOWN CONTACT"
	}
]



def draw_panel(surface, rect, color=Colors.PANEL_COLOR):
	pygame.draw.rect(surface, color, rect, border_radius=4)
	pygame.draw.rect(surface, Colors.BORDER_COLOR, rect, width=1, border_radius=4)


def draw_label(surface, font, text, pos: tuple[int, int], color=Colors.TEXT_COLOR):
	rendered = font.render(text, True, color)
	surface.blit(rendered, pos)


def draw_world_map(surface, rect):
	draw_panel(surface, rect, (18, 32, 39))
	map_image = pygame.transform.smoothscale(WORLD_MAP, rect.size)
	surface.blit(map_image, rect.topleft)


def draw_contact(surface, rect, contact):
	x = rect.x + int(contact['pos_x'] * rect.width)
	y = rect.y + int(contact['pos_y'] * rect.height)

	color = Colors.CAUTION_COLOR if contact["kind"] == "unknown" else Colors.TEXT_COLOR
	pygame.draw.circle(surface, color, (x, y), 5, 1)
	pygame.draw.line(surface, color, (x - 8, y), (x + 8, y), 1)
	pygame.draw.line(surface, color, (x, y - 8), (x, y + 8), 1)


