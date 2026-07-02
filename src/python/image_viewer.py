import pygame as pg
from settings import s


class ImageViewer:
	def __init__(self, images_dict, title):
		self.title = title
		self.names = [key for key in images_dict.keys()]
		self.images = [value for value in images_dict.values()]

		self.image = None
		self.window = pg.display.set_mode(s.IMAGEVIEWER_WINDOW_SIZE, pg.RESIZABLE)
		self.active = False

		self.ptr = 0
		self.collumns = 1
		self.rows = 1

		self.font = pg.font.Font(size=s.IMAGEVIEWER_HUD_FONT_SIZE)



	def run(self):
		self.change_image()
		self.active = True
		while self.active:
			self.handle_events()
			self.update_display()


	def update_display(self):
		self.window.fill(s.IMAGEVIEWER_BG_COLOR)
		window_rect = self.window.get_rect()
		rect = self.image.get_rect().fit(window_rect)
		image = pg.transform.scale(self.image, (rect.width, rect.height))
		self.window.blit(image, image.get_rect(center=window_rect.center))
		self.draw_hud()
		pg.display.flip()


	def handle_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.active = False
			elif event.type == pg.KEYDOWN:
				if event.key in s.IMAGEVIEWER_KEYS_EXIT:
					self.active = False
				elif event.key in s.IMAGEVIEWER_KEYS_RIGHT:
					self.increment_pointer()
				elif event.key in s.IMAGEVIEWER_KEYS_LEFT:
					self.decrement_pointer()
				elif event.key in s.IMAGEVIEWER_KEYS_ADD_COLLUMN:
					self.add_collumn()
				elif event.key in s.IMAGEVIEWER_KEYS_REMOVE_COLLUMN:
					self.remove_collumn()
				elif event.key in s.IMAGEVIEWER_KEYS_ADD_ROW:
					self.add_row()
				elif event.key in s.IMAGEVIEWER_KEYS_REMOVE_ROW:
					self.remove_row()


	def increment_pointer(self):
		self.ptr += self.collumns * self.rows
		if self.ptr >= len(self.images):
			self.ptr = 0
		self.change_image()


	def decrement_pointer(self):
		self.ptr -= self.collumns * self.rows
		if self.ptr < 0:
			self.ptr = len(self.images) - 1
			self.ptr -= self.ptr % (self.collumns * self.rows)
		self.change_image()


	def add_collumn(self):
		self.collumns += 1
		self.ptr = 0
		self.change_image()


	def remove_collumn(self):
		if self.collumns != 1:
			self.collumns = self.collumns - 1
			self.ptr = 0
			self.change_image()


	def add_row(self):
		self.rows += 1
		self.ptr = 0
		self.change_image()


	def remove_row(self):
		if self.rows != 1:
			self.rows = self.rows - 1
			self.ptr = 0
			self.change_image()


	def change_image(self):
		width = self.images[self.ptr].get_width()
		height = self.images[self.ptr].get_height()
		self.image = pg.Surface((width*self.collumns, height*self.rows))
		self.image.fill(s.IMAGEVIEWER_BG_COLOR)

		j = 0
		while j != self.rows:
			i = 0
			while i != self.collumns:
				p = self.ptr + i + j*self.collumns
				if p < len(self.images):
					image = self.images[p]
					pos = (width*i, height*j)
					self.image.blit(image, pos)
				i = i + 1 
			j = j + 1 

		showed = self.names[self.ptr:self.ptr + self.rows*self.collumns]
		pg.display.set_caption(f"Image Viewer : {self.title}")
		print(f"Showing : {", ".join(showed)}")


	def draw_hud(self):
		lines = [
			f"PTR : {self.ptr}",
			f"COL : {self.collumns}",
			f"ROW : {self.rows}",
		]
		
		i = 0
		for line in lines:
			surf = self.font.render(line, True, s.IMAGEVIEWER_HUD_FONT_COLOR)
			pos = (s.IMAGEVIEWER_HUD_X, s.IMAGEVIEWER_HUD_Y + s.IMAGEVIEWER_HUD_FONT_SPACING*s.IMAGEVIEWER_HUD_FONT_SIZE*i)
			self.window.blit(surf, pos)
			i += 1
