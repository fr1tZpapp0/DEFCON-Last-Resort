import pygame, sys


BACKGROUND_COLOR = (16, 23, 32)
BUTTON_MAIN_COLOR = (32, 61, 74)
BUTTON_HOVER_COLOR = (57, 109, 132)


class Button:
	def __init__(self, label_text, normal_color, hover_color, x_pos, y_pos):
		self.label_text = label_text
		self.normal_color = normal_color
		self.hover_color = hover_color
		self.x_pos = x_pos
		self.y_pos = y_pos


	def buildButton
	


def Touchscreen(WIDTH: int=1000, HEIGHT: int=600):
	pygame.init()

	size = (WIDTH, HEIGHT)

	interfaceRunning = True

	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("DEFCON: Last Resort")

	clock = pygame.time.Clock()
	title_font = pygame.font.SysFont("consolas", 42, bold=True)
	text_font = pygame.font.SysFont("consolas", 20)


	SPLASH = "splash"
	FADE = "fade"
	MENU = "menu"

	state = SPLASH
	splash_start = pygame.time.get_ticks()


	SPLASH_DURATION = 2000
	FADE_DURATION = 1000
	

	



	screen.fill(BACKGROUND_COLOR)




	splash = pygame.Surface(size)
	splash.fill((10, 18, 28))
	splash_title = title_font.render("DEFCON: Last Resort", True, (100, 220, 190))
	splash_subtitle = text_font.render("A game about a true horror....", True, (200, 210, 220))


	splash.blit(splash_title, splash_title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 25)))
	splash.blit(splash_subtitle, splash_subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 25)))



	menu = pygame.Surface(size)
	menu.fill((18, 30, 44))

	menu_title = title_font.render("DEFCON: Last Resort", True, (100, 220, 190))
	menu.blit(menu_title, menu_title.get_rect(center=(WIDTH // 2, HEIGHT // 2)))


	settings_button_label = text_font.render('Settings', True, (100, 220, 190))
	start_button_label = text_font.render('Start', True, (100, 220, 190))

	
	pygame.display.flip()
	while interfaceRunning:
		now = pygame.time.get_ticks()
		mouse = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == pygame.QUIT: interfaceRunning = False
			if state == MENU and event.type == pygame.MOUSEBUTTONDOWN:
				if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2 <= mouse[1] <= HEIGHT /2 + 40:
					print("PRESSED")

		if state == SPLASH:
			screen.blit(splash, (0, 0))

			if now - splash_start >= SPLASH_DURATION:
				state = FADE
				fade_start = now

		elif state == FADE:
			elapsed = now - fade_start
			progress = min(elapsed / FADE_DURATION, 1.0)

			screen.blit(menu, (0, 0))

			splash.set_alpha(int(255 * (1.0 - progress)))
			screen.blit(splash, (0, 0))

			if progress >= 1.0:
				splash.set_alpha(255)
				state = MENU

		elif state == MENU: screen.blit(menu, (0, 0))

		if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2 <= mouse[1] <= HEIGHT /2 + 40:
			pygame.draw.rect(screen, BUTTON_HOVER_COLOR, [WIDTH/2, HEIGHT/2, 140, 40])
		else:
			pygame.draw.rect(screen, BUTTON_MAIN_COLOR, [WIDTH/2, HEIGHT/2, 140, 40])

		screen.blit(settings_button_label, (WIDTH / 2 + 50, HEIGHT / 2))

		pygame.display.flip()
		clock.tick(60)

	else:
		pygame.quit()
		sys.exit()

