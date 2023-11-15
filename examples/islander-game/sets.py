from perlin_noise import PerlinNoise
from random import randint


class ButtonsInfo:
	LMB = False
	RMB = False
	m_pos = [0, 0]


class Sets:
	FPS: int = 60
	# square_size in [120, 60, 40, 30, 24, 20, 12, 10, 5, 2, 1]
	square_size: int = 10
	matching = True
	
	noise = PerlinNoise(octaves=12, seed=randint(1000, 1000000))
	#noise = PerlinNoise(octaves=6, seed=randint(1000, 1000000))
	
	class Sc:
		res: list[int] = [1920, 1080]
		width: int = res[0]
		height: int = res[1]
		h_width: int = width // 2
		h_height: int = height // 2
		center: list[int] = [h_width, h_height]
	
	amp = 1.6
	period = 2500 / square_size


class SelectedInfo:
	LMB_POS = None
	RMB_POS = None
	

if __name__ == '__main__':
	input("Это не основной файл. Откройте IslandCapture.py")
