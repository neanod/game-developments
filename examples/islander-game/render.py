from sets import SelectedInfo, ButtonsInfo, Sets
from world import WorldMap, find_path_a_star
from matan import get_clicked_rectangle, exit_game, get_color
import pygame as pg


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


def render_world(sc, offset):
	"""
	
	:param sc: Main surface
	:type sc: pg.Surface
	:param offset: Offset in "A" coordinate system
	:type offset: list[int, int] | tuple[int, int]
	:return: None
	"""
	a_screen_rect = pg.Rect((
		offset[0],
		offset[1],
		Sets.Sc.width,
		Sets.Sc.height,
	))
	
	for chunk in WorldMap.chunks:
		if chunk.get_rect().colliderect(a_screen_rect):
			chunk.render_to_source(
				sc,
				offset,
			)
		pg.draw.rect(
			sc,
			(255, 0, 0),
			[
				chunk.ax - offset[0],
				chunk.az - offset[1],
				WorldMap.chunk_size * Sets.square_size,
				WorldMap.chunk_size * Sets.square_size,
			],
			1
		)


def alternate_render_world(sc, offset):
	"""
	:type sc: pg.Surface
	:type offset: tuple[int, int]
	"""
	
	block_offset: list[int, int] = [int(offset[0] // Sets.square_size), int(offset[1] // Sets.square_size)]
	
	land_map = WorldMap.land_map
	for x in range(block_offset[0], WorldMap.size[0] + 1 + block_offset[0]):
		for z in range(block_offset[1], WorldMap.size[1] + block_offset[1] + 2):
			if (x, z) not in land_map.keys():
				continue
			rect = pg.Rect(
				[
					x * Sets.square_size - offset[0],
					z * Sets.square_size - offset[1],
					Sets.square_size,
					Sets.square_size,
				]
			)
			color = get_color(land_map[x, z])
			neighbours = list()  # [top, right, bottom, left]
			
			default_value = 0
			radius = Sets.square_size // 3
			
			if land_map[x, z] > Sets.water_level:
				
				if Sets.matching:
					try:
						neighbours.append(WorldMap.land_map[x, z - 1] > Sets.water_level)
					except KeyError:
						neighbours.append(default_value)
					try:
						neighbours.append(WorldMap.land_map[x + 1, z] > Sets.water_level)
					except KeyError:
						neighbours.append(default_value)
					try:
						neighbours.append(WorldMap.land_map[x, z + 1] > Sets.water_level)
					except KeyError:
						neighbours.append(default_value)
					try:
						neighbours.append(WorldMap.land_map[x - 1, z] > Sets.water_level)
					except KeyError:
						neighbours.append(default_value)
				
				else:
					pg.draw.rect(sc, color, rect)
				
				if (x, z) in WorldMap.land_map.keys():
					if Sets.matching:
						match neighbours:
							case [False, False, False, False]:
								pg.draw.rect(sc, color, rect, border_radius=radius)
							
							case [False, False, False, True]:
								pg.draw.rect(sc, color, rect, border_top_right_radius=radius,
								             border_bottom_right_radius=radius)
							case [False, False, True, False]:
								pg.draw.rect(sc, color, rect, border_top_right_radius=radius,
								             border_top_left_radius=radius)
							case [False, True, False, False]:
								pg.draw.rect(sc, color, rect, border_top_left_radius=radius,
								             border_bottom_left_radius=radius)
							case [True, False, False, False]:
								pg.draw.rect(sc, color, rect, border_bottom_left_radius=radius,
								             border_bottom_right_radius=radius)
							
							case [False, False, True, True]:
								pg.draw.rect(sc, color, rect, border_top_right_radius=radius)
							case [False, True, True, False]:
								pg.draw.rect(sc, color, rect, border_top_left_radius=radius)
							case [True, True, False, False]:
								pg.draw.rect(sc, color, rect, border_bottom_left_radius=radius)
							case [True, False, False, True]:
								pg.draw.rect(sc, color, rect, border_bottom_right_radius=radius)
							
							case _:
								pg.draw.rect(sc, color, rect)
			else:
				pg.draw.rect(sc, color, rect)


def render_selected_rect(pos, color, sc, offset):
	pg.draw.rect(
		surface=sc,
		rect=[
			Sets.square_size * pos[0] - offset[0],
			Sets.square_size * pos[1] - offset[1],
			Sets.square_size,
			Sets.square_size,
		],
		color=color,
		width=4,
		border_radius=6
	)


def draw_selected(sc, offset):
	if SelectedInfo.LMB_POS is not None:
		render_selected_rect(SelectedInfo.LMB_POS, (50, 50, 255), sc, offset)
	if SelectedInfo.RMB_POS is not None:
		render_selected_rect(SelectedInfo.RMB_POS, (255, 50, 50), sc, offset)


def get_clicked(offset):
	m_pos = pg.mouse.get_pos()
	ButtonsInfo.m_pos = m_pos[0], m_pos[1]
	if ButtonsInfo.LMB:
		clicked_rect = get_clicked_rectangle(ButtonsInfo.m_pos, offset)
		if clicked_rect in WorldMap.land_map.keys():
			if WorldMap.land_map[clicked_rect] > Sets.water_level:
				SelectedInfo.LMB_POS = clicked_rect
				update_path()
	if ButtonsInfo.RMB:
		clicked_rect = get_clicked_rectangle(ButtonsInfo.m_pos, offset)
		if clicked_rect in WorldMap.land_map.keys():
			if WorldMap.land_map[clicked_rect] > Sets.water_level:
				SelectedInfo.RMB_POS = clicked_rect
				update_path()


def draw_path(sc, offset):
	if Path.path:
		if len(Path.path) - 1:
			pg.draw.aalines(
				surface=sc,
				color=(255, 255, 255),
				closed=False,
				points=[
					[
						(x[0] + 0.5) * Sets.square_size - offset[0],
						(x[1] + 0.5) * Sets.square_size - offset[1]
					] for x in Path.path
				],
			)


class Path:
	path = []


def update_path():
	if SelectedInfo.LMB_POS and SelectedInfo.RMB_POS:
		Path.path = find_path_a_star(SelectedInfo.RMB_POS, SelectedInfo.LMB_POS, WorldMap.land_map)
