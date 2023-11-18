from math import sqrt
from sets import Sets
from pygame import draw, Surface


class Player:
	def __init__(self, x=None, y=None, color=None, speed_def=None, facing=None) -> None:
		"""
		:type x: int | float
		:type y: int | float
		:type color: list[int, int, int] | tuple[int, int, int]
		:type speed_def: int | float
		:type facing: str
		:param facing: up, up-right, right, down-right, down, down-left, left, up-left
		"""
		if color is None:
			color = 155, 0, 0
		if x is None or y is None:
			x, y = Sets.Sc.center
		if speed_def is None:
			speed_def = 8
		if facing is None:
			facing = 'up'
		self.color = color
		self.x, self.y = [int(x), int(y)]
		self.speed_def = speed_def
		self.speed = speed_def
		self.facing = facing
		self.sq2 = sqrt(2) / 2
	
	@property
	def pos(self) -> list[int, int]:
		return [self.x, self.y]
	
	@property
	def speed_x(self):
		match self.facing:
			case 'up':
				return 0
			case 'up-right':
				return self.speed * self.sq2
			case 'right':
				return self.speed
			case 'down-right':
				return self.speed * self.sq2
			case 'down':
				return -0
			case 'down-left':
				return -self.speed * self.sq2
			case 'left':
				return -self.speed
			case 'up-left':
				return -self.speed * self.sq2
			case _:
				print(f"invalid player facing \"{self.facing}\"")
				raise ValueError
	
	@property
	def speed_y(self):
		match self.facing:
			case 'up':
				return -self.speed
			case 'up-right':
				return -self.speed * self.sq2
			case 'right':
				return 0
			case 'down-right':
				return self.speed * self.sq2
			case 'down':
				return self.speed
			case 'down-left':
				return self.speed * self.sq2
			case 'left':
				return 0
			case 'up-left':
				return -self.speed * self.sq2
	
	@property
	def speed_dim(self):
		return self.speed_x, self.speed_y
	
	def render(self, sc: Surface, offset):
		# draw.rect(
		# 	sc,
		# 	(255, 255, 255),
		# 	Sets.Sc.cam_to_player_box,
		# 	3,
		# 	Sets.square_size,
		# )
		draw.circle(
			sc,
			self.color,
			[
				self.x - offset[0],
				self.y - offset[1],
			],
			Sets.square_size // 1.5
		)
	
	def logic(self):
		self.x += self.speed_x
		self.y += self.speed_y


def main():
	input("Этот файл не предназначен для запуска")


if __name__ == '__main__':
	main()
