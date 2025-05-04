import ControlRoom
import MainRoom
import PinkRoom
import PinkLowerWing
import BookcaseView

def getPipeDungeonInfo():
        return ControlRoom.level, ControlRoom.power

def getPinkWingInfo():
        return PinkRoom.upperWingPower, PinkRoom.lowerWingPower

class Area:
    def __init__(self, roomLayout):
        self.roomLayout = roomLayout

    def getRoom(self, Room, check):
        return self.roomLayout[Room][check]

    def getPos(self, screen, screen_res, events, room):
        player_pos, xSpeedScale, ySpeedScale = room.Room(screen, screen_res, events)
        return player_pos, xSpeedScale, ySpeedScale
    
PipeDungeon = Area(
    roomLayout = {
            ControlRoom: [MainRoom],
            MainRoom: [ControlRoom, PinkRoom],
            PinkRoom: [MainRoom, PinkLowerWing],
            PinkLowerWing: [PinkRoom, BookcaseView],
            BookcaseView: [PinkLowerWing]
    }
)