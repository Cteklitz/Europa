import pygame
import Assets
from typing import NamedTuple

# Item class behaves as an immutable struct
class Item(NamedTuple):
    id: int
    name: str
    description: str
    iventory_sprite: list # to hold an asset from Assets
    ground_sprite: list # to hold an asset from Assets

pinkKeycard = Item(0, "Pink Keycard", "Seems to be a keycard for a pink area", Assets.pinkKeycardGround[0], Assets.pinkKeycardGround[0])


