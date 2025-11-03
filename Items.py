import pygame
import Assets
from typing import NamedTuple

# Item class behaves as an immutable struct
class Item(NamedTuple):
    id: str # name to be used in code (USE CAMELCASE, USE SAME NAME AS ITEM INSTANCE NAME)
    name: str # Name to be displayed in game
    description: str
    inventory_sprite: list # to hold an asset from Assets
    ground_sprite: list # to hold an asset from Assets, for items that are never found on ground just reuse inventory sprite
    buttonType: str # use or equip

redPetriInv = pygame.image.load("Assets/redpetriInv.png")
bluePetriInv = pygame.image.load("Assets/bluepetriInv.png")
yellowPetriInv = pygame.image.load("Assets/yellowpetriInv.png")

pinkKeycard = Item("pinkKeycard", "Pink Keycard", "Seems to be a keycard for a pink area", Assets.pinkKeycard, Assets.pinkKeycardGround, "equip")

bandage = Item("bandage", "Bandage", "A roll of gauze used for covering wounds to stop bleeding", Assets.bandage, Assets.bandageGround, "use")

redPetri = Item("redPetri", "Petri Dish", "A petri dish containing red droplets", redPetriInv, Assets.redPetriGround, "equip")
bluePetri = Item("bluePetri", "Petri Dish", "A petri dish containing blue blobs", bluePetriInv, Assets.bluePetriGround, "equip")
yellowPetri = Item("yellowPetri", "Petri Dish", "A petri dish containing yellow particles", yellowPetriInv, Assets.yellowPetriGround, "equip")

letterTile = Item("letterTile", "Tile", "A ceramic tile with a letter incribed on it", Assets.letterTile, Assets.letterTile, "equip")

electricalTape = Item("electricalTape", "Electric Tape", "A plastic tape used for repairing electrical devices and wires", Assets.tapeInv, Assets.tapeGround, "equip")
mop = Item("mop", "Mop", "A standard mop used to clean floors", Assets.mopInv, Assets.mopGround, "equip")


