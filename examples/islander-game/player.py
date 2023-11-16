from math import sqrt

from sets import Sets


class Player:
	def __init__(self, x=None, y=None, color=None, speed=None, facing=None) -> None:
		"""
		:type x: int | float
		:type y: int | float
		:type color: list[int, int, int] | tuple[int, int, int]
		:type speed: int | float
		:type facing: str
		:param facing: up, up-right, right, down-right, down, down-left, left, up-left
		"""
		if color is None:
			color = 155, 0, 0
		if x is None or y is None:
			x, y = Sets.Sc.center
		if speed is None:
			speed = 8
		if facing is None:
			facing = 'up'
		self.color = color
		self.pos = [int(x), int(y)]
		self.speed = speed
		self.facing = facing
	
	@property
	def x(self) -> int:
		return self.pos[0]
	
	@property
	def y(self) -> int:
		return self.pos[1]
	
	@property
	def speed_x(self):
		match self.facing:
			case 'up':
				return 0
			case 'up-right':
				return self.speed * 0.5 * sqrt(2)
			case 'right':
				return self.speed
			case 'down-right':
				return self.speed * 0.5 * sqrt(2)
			case 'down':
				return -0
			case 'down-left':
				return -self.speed * 0.5 * sqrt(2)
			case 'left':
				return -self.speed
			case 'up-left':
				return -self.speed * 0.5 * sqrt(2)
		
	@property
	def speed_y(self):
		match self.facing:
			case 'up':
				return -self.speed
			case 'up-right':
				return -self.speed * 0.5 * sqrt(2)
			case 'right':
				return 0
			case 'down-right':
				return self.speed * 0.5 * sqrt(2)
			case 'down':
				return self.speed
			case 'down-left':
				return self.speed * 0.5 * sqrt(2)
			case 'left':
				return 0
			case 'up-left':
				return -self.speed * 0.5 * sqrt(2)
		
	@property
	def speed_dim(self):
		return self.speed_x, self.speed_y
				
	
def main():
	input("Этот файл не предназначен для запуска")


if __name__ == '__main__':
	main()
