# Example file showing a circle moving on screen
import pygame
import Assets

pipePuzzle = [
    [2,1,2,6,6],
    [6,4,1,2,5],
    [6,5,0,3,3],
    [3,1,4,5,6],
    [5,2,4,6,4]
]

activeSquares = [
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]
]

pinkSquares = [
    [0,0,0,0,0],
    [0,0,0,0,0],
    [1,1,0,1,0],
    [0,1,1,1,0],
    [0,0,0,0,0]
]

blueSquares = [
    [0,0,0,2,0],
    [0,0,2,0,0],
    [0,0,0,0,0],
    [2,0,0,0,0],
    [2,2,2,0,0]
]

greenSquares = [
    [3,3,0,0,0],
    [3,0,3,3,0],
    [3,0,3,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]
]

orangeSquares = [
    [0,4,0,0,4],
    [0,4,0,0,4],
    [0,0,0,0,4],
    [0,0,0,0,0],
    [4,0,0,4,4]
]

solution = {
    (0, 2): 2,
    (1, 0): 4,
    (1, 1): 5,
    (1, 2): 2,
    (2, 0): 6,
    (2, 1): 3,
    (2, 3): 5,
    (2, 4): 4,
    (3, 0): 4,
    (3, 1): 1,
    (3, 2): 6,
    (3, 3): 3,
    (3, 4): 6,
    (4, 0): 3,
    (4, 1): 1,
    (4, 2): 5
}

solved = False

def checkSolution(pipePuzzle, solution):
    global solved, activeSquares, power
    for (row, col), correct_value in solution.items():
        if pipePuzzle[row][col] != correct_value:
            return
    solved = True
    power = True
    activeSquares = [
        [0,0,level,0,0],
        [level,level,level,0,0],
        [level,level,level,level,level],
        [level,level,level,level,level],
        [level,level,level,0,0]
    ]


def rotatePipes(pipePuzzle):
    changed = False
    for row in range(5):
        for col in range(5):
            if activeSquares[row][col] != 0:
                changed = True
                val = pipePuzzle[row][col]
                if val == 1:
                    pipePuzzle[row][col] = 2
                elif val == 2:
                    pipePuzzle[row][col] = 1
                elif val == 3:
                    pipePuzzle[row][col] = 4
                elif val == 4:
                    pipePuzzle[row][col] = 5
                elif val == 5:
                    pipePuzzle[row][col] = 6
                elif val == 6:
                    pipePuzzle[row][col] = 3

    return changed

TILE_W, TILE_H = 32, 32

def draw_map(screen, tiles, map_data, xpos, ypos):
    for row_idx, row in enumerate(map_data):
        for col_idx, tile_idx in enumerate(row):
            tile_surf = tiles[tile_idx]
            x = xpos + col_idx * TILE_W
            y = ypos + row_idx * TILE_H
            screen.blit(tile_surf, (x, y))

pipeSound = pygame.mixer.Sound("Audio/pipe.wav")
valveSound = pygame.mixer.Sound("Audio/valve.wav")
switchSound = pygame.mixer.Sound("Audio/switch.wav")

class Valve:
    def __init__(self, xpos, ypos, action):
        self.x = xpos
        self.y = ypos
        self.image = Assets.valveSprites[0]
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
        self.activated_time = -1
        self.action = action

    def check_collision(self, player_pos, solved):
        in_range = (self.x - 8 < player_pos.x < self.x + 40) and (self.y - 8 < player_pos.y < self.y + 40)

        if in_range and self.activated_time == -1:
            valveSound.play()
            self.image = Assets.valveSprites[1]
            if not solved:
                changed = rotatePipes(pipePuzzle)
                if changed:
                    pipeSound.play()
                checkSolution(pipePuzzle, solution)
            else:
                self.action()
            self.activated_time = pygame.time.get_ticks()

    def update(self):
        if self.activated_time != -1:
            seconds = (pygame.time.get_ticks() - self.activated_time) / 1000

            if seconds > 0.25:
                self.image = Assets.valveSprites[0]
                self.activated_time = -1

class Switch:
    def __init__(self, xpos, ypos, sprite, active):
        self.x = xpos
        self.y = ypos
        self.tileset = sprite
        self.active = active
        self.image = sprite[0]
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
    
    def check_collision(self, player_pos):
        global activeSquares, level
        in_range = (self.x - 8 < player_pos.x < self.x + 40) and (self.y - 8 < player_pos.y < self.y + 40)
        if in_range:
            switchSound.play()
            if self.image == self.tileset[0]:
                self.image = self.tileset[1]
                if not solved:
                    activeSquares = self.active
                else:
                    for key, value in switches.items():
                        if value == self:
                            level = key
                            break
                    activeSquares = [
                        [0,0,level,0,0],
                        [level,level,level,0,0],
                        [level,level,level,level,level],
                        [level,level,level,level,level],
                        [level,level,level,0,0]
                    ]
            elif self.image == self.tileset[1]:
                level = 0
                self.image = self.tileset[0]
                activeSquares = [[0 for _ in range(5)] for _ in range(5)]
            return True
        return False
    
def inBounds(x, y):
    if y > 384:
        pygame.mixer.music.stop()
        return 0
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

virtual_res = (352, 384)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)
dark_overlay.fill((0, 0, 0, 50))

player_pos = pygame.Vector2(175, 340)

level = 0
power = False

def changePower():
    global power
    if power == False:
        power = True
    else:
        power = False

valve = Valve(160, 288, changePower)
switches = {
    1: Switch(64, 224, Assets.pinkSwitch, pinkSquares),
    2: Switch(128, 224, Assets.blueSwitch, blueSquares),
    3: Switch(192, 224, Assets.greenSwitch, greenSquares),
    4: Switch(256, 224, Assets.orangeSwitch, orangeSquares),
}

floor = pygame.image.load("Assets/floor.png")

def positionDeterminer(cameFrom):
    global player_pos
    player_pos = pygame.Vector2(175, 340)

def Room(screen, screen_res, events):
    global level, floor

    # poll for events
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                valve.check_collision(player_pos, solved)
                for key, switch in switches.items():
                    pressed = switch.check_collision(player_pos)
                    if pressed and switch.image == switch.tileset[1]:
                        level = key
                        for switch2 in switches.values():
                            if switch2 != switch:
                                switch2.image = switch2.tileset[0]

    # fill the screen with a color to wipe away anything from last frame
    virtual_screen.fill("gray")
    virtual_screen.blit(floor, (0, 256))
    pygame.draw.line(virtual_screen, (0,0,0), (64, 0), (64, 256), 1)
    pygame.draw.line(virtual_screen, (0,0,0), (288, 0), (288, 256), 1)
    draw_map(virtual_screen, Assets.tiles, activeSquares, 96, 32)
    draw_map(virtual_screen, Assets.pipes, pipePuzzle, 96, 32)

    valve.update()
    virtual_screen.blit(Assets.pipes[7], (160,0))
    for y in range(192, 384, 32):
        virtual_screen.blit(Assets.pipes[7], (160, y))
    virtual_screen.blit(Assets.pipes[10], (64,96))
    virtual_screen.blit(Assets.pipes[10], (256,96))
    virtual_screen.blit(Assets.pipes[8], (32,96))
    virtual_screen.blit(Assets.pipes[9], (288,96))
    
    for switch in switches.values():
        virtual_screen.blit(switch.image, switch.rect)

    if player_pos.y > 300:
        virtual_screen.blit(valve.image, valve.rect)
        pygame.draw.circle(virtual_screen, "red", player_pos, 16)
    else:
        pygame.draw.circle(virtual_screen, "red", player_pos, 16)
        virtual_screen.blit(valve.image, valve.rect)

    virtual_screen.blit(dark_overlay, (0, 0))

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)  # fix scaling and blit to screen

    return player_pos, screen.get_width()/virtual_screen.get_width(), screen.get_height()/virtual_screen.get_height()