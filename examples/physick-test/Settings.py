from pygame import Vector2


FPS = 60
instant_post_gen: bool = True


class Sc:
	width: int = 1920
	height: int = 1080
	h_width: int = width // 2
	h_height: int = height // 2
	res: Vector2 = Vector2(width, height)
	h_res: Vector2 = Vector2(h_width, h_height)


class SetsWorld:
	chunk_size = 8


class Pyx:
	size = 4
	try:
		assert not (Sc.width % size)
	except AssertionError:
		print(Sc.width % size)
		raise AssertionError
	try:
		assert not (Sc.height % size)
	except AssertionError:
		print(Sc.height % size)
		raise AssertionError
	