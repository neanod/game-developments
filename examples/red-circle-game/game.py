import random

import pygame as pg
from time import sleep
from math import sin, cos, radians, atan2, pi
from player_bullet import Bullet


def main():
	"""CONSTANTS"""
	
	class Settings:
		FPS = 60
		SCREEN_SIZE = [1920, 1080]
		
		SCREEN_WIDTH = SCREEN_SIZE[0]
		SCREEN_HEIGHT = SCREEN_SIZE[1]
		
		SCREEN_CENTER = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
		
		DEFAULT_PLAYER_SPEED = 8
		DEFAULT_PLAYER_SHOOT_CD = 2
		
		DEFAULT_BULLET_SPEED = 25
		
		PLAYER_R = 20
		
		SPAWNRATE = 1
	
	sc = pg.display.set_mode(Settings.SCREEN_SIZE)
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
	
	class Player:
		x, y = Settings.SCREEN_CENTER
		speed = 0
		speed_x = 0
		speed_y = 0
		speed_direct = 0
		do_move = False
		shoot_cd = 0
	
	class ButtonsInfo:
		W = False
		A = False
		S = False
		D = False
		
		LMB = False
		RMB = False
		
		MOUSE_POS = [0, 0]
	
	def game():
		
		game_over = False
		t = 0
		bullets = list()
		
		while not game_over:
			for event in pg.event.get():
				match event.type:
					case pg.QUIT:
						game_over = True
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
			
			"""bullets update"""
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
			
			"""RENDER"""
			draw_background()
			draw_player([Player.x, Player.y])
			for b in bullets:
				draw_bullet(b.pos)
			
			clock.tick(Settings.FPS)
			pg.display.update()
	
	def get_random_spawn_pos():
		match random.randint(0, 3):
			case 0:
				return [random.randint(0, Settings.SCREEN_WIDTH), 0]
			case 1:
				return [Settings.SCREEN_WIDTH, random.randint(0, Settings.SCREEN_HEIGHT)]
			case 2:
				return [random.randint(0, Settings.SCREEN_WIDTH), Settings.SCREEN_HEIGHT]
			case 3:
				return [0, random.randint(0, Settings.SCREEN_HEIGHT)]
				
	def clamp(_x, _min, _max):
		return max(_min, min(_max, _x))
	
	def clamp_player_pos():
		Player.x = clamp(Player.x, Settings.PLAYER_R, Settings.SCREEN_WIDTH - Settings.PLAYER_R)
		Player.y = clamp(Player.y, Settings.PLAYER_R, Settings.SCREEN_HEIGHT - Settings.PLAYER_R)
	
	def draw_player(pos):
		pg.draw.circle(sc, (155, 0, 0), pos, Settings.PLAYER_R, 6)
		
	def draw_bullet(pos):
		pg.draw.circle(sc, (0, 0, 0), pos, 10)
	
	def draw_sprite_rotated(pos: tuple | list, angle: float | int):
		sc.blit(*get_sprite_rotated(pos=pos, angle=angle))
	
	def get_sprite_rotated(pos: tuple | list, angle: float | int) -> list[pg.image, list[int, int]]:
		# Получение повернутого изображения
		texture = pg.transform.rotate(Textures.example[0],
		                              angle)  # Положительный угол для поворота по часовой стрелке
		
		# Получение нового прямоугольника границы
		new_rect = texture.get_rect(center=(pos[0], pos[1]))  # Явно укажем центр нового прямоугольника
		
		# Возврат повернутого изображения
		return [texture, new_rect.topleft]
	
	def get_curved_texture(texture, factor: int | float, pos: list[int, int], angle: int | float):
		rotated = pg.transform.rotate(texture[0], angle=angle)
		scaled = pg.transform.scale_by(surface=rotated, factor=factor)
		new_rect = scaled.get_rect(center=(pos[0], pos[1]))
		return [scaled, new_rect]
	
	def draw_curved_texture(texture, factor: int | float, pos: list[int, int], angle: int | float) -> None:
		sp = get_curved_texture(texture=texture, factor=factor, pos=pos, angle=angle)
		sc.blit(*sp)
	
	def draw_background():
		sc.blit(Textures.background[0], [0, 0, Settings.SCREEN_SIZE[0], Settings.SCREEN_SIZE[1]])
	
	game()


if __name__ == '__main__':
	main()
