import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import Player
import Items
from LightSource import LightSource
from LightFalloff import LightFalloff
from LightingUtils import apply_lighting, apply_falloff

virtual_res = (416, 256)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

ladderHatchOpen_original = pygame.image.load("Assets/LadderHatchOpen.png")

original_size = ladderHatchOpen_original.get_size()
new_size = (int(original_size[0] * 0.40), int(original_size[1] * 0.3))
ladderHatchOpen = pygame.transform.scale(ladderHatchOpen_original, new_size)

lightsNew = [LightSource(100, 128, radius=60, strength = 150),
             LightSource(300, 128, radius=60, strength = 150)]
falloff = [LightFalloff(virtual_screen.get_size(), darkness = 100)]

brokenWire = pygame.image.load("Assets/BrokenWire.png")

fixedWire = pygame.image.load("Assets/FixedWire.png")

# Load outer puddle image with 70% opacity
outerPuddle = pygame.image.load("Assets/OuterPuddle.png")
outerPuddle.set_alpha(179)

# puddle interaction region
puddleRegion = pygame.Rect(250, 70, 60, 115)  

# puddle collision area (blocks movement when puddles exist)
puddleCollisionArea = pygame.Rect(270, 20, 50, 300)  # Area around outerPuddle that blocks movement

lowerLevelFlooded = pygame.image.load("Assets/LowerLevelFlooded.png")
lowerLevelFloodedText = Objects.briefText(virtual_screen, lowerLevelFlooded, 15, 180, 3)

# puddle interaction variables
puddleSelected = False

# Wire repair variables
wireRepaired = False
wireRect = pygame.Rect(292, 95, 32, 32)  # Clickable area around the broken wire

# Electrical effect variables
import random
import math
electrical_timer = 0
spark_positions = []

hatchPosition = (90, 40)
hatchRect = pygame.Rect(hatchPosition[0], hatchPosition[1], new_size[0], new_size[1])  # Clickable area

bounds = Polygon([(48,48), (368,48), (368,208), (48,208)])

def draw_electrical_effects(surface, puddle_positions):
    global electrical_timer, spark_positions
    
    electrical_timer += 1
    
    
    if electrical_timer % 40 == 0:  # New sparks every 40 frames
        spark_positions.clear()
        
        outer_puddle_pos = (280, 80)
        for _ in range(random.randint(1, 2)):
            spark_x = outer_puddle_pos[0] + random.randint(0, 50)  # 50 pixel width region
            spark_y = outer_puddle_pos[1] + random.randint(0, 90)  # 90 pixel height region
            spark_positions.append((spark_x, spark_y))
    
    
    for pos in spark_positions:
        
        if random.random() > 0.55:  # 45% chance to show spark each interval

            surface.set_at(pos, (255, 255, 0))  # yellow pixel

lights = [
    Objects.Light(336, 80, 2),
    Objects.Light(336, 144, 2),
    Objects.Light(48, 48, 2),
    Objects.Light(48, 176, 2)
]

southDoor = Objects.Door((virtual_screen.get_width()/2) - 16, 208, Assets.grayDoorSouth)
westDoor = Objects.Door(16, 112, Assets.grayDoorWest)
eastDoor = Objects.Door(368, 112, Assets.grayDoorEast)
topRightWall = pygame.Rect(275, 48, 125, 31)
bottomRightWall = pygame.Rect(276, 176, 124, 32)

powerRoom = False

def inBounds(x, y):
    global powerRoom, puddleSelected

    level, power = Objects.getPipeDungeonInfo()
    if southDoor.rect.collidepoint((x,y)):
        cleanup()
        if not Objects.getBluePower():
            Sounds.ominousAmb.stop()
            Sounds.powerAmb.play(-1)
        lowerLevelFloodedText.activated_time = -1
        return 0
    elif westDoor.rect.collidepoint((x,y)):
        cleanup()
        Sounds.powerAmb.stop()
        Sounds.ominousAmb.play(-1)
        lowerLevelFloodedText.activated_time = -1
        return 1
    elif eastDoor.rect.collidepoint((x,y)):
        cleanup()
        if not Objects.getBluePower():
            Sounds.ominousAmb.stop()
            Sounds.powerAmb.play(-1)
        lowerLevelFloodedText.activated_time = -1
        return 2
    elif puddleSelected:
        puddleSelected = False
        return 4  
    elif powerRoom:
        cleanup()
        if Objects.getBluePower():
            Sounds.powerOnAmb.play(-1)
        powerRoom = False
        return 3
    elif not bounds.contains(Point(x,y)) or topRightWall.collidepoint((x,y)) or bottomRightWall.collidepoint((x,y)):
        return False
    else:
        # Check if puddles are cleaned up - if not, block movement through puddle area
        try:
            from Rooms import PuddleView
            puddles_cleaned = PuddleView.getPuddlesCleaned()
        except:
            puddles_cleaned = False
            
        if not puddles_cleaned and puddleCollisionArea.collidepoint((x,y)):
            return False  # Block movement through puddle area
            
    return True

def positionDeterminer(cameFrom):
    global player_pos
    if cameFrom == "Rooms.BreakerRoom":
        player_pos = pygame.Vector2(southDoor.x + 16, southDoor.y - 5)
    if cameFrom == "Rooms.StorageCloset":
        player_pos = pygame.Vector2(westDoor.x + 37, westDoor.y + 16)
    if cameFrom == "Rooms.ValvePuzzle":
        player_pos = pygame.Vector2(eastDoor.x - 5, eastDoor.y + 16)
    if cameFrom == "Rooms.BluePower":
        player_pos = pygame.Vector2(123, 75)

def cleanup():
    #Stop electricity sound when leaving the room
    if hasattr(Room, 'electricityChannel') and Room.electricityChannel:
        Room.electricityChannel.pause()
        Room.electricityPlaying = False

def Room(screen, screen_res, events):
    global powerRoom, puddleSelected, wireRepaired
    level, power = Objects.getPipeDungeonInfo()

    # Proximity-based electricity sound for puddle
    try:
        from Rooms import PuddleView
        puddlesCleaned = PuddleView.getPuddlesCleaned()
    except:
        puddlesCleaned = False
    
    if not puddlesCleaned:
        
        puddleCenter = pygame.Vector2(280, 110)  # Center of puddle area
        distance = player_pos.distance_to(puddleCenter)
        
        # Set volume based on distance
        maxDistance = 240  # Maximum distance for sound 
        minDistance = 80   # Minimum distance 
        
        if distance <= maxDistance:
            if distance <= minDistance:
                volume = 0.6  # Full volume when very close
            else:
                volume = 0.6 * (1.0 - (distance - minDistance) / (maxDistance - minDistance))
            
            # Calculate directional audio based on horizontal position
            horizontalDiff = puddleCenter.x - player_pos.x
            screenWidth = 416
            
            maxHorizontalDistance = screenWidth / 2
            panFactor = horizontalDiff / maxHorizontalDistance
            panFactor = max(-1.0, min(1.0, panFactor))
            
            if panFactor <= 0:
                
                leftVolume = volume
                rightVolume = volume * (1 + panFactor)  # Reduces as sound moves left
            else:
                
                leftVolume = volume * (1 - panFactor)  # Reduces as sound moves right
                rightVolume = volume
            
            # Set stereo volumes
            Sounds.electricityNoise.set_volume(leftVolume)
            
            if not hasattr(Room, 'electricityChannel'):
                Room.electricityChannel = Sounds.electricityNoise.play(-1)  # Loop indefinitely
                Room.electricityChannel.pause()
                Room.electricityPlaying = False
            elif not Room.electricityPlaying:
                Room.electricityChannel.unpause()
                Room.electricityPlaying = True
            else:
                Room.electricityChannel.set_volume(leftVolume, rightVolume)
            
        else:
            #stop the sound if too far away
            if hasattr(Room, 'electricityChannel') and Room.electricityChannel:
                Room.electricityChannel.stop()
                Room.electricityPlaying = False
    else:
        # Puddles are cleaned, stop electricity sound
        if hasattr(Room, 'electricityChannel') and Room.electricityChannel:
            Room.electricityChannel.stop()
            Room.electricityPlaying = False

    for event in events:
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if hatchRect.collidepoint(player_pos):
                        if not Objects.getWaterLevelsSolved():
                            lowerLevelFloodedText.activated_time = pygame.time.get_ticks()
                        else:
                            powerRoom = True
                    
                    elif Player.checkItem(Items.electricalTape):
                        if wireRect.collidepoint(player_pos) and not wireRepaired:
                            channel1 = pygame.mixer.Channel(5)
                            channel1.play(Sounds.tape)
                            wireRepaired = True
                    elif puddleRegion.collidepoint(player_pos):
                        # Check if puddles are already cleaned
                        try:
                            from Rooms import PuddleView
                            puddles_cleaned = PuddleView.getPuddlesCleaned()
                        except:
                            puddles_cleaned = False
                                
                        if not puddles_cleaned:
                            puddleSelected = True
                        # If puddles are cleaned, block entering puddle view again

    virtual_screen.fill((105,105,105))
    dark_overlay.fill((0, 0, 0, 150))
    outerRect = pygame.Rect((16,16,384,224))
    innerRect = pygame.Rect((48,48,320,160))

    # outer walls
    pygame.draw.rect(virtual_screen, "gray", outerRect)
    pygame.draw.rect(virtual_screen, "black", outerRect, 1)
    pygame.draw.rect(virtual_screen, "black", innerRect, 1)
    pygame.draw.line(virtual_screen, "black", outerRect.topleft, innerRect.topleft, 1)
    pygame.draw.line(virtual_screen, "black", outerRect.topright, innerRect.topright, 1)
    pygame.draw.line(virtual_screen, "black", outerRect.bottomleft, innerRect.bottomleft, 1)
    pygame.draw.line(virtual_screen, "black", outerRect.bottomright, innerRect.bottomright, 1)

    # hallway wall on bottom right
    pygame.draw.rect(virtual_screen, (105, 105, 105), (275, 176, 200, 200))
    pygame.draw.rect(virtual_screen, "black", (275, 176, 200, 200), 1)
    pygame.draw.line(virtual_screen, (105, 105, 105), (275,240), (275,256))
    pygame.draw.line(virtual_screen, (105, 105, 105), (400,176), (416,176))
    pygame.draw.rect(virtual_screen, "gray", bottomRightWall)
    pygame.draw.rect(virtual_screen, "black", bottomRightWall, 1)
    pygame.draw.line(virtual_screen, "gray", (398,176),(368,176), 2)
    pygame.draw.line(virtual_screen, "black", (399,207),(367,176))

    # hallway wall on top right
    pygame.draw.rect(virtual_screen, (105, 105, 105), (275, -120, 200, 200))
    pygame.draw.rect(virtual_screen, "black", (275, -120, 200, 200), 1)
    pygame.draw.line(virtual_screen, (105, 105, 105), (275,0), (275,15))
    pygame.draw.line(virtual_screen, (105, 105, 105), (400,79), (416,79))
    pygame.draw.rect(virtual_screen, "gray", topRightWall)
    pygame.draw.rect(virtual_screen, "black", topRightWall, 1)
    pygame.draw.line(virtual_screen, "gray", (398,78),(368,78), 2)
    pygame.draw.line(virtual_screen, "black", (399,48),(367,78))

    Done = False

    for light in lights:
        light.update()
        if not Done:
            #Assets.punch_light_hole(virtual_screen, dark_overlay, (112, 112), 300, (0, 162, 232))
            Done = True
        virtual_screen.blit(light.image, light.rect)

    for y in range(144, 208, 32):
        virtual_screen.blit(Assets.pipes[12], (int(virtual_screen.get_width()/2) - 16,y))

    virtual_screen.blit(Assets.pipes[15], (int(virtual_screen.get_width()/2) - 16,112))

    for x in range(int(virtual_screen.get_width()/2) + 16, 368, 32):
        virtual_screen.blit(Assets.pipes[10], (x,112))

    # Draw broken wire or repaired wire based on repair status
    if wireRepaired:
        virtual_screen.blit(fixedWire, (292, 85))  # Repaired wire
    else:
        virtual_screen.blit(brokenWire, (292, 85))  # Broken wire
    
    virtual_screen.blit(Assets.pipes[5], (300, 80))
    virtual_screen.blit(Assets.pipes[3], (250, 80))
    virtual_screen.blit(Assets.pipes[5], (250, 52))
    # horizontal connection toward ladder
    virtual_screen.blit(Assets.pipes[10], (270, 80))
    virtual_screen.blit(Assets.pipes[10], (228, 52))
    virtual_screen.blit(Assets.pipes[10], (198, 52))
    virtual_screen.blit(Assets.pipes[10], (166, 52))
    virtual_screen.blit(Assets.pipes[10], (134, 52))

    virtual_screen.blit(southDoor.image, southDoor.rect)
    virtual_screen.blit(westDoor.image, westDoor.rect)
    virtual_screen.blit(eastDoor.image, eastDoor.rect)

    virtual_screen.blit(ladderHatchOpen, hatchPosition)

    # Draw puddles only if they haven't been cleaned up
    try:
        from Rooms import PuddleView
        puddles_cleaned = PuddleView.getPuddlesCleaned()
    except:
        puddles_cleaned = False
        
    if not puddles_cleaned:
        virtual_screen.blit(outerPuddle, (250, 80))
        
        # Draw electrical effects on the electrified water only if puddle exists
        puddle_positions = [(250, 80)]  # Only OuterPuddle remains
        draw_electrical_effects(virtual_screen, puddle_positions)

    Player.animatePlayer(virtual_screen, player_pos, 32, 32, "top-down")

    apply_lighting(virtual_screen, lightsNew, darkness=10, ambient_color=(50, 50, 50), ambient_strength=10)
    apply_falloff(falloff, virtual_screen, (lightsNew[0].x, lightsNew[0].y))
    apply_falloff(falloff, virtual_screen, (lightsNew[1].x, lightsNew[1].y))

    lowerLevelFloodedText.update()

    #virtual_screen.blit(dark_overlay, (0, 0))

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 2, 2  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
