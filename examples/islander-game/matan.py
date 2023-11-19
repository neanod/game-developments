from numpy import sqrt

from sets import Sets
import pygame as pg


def clamp(_x, _min, _max):
	return max(_min, min(_max, _x))


def get_clicked_rectangle(pos, offset):
	x = (pos[0] + offset[0]) // Sets.square_size
	y = (pos[1] + offset[1]) // Sets.square_size
	return x, y


def sum_list(m: list[list]) -> list:
	res = list()
	for i in range(len(m[0])):
		res.append(sum([m[x][i] for x in range(len(m))]))
	return res


def get_camera_offset(camera_pos):
	return camera_pos[0] - Sets.Sc.h_width, camera_pos[1] - Sets.Sc.h_height


def get_color(n) -> pg.Color:
	"""
	:param n: Height
	:type n: float
	:return: color
	"""
	amplitude = Sets.amp
	water_level = Sets.water_level
	if n < water_level:
		minimum = 50
		b = int(n / water_level * (255 - minimum) + minimum)
		return pg.Color(0, 0, b)
	r = min(255, int((((n + 0.3) / amplitude) ** 5) * 455))
	g = 200
	b = 0
	return pg.Color(r, g, b)


def exit_game():
	pg.quit()
	quit(0)

