import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import Player
import Items

virtual_res = (389,189)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

background = pygame.image.load("Assets/spotDiffs.png")
background2 = pygame.image.load("Assets/spotDiffs2.png")
background3 = pygame.image.load("Assets/spotDiffs3.png")

found = 0
collected = False
exit = False
goodEye = False
played = False
lockboxExit = False

mat = False
stem = False
corner = False
water = False
light = False
backgroundDiff = False

eyeOpenSmall = pygame.transform.scale(pygame.image.load("Assets/EyeWall.png"), (30, 22))
eyeClosedSmall = pygame.transform.scale(pygame.image.load("Assets/eyeClosedWall.png"), (30, 22))
eyes = [eyeOpenSmall, eyeClosedSmall]

smallEyesPositions = [
    (105, 30),
    (135, 30),
    (165, 30),
    (195, 30),
    (225, 30),
    (255, 30)
]

goodEYE = pygame.image.load("Assets/goodEYE.png")
goodEYEtext = Objects.briefText(virtual_screen, goodEYE, 111, 117, 2)

matRect = pygame.Rect(263,154,44,17)
stemRect = pygame.Rect(283,6,14,15)
cornerRect = pygame.Rect(309,83,12,12)
waterRect = pygame.Rect(202,87,23,11)
lightRect = pygame.Rect(353,16,23,20)
backgroundRect = pygame.Rect(194,0,195,81)

matRect2 = pygame.Rect(74,154,44,17)
stemRect2 = pygame.Rect(94,6,14,15)
cornerRect2 = pygame.Rect(121,83,12,12)
waterRect2 = pygame.Rect(11,87,23,11)
lightRect2 = pygame.Rect(164,16,23,20)
backgroundRect2 = pygame.Rect(0,0,197,81)

chairRect1 = pygame.Rect(14,21,76,57)
chairRect2 = pygame.Rect(110,21,76,57)
chairRect3 = pygame.Rect(205,21,76,57)
chairRect4 = pygame.Rect(298,21,76,57)

# letterRect = pygame.Rect(168,119,42,28)
letterRect = pygame.Rect(180,117,32,6)

# Lockbox interact region rectangle 
lockboxRect = pygame.Rect(165, 110, 60, 35)

eye_squish_sound = Sounds.loadAudio("Audio/eyeSquish.wav")
eye_squish_sound.set_volume(.5)

def inBounds(x, y):
    global exit, lockboxExit
    if exit:
        exit = False
        return 0
    if lockboxExit:
        lockboxExit = False
        return 1  # Return to Lockboxpuzzle
    return False

def positionDeterminer(cameFrom):
    pass

def Room(screen, screen_res, events):
    global exit, goodEye, collected, mat, stem, corner, water, light, backgroundDiff, found, played, lockboxExit
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                exit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mouse_pos = (mouse_x/xScale, mouse_y/yScale)
                    if matRect.collidepoint(mouse_pos) or matRect2.collidepoint(mouse_pos):
                        if not mat:
                            eye_squish_sound.play()
                            mat = True
                            found += 1
                    elif stemRect.collidepoint(mouse_pos) or stemRect2.collidepoint(mouse_pos):
                        if not stem:
                            eye_squish_sound.play()
                            stem = True
                            found += 1
                    elif cornerRect.collidepoint(mouse_pos) or cornerRect2.collidepoint(mouse_pos):
                        if not corner:
                            eye_squish_sound.play()
                            corner = True
                            found += 1
                    elif waterRect.collidepoint(mouse_pos) or waterRect2.collidepoint(mouse_pos):
                        if not water:
                            eye_squish_sound.play()
                            water = True
                            found += 1
                    elif lightRect.collidepoint(mouse_pos) or lightRect2.collidepoint(mouse_pos):
                        if not light:
                            eye_squish_sound.play()
                            light = True
                            found += 1
                    elif backgroundRect.collidepoint(mouse_pos) or backgroundRect2.collidepoint(mouse_pos):
                        if not chairRect1.collidepoint(mouse_pos) and not chairRect2.collidepoint(mouse_pos) and not chairRect3.collidepoint(mouse_pos) and not chairRect4.collidepoint(mouse_pos):
                            if not backgroundDiff:
                                eye_squish_sound.play()
                                backgroundDiff = True
                                found += 1
                    elif lockboxRect.collidepoint(mouse_pos):
                        global lockboxExit
                        lockboxExit = True
                    if found == 6 and not goodEye:
                        goodEye = True
                        goodEYEtext.activated_time = pygame.time.get_ticks()

    virtual_screen.fill((195, 195, 195))

    # Assets.punch_light_hole(virtual_screen, dark_overlay, (virtual_screen.get_width()/2, virtual_screen.get_height()/2), 500, (100, 0, 100))

    if not Objects.getPinkPower():
        virtual_screen.blit(background2, (0,0))
    else:
        virtual_screen.blit(background3, (0,0))

    if found > 0 and not (goodEye and goodEYEtext.activated_time == -1):
        index = 0
        for eyePos in smallEyesPositions:
            if found > index:
                virtual_screen.blit(eyeClosedSmall, eyePos)
            else:
                virtual_screen.blit(eyeOpenSmall, eyePos)
            index += 1

    goodEYEtext.update()

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale