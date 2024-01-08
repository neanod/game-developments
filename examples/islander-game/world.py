import random
from math import dist, hypot
from typing import Callable
from sussy_things import get_color, exit_game, Vec2, bresenham_with_width
import pygame as pg
from sets import Sets, ButtonsInfo
import heapq
from numpy import sin, cos
from enemy import Enemy, Drop


class Camera:
	scope: float = 1
	pos = list(Sets.Sc.center.copy())
	offset = (0, 0)


def clamp(_x: int | float, _min: int | float, _max: int | float) -> int | float:
	"""
	clamps the number
	:param _x: num to clamp
	:param _min: minimum
	:param _max: maximum
	:return: clamped number
	"""
	return min(_max, max(_min, _x))


def heuristic_cost_estimate(pos, goal, *, random_k=0) -> float:
	return dist(pos, goal)


def camera_logic(camera_pos, player_pos, t, sc) -> list[int, int]:
	"""
	Returns clamped camera pos.
	Do world-gen logic
	:param sc: screen
	:type t: int
	:type camera_pos: list[int, int]
	:type player_pos: tuple[int, int]
	:return None
	"""
	if None in player_pos:
		return Sets.Sc.center
	delta = Vec2(player_pos) - camera_pos
	camera_pos = Vec2(camera_pos) + Vec2(delta) * Sets.camera_movement_k
	if t % 6:
		return camera_pos
	# world_generation
	camera_offset = camera_pos[0] - Sets.Sc.h_width, camera_pos[1] - Sets.Sc.h_height
	gen_size_x, gen_size_z = Sets.Sc.width // Sets.square_size + Sets.gen_dist * 2, Sets.Sc.height // Sets.square_size + Sets.gen_dist * 2
	left = int(camera_offset[0] // Sets.square_size - Sets.gen_dist + 1)
	top = int(camera_offset[1] // Sets.square_size - Sets.gen_dist + 1)
	world_keys = WorldMap.land_map.keys()
	
	for x_temp in range(left - 1, left + gen_size_x):
		for z_temp in range(top - 1, top + gen_size_z):
			if (x_temp, z_temp) not in world_keys:
				# if (x_temp, z_temp) not in WorldMap.to_gen:
				# 	WorldMap.to_gen.append((x_temp, z_temp))
				world_post_gen(x_temp, z_temp, sc)
	return camera_pos


def find_path_a_star(start_pos, end_pos, world_map):
	"""
	:type end_pos: list | tuple
	:type start_pos: list | tuple
	:type world_map: dict[tuple[int, int], bool]
	"""
	start_pos = tuple(start_pos)
	end_pos = tuple(end_pos)
	
	open_set = [(0, start_pos)]
	came_from = {start_pos: None}
	g_score = {start_pos: 0}
	
	while open_set:
		current_g, current_pos = heapq.heappop(open_set)
		
		if current_pos == end_pos:
			path = reconstruct_path(came_from, end_pos)
			return path
		
		for delta_pos in [
			(1, 0), (0, 1), (-1, 0), (0, -1),
			(1, 1), (1, -1), (-1, 1), (-1, -1),
		]:
			neighbor = (current_pos[0] + delta_pos[0], current_pos[1] + delta_pos[1])
			
			if neighbor in world_map.keys():
				if world_map[neighbor] > Sets.water_level:
					tentative_g = g_score[current_pos] + abs(Vec2(delta_pos))
					
					if neighbor not in g_score or tentative_g < g_score[neighbor]:
						g_score[neighbor] = tentative_g
						f_score = tentative_g + heuristic_cost_estimate(neighbor, end_pos)
						heapq.heappush(open_set, (f_score, neighbor))
						came_from[neighbor] = current_pos


def reconstruct_path(came_from, current_pos):
	path = [current_pos]
	while current_pos in came_from and came_from[current_pos] is not None:
		current_pos = came_from[current_pos]
		path.insert(0, current_pos)
	return path


def build_bridge(pos1: tuple, pos2: tuple, score_available: int):
	way: set[tuple[int, int]] = bresenham_with_width(Sets.bridge_width, *pos1, *pos2)
	wasted = 0
	# print(pg.Rect(1740, 2205, 15, 15) in WorldMap.land_colliding)
	for x, y in way:
		rect = pg.Rect(
			x * Sets.square_size,
			y * Sets.square_size,
			Sets.square_size,
			Sets.square_size
		)
		if rect in WorldMap.land_colliding:
			delta = setblock_bridge(x, y)
			score_available -= delta
			wasted += delta
			if not (Sets.Cheats.infinity_money or score_available):
				return wasted
			WorldMap.land_map[x, y] = 10
			WorldMap.land_colliding.remove(rect)
	return wasted


def setblock_bridge(x: int, y: int) -> bool:
	for i in range(len(WorldMap.chunks)):
		ch = WorldMap.chunks[i]
		if ch.cpos == (x // WorldMap.chunk_size, y // WorldMap.chunk_size):
			ch.add_block(x, y, height=10, round_borders=False)
			return True
	else:
		raise ValueError("cant find chunk")
	return False


def clamp_color_channel(_x) -> int:
	return max(0, min(255, _x))


def pre_world_gen(sc) -> None:
	"""
	World gen in big rectangle previous starting game
	:return: nothing
	"""
	bound = 90
	without_enemy_bound = -10
	for x in range(-bound, Sets.Sc.width // Sets.square_size + bound):
		for z in range(-bound, Sets.Sc.height // Sets.square_size + bound):
			world_post_gen(
				x,
				z,
				sc,
				spawn_enemy=all(
					(
						x not in range(-without_enemy_bound, Sets.Sc.width // Sets.square_size + without_enemy_bound),
						z not in range(-without_enemy_bound, Sets.Sc.height // Sets.square_size + without_enemy_bound)
					)
				)
			)


def world_post_gen(x_pos, z_pos, sc, *, spawn_enemy=True, spawn_block=True) -> None:
	"""
	:param sc: screen
	:type spawn_block: bool
	:type sc: pg.Surface
	:type spawn_enemy: bool
	:type z_pos: int
	:type x_pos: int
	"""
	h: float = get_block_at(x_pos, z_pos)
	if spawn_block:
		WorldMap.land_map[(x_pos, z_pos)] = h
		if h < Sets.water_level:
			WorldMap.land_colliding.append(
				pg.Rect(
					x_pos * Sets.square_size,
					z_pos * Sets.square_size,
					Sets.square_size,
					Sets.square_size
				)
			)
		# update image of chunk, where block is placed
		cposx: int = x_pos // WorldMap.chunk_size
		cposz: int = z_pos // WorldMap.chunk_size
		for c in WorldMap.chunks:
			if c.cx == cposx and c.cz == cposz:
				c.add_block(x_pos, z_pos, h)
				break
		else:
			WorldMap.chunks.append(
				WorldChunk(
					cposx,
					cposz,
					get_color,
				)
			)
			
			WorldMap.chunks[-1].add_block(x_pos, z_pos, h)
	if spawn_enemy and not random.randint(0, int(1 / Sets.enemy_spawn_chance) - 1) and h > Sets.water_level:
		EnemyList.enemies.append(
			Enemy(
				sc=sc,
				x=x_pos * Sets.square_size,
				y=z_pos * Sets.square_size,
				world_map=WorldMap.land_map,
				path_find_f=find_path_a_star,
				speed_def=5,
				all_enemies=EnemyList.enemies,
				list_to_drop=WorldMap.drop_list,
			)
		)


class WorldChunk:
	def __init__(self, cx: int, cz: int, color_function: Callable):
		"""
		:param cx: X position in chunk system
		:type cx: int
		:param cz: Y position in chunk system
		:type cz: int
		:param color_function: function, returns the color of block
		:type color_function: function
		"""
		self.ax = cx * Sets.square_size * WorldMap.chunk_size
		self.az = cz * Sets.square_size * WorldMap.chunk_size
		self.rect = pg.Rect(
			self.ax,
			self.az,
			*WorldMap.size,
		)
		
		self.cx = cx
		self.cz = cz
		self.sc = pg.Surface(
			size=(
				WorldMap.chunk_size * Sets.square_size,
				WorldMap.chunk_size * Sets.square_size,
			),
		)
		self.get_color = color_function
	
	def add_block(self, _x: int, _y: int, height: float, force=None, round_borders=True) -> None:
		"""
		:type round_borders: bool
		:param _x: x_pos in blocky system
		:param _y: y_pos in blocky system
		:param height: height of block in the world
		:type height: float
		:param force: force set the height of block
		"""
		
		color = self.get_color(height) if force is None else force
		rad: int = Sets.square_size
		
		if height <= Sets.water_level:
			self.sc.fill(
				color=color,
				rect=[
					_x * Sets.square_size - self.ax,
					_y * Sets.square_size - self.az,
					Sets.square_size,
					Sets.square_size,
				]
			)
			return
		
		if round_borders:
			self.sc.fill(
				color=(0, 0, 255),
				rect=[
					_x * Sets.square_size - self.ax,
					_y * Sets.square_size - self.az,
					Sets.square_size,
					Sets.square_size,
				]
			)
			# ground
			# соседство тьюринга. потому что не фон неймана
			neighbour: list[bool, bool, bool, bool] = list()
			for delta in [
				(0, -1),
				(1, 0),
				(0, 1),
				(-1, 0),
			]:
				if (delta[0] + _x, delta[1] + _y) in WorldMap.land_map.keys():
					neighbour.append(WorldMap.land_map[delta[0] + _x, delta[1] + _y] > Sets.water_level)
				else:
					neighbour.append(get_block_at(delta[0] + _x, delta[1] + _y) > Sets.water_level)
			
			match neighbour:
				case [0, 0, 0, 0]:
					args = rad,
				case [1, 0, 0, 0]:
					args = 0, 0, 0, rad, rad
				case [0, 1, 0, 0]:
					args = 0, rad, 0, rad, 0
				case [0, 0, 1, 0]:
					args = 0, rad, rad, 0, 0
				case [0, 0, 0, 1]:
					args = 0, 0, rad, 0, rad
				case [1, 1, 0, 0]:
					args = 0, 0, 0, rad, 0
				case [0, 1, 1, 0]:
					args = 0, rad, 0, 0, 0
				case [0, 0, 1, 1]:
					args = 0, 0, rad, 0, 0
				case [1, 0, 0, 1]:
					args = 0, 0, 0, 0, rad
				case _:  # [1, 1, 1, 1] | [0, 1, 1, 1] | [1, 0, 1, 1] | [1, 1, 0, 1] | [1, 1, 1, 0] | [1, 0, 1, 0] | [0, 1, 0, 1]:
					args = ()
			
			pg.draw.rect(
				self.sc,
				color,
				[
					_x * Sets.square_size - self.ax,
					_y * Sets.square_size - self.az,
					Sets.square_size,
					Sets.square_size,
				],
				0,
				*args,
			)
		else:
			self.sc.fill(
				color=color,
				rect=[
					_x * Sets.square_size - self.ax,
					_y * Sets.square_size - self.az,
					Sets.square_size,
					Sets.square_size,
				]
			)
	
	@property
	def cpos(self) -> tuple[int, int]:
		return self.cx, self.cz
	
	@property
	def bpos(self) -> tuple[int, int]:
		return self.cx // Sets.square_size, self.cz // Sets.square_size
	
	def get_a_pos(self) -> tuple[int, int]:
		return self.ax, self.az
	
	def get_rect(self) -> pg.Rect:
		return pg.Rect(
			[
				self.ax,
				self.az,
				WorldMap.chunk_size * Sets.square_size,
				WorldMap.chunk_size * Sets.square_size,
			]
		)
	
	def render_to_source(self, source: pg.Surface, _offset: tuple[int, int]):
		source.blit(
			source=self.sc,
			dest=(
				self.ax - _offset[0],
				self.az - _offset[1],
			)
		)


def get_pressed():
	for event in pg.event.get():
		match event.type:
			case pg.QUIT:
				exit_game()
			case pg.MOUSEBUTTONDOWN:
				match event.button:
					case 1:
						ButtonsInfo.LMB = True
					case 3:
						ButtonsInfo.RMB = True
			case pg.KEYDOWN:
				match event.key:
					case pg.K_w:
						ButtonsInfo.W = True
					case pg.K_a:
						ButtonsInfo.A = True
					case pg.K_s:
						ButtonsInfo.S = True
					case pg.K_d:
						ButtonsInfo.D = True
					
					case pg.K_r:
						ButtonsInfo.R = True
			case pg.MOUSEBUTTONUP:
				match event.button:
					case 1:
						ButtonsInfo.LMB = False
					case 3:
						ButtonsInfo.RMB = False
			case pg.KEYUP:
				match event.key:
					case pg.K_w:
						ButtonsInfo.W = False
					case pg.K_a:
						ButtonsInfo.A = False
					case pg.K_s:
						ButtonsInfo.S = False
					case pg.K_d:
						ButtonsInfo.D = False
					
					case pg.K_r:
						ButtonsInfo.R = False
			case pg.MOUSEWHEEL:
				ButtonsInfo.mwheel += event.precise_y


def get_block_at(x: int, z: int) -> float:
	"""
	Get height of the block by pos. WARN: Pos + screen_center
	:param x: x pos in B sys
	:param z: y pos in B sys
	:return: height
	"""
	x -= Sets.Sc.h_width // Sets.square_size
	z -= Sets.Sc.h_height // Sets.square_size
	
	return Sets.noise([x / Sets.period, z / Sets.period]) + 0.5 * Sets.amp
	# return hypot(x, 1000 / (z + 0.0001)) * 0.02
	# return sin((x + 8) / 15) * cos(z / 10) * 0.2 + 0.04 + Sets.water_level
	# return (x % 10 + z % 10 > 5 and abs(x) + abs(z) > 40) * Sets.water_level + 0.1


class WorldMap:
	chunk_size = 512
	chunks: list[WorldChunk] = list()
	size = int(Sets.Sc.width / Sets.square_size), int(Sets.Sc.height / Sets.square_size)
	to_gen: list = list()
	land_map: dict = dict()
	drop_list: list[Drop] = list()
	land_colliding: list[pg.Rect] = list()
	

class EnemyList:
	enemies: list[Enemy] = list()


if __name__ == '__main__':
	input("Это не основной файл. Откройте IslandCapture.py")
