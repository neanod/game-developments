import random
from typing import List

import pygame as pg
from numpy import floor
from perlin_noise import PerlinNoise
from pygame import Surface, SurfaceType


# import pygame_gui as pgg


def main():
	pg.init()
	
	def find_path():
		start_pos = SelectedInfo.RMB_POS
		end_pos = SelectedInfo.LMB_POS
		
		old_points = list()
		
		if isinstance(start_pos, list) and isinstance(end_pos, list):
			world_map = WorldMap.land_map
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
		
	class ButtonsInfo:
		LMB = False
		RMB = False
		m_pos = [0, 0]
	
	class Sets:
		FPS: int = 60
		# square_size in [120, 60, 40, 30, 24, 20, 12, 10, 5, 2, 1]
		square_size: int = 40
		matching = True
		noise = PerlinNoise(octaves=4, seed=random.randint(1000, 1000000))
		
		class Sc:
			res: list[int] = [1920, 1080]
			width: int = res[0]
			height: int = res[1]
			h_width: int = width // 2
			h_height: int = height // 2
			center: list[int] = [h_width, h_height]
		
		amp = 1.5
		period = 2000 / square_size
	
	sc: Surface | SurfaceType = pg.display.set_mode(Sets.Sc.res)
	pg.display.set_caption("тесты с графами")
	
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
	
	def render_world():
		sc.fill((0, 0, 120))
		for x in range(WorldMap.size[0]):
			for z in range(WorldMap.size[1]):
				if WorldMap.land_map[x][z]:
					color = 0, 155, 0
					
					neighbours = list()  # [top, right, bottom, left]
					
					default_value = True
					radius = Sets.square_size // 3
					
					try:
						neighbours.append(WorldMap.land_map[x][z - 1])
					except IndexError:
						neighbours.append(default_value)
					try:
						neighbours.append(WorldMap.land_map[x + 1][z])
					except IndexError:
						neighbours.append(default_value)
					try:
						neighbours.append(WorldMap.land_map[x][z + 1])
					except IndexError:
						neighbours.append(default_value)
					try:
						neighbours.append(WorldMap.land_map[x - 1][z])
					except IndexError:
						neighbours.append(default_value)
					
					if Sets.matching:
						match neighbours:
							case [False, False, False, False]:
								pg.draw.rect(sc, color, [
										x * Sets.square_size,
										z * Sets.square_size,
										Sets.square_size,
										Sets.square_size,
									], border_radius=radius)
								
							case [False, False, False, True]:
								pg.draw.rect(sc, color, [
										x * Sets.square_size,
										z * Sets.square_size,
										Sets.square_size,
										Sets.square_size,
									], border_top_right_radius=radius, border_bottom_right_radius=radius)
							case [False, False, True, False]:
								pg.draw.rect(sc, color, [
										x * Sets.square_size,
										z * Sets.square_size,
										Sets.square_size,
										Sets.square_size,
									], border_top_right_radius=radius, border_top_left_radius=radius)
							case [False, True, False, False]:
								pg.draw.rect(sc, color, [
										x * Sets.square_size,
										z * Sets.square_size,
										Sets.square_size,
										Sets.square_size,
									], border_top_left_radius=radius, border_bottom_left_radius=radius)
							case [True, False, False, False]:
								pg.draw.rect(sc, color, [
										x * Sets.square_size,
										z * Sets.square_size,
										Sets.square_size,
										Sets.square_size,
									], border_bottom_left_radius=radius, border_bottom_right_radius=radius)
								
							case [False, False, True, True]:
								pg.draw.rect(sc, color, [
									x * Sets.square_size,
									z * Sets.square_size,
									Sets.square_size,
									Sets.square_size,
								], border_top_right_radius=radius)
							case [False, True, True, False]:
								pg.draw.rect(sc, color, [
									x * Sets.square_size,
									z * Sets.square_size,
									Sets.square_size,
									Sets.square_size,
								], border_top_left_radius=radius)
							case [True, True, False, False]:
								pg.draw.rect(sc, color, [
									x * Sets.square_size,
									z * Sets.square_size,
									Sets.square_size,
									Sets.square_size,
								], border_bottom_left_radius=radius)
							case [True, False, False, True]:
								pg.draw.rect(sc, color, [
									x * Sets.square_size,
									z * Sets.square_size,
									Sets.square_size,
									Sets.square_size,
								], border_bottom_right_radius=radius)
								
							case _:
								pg.draw.rect(sc, color, [
										x * Sets.square_size,
										z * Sets.square_size,
										Sets.square_size,
										Sets.square_size,
									],)
					else:
						pg.draw.rect(sc, color, [
								x * Sets.square_size,
								z * Sets.square_size,
								Sets.square_size,
								Sets.square_size,
							],)
						
	def exit_game():
		pg.quit()
		quit(0)
	
	def render_selected_rect(pos, color):
		pg.draw.rect(
			surface=sc,
			rect=[
				Sets.square_size * pos[0],
				Sets.square_size * pos[1],
				Sets.square_size,
				Sets.square_size,
			],
			color=color,
			width=3,
			border_radius=4
		)
		
	def clamp(_x, _min, _max):
		return max(_min, min(_max, _x))
	
	def get_clicked_rectangle(pos):
		return [clamp(pos[0], 0, Sets.Sc.width - 1) // Sets.square_size, clamp(pos[1], 0, Sets.Sc.height - 1) // Sets.square_size]
	
	class SelectedInfo:
		LMB_POS = None
		RMB_POS = None
	
	def draw_selected():
		if SelectedInfo.LMB_POS is not None:
			render_selected_rect(SelectedInfo.LMB_POS, (50, 50, 255))
		if SelectedInfo.RMB_POS is not None:
			render_selected_rect(SelectedInfo.RMB_POS, (255, 50, 50))
	
	def get_clicked():
		ButtonsInfo.m_pos = pg.mouse.get_pos()
		if ButtonsInfo.LMB:
			clicked_rect = get_clicked_rectangle(ButtonsInfo.m_pos)
			if WorldMap.land_map[clicked_rect[0]][clicked_rect[1]]:
				SelectedInfo.LMB_POS = clicked_rect
				update_path()
		if ButtonsInfo.RMB:
			clicked_rect = get_clicked_rectangle(ButtonsInfo.m_pos)
			if WorldMap.land_map[clicked_rect[0]][clicked_rect[1]]:
				SelectedInfo.RMB_POS = clicked_rect
				update_path()
	
	def draw_path():
		if Path.path:
			path = [[(x[0] + 0.5) * Sets.square_size, (x[1] + 0.5) * Sets.square_size] for x in Path.path]
			pg.draw.lines(
				surface=sc,
				color=(255, 255, 255),
				closed=False,
				points=path,
				width=10,
			)
	
	class Path:
		path = []
	
	def update_path():
		Path.path = find_path()
	
	def game():
		running = True
		t = 0
		while running:
			"""LOGIC"""
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
					case pg.MOUSEBUTTONUP:
						match event.button:
							case 1:
								ButtonsInfo.LMB = False
							case 3:
								ButtonsInfo.RMB = False
			get_clicked()
			t += 1
			
			"""RENDER"""
			render_world()
			draw_path()
			draw_selected()
			pg.display.update()
	
	game()
	

if __name__ == '__main__':
	main()
