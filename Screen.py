class Screen(object):
	"""Represents the display which the player will see"""
	def __init__(self, width, height):
		super(Screen, self).__init__()
		self.width = width
		self.height = height
		self.screen_data = [[0 for i in range(self.width)] for j in range(self.height)]

	def print_screen(self):
		top_bar = "+{}+".format('-' * self.width)
		print(top_bar)
		for y in range(self.height):
			screen_row = ""
			for x in range(self.width):
				screen_row += str(self.get_pixel(x, y))
			print("|{}|".format(screen_row))
		print(top_bar)


	def set_pixel(self, x, y, state):
		self.screen_data[y][x] = state


	def get_pixel(self, x, y):
		return self.screen_data[y][x]
		
	def clear(self):
		for y in range(self.height):
			for x in range(self.width):
				self.set_pixel(x, y, '0')
