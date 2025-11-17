import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import random
import Player
import Items

virtual_res = (213, 134)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

background = pygame.image.load("Assets/mscopetablezoom.png")
background2 = pygame.image.load("Assets/mscopetablezoomOn.png")
opendrawer = pygame.image.load("Assets/opendrawer.png")
redpetri = pygame.image.load("Assets/redpetri.png")
redRect = pygame.Rect(81, 56, 13, 8)
yellowpetri = pygame.image.load("Assets/yellowpetri.png") 
yellowRect = pygame.Rect(102, 51, 13, 8)
bluepetri = pygame.image.load("Assets/bluepetri.png") 
blueRect = pygame.Rect(97, 63, 13, 8)
tableRect = pygame.Rect(15,48,184,31)
emptyBeaker = pygame.image.load("Assets/EmptyBeaker.png")
beakerLiquidOriginal = pygame.image.load("Assets/BeakerLiquid.png")
explosion = pygame.image.load("Assets/explosion.png")
beakerLiquid = beakerLiquidOriginal.copy()
beakerLiquidTint = (0, 0, 0, 100)

# Used for flame animation when bunsen burner on
flame1 = pygame.image.load("Assets/BunsenBurnerFire.png")
flame2 = pygame.image.load("Assets/BunsenBurnerFire2.png")
flame = [flame1, flame2]
firstTime = pygame.time.get_ticks()
currIndex = 0
currFlame = flame[0]
bunsenRect = pygame.Rect(143, 30, 30, 42)
switchRect = pygame.Rect(148, 62, 5, 5)

redPlaced = False
yellowPlaced = False
bluePlaced = False
bunsenOn = False
explosionHappening = False
correctIngredients = False
amountFilled = 0
herbicideIngredients = {"leaf": 0, "bleach": 0, "benzene": 0, "mercury": 0}

Cover = pygame.Surface((13, 8))
Cover.fill((127,127,127))
msRect = pygame.Rect(54,44,13,8)

MSRect = pygame.Rect(40,24,32,43)

beakerLiquidRect = pygame.Rect(0, 0, 0, 0)

exit = False
luckyNumber = random.randint(1,12)
luckyNumber2 = luckyNumber
while luckyNumber2 == luckyNumber:
    luckyNumber2 = random.randint(1,12)
redFound = False
selected = "None"
microscope = False

drawerTimer = Objects.timer(0.5, False)

class Drawer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 36, 12)
        self.state = "closed"

drawers = []
for y in range(3):
    for x in range(4):
        drawers.append(Drawer(33+(37*x), 90+(13*y)))

luckyRect = pygame.Rect(drawers[luckyNumber-1].rect.x+14, drawers[luckyNumber-1].rect.y, 11,5)
benzene = Objects.groundItem(drawers[luckyNumber2 - 1].x + 12, drawers[luckyNumber2 - 1].y, Items.benzene)

def inBounds(x, y):
    global exit, microscope
    if exit:
        exit = False
        return 0
    elif microscope:
        microscope = False
        return 1
    return False

def positionDeterminer(cameFrom):
    if cameFrom == "Rooms.PinkUpperWing":
        if bunsen and on:
            Sounds.bunsen.set_volume(.45)
            Sounds.bunsen.play(loops = -1)

def Room(screen, screen_res, events):
    global exit, redFound, visible, visible2, selected, microscope, redPlaced, yellowPlaced, bluePlaced, bunsenOn, firstTime, currIndex, currFlame, beakerLiquidTint, beakerLiquidRect, amountFilled, beakerLiquid, herbicideIngredients, explosionHappening, correctIngredients
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    level, power = Objects.getPipeDungeonInfo()
    upperWingPower, _ = Objects.getPinkWingInfo()
    lit = upperWingPower and level == 1 and power
    currTime = pygame.time.get_ticks()

    visible = False
    visible2 = False
    virtual_screen.fill((195, 195, 195))
    dark_overlay.fill((0, 0, 0, 150))

    Assets.punch_light_hole(virtual_screen, dark_overlay, (virtual_screen.get_width()/2, virtual_screen.get_height()/2), 500, (0, 0, 0))

    virtual_screen.blit(background, (0,0))
    if drawers[luckyNumber - 1].state == "open":
        above = luckyNumber - 5
        if above >= 0:
            if drawers[above].state == "closed":
                visible = True
        else:
            visible = True
    if drawers[luckyNumber2 - 1].state == "open":
        above = luckyNumber2 - 5
        if above >= 0:
            if drawers[above].state == "closed":
                visible2 = True
        else:
            visible2 = True
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                Sounds.bunsen.stop()
                exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_pos = (mouse_x/xScale, mouse_y/yScale)
                print(mouse_pos)
                mouse_pos_vec = pygame.Vector2(mouse_x/xScale, mouse_y/yScale)
                # player clicks red petri
                if visible2 and benzene.check_collision(mouse_pos_vec):
                    Sounds.pickup.play()
                elif luckyRect.collidepoint(mouse_pos) and not redFound and visible:           
                    if (Player.addItem(Items.redPetri)):
                        Sounds.glass1.play()
                        redFound = True
                elif redRect.collidepoint(mouse_pos) and redPlaced:
                    selected = "Red"
                elif yellowRect.collidepoint(mouse_pos) and yellowPlaced:
                    selected = "Yellow"
                elif blueRect.collidepoint(mouse_pos) and bluePlaced:
                    selected = "Blue"
                elif bunsenRect.collidepoint(mouse_pos):
                    # turns on bunsen burner if lighter equipped
                    if not bunsenOn:
                        if Player.checkItem(Items.lighter):
                            Sounds.lighter.play()
                            pygame.time.delay(1200)
                            Sounds.bunsen.set_volume(0.45)
                            Sounds.bunsen.play(loops = -1)
                            bunsenOn = True
                    # adds ingredient to beaker
                    else:
                        if Player.checkItem(Items.bleach):
                            herbicideIngredients["bleach"] = amountFilled + 1
                            beakerLiquidTint = (40, 40, 40, 100)
                            beakerLiquid.fill(beakerLiquidTint, special_flags=pygame.BLEND_ADD)
                            Sounds.pour.play()
                        elif Player.checkItem(Items.hogweedLeaf):
                            herbicideIngredients["leaf"] = amountFilled + 1
                            beakerLiquidTint = (150, 0, 150, 120)
                            beakerLiquid.fill(beakerLiquidTint, special_flags=pygame.BLEND_SUB)
                            Sounds.plop.play()
                        elif Player.checkItem(Items.brokenThermometer):
                            herbicideIngredients["mercury"] = amountFilled + 1
                            beakerLiquidTint = (0, 150, 150, 120)
                            beakerLiquid.fill(beakerLiquidTint, special_flags=pygame.BLEND_SUB)
                            Sounds.pour.play()
                        elif Player.checkItem(Items.benzene):
                            herbicideIngredients["benzene"] = amountFilled + 1
                            beakerLiquidTint = (40, 40, 40, 100)
                            beakerLiquid.fill(beakerLiquidTint, special_flags=pygame.BLEND_ADD)
                            Sounds.pour.play()
                        else:
                            break
                        amountFilled += 1
                        if herbicideIngredients == {"bleach": 3, "leaf": 1, "benzene": 2, "mercury":4}:
                            correctIngredients = True
                        elif (amountFilled == 4):
                            explosionHappening = True
                        beakerLiquidRect = pygame.Rect(0, beakerLiquid.get_height() - amountFilled * 2 - 2, beakerLiquid.get_width(),  amountFilled * 2)

                elif msRect.collidepoint(mouse_pos):
                    if Player.checkItem(Items.redPetri):
                        Player.removeItem(Items.redPetri)
                        redPlaced = True
                        selected = "Red"
                    elif Player.checkItem(Items.yellowPetri):
                        Player.removeItem(Items.yellowPetri)
                        yellowPlaced = True
                        selected = "Yellow"
                    elif Player.checkItem(Items.bluePetri):
                        Player.removeItem(Items.bluePetri)
                        bluePlaced = True
                        selected = "Blue"
                    else:
                        selected = "None"

                    print(selected)
                elif tableRect.collidepoint(mouse_pos):
                    # TODO: add "Place petri dishes?" prompt or smth
                    if Player.checkItem(Items.redPetri):
                        Player.removeItem(Items.redPetri)
                        redPlaced = True
                    if Player.checkItem(Items.yellowPetri):
                        Player.removeItem(Items.yellowPetri)
                        yellowPlaced = True
                    if Player.checkItem(Items.bluePetri):
                        Player.removeItem(Items.bluePetri)
                        bluePlaced = True
                elif MSRect.collidepoint(mouse_pos) and selected != "None":
                    microscope = True
                else:
                    for drawer in drawers:
                        if drawer.rect.collidepoint(mouse_pos):
                            if drawer.state == "closed":
                                Sounds.drawerclose.stop()
                                Sounds.draweropen.play()
                                drawer.state = "open"
                                drawer.rect.y += 4
                            else:
                                Sounds.draweropen.stop()
                                Sounds.drawerclose.play()
                                drawer.state = "closed"
                                drawer.rect.y -= 4
                            break
          

    count = 12
    for drawer in reversed(drawers):
        if drawer.state == "open":
            virtual_screen.blit(opendrawer, (drawer.rect.x, drawer.rect.y-4))
            if count == luckyNumber and not redFound and visible:
                virtual_screen.blit(redpetri, luckyRect, area=pygame.Rect(0, 0, 11, 5))
            elif count == luckyNumber2 and not benzene.collected and visible2:
                Objects.groundItem.draw(benzene, virtual_screen)
        count -= 1

    if not redPlaced or selected == "Red":
        virtual_screen.blit(Cover, redRect)
        if selected == "Red":
            virtual_screen.blit(redpetri, msRect)
    if not yellowPlaced or selected == "Yellow":
        virtual_screen.blit(Cover, yellowRect)
        if selected == "Yellow":
            virtual_screen.blit(yellowpetri, msRect)
    if not bluePlaced or selected == "Blue":
        virtual_screen.blit(Cover, blueRect)
        if selected == "Blue":
            virtual_screen.blit(bluepetri, msRect)
    if bunsen and on:
        if (currTime - firstTime >= 30):
                currIndex = (currIndex + 1) % len(flame)
                currFlame = flame[currIndex] # sets current flame for animation in array
                firstTime = currTime
        virtual_screen.blit(currFlame, (155, 47))
    if correctIngredients:
        beakerLiquidRect = pygame.Rect(0, beakerLiquid.get_height() - amountFilled * 2 - 2, beakerLiquid.get_width(),  amountFilled * 2)
        virtual_screen.blit(beakerLiquidOriginal, (149, 30))
        virtual_screen.blit(beakerLiquid, (149, 30 + (14 - (amountFilled * 2))), beakerLiquidRect)
        virtual_screen.blit(emptyBeaker, (149, 29))
        scaled = pygame.transform.scale(virtual_screen, screen_res)
        screen.blit(scaled, (0, 0))
        pygame.display.flip()
        pygame.time.delay(1000)
        Sounds.pickup.play()
        Player.addItem(Items.herbicide)
        correctIngredients = False
    elif explosionHappening:
        virtual_screen.blit(beakerLiquidOriginal, (149, 30))
        virtual_screen.blit(beakerLiquid, (149, 30 + (14 - (amountFilled * 2))), beakerLiquidRect)
        virtual_screen.blit(emptyBeaker, (149, 29))
        scaled = pygame.transform.scale(virtual_screen, screen_res)
        screen.blit(scaled, (0, 0))
        pygame.display.flip()
        pygame.time.delay(1000)
        virtual_screen.blit(explosion, (137, 20))
        Sounds.explosion.play()
        scaled = pygame.transform.scale(virtual_screen, screen_res)
        screen.blit(scaled, (0, 0))
        pygame.display.flip()
        pygame.time.delay(1000)
        herbicideIngredients = {"leaf": 0, "bleach": 0, "benzene": 0, "mercury": 0}
        amountFilled = 0
        beakerLiquid = beakerLiquidOriginal.copy()
        beakerLiquidRect = pygame.Rect(0, beakerLiquid.get_height() - amountFilled * 2 - 2, beakerLiquid.get_width(),  amountFilled * 2)
        explosionHappening = False
    if (amountFilled != 4):
        virtual_screen.blit(beakerLiquidOriginal, (149, 30))
        virtual_screen.blit(beakerLiquid, (149, 30 + (14 - (amountFilled * 2))), beakerLiquidRect)
        virtual_screen.blit(emptyBeaker, (149, 29))
    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale