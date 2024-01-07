from sets import SelectedInfo, ButtonsInfo, Sets
from world import WorldMap, find_path_a_star
from sussy_things import get_clicked_rectangle
import pygame as pg


def render_world(sc, offset):
	"""
	
	:param sc: Main surface
	:type sc: pg.Surface
	:param offset: Offset in "A" coordinate system
	:type offset: list[int, int] | tuple[int, int]
	:return: None
	"""
	screen_rect = pg.Rect((
		offset[0],
		offset[1],
		*Sets.Sc.res,
	))
	
	for chunk in WorldMap.chunks:
		if chunk.get_rect().colliderect(screen_rect):
			chunk.render_to_source(
				sc,
				offset,
			)
	for drop in WorldMap.drop_list:
		if screen_rect.collidepoint(drop.xy):
			drop.render(offset=offset)
		# pg.draw.rect(
		# 	sc,
		# 	(255, 0, 0),
		# 	[
		# 		chunk.ax - offset[0],
		# 		chunk.az - offset[1],
		# 		WorldMap.chunk_size * Sets.square_size,
		# 		WorldMap.chunk_size * Sets.square_size,
		# 	],
		# 	1
		# )


def scope_camera(sc, k) -> None:
	"""
	:param sc: Surface
	:param k: scope koof
	:return: None
	"""
	if k < 0:
		return
	sc.blit(
		source=pg.transform.scale_by(sc, k),
		dest=(
			(1 - k) * Sets.Sc.h_width,
			(1 - k) * Sets.Sc.h_height,
		),
	)


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
