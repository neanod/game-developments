import math
from sets import Sets
from numpy import floor
import heapq
from matan import clamp


class Camera:
	pos = Sets.Sc.center.copy()


def find_path(start_pos, end_pos, world_map):
	old_points = list()
	
	if isinstance(start_pos, list) and isinstance(end_pos, list):
		all_paths: list[list[list[int, int]]] = [[start_pos]]
		
		way_matrix = [
			[1, 0],
			[0, 1],
			[-1, 0],
			[0, -1],
			
			[1, 1],
			[1, -1],
			[-1, 1],
			[-1, -1],
			
			# [2, -2],
			# [2, -1],
			# [2, 0],
			# [2, 1],
			# [2, 2],
			# [-2, -2],
			# [-2, -1],
			# [-2, 0],
			# [-2, 1],
			# [-2, 2],
			# [1, 2],
			# [0, 2],
			# [-1, 2],
			# [1, -2],
			# [0, -2],
			# [-1, -2],
		]
		"""
		# ход конем
		way_matrix = [
			[0, 0],

			[1, 2],
			[-1, 2],
			[1, -2],
			[-1, -2],
			[2, 1],
			[2, -1],
			[-2, 1],
			[-2, -1],
		]
		"""
		"""
		way_matrix = [
			[0, 1],
			[1, 0],
			[0, -1],
			[-1, 0],
		]
		"""
		while True:
			new_paths: list[list[list[int, int]]] = list()
			
			path: list[list[int, int]]
			
			for path in all_paths:
				current_pos = path[-1]
				for delta_pos in way_matrix:
					current_possible_pos = [current_pos[0] + delta_pos[0], current_pos[1] + delta_pos[1]]
					try:
						if not world_map[current_possible_pos[0]][current_possible_pos[1]]:
							continue
					except IndexError:
						continue
					if current_possible_pos in old_points:
						continue
					
					old_points.append(current_possible_pos)
					
					new_path = path.copy()
					new_path.append(current_possible_pos)
					
					new_paths.append(new_path)
					if current_possible_pos == end_pos:
						return path + [current_possible_pos]
			all_paths = new_paths
			if not new_paths:
				return None


def heuristic_cost_estimate(pos, goal):
	x1, y1 = pos
	x2, y2 = goal
	n = 2
	return (abs(x1 - x2) ** n + abs(y1 - y2) ** n) ** (1 / n)


def camera_logic(camera_pos, player_pos, t):
	"""
	:type t: int
	:type camera_pos: list[int, int]
	:type player_pos: list[int, int]
	:return None
	"""
	
	camera_pos_clamped: list = [
		clamp(
			camera_pos[0],
			player_pos[0] - Sets.Sc.cam_to_player_box_size[0] // 2,
			player_pos[0] + Sets.Sc.cam_to_player_box_size[0] // 2,
		),
		clamp(
			camera_pos[0],
			player_pos[1] - Sets.Sc.cam_to_player_box_size[1] // 2,
			player_pos[1] + Sets.Sc.cam_to_player_box_size[1] // 2,
		)
	]
	
	# world_generation
	camera_offset = camera_pos_clamped[0] - Sets.Sc.h_width, camera_pos_clamped[1] - Sets.Sc.h_height
	
	if t % (Sets.FPS // 4):
		return
	
	gen_size_x, gen_size_y = Sets.Sc.width // Sets.square_size + Sets.gen_dist * 2, Sets.Sc.height // Sets.square_size + Sets.gen_dist * 2
	left = -camera_offset[0] // Sets.square_size - Sets.gen_dist
	top = -camera_offset[1] // Sets.square_size - Sets.gen_dist
	world_keys = WorldMap.land_map.keys()
	
	for x in range(left - 1, left + gen_size_x + 1):
		for z in range(top - 1, top + gen_size_y + 1):
			if (x, z) in world_keys:
				continue
			world_post_gen(x, z)
	return


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
			
			# (-1, 2), (0, 2), (1, 2), (2, 2),
			# (-2, -2), (0, -2), (1, -2), (1, -2),
			# (2, 1), (2, 0), (2, -1), (2, -2),
			# (-2, 2), (-2, 1), (-2, 0), (-2, -1),
		]:
			neighbor = (current_pos[0] + delta_pos[0], current_pos[1] + delta_pos[1])
			
			if neighbor in world_map:
				if world_map[neighbor]:
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


def world_post_gen(x, z) -> None:
	"""
	:type z: int
	:type x: int
	"""
	
	WorldMap.land_map[(x, z)] = not not int(floor((Sets.noise([x / Sets.period, z / Sets.period]) + 0.5) * Sets.amp))


def world_gen(size_x, size_z) -> dict:
	"""
	:type size_x: int
	:type size_z: int
	"""
	noise = Sets.noise
	
	amp = Sets.amp
	period = Sets.period
	
	land_map = [[0 for _ in range(size_z)] for _ in range(size_x)]
	map_dict: dict = {}
	
	for position in range(size_x * size_z * 2 - size_x * 2):
		# вычисление высоты y в координатах (x, z)
		x_pos = floor(position // size_x)
		z_pos = floor(position % size_z)
		y_pos = floor((noise([x_pos / period, z_pos / period]) + 0.5) * amp)
		try:
			land_map[int(x_pos)][int(z_pos)] = not not int(y_pos)
		except IndexError:
			pass
	
	for x in range(size_x):
		for z in range(size_z):
			map_dict[(x, z)] = land_map[x][z]
	
	spawn_zone = 150 // Sets.square_size
	center = Sets.Sc.h_width // Sets.square_size, Sets.Sc.h_height // Sets.square_size
	for i in range(Sets.Sc.h_width // Sets.square_size - spawn_zone, spawn_zone + Sets.Sc.h_width // Sets.square_size):
		for j in range(Sets.Sc.h_height // Sets.square_size - spawn_zone,
		               spawn_zone + Sets.Sc.h_height // Sets.square_size):
			if math.dist([i, j], center) <= spawn_zone:
				map_dict[i, j] = True
	
	return map_dict


class WorldMap:
	size = int(Sets.Sc.width / Sets.square_size), int(Sets.Sc.height / Sets.square_size)
	# шум Перлина
	land_map: dict = world_gen(*size)


if __name__ == '__main__':
	input("Это не основной файл. Откройте IslandCapture.py")
