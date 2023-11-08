from sets import Sets
from numpy import floor


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
			
			i = 0
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
				i += 1
			all_paths = new_paths
			if not new_paths:
				return None


def clamp_color_channel(_x) -> int:
	return max(0, min(255, _x))


def world_post_gen(x, z):
	noise = Sets.noise
	
	y = floor((noise([x / Sets.period, z / Sets.period]) + 0.5) * Sets.amp)


def world_gen(size_x, size_z) -> list[list[int]]:
	"""
	:type size_x: int
	:type size_z: int
	"""
	noise = Sets.noise
	
	amp = Sets.amp
	period = Sets.period
	
	land_map = [[0 for ix in range(size_z)] for iix in range(size_x)]
	
	for position in range(size_x * size_z * 2 - size_x * 2):
		# вычисление высоты y в координатах (x, z)
		x_pos = floor(position // size_x)
		z_pos = floor(position % size_z)
		y_pos = floor((noise([x_pos / period, z_pos / period]) + 0.5) * amp)
		try:
			land_map[int(x_pos)][int(z_pos)] = not not int(y_pos)
		except IndexError:
			pass
	return land_map


class WorldMap:
	size = int(Sets.Sc.width / Sets.square_size), int(Sets.Sc.height / Sets.square_size)
	# шум Перлина
	land_map = world_gen(*size)


if __name__ == '__main__':
	input("Это не основной файл. Откройте IslandCapture.py")
