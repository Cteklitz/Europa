import pygame

valveSound = pygame.mixer.Sound("Audio/valve.wav")
switchSound = pygame.mixer.Sound("Audio/switch.wav")

heartbeat = pygame.mixer.Sound("Audio/heartbeat.wav")

ominousAmb = pygame.mixer.Sound("Audio/mainroomambience-1.wav")
powerAmb = pygame.mixer.Sound("Audio/powerambience.wav")

brainwash = pygame.mixer.Sound("Audio/weird noises.-2.wav")
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

electricityNoise = pygame.mixer.Sound("Audio/ElectricityNoise.wav")

pipe = pygame.mixer.Sound("Audio/pipe.wav")

toolbox = pygame.mixer.Sound("Audio/toolboxOpenClose.wav")

lockerOpen = pygame.mixer.Sound("Audio/locker_open.wav")
lockerClose = pygame.mixer.Sound("Audio/locker_close.wav")

powerDown = pygame.mixer.Sound("Audio/power_down.mp3")

tape = pygame.mixer.Sound("Audio/tape.wav")

scaryBell = pygame.mixer.Sound("Audio/scary_bell.wav")
slowCreepy = pygame.mixer.Sound("Audio/slow_creepy.wav")

pickup = pygame.mixer.Sound("Audio/pickup.wav")
pickup.set_volume(.8)

spark1 = pygame.mixer.Sound("Audio/spark1.wav")
spark2 = pygame.mixer.Sound("Audio/spark2.wav")
spark3 = pygame.mixer.Sound("Audio/spark3.wav")
spark4 = pygame.mixer.Sound("Audio/spark4.wav")
spark5 = pygame.mixer.Sound("Audio/spark5.wav")
spark1.set_volume(0.4)
spark2.set_volume(0.4)
spark3.set_volume(0.4)
spark4.set_volume(0.4)
spark5.set_volume(0.4)

radioClose = pygame.mixer.Sound("Audio/radio_close.wav")
radioFar = pygame.mixer.Sound("Audio/radio_far.wav")

curtain = pygame.mixer.Sound("Audio/curtain.wav")
curtain.set_volume(.5)
openClose = pygame.mixer.Sound("Audio/toolboxOpenClose.wav")
openClose.set_volume(.5)
sink = pygame.mixer.Sound("Audio/sink.wav")
sink.set_volume(.3)
sink2 = pygame.mixer.Sound("Audio/sink.wav")
sink2.set_volume(.3)

accessGranted = pygame.mixer.Sound("Audio/accessgranted.mp3")

bunsen = pygame.mixer.Sound("Audio/bunsen.wav")
lighter = pygame.mixer.Sound("Audio/lighter.wav")

unlock = pygame.mixer.Sound("Audio/unlock.wav")

scary = pygame.mixer.Sound("Audio/scary.wav")
scary.set_volume(0.5)

TrashSounds = pygame.mixer.Sound("Audio/TrashSounds.wav")