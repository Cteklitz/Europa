import pygame
import Assets
from typing import NamedTuple

# Item class behaves as an immutable struct
class Item(NamedTuple):
    id: str # name to be used in code (USE CAMELCASE, USE SAME NAME AS ITEM INSTANCE NAME)
    name: str # Name to be displayed in game
    description: str
    iventory_sprite: list # to hold an asset from Assets
    ground_sprite: list # to hold an asset from Assets, for items that are never found on ground just reuse inventory sprite

pinkKeycard = Item("pinkKeycard", "Pink Keycard", "Seems to be a keycard for a pink area", Assets.pinkKeycardGround, Assets.pinkKeycardGround)

bandage = Item("bandage", "Bandage", "A roll of gauze used for covering wounds to stop bleeding", Assets.bandage, Assets.bandageGround)

redPetri = Item("redPetri", "Petri Dish", "A petri dish containing red droplets", Assets.redPetri, Assets.redPetriGround)
bluePetri = Item("bluePetri", "Petri Dish", "A petri dish containing blue blobs", Assets.bluePetri, Assets.bluePetriGround)
yellowPetri = Item("yellowPetri", "Petri Dish", "A petri dish containing yellow particles", Assets.yellowPetri, Assets.yellowPetriGround)


