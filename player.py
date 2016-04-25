SHIP_INFO = [
    ("Aircraft Carrier", 5),
    ("Battleship", 4),
    ("Submarine", 3),
    ("Cruiser", 3),
    ("Patrol Boat", 2)
]

BOARD_SIZE = 10

VERTICAL_SHIP = '|'
HORIZONTAL_SHIP = '-'
EMPTY = 'O'
MISS = '.'
HIT = '*'
SUNK = '#'


class Player:
    def __init__(self):
        self.name = 'default'
        self.board = []
        self.ships = {} # ships = ("Cruiser", 3, 2, 0,True, False) maps to (name, length, horizontal_position, vertical_position, is_horizontal, is_sunk)
        self.enemy_board = []
        self.alive = True
        for i in range(10):
            self.board.append([EMPTY for _ in range(10)])
            self.enemy_board.append([EMPTY for _ in range(10)])

    def place_ship(self, location, ship_name, ship_length, is_horizontal):
        # expected location type: 'a2', ship_length: 5, is_horizontal: True
        # verify location type
        try:
            horizontal_position = ord(location[0]) - 97
            vertical_position = int(location[1:]) - 1
        except:
            return 'invalid location type, you input should look like: a1'
        if is_horizontal and (not (0 <= horizontal_position < 11 - ship_length) or not (0 <= vertical_position < 10)):
            return 'invalid location position'
        if (not is_horizontal) and (not (0 <= horizontal_position < 10) or not (0 <= vertical_position < 11 - ship_length)):
            return 'invalid location position'

        # verify location not occupied on board
        if is_horizontal:
            for i in range(horizontal_position, horizontal_position + ship_length):
                if self.board[vertical_position][i] != EMPTY:
                    return 'ships can not be overlap'
        else:
            for j in range(vertical_position, vertical_position + ship_length):
                if self.board[j][horizontal_position] != EMPTY:
                    return 'ships can not be overlap'

        # place the ship
        self.ships[ship_name] = (ship_length, horizontal_position, vertical_position, is_horizontal, False)
        if is_horizontal:
            for i in range(horizontal_position, horizontal_position + ship_length):
                self.board[vertical_position][i] = HORIZONTAL_SHIP
        else:
            for j in range(vertical_position, vertical_position + ship_length):
                self.board[j][horizontal_position] = VERTICAL_SHIP
        return 'success'

    def check_sunk(self, horizontal_position, vertical_position, board):
        # board is the reference board where being attacked
        for item in self.ships.items():
            (name, value) = item
            (length, h_p, v_p, is_horizontal, is_sunk) = value
            if is_sunk:
                continue
            if is_horizontal:
                if not (h_p <= horizontal_position < h_p + length) or vertical_position != v_p:
                    continue
                check_hit = True
                for i in range(h_p, h_p + length):
                    if i == horizontal_position:
                        continue
                    if board[vertical_position][i] != HIT:
                        check_hit = False
                if not check_hit:
                    continue

                # this ship sunk
                self.ships[name] = (length, h_p, v_p, is_horizontal, True)
                # check if game over
                some_ship_alive = False
                for ship in self.ships.items():
                    (_, val) = ship
                    (_, _, _, _, sunk_or_not) = val
                    if not sunk_or_not:
                        some_ship_alive = True
                if not some_ship_alive:
                    self.alive = False
                return True, h_p, v_p, length
            else:
                if h_p != horizontal_position or not (v_p <= vertical_position < v_p + length):
                    continue
                check_hit = True
                for j in range(v_p, v_p + length):
                    if j == vertical_position:
                        continue
                    if board[j][horizontal_position] != HIT:
                        check_hit = False
                if not check_hit:
                    continue
                # This ship sunk
                self.ships[name] = (length, h_p, v_p, is_horizontal, True)
                # check if game over
                some_ship_alive = False
                for ship in self.ships.items():
                    (_, val) = ship
                    (_, _, _, _, sunk_or_not) = val
                    if not sunk_or_not:
                        some_ship_alive = True
                if not some_ship_alive:
                    self.alive = False
                return False, h_p, v_p, length
        return None

    def print_ships(self):
        for item in self.ships.items():
            print(item)
