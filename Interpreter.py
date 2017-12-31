import random

class Interpreter(object):
	"""Interpreter"""
	def __init__(self, game_system, debug_mode = False):
		super(Interpreter, self).__init__()
		self.game_system = game_system
		self.debug_mode = debug_mode


	def random_byte(self):
		# return "{0:08b}".format(random.randint(0, 255))
		return random.randint(0, 255)
	

	def execute_op(self, op):
		op = op.upper()
		game_system = self.game_system

		if self.debug_mode:
			if self.debug_mode:
				print("OP: {}".format(op))

		
		if op == '00E0':
			# Clear the display
			if self.debug_mode:
				print("Clear the display")
			game_system.screen.clear()

		elif op == '00EE':
			# Return from subroutine
			if self.debug_mode:
				print("Return from subroutine")
			game_system.return_from_subroutine()

		elif op[0] == '0':
			# Jump to sys routine at location (unused in modern machines)
			if self.debug_mode:
				print("Jump to sys routine at location (unused in modern machines/not implemented)")
			loc = op[1:]			
			print("0nnn not implemented")
			pass

		elif op[0] == '1':
			# Jump to location
			if self.debug_mode:
				print("Jump to location")
			address = int(op[1:], 16)
			game_system.jump(address)

		elif op[0] == '2':
			# Call subroutine at location
			if self.debug_mode:
				print("Call subroutine at location")
			address = int(op[1:], 16)
			game_system.execute_subroutine(address)

		elif op[0] == '3':
			# Skip next instruction if Vx == kk
			if self.debug_mode:
				print("Skip next instruction if Vx == kk")
			x = int(op[1], 16)
			kk = int(op[2:], 16)
			
			if (game_system.V[x] == kk):
				game_system.skip_next_instruction()

		elif op[0] == '4':
			# Skip next instruction if Vx != kk
			if self.debug_mode:
				print("Skip next instruction if Vx != kk")
			x = int(op[1], 16)
			kk = int(op[2:], 16)

			if (game_system.V[x] != kk):
				game_system.skip_next_instruction()

		elif op[0] == '5':
			# Skip next instruction if Vx == Vy
			if self.debug_mode:
				print("Skip next instruction if Vx == Vy")
			x = int(op[1], 16)
			y = int(op[2], 16)

			if (game_system.V[x] != game_system.V[y]):
				game_system.skip_next_instruction()

		elif op[0] == '6':
			# Set Vx = kk
			if self.debug_mode:
				print("Set Vx = kk")
			x = int(op[1], 16)
			kk = int(op[2:], 16)
			game_system.V[x] = kk

		elif op[0] == '7':
			# Add kk to Vx
			if self.debug_mode:
				print("Add kk to Vx")
			x = int(op[1], 16)
			kk = op[2:]
			game_system.V[x] += int(kk, 16)

		elif op[0] == '8':
			x = int(op[1], 16)
			y = int(op[2], 16)
			sub_op = op[3]

			if sub_op == '0':
				# Set Vx = Vy
				if self.debug_mode:
					print("Set Vx = Vy")
					game_system.V[x] = game_system.V[y]

			elif sub_op == '1':
				# Set Vx = Vx OR Vy
				if self.debug_mode:
					print("Set Vx = Vx OR Vy")
				game_system.V[x] = game_system.V[x] | game_system.V[y]

			elif sub_op == '2':
				# Set Vx = Vx AND Vy
				if self.debug_mode:
					print("Set Vx = Vx AND Vy")
				game_system.V[x] = game_system.V[x] & game_system.V[y]

			elif sub_op == '3':
				# Set Vx = Vx XOR Vy
				if self.debug_mode:
					print("Set Vx = Vx XOR Vy")
				game_system.V[x] = game_system.V[x] ^ game_system.V[y]

			elif sub_op == '4':
				# Set Vx = Vx + Vy
				# Set VF = carry
				# The values of Vx and Vy are added together.
				# If the result is greater than 8 bits (i.e., > 255,) VF is set to 1, otherwise 0.
				# Only the lowest 8 bits of the result are kept, and stored in Vx.
				if self.debug_mode:
					print("Set Vx = Vx + Vy\nSet VF = carry")

				result = game_system.V[x] + game_system.V[y]
				if result > 255:
					result -= 255
					game_system.V[15] = 1
				else:
					game_system.V[15] = 0
				game_system.V[x] = result

			elif sub_op == '5':
				# Set Vx = Vx - Vy
				# Set VF = NOT borrow
				if self.debug_mode:
					print("Set Vx = Vx - Vy\nSet VF = NOT borrow")
				
				result = game_system.V[x] - game_system.V[y]
				if result < 0:
					game_system.V[15] = 0
				else:
					game_system.V[15] = 1
				game_system.V[x] = result

			elif sub_op == '6':
				# Set Vx = Vx SHR 1
				if self.debug_mode:
					print("Set Vx = Vx SHR 1")
				game_system.V[x] = game_system.V[x] >> 1

			elif sub_op == '7':
				# Set Vx = Vy - Vx
				# Set VF = NOT borrow
				if self.debug_mode:
					print("Set Vx = Vy - Vx\nSet VF = NOT borrow")
				result = game_system.V[y] - game_system.V[x]
				if result < 0:
					game_system.V[15] = 0
				else:
					game_system.V[15] = 1
				game_system.V[x] = result

			elif sub_op == 'E':
				# Set Vx = Vx SHL 1
				if self.debug_mode:
					print("Set Vx = Vx SHL 1")
				game_system.V[x] = game_system.V[x] << 1

		elif op[0] == '9':
			# Skip next instruction if Vx != Vy
			if self.debug_mode:
				print("Skip next instruction if Vx != Vy")
			x = int(op[1], 16)
			y = int(op[2], 16)

			if (game_system.V[x] != game_system.V[y]):
				game_system.skip_next_instruction()

		elif op[0] == 'A':
			# Set I (address register) to location
			if self.debug_mode:
				print("Set I (address register) to location")
			address = int(op[1:], 16)
			game_system.I = address

		elif op[0] == 'B':
			# Jump to location + V0
			if self.debug_mode:
				print("Jump to location + V0")
			address_offset = int(op[1:], 16)
			game_system.jump(game_system.V[0] + address_offset)

		elif op[0] == 'C':
			# Set Vx = random_byte & kk
			if self.debug_mode:
				print("Set Vx = random_byte & kk")
			x = int(op[1], 16)
			kk = int(op[2:], 16)
			game_system.V[x] = self.random_byte() & kk

		elif op[0] == 'D':
			# Display n-byte sprite starting at location I at (Vx, Vy)
			# Set VF = collision
			if self.debug_mode:
				print("Display n-byte sprite starting at location I at (Vx, Vy)\nSet VF = collision")
			x = int(op[1], 16)
			y = int(op[2], 16)
			n = int(op[3], 16)

			game_system.V[15] = 0
			
			for i in range(n):
				sprite = "{0:08b}".format(game_system.memory[game_system.I+i])

				for j in range(len(sprite)):
					# Calculate the x position of the pixel
					x_pos = game_system.V[x] + j
					if x_pos >= game_system.screen.width:
						x_pos = x_pos % game_system.screen.width

					# Calculate the y position of the pixel
					y_pos = game_system.V[y] + i
					if y_pos >= game_system.screen.height:
						y_pos = y_pos % game_system.screen.height

					# Compare the new pixel to the existing pixel to check for collisions
					existing_pixel = game_system.screen.get_pixel(x_pos, y_pos)
					new_pixel = sprite[j]
					pixel_result = int(existing_pixel) ^ int(new_pixel)

					# If collision, set collision flag
					if (existing_pixel != 0) and not pixel_result:
						game_system.V[15] = 1

					# Set pixel
					game_system.screen.set_pixel(x_pos, y_pos, pixel_result)

			if self.debug_mode:
				game_system.screen.print_screen()
				print("Display {}-byte sprite starting at location {} at ({},{})\nSet VF = {}".format(n, game_system.I, x_pos, y_pos, game_system.V[15]))

		elif op[0] == 'E':
			x = op[1]
			sub_op = op[2:]

			if sub_op == '9E':
				# Skip next instruction if key with value Vx is pressed
				if self.debug_mode:
					print("Skip next instruction if key with value Vx is pressed")
				if game_system.get_pressed(x):
					game_system.skip_next_instruction()

			elif sub_op == 'A1':
				# Skip next instruction if key with value Vx is NOT pressed
				if self.debug_mode:
					print("Skip next instruction if key with value Vx is NOT pressed")
				if not game_system.get_pressed(x):
					game_system.skip_next_instruction()

		elif op[0] == 'F':
			x = int(op[1], 16)
			sub_op = op[2:]
			
			if sub_op == '07':
				# Set Vx = delay_timer
				if self.debug_mode:
					print("Set Vx = delay_timer")
				game_system.V[x] = game_system.delay_timer

			elif sub_op == '0A':
				# Block until keypress, store value in Vx
				if self.debug_mode:
					print("Block until keypress, store value in Vx")
				print("Fx0A not implemented")
				pass

			elif sub_op == '15':
				# Set delay_timer = Vx
				if self.debug_mode:
					print("Set delay_timer = Vx")
				game_system.delay_timer = game_system.V[x]

			elif sub_op == '18':
				# Set sound_timer = Vx
				if self.debug_mode:
					print("Set sound_timer = Vx")
				game_system.sound_timer = game_system.V[x]

			elif sub_op == '1E':
				# I = I + Vx
				if self.debug_mode:
					print("I = I + Vx")
				game_system.I += game_system.V[x]

			elif sub_op == '29':
				# Set I = location of sprite for digit Vx (font)
				if self.debug_mode:
					print("Set I = location of sprite for digit Vx (font)")
				address = x * 6 # Each font sprite is 6 bytes long
				game_system.I = address

			elif sub_op == '33':
				# Store BCD representaion of Vx in memory locations I, I+1, and I+2
				if self.debug_mode:
					print("Store BCD representaion of Vx in memory locations I, I+1, and I+2")

				value = str(game_system.V[x])
				for i in range(len(value)):
					game_system.memory[game_system.I + i] = int(value[i])

			elif sub_op == '55':
				# Store registers V0 to Vx in memory starting at location I
				if self.debug_mode:
					print("Store registers V0 to Vx in memory starting at location I")
				for i in range(len(game_system.V)):
					game_system.memory[game_system.I + i] = game_system.V[i]

			elif sub_op == '65':
				# Read registers V0 to Vx from memory starting at location I
				if self.debug_mode:
					print("Read registers V0 to Vx from memory starting at location I")
				for i in range(len(game_system.V)):
					game_system.V[i] = game_system.memory[game_system.I + i]

