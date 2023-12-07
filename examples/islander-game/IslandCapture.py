from pygame import Surface
from render import *
from matan import get_camera_offset, clamp, Vec2
from world import camera_logic, Camera, world_post_gen, get_pressed, EnemyList, WorldMap, pre_world_gen
from player import Player
import pygame_gui


PLAYER = Player(land=WorldMap, enemy_list=EnemyList.enemies, hp_max=1000)


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
	post_gen = lambda rate: [world_post_gen(*WorldMap.to_gen[i]) for i in range(rate)]
	pg.display.set_caption("Island Capture.")
	clock = pg.time.Clock()
	gen_per_tick = 500
	running = True
	pre_world_gen(sc)
	PLAYER.manager = pygame_gui.UIManager(Sets.Sc.res)
	PLAYER.hp_bar = pygame_gui.elements.UIProgressBar(
			relative_rect=PLAYER.RenderProperties.hp_bar_relative,
			manager=PLAYER.manager
		)
	PLAYER.hp_bar.border_colour = PLAYER.hp_bar.text_colour = pg.Color(0, 0, 0)
	PLAYER.hp_bar.text_shadow_colour = pg.Color(100, 100, 100)
	PLAYER.hp_bar.bar_filled_colour = pg.Color(0, 200, 0)
	PLAYER.hp_bar.bar_unfilled_colour = pg.Color(200, 0, 0)
	
	def logic(t):
		get_pressed()
		pressed_logic()
		Camera.pos = camera_logic(Camera.pos, PLAYER.pos.xy, t, sc)
		gen_need = min(gen_per_tick, len(WorldMap.to_gen))
		post_gen(gen_need)
		WorldMap.to_gen = WorldMap.to_gen[gen_need:]
		PLAYER.logic(WorldMap.land_colliding, get_camera_offset(Camera.pos), sc)
		[x.logic(PLAYER.pos) for x in EnemyList.enemies]
		if not t % Sets.FPS:
			pg.display.set_caption(f"Island Capture. FPS: {round(clock.get_fps(), 1)}; FT: {clock.get_time()}")
	
	def game():
		t = 0
		PLAYER.pos = Vec2(Sets.Sc.center)
		PLAYER.go_to_nearest_block()
		while running:
			"""LOGIC"""
			logic(t)
			camera_offset = get_camera_offset(Camera.pos)
			"""RENDER"""
			render_world(sc, camera_offset)
			PLAYER.render(sc, camera_offset)
			[x.render(sc, camera_offset) for x in EnemyList.enemies]
			scope_camera(sc, Camera.scope)
			PLAYER.post_render(sc)
			pg.display.update()
			clock.tick(Sets.FPS)
			t += 1
	
	game()


if __name__ == '__main__':
	main()
