from Screen import Screen
import pygame


class GameSystem(object):
	"""docstring for GameSystem"""
	def __init__(self, screen_width = 64, screen_height = 32, memory_size = 4096, stack_size = 16, load_generic_fonts = False, debug_mode = False):
		super(GameSystem, self).__init__()

		self.screen_width = screen_width
		self.screen_height = screen_height
		self.memory_size = memory_size
		self.stack_size = stack_size
		self.load_generic_fonts = load_generic_fonts
		self.debug_mode = debug_mode

		pygame.init()

		self.initialize_system()
		if self.load_generic_fonts:
			self.load_fonts()

	
	def initialize_system(self):
		# Memory is a block of 4096 bytes in CHIP-8. THey are 8bits each. (Ignore the fact that these are 32 bits here)
		self.memory = [0 for i in range(4096)]
		# The program counter, or where we are in the memory
		self.PC = 0

		# 16 registers, from V0 to VF, each are supposed to be 8 bit
		self.V = [0 for i in range(16)]
		# I is an address register, used to store addresses, and is usually 16 bits
		self.I = 0

		# The stack is an array of 16 bit values. It is usually at least length 16
		self.stack = [0 for i in range(16)]
		# The 8 bit stack pointer shows us where we are in the stack
		self.stack_index = 0

		# The delay timer counts down at 60Hz until it hits 0. It is used to schedule events
		self.delay_timer = 0
		# The sound timer counts down at 60Hz until it hits 0. While above 0, it makes the system beep
		self.sound_timer = 0

		# The screen that will be displayed to the user
		self.screen = Screen(self.screen_width, self.screen_height)


	def load_to_memory(self, data, start_location):
		current_location = start_location

		for byte in data:
			if current_location < len(self.memory):
				self.memory[current_location] = byte
				current_location += 1
			else:
				raise RuntimeError("Program exceeds memory")

		return current_location


	def load_fonts(self, start_location = 0):
		fonts = [
			b"\xF0\x90\x90\x90\xF0\x00", # 0
			b"\x20\x60\x20\x20\x70\x00", # 1
			b"\xF0\x10\xF0\x80\x20\x00", # 2
			b"\xF0\x10\xF0\x10\xF0\x00", # 3
			b"\x90\x90\xF0\x10\x10\x00", # 4
			b"\xF0\x80\xF0\x10\xF0\x00", # 5
			b"\xF0\x80\xF0\x90\xF0\x00", # 6
			b"\xF0\x10\x20\x40\x40\x00", # 7
			b"\xF0\x90\xF0\x90\xF0\x00", # 8
			b"\xF0\x90\xF0\x10\xF0\x00", # 9
			b"\xF0\x90\xF0\x90\x90\x00", # A
			b"\xE0\x90\xE0\x90\xE0\x00", # B
			b"\xF0\x80\x80\x80\xF0\x00", # C
			b"\xE0\x90\x90\x90\xE0\x00", # D
			b"\xF0\x80\xF0\x80\xF0\x00", # E
			b"\xF0\x80\xF0\x80\x80\x00"  # F
		]

		memory_location = start_location
		for font in fonts:
			memory_location = self.load_to_memory(font, memory_location)


	def load_game(self, game_path, start_location = 512):
		with open(game_path, 'rb') as game_file:
			game_data = game_file.read()
			self.load_to_memory(game_data, start_location)


	def print_memory(self, print_empty_blocks = False):
		print("{:>5}: {:>3} {:>3} {:>3} {:>3} {:>3} {:>3} {:>3} {:>3}".format("Index",0,1,2,3,4,5,6,7))
		print("-"*38)
		message = "{:>5}: ".format(0)
		empty = True

		for i in range(self.memory_size):
			message += "{:>3X} ".format(self.memory[i])

			if self.memory[i] != 0:
				empty = False

			if (i != 0) and (i % 8 == 7):
				if print_empty_blocks or not empty:
					print(message)
				empty = True
				message = "{:>5}: ".format(i+1)


	def print_register(self):
		print("+{}+{}+".format("-"*9, "-"*6))
		print("|{:>9}|{:>6}|".format("Register", "Value"))
		print("+{}+{}+".format("-"*9, "-"*6))
		for i in range(len(self.V)):
			print("|{:^9X}|{:>6d}|".format(i, self.V[i]))
		print("+{}+{}+".format("-"*9, "-"*6))


	def print_stack(self):
		for i in range(len(self.stack)):
			print("|{:^4X}|{:>6d}|".format(i, self.stack[i]))


	def skip_next_instruction(self):
		if (self.PC+2 < self.memory_size):
			self.PC += 2
		else:
			raise RuntimeError("Index out of bounds of memory")

	def jump(self, address):
		if (address >= 0) and (address < self.memory_size):
			self.PC = address
		else:
			raise RuntimeError("Index out of bounds of memory")

	def execute_subroutine(self, address):
		self.stack[self.stack_index] = self.PC
		self.stack_index += 1
		self.PC = address

	def return_from_subroutine(self):
		if self.stack_index > 0:
			self.stack_index -= 1
		else:
			raise RuntimeError("Index out of bounds of stack")
		self.PC = self.stack[self.stack_index]

	def get_op(self):
		return "{:02X}{:02X}".format(self.memory[self.PC], self.memory[self.PC+1])

	def increment_PC(self):
		self.PC += 2

	def update_timers(self):
		# Delay timer
		if self.delay_timer > 0:
			self.delay_timer -= 1

		# Sound timer
		if self.sound_timer > 0:
			self.sound_timer -= 1

	def get_pressed(self, button):
		if pygame.key.get_pressed()[pygame.K_KP0]:
			return True