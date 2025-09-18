import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import random

virtual_res = (750,500)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

exit = False

beakerPuzzle = [
    [0,2,0,0],
    [0,0,0,4],
    [0,0,3,0],
    [1,0,0,0]
]

beakerSolution = [
    [4,2,1,3],
    [3,1,2,4],
    [2,4,3,1],
    [1,3,4,2]
]

beakerCase = pygame.image.load("Assets/beakerPuzzle.png")
caseWidth = beakerCase.get_width()*3.3
caseHeight = beakerCase.get_height()*3.3
beakerCaseScale = pygame.transform.scale(beakerCase, (caseWidth, caseHeight))
beakerTiles = Assets.load_tileset("Assets/beakerTiles.png", 29, 29)
reset = pygame.image.load("Assets/reset.png")
beakerSolved = pygame.image.load("Assets/beakerSolved.png")
letter = pygame.transform.scale(Assets.letterTiles[0], (20,34))
letterRect = pygame.Rect(360, 233, 20, 34)

i = 0
for beaker in beakerTiles:
    beakerTiles[i] = pygame.transform.scale(beaker, (98,98))
    i += 1

resetBounds = Polygon([(370,225), (345, 250), (370, 275), (395, 250)])

class beakerTile:
    def __init__(self, row, col, rect):
        self.row = row
        self.col = col
        self.rect = rect
        self.state = 0

    def update(self):
        if self.state == 4:
            self.state = 0
        else:
            self.state += 1
        beakerPuzzle[self.row][self.col] = self.state

    def isClicked(self, pos):
        return self.rect.collidepoint(pos)

beakers = [
    beakerTile(0,0, pygame.Rect(161,43,98,98)),
    beakerTile(0,2, pygame.Rect(372,43,98,98)),
    beakerTile(0,3, pygame.Rect(474,43,98,98)),
    beakerTile(1,0, pygame.Rect(161,145,98,98)),
    beakerTile(1,1, pygame.Rect(263,145,98,98)),
    beakerTile(1,2, pygame.Rect(372,145,98,98)),
    beakerTile(2,0, pygame.Rect(161,254,98,98)),
    beakerTile(2,1, pygame.Rect(263,254,98,98)),
    beakerTile(2,3, pygame.Rect(474,254,98,98)),
    beakerTile(3,1, pygame.Rect(263,356,98,98)),
    beakerTile(3,2, pygame.Rect(372,356,98,98)),
    beakerTile(3,3, pygame.Rect(474,356,98,98))
]

solved = False
collected = False

def inBounds(x, y):
    global exit
    if exit:
        exit = False
        return 0
    return False

def positionDeterminer(cameFrom):
    pass

def Room(screen, screen_res, events):
    global exit, solved, beakerPuzzle, collected
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    level, power = Objects.getPipeDungeonInfo()
    upperWingPower, _ = Objects.getPinkWingInfo()
    lit = upperWingPower and level == 1 and power

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_pos = (mouse_x/xScale, mouse_y/yScale)
                if not solved:
                    if resetBounds.contains(Point(mouse_pos)):
                        for beaker in beakers:
                            beaker.state = 0
                    else:
                        for beaker in beakers:
                            if beaker.isClicked(mouse_pos):
                                beaker.update()
                                if beaker.state != 0:
                                    glassRand = random.randint(0,1)
                                    Sounds.glass[glassRand].play()
                                solved = True
                                for beaker in beakers:
                                    #print(beaker.row, beaker.col, ":", beaker.state, beakerSolution[beaker.row][beaker.col])
                                    if beaker.state != beakerSolution[beaker.row][beaker.col]:
                                        solved = False
                                if solved:
                                    Sounds.letter.play()
                elif letterRect.collidepoint(mouse_pos):
                    Sounds.letter.play()
                    collected = True

                    
    virtual_screen.fill((195, 195, 195))
    dark_overlay.fill((0, 0, 0, 150))

    Assets.punch_light_hole(virtual_screen, dark_overlay, (virtual_screen.get_width()/2, virtual_screen.get_height()/2), 500, (100, 0, 100))

    virtual_screen.blit(beakerCaseScale, (137, 18))

    for beaker in beakers:
        if beaker.state != 0:
            virtual_screen.blit(beakerTiles[beaker.state-1], beaker.rect)

    if not solved:
        virtual_screen.blit(reset, (345,225))
    else:
        virtual_screen.blit(beakerSolved, (345,225))
        if not collected:
            virtual_screen.blit(letter, letterRect)

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale