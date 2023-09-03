import random
import time
import pygame as pg
import random as rand
from math import *
from bullet_class import Bullet

clamp = lambda _x, _min, _max: min(_max, max(_min, _x))



def main():
	"""--------------------------------------
	# setup----------------------------------
	--------------------------------------"""
	#   screen
	pg.init()
	screenWidth = 1920
	screenHeight = 1080
	screenSize = (screenWidth, screenHeight)
	clock = pg.time.Clock()
	#   settings
	game_over = False
	undying_ticks = 60 * 2
	started = time.perf_counter()
	BPS = 8
	FPS = 60
	playerRadius = 20
	bulletSize = 32
	defaultPlayerSpeed = 8
	defaultBulletSpeed = 3
	bulletSpread = 10  # degrees
	#   other
	timer = 0
	player_angle = 0
	player_x = screenWidth * 0.5
	player_y = screenHeight * 0.5
	uber_unter_sphielen_sphielin_sphielin = 0
	default_shoot_delay = 50
	shoot_delay = 0
	player_bullet_timer = 0
	player_bullet_pos = [0, 0]
	
	sc = pg.display.set_mode(screenSize)
	#   sprite loading
	textures = {
		'bullet': pg.transform.scale(pg.image.load("f/sprites/bullet.png"), (bulletSize, bulletSize)).convert_alpha(),
		'background': pg.transform.scale(pg.image.load("f/sprites/background.jpg"), screenSize).convert_alpha(),
	}
	#   movement_buttons preset
	movement_buttons = {
		'w': False,
		'a': False,
		's': False,
		'd': False,
	}
	shoot = False
	
	#   functions
	
	def draw_bullet(pos: tuple | list, angle: float | int) -> None:
		offset = (bulletSize * (sin(radians(angle % 90)) + cos(radians((angle % 90)))) - bulletSize) * 0.5
		sprite = pg.transform.rotate(textures['bullet'], angle)
		sc.blit(sprite, [
			pos[0] - offset,
			pos[1] - offset,
			pos[0] + bulletSize + offset,
			pos[1] + bulletSize + offset,
		])
	
	def get_outline(timing: int | float) -> int:
		if timing < 120:
			return 1
		timing = timing % 60 * (pi + 1) / 60
		if timing < pi:
			return pow(sin(2 * timing), 10) * 3 + 1
		else:
			return 1
	
	def draw_player(pos: tuple | list, und_ticks: bool = False):
		pg.draw.circle(sc, (255, 255, 0) if und_ticks else (0, 80, 0), pos, get_outline(timer) + playerRadius)
		pg.draw.circle(sc, (0, 170, 0), pos, playerRadius - 2)
	
	def get_bullet_spawn_pos(_n: int):
		if _n < screenWidth:
			return _n, -bulletSize
		elif _n < screenWidth + screenHeight:
			return 1920, _n - screenWidth - bulletSize
		elif _n < 2 * screenWidth + screenHeight:
			return _n - (screenWidth + screenHeight), screenHeight,
		else:
			return -bulletSize, _n - (2 * screenWidth + screenHeight)
	
	bullets: list[Bullet] = []
	"""--------------------------------------
	# game-----------------------------------
	--------------------------------------"""
	while not game_over:
		for event in pg.event.get():
			match event.type:
				case pg.QUIT:
					game_over = True
				case pg.KEYDOWN:
					match event.key:
						case pg.K_w:
							movement_buttons['w'] = True
						case pg.K_a:
							movement_buttons['a'] = True
						case pg.K_s:
							movement_buttons['s'] = True
						case pg.K_d:
							movement_buttons['d'] = True
				case pg.KEYUP:
					match event.key:
						case pg.K_w:
							movement_buttons['w'] = False
						case pg.K_a:
							movement_buttons['a'] = False
						case pg.K_s:
							movement_buttons['s'] = False
						case pg.K_d:
							movement_buttons['d'] = False
				case pg.MOUSEBUTTONDOWN:
					shoot = True
				case pg.MOUSEBUTTONUP:
					print("hell")
		"""
		LOGIC
		"""
		timer += 1
		# bullet spawn
		if not timer % int(60 / BPS):
			# spawn bullet
			t_pos = get_bullet_spawn_pos(rand.randint(0, 2 * sum(screenSize) - 1))
			bullet_angle = radians(rand.randint(-bulletSpread, +bulletSpread))  # radians
			bullet_angle += 2.5 * pi - atan2(player_y - t_pos[1], player_x - t_pos[0])
			new_bullet = \
				Bullet(t_pos, degrees(bullet_angle) + random.randint(-int(radians(bulletSpread * 1000)),
				                                                     ceil(radians(bulletSpread * 1000)))
				       / dist([
					player_x,
					player_y
				], t_pos), defaultBulletSpeed, bulletSize)
			
			bullets.append(new_bullet)
		# унтер Шпилин тикс
		uber_unter_sphielen_sphielin_sphielin -= uber_unter_sphielen_sphielin_sphielin > 0
		"""bullet movement"""
		for bt in bullets:
			if bt.check_out_of_screen(screenSize):
				bullets.pop(bullets.index(bt))
				continue
			bt.x, bt.y = bt.next_pos
			# -bullets damage
			if dist(bt.pos, [player_x, player_y]) < bulletSize / 2 + playerRadius - 8:
				if uber_unter_sphielen_sphielin_sphielin:
					from pickle import dump, load
					game_time = round(timer / 60, 2)
					with open('save.pickle', 'rb') as f:
						best_result: int = load(f)
					if best_result < game_time:
						print(f"new record: {game_time}s")
						with open('save.pickle', 'wb') as f:
							dump(game_time, f)
					else:
						print(f"time: {game_time}s")
					pg.time.delay(1000)
					game_over = True
				uber_unter_sphielen_sphielin_sphielin = undying_ticks
				bullets.pop(bullets.index(bt))
		# bt.angle = degrees(2.5 * pi - atan2(player_y - bt.y, player_x - bt.x)) # TODO: УБРАТЬ
		
		"""player movement"""
		# buttons
		player_speed = defaultPlayerSpeed
		match list(movement_buttons.values()):
			case [1, 0, 0, 0] | [1, 1, 0, 1]:
				player_angle = 180
			case [0, 1, 0, 0] | [1, 1, 1, 0]:
				player_angle = 270
			case [0, 0, 1, 0] | [0, 1, 1, 1]:
				player_angle = 0
			case [0, 0, 0, 1] | [1, 0, 1, 1]:
				player_angle = 90
			case [1, 1, 0, 0]:
				player_angle = 225
			case [0, 1, 1, 0]:
				player_angle = 315
			case [0, 0, 1, 1]:
				player_angle = 45
			case [1, 0, 0, 1]:
				player_angle = 135
			case _:
				player_speed = 0
		# move
		player_x += sin(radians(player_angle)) * player_speed
		player_y += cos(radians(player_angle)) * player_speed
		# -screen borders
		player_x = clamp(player_x, playerRadius, screenWidth - playerRadius)
		player_y = clamp(player_y, playerRadius, screenHeight - playerRadius)
		"""shooting"""
		if shoot and not shoot_delay:
			mouse_pos = pg.mouse.get_pos()
			shoot_angle_aspect = (mouse_pos[1] - player_y) / (mouse_pos[0] - player_x)
		# TODO
		else:
			shoot_delay = default_shoot_delay
		"""
		RENDER
		"""
		sc.blit(textures['background'], [0, 0, screenWidth, screenHeight])
		draw_player([player_x, player_y], not not uber_unter_sphielen_sphielin_sphielin)
		"""bullets render"""
		for bt in bullets:
			draw_bullet(bt.draw_pos, bt.angle)
		# --temp--
		
		# update
		pg.display.flip()
		"""
		FPS
		"""
		clock.tick(FPS)
	
	"""--------------------------------------
	# endgame--------------------------------
	--------------------------------------"""
	print('game over')


if __name__ == '__main__':
	main()
