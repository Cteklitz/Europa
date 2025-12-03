import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Player
import Items
import Sounds

virtual_res = (250, 150)
virtual_screen = pygame.Surface(virtual_res)
virtual_res2 = (1106, 852)
virtual_screen2 = pygame.Surface(virtual_res2)

player_pos = pygame.Vector2(192, 128)

deskViewBg = pygame.image.load("Assets/BedroomDeskView.png")
deskViewBg2 = pygame.image.load("Assets/Bedroom3DeskView.png")

brokenThermometerImg = Assets.brokenThermometerInv

bookImg = pygame.image.load("Assets/Almanac.png")
content1Img = pygame.image.load("Assets/AlmanacContent1.png")
content2Img = pygame.image.load("Assets/AlmanacContent2.png")

# Item positions and interaction rects
thermometer_pos = (120, 25)  
thermometerRect = pygame.Rect(thermometer_pos[0], thermometer_pos[1], 25, 40)
thermometerCollected = False

bookRect = pygame.Rect(118, 19, 34, 46)
bigBookRect = Polygon([(257,3), (835,3), (835,855), (257,855)])
book = False
content1 = False
content2 = False

exit = False

def inBounds(x, y):
    global exit, book, content1, content2
    if exit:
        book = False
        content1 = False
        content2 = False
        exit = False
        return 0  
    return False

def positionDeterminer(cameFrom):
    pass

def Room(screen, screen_res, events):
    global exit, thermometerCollected, book, content1, content2
    
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    xScale2 = screen.get_width()/virtual_screen2.get_width() 
    yScale2 = screen.get_height()/virtual_screen2.get_height()

    bedroomNumber = Objects.getBedroomNumber()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                if book and not (content1 or content2):
                    Sounds.book.play()
                    book = False
                elif content1 and bedroomNumber == 3:
                    Sounds.page.play()
                    content1 = False
                    content2 = True
                elif content2 and bedroomNumber == 3:
                    Sounds.book.play()
                    book = False
                    content2 = False
                else:
                    exit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_pos = (mouse_x/xScale, mouse_y/yScale)
                mouse_pos2 = (mouse_x/xScale2, mouse_y/yScale2)
                
                # Player clicks broken thermometer
                if thermometerRect.collidepoint(mouse_pos) and not thermometerCollected and bedroomNumber == 1:     
                    if Player.addItem(Items.brokenThermometer):
                        thermometerCollected = True
                        # Force pickup sound to play immediately on a specific channel so radio doesnt interfer with sound
                        pickup_channel = pygame.mixer.Channel(7)  
                        pickup_channel.play(Sounds.pickup)
                if bedroomNumber == 3:
                    if bookRect.collidepoint(mouse_pos) and not book:
                        Sounds.book.play()
                        book = True
                    elif book and not (content1 or content2):
                        if bigBookRect.contains(Point(mouse_pos2)):
                            Sounds.page.play()
                            content1 = True
                    elif content1:
                        Sounds.page.play()
                        content1 = False
                        content2 = True
                    elif content2:
                        Sounds.book.play()
                        book = False
                        content2 = False

    # Display floor color background 
    virtual_screen.fill("gray")
    
    if bedroomNumber == 1:
        if deskViewBg:
            virtual_screen.blit(deskViewBg, (0, 0))
        
        # Draw gray rectangle over thermometer area when collected
        if thermometerCollected:
            pygame.draw.rect(virtual_screen, (127, 127, 127), (114, 19, 152-114, 62-19))
        
        Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)
    else:
        if not book:
            if deskViewBg2:
                virtual_screen.blit(deskViewBg2, (0, 0))
                Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)
        else:
            virtual_screen2.fill("black")
            if book and not (content1 or content2):
                virtual_screen2.blit(bookImg, (0,0))
            if content1:
                virtual_screen2.blit(content1Img, (0,0))
            if content2:
                virtual_screen2.blit(content2Img, (0,0))
            Assets.scaled_draw(virtual_res2, virtual_screen2, screen_res, screen)
    
    return player_pos, 1, 1