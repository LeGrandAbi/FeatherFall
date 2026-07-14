import sys

from settings import s
import legrandabi_cards_utils as lcu
import generate_content as gc


timestamp = lcu.start_process()

lcu.init()

extensions = sys.argv[1:]

for extension in extensions:
	lcu.execute_command(["mkdir", f"{s.PATH_PRINTABLES}/{extension}"])
	lcu.execute_command(["mkdir", f"{s.PATH_STANDALONES}/{extension}"])
	filepath = f"src/json/extensions/{extension}.json"
	extension_content = lcu.load_extension(filepath)
	for category in extension_content:
		category_name = category["name"]
		if category["enabled"] == False:
			lcu.print_separator()
			lcu.print_info(f"Skipping {category_name}")
		else:
			type = category["type"]
			if type == "build":
				cards = gc.build_cards(extension, category_name)
				if s.VIEW_CARDS:
					lcu.view_images(cards, category_name)
				if s.MAKE_PRINTABLES:
					dimensions = category["dimensions"]
					gc.build_printables(cards, extension, category_name, dimensions)
			elif type == "copy":
				filenames = category["filenames"]
				gc.copy_content(extension, category_name, filenames)
			elif type == "script":
				filename = category["filename"]
				gc.execute_script(extension, category_name, filename)
			else:
				lcu.print_error(f"Unrecognized category type : {type}")

lcu.end_process(timestamp)







