import pygame
virtual_res = (250, 150)
virtual_screen = pygame.Surface(virtual_res)
player_pos = pygame.Vector2(192, 128)

closed_toolbox = pygame.image.load('Assets/ToolboxZoomClosed.png')
open_toolbox = pygame.image.load('Assets/ToolboxZoomOpen.png')

open = False # changes to true when user opens toolbox
exit = False

toolbox_rect = closed_toolbox.get_rect()
toolbox_rect.center = (125, 75)

toolbox_rect.center = (125, 75)

def positionDeterminer(cameFrom):
    pass

def inBounds(x, y):
    global exit, open
    if exit:
        exit = False
        return 0
    return False

def Room(screen, screen_res, events):
    global exit, open
    virtual_screen.fill((0, 0, 0)) # fill screen with black, replace with bg later
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_x, click_y = event.pos
            # Changes toolbox to open or closed if clicked on
            if(285 < click_x < 1310 and 350 < click_y < 855):
                if(open):
                    open = False
                else:
                    open = True
    if (not open):
        virtual_screen.blit(closed_toolbox, toolbox_rect)
    else:
        virtual_screen.blit(open_toolbox, toolbox_rect)
    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))
    return player_pos, xScale, yScale