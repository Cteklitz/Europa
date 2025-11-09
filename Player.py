import pygame
import Items
import Assets
import Objects

health = 100
inventory = []
MaxInventorySize = 7
equipped = None

# adds an item to inventory
def addItem(item):
    if (len(inventory) < MaxInventorySize):
        inventory.append(item)
        return True
    else:
        return False

# checks if an item is in the inventory (can check based on item object or id); Probably try to use id mostly?
# def checkItem(_item):
#     if (type(_item) is Items.Item):
#         for item in inventory:
#             if _item.id == item.id:
#                 return True
#         return False # return false if item not found
#     elif (type(_item) is str):
#         for item in inventory:
#                 if _item == item.id:
#                     return True
#         return False # return false if item not found
#     else:
#         print("ERROR: Item type not valid")
#         return False
    
# checks if an item is in the inventory (can check based on item object or id); Probably try to use id mostly?
# Modified to check if item is equipped rather than in inventory
def checkItem(_item):
    if (type(_item) is Items.Item and type(equipped) is Items.Item):
        if _item.id == equipped.id:
            return True
        return False # return false if item not found
    else:
        print("ERROR: Item type not valid")
        return False

# removes an item from the inventory, takes either id or item object
# this is for removing items that dont have a global effect, like placing a quest item or dropping an item
# use consumeItem for consumable items that should do something
def removeItem(_item):
    global equipped
    if (type(_item) is Items.Item):
        for i in range(len(inventory)): # int itertor bc we need the index the item is found at to pop it
            if _item.id == inventory[i].id:
                inventory.pop(i)
                if _item.buttonType == "equip":
                    equipped = None
                return True
        return False # return false if item not found
    elif (type(_item) is str):
        for i in range(len(inventory)):
                if _item == inventory[i].id:
                    inventory.pop(i)
                    if _item.buttonType == "equip":
                        equipped = None
                    return True
        return False # return false if item not found
    else:
        print("ERROR: Item type not valid")
        return False
        
# Consumes the item at the input index in the player inventory. Will activate any global effects here
def consumeItem(index):
    global health, equipped
    if index in range(len(inventory)):
        item = inventory[index]

        if item.buttonType == "equip":
            if equipped == item:
                equipped = None
            else:
                equipped = item
            return True
        else:
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

class timer:
    def __init__(self, seconds, repeat):
        self.initial_time = -1
        self.seconds = seconds
        self.repeat = repeat

    def setInitial(self):
        if self.initial_time == -1:
            self.initial_time = pygame.time.get_ticks()

    def Done(self):
        if self.initial_time != -1:
            currentTime = (pygame.time.get_ticks() - self.initial_time) / 1000
            if currentTime < self.seconds:
                return False
            if self.repeat:
                self.initial_time = pygame.time.get_ticks()
            return True

animateTimer = timer(0.2, True)
animateTimer.setInitial()

up = False
left = True

down = True
right = False

# Isometric animations
left_down = Assets.load_tileset("Assets/left_down.png", 32, 32)
right_down = Assets.load_tileset("Assets/right_down.png", 32, 32)
left_up = Assets.load_tileset("Assets/left_up.png", 32, 32)
right_up = Assets.load_tileset("Assets/right_up.png", 32, 32)

# Top-Down Animations
upAnimation = Assets.load_tileset("Assets/topDown_Up.png", 32, 32)
downAnimation = Assets.load_tileset("Assets/topDown_Down.png", 32, 32)
leftAnimation = Assets.load_tileset("Assets/topDown_Left.png", 32, 32)
rightAnimation = Assets.load_tileset("Assets/topDown_Right.png", 32, 32)

playerIndex = 0
moving = False

# blits proper animation based on direction. xScale and yScale are absolute length and width of resulting image
def animatePlayer(surface, pos, xScale = 64, yScale = 64, perspective = "isometric"):
    global playerIndex, moving, animateTimer

    if not moving:
        playerIndex = 0
    elif animateTimer.Done():
        if playerIndex >= len(left_down) - 1:
            playerIndex = 0
        else:
            playerIndex = playerIndex + 1

    if perspective == "isometric":
        if up:
            if left:
                scaledImage = pygame.transform.scale(left_up[playerIndex], (xScale, yScale))
                surface.blit(scaledImage, (pos.x-(xScale/2), pos.y-yScale+16))
            else:
                scaledImage = pygame.transform.scale(right_up[playerIndex], (xScale, yScale))
                surface.blit(scaledImage, (pos.x-(xScale/2), pos.y-yScale+16))
        else:
            if left:
                scaledImage = pygame.transform.scale(left_down[playerIndex], (xScale, yScale))
                surface.blit(scaledImage, (pos.x-(xScale/2), pos.y-yScale+16))
            else:
                scaledImage = pygame.transform.scale(right_down[playerIndex], (xScale, yScale))
                surface.blit(scaledImage, (pos.x-(xScale/2), pos.y-yScale+16))
    else:
        if up:
            scaledImage = pygame.transform.scale(upAnimation[playerIndex], (32, 32))
            surface.blit(scaledImage, (pos.x-16, pos.y-16))
        elif down:
            scaledImage = pygame.transform.scale(downAnimation[playerIndex], (32, 32))
            surface.blit(scaledImage, (pos.x-16, pos.y-16))
        elif left:
            if not moving:
                scaledImage = pygame.transform.scale(downAnimation[playerIndex], (32, 32))
                surface.blit(scaledImage, (pos.x-16, pos.y-16))
            else:
                scaledImage = pygame.transform.scale(leftAnimation[playerIndex], (32, 32))
                surface.blit(scaledImage, (pos.x-16, pos.y-16))
        elif right:
            if not moving:
                scaledImage = pygame.transform.scale(downAnimation[playerIndex], (32, 32))
                surface.blit(scaledImage, (pos.x-16, pos.y-16))
            else:
                scaledImage = pygame.transform.scale(rightAnimation[playerIndex], (32, 32))
                surface.blit(scaledImage, (pos.x-16, pos.y-16))