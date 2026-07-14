import pygame as pg

class Settings:
	def __init__(self):
		self.VERBOSE = True

		self.SAVE_CARDS = True
		self.VIEW_CARDS = False
		self.MAKE_PRINTABLES = True

		self.PATH_SCRIPTS = "src/python/scripts"
		self.PATH_BASES = "src/images/bases"
		self.PATH_SHEETS = "src/sheets"
		self.PATH_BUILDS = "src/json/builds"
		self.PATH_EXTENSIONS = "src/json/extensions"
		self.PATH_ILLUSTRATIONS = "src/images/illustrations"
		self.PATH_FONTS = "src/fonts"
		self.PATH_LABELS = "src/images/labels"
		self.PATH_ICONS = "src/images/icons"
		self.PATH_STANDALONES = "content/standalones"
		self.PATH_PRINTABLES = "content/printables"

		self.IMAGEVIEWER_WINDOW_SIZE = (800, 800)
		self.IMAGEVIEWER_CAPTION = "Image Viewer"
		self.IMAGEVIEWER_BG_COLOR = (255, 255, 255)
		self.IMAGEVIEWER_KEYS_EXIT = [pg.K_RETURN, pg.K_ESCAPE]
		self.IMAGEVIEWER_KEYS_LEFT = [pg.K_a, pg.K_LEFT]
		self.IMAGEVIEWER_KEYS_RIGHT = [pg.K_d, pg.K_RIGHT]
		self.IMAGEVIEWER_KEYS_REMOVE_COLLUMN = [pg.K_4, pg.K_KP_4]
		self.IMAGEVIEWER_KEYS_ADD_COLLUMN = [pg.K_5, pg.K_KP_5]
		self.IMAGEVIEWER_KEYS_REMOVE_ROW = [pg.K_7, pg.K_KP_7]
		self.IMAGEVIEWER_KEYS_ADD_ROW = [pg.K_8, pg.K_KP_8]
		self.IMAGEVIEWER_HUD_X = 0
		self.IMAGEVIEWER_HUD_Y = 0
		self.IMAGEVIEWER_HUD_FONT_SPACING = 0.75
		self.IMAGEVIEWER_HUD_FONT_SIZE = 32
		self.IMAGEVIEWER_HUD_FONT_COLOR = (0,0,0)

		self.PRINT_INFO_COLOR = 0
		self.PRINT_TITLE_COLOR = 36
		self.PRINT_ERROR_COLOR = 37

s = Settings()