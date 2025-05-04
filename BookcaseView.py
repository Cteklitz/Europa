import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon

virtual_res = (384,271)
virtual_screen = pygame.Surface(virtual_res)
virtual_res2 = (1106, 852)
virtual_screen2 = pygame.Surface(virtual_res2)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

exit = False
screen2 = False

tooDark = Objects.briefText(virtual_screen, Assets.tooDark, -5, 200)

def inBounds(x, y):
    global exit, tooDark
    if exit:
        exit = False
        tooDark.activated_time = -1
        return 0
    return True

bookcaseView = pygame.image.load("Assets/BookcaseView.png")
Book1 = pygame.image.load("Assets/ResearchVol1.png")
Content1 = pygame.image.load("Assets/ResearchVol1Content.png")
Book2 = pygame.image.load("Assets/ResearchVol2.png")
Content2 = pygame.image.load("Assets/ResearchVol2Content.png")
Book3 = pygame.image.load("Assets/MoregelliumLog.png")
Content3 = pygame.image.load("Assets/MoregelliumLogContent.png")

book1 = False
content1 = False
book2 = False
content2 = False
book3 = False
content3 = False

def Room(screen, screen_res, events):
    global exit, screen2, bookcaseView, Book1, Content1, book1, content1, Book2, Content2, book2, content2, Book3, Content3, book3, content3

    level, power = Objects.getPipeDungeonInfo()
    _, lowerWingPower = Objects.getPinkWingInfo()
    lit = lowerWingPower and level == 1 and power

    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    xScale2 = screen.get_width()/virtual_screen2.get_width() 
    yScale2 = screen.get_height()/virtual_screen2.get_height()

    researchVol1Rect = Polygon([(80,14), (94,14), (94,55), (80,55)])
    researchVol2Rect = Polygon([(95,21), (105,13), (130,49), (119,55)])
    moregelliumLogRect = Polygon([(260,14), (275,14), (275,55), (260,55)])
    bigBookRect = Polygon([(257,3), (835,3), (835,855), (257,855)])

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if content1:
                    content1 = False
                elif content2:
                    content2 = False
                elif content3:
                    content3 = False
                elif screen2:
                    book1 = False
                    book2 = False
                    book3 = False
                    screen2 = False
                else:
                    exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                tooDark.activated_time = pygame.time.get_ticks()
                if lit:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    scaled_mouse_x = mouse_x / xScale
                    scaled_mouse_y = mouse_y / yScale
                    scaled_mouse_x2 = mouse_x / xScale2
                    scaled_mouse_y2 = mouse_y / yScale2
                    if researchVol1Rect.contains(Point(scaled_mouse_x, scaled_mouse_y)):
                        screen2 = True
                        book1 = True
                    elif researchVol2Rect.contains(Point(scaled_mouse_x, scaled_mouse_y)):
                        screen2 = True
                        book2 = True
                    elif moregelliumLogRect.contains(Point(scaled_mouse_x, scaled_mouse_y)):
                        screen2 = True
                        book3 = True
                    elif bigBookRect.contains(Point(scaled_mouse_x2, scaled_mouse_y2)):
                            if book1:
                                content1 = True
                            if book2:
                                content2 = True
                            if book3:
                                content3 = True

    virtual_screen.fill("gray")
    virtual_screen2.fill("black")
    dark_overlay.fill((0, 0, 0, 150))

    if lit:
        Assets.punch_light_hole(virtual_screen, dark_overlay, (virtual_screen.get_width()/2, virtual_screen.get_height()/2), 500, (100, 0, 100))

    virtual_screen.blit(bookcaseView, (0, 0))
    if book1:
        virtual_screen2.blit(Book1, (0, 0))
    if content1:
        virtual_screen2.blit(Content1, (0, 0))
    if book2:
        virtual_screen2.blit(Book2, (0, 0))
    if content2:
        virtual_screen2.blit(Content2, (0, 0))
    if book3:
        virtual_screen2.blit(Book3, (0, 0))
    if content3:
        virtual_screen2.blit(Content3, (0, 0))

    virtual_screen.blit(dark_overlay, (0, 0))

    if not lit:
        tooDark.update()

    if not screen2:
        scaled = pygame.transform.scale(virtual_screen, screen_res)
        screen.blit(scaled, (0, 0))
    else:
        scaled = pygame.transform.scale(virtual_screen2, screen_res)
        screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale