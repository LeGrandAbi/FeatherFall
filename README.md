# Feather Fall
My homebrew cooperation-based board game set in medieval times

This project contains a run.sh script that will build in a content/ directory th usable textures of cards, pannels, etc...

It uses LegrandabiCardUtils (LCU), my own framework for creating board games

# TODO

## Make a proper readme.md:
Rewrite this readme so taht it contains: a broad description (as above), a todo section (as rn), launch tutorial, files and program architecture, how the program works (lcu, main funcs, generate funcs, ...), personnal notes, project team description and listing, ...

## Revamp the insert_text() function:
It currently sucks... It's a lot of manual tideous tweakings.
Found in *src/python/legrandabi_card_utils.py*

## Fill lorem ipsum:
A lot of the cards (wich data can be found in *src/sheets/[extension]/*) do not have a proper decription, usually a lorem ispum. Feel free to fill them with whatever you want, the objective is (for the moment) quantity.
Cards that need description are mainly quests, missions and event cards.

## Create textures:
Many cards are still left without a texture (except a *WIP.png* one) like event, quests or competences cards.

## Play the game:
Obviously.