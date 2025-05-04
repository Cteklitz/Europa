import pygame
import Assets
import Area

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
            self.image = Assets.valveSprites[1]
            self.action()
            self.activated_time = pygame.time.get_ticks()

    def update(self):
        if self.activated_time != -1:
            seconds = (pygame.time.get_ticks() - self.activated_time) / 1000

            if seconds > 0.25:
                self.image = Assets.valveSprites[0]
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
        if level == self.type and power:
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
        if level == self.type and power:
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
    def __init__(self, screen, image, xpos, ypos):
        self.x = xpos
        self.y = ypos
        self.image = image
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
        self.screen = screen
        self.activated_time = -1

    def update(self):
        if self.activated_time != -1:
            self.screen.blit(self.image, self.rect)
            seconds = (pygame.time.get_ticks() - self.activated_time) / 1000

            if seconds > 3:
                self.activated_time = -1

def getPipeDungeonInfo():
        return Area.getPipeDungeonInfo()

def getPinkWingInfo():
        return Area.getPinkWingInfo()