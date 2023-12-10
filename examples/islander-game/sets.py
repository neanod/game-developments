from math import dist

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
	mwheel: int = 0


class Sets:
	running = True
	t = 0
	FPS: int = 60
	# square_size in [120, 60, 40, 30, 24, 20, 12, 10, 5, 2, 1]
	square_size: int = 15
	matching: bool = True
	enemy_spawn_chance = 0.0008
	
	spawn_zone: float = 0
	
	gen_dist: int = 10
	seed = randint(
			100000000,
			999999999
	)
	noise: PerlinNoise = PerlinNoise(
		octaves=5,
		seed=seed,
	)
	# noise: PerlinNoise = PerlinNoise(
	# 	octaves=12,
	# 	seed=seed,
	# )
	period: float = 2500 / square_size
	amp: float = 2
	water_level: float = 1.2
	
	class Sc:
		res: list[int, int] = [1920 - 200, 1080 - 200]
		# res: list[int, int] = [1920, 1080]
		width: int = res[0]
		height: int = res[1]
		h_width: int = width // 2
		h_height: int = height // 2
		center: list[int, int] = [h_width, h_height]
		
		cam_to_player_box_size: list[int, int] = [h_width // 4, h_height // 4]
		cam_to_player_box: pg.Rect = pg.Rect(
			[
				h_width - cam_to_player_box_size[0] * 0.5,
				h_height - cam_to_player_box_size[1] * 0.5,
				*cam_to_player_box_size,
			]
		)
		
	class II:
		a_star_min = 110
		a_star_max = ...
		# max distance between end point of way and target
		delta_offset_f = lambda __p, __q: dist(__p.xy, __q.xy) > 100
	II.a_star_max = Sc.width // 2
	

class SelectedInfo:
	LMB_POS = None
	RMB_POS = None


if __name__ == '__main__':
	input("Это не основной файл. Откройте IslandCapture.py")
