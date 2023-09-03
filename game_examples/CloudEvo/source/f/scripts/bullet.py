class Bullet:
	def __init__(self, angle, speed, x, y):
		self.color = (10, 10, 10)
		self.speed = speed
		self.angle = angle
		self.x = x
		self.y = y
	
	@property
	def angle_degrees(self):
		from math import degrees
		return degrees(self.angle)
	
	@property
	def pos(self):
		return self.x, self.y
	
	def set_next_pos(self):
		from math import sin, cos
		self.x += sin(self.angle) * self.speed
		self.y += cos(self.angle) * self.speed