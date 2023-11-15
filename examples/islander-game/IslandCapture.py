from pygame import Surface, SurfaceType
from render import *


class Camera:
	pos = [0, 0]


def exit_game():
	pg.quit()
	quit(0)


def main():
	pg.init()
	sc: Surface | SurfaceType = pg.display.set_mode(Sets.Sc.res)
	pg.display.set_caption("Island Capture")
	
	def game():
		running = True
		while running:
			"""LOGIC"""
			for event in pg.event.get():
				match event.type:
					case pg.QUIT:
						exit_game()
					case pg.MOUSEBUTTONDOWN:
						match event.button:
							case 1:
								ButtonsInfo.LMB = True
							case 3:
								ButtonsInfo.RMB = True
					case pg.MOUSEBUTTONUP:
						match event.button:
							case 1:
								ButtonsInfo.LMB = False
							case 3:
								ButtonsInfo.RMB = False
			get_clicked()
			
			"""RENDER"""
			
			render_world(sc)
			draw_path(sc)
			draw_selected(sc)
			pg.display.update()
	
	game()


if __name__ == '__main__':
	main()
