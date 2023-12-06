from math import sqrt, dist
from matan import Vec2, clamp
from sets import Sets
import pygame as pg
from enemy import Drop


class Player:
	def __init__(self, x=None, y=None, color=None, speed_def=None, facing=None, land=None) -> None:
		"""
		:type x: int | float
		:type y: int | float
		:type color: list[int, int, int] | tuple[int, int, int]
		:type speed_def: int | float
		:type facing: str
		:param facing: up, up-right, right, down-right, down, down-left, left, up-left
		"""
		self.score = 0
		self.land = land
		self.font = 'arial'
		self.sword_texture = None
		if color is None:
			color = 255, 255, 255
		if x is None or y is None:
			p = Sets.Sc.center
		if speed_def is None:
			speed_def = 12
		if facing is None:
			facing = 'up'
		if land is None:
			raise ValueError("Player initialised without worldmap")
		p = x, y
		self.land = land
		self.color = color
		self.pos = Vec2(p)
		self.speed_def = speed_def
		self.speed = speed_def
		self.facing = facing
		self.sq2 = sqrt(2) / 2
		self.sword_angle = .0
		self.show_sword = True
	
	@property
	def speed_x(self):
		match self.facing:
			case 'up':
				return 0
			case 'up-right':
				return self.speed * self.sq2
			case 'right':
				return self.speed
			case 'down-right':
				return self.speed * self.sq2
			case 'down':
				return -0
			case 'down-left':
				return -self.speed * self.sq2
			case 'left':
				return -self.speed
			case 'up-left':
				return -self.speed * self.sq2
			case _:
				raise ValueError(f"invalid player angle \"{self.facing}\"")
	
	@property
	def speed_y(self):
		match self.facing:
			case 'up':
				return -self.speed
			case 'up-right':
				return -self.speed * self.sq2
			case 'right':
				return 0
			case 'down-right':
				return self.speed * self.sq2
			case 'down':
				return self.speed
			case 'down-left':
				return self.speed * self.sq2
			case 'left':
				return 0
			case 'up-left':
				return -self.speed * self.sq2
	
	@property
	def speed_dim(self):
		return self.speed_x, self.speed_y
	
	@property
	def x(self) -> int | float:
		return self.pos.x
	
	@property
	def y(self) -> int | float:
		return self.pos.y
	
	def render(self, sc: pg.Surface, offset):
		pg.draw.circle(
			surface=sc,
			color=self.color,
			center=self.pos - offset,
			radius=Sets.square_size // 1.5,
			width=5,
		)
		if self.sword_texture is None:
			self.sword_texture = pg.transform.scale(
				pg.image.load('texture/sword.png').convert_alpha(),
				[
					Sets.square_size * 2,
					Sets.square_size * 8,
				]
			)
		
	def post_render(self, sc: pg.Surface):
		if isinstance(self.font, str):
			self.font = pg.font.Font(f'fonts/{self.font}.ttf', size=clamp(Sets.square_size, 40, 50))
		src = self.font.render(f"Score: {self.score}", True, (155, 255, 255))
		sc.blit(src, [0, 0])
	
	def logic(self, colliding: list[Drop]):
		if None in self.pos.xy:
			self.pos = Vec2(Sets.Sc.center)
		rect = pg.Rect(
			self.x + self.speed_x - Sets.square_size // 1.5,
			self.y + self.speed_y - Sets.square_size // 1.5,
			Sets.square_size // 1.5 * 2,
			Sets.square_size // 1.5 * 2,
		)
		for coll in colliding:
			if rect.colliderect(coll):
				return
		self.pos += self.speed_dim
		
		money: Drop
		for money in self.land.drop_list:
			if dist(money.center, self.pos.xy) < Sets.square_size * 2:
				self.score += money.value
				money.death()


def main():
	input("Этот файл не предназначен для запуска")


if __name__ == '__main__':
	main()
