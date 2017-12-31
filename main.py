#
# https://en.wikipedia.org/wiki/CHIP-8
# http://devernay.free.fr/hacks/chip8/C8TECH10.HTM
#
import sched, time
from GameSystem import GameSystem
from Interpreter import Interpreter


# def parse_args():
	# settings and switches:
	# -game path
	# -include premade fonts?
	# -debug
	# sys.argv
	# pass


def debug_print(game_system):
	game_system.print_memory()
	game_system.print_register()
	game_system.print_stack()

	print("Stack index: {} [{}]".format(game_system.stack_index, game_system.stack[game_system.stack_index]))
	print("Address register: {} [{}]".format(game_system.I, game_system.memory[game_system.I]))
	print("PC: {} [{}]".format(game_system.PC, game_system.memory[game_system.PC]))

	print("Delay timer: {}".format(game_system.delay_timer))
	print("Sound timer: {}".format(game_system.sound_timer))

	game_system.screen.print_screen()


def start_game_loop(updates_per_second, callback, *args):
	scheduler = sched.scheduler(time.time, time.sleep)
	period = 1.0 / updates_per_second
	def loop():
		callback(*args)
		scheduler.enter(period, 0, loop, ())
	scheduler.enter(period, 0, loop, ())
	scheduler.run()


def update(game_system, interpreter, debug_mode):
	op = game_system.get_op()
	game_system.update_timers()
	interpreter.execute_op(op)
	game_system.increment_PC()

	# game_system.screen.print_screen()


def main():
	#game_file = 'ch8/Particle Demo [zeroZshadow, 2008].ch8'
	# game_file = 'ch8/IBM Logo.ch8'
	# game_file = 'ch8/Maze (alt) [David Winter, 199x].ch8'
	# game_file = 'ch8/Trip8 Demo (2008) [Revival Studios].ch8'
	game_file = 'ch8/Pong (1 player).ch8'
	
	debug_mode = True
	scheduler_mode = False
	fast_mode = True
	updates_per_second = 10

	game_system = GameSystem(debug_mode = debug_mode)
	interpreter = Interpreter(game_system, debug_mode = debug_mode)

	game_system.load_game(game_file)
	game_system.print_memory()
	game_system.screen.print_screen()
	game_system.PC = 512

	if scheduler_mode:
		start_game_loop(updates_per_second, update, game_system, interpreter, debug_mode)
	else:
		run = True
		iteration = 0
		while run:

			update(game_system, interpreter, debug_mode)
			iteration += 1

			if fast_mode:
				if iteration % 1000 == 0:
					game_system.screen.print_screen()
					print("Iteration {}".format(iteration))
				else:
					continue

			if debug_mode:
				key = input()
				if key == "q":
					debug_print(game_system)
					print("Quitting...")
					return 0 




if __name__ == '__main__':
	main()