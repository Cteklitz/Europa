import pygame

valveSound = pygame.mixer.Sound("Audio/valve.wav")
heartbeat = pygame.mixer.Sound("Audio/heartbeat.wav")

ominousAmb = pygame.mixer.Sound("Audio/mainroomambience-1.wav")
powerAmb = pygame.mixer.Sound("Audio/powerambience.wav")

brainwash = pygame.mixer.Sound("Audio/weird noises..wav")
book = pygame.mixer.Sound("Audio/book.wav")
page = pygame.mixer.Sound("Audio/page.wav")

magnet1 = pygame.mixer.Sound("Audio/magnet1.wav")
magnet2 = pygame.mixer.Sound("Audio/magnet2.wav")
magnet3 = pygame.mixer.Sound("Audio/magnet3.wav")

glass1 = pygame.mixer.Sound("Audio/glass1.wav")
glass2 = pygame.mixer.Sound("Audio/glass2.wav")

magnets = [magnet1, magnet2, magnet3]
glass = [glass1, glass2]

for magnet in magnets:
    magnet.set_volume(0.75)

draweropen = pygame.mixer.Sound("Audio/draweropen.wav")
drawerclose = pygame.mixer.Sound("Audio/drawerclose.wav")

letter = pygame.mixer.Sound("Audio/opentriangle.wav")

combo = pygame.mixer.Sound("Audio/combo.wav")

powerOn = pygame.mixer.Sound("Audio/powerOnAmbStart.wav")
powerOnAmb = pygame.mixer.Sound("Audio/powerOnAmb.wav")

mopSound = pygame.mixer.Sound("Audio/mopsounds.wav")

pipe = pygame.mixer.Sound("Audio/pipe.wav")

toolbox = pygame.mixer.Sound("Audio/toolboxOpenClose.wav")

lockerOpen = pygame.mixer.Sound("Audio/locker_open.wav")
lockerClose = pygame.mixer.Sound("Audio/locker_close.wav")

powerDown = pygame.mixer.Sound("Audio/power_down.mp3")

tape = pygame.mixer.Sound("Audio/tape.wav")

scaryBell = pygame.mixer.Sound("Audio/scary_bell.wav")
slowCreepy = pygame.mixer.Sound("Audio/slow_creepy.wav")

pickup = pygame.mixer.Sound("Audio/pickup.wav")