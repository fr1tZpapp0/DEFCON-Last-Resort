import pygame, sys


BACKGROUND_COLOR = (16, 23, 32)

BUTTON_MAIN_COLOR = (32, 61, 74)
BUTTON_HOVER_COLOR = (57, 109, 132)

FONT_NAME = "Black Ops One"
TEXT_COLOR = (255, 255, 255)

class Button:
	def __init__(self, label_text: str, normal_color: tuple[int, int, int], 
	hover_color: tuple[int, int, int], pos: tuple[int, int], size: tuple[int, int]):
		self.label_text = label_text
		
		self.normal_color = normal_color
		self.hover_color = hover_color
		self.is_hovered = False
		self.is_pressed = False

		self.font = pygame.font.SysFont(FONT_NAME, 20)
		self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])


	def draw(self, surface):
		if self.is_hovered: current_color = self.hover_color
		else: current_color = self.normal_color

		pygame.draw.rect(surface, current_color, self.rect, border_radius=8)

		text_surface = self.font.render(self.label_text, True, TEXT_COLOR)
		text_rect = text_surface.get_rect(center=self.rect.center)
		surface.blit(text_surface, text_rect)




	def handleEvents(self, event):
		action = False

		mouse_pos = pygame.mouse.get_pos()
		self.is_hovered = self.rect.collidepoint(mouse_pos)

		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			if self.is_hovered: self.is_pressed = True

		elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			if self.is_pressed and self.is_hovered: action = True
			self.is_pressed = False

		return action






def Touchscreen(WIDTH: int=1000, HEIGHT: int=600):
	pygame.init()

	size = (WIDTH, HEIGHT)

	interfaceRunning = True

	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("DEFCON: Last Resort")

	clock = pygame.time.Clock()
	title_font = pygame.font.SysFont(FONT_NAME, 42)
	text_font = pygame.font.SysFont(FONT_NAME, 20)


	SPLASH = "splash"
	FADE = "fade"
	MENU = "menu"

	state = SPLASH
	splash_start = pygame.time.get_ticks()


	SPLASH_DURATION = 2500
	FADE_DURATION = 2000


	screen.fill(BACKGROUND_COLOR)




	splash = pygame.Surface(size)
	splash.fill((10, 18, 28))
	splash_title = title_font.render("DEFCON: Last Resort", True, TEXT_COLOR)
	splash_subtitle = text_font.render("A game about a true horror....", True, (TEXT_COLOR))

	splash.blit(splash_title, splash_title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 25)))
	splash.blit(splash_subtitle, splash_subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 25)))



	menu = pygame.Surface(size)
	menu.fill((18, 30, 44))

	menu_title = title_font.render("DEFCON: Last Resort", True, TEXT_COLOR)
	menu.blit(menu_title, menu_title.get_rect(center=(WIDTH // 2, HEIGHT // 2)))


	start_button = Button("START", BUTTON_MAIN_COLOR, BUTTON_HOVER_COLOR, ((WIDTH - 165) // 2, 338), (165, 65))
	settings_button = Button("SETTINGS", BUTTON_MAIN_COLOR, BUTTON_HOVER_COLOR, ((WIDTH - 165) // 2, 454), (165, 65))

	
	pygame.display.flip()
	while interfaceRunning:
		now = pygame.time.get_ticks()
		mouse = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == pygame.QUIT: interfaceRunning = False
			#if state == MENU and event.type == pygame.MOUSEBUTTONDOWN: print("Pos: ", mouse)
			if state == MENU and start_button.handleEvents(event): print("START!")
			if state == MENU and settings_button.handleEvents(event): print("SETTINGS!")




		if state == SPLASH:
			screen.blit(splash, (0, 0))
			if now - splash_start >= SPLASH_DURATION:
				state = FADE
				fade_start = now

		elif state == FADE:
			elapsed = now - fade_start # type: ignore
			progress = min(elapsed / FADE_DURATION, 1.0)

			screen.blit(menu, (0, 0))

			splash.set_alpha(int(255 * (1.0 - progress)))
			screen.blit(splash, (0, 0))

			if progress >= 1.0:
				splash.set_alpha(255)
				state = MENU

		elif state == MENU:
			screen.blit(menu, (0, 0))

			start_button.draw(screen)
			settings_button.draw(screen)




		pygame.display.flip()
		clock.tick(60)

	else:
		pygame.quit()
		sys.exit()

