import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Player
import Items
import Sounds

virtual_res = (250, 150)
virtual_screen = pygame.Surface(virtual_res)
player_pos = pygame.Vector2(192, 128)

deskViewBg = pygame.image.load("Assets/BedroomDeskView.png")

brokenThermometerImg = Assets.brokenThermometerInv

# Item positions and interaction rects
thermometer_pos = (120, 25)  
thermometerRect = pygame.Rect(thermometer_pos[0], thermometer_pos[1], 25, 40)

thermometerCollected = False
exit = False

def inBounds(x, y):
    global exit
    if exit:
        exit = False
        return 0  
    return False

def positionDeterminer(cameFrom):
    pass

def Room(screen, screen_res, events):
    global exit, thermometerCollected
    
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_pos = (mouse_x/xScale, mouse_y/yScale)
                
                # Player clicks broken thermometer
                if thermometerRect.collidepoint(mouse_pos) and not thermometerCollected:     
                    if Player.addItem(Items.brokenThermometer):
                        thermometerCollected = True
                        # Force pickup sound to play immediately on a specific channel so radio doesnt interfer with sound
                        pickup_channel = pygame.mixer.Channel(7)  
                        pickup_channel.play(Sounds.pickup)

    # Display floor color background 
    virtual_screen.fill("gray")
    
    if deskViewBg:
        virtual_screen.blit(deskViewBg, (0, 0))
    
    # Draw gray rectangle over thermometer area when collected
    if thermometerCollected:
        pygame.draw.rect(virtual_screen, (127, 127, 127), (114, 19, 152-114, 62-19))
    
    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)
    
    return player_pos, 1, 1