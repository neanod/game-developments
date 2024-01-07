from pygame import Surface
from render import *
from sussy_things import get_camera_offset, clamp, Vec2
from world import camera_logic, Camera, world_post_gen, get_pressed, EnemyList, WorldMap, pre_world_gen, build_bridge
from player import Player
import asyncio
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
	if ButtonsInfo.R:
		ButtonsInfo.R = Sets.flush_bridge_building
		PLAYER.score -= build_bridge(PLAYER.bpos, get_clicked_rectangle(pg.mouse.get_pos(), get_camera_offset(Camera.pos)), PLAYER.score)


async def main():
	sc: Surface = pg.display.set_mode(Sets.Sc.res)
	post_gen = lambda rate: [world_post_gen(*WorldMap.to_gen[i]) for i in range(rate)]
	clock = pg.time.Clock()
	gen_per_tick = 500
	
	async def setup():
		PLAYER.pos = Vec2(Sets.Sc.center)
		Camera.pos = PLAYER.pos.xy
		pg.init()
		pg.display.set_caption("Island Capture.")
		pre_world_gen(sc)
		PLAYER.go_to_nearest_block()
		
		PLAYER.manager = pygame_gui.UIManager(Sets.Sc.res)
		PLAYER.hp_bar = pygame_gui.elements.UIProgressBar(
			relative_rect=PLAYER.RenderProperties.hp_bar_relative,
			manager=PLAYER.manager
		)
		PLAYER.hp_bar.border_colour = PLAYER.hp_bar.text_colour = pg.Color(0, 0, 0)
		PLAYER.hp_bar.text_shadow_colour = pg.Color(100, 100, 100)
		PLAYER.hp_bar.bar_filled_colour = pg.Color(0, 200, 0)
		PLAYER.hp_bar.bar_unfilled_colour = pg.Color(200, 0, 0)
	
	async def logic():
		get_pressed()
		pressed_logic()
		Camera.pos = camera_logic(Camera.pos, PLAYER.pos.xy, Sets.t, sc)
		gen_need = min(gen_per_tick, len(WorldMap.to_gen))
		post_gen(gen_need)
		WorldMap.to_gen = WorldMap.to_gen[gen_need:]
		PLAYER.logic(WorldMap.land_colliding, get_camera_offset(Camera.pos), Camera.scope)
		[x.logic(PLAYER.pos) for x in EnemyList.enemies]
		Camera.offset = get_camera_offset(Camera.pos)
		if not Sets.t % Sets.FPS:
			pg.display.set_caption(f"Island Capture. FPS: {round(clock.get_fps(), 1)}; FT: {clock.get_time()}")
		Sets.t += 1
	
	async def render():
		render_world(sc, Camera.offset)
		PLAYER.render(sc, Camera.offset)
		[x.render(sc, Camera.offset) for x in EnemyList.enemies]
		scope_camera(sc, Camera.scope)
		PLAYER.render_gui(sc)
		pg.display.update()
		clock.tick(Sets.FPS)
	
	# Camera.pos = PLAYER.pos
	
	async def game():
		await setup()
		while Sets.running:
			await logic()
			await render()
	
	await game()


if __name__ == '__main__':
	asyncio.run(main())
