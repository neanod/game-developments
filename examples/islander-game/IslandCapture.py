from pygame import Surface
from render import *
from matan import get_camera_offset, clamp, Vec2
from world import camera_logic, Camera, world_post_gen, get_pressed, EnemyList
from player import Player

PLAYER = Player()


post_gen = lambda gen_per_tick: [world_post_gen(*WorldMap.to_gen[i]) for i in range(gen_per_tick)]


def pressed_logic():
	# camera scope
	Camera.scope += ButtonsInfo.mwheel / 10
	ButtonsInfo.mwheel = 0
	Camera.scope = clamp(Camera.scope, 1, 2)
	# player movement
	pressed_num_wasd = (ButtonsInfo.W, ButtonsInfo.A, ButtonsInfo.S, ButtonsInfo.D)
	match sum(pressed_num_wasd):
		case 0 | 4:
			PLAYER.speed = 0
		case 1:
			PLAYER.speed = PLAYER.speed_def
			match pressed_num_wasd:
				case (False, False, False, True):
					PLAYER.facing = 'right'
				case (False, False, True, False):
					PLAYER.facing = 'down'
				case (False, True, False, False):
					PLAYER.facing = 'left'
				case (True, False, False, False):
					PLAYER.facing = 'up'
		case 2:
			PLAYER.speed = PLAYER.speed_def
			match pressed_num_wasd:
				# case (True, False, True, False)|(False, True, False, True):
				# 	pass
				case (True, True, False, False):
					PLAYER.facing = 'up-left'
				case (True, False, False, True):
					PLAYER.facing = 'up-right'
				case (False, False, True, True):
					PLAYER.facing = 'down-right'
				case (False, True, True, False):
					PLAYER.facing = 'down-left'
			# (True, True, False, False) | (True, False, False, True) | (False, False, True, True) | (False, True, True, False)
	

def main():
	pg.init()
	sc: Surface = pg.display.set_mode(Sets.Sc.res)
	pg.display.set_caption("Island Capture.")
	clock = pg.time.Clock()
	
	def game():
		"""
		return None
		"""
		gen_per_tick = 500
		running = True
		t = 0
		def logic():
			get_pressed()
			pressed_logic()
			get_clicked(get_camera_offset(Camera.pos))
			Camera.pos = camera_logic(Camera.pos, PLAYER.pos.xy, t)
			gen_need = min(gen_per_tick, len(WorldMap.to_gen))
			post_gen(gen_need)
			WorldMap.to_gen = WorldMap.to_gen[gen_need:]
			PLAYER.logic(WorldMap.land_colliding)
			[x.logic(PLAYER.pos) for x in EnemyList.enemies]
		while running:
			"""LOGIC"""
			logic()
			camera_offset = get_camera_offset(Camera.pos)
			"""
			Спавн врагов
			Стройка мостов на R
			"""
			"""RENDER"""
			render_world(sc, camera_offset)
			PLAYER.render(sc, camera_offset)
			[x.render(sc, camera_offset) for x in EnemyList.enemies]
			draw_path(sc, camera_offset)
			draw_selected(sc, camera_offset)
			scope_camera(sc, Camera.scope)
			pg.display.update()
			clock.tick(Sets.FPS)
			if not t % Sets.FPS:
				pg.display.set_caption(f"Island Capture. FPS: {round(clock.get_fps(), 1)}; "
				                       f"FT: {clock.get_time()}")
			t += 1
	
	game()


if __name__ == '__main__':
	main()
