import pygame
import sys
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import Player
import Items

pygame.init()

VIRTUAL_RES = (400, 250)

player_pos = pygame.Vector2(192, 128)

# Images will be loaded when first needed
lockbox_img = None
lockbox_img_open = None
numbers_img = None

def load_images():
    global lockbox_img, lockbox_img_open, numbers_img
    if lockbox_img is None:
        lockbox_img = pygame.image.load("Assets/Lockbox_puzzle.png").convert_alpha()
        lockbox_img = pygame.transform.scale(lockbox_img, VIRTUAL_RES)
        lockbox_img_open = pygame.image.load("Assets/Lockbox_puzzle_open.png").convert_alpha()
        lockbox_img_open = pygame.transform.scale(lockbox_img_open, VIRTUAL_RES)
        numbers_img = pygame.image.load("Assets/Lockbox_numbers.png").convert_alpha()

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 28)

cell_w, cell_h = 166, 292

digit_map = [
    (3, 1), # 0
    (0, 0), # 1
    (1, 0), # 2
    (2, 0), # 3
    (3, 0), # 4
    (4, 0), # 5
    (5, 0), # 6
    (0, 1), # 7
    (1, 1), # 8
    (2, 1), # 9
]
digit_regions = []
for col, row in digit_map:
    left = col * cell_w
    top = row * cell_h
    right = left + cell_w
    bottom = top + cell_h
    digit_regions.append((left, top, right, bottom))

digit_positions = [
    [105, 113], [155, 113], [207, 113], [255, 113],
]
digit_size = [45, 41]

CORRECT_CODE = [1, 2, 3, 4]
digits = [0, 0, 0, 0]
selected = 0
unlocked = False
chestOpen = False
exit = False
collected = False



def inBounds(x=None, y=None):
    global exit
    if exit:
        exit = False
        return 0
    return False

def Room(screen, screen_res, events):
    global digits, selected, unlocked, chestOpen, exit, player_pos, collected
    
    # Load images if not already loaded
    load_images()
    
    # Handle events from main game loop
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and not unlocked:
            mx, my = pygame.mouse.get_pos()
            # Scale mouse coordinates to virtual resolution
            vmx = int(mx * VIRTUAL_RES[0] / screen_res[0])
            vmy = int(my * VIRTUAL_RES[1] / screen_res[1])
            arrow_w, arrow_h = 30, 18
            arrow_offset_y = 22
            for i in range(4):
                x, y = digit_positions[i]
                scale_w, scale_h = digit_size
                up_rect = pygame.Rect(x + (scale_w - arrow_w)//2, y - arrow_offset_y, arrow_w, arrow_h)
                down_rect = pygame.Rect(x + (scale_w - arrow_w)//2, y + scale_h + arrow_offset_y - arrow_h, arrow_w, arrow_h)
                if up_rect.collidepoint(vmx, vmy):
                    digits[i] += 1
                    if digits[i] > 9:
                        digits[i] = 0
                if down_rect.collidepoint(vmx, vmy):
                    digits[i] -= 1
                    if digits[i] < 0:
                        digits[i] = 9
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                exit = True
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                selected = (selected + 1) % 4
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                selected = (selected - 1) % 4
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                digits[selected] += 1
                if digits[selected] > 9:
                    digits[selected] = 0
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                digits[selected] -= 1
                if digits[selected] < 0:
                    digits[selected] = 9

    # Check if code is correct
    if digits == CORRECT_CODE:
        unlocked = True
        chestOpen = True
        collected = True

    # Draw the puzzle interface
    virtual = pygame.Surface(VIRTUAL_RES)
    if unlocked:
        virtual.blit(lockbox_img_open, (0, 0))
    else:
        virtual.blit(lockbox_img, (0, 0))

    # Only show keypad if not unlocked
    if not unlocked:
        arrow_w, arrow_h = 30, 18  # size of clickable arrow region
        arrow_offset_y = 22        # vertical offset above/below digit

        for i in range(4):
            x, y = digit_positions[i]
            scale_w, scale_h = digit_size
            left, top, right, bottom = digit_regions[digits[i] % 10]
            src_rect = pygame.Rect(left, top, right - left, bottom - top)
            digit_sprite = numbers_img.subsurface(src_rect)
            digit_sprite = pygame.transform.smoothscale(digit_sprite, (scale_w, scale_h))
            virtual.blit(digit_sprite, (x, y))
            rect = pygame.Rect(x, y, scale_w, scale_h)
            if i == selected:
                pygame.draw.rect(virtual, (255, 220, 80), rect, 3, border_radius=8)

    # Scale and display on screen
    scaled = pygame.transform.scale(virtual, screen_res)
    screen.blit(scaled, (0, 0))

    xScale = screen_res[0] / VIRTUAL_RES[0]
    yScale = screen_res[1] / VIRTUAL_RES[1]
    return player_pos, xScale, yScale

def positionDeterminer(arg):
    pass

