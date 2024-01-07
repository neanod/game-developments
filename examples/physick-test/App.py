from math import floor
from typing import Callable
from Settings import *
from Pyxel import Pyxel
import pygame as pg
import numpy as np


class Chunk:
	def __init__(self, cpos: pg.Vector2 | tuple[int | float, int | float] | list[int | float, int | float]):
		self.land = np.ndarray(
			shape=(SetsWorld.chunk_size, SetsWorld.chunk_size),
			dtype=Pyxel,
		)
		self.pos = cpos if isinstance(cpos, pg.Vector2) else pg.Vector2(cpos) if isinstance(cpos,
		                                                                                    (list, tuple)) else None
		self.sc: pg.Surface = pg.Surface((Pyx.size * SetsWorld.chunk_size,) * 2)
		assert self.pos is not None
	
	def __getitem__(self, item):
		return self.land[item]
	
	def __setitem__(self, key, value):
		self.land[key] = value


class World:
	def __init__(self, land_map: dict[tuple[int, int], Chunk] | None):
		self.land: dict[tuple[int, int], Chunk] = land_map if land_map is not None else False
		self.p_res: tuple[int, int] = tuple(map(int, Sc.res // Pyx.size))
		assert self.land is not False
	
	def __getitem__(self, item):
		return self.land.get(item)
	
	def __setitem__(self, key, value):
		self.land[key] = value
	
	def get_small_image(self, area: tuple[Vector2, Vector2],
	                    post_gen_function: Callable[[tuple[int, int]], None]) -> pg.Surface:
		arr = self.get_rect_area_to_array(area=area, post_gen_function=post_gen_function)
		res = pg.Surface(self.p_res)
		for x in range(arr.shape[0]):
			for y in range(arr.shape[1]):
				res.set_at((x, y), arr[x, y].color)
		return res
	
	@staticmethod
	def convert_ppos(*ppos) -> tuple[tuple[int, int], tuple[int, int]]:
		"""
		Converter to chunk and in-chunk pos
		:param ppos: pixel absolute position
		:return: chunk, in_chunk_pos
		"""
		return (
			(
				ppos[0] // SetsWorld.chunk_size,
				ppos[1] // SetsWorld.chunk_size,
			),
			(
				ppos[0] % SetsWorld.chunk_size,
				ppos[1] % SetsWorld.chunk_size,
			)
		)
	
	def get_rect_area_to_array(self, area: tuple[Vector2, Vector2],
	                           post_gen_function: Callable[[tuple[int, int]], None]) -> np.ndarray[Pyxel]:
		x_range = range(floor(area[0].x), floor(area[1].x))
		y_range = range(floor(area[0].y), floor(area[1].y))
		x_size: int = x_range.stop - x_range.start
		y_size: int = y_range.stop - y_range.start
		result = np.empty((x_size, y_size), dtype=Pyxel)
		for x in x_range:
			for y in y_range:
				chunk, in_chunk_pos = self.convert_ppos(x, y)
				ch: np.ndarray | None = self[chunk]
				if ch is None or ch[in_chunk_pos] is None:
					post_gen_function((x, y))
					if not instant_post_gen:
						continue
					ch: np.ndarray = self[chunk]
					assert ch is not None
				result[x - x_range.start, y - y_range.start] = ch[in_chunk_pos]
		return result
	
	def render(self, offset: Vector2, *, post_gen_function: Callable[[tuple[int, int]], None], surface: pg.Surface):
		pg.transform.scale_by(
			self.get_small_image(
				(
					Vector2(offset),
					Vector2(offset) + Vector2(Sc.res // Pyx.size)
				),
				post_gen_function),
			Pyx.size,
			surface
		)


class App:
	def __init__(self, *, world: World = None):
		self.sc: pg.Surface = pg.display.set_mode(Sc.res)
		self.world: World = world if world is not None else World(dict())
		self.timer: int = 0  # frames
		self.clock: pg.Clock = pg.Clock()
		self.camera_pos: Vector2 = Vector2(Sc.h_res)
	
	def start(self):
		self.world_gen()
		while True:
			self.logic()
			self.render()
			self.time_delay()
	
	def logic(self):
		for event in pg.event.get():
			match event.type:
				case pg.QUIT:
					pg.quit()
					quit()
		pg.display.set_caption(f"FPS: {self.clock.get_fps()}")
		self.camera_pos += (1, 0)
	
	def render(self):
		self.world.render(self.camera_pos, post_gen_function=self.world_post_gen, surface=self.sc)
		pg.display.update()
	
	def time_delay(self):
		self.clock.tick(FPS)
	
	def world_gen(self):
		...
	
	def world_post_gen(self, pxy: tuple[int, int]):
		vec = pg.Vector2(pxy)
		vec.rotate_ip_rad(np.pi / 8 + vec.x / 100)
		vec /= Pyx.size / 2
		block_color = floor(127.5 * (np.sin(vec.x) * np.sin(vec.y) + 1))
		block_color = pg.Color(block_color, block_color, block_color)
		converted = self.world.convert_ppos(*pxy)
		if converted[0] not in self.world.land:
			self.world.land[converted[0]] = Chunk(converted[0])
		self.world[converted[0]][converted[1]] = Pyxel(color=block_color, ppos=pxy)
