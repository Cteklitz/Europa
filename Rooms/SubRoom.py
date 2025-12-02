import pygame
import Assets
import Objects
import Items
from shapely.geometry import Point, Polygon
import Sounds
from LightSource import LightSource
from LightFalloff import LightFalloff
from LightingUtils import apply_lighting, apply_falloff
import Player
import random
import math

virtual_res = (648,357)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

virtual_res2 = (388, 343)
virtual_screen2 = pygame.Surface(virtual_res2)
dark_overlay2 = pygame.Surface(virtual_screen2.get_size(), pygame.SRCALPHA)

virtual_res3 = (288, 211)
virtual_screen3 = pygame.Surface(virtual_res3)

virtual_res4 = (288, 136)
virtual_screen4 = pygame.Surface(virtual_res3)

player_pos = pygame.Vector2(239, 180)

fuelLine = Assets.fuelLine
fuelLineFixed = Assets.fuelLineFixed
fuelLinePos = (34, 167)
puddle = Assets.fuelPuddle
puddlePos = (270,226)
puddleUpper = Assets.fuelPuddleUpper
puddleUpperPos = (300,207)

fuelLineInteractRect = pygame.Rect(270, 200, 80, 50)
consoleInteractRect = pygame.Rect(415, 134, 153, 134)

eyeOpen = pygame.transform.scale(pygame.image.load("Assets/EyeWall.png"), (120, 85))
eyeClosed = pygame.transform.scale(pygame.image.load("Assets/eyeClosedWall.png"), (120, 85))

eyeOpenSmall = pygame.transform.scale(pygame.image.load("Assets/EyeWall.png"), (30, 22))
eyeClosedSmall = pygame.transform.scale(pygame.image.load("Assets/eyeClosedWall.png"), (30, 22))

eye_rect = pygame.Rect(0, 0, eyeOpen.get_width(), 100)
eye_rect2 = pygame.Rect(0, 0, 30, 22)

eyes = [eyeOpen, eyeClosed]
eyes2 = [eyeOpenSmall, eyeClosedSmall]
currEye = eyes[0]
currEye2 = eyes2[1]
currIndex = 0
currIndex2 = 0

added = False

influence = pygame.image.load("Assets/influence.png")
hero1 = pygame.image.load("Assets/hero1.png")
hero2 = pygame.image.load("Assets/hero2.png")
hero3 = pygame.image.load("Assets/hero3.png")
whyshouldi = Objects.briefText(virtual_screen, Assets.whyshouldi, 15, 180, 3)

animationIndex = 0

animationTimer = Objects.timer(2.5, False)
lighterTimer = Objects.timer(1.5, False)

engineTimer = Objects.timer(3, False)
animationTimer2 = Objects.timer(1, False)

animation = []
for i in range(1, 18):
    animation.append(pygame.image.load(f"Assets/BadEndingCutscene{i}.png"))

endingScroll = pygame.image.load("Assets/EndingCutscene.png")
scrollSub = pygame.image.load("Assets/SubWhiteOutline.png")
scrollPos = -314
scrollTimer = Objects.timer(0.5, False)

cutscene1 = False
cutscene2 = False
brainwashPlayed = False
lighterPlayed = False
explosionPlayed = False
animate = False
scroll = False
eternityPlayed = False

smallEyesPositions = [
    (231, 40),
    (261, 91),
    (261, 141),
    (231, 177),
    (113, 177),
    (83, 141),
    (83, 91),
    (113, 40),
    (204, 53),      
    (237, 118),     
    (204, 168),     
    (140, 168), 
    (107, 118),
    (140, 53),
    (172, 72),
    (172, 151)
]

firstTime = pygame.time.get_ticks()
firstTime2 = pygame.time.get_ticks()
nextBlinkDelay = random.randint(3000, 5000)
nextBlinkDelay2 = random.randint(3000, 5000)

repairFuelLineTimer = Objects.timer(2, True)
playing = False

bounds = Polygon([(32,224),(0,287),(227,280),(453,247),(453,224)])

lit = False
light_pos = (70, 50)
light_pos2 = (240, 50)
wall_lights = [
    LightSource(light_pos[0], light_pos[1], radius=60, strength = 220),
    LightSource(light_pos2[0], light_pos2[1], radius=60, strength = 220)
]
falloff = [LightFalloff(virtual_screen.get_size(), darkness = 140)]

# load assets
background = pygame.image.load("Assets/SubRoom.png")
exitRect = pygame.Rect(4, 175, 21, 115)

# Fuel leak sound variables
fuel_leak_pos = (270, 226)
max_distance = 200  # Maximum distance where sound can be heard
fuel_sound_playing = False
base_volume = 0.8

# Track electrical tape equipping
last_equipped_item = None
evil_choice_played = False

fixed = False
explodeAttempt = False
leave = False

credits = False # True when time to go to credits

def inBounds(x, y):    
    if credits:
        print("Going to credits")
        return 1
    elif Player.cutscene:
        return False
    elif exitRect.collidepoint((x,y)):
        Sounds.whispers.stop()
        return 0
    elif not bounds.contains(Point(x,y)):
        return False
    return True

def check_electrical_tape_equip():
    """Function to check for electrical tape equipping even when inventory is open"""
    global last_equipped_item, evil_choice_played
    
    current_equipped = Player.equipped
    if current_equipped != last_equipped_item:
        if current_equipped is not None and hasattr(current_equipped, 'id') and current_equipped.id == "electricalTape":
            # Always play the sound, regardless of previous state
            try:
                Sounds.EvilChoice.play()  # Use the loaded sound object directly
                print("EvilChoice sound played!")  # Debug output
                evil_choice_played = True
            except Exception as e:
                print(f"Error playing EvilChoice sound: {e}")
        else:
            # Reset the flag when something else is equipped or nothing is equipped
            evil_choice_played = False
        last_equipped_item = current_equipped

def update_fuel_leak_sound():
    global fuel_sound_playing
    
    # distance between player and fuel leak
    distance = math.sqrt((player_pos.x - fuel_leak_pos[0])**2 + (player_pos.y - fuel_leak_pos[1])**2)
    
    if distance <= max_distance and not fixed:
        #volume based on distance
        volume = base_volume * (1 - (distance / max_distance))
        volume = max(0, min(1, volume))
        
        if not fuel_sound_playing:
            Sounds.FuelPipeLeaking.play(-1)  # Loop the sound
            fuel_sound_playing = True
        
        #Sounds.FuelPipeLeaking.set_volume(volume)
        Sounds.setVolume(Sounds.FuelPipeLeaking, volume)
    else:
        if fuel_sound_playing:
            Sounds.FuelPipeLeaking.stop()
            fuel_sound_playing = False

def positionDeterminer(cameFrom):
    global player_pos, added
    if not added:
        if Player.events != 0:
            Player.events += 1
        added = True
    if cameFrom == "Rooms.YellowHallway":
        Sounds.whispers.play(-1)
        player_pos = pygame.Vector2(exitRect.centerx + 35, exitRect.centery + 25)

def Room(screen, screen_res, events):
    global firstTime, currIndex, nextBlinkDelay, currEye, firstTime2, currIndex2, currEye2, nextBlinkDelay2, smallEyesPositions, fixed, explodeAttempt, leave, cutscene1, cutscene2, \
        animationIndex, lighterPlayed, explosionPlayed, brainwashPlayed, playing, animate, scroll, scrollPos, eternityPlayed, credits
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    
    update_fuel_leak_sound()

    currTime = pygame.time.get_ticks()
    if Sounds.whispers.get_num_channels() == 0:
        Sounds.whispers.play(-1)
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if fuelLineInteractRect.collidepoint(player_pos) and Player.checkItem(Items.electricalTape) and not fixed:
                    if Player.events != 7:
                        fixed = True
                        Sounds.tape.play()
                    else:
                        whyshouldi.activated_time = pygame.time.get_ticks()
                elif fuelLineInteractRect.collidepoint(player_pos) and Player.checkItem(Items.lighter) and not (cutscene1 or cutscene2) and not fixed:
                    if Player.events != 7:
                        explodeAttempt = True
                        Player.cutscene = True
                        animationTimer.setInitial()
                        virtual_screen2.blit(influence, (0,0))
                        Sounds.brainwash.play()
                        if Player.events == 0:
                            Player.ending = "hero"
                            cutscene1 = True
                        else:
                            cutscene2 = True
                    else:
                        whyshouldi.activated_time = pygame.time.get_ticks()
                elif consoleInteractRect.collidepoint(player_pos):
                    if fixed:
                        Player.cutscene = True
                        Player.ending = "evil"
                        Sounds.whispers.stop()
                        Sounds.whatAwaits.stop()
                        Sounds.ominousAmb.stop()
                        Sounds.engineStartup.play()
                        engineTimer.setInitial()
                    elif not playing:
                        Sounds.RepairFuelLine.play()
                        playing = True
                        repairFuelLineTimer.setInitial()

    virtual_screen.blit(background, (0,0))
    virtual_screen3.fill("black")
    virtual_screen4.blit(endingScroll, (0, scrollPos))
    virtual_screen4.blit(scrollSub, (0,-314))

    if fixed:
        virtual_screen.blit(fuelLineFixed, fuelLinePos)
        virtual_screen.blit(puddle, puddlePos)
    else:
        virtual_screen.blit(fuelLine, fuelLinePos)
        virtual_screen.blit(puddle, puddlePos)
        virtual_screen.blit(puddleUpper, puddleUpperPos)


    if (currTime - firstTime2 >= nextBlinkDelay2) and not Player.cutscene:
            currIndex2 = (currIndex2 + 1) % len(eyes2)
            currEye2 = eyes2[currIndex2] # sets current eye for animation in array
            firstTime2 = currTime
            if currIndex2 == 1: # closed eye
                nextBlinkDelay2 = random.randint(70, 120)
                Sounds.blink.play()
            else: # open eye
                nextBlinkDelay2 = random.randint(2000, 5000)
    for position in smallEyesPositions:    
        virtual_screen.blit(currEye2, position, eye_rect2)

    if (currTime - firstTime >= nextBlinkDelay) and not Player.cutscene:
        currIndex = (currIndex + 1) % len(eyes)
        currEye = eyes[currIndex] # sets current eye for animation in array
        firstTime = currTime
        if currIndex == 1: # closed eye
            nextBlinkDelay = random.randint(70, 120)
            Sounds.blink.play()
        else: # open eye
            nextBlinkDelay = random.randint(2000, 5000)
    virtual_screen.blit(currEye, (130, 80), eye_rect)           

    Player.animatePlayer(virtual_screen, player_pos)

    apply_lighting(virtual_screen, wall_lights, darkness=10, ambient_color=(50, 50, 50), ambient_strength=10)
    apply_falloff(falloff, virtual_screen, light_pos)

    if animationTimer.Done() and cutscene1:
        if animationIndex == 0:
            virtual_screen2.blit(hero1, (0,0))
        elif animationIndex == 1:
            virtual_screen2.blit(hero2, (0,0))
        elif animationIndex == 2:
            lighterTimer.setInitial()
            virtual_screen2.blit(hero3, (0,0))
        else:
            if not explosionPlayed:
                Sounds.brainwash.stop()
                Sounds.whispers.stop()
                Sounds.explosion2.play()
                explosionPlayed = True
                Sounds.FuelPipeLeaking.stop()
                Sounds.whatAwaits.stop()
                Sounds.ominousAmb.stop()
                virtual_screen2.fill("black")
                engineTimer.setInitial()
        animationIndex += 1
        animationTimer.reset()
        animationTimer.setInitial()

    if lighterTimer.Done() and not lighterPlayed:
        Sounds.lighter.play()
        Sounds.screech.play()
        lighterPlayed = True

    if animationTimer.Done() and cutscene2 and explodeAttempt:
        Sounds.brainwash.stop()
        explodeAttempt = False
        Player.cutscene = False

    if repairFuelLineTimer.Done():
        playing = False

    if engineTimer.Done() and explosionPlayed:
        Sounds.loadMusic("Audio/Europa.wav")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1) 
        credits = True
    elif engineTimer.Done() and not leave:
        engineTimer.reset()
        engineTimer.setInitial()
        leave = True

    if engineTimer.Done() and leave and not eternityPlayed:
        Sounds.facingEternity.play()
        scrollTimer.setInitial()
        eternityPlayed = True
        scroll = True

    if animationIndex < 16:
        if animationTimer2.Done():
            if animationIndex == 0:
                Sounds.bubbles.play(-1)
            if animationIndex == 6:
                Sounds.setVolume(Sounds.bunsen, 0.7)
                Sounds.bunsen.play()
            if animationIndex == 8:
                Sounds.accessGranted.play()
            if animationIndex == 9:
                Sounds.DestinationEarth.play()
            if animationIndex == 10:
                Sounds.setVolume(Sounds.bunsen, 1)
                Sounds.setVolume(Sounds.EvilChoice, 1)
                Sounds.EvilChoice.play()
            if animationIndex == 12:
                Sounds.bunsen.stop()
                Sounds.blastoff.play()
            if animationIndex == 15:
                Sounds.bubbles.stop()
            animationIndex += 1
            animationTimer2.reset()
            animationTimer2.setInitial()

    if animationTimer2.Done() and animationIndex == 16 and animate:
        animate = False
        Sounds.EvilChoice.stop()
        Sounds.setVolume(Sounds.facingEternity, 0.6)
        credits = True

    whyshouldi.update()

    if animate:
        virtual_screen3.blit(animation[animationIndex], (0,0))

    if scrollPos < -200:
        if scrollTimer.Done():
            scrollPos += 1
            scrollTimer.reset()
            scrollTimer.setInitial()
    else:
        scroll = False
        animationTimer2.setInitial()
        animate = True
        Sounds.setVolume(Sounds.facingEternity, 0.5)

    if explodeAttempt:
        Assets.scaled_draw(virtual_res2, virtual_screen2, screen_res, screen)
    elif scroll:
        Assets.scaled_draw(virtual_res4, virtual_screen4, screen_res, screen)
    elif leave:
        Assets.scaled_draw(virtual_res3, virtual_screen3, screen_res, screen)
    else:
        Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 3.5, 3.5  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
