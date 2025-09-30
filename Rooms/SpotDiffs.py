import pygame
import Assets
import Objects
import Sounds
from Rooms import Lockbox_puzzle 

virtual_res = (389,189)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

# Load all background variations
background = pygame.image.load("Assets/spotDiffs.png")
background2 = pygame.image.load("Assets/spotDiffs2.png")
background3 = pygame.image.load("Assets/spotDiffs3.png")

# Define the clickable chest region around the chest in the center
chest_rect = pygame.Rect(166, 110, 60, 35)

chestOpen = False
exit = False

def inBounds(x, y):
    global exit
    if exit:
        exit = False
        return 0  # Always return 0 when exiting, to go back to previous room

def positionDeterminer(cameFrom):
    pass

def Room(screen, screen_res, events):
    global exit, chestOpen
    # Make sure cursor is visible since we need to click
    pygame.mouse.set_visible(True)
    
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()
    
    # Check if lockbox has been opened
    if Lockbox_puzzle.unlocked:
        chestOpen = True  # Show the open chest
    
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                exit = True
                return player_pos, xScale, yScale, 0  # Return immediately with no transition
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Get mouse position and scale it to virtual resolution
                mouse_x, mouse_y = pygame.mouse.get_pos()
                scaled_x = mouse_x / xScale
                scaled_y = mouse_y / yScale
                
                # Check if click is in chest region
                if chest_rect.collidepoint(scaled_x, scaled_y) and not Lockbox_puzzle.unlocked:
                    Sounds.draweropen.play()
                    chestOpen = True
                    return player_pos, xScale, yScale, 1  # Return transition to lockbox puzzle 

    virtual_screen.fill((0, 0, 0))  # Black background
    
    # Show the appropriate background based on chest state
    if not chestOpen:
        virtual_screen.blit(background, (0,0))
    else:
        if not Objects.getPinkPower():
            virtual_screen.blit(background2, (0,0))
        else:
            virtual_screen.blit(background3, (0,0))
    
    # Scale and display
    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))


    if chestOpen and not Lockbox_puzzle.unlocked:
        return player_pos, xScale, yScale, 1
    return player_pos, xScale, yScale, 0