import json
from pandas_ods_reader import read_ods
import pygame as pg
import traceback
from datetime import datetime
import random
import subprocess

from settings import s
from image_viewer import ImageViewer


def init():
	pg.init()
	pg.font.init()
	pg.display.set_mode((100,100)).convert_alpha()
	execute_command(["mkdir", "content"])
	execute_command(["mkdir", s.PATH_STANDALONES])
	execute_command(["mkdir", s.PATH_PRINTABLES])

	# ... assures the directory achitecture (src/ and content/)

######################################################################################################################################

def view_images(images_dict, title):
	if len(images_dict) == 0:
		print_error("Empty dictionnary given to the image viewer")
	else:
		print_title(f"image viewer : {title}")
		print_info("Initializing the image viewer")
		viewer = ImageViewer(images_dict, title)
		print_info("Running the image viewer")
		viewer.run()
		print_info("The image viewer closed with no failures")

######################################################################################################################################

def fit_surf(surf, rect):
	surf_rect = surf.get_rect()
	fitted_rect = surf_rect.fit(rect)
	fitted_surf = pg.transform.scale(surf, (fitted_rect.width, fitted_rect.height))
	return fitted_surf
	

def render_text(text, font, color, max_len=50):
	words = text.split()
	lines = []
	line = ""
	while words != []:
		current_word = words.pop(0)
		if (len(line) + len(current_word) <= max_len):
			line = line + current_word + " "
		else:
			lines.append(line)
			line = current_word + " "
	if (len(lines) == 0) or (line != ""):
		lines.append(line)
	lines_render = [font.render(line, True, color) for line in lines]
	surf_width = max([line.get_width() for line in lines_render])
	surf_height = len(lines) * lines_render[0].get_height()
	surf = pg.Surface((surf_width, surf_height), pg.SRCALPHA)
	y = 0
	x = surf_width/2
	for line in lines_render:
		surf.blit(line, line.get_rect(midtop=(x,y)))
		y = y + line.get_height()
	return surf

######################################################################################################################################

def print_info(text, forced=False):
	if s.VERBOSE or forced:
		print(f"\033[{s.PRINT_INFO_COLOR}m[INFO] [{get_time_str()}] {text}\033[0m")


def print_error(text="", e=None):
	message = f"\033[{s.PRINT_ERROR_COLOR}m[WARNING] [{get_time_str()}] {text}"
	if e != None:
		tb = ''.join(traceback.format_exception(e))
		message = message + " : " + tb
	message = message + "\033[0m"
	print(message)


def print_title(text):
	if s.VERBOSE:
	    print(f"\033[{s.PRINT_TITLE_COLOR}m" + "============" + (len(text)*'=') + "============")
	    print("=========== " + text.upper() + " ===========")
	    print("============" + (len(text)*'=') + "============" + "\033[0m")
	else:
		print(f"========== {text} ==========")


def print_separator(forced=False):
	if s.VERBOSE or forced:
		print(f"\033[{s.PRINT_INFO_COLOR}m===============================================\033[0m")


def get_time_str():
	now = datetime.now()
	s = now.strftime("%H:%M:%S.%f")
	return s[:-3]

######################################################################################################################################

def load_image(filepath):
    try:
        image = pg.image.load(filepath).convert_alpha()
    except FileNotFoundError as e:
        print_error(f"Couldn't load image : {filepath}")
        image = pg.image.load(f"{s.PATH_ILLUSTRATIONS}/wip.png").convert_alpha()
    return image


def load_base(filepath):
    print_info(f"Loading base : {filepath}")
    try:
        base = pg.image.load(filepath).convert_alpha()
    except FileNotFoundError as e:
        print_error("Couldn't load base", e)
        base = pg.image.load(f"{s.PATH_BASES}/wip.png").convert_alpha()
    return base


def load_sheet(filepath):
	print_info(f"Loading sheet : {filepath}")
	sheet = []
	try:
		data = read_ods(filepath)
	except FileNotFoundError as e:
		print_error("Couldn't load sheet, it has been replaced by an empty one", e)
		sheet = []
		return sheet

	i = 0
	while (i != len(data)) and (str(data.iloc[i, 0]) != "nan"):
		d = {}
		j = 0
		while j != len(data.columns):
			d[data.columns[j]] = data.iloc[i, j]
			j = j + 1
		sheet.append(d)
		i = i + 1
	return sheet


def load_build(filepath):
    print_info(f"Loading build : {filepath}")
    try:
        with open(filepath, 'r') as f:
            build = json.load(f)
            f.close()
    except FileNotFoundError as e:
        print_error("Couldn't load build, it has been replaced by a empty one", e)
        build = []
    return build


def load_extension(filepath):
    print_info(f"Loading extension : {filepath}")
    try:
        with open(filepath, 'r') as f:
            extension = json.load(f)
            f.close()
    except FileNotFoundError as e:
        print_error("Couldn't load extension, it has been replaced by a default one", e)
        extension = []
    return extension


def save_image(image, filepath):
	try:
		print_info(f"Saving image : {filepath}")
		pg.image.save(image, filepath)
	except FileNotFoundError:
		print_error(f"Couldn't save image: {filepath}")


def execute_command(command):
	subprocess.run(command)


def empty_directory(filepath):
	subprocess.run(["rm", "-r", filepath])
	subprocess.run(["mkdir", filepath])

######################################################################################################################################

def shuffle(l):
	random.shuffle(l)

######################################################################################################################################

def start_process():
	print_separator(True)
	print_info(f"Starting process", forced=True)
	print_separator(True)
	
	return datetime.now()

def end_process(timestamp):
	now = datetime.now()
	print_separator(True)
	print_info("Ending process", forced=True)
	print_info(f"Time took : {now - timestamp}", forced=True)
	print_separator(True)


