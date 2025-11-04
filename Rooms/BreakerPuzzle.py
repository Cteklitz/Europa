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
        if self.connection_below is not None:
            print("Disconnecting")
            if (self.connection_below.disconnect_back(self)):
                self.connection_below = None
                return True
            else:
                return False
        else:
            return False

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
        print("Attempting connection")
        # check if connection is coming from above or below
        if other.node_height == 1: # connection comes from above
            print("Connection coming from above")
            # check that there is an open input
            if self.num_inputs_allowed > len(self.connections_above):
                if (other.connect_back(self)):
                    self.connections_above.append(other)
                    return True
                else:
                    return False
            elif self.connections_above[0] is None:
                if (other.connect_back(self)):
                    self.connections_above[0] = other
                    return True
                else:
                    return False
            else:
                print("Breaker Puzzle: Operator node does not have open inputs")
                return False
        elif other.node_height == 3: # connection comes from below
            print("Connection coming from below")
            if self.connection_below is not None:  # make sure that output is empty
                print("Breaker Puzzle connect: Operator <--> Output --- Operator output already connected")
                return False
            else:
                if other.connect_back(self):
                    self.connection_below = other
                    return True
                else:
                    return False
        elif other.node_height == 2:
            print("Breaker Puzzle: Cannot connect two operator nodes")
            return False      
        else:
            print(f"Breaker Puzzle: Invalid height value of {other.height}")
            return False

        return True

    def connect_back(self, other):
        if self.node_height == other.node_height - 1:  # self is one level above (note that height grows down)
            if self.connection_below is not None:  # make sure that the number of connections is valid
                print("Breaker Puzzle connect back: Output <--> Operator --- operator already connected")
                return False
            self.connection_below = other
        elif self.node_height == other.node_height + 1:  # self is one level below
            if len(self.connections_above) == 0:
                self.connections_above.append(other)
            elif self.connections_above[0] is None:
                self.connections_above[0] = other
            elif len(self.connections_above) == self.num_inputs_allowed:
                print("Breaker Puzzle connection: Input <--> Operator --- operator has full connections")
                return False
            else:
                self.connections_above.append(other)
            # only evaluate if all connections are filled
            if len(self.connections_above) == self.num_inputs_allowed and self.connections_above[0] is not None:
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
        # TODO: Handle case where first connection is disconnected (rn it just moves the other connection over; going to need to rework connect and drawing wires to handle this case)
        # check if disconnect comes from above or below
        if other.node_height == 1: # input node
            for i in range(len(self.connections_above)):
                if self.connections_above[i] == other:
                    self.cur_result = None
                    self.connections_above[i] = None
                    if i == 1:
                        self.connections_above.pop()
                    return True
            return False
        elif other.node_height == 3: # output node
            if self.connection_below == other:
                self.cur_result = None
                self.connection_below = None
                return True
            else:
                return False
        else:
            return False


class OutputNode(Node):
    def __init__(self, rect, expected_out):
        super().__init__(rect=rect)
        self.node_height = 3
        self.expected_out = expected_out
        Node.end_nodes.append(self)  # keep track of end nodes

    def connect(self, other):
        if len(self.connections_above) == 0: # check that node does not already have connection
            if other.node_height == 2: # check that other node is an operator node
                if (other.connect_back(self)):
                    self.connections_above.append(other)
                    return True
        return False

    def connect_back(self, other):
        if len(self.connections_above) == 0: # check that node does not already have connection
            if other.node_height == 2: # check that other node is an operator node
                self.connections_above.append(other)
                return True
        return False

    def disconnect(self):
        if len(self.connections_above) == 1: # check that node has connection
            if self.connections_above[0].disconnect_back(self):
                self.connections_above.pop()
                return True
        return False

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
    InputNode(pygame.Rect(39, 12, 12, 14), 13),
    InputNode(pygame.Rect(53, 12, 12, 14), 8),
    InputNode(pygame.Rect(67, 12, 12, 14), 9),
    InputNode(pygame.Rect(81, 12, 12, 14), 8),
    InputNode(pygame.Rect(95, 12, 12, 14), 6),
    InputNode(pygame.Rect(109, 12, 12, 14), 2),
    InputNode(pygame.Rect(123, 12, 12, 14), 4),
    OperatorNode(pygame.Rect(40, 48, 13, 17), 1, lambda x: x + 3),
    OperatorNode(pygame.Rect(56, 48, 13, 17), 2, lambda x, y: x - y),
    OperatorNode(pygame.Rect(72, 48, 13, 17), 2, lambda x, y: x * y),
    OperatorNode(pygame.Rect(88, 48, 13, 17), 2, lambda x, y: x + y),
    OperatorNode(pygame.Rect(104, 48, 13, 17), 2, lambda x, y: x // y),
    OperatorNode(pygame.Rect(120, 48, 13, 17), 2, lambda x, y: x % y),
    OutputNode(pygame.Rect(43, 93, 12, 14), 3),
    OutputNode(pygame.Rect(68, 93, 12, 14), 5),
    OutputNode(pygame.Rect(93, 93, 12, 14), 16),
    OutputNode(pygame.Rect(118, 93, 12, 14), 7)
]

# TODO: delete these after testing is complete
#nodes[0].connect(nodes[7])
#print(f"{nodes[7].cur_result} should be 16")
#nodes[0].connect(nodes[8])
#print(f"{nodes[8].cur_result} should be None, {nodes[8]} and {nodes[0].connection_below} should not match.")


def inBounds(x, y):
    global exit
    if exit:
        exit = False
        return 0
    return False


def positionDeterminer(cameFrom):
    pass

recently_selected = None 
def Room(screen, screen_res, events):
    global exit, solved, beakerPuzzle, collected, recently_selected
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
                    #recently_selected = None  # track the most recently selected node
                    # map clicks to nodes/rectangles, do logic
                    anySelected = False
                    for node in nodes:
                        if node.isClicked(mouse_pos):
                            anySelected = True
                            #print(f"{node.rect}, {mouse_pos}")
                            #print(f"{recently_selected}")
                            # if clicked node is end-point and already has connection, disconnect it
                            if node.node_height % 2 != 0 and node.disconnect():
                                recently_selected = None
                                break

                            if recently_selected is None:
                                print("selected node")
                                recently_selected = node
                            elif node.connect(recently_selected):
                                print("connection made!")
                                recently_selected = None  # connection was made, reset
                            else:
                                recently_selected = node  # connection could not be made, set clicked node as selected
                            break  # node was found, break
                    if not anySelected:
                        print("deselected node")
                        recently_selected = None  # allow user to reset their node selection by clicking elsewhere
                    pass

    virtual_screen.fill((195, 195, 195))
    dark_overlay.fill((0, 0, 0, 150))

    Assets.punch_light_hole(virtual_screen, dark_overlay,
                            (virtual_screen.get_width() / 2, virtual_screen.get_height() / 2), 500, (0, 0, 0))

    virtual_screen.blit(background, (0, 0))

    # draw wires for connections
    for node in nodes:
        if node.node_height == 2: # start all connections from operator nodes
            if len(node.connections_above) >= 1 and node.connections_above[0] is not None:
                pygame.draw.line(virtual_screen, (100,0,0), (node.rect.left + 3, node.rect.top + 1), (node.connections_above[0].rect.left + 5, node.connections_above[0].rect.top + 12), width=2)
            if len(node.connections_above) == 2 and node.connections_above[1] is not None:
                pygame.draw.line(virtual_screen, (100,0,0), (node.rect.left + 8, node.rect.top + 1), (node.connections_above[1].rect.left + 5, node.connections_above[1].rect.top + 12), width=2)
            if node.connection_below is not None:
                pygame.draw.line(virtual_screen, (100,0,0), (node.rect.left + 3, node.rect.top + 15), (node.connection_below.rect.left + 5, node.connection_below.rect.top + 1), width=2)

    # draw wire from current selected node to mouse
    if recently_selected is not None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pos = (mouse_x / xScale, mouse_y / yScale)
        if recently_selected.node_height == 1: # input node
            pygame.draw.line(virtual_screen, (100,0,0), (recently_selected.rect.left + 5, recently_selected.rect.top + 12), mouse_pos, width=2)
        elif recently_selected.node_height == 2: # operator node
            # idk how to handle this and make it look good, temp implmentation for now
            pygame.draw.line(virtual_screen, (100,0,0), (recently_selected.rect.left + 3, recently_selected.rect.top + 15), mouse_pos, width=2)
        elif recently_selected.node_height == 3: # output node
            pygame.draw.line(virtual_screen, (100,0,0), (recently_selected.rect.left + 5, recently_selected.rect.top + 1), mouse_pos, width=2)

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale