import pygame
import Items

inventory = []

# adds an item to iventory
def addItem(item):
    if (len(inventory) < 7):
        inventory.append(item)
        return True
    else:
        return False
    
# checks if an item is in the inventory (can check based on item object or id); Probably try to use id mostly?
def checkItem(_item):
    if (type(_item) is Items.Item):
        for item in inventory:
            if _item.id == item.id:
                return True
        return False # return false if item not found
    elif (type(_item) is str):
        for item in inventory:
                if _item == item.id:
                    return True
        return False # return false if item not found
    else:
        print("ERROR: Item type not valid")
        return False