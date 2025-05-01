import ControlRoom
import MainRoom
import PinkRoom

def getPipeDungeonInfo():
        return ControlRoom.level, ControlRoom.power

class Area:
    def __init__(self, roomLayout):
        self.roomLayout = roomLayout

    def getRoom(self, Room, check):
        return self.roomLayout[Room][check]

    def getPos(self, screen, screen_res, events, room):
        player_pos = room.Room(screen, screen_res, events)
        return player_pos
    
PipeDungeon = Area(
    roomLayout = {
            ControlRoom: [MainRoom],
            MainRoom: [ControlRoom, PinkRoom],
            PinkRoom: [MainRoom]
    }
)