import pygame as pg
from time import sleep
from math import sin, cos, radians


def main():
	"""CONSTANTS"""
	
	class Settings:
		FPS = 60
		SCREEN_SIZE = [1920, 1080]
		
		SCREEN_WIDTH = SCREEN_SIZE[0]
		SCREEN_HEIGHT = SCREEN_SIZE[1]
	
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
	
	def get_sprite_rotated(pos: tuple | list, angle: float | int) -> list[pg.image, list[int, int]]:
		# Получение повернутого изображения
		texture = pg.transform.rotate(Textures.example[0], angle)  # Положительный угол для поворота по часовой стрелке
		
		# Получение нового прямоугольника границы
		new_rect = texture.get_rect(center=(pos[0], pos[1]))  # Явно укажем центр нового прямоугольника
		
		# Возврат повернутого изображения
		return [texture, new_rect.topleft]
	
	def draw_sprite_rotated(pos: tuple | list, angle: float | int):
		sc.blit(*get_sprite_rotated(pos=pos, angle=angle))
	
	def get_curved_texture(texture, factor: int | float, pos: list[int, int], angle: int | float):
		rotated = pg.transform.rotate(texture[0], angle=angle)
		scaled = pg.transform.scale_by(surface=rotated, factor=factor)
		new_rect = scaled.get_rect(center=(pos[0], pos[1]))
		return [scaled, new_rect]
	
	def draw_curved_texture(texture, factor: int | float, pos: list[int, int], angle: int | float) -> None:
		sp = get_curved_texture(texture=texture, factor=factor, pos=pos, angle=angle)
		sc.blit(*sp)
		pg.draw.rect(sc, (0, 0, 0), sp[1], width=3)
	
	def draw_background():
		sc.blit(Textures.background[0], [0, 0, Settings.SCREEN_SIZE[0], Settings.SCREEN_SIZE[1]])
	
	def render_example():
		game_over = False
		t = 0
		while not game_over:
			for event in pg.event.get():
				match event.type:
					case pg.QUIT:
						game_over = True
			t += 1
			"""RENDER"""
			draw_background()
			
			draw_curved_texture(Textures.example, 10, [Settings.SCREEN_WIDTH / 2, Settings.SCREEN_HEIGHT / 2],
			                    t / 2)
			
			clock.tick(Settings.FPS)
			pg.display.update()
	
	render_example()


if __name__ == '__main__':
	main()
