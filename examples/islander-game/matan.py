from sets import Sets


def clamp(_x, _min, _max):
	return max(_min, min(_max, _x))


def get_clicked_rectangle(pos):
	return [clamp(pos[0], 0, Sets.Sc.width - 1) // Sets.square_size,
	        clamp(pos[1], 0, Sets.Sc.height - 1) // Sets.square_size]

