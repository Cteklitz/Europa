import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import Player

virtual_res = (384,271)
virtual_screen = pygame.Surface(virtual_res)
virtual_res2 = (1106, 852)
virtual_screen2 = pygame.Surface(virtual_res2)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

exit = False
screen2 = False

tooDark = Objects.briefText(virtual_screen, Assets.tooDarkRead, -5, 200, 3)

def inBounds(x, y):
    global exit, tooDark, orangeYellow, safe
    if exit:
        exit = False
        tooDark.activated_time = -1
        return 0
    elif orangeYellow:
        orangeYellow = False
        return 1
    elif safe:
        safe = False
        return 2
    return False

bookcaseView = pygame.image.load("Assets/BookcaseView.png")
bookcaseView2 = pygame.image.load("Assets/BookcaseView2.png")
Book1 = pygame.image.load("Assets/ResearchVol1.png")
Content1 = pygame.image.load("Assets/ResearchVol1Content.png")
Book2 = pygame.image.load("Assets/ResearchVol2.png")
Content2 = pygame.image.load("Assets/ResearchVol2Content.png")
Book3 = pygame.image.load("Assets/MoregelliumLog.png")
Content3 = pygame.image.load("Assets/MoregelliumLogContent.png")
Book4 = pygame.image.load("Assets/THETRUTH.png")
Content4 = pygame.image.load("Assets/THETRUTHCONTENT.png")
Eye = pygame.image.load("Assets/EYE.png")
Iseeyou = pygame.image.load("Assets/ISEEYOU.png")
Onewayout = pygame.image.load("Assets/ONEWAYOUT.png")
Onewayout = pygame.transform.scale(Onewayout, (Onewayout.get_width() * 2.25, Onewayout.get_height() * 4))

scaled_eye = Eye
centerPos = (540, 416)

book1 = False
content1 = False
book2 = False
content2 = False
book3 = False
content3 = False
book4 = False
content4 = False
cutscene = False
orangeYellow = False
safe = False

timer1 = Objects.timer(10, False)
timer2 = Objects.timer(5, False)
timer3 = Objects.timer(0.05, True)
timer4 = Objects.timer(4, False)
timer5 = Objects.timer(6, False)
timer6 = Objects.timer(0, False)
timer7 = Objects.timer(0.01, True)
timer8 = Objects.timer(1, False)

def positionDeterminer(cameFrom):
    pass

def Room(screen, screen_res, events):
    global exit, screen2, bookcaseView, Book1, Content1, book1, content1, Book2, Content2, book2, content2, Book3, Content3, book3, content3, Book4, Content4, book4, content4, cutscene, centerPos, scaled_eye, orangeYellow, orangeYellowRect, safe

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
    THETRUTHRect = Polygon([(87,87), (100,87), (100,123), (87,123)])
    bigBookRect = Polygon([(257,3), (835,3), (835,855), (257,855)])
    orangeYellowRect = pygame.Rect(207,162,52,29)
    safeRect = pygame.Rect(136,222,89,36)

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if not content4:
                    if screen2:
                        if content1 or content2 or content3:
                            Sounds.book.play()
                        if content3:
                            Sounds.powerAmb.play(-1)
                        content1 = False
                        content2 = False
                        content3 = False
                        book1 = False
                        book2 = False
                        if book3:
                            Sounds.heartbeat.stop()
                            book3 = False
                        if book4:
                            pygame.mixer.music.stop()
                            Sounds.powerAmb.play(-1)
                            book4 = False
                        screen2 = False
                    else:
                        exit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                tooDark.activated_time = pygame.time.get_ticks()
                if lit or Objects.getPinkPower():
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    scaled_mouse_x = mouse_x / xScale
                    scaled_mouse_y = mouse_y / yScale
                    scaled_mouse_x2 = mouse_x / xScale2
                    scaled_mouse_y2 = mouse_y / yScale2
                    if not content1 and not content2 and not content3 and not content4:
                        if not book1 and not book2 and not book3 and not book4:
                            if orangeYellowRect.collidepoint((scaled_mouse_x,scaled_mouse_y)):
                                orangeYellow = True
                            if safeRect.collidepoint((scaled_mouse_x,scaled_mouse_y)):
                                safe = True
                            if researchVol1Rect.contains(Point(scaled_mouse_x, scaled_mouse_y)):
                                Sounds.book.play()
                                screen2 = True
                                book1 = True
                            elif researchVol2Rect.contains(Point(scaled_mouse_x, scaled_mouse_y)):
                                Sounds.book.play()
                                screen2 = True
                                book2 = True
                            elif moregelliumLogRect.contains(Point(scaled_mouse_x, scaled_mouse_y)):
                                Sounds.book.play()
                                screen2 = True
                                book3 = True
                            elif THETRUTHRect.contains(Point(scaled_mouse_x, scaled_mouse_y)) and not cutscene:
                                Sounds.powerAmb.stop()
                                pygame.mixer.music.load("Audio/dark ambience.wav")
                                pygame.mixer.music.play(-1)
                                screen2 = True
                                book4 = True
                        elif bigBookRect.contains(Point(scaled_mouse_x2, scaled_mouse_y2)):
                            if book1:
                                Sounds.page.play()
                                content1 = True
                            if book2:
                                Sounds.page.play()
                                content2 = True
                            if book3:
                                Sounds.powerAmb.stop()
                                Sounds.heartbeat.play(-1)
                                Sounds.page.play()
                                content3 = True
                            if book4:
                                pygame.mixer.music.stop()
                                Sounds.page.play()
                                content4 = True
                                Player.cutscene = True

    virtual_screen.fill("gray")
    virtual_screen2.fill("black")
    dark_overlay.fill((0, 0, 0, 150))

    # if lit or Objects.getPinkPower():
    #     Assets.punch_light_hole(virtual_screen, dark_overlay, (virtual_screen.get_width()/2, virtual_screen.get_height()/2), 500, (100, 0, 100))

    if not cutscene:
        virtual_screen.blit(bookcaseView, (0, 0))
    else:
        virtual_screen.blit(bookcaseView2, (0, 0))

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
    if book4:
        virtual_screen2.fill((136,0,21))
        virtual_screen2.blit(Book4, (0, 0))
    if content4:
        timer1.setInitial()
        virtual_screen2.blit(Content4, (0, 0))
        scaled_width = int(scaled_eye.get_width())
        scaled_height = int(scaled_eye.get_height())
        if timer1.Done():
            virtual_screen2.blit(Iseeyou, (350, 150))
            timer2.setInitial()
            if timer2.Done():
                timer3.setInitial()
                timer4.setInitial()
                if not timer4.Done():
                    if(timer3.Done()):
                        scaled_width = int(scaled_eye.get_width() / 1.05)
                        scaled_height = int(scaled_eye.get_height() / 1.05)
                        scaled_eye = pygame.transform.scale(Eye, (scaled_width, scaled_height))
                else:
                    timer5.setInitial()
                    if timer5.Done():
                        timer6.setInitial()
                        Sounds.brainwash.play()
                        if timer6.Done():
                            timer7.setInitial()
                            timer8.setInitial()
                            if not timer8.Done():
                                if timer7.Done():
                                    scaled_width = int(scaled_eye.get_width() / 0.5)
                                    scaled_height = int(scaled_eye.get_height() / 0.5)
                                    scaled_eye = pygame.transform.scale(Eye, (scaled_width, scaled_height))
                            else:
                                Sounds.brainwash.stop()
                                level, power = Objects.getPipeDungeonInfo()
                                _, lowerWingPower = Objects.getPinkWingInfo()
                                if (level == 1 and power and lowerWingPower) or Objects.getPinkPower():
                                    Sounds.ominousAmb.stop()
                                    Sounds.powerAmb.play(-1)
                                else:
                                    Sounds.ominousAmb.play(-1)
                                    Sounds.powerAmb.stop()
                                screen2 = False
                                content4 = False
                                book4 = False
                                cutscene = True
                                Player.cutscene = False
        virtual_screen2.blit(scaled_eye, (centerPos[0] - scaled_width // 2, centerPos[1] - scaled_height // 2))
        if timer6.Done():
            virtual_screen2.blit(Onewayout, (0,0))

    if not (lit or Objects.getPinkPower()):
        virtual_screen.blit(dark_overlay, (0, 0))

    if not lit and not Objects.getPinkPower():
        tooDark.update()

    if not screen2:
        scaled = pygame.transform.scale(virtual_screen, screen_res)
        screen.blit(scaled, (0, 0))
    else:
        scaled = pygame.transform.scale(virtual_screen2, screen_res)
        screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale