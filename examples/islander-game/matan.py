from sets import Sets
import pygame as pg


def clamp(_x, _min, _max):
	return max(_min, min(_max, _x))


def get_clicked_rectangle(pos, offset):
	x = (pos[0] - offset[0]) // Sets.square_size
	y = (pos[1] - offset[1]) // Sets.square_size
	return x, y


def sum_list(m: list[list]) -> list:
	res = list()
	for i in range(len(m[0])):
		res.append(sum([m[x][i] for x in range(len(m))]))
	return res


def get_camera_offset(camera_pos):
	return camera_pos[0] - Sets.Sc.h_width, camera_pos[1] - Sets.Sc.h_height


def exit_game():
	pg.quit()
	quit(0)

