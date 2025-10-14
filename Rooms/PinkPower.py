# Example file showing a circle moving on screen
import pygame
import Assets
import Objects
import Sounds
from LightSource import LightSource
from LightFalloff import LightFalloff
from LightingUtils import apply_lighting, apply_falloff

pinkPower = False
played = False

switchSound = pygame.mixer.Sound("Audio/switch.wav")

powerSoundTimer = Objects.timer(1.5, False)
pulseTimer = Objects.timer(0.099, True)

virtual_res = (352, 384)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)
dark_overlay.fill((0, 0, 0, 50))

player_pos = pygame.Vector2(175, 340)

floor = pygame.image.load("Assets/floor.png")
door = pygame.image.load("Assets/powerRoomDoor.png")

scaledSwitch = []

for tile in Assets.pinkSwitch:
    scaledTile = pygame.transform.scale(tile, (tile.get_width()*2,tile.get_height()*2))
    scaledSwitch.append(scaledTile)

switchRect = pygame.Rect(136,256,80,8)

dimLightScale1 = pygame.transform.scale(Assets.squishedDimTiles[1], (Assets.squishedDimTiles[1].get_width()/2, Assets.squishedDimTiles[1].get_height()*1.5))
dimLightScale2 = pygame.transform.scale(Assets.squishedDimTiles[1], (Assets.squishedDimTiles[1].get_width()/2.2, Assets.squishedDimTiles[1].get_height()*1.5))
dimLightScale3 = pygame.transform.scale(Assets.squishedDimTiles[1], (Assets.squishedDimTiles[1].get_width()/2.5, Assets.squishedDimTiles[1].get_height()*1.5))

LightScale1 = pygame.transform.scale(Assets.squishedTiles[1], (Assets.squishedTiles[1].get_width()/2, Assets.squishedTiles[1].get_height()*1.5))
LightScale2 = pygame.transform.scale(Assets.squishedTiles[1], (Assets.squishedTiles[1].get_width()/2.2, Assets.squishedTiles[1].get_height()*1.5))
LightScale3 = pygame.transform.scale(Assets.squishedTiles[1], (Assets.squishedTiles[1].get_width()/2.5, Assets.squishedTiles[1].get_height()*1.5))

class Light:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 1

lights = [
    [Light(156, 180), dimLightScale1, LightScale1],
    [Light(156, 172), dimLightScale1, LightScale1],
    [Light(156, 164), dimLightScale1, LightScale1],
    [Light(156, 156), dimLightScale1, LightScale1],
    [Light(156, 148), dimLightScale1, LightScale1],
    [Light(156, 140), dimLightScale1, LightScale1],
    [Light(156, 132), dimLightScale1, LightScale1],
    [Light(158, 124), dimLightScale2, LightScale2],
    [Light(160, 116), dimLightScale3, LightScale3]
]

lightPos = [(64 + 16,0 + 16), (256 + 16,0 + 16), (64 + 16,224 + 16), (256 + 16,224 + 16)]
lightsNew = [LightSource(lightPos[0][0], lightPos[0][1], radius=60, strength = 220),
             LightSource(lightPos[1][0], lightPos[1][1], radius=60, strength = 220),
             LightSource(lightPos[2][0], lightPos[2][1], radius=60, strength = 220),
             LightSource(lightPos[3][0], lightPos[3][1], radius=60, strength = 220),]
falloff = [LightFalloff((virtual_res[0], virtual_res[1]), darkness = 25)]

pulse = 8
setup = False

def lightFunction():
    global lights, powerSoundTimer, pulseTimer, pulse, setup

    if not powerSoundTimer.Done():
        for light in lights:
                light[0].state = 2
    else:
        if not setup:
            for light in lights:
                light[0].state = 1
            setup = True
        pulseTimer.setInitial()
        if pulseTimer.Done():
            if pulse == 0:
                newPulse = 8
            else:
                newPulse = pulse - 1
            lights[pulse][0].state = 1
            lights[newPulse][0].state = 2
            if newPulse - 1 >= 0:
                lights[newPulse-1][0].state = 2
            if newPulse - 2 >= 0:
                lights[newPulse-2][0].state = 2
            if newPulse - 3 >= 0:
                lights[newPulse-3][0].state = 2
            pulse = newPulse
        

def inBounds(x, y):
    global pinkPower, pulse
    doorRect = pygame.Rect(300,208,door.get_width(),door.get_height())
    if doorRect.collidepoint(x,y):
        level, power = Objects.getPipeDungeonInfo()
        _, lowerWingPower = Objects.getPinkWingInfo()
        if not pinkPower and level == 1 and power and lowerWingPower:
            Sounds.powerAmb.play(-1)
            Sounds.ominousAmb.stop()
        if pinkPower:
            Sounds.powerOnAmb.stop()
        return 0
    if y > 368:
        return False
    if x < 16 or x > 336:
        return False
    if x < 64:
        if y > 384 - (x + 64):
            return True
        return False
    if x >= 64 and x < 288:
        if y > 256:
            return True
        return False
    if x >= 288:
        if y > 384 - (352 - x + 64):
            return True
        return False

def positionDeterminer(cameFrom):
    global player_pos
    player_pos = pygame.Vector2(300 - 20 + door.get_width()/4, 208 + (door.get_height()*5/6))

def Room(screen, screen_res, events):
    global pinkPower, played

    # poll for events
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if switchRect.collidepoint(player_pos) and not pinkPower:
                    Sounds.powerOn.play()
                    Sounds.powerAmb.play(-1)
                    Sounds.ominousAmb.stop()
                    pinkPower = True
                    powerSoundTimer.setInitial()

    if powerSoundTimer.Done() and not played:
        played = True
        Sounds.powerOnAmb.play(-1)

    if pinkPower:
        lightFunction()

    # fill the screen with a color to wipe away anything from last frame
    virtual_screen.fill("gray")
    dark_overlay.fill((0, 0, 0, 150))

    virtual_screen.blit(floor, (0, 256))
    pygame.draw.line(virtual_screen, (0,0,0), (64, 0), (64, 256), 1)
    pygame.draw.line(virtual_screen, (0,0,0), (288, 0), (288, 256), 1)

    if pinkPower:
        Assets.punch_light_hole(virtual_screen, dark_overlay, (virtual_screen.get_width()/1.8, virtual_screen.get_height()/2), 500, (0, 0, 0))

    if pinkPower:
        virtual_screen.blit(Assets.tiles[1], (64,0))
        virtual_screen.blit(Assets.tiles[1], (256,0))
        virtual_screen.blit(Assets.tiles[1], (64,224))
        virtual_screen.blit(Assets.tiles[1], (256,224))
    else:
        virtual_screen.blit(Assets.dimTiles[1], (64,0))
        virtual_screen.blit(Assets.dimTiles[1], (256,0))
        virtual_screen.blit(Assets.dimTiles[1], (64,224))
        virtual_screen.blit(Assets.dimTiles[1], (256,224))

    for light in lights:
        virtual_screen.blit(light[light[0].state], (light[0].x, light[0].y))

    virtual_screen.blit(Assets.pipes[7], (160, 242))
    virtual_screen.blit(Assets.pipes[10], (190, 272))
    virtual_screen.blit(Assets.pipes[10], (290, 272))

    for y in range(208, 272, 32):
        virtual_screen.blit(Assets.pipes[7], (160, y))

    virtual_screen.blit(Assets.pipes[3], (160, 272))

    for x in range(192, 320, 32):
        virtual_screen.blit(Assets.pipes[10], (x, 272))

    if not pinkPower:
        virtual_screen.blit(scaledSwitch[0], (144,192))
    else:
        virtual_screen.blit(scaledSwitch[1], (144,192))

    virtual_screen.blit(door, (300,208))

    pygame.draw.circle(virtual_screen, "red", player_pos, 16)

    # apply lighting
    if pinkPower:
        # add pulse lights to lights array
        lightsNew.append(LightSource(lights[(pulse - 1) % 8][0].x + 20, lights[(pulse - 1) % 8][0].y + 15, radius=50, strength=100, color=(150,0,100)))
        #LightSource(upperWingLight.x + 16, upperWingLight.y + 16, radius=pinkLightRadius, strength = pinkLightStrength, color = pinkLightColor)
        apply_lighting(virtual_screen, lightsNew, darkness=10, ambient_color=(50, 50, 50), ambient_strength=10)
        # apply falloff
        apply_falloff(falloff, virtual_screen, (lightsNew[0].x, lightsNew[0].y + 100)) # +100 bc otherwise the falloff does not cover the whole scree (i think this is caused by the lights being too close to the edge of the screen? maybe can be fixed)
        apply_falloff(falloff, virtual_screen, (lightsNew[1].x, lightsNew[1].y + 100))
        apply_falloff(falloff, virtual_screen, (lightsNew[2].x, lightsNew[2].y))
        apply_falloff(falloff, virtual_screen, (lightsNew[3].x, lightsNew[3].y))
        apply_falloff(falloff, virtual_screen, (lightsNew[4].x, lightsNew[4].y))

        lightsNew.pop()

        #for i in range(4, len(lightsNew)):
            #apply_falloff(falloff, virtual_screen, (lightsNew[i].x, lightsNew[i].y))

    virtual_screen.blit(dark_overlay, (0, 0))

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 2, 2  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
