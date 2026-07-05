import pygame as pg
from math import ceil
import legrandabi_cards_utils as lcu
from settings import s
from pathlib import Path

def build_cards(extension, category):
    lcu.print_title(f"BUILDING {extension.upper()} {category.upper()}")

    if s.SAVE_CARDS:
        lcu.empty_directory(f"{s.PATH_STANDALONES}/{extension}/{category}")

    base = lcu.load_base(f"{s.PATH_BASES}/{extension}/{category}.png")
    sheet = lcu.load_sheet(f"{s.PATH_SHEETS}/{extension}/{category}.ods")
    instructions = lcu.load_build(f"{s.PATH_BUILDS}/{category}.json")

    cards = {}
    i = 1
    for card_info in sheet:
        lcu.print_separator()
        lcu.print_info(f"[{i}/{len(sheet)}] Building card : {card_info["id"]}")
        card = base.copy()
        for instruction in instructions:
            handle_instruction(instruction, card, card_info, extension, category)

        name = card_info["id"]

        if name in cards.keys():
            lcu.print_error(f"Id already given : {name}")

        cards[name] = card
        if s.SAVE_CARDS:
            filepath = f"{s.PATH_STANDALONES}/{extension}/{category}/{name}.png"
            lcu.save_image(card, filepath)
        i = i + 1
    lcu.print_separator()

    if len(sheet) != len(cards):
        lcu.print_error(f"Total number of id duplicates : {len(sheet) - len(cards)}")

    return cards


def build_printables(cards, extension, category, dimensions):
    lcu.print_title(f"BUILDING {extension.upper()} {category.upper()} PRINTABLES")

    lcu.empty_directory(f"{s.PATH_PRINTABLES}/{extension}/{category}")

    printables = {}
    if cards == {}:
        lcu.print_error("Cannot build printables from empty card set")
        return printables

    sheet = lcu.load_sheet(f"{s.PATH_SHEETS}/{extension}/{category}.ods")

    stack = []
    i = 0
    for image in cards.values():
        try:
            n = int(sheet[i]["n"])
        except ValueError:
            lcu.print_error(f"Incorrect \"n\" value for card \"{sheet[i]["id"]} : {sheet[i]["n"]}")
            n = 1
        for j in range(n):
            stack.append(image)
        i = i + 1
    lcu.shuffle(stack)

    dim_x, dim_y = dimensions
    width, height = stack[0].get_size()
    printable_size = (width*dimensions[0], height*dimensions[1])

    i = 1
    j = 0
    l = len(stack)
    n = ceil(l / (dim_x*dim_y))
    while stack != []:
        name = f"{category}_{i}"
        lcu.print_separator()
        lcu.print_info(f"[{i}/{n}] Building printable : {name}")
        printable = pg.Surface(printable_size)
        for y in range(dim_y):
            for x in range(dim_x):
                if stack != []:
                    lcu.print_info(f"[{j+1}/{l}] Adding card to printable")
                    card = stack.pop(0)
                    pos = (x*width, y*height)
                    printable.blit(card ,pos)
                    j = j + 1
        printables[name] = printable
        filepath = f"{s.PATH_PRINTABLES}/{extension}/{category}/{name}.png"
        lcu.save_image(printable, filepath)
        i = i + 1


def copy_content(extension, category, filenames):
    lcu.print_title(f"COPYING {extension.upper()} {category.upper()}")

    lcu.empty_directory(f"{s.PATH_STANDALONES}/{extension}/{category}")

    if filenames[0] == "all":
        filenames = []
        directory = Path(f"{s.PATH_ILLUSTRATIONS}/{extension}/{category}")
        filepaths = [f for f in directory.iterdir() if f.is_file()]
        for filepath in filepaths:
            path = str(filepath).split("/")
            filenames.append(path[-1])

    for filename in filenames:
        filepath = f"{s.PATH_ILLUSTRATIONS}/{extension}/{category}/{filename}"
        dest = f"{s.PATH_STANDALONES}/{extension}/{category}/{filename}"
        lcu.print_info(f"Copying \"{filename}\" to \"{dest}\"")
        lcu.execute_command(["cp", filepath, dest])


def handle_instruction(instruction, card, card_info, extension, category):
    match instruction["type"].lower():
        case "insert text" : 
            insert_text(instruction, card, card_info)
        case "insert image" : 
            filename = f"{card_info[instruction["collumn"]]}"
            filepath = f"{s.PATH_ILLUSTRATIONS}/{extension}/{category}/{filename}"
            insert_image(instruction, card, filepath)
        case "insert static image" :
            filepath = f"{instruction["filepath"]}"
            insert_image(instruction, card, filepath)
        case "insert label" :
            insert_label(instruction, card, extension)
        case "insert icons" :
            icons = card_info[instruction["collumn"]].split(", ")
            insert_icons(instruction, card, icons)
        case _ :
            lcu.print_error(f"Incorrect instruction type : \"{instruction["type"]}\"")



def insert_text(instruction, card, card_info):
    text = str(card_info[instruction["collumn"]])
    if text != "nan":
        color = instruction["color"]
        cpl = instruction["cpl"]
        rect = pg.Rect(instruction["pos"])
        font_path = f"{s.PATH_FONTS}/{instruction["font"]}.ttf"
        try:
            font = pg.font.Font(font_path, size=128)
        except FileNotFoundError:
            lcu.print_error(f"Couldn't load font : \"{font_path}\"")
            font = pg.font.Font(size=128)
        surf = lcu.render_text(text, font, color, cpl)
        lcu.print_info(f"Inserting text : {text}")
        apply_surf(surf, card, instruction)


def insert_image(instruction, card, filepath):
    image = lcu.load_image(filepath)
    lcu.print_info(f"Inserting image : {filepath}")
    apply_surf(image, card, instruction)


def apply_surf(surf, dest, instruction):
    rect = pg.Rect(instruction["pos"])
    specs = instruction["specs"]
    for args in specs:
        args = args.split(" ")
        match args[0]:
            case "fit" :
                surf = lcu.fit_surf(surf, rect)
            case "flip" :
                flip_x = "horizontal" in args
                flip_y = "vertical" in args
                surf = pg.transform.flip(surf, flip_x, flip_y)
            case "rotate" :
                rot = int(args[1])
                surf = pg.transform.rotate(surf, rot)
            case "background":
                # the background argument is a blit operation and is therefor treated later
                pass
            case _ :
                lcu.print_error(f"Incorrect specs argument : \"{args[0]}\"")
    if "background" in specs:
        new_dest = pg.Surface(dest.get_size(), pg.SRCALPHA)
        new_dest.blit(surf, surf.get_rect(center=rect.center))
        new_dest.blit(dest, (0,0))
        dest.blit(new_dest, (0,0))
    else:
        dest.blit(surf, surf.get_rect(center=rect.center))


def insert_label(instruction, card, extension):
    rect = pg.Rect(instruction["pos"])
    filepath = f"{s.PATH_LABELS}/{extension}.png"
    surf = pg.image.load(filepath).convert_alpha()
    surf = lcu.fit_surf(surf, rect)
    card.blit(surf, surf.get_rect(center=rect.center))


def insert_icons(instruction, card, icons):
    rect = pg.Rect(instruction["pos"])
    dx, dy = instruction["displacement"]
    offset = instruction["offset"]
    for icon in icons:
        filepath = f"{s.PATH_ICONS}/{icon}.png"
        surf = lcu.load_image(filepath)
        surf = lcu.fit_surf(surf, rect)
        card.blit(surf, surf.get_rect(center=rect.center))
        rect.x += dx*(rect.width + offset)
        rect.y += dy*(rect.width + offset)
