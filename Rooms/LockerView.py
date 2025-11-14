import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Player
import Items
from LightSource import LightSource
from LightFalloff import LightFalloff
from LightingUtils import apply_lighting, apply_falloff
import Sounds
import random

virtual_res = (389, 195)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

# Item positions and scales
mop_pos = (108, 92)
mop_scale = 0.6
tape_pos = (125, 40)
tape_scale = 0.2

# Load images
lockerViewBg = pygame.image.load("Assets/LockerView.png")
backgroundClosed = Assets.lockerViewClosed
backgroundOpen = Assets.lockerViewOpen
lock = Assets.lock
mop = pygame.image.load("Assets/Mop.png")
yellowElectricalTape = pygame.image.load("Assets/tape_lockerview.png")
numberTiles = Assets.numberTiles
lockInterface = Assets.lockInterface

tapeRect = pygame.Rect(tape_pos[0], tape_pos[1], 16, 16)
mopRect = pygame.Rect(mop_pos[0], mop_pos[1], 60, 100)
lockRect = pygame.Rect(16, 96, 8, 9)
eyeDoorRect = pygame.Rect(12, 12, 67, 172)
lockInterfaceRect = pygame.Rect(4, 105, 119, 51)

light_pos = (389 / 2, 0)
lightsNew = [LightSource(light_pos[0], light_pos[1], radius=100, strength = 50)]
falloff = [LightFalloff(virtual_screen.get_size(), darkness = 160)]

tapeCollected = False
mopCollected = False
exit = False
unlocked = False # if the eye locker has been unlocked
open = False # if the eye locker is open
interface = False # if the lock interface is open

x = lockInterfaceRect.topleft[0] + 5
y = lockInterfaceRect.topleft[1] + 5
numbers = [
    Objects.Code(x, y),
    Objects.Code(x + 22, y),
    Objects.Code(x + (22 * 2), y),
    Objects.Code(x + (22 * 3), y),
    Objects.Code(x + (22 * 4), y)
]

lights = True

def inBounds(x, y):
    global exit
    if exit:
        exit = False
        return 0
    return False

def positionDeterminer(cameFrom):
    Sounds.lockerOpen.play()
    pass

def Room(screen, screen_res, events):
    global exit, tapeCollected, mopCollected, lights, unlocked, open, interface
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()
    dark_overlay.fill((0, 0, 0, 50))

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                if interface:
                    interface = False
                else:
                    Sounds.lockerClose.play()
                    exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_pos = (mouse_x/xScale, mouse_y/yScale)
                # player clicks tape
                if tapeRect.collidepoint(mouse_pos) and not tapeCollected:     
                    if (Player.addItem(Items.electricalTape)):
                        tapeCollected = True
                        Sounds.pickup.play()
                # player clicks mop
                if mopRect.collidepoint(mouse_pos) and not mopCollected:     
                    if (Player.addItem(Items.mop)):
                        mopCollected = True
                        Sounds.pickup.play()
                # clicks lock
                if lockRect.collidepoint(mouse_pos) and not unlocked:
                    interface = True
                # clicks eye locker door
                if eyeDoorRect.collidepoint(mouse_pos) and unlocked and not open:
                    open = True
                    Sounds.lockerOpen.play()
                
                # lock interface
                if interface:
                    for number in numbers:
                        if number.rect.collidepoint(mouse_pos):
                            Sounds.combo.play()
                            if number.state == 9:
                                number.state = 0
                            else:
                                number.state += 1
                            # code = 54937
                            if numbers[0].state == 5 and numbers[1].state == 4 and numbers[2].state == 9 and numbers[3].state == 3 and numbers[4].state == 7:
                                Sounds.unlock.play()
                                unlocked = True
                                interface = False

    # Display background image
    virtual_screen.fill("gray")
    if open:
        virtual_screen.blit(backgroundOpen, (0, 0))
    else:
        virtual_screen.blit(backgroundClosed, (0, 0))

    if not unlocked:
        virtual_screen.blit(lock, lockRect)

    scaled_mop = pygame.transform.scale(mop, (int(mop.get_width() * mop_scale), int(mop.get_height() * mop_scale)))
    #scaled_tape = pygame.transform.scale(yellowElectricalTape, (int(yellowElectricalTape.get_width() * tape_scale), int(yellowElectricalTape.get_height() * tape_scale)))

    lightRng = random.randint(0, 100)
    if lightRng < 2:
        lights = False

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

    # apply lights, make dark if flicker happening
    if (lights):
        apply_lighting(virtual_screen, lightsNew, darkness=60, ambient_color=(20, 20, 20), ambient_strength=10)
        apply_falloff(falloff, virtual_screen, light_pos)
    else:
        dark_overlay.fill((0, 0, 0, 180))

    # determine if light flicker should end this frame
    lightRng = random.randint(0, 100)
    if not lights and lightRng < 30:
        lights = True
    
    if not mopCollected:
        virtual_screen.blit(scaled_mop, mop_pos)
    if not tapeCollected:
        virtual_screen.blit(yellowElectricalTape, tape_pos)

    if interface:
        virtual_screen.blit(lockInterface, lockInterfaceRect)
        for number in numbers:
            virtual_screen.blit(numberTiles[number.state], number.rect)

    virtual_screen.blit(dark_overlay, (0, 0))
    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale