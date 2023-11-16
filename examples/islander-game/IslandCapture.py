from math import cos

from numpy import sin
from pygame import Surface, SurfaceType
from render import *
from matan import get_camera_offset
from world import camera_logic, Camera, ToGen, world_post_gen
from player import Player

PLAYER = Player()


def post_gen(gen_per_tick) -> None:
	"""
	:return: None
	"""
	
	for i in range(gen_per_tick):
		world_post_gen(*ToGen.al[i])


def main():
	pg.init()
	sc: Surface | SurfaceType = pg.display.set_mode(Sets.Sc.res)
	pg.display.set_caption("Island Capture.")
	clock = pg.time.Clock()
	
	def game():
		"""
		return None
		"""
		gen_per_tick = 10
		running = True
		t = 0
		while running:
			"""LOGIC"""
			get_pressed()
			get_clicked(get_camera_offset(Camera.pos))
			Camera.pos = camera_logic(Camera.pos, PLAYER.pos, t)
			# post_gen(gen_per_tick)
			# ToGen.al = ToGen.al[gen_per_tick:]
			for i in ToGen.al:
				world_post_gen(*i)
			ToGen.al = list()
			camera_offset = get_camera_offset(Camera.pos)
			
			PLAYER.y -= sin(t / 60) * 16
			PLAYER.x -= cos(t / 60) * 16
			# TODO
			"""
			Определение острова - если окружен водой
			Спавн врагов - p(A)
			
			Нажать R чтобы построить мост
			"""
			
			"""RENDER"""
			render_world(sc, camera_offset)
			
			pg.draw.rect(
				sc,
				(255, 255, 255),
				Sets.Sc.cam_to_player_box,
				3,
				Sets.square_size,
			)
			
			PLAYER.render(sc, camera_offset)
			draw_path(sc, camera_offset)
			draw_selected(sc, camera_offset)
			pg.display.update()
			clock.tick(Sets.FPS)
			if not t % Sets.FPS:
				# каждую секунду
				pg.display.set_caption(f"Island Capture. FPS: {round(clock.get_fps(), 1)}; "
				                       f"FT: {clock.get_time()}")
			t += 1
	
	game()


if __name__ == '__main__':
	main()
