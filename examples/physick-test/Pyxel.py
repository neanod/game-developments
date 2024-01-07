import numpy as np
from pygame import Color, Rect
from Settings import *
from typing import Union, Type


class Prop:
	def __init__(
			self,
			is_bedrock: bool = False,
			is_movable: bool = True,
	):
		self.is_bedrock: bool = is_bedrock
		self.is_movable: bool = is_movable
	
	@staticmethod
	def is_move_in(arr: np.ndarray) -> bool:
		"""
		:param arr: array 3 by 3
		:return: velocity Vector
		"""
		return not any((arr[pos] for pos in (
			(0, 1),
			(2, 1),
			(1, 0),
			(1, 2),
		)))
		

class Pyxel:
	def __init__(
			self, color: Color | tuple[int, int, int] | None,
			ppos: tuple[int, int] | Vector2 | None = None,
			spos: tuple[int, int] | Vector2 | None = None,
			prop: Union[Prop, Type[Prop]] = None,
	):
		self.color: Color = color if isinstance(color, Color) else Color(color) if color is not None else None
		self.ppos: Vector2 = Vector2(ppos) if ppos is not None else Vector2(spos) if spos is not None else None
		self.properties: Union[Prop, Type[Prop]] = prop
		assert all((self.ppos is not None, self.color is not None, self.properties is not None))
	
	@property
	def sc_left_top(self) -> Vector2:
		return self.ppos * Pyx.size + Vector2(0, Pyx.size)
	
	@property
	def sc_right_top(self) -> Vector2:
		return self.ppos * Pyx.size + Vector2(Pyx.size, 0)
	
	@property
	def sc_left_bottom(self) -> Vector2:
		return self.ppos * Pyx.size
	
	@property
	def sc_right_bottom(self) -> Vector2:
		return self.ppos * Pyx.size + Vector2(Pyx.size, Pyx.size)
	
	@property
	def px(self):
		return self.ppos.x
	
	@property
	def py(self):
		return self.ppos.y
	
	@property
	def pxy(self):
		return self.ppos.xy
	
	def get_rect_with_offset(self, *, soffset: tuple[int, int] | list[int, int] | Vector2) -> Rect:
		return self.get_rect().move(*soffset)
	
	def get_rect(self) -> Rect:
		return Rect(
			*self.sc_left_bottom,
			Pyx.size,
			Pyx.size,
		)
	
	def get_pos_with_offset(self, psoffset: tuple[int, int] | list[int, int] | Vector2) -> Vector2:
		return self.ppos + psoffset
