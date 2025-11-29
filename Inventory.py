import pygame
import Assets
import Player
import Objects
import Items
import random

virtual_res = (900, 650)
#virtual_res = (1024, 720)
virtual_screen = pygame.Surface(virtual_res)
open = False
inventory = pygame.image.load("Assets/InventoryMenu.png")
emptySlot = pygame.image.load("Assets/emptyslot.png")
fullSlot = pygame.image.load("Assets/fullslot.png")
slotsBase = (407, 240)
slotsbuffer = 2

randomNames = ["Electric Tape", "Lighter", "STORAGE", "STATUS", "DESCRIPTION"]
frames = 5

index = 0
imagePositions = [
    (110,85),
    (307,85),
    (503,85),
    (699,85)
]

selected = -1
selectionRects = [
    pygame.Rect(72,80,175,144),
    pygame.Rect(269,80,175,144),
    pygame.Rect(465,80,175,144),
    pygame.Rect(661,80,175,144)
]

# finds what index in the player's inventory the selected item is referencing
def findIndex():
    return (selected + index) % Player.MaxInventorySize

leftArrowRect = pygame.Rect(17,103,37,84)
rightArrowRect = pygame.Rect(847,103,37,84)

useRect = pygame.Rect(760,550,95,53)
equipRect = pygame.Rect(685,550,170,53)

descRect = pygame.Rect(353,323,510,285)

running = True

def Inventory(screen, screen_res, events):
    global open, index, selected, running, frames
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    for event in events:
        if event.type == pygame.QUIT:
            running = False      
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                open = False
            if event.key == pygame.K_TAB or event.key == pygame.K_BACKSPACE:
                open = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_pos = (mouse_x/xScale, mouse_y/yScale)
                if leftArrowRect.collidepoint(mouse_pos):
                    if index == 0:
                        index = Player.MaxInventorySize - 4
                    else: 
                        index = index - 4
                if rightArrowRect.collidepoint(mouse_pos):
                    if index == Player.MaxInventorySize - 4:
                        index = 0
                    else:
                        index = index + 4
                if findIndex() < len(Player.inventory):
                    if equipRect.collidepoint(mouse_pos) and Player.inventory[findIndex()].buttonType == "equip":
                        Player.consumeItem(findIndex())
                    elif useRect.collidepoint(mouse_pos) and Player.inventory[findIndex()].buttonType == "use":
                        Player.consumeItem(findIndex())
                
                count = 0
                for slot in selectionRects:
                    if slot.collidepoint(mouse_pos):
                        if selected == count:
                            selected = -1
                        else:
                            selected = count
                    count += 1

    virtual_screen.blit(inventory, (0,0))
    valvePlaced = Objects.getValvePlaced()

    if valvePlaced: # if the final valve has been placed
        if frames == 5:
            frames = 0
            # randomize the names of the final items
            for i in range(len(randomNames)):
                chars = list(randomNames[i])
                for j in range(len(chars)):
                    if chars[j] != ' ' and random.randint(0,2) == 0: # skip space and only change each letter 1/3 times
                        chars[j] = chr(random.randint(1,128))
                        if chars[j] == ' ': # ensure the name does not become all spaces
                            chars[j] = '%'
                randomNames[i] = "".join(chars)
        frames += 1

    # draw titles
    font = pygame.font.Font("Assets/asusrog_regular.ttf", 36)
    text = font.render(randomNames[2], False, "black")
    textRect = text.get_rect()
    textRect.center = (450, 50)
    virtual_screen.blit(text, textRect)

    text = font.render(randomNames[3], False, "black")
    textRect = text.get_rect()
    textRect.center = (139, 300)
    virtual_screen.blit(text, textRect)

    text = font.render(randomNames[4], False, "black")
    textRect = text.get_rect()
    textRect.center = (497, 300)
    virtual_screen.blit(text, textRect)

    i = index
    for slot in imagePositions:
        if len(Player.inventory) > i:
            if not valvePlaced:
                virtual_screen.blit(Player.inventory[i].inventory_sprite, slot)
                font = pygame.font.Font("Assets/Minecraft.ttf", 24)
                text = font.render(Player.inventory[i].name, False, "white")
                textRect = text.get_rect()
                textRect.center = (slot[0]+50, slot[1]+105)
                virtual_screen.blit(text, textRect)
            else: # print random names if valve placed
                virtual_screen.blit(Player.inventory[i].inventory_sprite, slot)
                font = pygame.font.Font("Assets/Minecraft.ttf", 24)
                text = font.render(randomNames[i], False, "white")
                textRect = text.get_rect()
                textRect.center = (slot[0]+50, slot[1]+105)
                virtual_screen.blit(text, textRect)
            
        if i == Player.MaxInventorySize - 1:
            i = 0
        else:
            i += 1

    if selected != -1:
        pygame.draw.rect(virtual_screen, "white", selectionRects[selected], 5)
        if findIndex() < len(Player.inventory):
            font = pygame.font.Font("Assets/Minecraft.ttf", 24)
            Assets.draw_text(virtual_screen, Player.inventory[findIndex()].description, "white", descRect, font)

            if Player.inventory[findIndex()].buttonType == "equip":
                if Player.checkItem(Player.inventory[findIndex()]):
                    virtual_screen.blit(Assets.unequipButton, equipRect)
                else:
                    virtual_screen.blit(Assets.equipButton, equipRect)
            else:
                    virtual_screen.blit(Assets.useButton, useRect)

    for i in range(int(Player.MaxInventorySize / 4)):
        if index not in range (i * 4, (i + 1) * 4):
            virtual_screen.blit(emptySlot, (slotsBase[0] + (i * (slotsbuffer + emptySlot.get_width())), slotsBase[1]))
        else:
            virtual_screen.blit(fullSlot, (slotsBase[0] + (i * (slotsbuffer + emptySlot.get_width())), slotsBase[1]))

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return running