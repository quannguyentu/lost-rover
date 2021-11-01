""" Game to play 'Lost Rovers'. This is the file you edit.
To make more ppm files, open a gif or jpg in xv and save as ppm raw.
Put the three ADTs in their own files.

Team: Quan Nguyen Tu, Quan Zhou
CSCI 204
"""
from gameboard import *
from random import *
from LinkedList import *
from Stack import *


class Game:
    SIZE = 15  # rooms are 15x15

    def __init__(self):
        # put other instance variables here
        self.gui = GameBoard("Lost Rover", self, Game.SIZE)
        self.rover = Rover()
        self.initial_room = Room(Game.SIZE)
        self.current_room = self.initial_room
        self.create_room(self.initial_room)
        self.__undo_room = Stack()
        self.tracked_flash = None
        self.portal_list = []

    def create_room(self, room):
        if room == self.initial_room:
            room.set_up_portal()
            room.set_up_parts()
            room.set_up_ship_components()
        else:
            room.set_up_portal()
            room.set_up_parts()

    def start_game(self):
        self.gui.run()

    @staticmethod
    def get_rover_image():
        """ Called by GUI when screen updates.
            Returns image name (as a string) of the rover.
            (Likely 'rover.ppm') """
        return 'rover.ppm'

    def get_rover_location(self):
        """ Called by GUI when screen updates.
            Returns location (as a Point). """
        coordinate = self.rover.current_location()
        x = coordinate[0]
        y = coordinate[1]
        return Point(x, y)

    def get_image(self, point):
        """ Called by GUI when screen updates.
            Returns image name (as a string) or None for the part, ship component, or portal at the given
            coordinates. ('engine.ppm' or 'cake.ppm' or
            'portal.ppm', etc) """
        x = point.getX()
        y = point.getY()

        items = self.current_room.items
        item_location_list = []
        for item in items:
            item_location_list.append([item.location.x, item.location.y])

        for i in range(len(item_location_list)):
            if x == item_location_list[i][0] and y == item_location_list[i][1]:

                return items[i].get_image()
            else:
                pass

    def go_up(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        self.rover.go_up()
        self.check_portal()

    def go_down(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        self.rover.go_down()
        self.check_portal()

    def go_left(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        self.rover.go_left()
        self.check_portal()

    def go_right(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        # Your code goes here
        self.rover.go_right()
        self.check_portal()

    def show_way_back(self):
        """ Called by GUI when button clicked.
            Flash the portal leading towards home. """
        if self.__undo_room.is_empty() is False:
            # Flash the portal on top
            curr_portal = self.__undo_room.peek()
            curr_portal.flash()
            self.tracked_flash = curr_portal

    def get_inventory(self):
        """ Called by GUI when inventory updates.
            Returns entire inventory (as a string).
        3 cake
        2 screws
        1 rug
      """
        return str(self.rover.inventory)

    def pick_up(self):
        """ Called by GUI when button clicked.
        If rover is standing on a part (not a portal
        or ship component), pick it up and add it
        to the inventory. """
        for item in self.current_room.items:
            if self.rover.location == item.location:
                if isinstance(item, Parts):
                    self.rover.inventory.add(item, item.name)
                    self.current_room.items.remove(item)
                else:
                    pass

    def get_current_task(self):
        """ Called by GUI when task updates.
            Returns top task (as a string).
        'Fix the engine using 2 cake, 3 rugs' or
        'You win!'
       """
        pass  # Your code goes here

    def perform_task(self):
        """ Called by the GUI when button clicked.
            If necessary parts are in inventory, and rover
            is on the relevant broken ship piece, then fixes
            ship piece and removes parts from inventory. If
            we run out of tasks, we win. """
        pass  # Your code goes here

    # Put other methods here as needed.
    def check_portal(self):
        item_portal_index = []
        for i in range(len(self.current_room.items)):
            if type(self.current_room.items[i]) == Portals:
                item_portal_index.append(i)
        for i in item_portal_index:
            if self.rover.location == self.current_room.items[i].location:
                portal = self.current_room.items[i]
                # pop the portal after stepping on the portal to other room
                if self.__undo_room.is_empty() is False and self.__undo_room.peek() is portal:
                    self.__undo_room.pop()
                if self.tracked_flash is not None:
                    self.tracked_flash.unflash()
                # Establish a new linked room if the portal doesnt have any linked room
                if portal.linked_portal is None:
                    self.link_portal(portal)
                    break
                # Else go to the linked room
                else:
                    self.current_room = portal.linked_room
                    if portal in self.portal_list:
                        self.__undo_room.push(portal.linked_portal)
                    break

    def link_portal(self, portal):
        # Set up the new room
        new_room = Room(15)
        new_portal = Portals()
        self.create_room(new_room)
        # Create a new portal in the same location
        new_portal.location = portal.location
        new_room.items.append(new_portal)
        self.__undo_room.push(new_portal)
        # Link the two portal
        portal.linked_portal = new_portal
        new_portal.linked_portal = portal
        # Link the room
        portal.linked_room = new_room
        new_portal.linked_room = self.current_room
        # Go to the new room
        self.current_room = new_room
        self.portal_list.append(portal)

# Put other classes here or in other files as needed.


class Location:
    x = 0
    y = 0

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, location):
        return self.x == location.x and self.y == location.y


class Room:
    def __init__(self, size):
        self.size = size
        self.items = []
        self.num_portals = randint(2, 4)
        self.num_parts = randint(6, 12)
        self.parts_name = ['gear', 'screw', 'cake', 'bagel', 'lettuce']

    def set_up_portal(self):
        for i in range(self.num_portals):
            obj = Portals()
            self.items.append(obj)

    # return self.items

    def set_up_parts(self):
        for i in self.parts_name:
            obj = Parts(i)
            self.items.append(obj)
        for i in range(self.num_parts - len(self.parts_name)):
            obj = Parts(choice(self.parts_name))
            self.items.append(obj)

    def set_up_ship_components(self):
        ship1 = ShipComponents(Location(5, 6), 'cabin', 'broken')
        ship2 = ShipComponents(Location(5, 7), 'cabin')
        ship3 = ShipComponents(Location(6, 6), 'engine', 'broken')
        ship4 = ShipComponents(Location(6, 7), 'engine')
        ship5 = ShipComponents(Location(8, 6), 'exhaust')
        ship6 = ShipComponents(Location(5, 6), 'exhaust', 'broken')
        ship_components = [ship1, ship2, ship3, ship4, ship5, ship6]
        for i in ship_components:
            self.items.append(i)

    def get_item(self, point):

        for i in range(len(self.items)):
            if type(self.items[i]) == int:
                pass
            else:
                if self.items[i].get_location().x == point.x and self.items[i].get_location().y == point.y:
                    return self.items[i]


class Items:
    def __init__(self):
        self.location = Location(randint(0, Game.SIZE - 1), randint(0, Game.SIZE - 1))
        self.name = ''

    def get_location(self):
        return Point(self.location.x, self.location.y)

    def get_image(self):
        return self.name + '.ppm'


class Portals(Items):
    def __init__(self):
        """Portal class with default name: Portal"""
        super().__init__()
        self.name = 'portal'
        self.linked_portal = None
        self.linked_room = None

    def get_image(self):
        return self.name + ".ppm"

    def flash(self):
        self.name = "portal-flashing"

    def unflash(self):
        self.name = "portal"


class Parts(Items):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.amount = 0


class ShipComponents(Items):
    def __init__(self, location, name, state=''):
        super().__init__()
        self.location = location
        self.name = name
        self.state = state

    def get_image(self):
        i = self.name + self.state + '.ppm'
        return i


class Rover:
    def __init__(self):
        self.location = Location(randint(0, (Game.SIZE - 1)), randint(0, (Game.SIZE - 1)))
        self.inventory = LinkedList()

    def current_location(self):
        """Get the current coordination in the tuple format (x,y)"""
        return self.location.x, self.location.y

    def go_up(self):
        """If legal, moves rover. If hit the border, soft wrap. If the robot lands on a portal, it will teleport. """
        if self.location.y != 0:
            self.location.y -= 1
        else:
            self.location.y = (Game.SIZE - 1)

        return self.location.y

    def go_down(self):
        """If legal, moves rover. If hit the border, soft wrap. If the robot lands on a portal, it will teleport. """
        if self.location.y != (Game.SIZE - 1):
            self.location.y += 1
        else:
            self.location.y = 0

        return self.location.y

    def go_left(self):
        """If legal, moves rover. If hit the border, soft wrap. If the robot lands on a portal, it will teleport. """
        if self.location.x != 0:
            self.location.x -= 1
        else:
            self.location.x = (Game.SIZE - 1)

        return self.location.x

    def go_right(self):
        """If legal, moves rover. If hit the border, soft wrap. If the robot lands on a portal, it will teleport. """
        if self.location.x != (Game.SIZE - 1):
            self.location.x += 1
        else:
            self.location.x = 0
        return self.location.x


""" Launch the game. """

g = Game()

g.start_game()  # This does not return until the game is over
