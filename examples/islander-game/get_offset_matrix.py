def get_offset_matrix(n, m) -> list[tuple[int, int]]:
	for x in range(-n // 2 + 1, n // 2 + 1):
		for y in range(-m // 2 + 1, m // 2 + 1):
			if not not x and not not y:
				yield x, y


def main():
	print(*(x for x in get_offset_matrix(5, 5)), sep=',\n')
	
	
if __name__ == '__main__':
	main()
