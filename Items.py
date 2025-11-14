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

greenKeycard = Item("greenKeycard", "Green Keycard", "Seems to be a keycard... that is green", Assets.greenKeycard, Assets.greenKeycardGround, "equip")

bandage = Item("bandage", "Bandage", "A roll of gauze used for covering wounds to stop bleeding", Assets.bandage, Assets.bandageGround, "use")

redPetri = Item("redPetri", "Petri Dish", "A petri dish containing red droplets", redPetriInv, Assets.redPetriGround, "equip")
bluePetri = Item("bluePetri", "Petri Dish", "A petri dish containing blue blobs", bluePetriInv, Assets.bluePetriGround, "equip")
yellowPetri = Item("yellowPetri", "Petri Dish", "A petri dish containing yellow particles", yellowPetriInv, Assets.yellowPetriGround, "equip")

letterTile = Item("letterTile", "Tile", "A ceramic tile with a letter incribed on it", Assets.letterTile, Assets.letterTile, "equip")

electricalTape = Item("electricalTape", "Electric Tape", "A plastic tape used for repairing electrical devices and wires", Assets.tapeInv, Assets.tapeGround, "equip")
mop = Item("mop", "Mop", "A standard mop used to clean floors", Assets.mopInv, Assets.mopGround, "equip")

multimeter = Item("multimeter", "Multimeter", "An electrical instrument used to measure things such as voltage, current, and resistance", Assets.multiInv, Assets.multiInv, "equip")

brokenThermometer = Item("brokenThermometer", "Thermometer", "A damaged thermometer that no longer functions properly, leaking with mercury", Assets.brokenThermometerInv, Assets.brokenThermometerGround, "equip")

bleach = Item("bleachInv", "Bleach", "A solution of sodium hypochlorite in water commonly used in laundry and household cleaning", Assets.bleachInv, Assets.bleachGround, "equip")

hogweedLeaf = Item("hogweedLeaf", "Hogweed Leaf", "Leaf of a large, invasive plant with a toxic sap containing furanocoumarins", Assets.hogweedLeaf, Assets.hogweedPlant, "equip")

benzene = Item("benzene", "Benzene", "A colorless, flammable chemical", Assets.benzeneInv, Assets.benzeneDrawer, "equip")

lighter = Item("lighter", "Lighter", "A device that produces a small flame", Assets.lighterInv, Assets.lighterBed, "use")