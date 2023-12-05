from sets import Sets
from math import hypot
from numpy import cross, ndarray
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
	if n <= water_level:
		minimum = 50
		r = g = 0
		b = clamp(int(n / water_level * (255 - minimum) + minimum), 0, 255)
		return pg.Color(r, g, b)
	r = min(255, int((((n + 0.3) / amplitude) ** 5) * 455))
	g = 200
	b = 0
	return pg.Color(r, g, b)


def exit_game():
	pg.quit()
	quit(0)


class Vec2:
	def __init__(self, xy):
		"""
		vector in 2 dimensions
		:type xy: tuple[int|float, int|float] | list[int|float, int|float]
		:param xy: position
		"""
		self.x, self.y = xy
	
	def __abs__(self):
		return hypot(self.x, self.y)
	
	def __iadd__(self, other):
		self.x += other[0]
		self.y += other[1]
		return self
	
	def __isub__(self, other):
		self.x -= other[0]
		self.y -= other[1]
		return self
	
	def __imul__(self, other):
		if isinstance(other, (int, float)):
			self.x *= other
			self.y *= other
		elif isinstance(other, (tuple, list)):
			self.x, self.y = cross(self.xy, other)
		return self
	
	def __add__(self, other) -> tuple:
		return self.x + other[0], self.y + other[1]
	
	def __sub__(self, other) -> tuple:
		return self.x - other[0], self.y - other[1]
	
	def __mul__(self, other) -> ndarray | tuple:
		if isinstance(other, (int, float)):
			return self.x * other, self.y * other
		return cross(self.xy, other)
	
	def __truediv__(self, other: int | float):
		return self.x / other, self.y / other
	
	def __floordiv__(self, other: int | float):
		return int(self.x // other), int(self.y // other)
	
	def __radd__(self, other) -> tuple:
		return self.x + other[0], self.y + other[1]
	
	def __rsub__(self, other) -> tuple:
		return self.x - other[0], self.y - other[1]
	
	def __rmul__(self, other) -> ndarray | tuple:
		if isinstance(other, (int, float)):
			return self.x * other, self.y * other
		return cross(self.xy, other)
	
	@property
	def xy(self):
		return self.x, self.y
	