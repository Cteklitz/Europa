from Rooms import ControlRoom, MainRoom, PinkRoom, PinkLowerWing, BookcaseView, OrangeYellow, \
Safe, PinkUpperWing, TrianglePuzzle, TriangleSolution, BeakerPuzzle, MscopeTable, Microscope, \
LockedDoor, Desk, SpotDiffs, PinkPower, BlueRoom

def getPipeDungeonInfo():
    return ControlRoom.level, ControlRoom.power

def getPinkWingInfo():
    return PinkRoom.upperWingPower, PinkRoom.lowerWingPower

def getCutscene():
    return BookcaseView.cutscene

def getTriangleSolved():
    return TrianglePuzzle.solved

def getBeakerSolved():
    return BeakerPuzzle.solved

def getSpotDiffsSolved():
    return SpotDiffs.chestOpen

def getColors():
    return MscopeTable.redFound, OrangeYellow.yellowFound, Desk.blueFound

def getSelected():
    return MscopeTable.selected

def getOpen():
    return LockedDoor.solved

def getPinkPower():
    return PinkPower.pinkPower

def getLetterCount():
    count = 0
    if TrianglePuzzle.collected:
        count += 1
    if BeakerPuzzle.collected:
        count += 1
    if Safe.collected:
        count += 1
    if SpotDiffs.collected:
        count += 1
    return count

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
            MainRoom: [ControlRoom, PinkRoom, BlueRoom],
            PinkRoom: [MainRoom, PinkLowerWing, PinkUpperWing],
            PinkLowerWing: [PinkRoom, BookcaseView, LockedDoor, Desk, SpotDiffs, PinkPower],
            BookcaseView: [PinkLowerWing, OrangeYellow, Safe],
            OrangeYellow: [BookcaseView],
            Safe: [BookcaseView],
            LockedDoor: [PinkLowerWing, PinkPower],
            Desk: [PinkLowerWing],
            SpotDiffs: [PinkLowerWing],
            PinkUpperWing: [PinkRoom, TrianglePuzzle, TriangleSolution, BeakerPuzzle, MscopeTable],
            TrianglePuzzle: [PinkUpperWing],
            TriangleSolution: [PinkUpperWing],
            BeakerPuzzle: [PinkUpperWing], 
            MscopeTable: [PinkUpperWing, Microscope],
            Microscope: [MscopeTable],
            PinkPower: [PinkLowerWing],
            BlueRoom: [MainRoom]
    }
)

