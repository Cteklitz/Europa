import pygame
import Items

inventory = []

def addItem(item):
    if (len(inventory) < 7):
        inventory.append(item)
        return True
    else:
        return False