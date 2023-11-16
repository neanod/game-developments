from sets import SelectedInfo, ButtonsInfo, Sets
from world import WorldMap, find_path_a_star
from matan import get_clicked_rectangle
import pygame as pg


def render_world(sc, offset):
	"""
	:type sc: pg.Surface
	:type offset: list[int, int] | tuple[int, int]
	"""
	
	sc.fill((0, 0, 120))
	color = 0, 155, 0
	block_offset = [-offset[0] // Sets.square_size, -offset[1] // Sets.square_size]
	for x in range(block_offset[0], WorldMap.size[0] + block_offset[0] + 1):
		for z in range(block_offset[1], WorldMap.size[1] + block_offset[1] + 1):
			if (x, z) in WorldMap.land_map.keys():
				if not WorldMap.land_map[x, z]:
					continue
				neighbours = list()  # [top, right, bottom, left]
				
				default_value = False
				radius = Sets.square_size // 3
				
				try:
					neighbours.append(WorldMap.land_map[x, z - 1])
				except KeyError:
					neighbours.append(default_value)
				try:
					neighbours.append(WorldMap.land_map[x + 1, z])
				except KeyError:
					neighbours.append(default_value)
				try:
					neighbours.append(WorldMap.land_map[x, z + 1])
				except KeyError:
					neighbours.append(default_value)
				try:
					neighbours.append(WorldMap.land_map[x - 1, z])
				except KeyError:
					neighbours.append(default_value)
				
				if (x, z) in WorldMap.land_map.keys():
					if Sets.matching:
						match neighbours:
							case [False, False, False, False]:
								pg.draw.rect(sc, color, [
									x * Sets.square_size + offset[0],
									z * Sets.square_size + offset[1],
									Sets.square_size,
									Sets.square_size,
								], border_radius=radius)
							
							case [False, False, False, True]:
								pg.draw.rect(sc, color, [
									x * Sets.square_size + offset[0],
									z * Sets.square_size + offset[1],
									Sets.square_size,
									Sets.square_size,
								], border_top_right_radius=radius, border_bottom_right_radius=radius)
							case [False, False, True, False]:
								pg.draw.rect(sc, color, [
									x * Sets.square_size + offset[0],
									z * Sets.square_size + offset[1],
									Sets.square_size,
									Sets.square_size,
								], border_top_right_radius=radius, border_top_left_radius=radius)
							case [False, True, False, False]:
								pg.draw.rect(sc, color, [
									x * Sets.square_size + offset[0],
									z * Sets.square_size + offset[1],
									Sets.square_size,
									Sets.square_size,
								], border_top_left_radius=radius, border_bottom_left_radius=radius)
							case [True, False, False, False]:
								pg.draw.rect(sc, color, [
									x * Sets.square_size + offset[0],
									z * Sets.square_size + offset[1],
									Sets.square_size,
									Sets.square_size,
								], border_bottom_left_radius=radius, border_bottom_right_radius=radius)
							
							case [False, False, True, True]:
								pg.draw.rect(sc, color, [
									x * Sets.square_size + offset[0],
									z * Sets.square_size + offset[1],
									Sets.square_size,
									Sets.square_size,
								], border_top_right_radius=radius)
							case [False, True, True, False]:
								pg.draw.rect(sc, color, [
									x * Sets.square_size + offset[0],
									z * Sets.square_size + offset[1],
									Sets.square_size,
									Sets.square_size,
								], border_top_left_radius=radius)
							case [True, True, False, False]:
								pg.draw.rect(sc, color, [
									x * Sets.square_size + offset[0],
									z * Sets.square_size + offset[1],
									Sets.square_size,
									Sets.square_size,
								], border_bottom_left_radius=radius)
							case [True, False, False, True]:
								pg.draw.rect(sc, color, [
									x * Sets.square_size + offset[0],
									z * Sets.square_size + offset[1],
									Sets.square_size,
									Sets.square_size,
								], border_bottom_right_radius=radius)
							
							case _:
								pg.draw.rect(sc, color, [
									x * Sets.square_size + offset[0],
									z * Sets.square_size + offset[1],
									Sets.square_size,
									Sets.square_size,
								], )
					else:
						pg.draw.rect(sc, color, [
							x * Sets.square_size + offset[0],
							z * Sets.square_size + offset[1],
							Sets.square_size,
							Sets.square_size,
						], )


def render_selected_rect(pos, color, sc, offset):
	pg.draw.rect(
		surface=sc,
		rect=[
			Sets.square_size * pos[0] + offset[0],
			Sets.square_size * pos[1] + offset[1],
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
			if WorldMap.land_map[clicked_rect]:
				SelectedInfo.LMB_POS = clicked_rect
				update_path()
	if ButtonsInfo.RMB:
		clicked_rect = get_clicked_rectangle(ButtonsInfo.m_pos, offset)
		if clicked_rect in WorldMap.land_map.keys():
			if WorldMap.land_map[clicked_rect]:
				SelectedInfo.RMB_POS = clicked_rect
				update_path()


def draw_path(sc, offset):
	if Path.path:
		path = [[(x[0] + 0.5) * Sets.square_size + offset[0], (x[1] + 0.5) * Sets.square_size + offset[1]] for x in Path.path]
		
		if len(path) - 1:
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
	if SelectedInfo.LMB_POS and SelectedInfo.RMB_POS:
		Path.path = find_path_a_star(SelectedInfo.RMB_POS, SelectedInfo.LMB_POS, WorldMap.land_map)
