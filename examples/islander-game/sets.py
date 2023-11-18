from perlin_noise import PerlinNoise
from random import randint
import pygame as pg


class ButtonsInfo:
	LMB = False
	RMB = False
	W = False
	A = False
	S = False
	D = False
	
	m_pos: tuple[int, int] = 0, 0


class Sets:
	FPS: int = 60
	# square_size in [120, 60, 40, 30, 24, 20, 12, 10, 5, 2, 1]
	square_size: int = 17
	matching: bool = True
	
	spawn_zone: float = 6.0
	water_level: float = 0.85
	
	gen_dist: int = -3
	noise: PerlinNoise = PerlinNoise(octaves=15, seed=randint(10000, 1000000))
	amp: float = 1.6
	period: float = 1500 / square_size
	
	class Sc:
		res: list[int, int] = [1920 - 200, 1080 - 200]
		# res: list[int, int] = [1920, 1080]
		width: int = res[0]
		height: int = res[1]
		h_width: int = width // 2
		h_height: int = height // 2
		center: list[int, int] = [h_width, h_height]
		
		cam_to_player_box_size: list[int, int] = [h_width // 2, h_height // 2]
		cam_to_player_box: pg.Rect = pg.Rect(
			[
				h_width - cam_to_player_box_size[0] * 0.5,
				h_height - cam_to_player_box_size[1] * 0.5,
				*cam_to_player_box_size,
			]
		)


class SelectedInfo:
	LMB_POS = None
	RMB_POS = None


if __name__ == '__main__':
	input("Это не основной файл. Откройте IslandCapture.py")
