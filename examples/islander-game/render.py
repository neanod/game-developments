from sets import SelectedInfo, ButtonsInfo
from world import *
from matan import get_clicked_rectangle
import pygame as pg


def render_world(sc):
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
							], )
				else:
					pg.draw.rect(sc, color, [
						x * Sets.square_size,
						z * Sets.square_size,
						Sets.square_size,
						Sets.square_size,
					], )


def render_selected_rect(pos, color, sc):
	pg.draw.rect(
		surface=sc,
		rect=[
			Sets.square_size * pos[0],
			Sets.square_size * pos[1],
			Sets.square_size,
			Sets.square_size,
		],
		color=color,
		width=4,
		border_radius=6
	)


def draw_selected(sc):
	if SelectedInfo.LMB_POS is not None:
		render_selected_rect(SelectedInfo.LMB_POS, (50, 50, 255), sc)
	if SelectedInfo.RMB_POS is not None:
		render_selected_rect(SelectedInfo.RMB_POS, (255, 50, 50), sc)


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


def draw_path(sc):
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
	Path.path = find_path(SelectedInfo.RMB_POS, SelectedInfo.LMB_POS, WorldMap.land_map)
