import pygame
import Assets
import Player

virtual_res = (900, 650)
virtual_screen = pygame.Surface(virtual_res)
open = False
inventory = pygame.image.load("Assets/InventoryMenu.png")

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

def findIndex():
    return (selected + index) % Player.MaxInventorySize

leftArrowRect = pygame.Rect(17,103,54,188)
rightArrowRect = pygame.Rect(847,103,54,188)

useRect = pygame.Rect(760,550,95,53)

descRect = pygame.Rect(353,323,510,285)

def Inventory(screen, screen_res, events):
    global open, index, selected
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                open = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_pos = (mouse_x/xScale, mouse_y/yScale)
                if leftArrowRect.collidepoint(mouse_pos):
                    if index == 0:
                        index = Player.MaxInventorySize - 1
                    else: 
                        index = index - 1
                if rightArrowRect.collidepoint(mouse_pos):
                    if index == Player.MaxInventorySize - 1:
                        index = 0
                    else:
                        index = index + 1
                if useRect.collidepoint(mouse_pos) and selected != -1:
                    Player.consumeItem(selected)
                
                count = 0
                for slot in selectionRects:
                    if slot.collidepoint(mouse_pos):
                        if selected == count:
                            selected = -1
                        else:
                            selected = count
                    count += 1

    virtual_screen.blit(inventory, (0,0))

    i = index
    for slot in imagePositions:
        if len(Player.inventory) > i:
            virtual_screen.blit(Player.inventory[i].inventory_sprite, slot)
            font = pygame.font.SysFont("Cascadia Code", 24)
            text = font.render(Player.inventory[i].name, True, "white")
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
            font = pygame.font.SysFont("Cascadia Code", 34)
            Assets.draw_text(virtual_screen, Player.inventory[findIndex()].description, "white", descRect, font)

        virtual_screen.blit(Assets.useButton, useRect)

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))