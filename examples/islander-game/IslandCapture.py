from pygame import Surface, SurfaceType
from render import *
from matan import get_camera_offset, get_pressed
from world import camera_logic, Camera
from player import Player


PLAYER = Player()


def main():
	pg.init()
	sc: Surface | SurfaceType = pg.display.set_mode(Sets.Sc.res, pg.FULLSCREEN)
	pg.display.set_caption("Island Capture.")
	clock = pg.time.Clock()
	
	def game():
		"""
		return None
		"""
		running = True
		t = 0
		while running:
			"""LOGIC"""
			get_pressed()
			get_clicked(get_camera_offset(Camera.pos))
			camera_logic(Camera.pos.copy(), PLAYER.pos, t)
			# TODO
			"""
			Определение острова - если окружен водой
			Спавн врагов - p(A)
			
			Нажать R чтобы построить мост
			"""
			
			"""RENDER"""
			render_world(sc, get_camera_offset(Camera.pos))
			draw_path(sc, get_camera_offset(Camera.pos))
			draw_selected(sc, get_camera_offset(Camera.pos))
			pg.display.update()
			clock.tick(Sets.FPS)
			t += 1
	
	game()


if __name__ == '__main__':
	main()
