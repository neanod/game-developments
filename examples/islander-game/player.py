from math import sqrt, dist, sin, cos, degrees, atan2, pi, floor
import pygame_gui
from types import FunctionType
from sussy_things import Vec2, clamp, collisionCircleLine
from sets import Sets
import pygame as pg
from enemy import Drop, Enemy


empty_f = lambda: None


class ColorTheme:
	def __init__(self, foreground_color, background_color, frame_color, text_color):
		"""
		:type foreground_color: tuple[int, int, int]
		:type background_color: tuple[int, int, int]
		:type frame_color: tuple[int, int, int]
		"""
		self.fg = pg.Color(foreground_color)
		self.bg = pg.Color(background_color)
		self.fc = pg.Color(frame_color)
		self.tc = pg.Color(text_color)


class Button:
	def __init__(
			self,
			relative_rect: pg.Rect,
			theme: ColorTheme,
			text: str,
			function: FunctionType,
			font: pg.Font,
			pos: tuple[int, int]
	):
		pg.init()
		self.relative_rect: pg.Rect = relative_rect
		self.theme: ColorTheme = theme
		self.text: str = text
		self.func: FunctionType = function
		self.font: pg.Font = font
		self.manager = pygame_gui.UIManager(Sets.Sc.res)
		self.button = pygame_gui.elements.UIButton(
			relative_rect=self.relative_rect,
			text=self.text,
			manager=self.manager,
		)
		self.pos = pos
	
	def render(self, sc: pg.Surface, offset: tuple[int, int], delta_time: float):
		self.button.set_position(Vec2(offset) + self.pos)
		self.manager.update(delta_time)
		self.manager.draw_ui(sc)


class Cell(Button):
	def __init__(self, relative_rect: pg.Rect, theme: ColorTheme, function: FunctionType, font: pg.Font, pos: tuple[int, int]):
		from random import choice
		super().__init__(relative_rect, theme, choice('adfsgfhdghdsafdsgfrhtrd'), function, font, pos)
		

class ButtonMenu:
	def __init__(
			self,
			button_list=None,
	):
		if button_list is None:
			button_list = list()
		self.b_list = button_list
	
	def render(self, sc, offset):
		button: Button
		for button in self.b_list:
			button.render(sc, offset, 1 / Sets.FPS)


class CellMenu(ButtonMenu):
	def __init__(self, left_top_pos: Vec2, distance_between_cells: int, cell_size: int, inventory_size: tuple[int, int], theme: ColorTheme):
		super().__init__()
		self.theme: ColorTheme = theme
		for x in range(left_top_pos.x + distance_between_cells, left_top_pos.x + (cell_size + distance_between_cells) * inventory_size[0] + distance_between_cells - 1, (cell_size + distance_between_cells)):
			for y in range(left_top_pos.y + distance_between_cells, left_top_pos.y + (cell_size + distance_between_cells) * inventory_size[1] + distance_between_cells - 1, (cell_size + distance_between_cells)):
				self.b_list.append(
					Cell(
						relative_rect=pg.Rect(
							0,
							0,
							cell_size,
							cell_size,
						),
						theme=self.theme,
						function=empty_f,
						font=None,
						pos=(x, y),
					)
				)
		self.border_radius = int(Sets.square_size // 1.5)
		self.relative_rect = pg.Rect(
			0,
			0,
			(cell_size + distance_between_cells) * inventory_size[0] + self.border_radius,
			(cell_size + distance_between_cells) * inventory_size[1] + self.border_radius,
		)
		self.rect_width = 5
		
	def render(self, sc, offset):
		pg.draw.rect(
			surface=sc,
			color=self.theme.bg,
			rect=self.relative_rect.move(*offset),
			border_radius=self.border_radius,
		)
		pg.draw.rect(
			surface=sc,
			color=self.theme.tc,
			rect=self.relative_rect.move(offset),
			border_radius=self.border_radius,
			width=self.rect_width,
		)
		super().render(sc, Vec2(offset) - 11)
		
		
class Inventory:
	def __init__(
			self,
			*,
			inventory_size: tuple[int, int],
			cell_size: int,
			font: pg.Font,
			left_top_pos: Vec2 = Vec2((Sets.square_size, Sets.square_size)),
			distance_between_cells: int = 3,
			theme: ColorTheme = ColorTheme(
				(200, 200, 200),
				(155, 155, 155),
				(000, 000, 000),
				(000, 000, 000),
			)
	):
		self.theme = theme
		self.font = font
		self.menu = CellMenu(
			left_top_pos=left_top_pos,
			inventory_size=inventory_size,
			cell_size=cell_size,
			distance_between_cells=distance_between_cells,
			theme=self.theme,
		)
		

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

		if enemy_list is None:
			raise ValueError("Player initialised without enemy list")
		if color is None:
			color = 255, 255, 255
		if speed_def is None:
			speed_def = 8
		if facing is None:
			facing = 'up'
		if land is None:
			raise ValueError("Player initialised without world map")

		class RP:
			hp_bar_relative = pg.Rect((0, 0), (7 * Sets.square_size, 1.5 * Sets.square_size))
			draw_path = False
			hp_bar_offset = Vec2((-hp_bar_relative.width * 0.5, -Sets.square_size * 2.5))
		self.RenderProperties = RP

		self.max_hp: int = floor(hp_max)
		self.manager: pygame_gui.UIManager = None
		self.hp_bar: pygame_gui.elements.UIProgressBar = None
		self.hp: int = self.max_hp
		self.score: int = 0
		self.land = land
		self.font: pg.Font | str = 'arial'
		self.fire_gun_texture: pg.Surface = None
		self.enemy_list: list[Enemy] = enemy_list
		self.color: pg.Color = color
		self.pos: Vec2 = Vec2((x, y))
		self.speed_def: int | float = speed_def
		self.speed: int | float = speed_def
		self.facing: str = facing
		self.sq2: float = sqrt(2) / 2
		self.fire_gun_rangle: float = .0
		self.show_firegun: bool = True
		self.inventory_open: bool = False
		self.inventory: Inventory = Inventory(
			inventory_size=(15, 15),
			cell_size=30,
			font=None,
			distance_between_cells=-5,
		)
	
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
	
	def go_to_nearest_block(self):
		if None in self.pos.xy:
			raise ValueError("position is not initialised")
		res = ((0, 0), 10000)
		for block in self.land.land_map.keys():
			distance = dist(self.bpos, block)
			if self.land.land_map[block] > Sets.water_level and res[1] > distance:
				res = block, distance
		if res[0][0] is None:
			raise ValueError("player trying to go to island, but no blocks in world")
		self.pos.x, self.pos.y = (
			(res[0][0] + 0.5) * Sets.square_size,
			(res[0][1] + 0.5) * Sets.square_size,
		)
	
	@property
	def x(self) -> int | float:
		return self.pos.x
	
	@property
	def bx(self):
		return self.pos.x // Sets.square_size
	
	@property
	def y(self) -> int | float:
		return self.pos.y
	
	@property
	def by(self):
		return self.pos.y // Sets.square_size
	
	@property
	def bpos(self):
		return self.bx, self.by
	
	def render(self, sc: pg.Surface, offset):
		self.hp_bar.set_position(Vec2(self.RenderProperties.hp_bar_offset + self.pos.xy) - offset)
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
	
	def render_gui(self, sc: pg.Surface):
		if self.manager:
			if self.inventory_open:
				self.inventory.menu.render(sc, offset=(100, 100))
				self.manager.draw_ui(sc)
		if isinstance(self.font, str):
			self.font = pg.font.Font(f'fonts/{self.font}.ttf', size=clamp(Sets.square_size, 40, 50))
			self.inventory.font = self.font
		src_player_score = self.font.render(f"Score: {self.score}", True, (155, 255, 255))
		sc.blit(src_player_score, [0, 0])
	
	def logic(self, colliding: list[Drop], offset: tuple, scope: float):
		if None in self.pos.xy:
			self.pos = Vec2(Sets.Sc.center)
		
		if self.manager is not None:
			self.hp_bar.set_current_progress(self.hp / self.max_hp * 100)
			self.manager.update(1 / Sets.FPS)
		
		if pg.mouse.get_pressed()[0]:
			self.show_firegun = True
			mpos = pg.mouse.get_pos()
			mpos = (
				(mpos[0] - Sets.Sc.h_width) / scope + Sets.Sc.h_width + offset[0],
				(mpos[1] - Sets.Sc.h_height) / scope + Sets.Sc.h_height + offset[1],
			)
			self.fire_gun_rangle = atan2(*(self.pos - mpos)) + pi
			to = (Sets.square_size * 8 * sin(self.fire_gun_rangle) + self.x,
			      Sets.square_size * 8 * cos(self.fire_gun_rangle) + self.y)
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
				if dist(self.pos.xy, (enemy.x, enemy.y)) < Sets.square_size * 8 and collisionCircleLine(
						circle={
							'x': enemy.x,
							'y': enemy.y,
							'radius': int(Sets.square_size // 1.2),
						},
						line=line,
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
		
		money: Drop
		for money in self.land.drop_list:
			if dist(money.center, self.pos.xy) < Sets.square_size * 2:
				self.score += money.value
				money.death()
		
		for coll in colliding:
			if rect.colliderect(coll):
				return
		self.pos += self.speed_dim


def main():
	input("Этот файл не предназначен для запуска")


if __name__ == '__main__':
	main()
