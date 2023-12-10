from sets import Sets
from math import sqrt, hypot, pi, atan2
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
	Sets.running = False
	pg.quit()
	quit(0)


def collisionCircleLine(circle, line):
	side1 = sqrt((circle['x'] - line['p1']['x']) ** 2 + (circle['y'] - line['p1']['y']) ** 2)
	side2 = sqrt((circle['x'] - line['p2']['x']) ** 2 + (circle['y'] - line['p2']['y']) ** 2)
	base = sqrt((line['p2']['x'] - line['p1']['x']) ** 2 + (line['p2']['y'] - line['p1']['y']) ** 2)
	
	if circle['radius'] > side1 or circle['radius'] > side2:
		return True
	
	angle1 = atan2(line['p2']['x'] - line['p1']['x'], line['p2']['y'] - line['p1']['y']) - atan2(
		circle['x'] - line['p1']['x'], circle['y'] - line['p1']['y'])
	angle2 = atan2(line['p1']['x'] - line['p2']['x'], line['p1']['y'] - line['p2']['y']) - atan2(
		circle['x'] - line['p2']['x'], circle['y'] - line['p2']['y'])
	
	if angle1 > pi / 2 or angle2 > pi / 2:
		return False
	
	semiperimeter = (side1 + side2 + base) / 2
	areaOfTriangle = sqrt(semiperimeter * (semiperimeter - side1) * (semiperimeter - side2) * (semiperimeter - base))
	height = 2 * areaOfTriangle / base
	
	return height < circle['radius']


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
		if isinstance(other, type(self)):
			return self.x + other.x, self.y + other.y
		elif isinstance(other, (int, float)):
			return self.x + other, self.y + other
		elif isinstance(other, (tuple, list)):
			return self.x + other[0], self.y + other[1]
	
	def __sub__(self, other) -> tuple:
		if isinstance(other, type(self)):
			return self.x - other.x, self.y - other.y
		elif isinstance(other, (int, float)):
			return self.x - other, self.y - other
		elif isinstance(other, (tuple, list)):
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


if __name__ == '__main__':
	def test_collisionCircleLine():
		circle = {'x': 0, 'y': 0, 'radius': 1}
		line = {'p1': {'x': -1, 'y': -1}, 'p2': {'x': 1, 'y': 1}}
		
		assert collisionCircleLine(circle, line) == True
		
		circle = {'x': 0, 'y': 0, 'radius': 1}
		line = {'p1': {'x': -2, 'y': -2}, 'p2': {'x': 2, 'y': 2}}
		
		assert collisionCircleLine(circle, line) == False
		
		print("All tests passed.")
	
	
	test_collisionCircleLine()
