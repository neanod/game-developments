from App import App, Chunk, Pyxel, World


def main():
	App(world=World({(0, 0): Chunk(cpos=(0, 0))})).start()
	
	
if __name__ == '__main__':
	main()
	