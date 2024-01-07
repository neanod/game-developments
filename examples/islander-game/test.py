def bresenham(x0, y0, x1, y1):
	dx = abs(x1 - x0)
	dy = abs(y1 - y0)
	sx = 1 if x0 < x1 else -1
	sy = 1 if y0 < y1 else -1
	err = dx - dy
	res = []
	while True:
		res.append((x0, y0))
		if x0 == x1 and y0 == y1:
			break
		e2 = 2 * err
		if e2 > -dy:
			err -= dy
			x0 += sx
		if e2 < dx:
			err += dx
			y0 += sy
	return res


def bresenham_with_width(width, x0, y0, x1, y1):
	tin = set(bresenham(x0, y0, x1, y1))
	res = set()
	cell: tuple[int, int]
	for cell in tin:
		for delta_x in range(-width // 2 + 1, width // 2 + 1):
			for delta_y in range(-width // 2 + 1, width // 2 + 1):
				res.add((cell[0] + delta_x, cell[1] + delta_y))
	return res


br = bresenham_with_width(3, 10, 4, 20, 14)


for x in range(40):
	for y in range(40):
		print('##' if (x, y) in br else '--', end='')
	print()
