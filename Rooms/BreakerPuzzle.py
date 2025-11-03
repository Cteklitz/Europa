import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import random
import Player
import Items
from abc import ABC, abstractmethod

virtual_res = (250, 150)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

exit = False

background = pygame.image.load("Assets/breaker_zoom.png")

solved = False

'''
DEV NOTES:
Connections are not drag and drop, they're click-click. Disconnect works by clicking an endpoint since all endpoints
can only have one connection. In the room loop, I have it such that clicking anywhere besides a node after a first
click should reset the selection. The way that the code is currently written, the connection evaluation can happen in 
any order, but make sure that if a valid connection is made from the output node to the operator node before that 
operator node is fully connected, the final result evaluation pends full connection (should be able to use 
is_fully_connected for this). The plan that I had for the Multimeter (but have not implemented yet) was that it could 
have a smaller lower display that shows all 4 of the output connections as +, 0, or -. '+' means you're over, '0' (or 
'=' maybe) means you got it right, '-' means you're under. So it would show something like XXXX to start (you'd also 
have the number at the top to say how much you're off by) and then if you went over by 3, it would go to +XXX and the 
number would go to 3. If you then got the next one wrong, it would sum the differences ([ev1 - av1] + [ev2 - av2]) and 
display +-XX. The idea behind doing it like that is that it might be confusing if we just tally the difference 
between the expected results and the actual result: if two or more components of the actual result are wrong but the 
output tallies to zero because it's +3, -3, X, X = 0, it would be unintuitive. Since I've yet to implement that aspect, 
it's designer's choice. 

Here are some of the TODOs I have written in my notes (besides general method implementation):

1. Make rectangles opaque (and draw them, not sure if they're drawn or need to be drawn?) so i can see where they need to move
   * I think I need to get rectangles to correspond to mouse_pos by dividing all my x and y coordinates by xScale, yScale

2. Implement actual unique evaluation/comparison logic in each connection() method
   * store how much cur_result=None is over (positive), correct (0), or under (negative) in the OutputNode

3. Click on already connected endpoint to detach wire; create disconnect() function (will need a disconnect_back() too)

4. Draw wires on valid connection

5. Implement Multimeter, check for multimeter equipped
'''


# Linked list implementation using inheritance that connects each link bidirectionally
class Node:
    # every class instance keeps track of same start nodes (not copied)
    start_nodes = []
    operator_nodes = []
    end_nodes = []

    def __init__(self, rect):
        self.node_height = 0  # making height 1 based, 0 is default value
        self.connections_above = []
        self.connection_below = None
        self.rect = rect

    def isClicked(self, pos):
        return self.rect.collidepoint(pos)

    @abstractmethod
    def connect(self, other):
        pass

    @abstractmethod
    def connect_back(self, other):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def disconnect_back(self, other):
        pass


class InputNode(Node):
    def __init__(self, rect, signal_strength=0):
        super().__init__(rect=rect)
        self.node_height = 1
        self.signal_strength = signal_strength
        Node.start_nodes.append(self)  # keep track of input nodes

    def connect(self, other):
        if self.connection_below is not None:  # make sure that the number of connections is valid
            print("Breaker Puzzle connect: Input <--> Operator --- input already connected")
            return False

        if self.node_height == other.node_height - 1:  # node is one level above (note that height grows down)
            # if other node cannot connect, don't connect here; return False
            # this calls connect_back in the OperatorNode subclass, it won't use the implementation given in this subclass
            if other.connect_back(self):
                self.connection_below = other
            else:
                return False
        else:
            print("Breaker Puzzle: cannot connect Input node to node of same height or height difference > 1.")
            return False

        return True

    def connect_back(self, other):
        if self.connection_below is not None:  # make sure that the number of connections is valid
            return False
        if self.node_height == other.node_height - 1:  # node is one level above (note that height grows down)
            self.connection_below = other
        else:
            print("Breaker Puzzle: cannot connect nodes of same height or height difference > 1.")
            return False
        return True

    # TODO: returns True if disconnection was successful in both directions, False otherwise
    def disconnect(self):
        pass

    # TODO: returns True if self can and does disconnect itself from other, False otherwise
    def disconnect_back(self, other):
        pass


class OperatorNode(Node):
    def __init__(self, rect, num_inputs_allowed=0, operation=None):
        super().__init__(rect=rect)
        self.node_height = 2
        self.cur_result = None
        self.num_inputs_allowed = num_inputs_allowed
        self.operation = operation  # lambda function passed as parameter
        Node.operator_nodes.append(self)  # keep track of operator nodes

    def connect(self, other):
        pass

    def connect_back(self, other):
        if self.node_height == other.node_height - 1:  # self is one level above (note that height grows down)
            if self.connection_below is not None:  # make sure that the number of connections is valid
                print("Breaker Puzzle connect back: Output <--> Operator --- operator already connected")
                return False
            self.connection_below = other
        elif self.node_height == other.node_height + 1:  # self is one level below
            if len(self.connections_above) == self.num_inputs_allowed:
                print("Breaker Puzzle connection: Input <--> Operator --- operator has full connections")
                return False
            self.connections_above.append(other)
            # only evaluate if all connections are filled
            if len(self.connections_above) == self.num_inputs_allowed:
                self.evaluate_operation(*self.connections_above)  # evaluate operation and store result
        else:
            print("Breaker Puzzle: cannot connect nodes of same height or height difference > 1.")
            return False
        return True

    # check if an operator node has all connections in and out
    def is_fully_connected(self):
        if self.num_inputs_allowed == len(self.connections_above) and (len(self.connection_below) == 1):
            return True
        return False

    # evaluate using lambda function and 1 or 2 args
    def evaluate_operation(self, val1, val2=None):
        if val2 is None:
            self.cur_result = self.operation(val1.signal_strength)
        else:
            self.cur_result = self.operation(val1.signal_strength,
                                             val2.signal_strength)  # save lambda function result as cur_result
        return self.cur_result

    # TODO:
    #  - Note that here disconnect and disconnect_back can be validly called for connections both above and below.
    #  - Similarly to connect() and connect_back(), must ensure that disconnect_back is checked first with T or F.
    #  - Set cur_result to None before removing connection.
    #  - For above, need to compare object addresses to ensure removal of correct array object (should be easy in
    #    python with objects i would imagine).
    #  - Return True if disconnect succeeds, False otherwise.
    def disconnect(self):
        pass

    def disconnect_back(self, other):
        pass


class OutputNode(Node):
    def __init__(self, rect, expected_out):
        super().__init__(rect=rect)
        self.node_height = 3
        self.expected_out = expected_out
        Node.end_nodes.append(self)  # keep track of end nodes

    def connect(self, other):
        pass

    def connect_back(self, other):
        pass

    def disconnect(self):
        pass

    def disconnect_back(self, other):
        pass


# TODO: don't need this if we're not connecting directly to multimeter, some other implementation needed
class MultimeterNode(Node):
    def __init__(self, display=0):
        super().__init__()
        self.display = display


# 7 input nodes, 6 operator nodes, 4 output nodes
# TODO fix rectangle locations and sizes?; divide by xScale, yScale? Got these based on mouse xPos, yPos by clicking the centers
#  (not top left corner) of the nodes on the image. Note: haven't tested the rectangles much yet
nodes = [
    InputNode(pygame.Rect(229, 82, 40, 40), 13),
    InputNode(pygame.Rect(301, 82, 40, 40), 8),
    InputNode(pygame.Rect(373, 82, 40, 40), 9),
    InputNode(pygame.Rect(444, 82, 40, 40), 8),
    InputNode(pygame.Rect(517, 82, 40, 40), 6),
    InputNode(pygame.Rect(587, 82, 40, 40), 2),
    InputNode(pygame.Rect(659, 82, 40, 40), 4),
    OperatorNode(pygame.Rect(237, 270, 50, 50), 1, lambda x: x + 3),
    OperatorNode(pygame.Rect(319, 270, 50, 50), 2, lambda x, y: x - y),
    OperatorNode(pygame.Rect(401, 270, 50, 50), 2, lambda x, y: x * y),
    OperatorNode(pygame.Rect(482, 270, 50, 50), 2, lambda x, y: x + y),
    OperatorNode(pygame.Rect(565, 270, 50, 50), 2, lambda x, y: x // y),
    OperatorNode(pygame.Rect(646, 270, 50, 50), 2, lambda x, y: x % y),
    OutputNode(pygame.Rect(249, 480, 40, 40), 3),
    OutputNode(pygame.Rect(377, 480, 40, 40), 5),
    OutputNode(pygame.Rect(505, 480, 40, 40), 16),
    OutputNode(pygame.Rect(634, 480, 40, 40), 7)
]

# TODO: delete these after testing is complete
nodes[0].connect(nodes[7])
print(f"{nodes[7].cur_result} should be 16")
nodes[0].connect(nodes[8])
print(f"{nodes[8].cur_result} should be None, {nodes[8]} and {nodes[0].connection_below} should not match.")


def inBounds(x, y):
    global exit
    if exit:
        exit = False
        return 0
    return False


def positionDeterminer(cameFrom):
    pass


def Room(screen, screen_res, events):
    global exit, solved, beakerPuzzle, collected
    xScale = screen.get_width() / virtual_screen.get_width()
    yScale = screen.get_height() / virtual_screen.get_height()

    level, power = Objects.getPipeDungeonInfo()
    upperWingPower, _ = Objects.getPinkWingInfo()
    lit = upperWingPower and level == 1 and power

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_pos = (mouse_x / xScale, mouse_y / yScale)
                if not solved:
                    # TODO: correctly placed and working clickable object implementation
                    recently_selected = None  # track the most recently selected node
                    # map clicks to nodes/rectangles, do logic
                    for node in nodes:
                        if node.isClicked(mouse_pos):
                            # if clicked node is end-point and already has connection, disconnect it
                            if node.node_height % 2 != 0 and node.disconnect():
                                recently_selected = None
                                break

                            if recently_selected is None:
                                recently_selected = node
                            elif node.connect(recently_selected):
                                recently_selected = None  # connection was made, reset
                            else:
                                recently_selected = node  # connection could not be made, set clicked node as selected
                            break  # node was found, break
                        else:
                            recently_selected = None  # allow user to reset their node selection by clicking elsewhere
                    pass

    virtual_screen.fill((195, 195, 195))
    dark_overlay.fill((0, 0, 0, 150))

    Assets.punch_light_hole(virtual_screen, dark_overlay,
                            (virtual_screen.get_width() / 2, virtual_screen.get_height() / 2), 500, (0, 0, 0))

    virtual_screen.blit(background, (0, 0))

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale