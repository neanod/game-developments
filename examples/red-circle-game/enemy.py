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
		self.angle = 0
		self.hp = hp
	
	def do_moving(self, target_pos: list[int, int]):
		dist_to_target = dist([self.x, self.y], target_pos)
		if dist_to_target <= self.speed_dia[1]:
			pass
		else:
			self.speed = (atan(dist_to_target) / pi + 0.5) * (self.speed_dia[1] - self.speed_dia[0]) + self.speed_dia[0]
			"""
			self.speed вычисляется по принципу:
			atan в пределах speed_dia
			"""
			self.angle = -atan2(self.y - target_pos[1], self.x - target_pos[0]) + pi * 0.5
			self.x, self.y = self.next_pos
	
	def get_hp_rect_args(self, size):
		h = 20
		black_rect = [self.x - size / 2, self.y - size / 2 - 2 * h, size, h]
		green_rect = [self.x - size / 2, self.y - size / 2 - 2 * h, size * self.hp / self.max_hp, h]
		return [black_rect, green_rect]
		
	@property
	def next_pos(self):
		return [self.x + sin(-self.angle) * self.speed, self.y - cos(-self.angle) * self.speed]
	
	@property
	def pos(self):
		return [self.x, self.y]
	
