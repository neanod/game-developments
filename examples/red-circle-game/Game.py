import random
import pygame as pg
import pygame_gui as pgg
from pygame_gui import UIManager
from pygame_gui import elements
from math import sin, cos, radians, atan2, pi, degrees, dist
from player_bullet import Bullet
import sys
import webbrowser
from enemy import Enemy


# TODO: Добавить плавный поворот врагов, настройки: спавнрейт и режим отрисовки врагов


def main():
	"""CONSTANTS"""
	
	class Settings:
		FPS = 60
		SCREEN_SIZE = [1920, 1080]
		TEXT_FONT_ARIAL = "fonts\\arial.ttf"
		TEXT_FONT_TIMES_NEW_ROMAN = "fonts\\timesnewroman.ttf"
		FONT_SIZE = 30
		
		RENDER_MODE = 0
		RENDER_MODE_N = 2
		
		SCREEN_WIDTH = SCREEN_SIZE[0]
		SCREEN_HEIGHT = SCREEN_SIZE[1]
		
		SCREEN_CENTER = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
		
		DEFAULT_PLAYER_SPEED = 8
		DEFAULT_PLAYER_SHOOT_CD = 2
		
		DEFAULT_BULLET_SPEED = 25
		
		PLAYER_R = 20
		
		SPAWNRATE = 1.2
		PAUSE = False
		
		MENU_BOX_SIZE = [600, 500]
		MENU_WHITE_BOX_RECT = pg.Rect(SCREEN_WIDTH / 2 - MENU_BOX_SIZE[0] // 2,
		                              SCREEN_HEIGHT / 2 - MENU_BOX_SIZE[1] // 2, *MENU_BOX_SIZE)
		SETTINGS_WHITE_BOX_RECT = pg.Rect(SCREEN_WIDTH / 2 - MENU_BOX_SIZE[0] // 2,
		                                  SCREEN_HEIGHT / 2 - MENU_BOX_SIZE[1] // 2, *MENU_BOX_SIZE)
		
		INGAME_MENU_RUNNING = False
		CREATORS_MENU_RUNNING = False
		SETTINGS_MENU_RUNNING = False
		START_MENU_RUNNING = False
		
		ENEMY_SIZE = 200
	
	sc = pg.display.set_mode(Settings.SCREEN_SIZE, pg.DOUBLEBUF)
	"""VARS"""
	pg.init()
	clock = pg.time.Clock()
	"""LOADING IMAGES"""
	
	class Textures:
		example_square = [
			x := pg.image.load("textures/white_example_square.png").convert_alpha(),
			x.get_rect().size,
		]
		
		example = [
			x := pg.image.load("textures/white_example_rect.png").convert_alpha(),
			x.get_rect().size,
		]
		
		background = [
			x := pg.image.load("textures/background.png").convert(),
			x.get_rect().size,
		]
		enemy = [
			x := pg.image.load("textures/enemy1.png").convert_alpha(),
			x.get_rect().size
		]
	
	def get_random_spawn_pos() -> list[int, int]:
		right = Settings.SCREEN_WIDTH + Settings.ENEMY_SIZE // 2
		bottom = Settings.SCREEN_HEIGHT + Settings.ENEMY_SIZE // 2
		left = -Settings.ENEMY_SIZE // 2
		up = -Settings.ENEMY_SIZE // 2
		match random.randint(0, 3):
			case 0:
				return [random.randint(left, right), up]
			case 1:
				return [right, random.randint(up, bottom)]
			case 2:
				return [random.randint(left, right), bottom]
			case 3:
				return [left, random.randint(up, bottom)]
	
	class Enemies:
		enemy_list: list[Enemy] = list()
		enemy_list.append(Enemy(get_random_spawn_pos))
	
	class Player:
		x, y = Settings.SCREEN_CENTER
		speed = 0
		speed_x = 0
		speed_y = 0
		speed_direct = 0
		do_move = False
		shoot_cd = 0
	
	class Button:
		def __init__(self, x, y, width, height, text, action=None):
			self.rect = pg.Rect(Settings.SCREEN_WIDTH / 2 + x - width / 2, Settings.SCREEN_HEIGHT / 2 + y - height / 2,
			                    width, height)
			self.color = (100, 100, 100)
			self.text = text
			self.action = action
		
		def draw(self):
			pg.draw.rect(sc, self.color, self.rect, border_radius=5)
			font = pg.font.Font(Settings.TEXT_FONT_TIMES_NEW_ROMAN, Settings.FONT_SIZE)
			text = font.render(self.text, True, (255, 255, 255))
			text_rect = text.get_rect(center=self.rect.center)
			sc.blit(text, text_rect)
		
		def handle_event(self, event):
			if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
				if self.rect.collidepoint(event.pos):
					if self.action:  # Выполнение действия, связанного с кнопкой
						self.action()
	
	class ButtonsInfo:
		W = False
		A = False
		S = False
		D = False
		ESC = False
		
		LMB = False
		RMB = False
		
		MOUSE_POS = [0, 0]
	
	def game():
		
		close_start_menu()
		game_over = False
		t = 0
		bullets = list()
		
		while not game_over:
			for event in pg.event.get():
				match event.type:
					case pg.QUIT:
						game_over = True
						quit_game()
					case pg.KEYDOWN:
						match event.key:
							case pg.K_w:
								ButtonsInfo.W = True
							case pg.K_a:
								ButtonsInfo.A = True
							case pg.K_s:
								ButtonsInfo.S = True
							case pg.K_d:
								ButtonsInfo.D = True
							case pg.K_ESCAPE:
								ButtonsInfo.ESC = True
					case pg.KEYUP:
						match event.key:
							case pg.K_w:
								ButtonsInfo.W = False
							case pg.K_a:
								ButtonsInfo.A = False
							case pg.K_s:
								ButtonsInfo.S = False
							case pg.K_d:
								ButtonsInfo.D = False
							case pg.K_ESCAPE:
								ButtonsInfo.ESC = False
					case pg.MOUSEBUTTONDOWN:
						match event.button:
							case 1:
								ButtonsInfo.LMB = True
							case 0:
								ButtonsInfo.RMB = True
					case pg.MOUSEBUTTONUP:
						match event.button:
							case 1:
								ButtonsInfo.LMB = False
							case 0:
								ButtonsInfo.RMB = False
			ButtonsInfo.MOUSE_POS = pg.mouse.get_pos()
			Settings.PAUSE = ButtonsInfo.ESC
			t += 1
			"""LOGIC"""
			clamp_player_pos()
			Player.do_move = False
			
			match [ButtonsInfo.W, ButtonsInfo.A, ButtonsInfo.S, ButtonsInfo.D]:
				# прямое направление - |
				case [True, False, False, False] | [True, True, False, True]:
					Player.speed_direct = 0
					Player.do_move = True
				case [False, True, False, False] | [True, True, True, False]:
					Player.speed_direct = 270
					Player.do_move = True
				case [False, False, True, False] | [False, True, True, True]:
					Player.speed_direct = 180
					Player.do_move = True
				case [False, False, False, True] | [True, False, True, True]:
					Player.speed_direct = 90
					Player.do_move = True
				# диагональ \ /
				case [True, True, False, False]:
					Player.speed_direct = 315
					Player.do_move = True
				case [False, True, True, False]:
					Player.speed_direct = 225
					Player.do_move = True
				case [False, False, True, True]:
					Player.speed_direct = 135
					Player.do_move = True
				case [True, False, False, True]:
					Player.speed_direct = 45
					Player.do_move = True
				case _:
					Player.speed -= 3
					Player.speed = max(0, Player.speed)
			
			if Player.do_move:
				Player.speed = Settings.DEFAULT_PLAYER_SPEED
			
			Player.speed_x = sin(radians(Player.speed_direct)) * Player.speed
			Player.speed_y = -cos(radians(Player.speed_direct)) * Player.speed
			
			Player.x += Player.speed_x
			Player.y += Player.speed_y
			
			Player.shoot_cd = Player.shoot_cd - (not not Player.shoot_cd)  # CD таймер
			SHOOTING = ButtonsInfo.LMB and not Player.shoot_cd
			if SHOOTING:
				Player.shoot_cd = Settings.DEFAULT_PLAYER_SHOOT_CD
				shoot_angle = 0.5 * pi - atan2(Player.y - ButtonsInfo.MOUSE_POS[1], ButtonsInfo.MOUSE_POS[0] - Player.x)
				spawn_pos = Player.x, Player.y
				
				new_bullet = Bullet(spawn_pos, Settings.DEFAULT_BULLET_SPEED, shoot_angle)
				
				bullets.append(new_bullet)
			
			"""
			bullets update
			"""
			i = 0
			k = len(bullets)
			while i < k:
				b = bullets[i]
				# world borders
				if 0 < b.x < Settings.SCREEN_WIDTH and 0 < b.y < Settings.SCREEN_HEIGHT:
					b.set_next_pos()
				else:
					bullets.pop(i)
					k -= 1
				i += 1
			"""
			enemy update
			"""
			i = 0
			k = len(Enemies.enemy_list)
			while i < k:
				e = Enemies.enemy_list[i]
				# world borders
				if e.hp >= 0:
					"""moving"""
					e.do_moving(target_pos=[Player.x, Player.y])
					"""damage"""
					
					ii = 0
					kk = len(bullets)
					while ii < kk:
						b = bullets[ii]
						# collision
						if dist(b.pos, e.pos) < Settings.ENEMY_SIZE / 2:
							kk -= 1
							try:
								bullets.pop(i)
							except IndexError:
								pass
							e.hp -= 4
						ii += 1
				
				else:
					Enemies.enemy_list.pop(i)
					k -= 1
				i += 1
			"""ingame menu"""
			if Settings.PAUSE:
				ingame_menu()
				ButtonsInfo.ESC = False
				ButtonsInfo.LMB = False
				ButtonsInfo.RMB = False
				ButtonsInfo.W = False
				ButtonsInfo.A = False
				ButtonsInfo.S = False
				ButtonsInfo.D = False
			"""enemy spawn"""
			if t % (Settings.FPS // Settings.SPAWNRATE) == 0:
				Enemies.enemy_list.append(Enemy(get_random_spawn_pos))
			"""RENDER"""
			draw_background()
			draw_player(pos=[Player.x, Player.y], timing=t)
			for b in bullets:
				draw_bullet(b.pos)
			for e in Enemies.enemy_list:
				draw_enemy(e.pos, degrees(e.angle) + 135)
				rects = e.get_hp_rect_args(Settings.ENEMY_SIZE)
				pg.draw.rect(sc, (0, 200, 0), rects[1], border_radius=5)
				pg.draw.rect(sc, (0, 0, 0), rects[0], 3, border_radius=5)
			
			clock.tick(Settings.FPS)
			pg.display.update()
			
	def change_render_mode():
		Settings.RENDER_MODE += 1
		if Settings.RENDER_MODE == Settings.RENDER_MODE_N:
			Settings.RENDER_MODE = 0
		buttons_settings[1] = Button(0, -50, 400, 50, f"Режим отрисовки: {Settings.RENDER_MODE + 1}-й", change_render_mode)
	
	def draw_enemy(pos, angle):
		render_sprite(texture=Textures.enemy, factor=(Settings.ENEMY_SIZE / Textures.enemy[1][1]), pos=pos, angle=angle, render_mode=Settings.RENDER_MODE)
	
	def clamp(_x, _min, _max):
		return max(_min, min(_max, _x))
	
	def clamp_player_pos():
		Player.x = clamp(Player.x, Settings.PLAYER_R, Settings.SCREEN_WIDTH - Settings.PLAYER_R)
		Player.y = clamp(Player.y, Settings.PLAYER_R, Settings.SCREEN_HEIGHT - Settings.PLAYER_R)
	
	def draw_player(pos, timing):
		line = get_outline(timing=timing)
		pg.draw.circle(sc, (155, 0, 0), pos, Settings.PLAYER_R + line // 2, 6 + line)
	
	def draw_bullet(pos):
		pg.draw.circle(sc, (0, 0, 0), pos, 10)
	
	def draw_sprite_rotated(texture, factor: int | float, pos: tuple | list, angle: float | int):
		sc.blit(*get_sprite_rotated(texture=texture, factor=factor, pos=pos, angle=angle))
	
	def get_sprite_rotated(texture, factor: int | float, pos: tuple | list, angle: float | int) -> list[
		pg.image, list[int, int]]:
		# Получение повернутого изображения
		texture = pg.transform.scale_by(surface=texture[0], factor=factor)
		texture = pg.transform.rotate(surface=texture, angle=angle)
		
		# Получение нового прямоугольника границы
		new_rect = texture.get_rect(center=(pos[0], pos[1]))  # Явно укажем центр нового прямоугольника
		
		# Возврат повернутого изображения
		return [texture, new_rect.topleft]
	
	def render_sprite(
			texture,
			factor: int | float,
			pos: tuple | list,
			angle: float | int,
			render_mode: int,
			render_engines: None = None,
	):
		if render_engines is None:
			render_engines = [draw_curved_texture, draw_sprite_rotated]
		render_engines[render_mode](texture=texture, factor=factor, pos=pos, angle=angle)
	
	def get_curved_texture(texture, factor: int | float, pos: list[int, int], angle: int | float):
		rotated = pg.transform.rotate(texture[0], angle=angle)
		scaled = pg.transform.scale_by(surface=rotated, factor=factor)
		new_rect = scaled.get_rect(center=(pos[0], pos[1]))
		return [scaled, new_rect]
	
	def draw_curved_texture(texture, factor: int | float, pos: list[int, int], angle: int | float) -> None:
		sp = get_curved_texture(texture=texture, factor=factor, pos=pos, angle=angle)
		sc.blit(*sp)
	
	def get_outline(timing: int | float) -> int:
		if timing < 120:
			return 1
		timing = timing % 60 * (pi + 1) / 60
		if timing < pi:
			return int(pow(sin(2 * timing), 10) * 3 + 1)
		else:
			return 1
	
	def draw_background():
		sc.blit(Textures.background[0], [0, 0, Settings.SCREEN_SIZE[0], Settings.SCREEN_SIZE[1]])
	
	def quit_game():
		pg.quit()
		sys.exit()
	
	def do_dark_screen():
		s = pg.Surface(Settings.SCREEN_SIZE)
		s.set_alpha(100)
		s.fill((0, 0, 0))
		sc.blit(s, (0, 0))
		pg.display.update()
	
	def start_menu():
		Settings.START_MENU_RUNNING = True
		while Settings.START_MENU_RUNNING:
			sc.fill((255, 255, 255))
			
			# Обработка событий
			for event in pg.event.get():
				if event.type == pg.QUIT:
					close_start_menu()
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_KP_ENTER:
						game()
				for button in buttons:
					button.handle_event(event)
			
			# Отрисовка кнопок
			for button in buttons:
				button.draw()
			
			pg.display.flip()
	
	def ingame_menu():
		do_dark_screen()
		Settings.INGAME_MENU_RUNNING = True
		while Settings.INGAME_MENU_RUNNING:
			pg.draw.rect(sc, (255, 255, 255), Settings.MENU_WHITE_BOX_RECT, border_radius=10)
			pg.draw.rect(sc, (100, 100, 100), Settings.MENU_WHITE_BOX_RECT, width=5, border_radius=10)
			
			# Обработка событий
			for event in pg.event.get():
				match event.type:
					case pg.QUIT:
						quit_game()
					case pg.KEYDOWN:
						if event.key == pg.K_ESCAPE:
							end_pause()
				
				for button in buttons_ingame_menu:
					button.handle_event(event)
			
			# Отрисовка кнопок
			for button in buttons_ingame_menu:
				button.draw()
			
			pg.display.update(Settings.MENU_WHITE_BOX_RECT)
	
	def white_creators_menu():
		creators_menu(dark_screen=False)
	
	def creators_menu(dark_screen=True):
		if dark_screen:
			do_dark_screen()
		Settings.CREATORS_MENU_RUNNING = True
		while Settings.CREATORS_MENU_RUNNING:
			pg.draw.rect(sc, (255, 255, 255), Settings.MENU_WHITE_BOX_RECT, border_radius=10)
			pg.draw.rect(sc, (100, 100, 100), Settings.MENU_WHITE_BOX_RECT, width=5, border_radius=10)
			
			# Обработка событий
			for event in pg.event.get():
				match event.type:
					case pg.QUIT:
						quit_game()
					case pg.KEYDOWN:
						if event.key == pg.K_ESCAPE:
							close_creator_menu()
				
				for button in buttons_creators:
					button.handle_event(event)
			
			# Отрисовка кнопок
			for button in buttons_creators:
				button.draw()
			
			pg.display.update(Settings.MENU_WHITE_BOX_RECT)
	
	def settings_menu():
		do_dark_screen()
		Settings.SETTINGS_MENU_RUNNING = True
		close_start_menu()
		ui_manager = UIManager(Settings.SCREEN_SIZE)
		
		size = [400, 20]
		offset = [0, 70]
		rect = pg.Rect(
			[Settings.SCREEN_WIDTH / 2 - size[0] / 2 + offset[0], Settings.SCREEN_HEIGHT / 2 - size[1] / 2 + offset[1],
			 size[0], size[1]])
		
		spawnrate_slider = elements.ui_horizontal_slider.UIHorizontalSlider(
			relative_rect=rect,
			start_value=Settings.SPAWNRATE,
			value_range=[0.5, 2],
			manager=ui_manager,
		)
		
		local_clock = pg.time.Clock()
		while Settings.SETTINGS_MENU_RUNNING:
			# Обработка событий
			for event in pg.event.get():
				match event.type:
					case pg.QUIT:
						quit_game()
					case pg.KEYDOWN:
						if event.key == pg.K_ESCAPE:
							close_settings_menu()
				
				for button in buttons_settings:
					button.handle_event(event)
				
				ui_manager.process_events(event)
			time_delta = local_clock.tick(Settings.FPS) / 1000
			ui_manager.update(time_delta)
			# white_rect
			pg.draw.rect(sc, (255, 255, 255), Settings.SETTINGS_WHITE_BOX_RECT, border_radius=10)
			pg.draw.rect(sc, (100, 100, 100), Settings.SETTINGS_WHITE_BOX_RECT, width=5, border_radius=10)
			
			# Отрисовка кнопок
			for button in buttons_settings:
				button.draw()
			# Отрисовка прочих элементов
			ui_manager.draw_ui(sc)
			
			# надпись
			font = pg.font.Font(Settings.TEXT_FONT_TIMES_NEW_ROMAN, Settings.FONT_SIZE)
			text = font.render("Спавнрейт врагов", True, (20, 20, 20), wraplength=spawnrate_slider.get_abs_rect().width)
			base = pg.Rect(rect[0], rect[1], *rect[2:]).center
			t_rect = text.get_rect()
			now = t_rect.center
			
			offset = [0, 50]
			
			res_rect = pg.Rect(t_rect[0] + base[0] - now[0] + offset[0], t_rect[1] + base[1] - now[0] + offset[1],
			                   *t_rect.size)
			
			sc.blit(text, res_rect)
			
			# Апдейт
			pg.display.update(Settings.SETTINGS_WHITE_BOX_RECT)
		Settings.SPAWNRATE = spawnrate_slider.current_value
		
		start_menu()
	
	def end_pause():
		Settings.INGAME_MENU_RUNNING = False
		Settings.PAUSE = False
	
	def close_start_menu():
		Settings.START_MENU_RUNNING = False
	
	def close_creator_menu():
		Settings.CREATORS_MENU_RUNNING = False
	
	def close_settings_menu():
		Settings.SETTINGS_MENU_RUNNING = False
	
	def open_git(name):
		url = f'https://github.com/{name}'
		webbrowser.open_new(url=url)
	
	def open_agl_vk():
		webbrowser.open_new("https://lomonosov-gymnasium.edusite.ru/")
	
	def open_neanod_git():
		open_git('azaz-azaz')
	
	def open_kotsem_git():
		open_git('KotSem')
	
	buttons = [
		Button(0, -60, 200, 50, "Играть", game),
		Button(0, 60, 200, 50, "Настройки", settings_menu),
		Button(0, 150, 200, 50, "Создатели", creators_menu),
		Button(0, 240, 200, 50, "Выйти", quit_game),
	]
	buttons_ingame_menu = [
		Button(0, -70, 200, 50, "Продолжить", end_pause),
		Button(0, 0, 200, 50, "Создатели", white_creators_menu),
		Button(0, 70, 200, 50, "Выйти", quit_game),
	]
	buttons_creators = [
		Button(0, -150, 200, 50, "Закрыть", close_creator_menu),
		Button(0, -70, 560, 60, "АГЛ, 9Т", open_agl_vk),
		Button(-155, 60, 250, 100, "Никита, Neanod", open_neanod_git),
		Button(155, 60, 250, 100, "Костя, Kotsem", open_kotsem_git),
	]
	buttons_settings = [
		Button(0, -150, 400, 50, "Закрыть", close_settings_menu),
		Button(0, -50, 400, 50, f"Режим отрисовки: {Settings.RENDER_MODE + 1}-й", change_render_mode),
	]
	
	start_menu()


if __name__ == '__main__':
	main()
