import random

from battleship.board import Board
from battleship.convert import CellConverter

class Player:
    """ Class representing the player
    """
    count = 0  # for keeping track of number of players
    
    def __init__(self, board=None, name=None):
        """ Initialises a new player with its board.

        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """
        
        if board is None:
            self.board = Board()
        else:
            self.board = board
        
        Player.count += 1
        if name is None:
            self.name = f"Player {self.count}"
        else:
            self.name = name
    
    def __str__(self):
        return self.name
    
    def select_target(self):
        """ Select target coordinates to attack.
        
        Abstract method that should be implemented by any subclasses of Player.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        raise NotImplementedError
    
    def receive_result(self, is_ship_hit, has_ship_sunk):
        """ Receive results of latest attack.
        
        Player receives notification on the outcome of the latest attack by the 
        player, on whether the opponent's ship is hit, and whether it has been 
        sunk. 
        
        This method does not do anything by default, but can be overridden by a 
        subclass to do something useful, for example to record a successful or 
        failed attack.
        
        Returns:
            None
        """
        return None
    
    def has_lost(self):
        """ Check whether player has lost the game.
        
        Returns:
            bool: True if and only if all the ships of the player have sunk.
        """
        return self.board.have_all_ships_sunk()


class ManualPlayer(Player):
    """ A player playing manually via the terminal
    """
    def __init__(self, board, name=None):
        """ Initialise the player with a board and other attributes.
        
        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """
        super().__init__(board=board, name=name)
        self.converter = CellConverter((board.width, board.height))
        
    def select_target(self):
        """ Read coordinates from user prompt.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        print(f"It is now {self}'s turn.")

        while True:
            try:
                coord_str = input('coordinates target = ')
                x, y = self.converter.from_str(coord_str)
                return x, y
            except ValueError as error:
                print(error)


class RandomPlayer(Player):
    """ A Player that plays at random positions.

    However, it does not play at the positions:
    - that it has previously attacked
    """
    def __init__(self, name=None):
        """ Initialise the player with an automatic board and other attributes.
        
        Args:
            name (str): Player's name
        """
        # Initialise with a board with ships automatically arranged.
        super().__init__(board=Board(), name=name)
        self.tracker = set()

    def select_target(self):
        """ Generate a random cell that has previously not been attacked.
        
        Also adds cell to the player's tracker.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        target_cell = self.generate_random_target()
        self.tracker.add(target_cell)
        return target_cell

    def generate_random_target(self):
        """ Generate a random cell that has previously not been attacked.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        has_been_attacked = True
        random_cell = None
        
        while has_been_attacked:
            random_cell = self.get_random_coordinates()
            has_been_attacked = random_cell in self.tracker

        return random_cell

    def get_random_coordinates(self):
        """ Generate random coordinates.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        x = random.randint(1, self.board.width)
        y = random.randint(1, self.board.height)
        return (x, y)


class AutomaticPlayer(Player):
    """ Player playing automatically using a strategy."""
    def __init__(self, name=None):
        """ Initialise the player with an automatic board and other attributes.
        
        Args:
            name (str): Player's name
        """
        # Initialise with a board with ships automatically arranged.
        super().__init__(board=Board(), name=name)
        self.board.name = "Robot"
        
        # Set of cells that have been attacked
        self.tracker = set()
        self.target_coordinates = ()
        self.unsuccessful_hit_coordinates = []
        self.successful_hit_coordinates = []
        self.possible_cells = [(x,y) for x in range(1,self.board.width + 1) for y in range(1, self.board.height + 1)]

    def is_vertical(self):
        """ Check whether the ship is vertical.
        
        Returns:
            bool : True if the ship is vertical. False otherwise.
        """
        # TODO:
        if len(self.successful_hit_coordinates) >= 2:
            x_coords = []
            y_coords = []
            for coordinates in self.successful_hit_coordinates:
                x_coords.append(coordinates[0])
                y_coords.append(coordinates[1])
        if x_coords[0] == x_coords[1]:
            return True
        
        # Ship is horizontal
        else:
            return False

    def is_cell_on_left_edge(self, cell):
        """ Check whether a cell is on the edge or outside the board.

        Args:
            cell (tuple[int, int]): (x, y) cell coordinates to check

        Returns:
            bool: True if the cell is on the edge or outside the board's boundaries.
        """
        on_left_edge = cell[0] == 1
        return on_left_edge

    def is_cell_on_top_edge(self, cell):
        """ Check whether a cell is on the edge or outside the board.

        Args:
            cell (tuple[int, int]): (x, y) cell coordinates to check

        Returns:
            bool: True if the cell is on the edge or outside the board's boundaries.
        """
        on_top_edge = cell[1] == 1
        return on_top_edge

    def is_cell_on_right_edge(self, cell):
        """ Check whether a cell is on the edge or outside the board.

        Args:
            cell (tuple[int, int]): (x, y) cell coordinates to check

        Returns:
            bool: True if the cell is on the edge or outside the board's boundaries.
        """
        on_right_edge = cell[0] == self.board.width
        return on_right_edge

    def is_cell_on_bottom_edge(self, cell):
        """ Check whether a cell is on the edge or outside the board.

        Args:
            cell (tuple[int, int]): (x, y) cell coordinates to check

        Returns:
            bool: True if the cell is on the edge or outside the board's boundaries.
        """
        on_bottom_edge = cell[1] == self.board.height
        return on_bottom_edge

    def is_valid_target(self, cell):
        return (cell in self.possible_cells)   
        
    def select_target(self):
        """ Select target coordinates to attack.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        
        if len(self.successful_hit_coordinates) < 1:
            # select_random_target in self.possible_cells
            self.target_coordinates = self.select_random_target()

            # Removes cell from the player's possible options
            self.possible_cells.remove(self.target_coordinates)
 
        # 1. If a square has been hit, I want to keep shooting nearby.
        # First at random either select horizontal or vertical strategy
        if len(self.successful_hit_coordinates) == 1:
            
            while self.target_coordinates not in self.possible_cells: 
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
                current_hit = self.successful_hit_coordinates[0]
                
                for dx, dy in directions:
                    potential_target = (current_hit[0] + dx, current_hit[1] + dy)
                    if self.is_valid_target(potential_target):
                        self.target_coordinates = potential_target
                        break

                else:
                    print("len ==1 conditions not met")
                    self.target_coordinates = self.select_random_target()

                self.possible_cells.remove(self.target_coordinates)
                return self.target_coordinates


        if len(self.successful_hit_coordinates) >= 2:
            # Then check whether to use a horizontal or vertical strategy
            while self.target_coordinates not in self.possible_cells: 
                if self.is_vertical():
                    # Check the length of the list to find out where the start and end (max & min) of my vertical section are for my next hit. 
                    min_y_coord = min([coord[1] for coord in self.successful_hit_coordinates])
                    max_y_coord = max([coord[1] for coord in self.successful_hit_coordinates])
                    x = self.successful_hit_coordinates[0][0]
                    
                    # Just checking that either end hasn't already been hit and isn't off the edge of the board or otherwise in the possible squares 
                    if (x, max_y_coord + 1) in self.possible_cells and not self.is_cell_on_bottom_edge((x, max_y_coord)):
                        self.target_coordinates = (x, max_y_coord + 1)
                        break
                    
                    elif (x, min_y_coord - 1) in self.possible_cells and not self.is_cell_on_top_edge((x, min_y_coord)):
                        self.target_coordinates = (x, min_y_coord - 1)
                        break

                    elif any((x, y) in self.possible_cells for y in range(min_y_coord, max_y_coord + 1)):
                        # Find a cell within the vertical range that is a valid target
                        for y in range(min_y_coord, max_y_coord + 1):
                            if (x, y) in self.possible_cells:
                                self.target_coordinates = (x, y)
                                break

                    else:
                        print("vertical >2 conditions not met")
                        self.target_coordinates = self.select_random_target()

                else:
                    # Check the length of the list to find out where the start and end (max & min) of my horizontal section are for my next hit.
                    min_x_coord = min([coord[0] for coord in self.successful_hit_coordinates])
                    max_x_coord = max([coord[0] for coord in self.successful_hit_coordinates])
                    y = self.successful_hit_coordinates[0][1]

                    # Just checking that either end hasn't already been hit
                    if (min_x_coord  - 1, y) in self.possible_cells and not self.is_cell_on_left_edge((min_x_coord, y)):
                        self.target_coordinates = (min_x_coord  - 1, y)
                        break
                    
                    elif (max_x_coord + 1, y) in self.possible_cells and not self.is_cell_on_right_edge((max_x_coord, y)):
                        self.target_coordinates = (max_x_coord  + 1, y)
                        break

                    elif any((x, y) in self.possible_cells for x in range(min_x_coord, max_x_coord + 1)):
                        # Find a cell within the vertical range that is a valid target
                        for x in range(min_x_coord, max_x_coord + 1):
                            if (x, y) in self.possible_cells:
                                self.target_coordinates = (x, y)
                                break

                    else:
                        print("horizontal >2 conditions not met")
                        self.target_coordinates = self.select_random_target()

            # Also removes cell from the player's tracker
            self.possible_cells.remove(self.target_coordinates)

        # print("target_coordinates: ", self.target_coordinates)
        return self.target_coordinates
    
    def select_random_target(self):
        """ Generate a random cell that has previously not been attacked for the first attack.
        
        Also adds cell to the player's tracker.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        # Get random coordinates:

        # Generate a random cell that has previously not been attacked
        if not self.possible_cells:
            print("self.possible_cells: ", self.possible_cells)
            return None
        random_cell = random.choice(self.possible_cells)
        return random_cell

    
    def receive_result(self, is_ship_hit, has_ship_sunk):
        """ Receive results of latest attack.
        
        Player receives notification on the outcome of the latest attack by the 
        player, on whether the opponent's ship is hit, and whether it has been 
        sunk. 
        
        This method does not do anything by default, but can be overridden by a 
        subclass to do something useful, for example to record a successful or 
        failed attack.
        
        Returns:
            None
        """
        # Appends my hit entries to my hit_coordinates list attribute for checking against my strategy
        if is_ship_hit:
            self.successful_hit_coordinates.append(self.target_coordinates)

            if has_ship_sunk:
                for cell in self.successful_hit_coordinates:
                    for neighbour in self.get_neighbours_inc_diag(cell):
                        if neighbour in self.possible_cells and neighbour not in self.successful_hit_coordinates:
                            self.possible_cells.remove(neighbour)
                self.successful_hit_coordinates = []

        else:
            self.unsuccessful_hit_coordinates.append(self.target_coordinates)
            
        return None
    
    def get_neighbours_inc_diag(self, cell):
        x,y = cell
        neighbours = []

        for x_coord in [-1,0,1]:
            for y_coord in [-1,0,1]:
                if x_coord == 0 and y_coord == 0:
                    continue
                
                neighbouring_x, neighbouring_y = x + x_coord, y + y_coord
                if 1<= neighbouring_x <= self.board.width and 1 <= neighbouring_y <= self.board.height:
                    neighbours.append((neighbouring_x, neighbouring_y))

        return neighbours
    

    def has_lost(self):
        """ Check whether player has lost the game.
        
        Returns:
            bool: True if and only if all the ships of the player have sunk.
        """
        return self.board.have_all_ships_sunk()


