from math import sqrt, dist, sin, cos, degrees, atan2, pi
import pygame_gui
from matan import Vec2, clamp, collisionCircleLine
from sets import Sets
import pygame as pg
from enemy import Drop, Enemy


class Player:
	def __init__(self, x=None, y=None, color=None, speed_def=None, facing=None, land=None, enemy_list=None, hp_max=100) -> None:
		"""
		:type hp_max: int | float
		:type x: int | float
		:type y: int | float
		:type color: list[int, int, int] | tuple[int, int, int]
		:type speed_def: int | float
		:type facing: str
		:param facing: up, up-right, right, down-right, down, down-left, left, up-left
		"""
		
		self.manager = None
		self.max_hp = int(hp_max)
		self.hp_bar = None
		class RP:
			hp_bar_relative = pg.Rect((0, 0), (7 * Sets.square_size, 1.5 * Sets.square_size))
			draw_path = False
			hp_bar_offset = Vec2((-hp_bar_relative.width * 0.5, -Sets.square_size * 2.5))
		self.RenderProperties = RP
		self.hp = self.max_hp
		self.score = 0
		self.land = land
		self.font = 'arial'
		self.fire_gun_texture = None
		if enemy_list is None:
			raise ValueError("Player initialised without enemy list")
		if color is None:
			color = 255, 255, 255
		if speed_def is None:
			speed_def = 9
		if facing is None:
			facing = 'up'
		if land is None:
			raise ValueError("Player initialised without world map")
		p = x, y
		self.enemy_list = enemy_list
		self.land = land
		self.color = color
		self.pos = Vec2(p)
		self.speed_def = speed_def
		self.speed = speed_def
		self.facing = facing
		self.sq2 = sqrt(2) / 2
		self.fire_gun_rangle = .0
		self.show_firegun = True
	
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
		self.hp_bar.set_position(Vec2(self.RenderProperties.hp_bar_offset + self.pos.xy) - offset)
		if self.manager:
			self.manager.draw_ui(sc)
		pg.draw.circle(
			surface=sc,
			color=self.color,
			center=self.pos - offset,
			radius=Sets.square_size // 1.5,
			width=5,
		)
		if self.fire_gun_texture is None:
			self.fire_gun_texture = pg.transform.scale(
				pg.image.load('texture/firegun.png').convert_alpha(),
				[
					Sets.square_size * 2,
					Sets.square_size * 8,
				]
			)
		
		if self.show_firegun:
			# firegun render
			sprite_rotated = pg.transform.rotate(self.fire_gun_texture, degrees(self.fire_gun_rangle) + 180)
			c_pos = list(self.pos - offset)
			c_pos[0] += Sets.square_size * 4 * sin(self.fire_gun_rangle)
			c_pos[1] += Sets.square_size * 4 * cos(self.fire_gun_rangle)
			rect = sprite_rotated.get_rect(center=c_pos)
			sc.blit(
				sprite_rotated,
				rect,
			)
		
	def post_render(self, sc: pg.Surface):
		if isinstance(self.font, str):
			self.font = pg.font.Font(f'fonts/{self.font}.ttf', size=clamp(Sets.square_size, 40, 50))
		src = self.font.render(f"Score: {self.score}", True, (155, 255, 255))
		sc.blit(src, [0, 0])
	
	def logic(self, colliding: list[Drop], offset: tuple, sc: pg.Surface):
		if None in self.pos.xy:
			self.pos = Vec2(Sets.Sc.center)
		if self.manager is not None:
			self.hp_bar.set_current_progress(self.hp / self.max_hp * 100)
			self.manager.update(1 / Sets.FPS)
		if pg.mouse.get_pressed()[0]:
			self.show_firegun = True
			mpos = Vec2(pg.mouse.get_pos()) + offset
			self.fire_gun_rangle = atan2(*(self.pos - mpos)) + pi
			to = (Sets.square_size * 8 * sin(self.fire_gun_rangle) + self.x, Sets.square_size * 8 * cos(self.fire_gun_rangle) + self.y)
			line = {
				'p1': {
					'x': self.x,
					'y': self.y,
				},
				'p2': {
					'x': to[0],
					'y': to[1],
				}
			}
			enemy: Enemy
			for enemy in self.enemy_list:
				if collisionCircleLine(
					circle={
						'x': enemy.x,
						'y': enemy.y,
						'radius': int(Sets.square_size // 1.2),
					},
					line=line
				):
					enemy.hp -= 1
				# pg.draw.line(
				# 	sc,
				# 	(255, 255, 255),
				# 	(self.x - offset[0], self.y - offset[1]),
				# 	(line['p2']['x'] - offset[0], line['p2']['y'] - offset[1]),
				# 	10,
				# )
			
		else:
			self.show_firegun = False
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
