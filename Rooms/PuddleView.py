import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon

virtual_res = (800, 600)  
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)


puddle1_original = pygame.image.load("Assets/Puddle1.png")
puddle2_original = pygame.image.load("Assets/Puddle2.png")
puddle3_original = pygame.image.load("Assets/Puddle3.png")

# Load mop for cursor
mop_cursor = pygame.image.load("Assets/Mop.png")

# puddle scaling
scale_factor = 6
puddle1 = pygame.transform.scale(puddle1_original, (puddle1_original.get_width() * scale_factor, puddle1_original.get_height() * scale_factor))
puddle2 = pygame.transform.scale(puddle2_original, (puddle2_original.get_width() * scale_factor, puddle2_original.get_height() * scale_factor))
puddle3 = pygame.transform.scale(puddle3_original, (puddle3_original.get_width() * scale_factor, puddle3_original.get_height() * scale_factor))

puddle1_pos = (330, 20)
puddle2_pos = (255, 205)
puddle3_pos = (390, 265)

# puddle masks 
puddle_mask = pygame.Surface(virtual_res, pygame.SRCALPHA)
puddle_mask.fill((0, 0, 0, 0))


puddle_mask.blit(puddle1, puddle1_pos)
puddle_mask.blit(puddle2, puddle2_pos)
puddle_mask.blit(puddle3, puddle3_pos)

# cleanup mask to track whats been mopped
cleanup_mask = pygame.Surface(virtual_res, pygame.SRCALPHA)
cleanup_mask.fill((0, 0, 0, 0))

mouse_pos = (0, 0)
is_mopping = False
mop_radius = 30

exit = False

def inBounds(x, y):
    global exit
    if exit:
        exit = False
        return 0
    return False

def positionDeterminer(cameFrom):
    pass

def PuddleView(screen, screen_res, events):
    global exit, mouse_pos, is_mopping, cleanup_mask
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    real_mouse_pos = pygame.mouse.get_pos()
    mouse_pos = (real_mouse_pos[0] / xScale, real_mouse_pos[1] / yScale)
    
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                exit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                is_mopping = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                is_mopping = False
    
    if is_mopping:
        pygame.draw.circle(cleanup_mask, (195, 195, 195, 255), 
                          (int(mouse_pos[0]), int(mouse_pos[1])), mop_radius)

    virtual_screen.fill((195, 195, 195))
    
    virtual_screen.blit(puddle_mask, (0, 0))
    
    virtual_screen.blit(cleanup_mask, (0, 0))
    
    mop_rect = mop_cursor.get_rect()
    # mop mosition
    mop_rect.centerx = int(mouse_pos[0]) - 15
    mop_rect.bottom = int(mouse_pos[1]) + 30
    virtual_screen.blit(mop_cursor, mop_rect)

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale

def Room(screen, screen_res, events):
    return PuddleView(screen, screen_res, events)