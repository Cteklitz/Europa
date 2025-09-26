import pygame
import Player

virtual_res = (900, 650)
virtual_screen = pygame.Surface(virtual_res)
open = False
inventory = pygame.image.load("Assets/InventoryMenu.png")

index = 0
slotPositions = [
    (107,85),
    (307,85),
    (507,85),
    (707,85)
]

leftArrowRect = pygame.Rect(17,103,54,188)
rightArrowRect = pygame.Rect(847,103,54,188)

def Inventory(screen, screen_res, events):
    global open, index
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

    virtual_screen.blit(inventory, (0,0))

    i = index
    for slot in slotPositions:
        if len(Player.inventory) > i:
            virtual_screen.blit(Player.inventory[i].inventory_sprite, slot)
        if i == Player.MaxInventorySize - 1:
            i = 0
        else:
            i += 1

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))