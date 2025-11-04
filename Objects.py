import pygame
import Assets
import Area
import Sounds
import Items
import Player

class groundItem:
    def __init__(self, xpos, ypos, item):
        self.x = xpos
        self.y = ypos
        self.item = item
        self.rect = item.ground_sprite.get_rect(topleft=(xpos, ypos))
        self.collected = False

    def check_collision(self, player_pos):
        in_range = (self.x - 8 < player_pos.x < self.x + 8) and (self.y - 8 < player_pos.y < self.y + 8)

        if in_range and not self.collected:
            if (Player.addItem(self.item)):
                self.collected = True
            else:
                print("Inventory is full!")
                # TODO: Add proper inventory is full msg

    def draw(self, virtual_screen):
        if (self.collected == False):
            virtual_screen.blit(self.item.ground_sprite, self.rect)

class Valve:
    def __init__(self, xpos, ypos, action):
        self.x = xpos
        self.y = ypos
        self.image = Assets.valveSprites[0]
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
        self.activated_time = -1
        self.action = action

    def check_collision(self, player_pos):
        in_range = (self.x - 8 < player_pos.x < self.x + 40) and (self.y - 8 < player_pos.y < self.y + 40)

        if in_range and self.activated_time == -1:
            Sounds.valveSound.play()
            self.image = Assets.valveSprites[1]
            self.action()
            self.activated_time = pygame.time.get_ticks()

    def update(self):
        if self.activated_time != -1:
            seconds = (pygame.time.get_ticks() - self.activated_time) / 1000

            if seconds > 0.25:
                self.image = Assets.valveSprites[0]
                self.activated_time = -1

class TopDownValve:
    def __init__(self, xpos, ypos, action):
        self.x = xpos
        self.y = ypos
        self.image = Assets.topDownValveSprites[0]
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
        self.activated_time = -1
        self.action = action

    def check_collision(self, player_pos):
        in_range = (self.x - 8 < player_pos.x < self.x + 40) and (self.y - 8 < player_pos.y < self.y + 40)

        if in_range and self.activated_time == -1:
            Sounds.valveSound.play()
            self.image = Assets.topDownValveSprites[1]
            self.action()
            self.activated_time = pygame.time.get_ticks()

    def update(self):
        if self.activated_time != -1:
            seconds = (pygame.time.get_ticks() - self.activated_time) / 1000

            if seconds > 0.25:
                self.image = Assets.topDownValveSprites[0]
                self.activated_time = -1

class Light:
    def __init__(self, xpos, ypos, type):
        self.x = xpos
        self.y = ypos
        self.image = Assets.dimTiles[type]
        self.type = type
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
        if type == 1:
            self.color = (255, 0, 255)
        elif type == 2:
            self.color = (0, 162, 232)
        elif type == 3:
            self.color = (181, 230, 29)
        elif type == 4:
            self.color = (255, 201, 14)

    def update(self):
        level, power = Area.getPipeDungeonInfo()
        if (level == self.type and power) or (self.type == 1 and Area.getPinkPower()):
            self.image = Assets.tiles[self.type]
            return True
        else:
            self.image = Assets.dimTiles[self.type]
            return False
        
class SquishedLight:
    def __init__(self, xpos, ypos, type):
        self.x = xpos
        self.y = ypos
        self.image = Assets.squishedDimTiles[type]
        self.type = type
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
        if type == 1:
            self.color = (255, 0, 255)
        elif type == 2:
            self.color = (0, 162, 232)
        elif type == 3:
            self.color = (181, 230, 29)
        elif type == 4:
            self.color = (255, 201, 14)

    def update(self):
        level, power = Area.getPipeDungeonInfo()
        if (level == self.type and power) or (self.type == 1 and Area.getPinkPower()):
            self.image = Assets.squishedTiles[self.type]
            return True
        else:
            self.image = Assets.squishedDimTiles[self.type]
            return False

class Door:
    def __init__(self, xpos, ypos, image):
        self.x = xpos
        self.y = ypos
        self.image = image
        self.rect = self.image.get_rect(topleft=(xpos, ypos))

class briefText:
    def __init__(self, screen, image, xpos, ypos, time):
        self.x = xpos
        self.y = ypos
        self.image = image
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
        self.screen = screen
        self.activated_time = -1
        self.time = time

    def update(self):
        if self.activated_time != -1:
            self.screen.blit(self.image, self.rect)
            seconds = (pygame.time.get_ticks() - self.activated_time) / 1000

            if seconds > self.time:
                self.activated_time = -1
                
class timer:
    def __init__(self, seconds, repeat):
        self.initial_time = -1
        self.seconds = seconds
        self.repeat = repeat

    def setInitial(self):
        if self.initial_time == -1:
            self.initial_time = pygame.time.get_ticks()

    def Done(self):
        if self.initial_time != -1:
            currentTime = (pygame.time.get_ticks() - self.initial_time) / 1000
            if currentTime < self.seconds:
                return False
            if self.repeat:
                self.initial_time = -1
            return True
        
class Code():
    def __init__(self, x, y):
        self.state = 0
        self.rect = pygame.Rect(x,y,21,41)

# Same getter functions for getting information about rooms the player isn't currently in that are in Area.py. 
# Rooms can't call the functions directly in Area.py due to circular import, so passing them to here is a workaround. 
# Call these functions when in a room file, not the ones in Area.py.
def getPipeDungeonInfo():
    return Area.getPipeDungeonInfo()

def getPinkWingInfo():
    return Area.getPinkWingInfo()

def getCutscene():
    return Area.getCutscene()

def getTriangleSolved():
    return Area.getTriangleSolved()

def getBeakerSolved():
    return Area.getBeakerSolved()

def getSpotDiffsSolved():
    return Area.getSpotDiffsSolved()

def getColorsFound():
    return Area.getColorsFound()

def getColorsPlaced():
    return Area.getColorsPlaced()

def getSelected():
    return Area.getSelected()

def getLetterCount():
    return Area.getLetterCount()

def getOpen():
    return Area.getOpen()

def getPinkPower():
    return Area.getPinkPower()

def getBluePower():
    return Area.getBluePower()

def getWaterLevelsSolved():
    return Area.getWaterLevelsSolved()

def getBreakerSolved():
    return Area.getBreakerSolved()

def RepairWire():
    return Area.RepairWire()

def getWireRepaired():
    return Area.getWireRepaired()