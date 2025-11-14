import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
from LightSource import LightSource
from LightFalloff import LightFalloff
from LightingUtils import apply_lighting, apply_falloff
import Player
import Items
import random
from Rooms import BedroomDeskView

virtual_res = (256, 256)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

bounds = Assets.draw_polygon(virtual_screen, (208, 208), 4, 160, "gray")
outline = Polygon(bounds)

# Determines which room is loaded
BedroomNumber = 1

lights = [
    Objects.Light(176, 48, 1),
    Objects.Light(176, 176, 1)
]

leftBed = pygame.image.load("Assets/leftBed.png")
rightBed = pygame.image.load("Assets/rightBed.png")
leftDesk = pygame.image.load("Assets/leftBedroomDesk.png")
rightDesk = pygame.image.load("Assets/rightBedroomDesk.png")
thermometerOnDesk = pygame.image.load("Assets/ThermometerOnDesk.png")


trash = pygame.image.load("Assets/Trash.png")
trashInteractRect = trash.get_rect()
trashInteractRect.topleft = (108,185)

leftDeskInteractRect = leftDesk.get_rect()
leftDeskInteractRect.topleft = (25, 160)
leftDeskInteractRect.bottomright = (leftDeskInteractRect.bottomright[0] + 20, leftDeskInteractRect.bottomright[1])

leftBedInteractRect = leftBed.get_rect()
leftBedInteractRect.topleft = (37,37)
leftBedInteractRect.bottomright = (leftBedInteractRect.bottomright[0] + 20, leftBedInteractRect.bottomright[1])

rightBedInteractRect = rightBed.get_rect()
rightBedInteractRect.topleft = (172,37)
rightBedInteractRect.bottomleft = (rightBedInteractRect.bottomleft[0] - 20, rightBedInteractRect.bottomleft[1])

# New Lighting
pinkLightRadius = 25
pinkLightStrength = 100
#pinkLightColor = (245, 118, 238)
pinkLightColor = (255, 20, 243)
ambientLightPos = (256/2, 256/2)
lightsNew = [LightSource(ambientLightPos[0], ambientLightPos[1], radius=60, strength = 200),
             LightSource(lights[0].x + 16, lights[0].y + 16, radius=pinkLightRadius, strength = pinkLightStrength, color = pinkLightColor),
             LightSource(lights[1].x + 16, lights[1].y + 16, radius=pinkLightRadius, strength = pinkLightStrength, color = pinkLightColor)]
falloff = [LightFalloff(virtual_screen.get_size(), darkness = 50)]
falloffPartial = [LightFalloff(virtual_screen.get_size(), darkness = 75)]

northDoor = Objects.Door(112, 16, Assets.grayDoorNorth)

tooDarkSeeScaled = pygame.transform.scale(Assets.tooDarkSee, (Assets.tooDarkSee.get_width()/1.5, Assets.tooDarkSee.get_height()/1.5))
tooDarkSee = Objects.briefText(virtual_screen, tooDarkSeeScaled, 5, 90, 3)
trashEmpty = Objects.briefText(virtual_screen, Assets.trashEmpty, 0, 90, 3)
somethingInside = Objects.briefText(virtual_screen, Assets.somethingInside, 0, 90, 3)

bedView = False
deskView = False

lightsOn = True
greenPowerOn = False
notePuzzle = False

def inBounds(x, y):
    global leftBed, rightBed, bedView, notePuzzle, deskView
    level, power = Objects.getPipeDungeonInfo()
    leftBedRect = leftBed.get_rect()
    leftBedRect.topleft = (37,37)
    rightBedRect = rightBed.get_rect()
    rightBedRect.topleft = (172,37)
    rightDeskRect = rightDesk.get_rect()
    rightDeskRect.topleft = (148, 168)
    leftDeskRect = leftDesk.get_rect()
    leftDeskRect.topleft = (45, 168)
    #rightDeskRect.topleft = (45, 176)
    trashRect = pygame.Rect(112,190, 30, 40)
    backWallRect = pygame.Rect(100,200, 60, 60)

    if northDoor.rect.collidepoint((x,y)):
        tooDarkSee.activated_time = -1
        trashEmpty.activated_time = -1
        somethingInside.activated_time = -1
        if BedroomNumber == 2:
            if (level == 3 and power) or Objects.getGreenPower():
                Sounds.ominousAmb.stop()
                Sounds.powerAmb.play(-1)
        return 0
    elif bedView:
        bedView = False
        return 1
    elif deskView:
        deskView = False
        return 3  # Return BedroomDeskView
    elif notePuzzle:
        if somethingInside.activated_time == -1:
            notePuzzle = False
            return 2
        else:
            return False
    elif leftBedRect.collidepoint((x,y)) or rightBedRect.collidepoint((x,y)) or leftDeskRect.collidepoint(x, y) or rightDeskRect.collidepoint(x, y) \
    or trashRect.collidepoint(x,y) or backWallRect.collidepoint(x, y):
        return False
    elif not outline.contains(Point(x,y)):
        return False
    return True

def positionDeterminer(cameFrom):
    global player_pos, leftBedInteractRect, rightBedInteractRect, leftDeskInteractRect
    bedNum = Objects.getBedNumber()
    if cameFrom == "Rooms.GreenRoom":
        player_pos = pygame.Vector2(northDoor.x + northDoor.rect.width/2, northDoor.y + northDoor.rect.height + 5)
    elif cameFrom == "Rooms.TornNotePuzzle":
        player_pos = pygame.Vector2(northDoor.x + northDoor.rect.width/2, 190)
    elif cameFrom == "Rooms.BedroomDeskView": # came from desk view
        player_pos = pygame.Vector2(leftDeskInteractRect.x + 40, leftDeskInteractRect.y - 10)
    elif bedNum == 0: # came from left bed view
        player_pos = pygame.Vector2(leftBedInteractRect.x + 40, leftBedInteractRect.y + 44)
    else: # came from right bed view
        player_pos = pygame.Vector2(rightBedInteractRect.x + 8, rightBedInteractRect.y + 44)

def Room(screen, screen_res, events):
    global bedView, lightsOn, greenPowerOn, notePuzzle, deskView
    level, power = Objects.getPipeDungeonInfo()

    # Add greenpower statement
    if (level == 3 and power) or Objects.getGreenPower():
        greenPowerOn = True
    else:
        greenPowerOn = False
    #greenPowerOn = True # FOR TESTING

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if leftBedInteractRect.collidepoint(player_pos): # go to left bedview
                    if greenPowerOn:
                        Objects.setBedNumber(0)
                        bedView = True
                    else:
                        tooDarkSee.activated_time = pygame.time.get_ticks()
                elif rightBedInteractRect.collidepoint(player_pos): # go to right bedview
                    if greenPowerOn:
                        Objects.setBedNumber(1)
                        bedView = True
                    else:
                        tooDarkSee.activated_time = pygame.time.get_ticks()
                elif leftDeskInteractRect.collidepoint(player_pos) and BedroomNumber == 1: # go to bedroom 1 desk view
                    if greenPowerOn:
                        deskView = True
                    else:
                        tooDarkSee.activated_time = pygame.time.get_ticks()
                elif trashInteractRect.collidepoint(player_pos):
                    if not greenPowerOn:
                        tooDarkSee.activated_time = pygame.time.get_ticks()
                    elif BedroomNumber == 1 or BedroomNumber == 2:
                        trashEmpty.activated_time = pygame.time.get_ticks()
                    else:
                        somethingInside.activated_time = pygame.time.get_ticks()
                        notePuzzle = True          

    virtual_screen.fill((105,105,105))
    dark_overlay.fill((0, 0, 0, 150))
    outer = Assets.draw_polygon(virtual_screen, (240, 240), 4, 224, "gray", 1, True)
    outer = Assets.draw_polygon(virtual_screen, (240, 240), 4, 224, "black")
    inner = Assets.draw_polygon(virtual_screen, (208, 208), 4, 160, "black")
    for i in range(4):
        pygame.draw.line(virtual_screen, "black", outer[i], inner[i], 1)

    Done = False

    '''
    if not Objects.getPinkPower():
        for light in lights:
            lit = light.update()
            if not Done and lit:
                if upperWingPower:
                    shadowRect = pygame.Rect(0,144,112,112)
                    shadow = virtual_screen.subsurface(shadowRect).copy()
                elif lowerWingPower:
                    shadowRect = pygame.Rect(0,0,112,112)
                    shadow = virtual_screen.subsurface(shadowRect).copy()
                Assets.punch_light_hole(virtual_screen, dark_overlay, (112, 112), 300, (1, 0, 1))
                virtual_screen.blit(shadow, shadowRect)
                Done = True
            # virtual_screen.blit(light.image, light.rect)
    else:
        for light in lights:
            light.update()
            if not Done:
                Assets.punch_light_hole(virtual_screen, dark_overlay, (112, 112), 300, (1, 0, 1))
                Done = True
            # virtual_screen.blit(light.image, light.rect)
    '''
    virtual_screen.blit(northDoor.image, northDoor.rect)

    virtual_screen.blit(leftBed, (37,37))
    virtual_screen.blit(rightBed, (172,37))
    virtual_screen.blit(rightDesk, (148,168))
    virtual_screen.blit(leftDesk, (45,168))
    
    # Draw thermometer on desk only if not collected and in bedroom 1
    if BedroomNumber == 1 and not BedroomDeskView.thermometerCollected:
        virtual_screen.blit(thermometerOnDesk, (60,175))  # Positioned on the desk
    
    virtual_screen.blit(trash, (108,185))
    
    Player.animatePlayer(virtual_screen, player_pos, 32, 32, "top-down")

    # Unique things in each room here
    if BedroomNumber == 1:
        lightsOn = True
    elif BedroomNumber == 2:
        # light flickering
        lightRng = random.randint(0, 100)
        if lightRng < 2:
            lightsOn = False

            if greenPowerOn:
            # play flicker sound
                lightRng = random.randint(1,5)
                match lightRng:
                    case 1:
                        Sounds.spark1.play()
                    case 2:
                        Sounds.spark2.play()
                    case 3:
                        Sounds.spark3.play()
                    case 4:
                        Sounds.spark4.play()
                    case 5:
                        Sounds.spark5.play()
    elif BedroomNumber == 3:
        lightsOn = True

    # if not Objects.getPinkPower():
    #     if power and level == 1:
    #         # the lights are done using an array like this because apply_lighting() only works properly if all the lights in the room are in 1 array. Does not work propely if called multiple times
    #         # remove upper and lower lights
    #         while len(lightsNew) > 3:
    #             lightsNew.pop()

    #         # apply lighting
    #         apply_lighting(virtual_screen, lightsNew, darkness=10, ambient_color=(50, 50, 50), ambient_strength=10)
    #         apply_falloff(falloffPartial, virtual_screen, ambientLightPos)
    #         apply_falloff(falloffPartial, virtual_screen, (lightsNew[1].x, lightsNew[1].y))  
    #         apply_falloff(falloffPartial, virtual_screen, (lightsNew[2].x, lightsNew[2].y))  
    #         apply_falloff(falloffPartial, virtual_screen, (lightsNew[3].x, lightsNew[3].y)) 
            
    # else:
    #     if len(lightsNew) != 5: # reset lights array if the right amount of lights is not in it
    #         while len(lightsNew) > 3:
    #                 lightsNew.pop()

    #     # apply lighting
    #     apply_lighting(virtual_screen, lightsNew, darkness=10, ambient_color=(50, 50, 50), ambient_strength=10)
    #     apply_falloff(falloff, virtual_screen, ambientLightPos)
    #     apply_falloff(falloff, virtual_screen, (lightsNew[1].x, lightsNew[1].y))  
    #     apply_falloff(falloff, virtual_screen, (lightsNew[2].x, lightsNew[2].y)) 
    #     apply_falloff(falloff, virtual_screen, (lightsNew[3].x, lightsNew[3].y)) 
    #     apply_falloff(falloff, virtual_screen, (lightsNew[4].x, lightsNew[4].y)) 

    if greenPowerOn and lightsOn and BedroomNumber != 2:
        Assets.punch_light_hole(virtual_screen, dark_overlay, (112, 112), 300, (1, 0, 1))
    elif greenPowerOn and lightsOn:
        Assets.punch_light_hole(virtual_screen, dark_overlay, (112, 112), 300, (1, 0, 1)) # TODO: Make darker here

    # determine if light flicker should end this frame
    lightRng = random.randint(0, 100)
    if not lightsOn and lightRng < 30:
        lightsOn = True

    virtual_screen.blit(dark_overlay, (0, 0))

    tooDarkSee.update()
    trashEmpty.update()
    somethingInside.update()

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 2, 2  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
