import pygame
import Items

health = 100
inventory = []
MaxInventorySize = 7

# adds an item to inventory
def addItem(item):
    if (len(inventory) < MaxInventorySize):
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

# removes an item from the inventory, takes either id or item object
# this is for removing items that dont have a global effect, like placing a quest item or dropping an item
# use consumeItem for consumable items that should do something
def removeItem(_item):
    if (type(_item) is Items.Item):
        for i in range(len(inventory)): # int itertor bc we need the index the item is found at to pop it
            if _item.id == inventory[i].id:
                inventory.pop(i)
                return True
        return False # return false if item not found
    elif (type(_item) is str):
        for i in range(len(inventory)):
                if _item == inventory[i].id:
                    inventory.pop(i)
                    return True
        return False # return false if item not found
    else:
        print("ERROR: Item type not valid")
        return False
        
# Consumes the item at the input index in the player inventory. Will activate any global effects here
def consumeItem(index):
    global health
    if index in range(len(inventory)):
        item = inventory[index]

        match item:
            case Items.bandage:
                health += 15
                if health >= 100:
                    health = 100
                inventory.pop(index)
                return True
            case _:
                print(item.name + " cannot be consumed")
                return False
    else:
        print(str(index) + " is not a valid inventory value")
        return False