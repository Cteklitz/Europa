import pygame
import Player
import Items
import Sounds
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
eye_open = pygame.transform.scale(pygame.image.load('Assets/EYE.png'), (500, 460))
eye_closed = pygame.image.load('Assets/eyeClosed.png')
jumpscare_text = pygame.image.load('Assets/GiftForYouText.png')
eye_closed_scale = 10.0
eye_closed_pos = pygame.Vector2(130.0, 56.0)
eyes = [eye1, eye2, eye1, eye3, eye1, eye5, eye1, eye4] # Array holding images of eye in animated eye object

open = False # changes to true when user opens toolbox
paper_open = False
exit = False
multimeter_found = False
found = 0 # 2 if multimeter has been collected and paper has been opened
cutscene = False # true if cutscene is playing
cutscene_start = 0
played = False # turns true if jumpscare sound is played

toolbox_rect = closed_toolbox.get_rect()
toolbox_rect.center = (125, 75)
multimeter_rect = pygame.Rect(0, 0, multimeter.get_width(), 30)
multimeter_click_rect = pygame.Rect(50, 54, multimeter.get_width(), 30)
crumpled_paper_rect = pygame.Rect(0, 0, multimeter.get_width(), 28)
crumpled_paper_click_rect = pygame.Rect(130, 56, multimeter.get_width(), 28)
toolbox_rect.center = (125, 75)
open_paper_rect = open_paper.get_rect()
eye_rect = pygame.Rect(0, 0, eye1.get_width(), 40)
eye_click_rect = pygame.Rect(70, 44, eye1.get_width(), 40)
open_eye_rect = eye_open.get_rect()
open_eye_rect.center = (250/2 - 4, 150/2 - 15)
closed_eye_rect = eye_closed.get_rect()
closed_eye_rect.center = (250/2 + 5, 150/2)
first_time = pygame.time.get_ticks()
curr_index = 0
curr_eye = eyes[0]

# sounds
eye_squish_sound = pygame.mixer.Sound("Audio/eyeSquish.wav")
pre_jumpscare_sound = pygame.mixer.Sound("Audio/evil2Trimmed1.wav")
jumpscare_sound = pygame.mixer.Sound("Audio/toolboxJumpscare.wav")
jumpscare_layer_sound = pygame.mixer.Sound("Audio/evil2.wav")
paper_crumple_sound = pygame.mixer.Sound("Audio/paperCrumple.wav")
paper_open_sound = pygame.mixer.Sound("Audio/paperOpen.wav")
toolbox_open_close_sound = pygame.mixer.Sound("Audio/toolboxOpenClose.wav")

pre_jumpscare_sound.set_volume(.05) # make audio quieter prejumpscare

def positionDeterminer(cameFrom):
    pass

def inBounds(x, y):
    global exit, open
    if exit:
        exit = False
        return 0
    return False

def Room(screen, screen_res, events):
    global exit, open, multimeter_found, paper_open, first_time, found, curr_index, curr_eye, cutscene, cutscene_start, played, eye_closed_scale, eye_closed_pos, closed_eye_rect
    virtual_screen.fill((159, 161, 160))
    pygame.draw.line(virtual_screen, (0, 0, 0), (0, 100), (screen.get_width(), 100))
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
                        Sounds.letter.play()
                        multimeter_found = True
                        found += 1
                        if found == 2:
                            cutscene = True
                            cutscene_start = pygame.time.get_ticks()
            # Opens and closes paper
            elif crumpled_paper_click_rect.collidepoint((click_x_unscaled, click_y_unscaled)) and open:
                if (not paper_open):
                    paper_open_sound.play()
                    paper_open = True
                else:
                    paper_crumple_sound.play()
                    paper_open = False
                    if (multimeter_found and found == 1 or not multimeter_found and found == 0):
                        found += 1
                        if found == 2:
                            cutscene = True
                            cutscene_start = pygame.time.get_ticks()
            # opens and closes toolbox if animated eye object is not present
            elif(285 < click_x < 1310 and 350 < click_y < 855) and not paper_open and found!=2:
                if(open):
                    toolbox_open_close_sound.play()
                    open = False
                else:
                    toolbox_open_close_sound.play()
                    open = True
            # plays squished sound if eye clicked
            elif eye_click_rect.collidepoint((click_x_unscaled, click_y_unscaled)) and found == 2:
                eye_squish_sound.play()
    if (not open):
        virtual_screen.blit(closed_toolbox, toolbox_rect)
    else:
        virtual_screen.blit(open_toolbox, toolbox_rect)
        # Adds multimeter to screen if it has not been collected
        if (not multimeter_found):
            virtual_screen.blit(multimeter, (50, 54), multimeter_rect)
        # Adds animated eye object if paper has been opened and multimeter collected
        elif (found == 2 and played):
            if (curr_time - first_time >= 740):
                curr_index = (curr_index + 1) % len(eyes)
                curr_eye = eyes[curr_index] # sets current eye for animation in array
                first_time = curr_time
            virtual_screen.blit(curr_eye, (70, 44), eye_rect)
        if (paper_open):
            virtual_screen.blit(open_paper, open_paper_rect) 
        elif (not paper_open):
            virtual_screen.blit(crumpled_paper, (130, 56), crumpled_paper_rect)
        # eye jumpscare cutscene
        if (cutscene):
            if (eye_closed_scale < 280):
                pre_jumpscare_sound.play()
                target_scale = 280
                target_center = pygame.Vector2(virtual_res[0] / 2, virtual_res[1] / 2)
                start_pos = pygame.Vector2(130.0, 56.0)
                progress = (eye_closed_scale - 5.0) / (target_scale - 5.0)
                temp_x = start_pos.x + (target_center.x - start_pos.x) * progress
                temp_y = start_pos.y + (target_center.y - start_pos.y) * progress
            
                eye_closed_pos.x = temp_x
                eye_closed_pos.y = temp_y

                eye_closed_temp = pygame.transform.scale(eye_closed, (int(eye_closed_scale), int(eye_closed_scale)))
                
                eye_closed_scale += 1.5
                closed_eye_rect = eye_closed_temp.get_rect(center=eye_closed_pos)
                
                virtual_screen.blit(eye_closed_temp, closed_eye_rect)
            elif (eye_closed_scale >= 280 and curr_time - cutscene_start < 9000):
                eye_closed_temp = pygame.transform.scale(eye_closed, (280, 280))
                closed_eye_rect = eye_closed_temp.get_rect(center=(virtual_res[0] / 2, virtual_res[1] / 2))
                virtual_screen.blit(eye_closed_temp, closed_eye_rect)
            elif (curr_time - cutscene_start < 13000):
                if (not played):
                    pre_jumpscare_sound.stop()
                    channel1 = pygame.mixer.find_channel(True)
                    channel1.play(jumpscare_layer_sound)
                    channel2 = pygame.mixer.find_channel(True)
                    channel2.play(jumpscare_sound)
                    played = True
                virtual_screen.blit(eye_open, open_eye_rect)
            elif (curr_time - cutscene_start < 16000):
                virtual_screen.blit(jumpscare_text, (0, 0))
    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))
    return player_pos, xScale, yScale