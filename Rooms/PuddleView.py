import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Player
import Items
import Sounds

virtual_res = (800, 600)  
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

# Load mop for cursor
mop_cursor = pygame.image.load("Assets/Mop.png")

# puddle scaling
scale_factor = 8
puddle1 = pygame.transform.scale(Assets.puddle1, (Assets.puddle1.get_width() * scale_factor, Assets.puddle1.get_height() * scale_factor))
puddle2 = pygame.transform.scale(Assets.puddle2, (Assets.puddle2.get_width() * scale_factor, Assets.puddle2.get_height() * scale_factor))
puddle3 = pygame.transform.scale(Assets.puddle3, (Assets.puddle3.get_width() * scale_factor, Assets.puddle3.get_height() * scale_factor))

# pipe scaling
brokenWire = pygame.image.load("Assets/BrokenWire.png")
fixedWire = pygame.image.load("Assets/FixedWire.png")

horizontalPipe = pygame.transform.scale(Assets.pipes[10], (Assets.pipes[10].get_width() * scale_factor, Assets.pipes[10].get_height() * scale_factor))
brokenPipe = pygame.transform.scale(brokenWire, (brokenWire.get_width() * scale_factor, brokenWire.get_height() * scale_factor))
repairRect = pygame.Rect(350 + 136, virtual_screen.get_height()/2 - 128 - 256 + 40 + 192, 96, 88)
fixedPipe = pygame.transform.scale(fixedWire, (fixedWire.get_width() * scale_factor, fixedWire.get_height() * scale_factor))
elbow1 = pygame.transform.scale(Assets.pipes[5], (Assets.pipes[5].get_width() * scale_factor, Assets.pipes[5].get_height() * scale_factor))
elbow2 = pygame.transform.scale(Assets.pipes[18], (Assets.pipes[18].get_width() * scale_factor, Assets.pipes[18].get_height() * scale_factor))

# puddle positions
puddle1_pos = (330, 10)
puddle2_pos = (230, 235)
puddle3_pos = (390, 300)

# puddle masks 
puddle_mask = pygame.Surface(virtual_res, pygame.SRCALPHA)
puddle_mask.fill((0, 0, 0, 0))

puddle_mask.blit(puddle1, puddle1_pos)
puddle_mask.blit(puddle2, puddle2_pos)
puddle_mask.blit(puddle3, puddle3_pos)

mouse_pos = (0, 0)
is_mopping = False
mop_radius = 30

exit = False

puddlesCleaned = False
cleanup_check_timer = 0

# Eye effect variables
eye_image_original = pygame.image.load("Assets/eye_water.png")

eye_size = (eye_image_original.get_width() // 3, eye_image_original.get_height() // 3)
eye_image = pygame.transform.scale(eye_image_original, eye_size)
eye_alpha = 0
eye_fade_direction = 1
eye_timer = 0
eye_position = (360, 80)
eye_cycle_complete = False
eye_max_alpha = 204  # 80% of 255 (80% visibility)
cleanup_percent = 0.0

playedBell = False

def calculate_cleanup_percentage():
    step = 10
    puddle_pixels = 0
    cleaned_pixels = 0
    
    for x in range(0, virtual_res[0], step):
        for y in range(0, virtual_res[1], step):
            puddle_alpha = puddle_mask.get_at((x, y))[3]
            
            if puddle_alpha == 0:
                cleaned_pixels += 1
                
            puddle_pixels += 1
    
    if puddle_pixels == 0:
        return 0
    
    return (cleaned_pixels / puddle_pixels) * 100

def inBounds(x, y):
    global exit
    if exit:
        exit = False
        return 0
    return False

def positionDeterminer(cameFrom):
    pass

def PuddleView(screen, screen_res, events):
    global eye_alpha, eye_fade_direction, eye_timer, eye_cycle_complete, eye_max_alpha, cleanup_percent, playedBell
    global exit, mouse_pos, is_mopping, puddlesCleaned
    
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    real_mouse_pos = pygame.mouse.get_pos()
    mouse_pos = (real_mouse_pos[0] / xScale, real_mouse_pos[1] / yScale)
    
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                exit = True
                # Stop mop sound if playing when exiting
                Sounds.mopSound.stop()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if Player.checkItem(Items.mop):
                    is_mopping = True
                    # Start playing mop sound on loop
                    Sounds.mopSound.play(-1)
                if repairRect.collidepoint(mouse_pos) and Player.checkItem(Items.electricalTape) and puddlesCleaned:
                    Objects.RepairWire()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                is_mopping = False
                Sounds.mopSound.stop()
    
    if is_mopping and Player.checkItem(Items.mop):
        pygame.draw.circle(puddle_mask, (0, 0, 0, 0), (int(mouse_pos[0]), int(mouse_pos[1])), mop_radius)

        global cleanup_check_timer
        cleanup_check_timer += 1
        if cleanup_check_timer >= 30 and not puddlesCleaned:
            cleanup_percent = calculate_cleanup_percentage()
            if cleanup_percent >= 95.0:
                puddlesCleaned = True
            cleanup_check_timer = 0

    virtual_screen.fill((195, 195, 195))

    for x in range(0,800,256):
        virtual_screen.blit(horizontalPipe, (x, virtual_screen.get_height()/2 - 128))

    if not Objects.getWireRepaired():
        virtual_screen.blit(brokenPipe, (350, virtual_screen.get_height()/2 - 128 - 256 + 40))
    else:
        virtual_screen.blit(fixedPipe, (350, virtual_screen.get_height()/2 - 128 - 256 + 40))

    virtual_screen.blit(elbow1, (414, -90))

    virtual_screen.blit(horizontalPipe, (174, -90))

    virtual_screen.blit(elbow2, (-82, -90))
    
    virtual_screen.blit(puddle_mask, (0, 0))
    
    # EYE EFFECT
    if not eye_cycle_complete:
        eye_timer += 1
        
        # Fade in and out slowly
        if eye_timer % 2 == 0:  
            eye_alpha += eye_fade_direction * 2
            
            # Eye alpha boundaries
            
            if eye_alpha >= eye_max_alpha:
                eye_alpha = eye_max_alpha
                eye_fade_direction = -1  
            elif eye_alpha <= 0 and eye_fade_direction == -1:
                eye_alpha = 0
                eye_cycle_complete = True  
    
    if eye_alpha > 0 and cleanup_percent > 1.0 and not playedBell:
        Sounds.scaryBell.play()
        playedBell = True

    if eye_alpha > 0 and cleanup_percent < 1.0:
        eye_surface = eye_image.copy()
        eye_surface.set_alpha(eye_alpha)
        virtual_screen.blit(eye_surface, eye_position)
    
    mop_rect = mop_cursor.get_rect()
    # mop mosition
    mop_rect.centerx = int(mouse_pos[0]) - 15
    mop_rect.bottom = int(mouse_pos[1]) + 30
    if Player.checkItem(Items.mop):
        virtual_screen.blit(mop_cursor, mop_rect)

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale

def getPuddlesCleaned():
    """Get the puddle cleaning state"""
    return puddlesCleaned

def Room(screen, screen_res, events):
    return PuddleView(screen, screen_res, events)