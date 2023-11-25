from battleship.player import RandomPlayer

def test_player():
    player = RandomPlayer("Alice")
    print(player.select_target())
    print(player.select_target())
    print(player.select_target())
    
def is_cell_on_min_edge(cell):
    """ Check whether a cell is on the edge or outside the board.

    Args:
        cell (tuple[int, int]): (x, y) cell coordinates to check

    Returns:
        bool: True if the cell is on the edge or outside the board's boundaries.
    """
    
    on_left_edge = cell[0] == 1
    on_top_edge = cell[1] == 1
    
    return on_left_edge or on_top_edge

print("is_cell_on_min_edge: ", is_cell_on_min_edge((1,5)))
    
if __name__ == "__main__":
    test_player()