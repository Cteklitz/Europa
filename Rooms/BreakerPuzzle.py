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
multimeter = Assets.multimeter
multimeter_toggled = Assets.multimeter_toggled
multimeter_toggle_rect = pygame.Rect(170 + 22, 20 + 45, 25, 25)
numbers = Assets.multiNumbers
multimeter_status = False

# TODO: toggle to True to override BreakerPuzzle
# solved = True
solved = False

'''
DEV NOTES:
To solve the Breaker Puzzle, Player must connect input nodes containing integer values through unspecified operator 
nodes--which perform mathematical expressions using input values--to output nodes that check for the correct 'voltage'. 
The Player can use a multimeter item that both tells whether each connection is over, under, or correct and totals the 
cumulative error. Player connects nodes using wires, connecting each level to the next until all output nodes are 
satisfied.
We use a Linked List representation with inheritance and abstract methods so that our implementation would allow 
multiple possible answers to be verified. Each node is able to disconnect from other nodes if (1) its node is clicked 
(if node only has 1 prong: input, output nodes) or (2) its prongs are clicked (if node has more than 1 prong: operator 
nodes) while those prongs are connected (There's gotta be a better word than prongs, it just happened to be the only 
word I could think of. Feel free to refactor variables and comments if you come up with a more representative word!). 
Each operator node has its own wire color for all of its connections to make wires distinguishable.
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

    # returns True if disconnection was successful in both directions, False otherwise
    def disconnect(self):
        if self.connection_below is not None:
            print(f"Disconnecting node: {self} from ")
            if self.connection_below.disconnect_back(self):
                self.connection_below = None
                return True
            else:
                return False
        else:
            return False

    # returns True if self can and does disconnect itself from other, False otherwise
    def disconnect_back(self, other):
        if self.connection_below is not None:
            print(f"Disconnecting node: {self} from ")
            self.connection_below = None
            return True
        else:
            return False


class OperatorNode(Node):
    def __init__(self, rect, num_inputs_allowed=0, operation=None):
        super().__init__(rect=rect)
        self.node_height = 2
        self.cur_result = None
        self.num_inputs_allowed = num_inputs_allowed
        self.operation = operation  # lambda function passed as parameter
        Node.operator_nodes.append(self)  # keep track of operator nodes
        for i in range(num_inputs_allowed):
            self.connections_above.append(None)  # set to None so that the first 1-2 indices are defined

        operator_index = len(self.operator_nodes)-1  # note, for indexing, that this node has already been added to operator_nodes
        self.top_left_rect = pygame.Rect(42+(16*operator_index),48,4,3)
        self.top_right_rect = None
        if num_inputs_allowed == 2:
            self.top_right_rect = pygame.Rect(47+(16*(operator_index)),48,4,3)
        self.bottom_rect = pygame.Rect(42+(16*operator_index),62,4,3)
        self.selected_prong = None  # None = None, 0 = tl, 1 = tr, 2 = bottom

    def isClicked(self, pos):
        # Not great design, but we just use these prong rectangles instead of the node's rectangle
        if self.top_left_rect.collidepoint(pos):
            self.selected_prong = 0
            print(f"Top Left Prong selected")
        elif self.top_right_rect is not None and self.top_right_rect.collidepoint(pos):
            self.selected_prong = 1
            print(f"Top Right Prong selected")
        elif self.bottom_rect.collidepoint(pos):
            self.selected_prong = 2
            print(f"Bottom Prong selected")
        else:
            return False
        return True

    def connect(self, other):
        print(f"Attempting connection from {self} to {other}")
        # check if connection is coming from above or below
        if other.node_height == 1:  # connection comes from above
            # check that selected prong is open to input, can be connected
            if self.connections_above[0] is None and self.selected_prong == 0:
                if other.connect_back(self):
                    self.connections_above[0] = other
                else:
                    print(f"{other} connect_back to {self} failed")
                    return False
            elif self.connections_above[1] is None and self.selected_prong == 1:
                if other.connect_back(self):
                    self.connections_above[1] = other
                else:
                    print(f"{other} connect_back to {self} failed")
                    return False
            else:
                print(f"Operator Connect to INPUT: selected operator--{self}--prong #{self.selected_prong}, but "
                      f"connections above are {self.connections_above}")
                return False
        elif other.node_height == 3:  # connection comes from below
            if self.connection_below is not None:  # make sure that output is empty
                print("Breaker Puzzle connect: Operator <--> Output --- Operator output already connected")
                return False
            else:
                # if bottom prong selected, try to initiate connection
                if self.selected_prong == 2:
                    if other.connect_back(self):
                        self.connection_below = other
                    else:
                        print(f"{other} connect_back to {self} failed")
                        return False
                else:
                    print(f"OPERATOR Connect to OUTPUT: selected operator--{self}--prong #{self.selected_prong}, but "
                          f"connection below is {self.connection_below}")
                    return False
        elif other.node_height == 2:
            print("Breaker Puzzle: Cannot connect two operator nodes")
            return False
        else:
            print(f"Breaker Puzzle Operator Connect: Invalid other-height value of {other.height}")
            return False

        # only evaluate if all connections are filled
        if len(self.connections_above) == self.num_inputs_allowed and self.connections_above[0] is not None:
            if self.num_inputs_allowed == 2 and self.connections_above[1] is not None:
                self.evaluate_operation(*self.connections_above)  # evaluate operation and store result
            elif self.num_inputs_allowed == 1:
                self.evaluate_operation(*self.connections_above)
        print(f"---Node's Connections---\n---Top: {self.connections_above}---\n---Bottom: {self.connection_below}---")
        return True

    def connect_back(self, other):
        if self.node_height == other.node_height - 1:  # self is one level above (note that height grows down)
            # make sure that the correct prong was selected, can be attached
            if self.connection_below is not None:  # make sure that the number of connections is valid
                print("Breaker Puzzle connect back: Output <--> Operator --- operator already connected")
                return False
            if self.selected_prong == 2:
                self.connection_below = other
            else:
                print(f"OPERATOR Connect-Back to OUTPUT: selected operator--{self}--prong #{self.selected_prong}, "
                      f"but connection below is {self.connection_below}")
                return False
        elif self.node_height == other.node_height + 1:  # self is one level below
            # see which prong was selected, if it can be attached
            if self.connections_above[0] is None and self.selected_prong == 0:
                self.connections_above[0] = other
            elif self.connections_above[1] is None and self.selected_prong == 1:
                self.connections_above[1] = other
            else:
                print(f"OPERATOR Connect-Back to INPUT: selected operator--{self}--prong #{self.selected_prong}, "
                      f"but connections above are {self.connections_above}")
                return False

            # only evaluate if all connections are filled  (doesn't look very pretty, but it should work)
            if len(self.connections_above) == self.num_inputs_allowed and self.connections_above[0] is not None:
                if self.num_inputs_allowed == 2 and self.connections_above[1] is not None:
                    self.evaluate_operation(*self.connections_above)  # evaluate operation and store result
                elif self.num_inputs_allowed == 1:
                    self.evaluate_operation(*self.connections_above)
        else:
            print("Breaker Puzzle: cannot connect nodes of same height or height difference > 1.")
            return False
        print(f"---Node's Connections---\n---Top: {self.connections_above}---\n---Bottom: {self.connection_below}---")
        return True

    # check if an operator node has all connections in and out
    def is_fully_connected(self):
        if self.num_inputs_allowed == len(self.connections_above) and (len(self.connection_below) == 1) and self.connections_above[0] is not None:
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

    def disconnect(self):
        if self.selected_prong is None:
            return False
        other = self.connections_above[self.selected_prong] if self.selected_prong < 2 else self.connection_below
        if other is None:
            return False  # nothing to disconnect
        # check if disconnect comes from above or below
        if other.node_height == 1:  # input node
            for i in range(len(self.connections_above)):
                if self.connections_above[i] == other and other.disconnect_back(self):
                    self.cur_result = None
                    self.connections_above[i] = None
                    return True
            return False
        elif other.node_height == 3:  # output node
            if self.connection_below == other and other.disconnect_back(self):
                self.cur_result = None
                self.connection_below = None
                return True
            else:
                return False
        else:
            return False
        pass

    def disconnect_back(self, other):
        # check if disconnect comes from above or below
        if other.node_height == 1:  # input node
            for i in range(len(self.connections_above)):
                if self.connections_above[i] == other:
                    self.cur_result = None
                    self.connections_above[i] = None
                    return True
            return False
        elif other.node_height == 3:  # output node
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
        if len(self.connections_above) == 0:  # check that node does not already have connection
            if other.node_height == 2:  # check that other node is an operator node
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
        if len(self.connections_above) == 1:  # check that node has connection
            self.connections_above.pop()
            return True
        return False


# 7 input nodes, 6 operator nodes, 4 output nodes
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
    OutputNode(pygame.Rect(118, 93, 12, 14), 7)]


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
    global exit, solved, beakerPuzzle, collected, recently_selected, multimeter_status
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
                if multimeter_toggle_rect.collidepoint(mouse_pos) and recently_selected is None:                   
                    multimeter_status = not multimeter_status
                    Sounds.pipe.play()
                elif not solved:
                    # map clicks to nodes/rectangles, do logic
                    anySelected = False
                    for node in nodes:
                        if node.isClicked(mouse_pos):
                            anySelected = True
                            if node.disconnect():
                                Sounds.toolbox.play()
                                recently_selected = None
                                break
                            if recently_selected is None:
                                print("selected node")
                                recently_selected = node
                            elif node.connect(recently_selected):
                                print("connection made!")
                                Sounds.combo.play()
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

    # choose wire colors from array
    color_array = [
        (255,0,0), (255,128,0), (255,255,0), (255,255,255),
        (0,255,0), (0,255,255), (0,0,255), (128,128,128),
        (127,0,255), (255,0,255), (255,0,127), (0,0,0)
    ]

    wire_count = 0
    # draw wires for connections
    for node in Node.operator_nodes:
        if node.node_height == 2:  # start all connections from operator nodes
            if len(node.connections_above) >= 1 and node.connections_above[0] is not None:
                pygame.draw.line(virtual_screen, color_array[wire_count], (node.rect.left + 3, node.rect.top + 1), (node.connections_above[0].rect.left + 5, node.connections_above[0].rect.top + 12), width=2)
            if len(node.connections_above) == 2 and node.connections_above[1] is not None:
                pygame.draw.line(virtual_screen, color_array[wire_count], (node.rect.left + 8, node.rect.top + 1), (node.connections_above[1].rect.left + 5, node.connections_above[1].rect.top + 12), width=2)
            if node.connection_below is not None:
                pygame.draw.line(virtual_screen, color_array[wire_count], (node.rect.left + 3, node.rect.top + 15), (node.connection_below.rect.left + 5, node.connection_below.rect.top + 1), width=2)
        wire_count += 1  # iterate here so each operator gets own wire color (6<11, don't worry about access errors)

    # draw wire from current selected node to mouse
    if recently_selected is not None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pos = (mouse_x / xScale, mouse_y / yScale)
        if recently_selected.node_height == 1: # input node
            pygame.draw.line(virtual_screen, (100,0,0), (recently_selected.rect.left + 5, recently_selected.rect.top + 12), mouse_pos, width=2)
        elif recently_selected.node_height == 2:  # operator node
            if recently_selected.selected_prong == 0:
                pygame.draw.line(virtual_screen, (100,0,0), (recently_selected.rect.left + 3, recently_selected.rect.top + 1), mouse_pos, width=2)
            elif recently_selected.selected_prong == 1:
                pygame.draw.line(virtual_screen, (100,0,0), (recently_selected.rect.left + 8, recently_selected.rect.top + 1), mouse_pos, width=2)
            elif recently_selected.selected_prong == 2:
                pygame.draw.line(virtual_screen, (100,0,0), (recently_selected.rect.left + 3, recently_selected.rect.top + 15), mouse_pos, width=2)
        elif recently_selected.node_height == 3:  # output node
            pygame.draw.line(virtual_screen, (100,0,0), (recently_selected.rect.left + 5, recently_selected.rect.top + 1), mouse_pos, width=2)

    # evaluate connections
    output_diffs = [None, None, None, None]
    display_diffs = ['X', 'X', 'X', 'X']
    total_diff = 0
    i = 0
    for node in nodes:
        if node.node_height == 3:
            if len(node.connections_above) == 1:
                if node.connections_above[0].cur_result is not None:
                    output_diffs[i] = node.connections_above[0].cur_result - node.expected_out
                    total_diff += output_diffs[i]
                    if output_diffs[i] > 0:
                        display_diffs[i] = '+'
                    elif output_diffs[i] < 0:
                        display_diffs[i] = '-'
                    elif output_diffs[i] == 0:
                        display_diffs[i] = '='
            i += 1

    display = [13, 13, 13, 13]
    displayRect = pygame.Rect(170 + 19, 20 + 24, 5, 9)
    if Player.checkItem(Items.multimeter):
        if multimeter_status: # total difference
            virtual_screen.blit(multimeter, (170, 20))
            string = str(abs(total_diff))            
            while(len(string) < 4):
                string = "0" + string
                
            if (total_diff < 0):
                display[0] = 11
            for i in range(1, len(string)):
                num = int(string[i])
                display[i] = num
            
        else:
            virtual_screen.blit(multimeter_toggled, (170, 20))
            for i in range(4):
                match display_diffs[i]:
                    case 'X':
                        display[i] = 10
                    case '+':
                        display[i] = 12
                    case '-':
                        display[i] = 11
                    case '=':
                        display[i] = 0

        virtual_screen.blit(numbers[display[0]], (displayRect.x, displayRect.y))
        virtual_screen.blit(numbers[display[1]], (displayRect.x + 6, displayRect.y))
        virtual_screen.blit(numbers[display[2]], (displayRect.x + 12, displayRect.y))
        virtual_screen.blit(numbers[display[3]], (displayRect.x + 18, displayRect.y))

    # check if puzzle is solved
    correct = 0
    for num in output_diffs:
        if num is not None:
            if num == 0:
                correct += 1
    if correct == 4:
        solved = True
        
    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale