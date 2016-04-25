import os

from player import *


class Game:
    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        self.start_game()

    def start_game(self):
        # init state
        self.ask_for_name_to_start_the_game()
        self.ask_for_place_ship(self.player1)
        self.ask_for_place_ship(self.player2)
        # for debugging
        #self.auto_fill_boards()

        # game play
        while self.player1.alive and self.player2.alive:
            self.take_turn(guessing_player=self.player1, being_guessed_player=self.player2)
            if not self.player2.alive:
                break
            self.take_turn(guessing_player=self.player2, being_guessed_player=self.player1)

        # end game
        Game.clear_screen()
        if self.player1.alive:
            print('Congratulations, {} won the game!'.format(self.player1.name))
        elif self.player2.alive:
            print('Congratulations, {} won the game!'.format(self.player2.name))

    def ask_for_name_to_start_the_game(self):
        Game.clear_screen()
        self.player1.name = input("Please set player1's name: ")
        Game.clear_screen()
        self.player2.name = input("Please set player2's name: ")
        Game.clear_screen()
        print("Player1's name is {}.".format(self.player1.name))
        print("Player2's name is {}.".format(self.player2.name))
        input('Press any key to continue')
        Game.clear_screen()

    def ask_for_place_ship(self, player):
        for ship_name, ship_length in SHIP_INFO:
            self.print_board(player.board)
            print("{}'s turn".format(player.name))
            location = input("Place the top left location of the {name} ({length} spaces):".format(name=ship_name, length=ship_length)).lower()
            is_horizontal = input("Is it horizontal? (Y)/N:").lower() != 'n'
            while True:
                message = player.place_ship(location, ship_name, ship_length, is_horizontal)
                if message == 'success':
                    break
                self.print_board(player.board)
                print(message)
                location = input("Place the top left location of the {name} ({length} spaces):".format(name=ship_name, length=ship_length)).lower()
                is_horizontal = input("Is it horizontal? (Y)/N:").lower() != 'n'
        Game.clear_screen()

    @staticmethod
    def take_turn(guessing_player, being_guessed_player):
        # hand over to another player
        input("{}'s turn, press any key to continue".format(guessing_player.name))
        Game.clear_screen()

        # input guessing and validate
        Game.print_battle_board(guessing_player.enemy_board, guessing_player.board)
        location = input("{}, select a location to shoot at:".format(guessing_player.name)).lower()
        message = Game.validate_battle_location(location, guessing_player)
        while message != 'success':
            Game.clear_screen()
            Game.print_battle_board(guessing_player.enemy_board, guessing_player.board)
            print(message)
            location = input("{}, select a location to shoot at:".format(guessing_player.name)).lower()
            message = Game.validate_battle_location(location, guessing_player)

        # process guessing logic
        horizontal_position = ord(location[0]) - 97
        vertical_position = int(location[1:]) - 1
        if being_guessed_player.board[vertical_position][horizontal_position] == EMPTY:
            state = 'MISS'
            guessing_player.enemy_board[vertical_position][horizontal_position] = MISS
        elif being_guessed_player.board[vertical_position][horizontal_position] == HORIZONTAL_SHIP or being_guessed_player.board[vertical_position][horizontal_position] == VERTICAL_SHIP:
            data = being_guessed_player.check_sunk(vertical_position=vertical_position, horizontal_position=horizontal_position, board=guessing_player.enemy_board)
            if not data:
                # hit but not sunk yet
                state = 'HIT'
                guessing_player.enemy_board[vertical_position][horizontal_position] = HIT
                being_guessed_player.board[vertical_position][horizontal_position] = HIT
            else:
                # sunk a ship
                state = 'SUNK'
                is_horizontal, h_p, v_p, length = data
                if is_horizontal:
                    for h_index in range(h_p, h_p + length):
                        guessing_player.enemy_board[vertical_position][h_index] = SUNK
                        being_guessed_player.board[vertical_position][h_index] = SUNK
                else:
                    for v_index in range(v_p, v_p + length):
                        guessing_player.enemy_board[v_index][horizontal_position] = SUNK
                        being_guessed_player.board[v_index][horizontal_position] = SUNK

        # print the new result
        Game.print_battle_board(guessing_player.enemy_board, guessing_player.board)
        if state == 'MISS':
            print('Oops, you missed')
        elif state == 'HIT':
            print('Yeah, you hit it')
        elif state == 'SUNK':
            print('Great! You sunk the ship')

    # helper function
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_board_heading():
        print("   " + " ".join([chr(c) for c in range(ord('A'), ord('A') + BOARD_SIZE)]))

    @staticmethod
    def print_board(board):
        Game.clear_screen()
        Game.print_board_heading()

        row_num = 1
        for row in board:
            print(str(row_num).rjust(2) + " " + (" ".join(row)))
            row_num += 1

    @staticmethod
    def print_battle_board(enemy_board, my_board):
        Game.clear_screen()
        print("Enemy board")
        Game.print_board_heading()

        row_num = 1
        for row in enemy_board:
            print(str(row_num).rjust(2) + " " + (" ".join(row)))
            row_num += 1

        print("My board")
        Game.print_board_heading()

        row_num = 1
        for row in my_board:
            print(str(row_num).rjust(2) + " " + (" ".join(row)))
            row_num += 1

    @staticmethod
    def validate_battle_location(location, player):
        # validate format
        try:
            horizontal_position = ord(location[0]) - 97
            vertical_position = int(location[1:]) - 1
        except:
            return 'invalid location type, you input should look like: a1'
        if not (0 <= horizontal_position < 10) or not (0 <= vertical_position < 10):
            return 'invalid location position'

        # validate redundant guess
        if player.enemy_board[vertical_position][horizontal_position] != EMPTY:
            return 'you already guessed this block'

        return 'success'

    def auto_fill_boards(self):
        self.player1.name = 'Vincent'
        self.player2.name = 'Saya'

        print(self.player1.place_ship('a1', 'Aircraft Carrier', 5, True))
        print(self.player1.place_ship('a2', 'Battleship', 4, False))
        print(self.player1.place_ship('b2', 'Submarine', 3, True))
        print(self.player1.place_ship('b3', 'Cruiser', 3, False))
        print(self.player1.place_ship('c3', 'Patrol Boat', 2, True))

        print(self.player2.place_ship('a1', 'Aircraft Carrier', 5, True))
        print(self.player2.place_ship('a2', 'Battleship', 4, False))
        print(self.player2.place_ship('b2', 'Submarine', 3, True))
        print(self.player2.place_ship('b3', 'Cruiser', 3, False))
        print(self.player2.place_ship('c3', 'Patrol Boat', 2, True))

        self.player1.print_ships()
        self.player2.print_ships()

#Game()
