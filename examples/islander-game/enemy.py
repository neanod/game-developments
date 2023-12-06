from math import sqrt, sin, cos, atan2, degrees, dist
from matan import Vec2
from sets import Sets
from pygame import draw, Surface, Color, Rect, image, transform
import pygame_gui


money = image.load('texture/money.png')


class Drop(Vec2):
	def __init__(self, xy: tuple, drop_list: list, sc: Surface, value: int):
		super().__init__(xy)
		self.another_drop = drop_list
		self.scale_k = 1
		self.texture = transform.scale(
			money.convert_alpha(),
			[int(Sets.square_size * self.scale_k)] * 2,
		)
		self.sc = sc
		self.value = value
	
	@property
	def xy(self) -> tuple:
		return self.x * Sets.square_size, self.y * Sets.square_size
	
	@property
	def center(self) -> tuple:
		return (self.x + 0.5) * Sets.square_size, (self.y + 0.5) * Sets.square_size
		
	def render(self, offset: tuple):
		self.sc.blit(
			money,
			[
				*(Vec2(self.xy) - offset)
			]
		)
	
	def death(self):
		self.another_drop.remove(self)


class Enemy:
	def __init__(self, sc, x=None, y=None, color=None, speed_def=None, world_map=None, path_find_f=None, max_hp=64,
	             all_enemies=None, list_to_drop=None) -> None:
		"""
		:type x: int | float
		:type y: int | float
		:type color: list[int, int, int] | tuple[int, int, int]
		:type speed_def: int | float
		:type world_map: dict[tuple[int, int], float
		:type path_find_f: FunctionType
		:type all_enemies: list[Enemy]
		"""
		
		class RP:
			hp_bar_relative = Rect((0, 0), (7 * Sets.square_size, 1.5 * Sets.square_size))
			draw_path = False
			hp_bar_offset = Vec2((-hp_bar_relative.width * 0.5, -Sets.square_size * 2.5))

		if list_to_drop is None:
			list_to_drop = []
		if all_enemies is None:
			all_enemies = []
		if color is None:
			color = 255, 0, 0
		p = x, y
		if x is None or y is None:
			p = Sets.Sc.center
		if speed_def is None:
			speed_def = 12
		
		self.RenderProperties = RP
		
		self.enemy_list = all_enemies
		self.list_to_drop = list_to_drop
		self.max_hp = max_hp
		self.hp = max_hp
		self.manager = pygame_gui.UIManager(Sets.Sc.res)
		self.hp_bar = pygame_gui.elements.UIProgressBar(
			relative_rect=self.RenderProperties.hp_bar_relative,
			manager=self.manager
		)
		self.hp_bar.border_colour = self.hp_bar.text_colour = Color(0, 0, 0)
		self.hp_bar.text_shadow_colour = Color(100, 100, 100)
		self.hp_bar.bar_filled_colour = Color(0, 200, 0)
		self.hp_bar.bar_unfilled_colour = Color(200, 0, 0)
		self.color = Color(color)
		self.rangle = .0
		self.pos = Vec2(p)
		self.speed_def = speed_def
		self.speed = speed_def
		self.sq2 = sqrt(2) / 2
		self.world_map = world_map
		self.path: list[tuple[int, int]] = list()
		self.find_path = path_find_f
		self.sc = sc
		self.drop = Drop(self.bpos(), self.list_to_drop, self.sc, 100)
		
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
		
	def death(self):
		self.enemy_list.remove(self)
		self.drop.x, self.drop.y = self.pos // Sets.square_size
		self.list_to_drop.append(self.drop)
		
	def render(self, sc: Surface, offset):
		draw.circle(
			surface=sc,
			color=self.color,
			center=self.pos - offset,
			radius=int(Sets.square_size // 1.2),
			width=int(Sets.square_size // 1.8),
		)
		self.hp_bar.set_position(Vec2(self.RenderProperties.hp_bar_offset + self.xy) - offset)
		self.manager.draw_ui(self.sc)
		if self.RenderProperties.draw_path and self.path:
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
		self.hp -= 0.5  # Temp
		if self.hp <= 0:
			self.death()
		self.hp_bar.set_current_progress(self.hp / self.max_hp * 100)
		self.manager.update(1 / Sets.FPS)
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
