import random
from battleship.convert import CellConverter

class Ship:
    """ Represent a ship that is placed on the board.
    """
    def __init__(self, start, end, should_validate=True):
        """ Creates a ship given its start and end coordinates on the board. 
        
        The order of the cells do not matter.

        Args:
            start (tuple[int, int]): tuple of 2 positive integers representing
                the starting cell coordinates of the Ship on the board
            end (tuple[int, int]): tuple of 2 positive integers representing
                the ending cell coordinates of the Ship on the board
            should_validate (bool): should the constructor check whether the 
                given coordinates result in a horizontal or vertical ship? 
                Defaults to True.

        Raises:
            ValueError: if should_validate==True and 
                if the ship is neither horizontal nor vertical
        """
        # Start and end (x, y) cell coordinates of the ship
        self.x_start, self.y_start = start
        self.x_end, self.y_end = end

        # make x_start on left and x_end on right
        self.x_start, self.x_end = (
            min(self.x_start, self.x_end), max(self.x_start, self.x_end)
        )
        
        # make y_start on top and y_end on bottom
        self.y_start, self.y_end = (
            min(self.y_start, self.y_end), max(self.y_start, self.y_end)
        )
        
        if should_validate:
            if not self.is_horizontal() and not self.is_vertical():
                raise ValueError("The given coordinates are invalid. "
                    "The ship needs to be either horizontal or vertical.")

        # Set of all (x,y) cell coordinates that the ship occupies
        self.cells = self.get_cells()
        
        # Set of (x,y) cell coordinates of the ship that have been damaged
        self.damaged_cells = set()
    
    def __len__(self):
        return self.length()
        
    def __repr__(self):
        return (f"Ship(start=({self.x_start},{self.y_start}), "
            f"end=({self.x_end},{self.y_end}))")
        
    def is_vertical(self):
        """ Check whether the ship is vertical.
        
        Returns:
            bool : True if the ship is vertical. False otherwise.
        """
        # TODO: 
        # Complete this method - self.x_start, self.y_start, self.x_end, self.y_end
        if self.x_start == self.x_end:
            return True
        else:
            return False
   
    def is_horizontal(self):
        """ Check whether the ship is horizontal.
        
        Returns:
            bool : True if the ship is horizontal. False otherwise.
        """
        # TODO: Complete this method
        if self.y_start == self.y_end:
            return True
        else:
            return False
    
    def get_cells(self):
        """ Get the set of all cell coordinates that the ship occupies.
        
        For example, if the start cell is (3, 3) and end cell is (5, 3),
        then the method should return {(3, 3), (4, 3), (5, 3)}.
        
        This method is used in __init__() to initialise self.cells
        
        Returns:
            set[tuple] : Set of (x ,y) coordinates of all cells a ship occupies
        """
        # TODO: Complete this method       
        cells = set()
        if self.is_horizontal():
            for x_coord in range(self.x_start, self.x_end +1):
                cells.add((x_coord, self.y_end))
        
        elif self.is_vertical():
            for y_coord in range(self.y_start, self.y_end +1):
                cells.add((self.x_start, y_coord))

        return cells 

    def length(self):
        """ Get length of ship (the number of cells the ship occupies).
        
        Returns:
            int : The number of cells the ship occupies
        """
        # TODO: Complete this method
        return len(self.get_cells())

    def is_occupying_cell(self, cell):
        """ Check whether the ship is occupying a given cell

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the (x, y) cell coordinates to check

        Returns:
            bool : return True if the given cell is one of the cells occupied 
                by the ship. Otherwise, return False
        """
        # TODO: Complete this method
        if cell in self.get_cells():
            return True 
        else:
            return False
    
    def receive_damage(self, cell):
        """ Receive attack at given cell. 
        
        If ship occupies the cell, add the cell coordinates to the set of 
        damaged cells. Then return True. 
        
        Otherwise return False.

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the cell coordinates that is damaged

        Returns:
            bool : return True if the ship is occupying cell (ship is hit). 
                Return False otherwise.
        """
        # TODO: Complete this method
        if self.is_occupying_cell(cell):
            self.damaged_cells.add(cell)
            return True
        else:
            return False
    
    def count_damaged_cells(self):
        """ Count the number of cells that have been damaged.
        
        Returns:
            int : the number of cells that are damaged.
        """
        # TODO: Complete this method
        return len(self.damaged_cells)
        
    def has_sunk(self):
        """ Check whether the ship has sunk.
        
        Returns:
            bool : return True if the ship is damaged at all its positions. 
                Otherwise, return False
        """
        # TODO: Complete this method
        return self.get_cells() == self.damaged_cells

    def is_near_ship(self, other_ship):
        """ Check whether a ship is near another ship instance.
        
        Hint: Use the method is_near_cell(...) to complete this method.

        Args:
            other_ship (Ship): another Ship instance against which to compare

        Returns:
            bool : returns True if and only if the coordinate of other_ship is 
                near to this ship. Returns False otherwise.
        """
        # TODO: Complete this method
        for o_cell in other_ship.get_cells():
            if self.is_near_cell(o_cell):
                return True
        else:
            return False

    def is_near_cell(self, cell):
        """ Check whether the ship is near an (x,y) cell coordinate.
        # NOTE check this out w
        In the example below:
        - There is a ship of length 3 represented by the letter S.
        - The positions 1, 2, 3 and 4 are near the ship
        - The positions 5 and 6 are NOT near the ship

        --------------------------
        |   |   |   |   | 3 |   |
        -------------------------
        |   | S | S | S | 4 | 5 |
        -------------------------
        | 1 |   | 2 |   |   |   |
        -------------------------
        |   |   | 6 |   |   |   |
        -------------------------

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the (x, y) cell coordinates to compare

        Returns:
            bool : returns True if and only if the (x, y) coordinate is at most
                one cell from any part of the ship OR is at the corner of the 
                ship. Returns False otherwise.
        """
        return (self.x_start-1 <= cell[0] <= self.x_end+1 
                and self.y_start-1 <= cell[1] <= self.y_end+1)


class ShipFactory:
    """ Class to create new ships in specific configurations."""
    def __init__(self, board_size=(10,10), ships_per_length=None):
        """ Initialises the ShipFactory class with necessary information.
        
        Args: 
            board_size (tuple[int,int]): the (width, height) of the board in 
                terms of number of cells. Defaults to (10, 10)
            ships_per_length (dict): A dict with the length of ship as keys and
                the count as values. Defaults to 1 ship each for lengths 1-5.
        """
        self.board_size = board_size
        
        if ships_per_length is None:
            # Default: lengths 1 to 5, one ship each
            self.ships_per_length = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
        else:
            self.ships_per_length = ships_per_length

    @classmethod
    def create_ship_from_str(cls, start, end, board_size=(10,10)):
        """ A class method for creating a ship from string based coordinates.
        
        Example usage: ship = ShipFactory.create_ship_from_str("A3", "C3")
        
        Args:
            start (str): starting coordinate of the ship (example: 'A3')
            end (str): ending coordinate of the ship (example: 'C3')
            board_size (tuple[int,int]): the (width, height) of the board in 
                terms of number of cells. Defaults to (10, 10)

        Returns:
            Ship : a Ship instance created from start to end string coordinates
        """
        converter = CellConverter(board_size)
        return Ship(start=converter.from_str(start),
                    end=converter.from_str(end))

    def generate_ships(self):
        """ Generate a list of ships in the appropriate configuration.
        
        The number and length of ships generated must obey the specifications 
        given in self.ships_per_length.
        
        The ships must also not overlap with each other, and must also not be 
        too close to one another (as defined earlier in Ship::is_near_ship())
        
        The coordinates should also be valid given self.board_size
        
        Returns:
            list[Ships] : A list of Ship instances (+ start and end coords), adhering to the rules above
        """
        # TODO: Complete this method
        ships = []
        ship_cells = set()

        # NOTE I think I may still need to check valid lengths and stuff? Ask helper ** 
        # I want to iterate through each of the ship entries in the self.ships_per_length, 
        for ship_length, ship_quantity in sorted(self.ships_per_length.items(), key = lambda x:x[0], reverse = True):
            if ship_quantity > 0:
                for _ in range(ship_quantity):
                    valid_ship = False
                    attempts = 0 

                    while not valid_ship and attempts < 100:
                        attempts += 1
                        valid_ship = True 

                        if random.choice(['horizontal', 'vertical']) == 'horizontal':
                            x_start = random.randint(1, 10 - ship_length)
                            y_start = random.randint(1, 10)

                            x_end = x_start + ship_length - 1
                            y_end = y_start

                        else:
                            x_start = random.randint(1, 10)
                            y_start = random.randint(1, 10 - ship_length)

                            x_end = x_start
                            y_end = y_start + ship_length - 1

                        new_ship = Ship((x_start, y_start), (x_end, y_end))

                        new_ship_cells = set(new_ship.get_cells())
                        if any(new_cell in ship_cells for new_cell in new_ship_cells):
                            valid_ship = False
                            continue  # Skip the rest of the loop and try again

                        if any(new_ship.is_near_ship(existing_ship) for existing_ship in ships):
                            valid_ship = False
                            continue  # Skip the rest of the loop and try again

                        # If we made it here, the ship is valid
                        ships.append(new_ship)
                        ship_cells.update(new_ship_cells)

                    if attempts == 100:
                        raise RuntimeError(f"Unable to place ship of length {ship_length} after 100 attempts.")
                # print("for _ in range(ship_quantity): ships, ship_cells: ", ships, ship_cells)
        return ships
        
        
if __name__ == '__main__':
    # SANDBOX for you to play and test your methods

    ship = Ship(start=(3, 3), end=(5, 3))
    print(ship.get_cells())
    print(ship.is_horizontal())
    print(ship.is_vertical())
    print(ship.length())
    print(ship.is_near_cell((5, 3)))
    
    print(ship.receive_damage((4, 3)))
    print(ship.receive_damage((5, 3)))
    print(ship.receive_damage((3, 3)))  
    # print("Has sunk?", ship.has_sunk())    
    print(ship.receive_damage((10, 3)))
    print(ship.damaged_cells)
    
    ship2 = Ship(start=(3, 4), end=(5, 4))
    print(ship.is_near_ship(ship2))

    # For Task 3
    ships = ShipFactory().generate_ships()
    print(ships)
        
    