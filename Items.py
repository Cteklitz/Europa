import pygame
import Assets
from typing import NamedTuple

# Item class behaves as an immutable struct
class Item(NamedTuple):
    id: str # name to be used in code (USE CAMELCASE, USE SAME NAME AS ITEM INSTANCE NAME)
    name: str # Name to be displayed in game
    description: str
    iventory_sprite: list # to hold an asset from Assets
    ground_sprite: list # to hold an asset from Assets

pinkKeycard = Item("pinkKeycard", "Pink Keycard", "Seems to be a keycard for a pink area", Assets.pinkKeycardGround[0], Assets.pinkKeycardGround[0])

redPetri = Item("redPetri", "Petri Dish", "A petri dish containing red droplets", Assets.redPetri[0], Assets.redPetriGround[0])


