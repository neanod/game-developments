import pygame as pg
from math import *
from f.scripts.bullet import Bullet


clamp = lambda _x, _min, _max: min(_max, max(_min, _x))


def main():
	"""--------------------------------------
	# setup----------------------------------
	--------------------------------------"""
	# init
	timer = 0
	playerRadius = 20
	defaultPlayerSpeed = 8
	default_shoot_delay = 0.1
	game_over = False
	player_angle = 0
	shoot_delay = 0
	screenWidth = 1920
	screenHeight = 1080
	player_y = screenHeight / 2
	player_x = screenWidth / 2
	bullet_size = 3
	bullets = []
	default_bullet_speed = 32
	#   screen
	pg.init()
	screenSize = (screenWidth, screenHeight)
	clock = pg.time.Clock()
	FPS = 60
	sc = pg.display.set_mode(screenSize)
	#   sprite loading
	textures = {
		'cloud': pg.image.load("f/sprites/cloud.png").convert_alpha(),
		'back': pg.transform.scale(pg.image.load("f/sprites/background.png"), screenSize).convert_alpha(),
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
		offset = (bullet_size * (sin(radians(angle % 90)) + cos(radians((angle % 90)))) - bullet_size) * 0.5
		sprite = pg.transform.rotate(textures['bullet'], angle)
		sc.blit(sprite, [
			pos[0] - offset,
			pos[1] - offset,
			pos[0] + bullet_size + offset,
			pos[1] + bullet_size + offset,
		])
	
	def get_outline(timing: int | float) -> int:
		if timing < 2 * FPS:
			return 1
		timing = timing % FPS * (pi + 1) / FPS
		if timing < pi:
			return pow(sin(2 * timing), 10) * 3 + 1
		else:
			return 1
	
	def draw_player(pos: tuple | list):
		pg.draw.circle(sc, (0, 80, 0), pos, get_outline(timer) + playerRadius)
		pg.draw.circle(sc, (0, 170, 0), pos, playerRadius - 2)
	
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
					shoot = False
		"""
		LOGIC
		"""
		timer += 1
		
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
		player_y += cos(radians(player_angle)) * player_speed
		player_x += sin(radians(player_angle)) * player_speed
		# -screen borders
		player_x = clamp(player_x, playerRadius, screenWidth - playerRadius)
		player_y = clamp(player_y, playerRadius, screenHeight - playerRadius)
		"""shooting"""
		if shoot and not shoot_delay:
			mouse_pos = pg.mouse.get_pos()
			shoot_angle = -atan2((mouse_pos[1] - player_y), (mouse_pos[0] - player_x)) + pi / 2
			bullets.append(Bullet(shoot_angle, default_bullet_speed, player_x, player_y))
			shoot_delay = default_shoot_delay * FPS
			
		shoot_delay -= not not shoot_delay
		# bullet logic
		i = 0
		bullets_n = len(bullets)
		while i < bullets_n:
			b = bullets[i]
			b.set_next_pos()
			if (not 0 < b.x < screenWidth) | (not 0 < b.y < screenHeight):
				bullets.pop(i)
				bullets_n -= 1
			else:
				i += 1
		"""
		RENDER
		"""
		sc.blit(textures['back'], [0, 0, screenWidth, screenHeight])
		draw_player([player_x, player_y])
		for b in bullets:
			pg.draw.circle(sc, b.color, b.pos, bullet_size)
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
