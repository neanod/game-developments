from numpy import sin, cos, arctan2
from math import dist
from sets import Sets
from pygame import draw, Surface, Color


class Enemy:
	def __init__(self, x=None, y=None, color=None, speed_def=None, angle=None, path_find_algo=None) -> None:
		"""
		:type x: int | float
		:type y: int | float
		:type color: list[int, int, int] | tuple[int, int, int] | Color
		:type speed_def: int | float
		:type angle: int | float
		:param angle: up, up-right, right, down-right, down, down-left, left, up-left
		:type path_find_algo: FunctionType
		:param path_find_algo: a* algo to find path
		"""
		if color is None:
			color = 255, 0, 0
		if x is None or y is None:
			x, y = Sets.Sc.center
		if speed_def is None:
			speed_def = 12
		if angle is None:
			angle = 0
		self.color = color
		self.x, self.y = [int(x), int(y)]
		self.speed_def = speed_def
		self.speed = speed_def
		self.angle = angle
		
		self.find_path = path_find_algo  # start_pos, end_pos, world_map
		self.target_x = 0
		self.target_y = 0
		
		self.t = 0
		self.path: tuple[tuple[int, int]] = ()
	
	@property
	def pos(self) -> tuple[int, int]:
		return self.x, self.y
	
	@property
	def speed_x(self):
		return self.speed * sin(self.angle)
	
	@property
	def speed_y(self):
		return -self.speed * cos(self.angle)
	
	@property
	def speed_dim(self) -> tuple[int | float, int | float]:
		"""
		:return: Next tick position
		"""
		return self.speed_x, self.speed_y
	
	def render(self, sc: Surface, offset) -> None:
		draw.circle(
			surface=sc,
			color=self.color,
			center=[
				self.x - offset[0],
				self.y - offset[1],
			],
			radius=Sets.square_size,
		)
	
	def go_to_target(self) -> None:
		self.angle = arctan2(self.target_y - self.y, self.x - self.target_x)
	
	def update_way_to_target(self, tx: int | float, ty: int | float) -> None:
		"""
		:param tx: target x in A system
		:param ty: target y in A system
		:return: None
		"""
		if (d := dist(self.pos, (tx, ty))) < Sets.II.a_star_max:
			if d < Sets.II.a_star_min:
				self.target_x, self.target_y = tx, ty
				self.go_to_target()
			else:
				self.t += 1
				if not self.t % Sets.FPS:
					# TODO: update path & reformat pos to относительную систему "А"
					...
				# TODO определение пройденных точек
				# TODO перемещение к первому блоку пути
		
	def logic(self):
		self.x += self.speed_x
		self.y += self.speed_y


if __name__ == '__main__':
	input("Этот файл не предназначен для запуска")
