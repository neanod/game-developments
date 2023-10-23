from math import sin, cos, atan2


class Bullet:
	def __init__(self, pos, speed, speed_direct):
		self.x = pos[0]
		self.y = pos[1]
		self.speed = speed
		self.angle = speed_direct
	
	@property
	def pos(self):
		return [self.x, self.y]
	
	@property
	def next_pos(self):
		return [self.x + sin(self.angle) * self.speed, self.y - cos(self.angle) * self.speed]
	
	def set_next_pos(self):
		self.x, self.y = self.next_pos
	
	def get_angle_to_target(self, target: list[int, int]):
		return atan2(self.y - target[1], target[0] - self.x)
	
	def rotate_to_pos(self, pos):
		self.angle = self.get_angle_to_target(pos)
