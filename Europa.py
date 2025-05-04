# Example file showing a circle moving on screen
import pygame
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

import Area
import MainRoom

# pygame setup
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_res = screen.get_size()
clock = pygame.time.Clock()
running = True
dt = 0
area = Area.PipeDungeon
Room = MainRoom

def updateRoom(room):
    global Room
    Room = room

while running:
    events = pygame.event.get()
    player_pos, xSpeedScale, ySpeedScale = area.getPos(screen, screen_res, events, Room)
    for event in events:
        if event.type == pygame.QUIT:
                running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_BACKSPACE:
                check = Room.inBounds(player_pos.x, y)
                if type(check) == int:
                    updateRoom(area.getRoom(Room, check))
            if event.key == pygame.K_e:
                check = Room.inBounds(player_pos.x, y)
                if type(check) == int:
                    updateRoom(area.getRoom(Room, check))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        y = player_pos.y - 325 * dt / ySpeedScale
        check = Room.inBounds(player_pos.x, y)
        if type(check) == int:
            updateRoom(area.getRoom(Room, check))
        elif check:
            player_pos.y = y
    if keys[pygame.K_s]:
        y = player_pos.y + 325 * dt / ySpeedScale
        check = Room.inBounds(player_pos.x, y)
        if type(check) == int:
            updateRoom(area.getRoom(Room, check))
        elif check:
            player_pos.y = y
    if keys[pygame.K_a]:
        x = player_pos.x - 325 * dt / xSpeedScale
        check = Room.inBounds(x, player_pos.y)
        if type(check) == int:
            updateRoom(area.getRoom(Room, check))
        elif check:
            player_pos.x = x
    if keys[pygame.K_d]:
        x = player_pos.x + 325 * dt / xSpeedScale
        check = Room.inBounds(x, player_pos.y)
        if type(check) == int:
            updateRoom(area.getRoom(Room, check))
        elif check:
            player_pos.x = x

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()