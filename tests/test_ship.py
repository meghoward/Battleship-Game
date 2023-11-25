from battleship.ship import Ship, ShipFactory

def test_horizontal():
    start = (4, 5)
    end = (2, 5)
    ship = Ship(start=start, end=end)
    output = ship.is_horizontal()
    print(output)
    assert output == True

def test_ships():
    ship = Ship(start=(3, 3), end=(5, 3))
    print(ship.get_cells())
    print(ship.is_horizontal())
    print(ship.is_vertical())
    print(ship.length())
    print(ship.is_near_cell((5, 3)))
    
    print(ship.receive_damage((4, 3)))
    print(ship.receive_damage((5, 3)))
    print(ship.receive_damage((3, 3)))  
    print("Has sunk?", ship.has_sunk())    
    print(ship.receive_damage((10, 3)))
    print(ship.damaged_cells)
    
    ship2 = Ship(start=(3, 4), end=(5, 4))
    print(ship.is_near_ship(ship2))

    # For Task 3
    ships = ShipFactory().generate_ships()
    print(ships)


if __name__ == "__main__":
    test_horizontal()
    test_ships()