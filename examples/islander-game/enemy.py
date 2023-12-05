from math import sqrt, sin, cos, atan2, degrees, dist, pi
from matan import Vec2
from sets import Sets
from pygame import draw, Surface, Color


class Enemy:
	def __init__(self, x=None, y=None, color=None, speed_def=None, world_map=None, path_find_f=None) -> None:
		"""
		:type x: int | float
		:type y: int | float
		:type color: list[int, int, int] | tuple[int, int, int]
		:type speed_def: int | float
		:type world_map: dict[tuple[int, int], float]
		:type path_find_f: FunctionType
		"""
		if color is None:
			color = 255, 0, 0
		p = x, y
		if x is None or y is None:
			p = Sets.Sc.center
		if speed_def is None:
			speed_def = 12
		self.color = Color(color)
		self.rangle = .0
		self.pos = Vec2(p)
		self.speed_def = speed_def
		self.speed = speed_def
		self.sq2 = sqrt(2) / 2
		self.world_map = world_map
		self.path: list[tuple[int, int]] = list()
		self.find_path = path_find_f
	
	@property
	def speed_x(self) -> float:
		return self.speed * sin(self.rangle)
	
	@property
	def speed_y(self) -> float:
		return -self.speed * cos(self.rangle)
	
	@property
	def speed_dim(self) -> tuple[float, float]:
		return self.speed_x, self.speed_y
	
	@property
	def x(self) -> int | float:
		return self.pos.x
	
	@property
	def y(self) -> int | float:
		return self.pos.y
	
	@property
	def x(self) -> int | float:
		return self.pos.x
	
	@property
	def bx(self):
		return self.pos.x // Sets.square_size
	
	@property
	def by(self):
		return self.pos.y // Sets.square_size
	
	@property
	def xy(self) -> tuple[int | float, int | float]:
		return self.pos.xy
	
	@property
	def dangle(self) -> float:
		"""
		Angle of movement in degrees
		:return: degrees
		"""
		return degrees(self.rangle)
	
	def bpos(self) -> tuple[int, int]:
		return int(self.x // Sets.square_size), int(self.y // Sets.square_size)
	
	def update_path(self, target: Vec2) -> None:
		"""
		Updates the path to player or any other target you want
		:param target: target pos in vector
		:return: None
		"""
		self.path = self.find_path(self.bpos(), target // Sets.square_size, world_map=self.world_map)
	
	def render(self, sc: Surface, offset):
		draw.circle(
			surface=sc,
			color=self.color,
			center=self.pos - offset,
			radius=Sets.square_size // 1.2,
			width=min(10, Sets.square_size // 4),
		)
		return
		if self.path:
			if self.path.__len__() > 1:
				draw.aalines(
					surface=sc,
					color=(255, 255, 255),
					closed=False,
					points=[
						[
							(i[0] + 0.5) * Sets.square_size - offset[0],
							(i[1] + 0.5) * Sets.square_size - offset[1]
						] for i in self.path
					],
				)
	
	def logic(self, target: Vec2 = None):
		if target is not None:
			d = dist(self.xy, target.xy)
			if d < Sets.II.a_star_max:
				self.speed = self.speed_def
				if self.speed_def + 1 < d < Sets.II.a_star_min:
					self.rangle = -atan2(*(self.pos - target.xy))
					self.path = list()
				else:
					if Sets.II.delta_offset_f(self, target):
						# reconstruct path
						self.update_path(target=target)
					# angle calc
					if self.path is None or len(self.path) < 2:
						self.speed = 0
						return
					
					to = Vec2(Vec2(self.path[1]) + (0.5, 0.5)) * Sets.square_size
					if dist(self.xy, Vec2(self.path[0]) * Sets.square_size) < self.speed_def * 6:
						self.path.pop(0)
					
					self.rangle = -atan2(*(self.pos - to))
			else:
				self.speed = 0
				self.path = list()
		self.pos += self.speed_dim


if __name__ == '__main__':
	input("Этот файл не предназначен для запуска")
