import pygame
import Player
import Items
virtual_res = (250, 150)
virtual_screen = pygame.Surface(virtual_res)
player_pos = pygame.Vector2(192, 128)

closed_toolbox = pygame.image.load('Assets/ToolboxZoomClosed.png')
open_toolbox = pygame.image.load('Assets/ToolboxZoomOpen.png')
multimeter_unscaled = pygame.image.load('Assets/multimeter.png')
multimeter = pygame.transform.scale(multimeter_unscaled, (46, 80))
crumpled_paper = pygame.image.load('Assets/crumpledPaper.png')
open_paper = pygame.image.load('Assets/openToolboxPaper.png')
eye1 = pygame.image.load('Assets/toolboxEye1.png')
eye2 = pygame.image.load('Assets/toolboxEye2.png') 
eye3 = pygame.image.load('Assets/toolboxEye3.png')         
eye4 = pygame.image.load('Assets/toolboxEye4.png') 
eye5 = pygame.image.load('Assets/toolboxEye5.png')        
eyes = [eye1, eye2, eye1, eye3, eye1, eye5, eye1, eye4]

open = False # changes to true when user opens toolbox
paper_open = False
exit = False
multimeter_found = False
found = 0 # 2 if multimeter has been collected and paper has been opened


toolbox_rect = closed_toolbox.get_rect()
toolbox_rect.center = (125, 75)
multimeter_rect = pygame.Rect(0, 0, multimeter.get_width(), 30)
multimeter_click_rect = pygame.Rect(50, 54, multimeter.get_width(), 30)
crumpled_paper_rect = pygame.Rect(0, 0, multimeter.get_width(), 28)
crumpled_paper_click_rect = pygame.Rect(130, 56, multimeter.get_width(), 28)
toolbox_rect.center = (125, 75)
open_paper_rect = open_paper.get_rect()
eye_rect = (0, 0, eye1.get_width(), 40)
first_time = pygame.time.get_ticks()
curr_index = 0
curr_eye = eyes[0]
def positionDeterminer(cameFrom):
    pass

def inBounds(x, y):
    global exit, open
    if exit:
        exit = False
        return 0
    return False

def Room(screen, screen_res, events):
    global exit, open, multimeter_found, paper_open, first_time, found, curr_index, curr_eye
    virtual_screen.fill((0, 0, 0)) # fill screen with black, replace with bg later
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()
    curr_time = pygame.time.get_ticks()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE and not paper_open:
                exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_x, click_y = event.pos
            click_x_unscaled = click_x/xScale
            click_y_unscaled = click_y/yScale
            # Changes toolbox to open or closed if clicked on
            if multimeter_click_rect.collidepoint((click_x_unscaled, click_y_unscaled)) and open and not multimeter_found and not paper_open:           
                    if (Player.addItem(Items.multimeter)):
                        multimeter_found = True
                        found += 1
            elif crumpled_paper_click_rect.collidepoint((click_x_unscaled, click_y_unscaled)) and open:
                if (not paper_open):
                    paper_open = True
                    if (multimeter_found and found == 1 or not multimeter_found and found == 0):
                        found += 1
                else:
                    paper_open = False
            elif(285 < click_x < 1310 and 350 < click_y < 855) and not paper_open and found!=2:
                if(open):
                    open = False
                else:
                    open = True
    if (not open):
        virtual_screen.blit(closed_toolbox, toolbox_rect)
    else:
        virtual_screen.blit(open_toolbox, toolbox_rect)
        if (not multimeter_found):
            virtual_screen.blit(multimeter, (50, 54), multimeter_rect)
        if (paper_open):
            virtual_screen.blit(open_paper, open_paper_rect) 
        elif (not paper_open):
            virtual_screen.blit(crumpled_paper, (130, 56), crumpled_paper_rect)
            if (found == 2):
                if (curr_time - first_time >= 740):
                    curr_index = (curr_index + 1) % len(eyes)
                    curr_eye = eyes[curr_index]
                    first_time = curr_time
                virtual_screen.blit(curr_eye, (70, 44), eye_rect)

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))
    return player_pos, xScale, yScale