from math import *


class Bullet:
	def __init__(self, pos, angle, speed, size=16):
		self.size = size
		self.speed = speed
		self.angle = angle
		self.x = pos[0]
		self.y = pos[1]
	
	@property
	def pos(self):
		return self.x, self.y
	
	@property
	def draw_pos(self):
		return self.x - self.size/2, self.y - self.size/2
	
	@property
	def rangle(self):
		return radians(self.angle)
	
	@property
	def next_pos(self):
		return self.x + sin(self.rangle) * self.speed, self.y + cos(self.rangle) * self.speed
	
	def check_out_of_screen(self, screen_size):
		"""
		True if out of screen
		"""
		return self.x > screen_size[0] or self.y > screen_size[1] or self.x + self.size < 0 or self.y + self.size < 0
