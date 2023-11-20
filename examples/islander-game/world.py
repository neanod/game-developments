from math import dist
from matan import get_color
import pygame
from sets import Sets
import heapq


class Camera:
	pos = list(Sets.Sc.center.copy())


def clamp(_x, _min, _max):
	return min(_max, max(_min, _x))


def heuristic_cost_estimate(pos, goal):
	x1, y1 = pos
	x2, y2 = goal
	n = 2
	return (abs(x1 - x2) ** n + abs(y1 - y2) ** n) ** (1 / n)


def camera_logic(camera_pos, player_pos, t) -> list[int, int]:
	"""
	Returns clamped camera pos.
	Do world-gen logic
	:type t: int
	:type camera_pos: list[int, int]
	:type player_pos: list[int, int]
	:return None
	"""
	
	camera_pos = [
		clamp(
			camera_pos[0],
			player_pos[0] - Sets.Sc.cam_to_player_box_size[0] // 2,
			player_pos[0] + Sets.Sc.cam_to_player_box_size[0] // 2,
		),
		clamp(
			camera_pos[1],
			player_pos[1] - Sets.Sc.cam_to_player_box_size[1] // 2,
			player_pos[1] + Sets.Sc.cam_to_player_box_size[1] // 2,
		)
	]
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
				world_post_gen(x_temp, z_temp)
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
			# (1, 1), (1, -1), (-1, 1), (-1, -1),
			
			# (-1, 2), (0, 2), (1, 2), (2, 2),
			# (-2, -2), (0, -2), (1, -2), (1, -2),
			# (2, 1), (2, 0), (2, -1), (2, -2),
			# (-2, 2), (-2, 1), (-2, 0), (-2, -1),
		]:
			neighbor = (current_pos[0] + delta_pos[0], current_pos[1] + delta_pos[1])
			
			if neighbor in world_map.keys():
				if world_map[neighbor] > Sets.water_level:
					tentative_g = g_score[current_pos] + 1
					
					if neighbor not in g_score or tentative_g < g_score[neighbor]:
						g_score[neighbor] = tentative_g
						f_score = tentative_g + heuristic_cost_estimate(neighbor, end_pos)
						heapq.heappush(open_set, (f_score, neighbor))
						came_from[neighbor] = current_pos
	
	return None


def reconstruct_path(came_from, current_pos):
	path = [current_pos]
	while current_pos in came_from and came_from[current_pos] is not None:
		current_pos = came_from[current_pos]
		path.insert(0, current_pos)
	return path


def clamp_color_channel(_x) -> int:
	return max(0, min(255, _x))


def world_post_gen(x_pos, z_pos) -> None:
	"""
	:type z_pos: int
	:type x_pos: int
	"""
	h = (Sets.noise([x_pos / Sets.period, z_pos / Sets.period]) + 0.5 * Sets.amp)
	WorldMap.land_map[(x_pos, z_pos)] = h
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
				pygame.Surface(
					(
						WorldMap.chunk_size * Sets.square_size,
						WorldMap.chunk_size * Sets.square_size,
					)
				),
				get_color,
			)
		)
		
		WorldMap.chunks[-1].add_block(x_pos, z_pos, h)
		

class WorldChunk:
	def __init__(self, cx, cz, surface, color_function):
		"""
		
		:param cx: X position in chunk system
		:type cx: int
		:param cz: Y position in chunk system
		:type cz: int
		:param surface: Surfaces to render
		:type surface: pygame.Surface
		:param color_function: function, returns the color of block
		:type color_function: function
		"""
		self.ax = cx * Sets.square_size * WorldMap.chunk_size
		self.az = cz * Sets.square_size * WorldMap.chunk_size
		self.rect = pygame.Rect(
			self.ax,
			self.az,
			*WorldMap.size,
		)
		self.cx = cx
		self.cz = cz
		self.sc = surface
		self.get_color = color_function
		
	def add_block(self, _x, _y, height, force=None) -> None:
		"""
		:param _x: x_pos in blocky system
		:param _y: y_pos in blocky system
		:param height: height of block in the world
		:type height: float
		:param force: force set the height of block
		:return: None
		"""
		
		# in_chunk: bool = (_x // WorldMap.chunk_size == self.cx) and (_y // WorldMap.chunk_size == self.cz)
		# if not in_chunk:
		# 	print(f"Block B({_x, _y}) not in chunk C({self.cx, self.cz})")
		# 	raise ValueError
		# 	return
		
		color = self.get_color(height) if force is None else force
		
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
	
	def get_rect(self) -> pygame.Rect:
		return pygame.Rect(
			[
				self.ax,
				self.az,
				WorldMap.chunk_size * Sets.square_size,
				WorldMap.chunk_size * Sets.square_size,
			]
		)
	
	def render_to_source(self, source: pygame.Surface, _offset: tuple[int, int]):
		source.blit(
			source=self.sc,
			dest=(
				self.ax - _offset[0],
				self.az - _offset[1],
			)
		)


class WorldMap:
	chunk_size = 128
	chunks: list[WorldChunk] = list()
	size = int(Sets.Sc.width / Sets.square_size), int(Sets.Sc.height / Sets.square_size)
	to_gen: set = set()
	land_map: dict = dict()


offset = 30, 30
size = WorldMap.size
center = (Sets.Sc.h_width // Sets.square_size, Sets.Sc.h_height // Sets.square_size)
if Sets.spawn_zone:
	for x in range(-offset[0], size[0] + offset[0]):
		for z in range(-offset[1], size[1] + 1 + offset[1]):
			if dist((x, z), center) < Sets.spawn_zone:
				minim = Sets.water_level
				lvl = (1 - dist((x, z), center) / Sets.spawn_zone) / 3 * (Sets.amp - minim) + minim
				WorldMap.land_map[x, z] = lvl
				for ch in WorldMap.chunks:
					if ch.bpos == (x, z):
						ch.add_block(x, z, height=None, force=lvl)
						break
				else:
					s = WorldMap.chunk_size * Sets.square_size
					WorldMap.chunks.append(WorldChunk(
						x % WorldMap.chunk_size,
						z % WorldMap.chunk_size,
						pygame.Surface((s, s)),
						get_color,
					))
			else:
				world_post_gen(x, z)


if __name__ == '__main__':
	input("Это не основной файл. Откройте IslandCapture.py")
