from math import sin, cos, atan, atan2, dist, pi


class Enemy:
	def __init__(self, random_pos_function, speed_dia=None, hp=None):
		if speed_dia is None:
			speed_dia = [8, 12]
		if hp is None:
			hp = 64
		self.max_hp = hp
		self.x, self.y = random_pos_function()
		self.speed_dia = speed_dia
		self.speed = 0
		from random import randint
		self.angle = randint(0, 3141592653 * 2) / 1000000000
		self.hp = hp
	
	def do_moving(self, target_pos: list[int, int]):
		dist_to_target = dist([self.x, self.y], target_pos)
		if dist_to_target > self.speed_dia[1]:
			self.speed = (atan(dist_to_target) / pi + 0.5) * (self.speed_dia[1] - self.speed_dia[0]) + self.speed_dia[0]
			"""
			self.speed вычисляется по принципу:
			atan в пределах speed_dia
			"""
			target_angle = -atan2(self.y - target_pos[1], self.x - target_pos[0]) + pi * 0.5
			angle_r = self.angle - target_angle
			rotate_speed = 0.04
			if abs(angle_r) > rotate_speed * 4:
				if angle_r % (2 * pi) < -angle_r % (2 * pi):
					# left
					self.angle -= rotate_speed
				else:
					self.angle += rotate_speed
			self.x, self.y = self.next_pos
	
	def get_hp_rect_args(self, size):
		h = 20
		black_rect = [self.x - size / 2, self.y - size / 2 - 2 * h, size, h]
		green_rect = [self.x - size / 2, self.y - size / 2 - 2 * h, size * self.hp / self.max_hp, h]
		return [black_rect, green_rect]
	
	def warp_jump(self):
		self.x, self.y = [self.x + sin(-self.angle) * self.speed * 5, self.y - cos(-self.angle) * self.speed * 5]
		
	@property
	def next_pos(self):
		return [self.x + sin(-self.angle) * self.speed, self.y - cos(-self.angle) * self.speed]
	
	@property
	def pos(self):
		return [self.x, self.y]
	
