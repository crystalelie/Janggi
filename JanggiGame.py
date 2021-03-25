from termcolor import colored


class JanggiGame:
    """
    The class JanggiGame includes functions to create the game board, initialize pieces, make moves and
    check if a player is in check or checkmate. The class is responsible for running the game. It will create the game
    board and initialize the coordinates for each of the pieces. It will need to interact with each of the pieces
    classes, since the make_move function will need to validate that the move the player is attempting to make
    is valid for the particular piece that they are moving. It also will communicate with the methods to see if
    a general is in check with valid moves, or if they are in checkmate.
    """

    def __init__(self):
        """
        Initializes the following private data members, the game board, a list to hold the coordinates of each of the
        palaces, a list to hold the letters for the columns of the board, initializing the game_state to "UNFINISHED",
        the player_turn initializing to "BLUE", in_check initializing to "No" and dictionaries to hold the pieces and
        coordinates for each player.
        """
        self._board = self.create_board()
        self._letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        self._game_state = 'UNFINISHED'
        self._player_turn = "blue"
        self._in_check = None
        self._red_pieces = {"CH": [0, 0], "CH1": [8, 0], "EL": [1, 0], "EL1": [6, 0], "HR": [2, 0], "HR1": [7, 0],
                            "GD": [3, 0], "GD1": [5, 0], "GN": [4, 1], "CA": [1, 2], "CA1": [7, 2], "SD": [0, 3],
                            "SD1": [2, 3], "SD2": [4, 3], "SD3": [6, 3], "SD4": [8, 3]}
        self._blue_pieces = {"CH": [0, 9], "CH1": [8, 9], "EL": [1, 9], "EL1": [6, 9], "HR": [2, 9], "HR1": [7, 9],
                             "GD": [3, 9], "GD1": [5, 9], "GN": [4, 8], "CA": [1, 7], "CA1": [7, 7], "SD": [0, 6],
                             "SD1": [2, 6], "SD2": [4, 6], "SD3": [6, 6], "SD4": [8, 6]}

    def get_blue_pieces(self):
        """
        Returns the dictionary that holds the coordinates of each of the blue pieces
        """
        return self._blue_pieces

    def get_red_pieces(self):
        """
        Returns the dictionary that holds the coordinates of each of the red pieces
        """
        return self._red_pieces

    def get_in_check(self):
        """
        Returns the player who is currently in check. Returns None if no player is in check
        """
        return self._in_check

    def get_player_turn(self):
        """
        Returns the current player's turn
        """
        return self._player_turn

    def get_game_state(self):
        """
        Returns the game state as "UNFINISHED", "RED_WON", or "BLUE_WON"
        """
        return self._game_state

    ################################ MOVES #######################################

    def make_move(self, from_square, to_square):
        """
        Takes two string parameters, and determines the from coordinates and the to coordinates. It will check the game
        state to see if the game has already been won, then it will iterate through the opposing player's dictionary of
        pieces to verify that the piece they are trying to move is in fact their own piece. It will return false if the
        square they are trying to move to already has their own piece, since they can't capture their own piece. This
        will interact with each of the pieces' classes to validate that the coordinates that are entered are valid
        movements for the type of piece. If any part of the move is invalid, it will return false. Otherwise it will
        return true and update the coordinates for the players piece, update the gameboard, and update the players_turn
        """
        from_input_letter = from_square[0]                          # extracting the letter
        from_letter_index = self._letters.index(from_input_letter)  # turning the letter into a number based on the letter's list
        from_number_index = int(from_square[1:]) - 1                # extracting the number and subtracting 1
        from_coordinates = [from_letter_index, from_number_index]   # turning it into an ordered pair of coordinates

        to_input_letter = to_square[0]
        to_letter_index = self._letters.index(to_input_letter)
        to_number_index = int(to_square[1:]) - 1
        to_coordinates = [to_letter_index, to_number_index]

        # If a player is in check, it will validate that the move helps them move out of check
        if self._player_turn == self._in_check:
            if not self.move_out_check(from_coordinates, to_coordinates, self._player_turn):
                return False

        # If it moves them out of check, the move will be validated and the board/dictionaries will be updated
            else:
                if self._player_turn == "blue":
                    self.validate_moves("blue", from_coordinates, to_coordinates)
                    self.update_pieces('blue', from_coordinates, to_coordinates)
                    self.is_in_check("red")
                    self._player_turn = "red"
                    return True

                if self._player_turn == "red":
                    self.validate_moves("red", from_coordinates, to_coordinates)
                    self.update_pieces('red', from_coordinates, to_coordinates)
                    self.is_in_check("blue")
                    self._player_turn = "blue"
                    return True

        # If the game has already been won, then it will return False
        if self._game_state == "RED_WON" or self._game_state == "BLUE_WON":
            return False

        # If the piece that is being moved does not belong to the player who's turn it is, it will return False
        if self._player_turn == "blue" and from_coordinates in self._red_pieces.values():
            return False

        if self._player_turn == "red" and from_coordinates in self._blue_pieces.values():
            return False

        # If the move is not on the board
        if not self.on_board(to_coordinates[0], to_coordinates[1]):
            return False

        # If a player decides to pass their turn
        if from_coordinates == to_coordinates:
            if self._player_turn == "blue":
                self._player_turn = "red"
                return True
            if self._player_turn == "red":
                self._player_turn = "blue"
                return True

        # If the to coordinate already has one of the player's pieces
        if self._player_turn == "blue" and self._board[to_coordinates[0]][to_coordinates[1]] != ' | ':
            for key, value in self._blue_pieces.items():
                if value == to_coordinates:
                    return False

        if self._player_turn == "red" and self._board[to_coordinates[0]][to_coordinates[1]] != ' | ':
            for key, value in self._red_pieces.items():
                if value == to_coordinates:
                    return False

        # If the from square is empty
        if self._player_turn == "blue":
            if from_coordinates not in self._blue_pieces.values():
                return False

        if self._player_turn == "red":
            if from_coordinates not in self._red_pieces.values():
                return False

        # If the to square holds the other player's General. They are only able to put the general in check, not capture
        if self._player_turn == "blue":
            for key, value in self._red_pieces.items():
                if key == "GN" and value == to_coordinates:
                    return False

        if self._player_turn == "red":
            for key, value in self._blue_pieces.items():
                if key == "GN" and value == to_coordinates:
                    return False

        # Communicates with the piece's methods to see if the move is valid per the piece's movement rule
        if self._player_turn == "blue":
            for key, value in list(self._blue_pieces.items()):
                if value == from_coordinates:
                    piece = key
                    if piece == "CH" or piece == "CH1":
                        if not self.chariot_valid_moves(from_coordinates, to_coordinates):
                            return False

                    if piece == "EL" or piece == "EL1":
                        if not self.elephant_valid_moves(from_coordinates, to_coordinates):
                            return False

                    if piece == "HR" or piece == "HR1":
                        if not self.horse_valid_moves(from_coordinates, to_coordinates):
                            return False

                    if piece == "GD" or piece == "GD1":
                        if not self.guard_valid_moves(from_coordinates, to_coordinates):
                            return False

                    if piece == 'GN':
                        if not self.general_valid_moves(from_coordinates, to_coordinates):
                            return False

                    if piece == "CA" or piece == "CA1":
                        if not self.cannon_valid_moves(from_coordinates, to_coordinates):
                            return False

                    if piece == "SD" or piece == "SD1" or piece == "SD2" or piece == "SD3" or piece == "SD4":
                        if not self.soldier_valid_moves(from_coordinates, to_coordinates, "blue"):
                            return False
                    else:
                        continue

        if self._player_turn == "red":
            for key, value in list(self._red_pieces.items()):
                if value == from_coordinates:
                    piece = key
                    if piece == "CH" or piece == "CH1":
                        if not self.chariot_valid_moves(from_coordinates, to_coordinates):
                            return False

                    if piece == "EL" or piece == "EL1":
                        if not self.elephant_valid_moves(from_coordinates, to_coordinates):
                            return False

                    if piece == "HR" or piece == "HR1":
                        if not self.horse_valid_moves(from_coordinates, to_coordinates):
                            return False

                    if piece == "GD" or piece == "GD1":
                        if not self.guard_valid_moves(from_coordinates, to_coordinates):
                            return False

                    if piece == 'GN':
                        if not self.general_valid_moves(from_coordinates, to_coordinates):
                            return False

                    if piece == "CA" or piece == "CA1":
                        if not self.cannon_valid_moves(from_coordinates, to_coordinates):
                            return False

                    if piece == "SD" or piece == "SD1" or piece == "SD2" or piece == "SD3" or piece == "SD4":
                        if not self.soldier_valid_moves(from_coordinates, to_coordinates, "red"):
                            return False
                    else:
                        continue

        # Calls the validate_moves function to make the necessary updates to the board, pieces dictionary, and captured pieces
        # Makes sure the player's move won't put them into check
        if self._player_turn == "blue":
            self.validate_moves("blue", from_coordinates, to_coordinates)
            self.update_pieces('blue', from_coordinates, to_coordinates)
            if self.is_in_check("blue"):
                self.validate_moves("blue", to_coordinates, from_coordinates)
                self.update_pieces('blue', to_coordinates, from_coordinates)
                return False
            self.is_in_check("red")
            self._player_turn = "red"
            return True

        if self._player_turn == "red":
            self.validate_moves("red", from_coordinates, to_coordinates)
            self.update_pieces('red', from_coordinates, to_coordinates)
            if self.is_in_check("red"):
                self.validate_moves("red", to_coordinates, from_coordinates)
                self.update_pieces('red', from_coordinates, to_coordinates)
                return False
            self.is_in_check("blue")
            self._player_turn = "blue"
            return True

    def validate_moves(self, player, from_coordinates, to_coordinates):
        """
        This method is called on by the make_move method. It is set to take a player, from coordinates and to coordinates.
        It will update the board with the piece's movement and will return back to the make_move function
        """
        if player == "blue":
            self._board[to_coordinates[0]][to_coordinates[1]] = self._board[from_coordinates[0]][from_coordinates[1]]
            self._board[from_coordinates[0]][from_coordinates[1]] = ' | '

        if player == "red":
            self._board[to_coordinates[0]][to_coordinates[1]] = self._board[from_coordinates[0]][from_coordinates[1]]
            self._board[from_coordinates[0]][from_coordinates[1]] = ' | '

        return

    def update_pieces(self, player, from_coordinates, to_coordinates):
        """
        This method is called on by the make_move function. It takes a player, from coordinates, and to coordinates.
        It will look through the player's piece dictionary and will update the piece value for the piece that moved. If
        the movement caused the piece to capture a piece from the opposing player, it will remove that piece from the
        opposing player's piece dictionary
        """
        # Updates the dictionary for the coordinate of the piece moving
        if player == 'blue':
            for key, value in list(self._blue_pieces.items()):
                if value == from_coordinates:
                    if key == "CH":
                        self._blue_pieces.update(CH=to_coordinates)
                    elif key == "CH1":
                        self._blue_pieces.update(CH1=to_coordinates)
                    elif key == "EL":
                        self._blue_pieces.update(EL=to_coordinates)
                    elif key == "EL1":
                        self._blue_pieces.update(EL1=to_coordinates)
                    elif key == "HR":
                        self._blue_pieces.update(HR=to_coordinates)
                    elif key == "HR1":
                        self._blue_pieces.update(HR1=to_coordinates)
                    elif key == "GD":
                        self._blue_pieces.update(GD=to_coordinates)
                    elif key == "GD1":
                        self._blue_pieces.update(GD1=to_coordinates)
                    elif key == "GN":
                        self._blue_pieces.update(GN=to_coordinates)
                    elif key == "CA":
                        self._blue_pieces.update(CA=to_coordinates)
                    elif key == "CA1":
                        self._blue_pieces.update(CA1=to_coordinates)
                    elif key == "SD":
                        self._blue_pieces.update(SD=to_coordinates)
                    elif key == "SD1":
                        self._blue_pieces.update(SD1=to_coordinates)
                    elif key == "SD2":
                        self._blue_pieces.update(SD2=to_coordinates)
                    elif key == "SD3":
                        self._blue_pieces.update(SD3=to_coordinates)
                    elif key == "SD4":
                        self._blue_pieces.update(SD4=to_coordinates)

                # Removes the piece that has been captured, if one has been captured
            self._red_pieces = {key: value for key, value in self._red_pieces.items() if value != to_coordinates}

        if player == 'red':
            for key, value in list(self._red_pieces.items()):
                if value == from_coordinates:
                    if key == "CH":
                        self._red_pieces.update(CH=to_coordinates)
                    elif key == "CH1":
                        self._red_pieces.update(CH1=to_coordinates)
                    elif key == "EL":
                        self._red_pieces.update(EL=to_coordinates)
                    elif key == "EL1":
                        self._red_pieces.update(EL1=to_coordinates)
                    elif key == "HR":
                        self._red_pieces.update(HR=to_coordinates)
                    elif key == "HR1":
                        self._red_pieces.update(HR1=to_coordinates)
                    elif key == "GD":
                        self._red_pieces.update(GD=to_coordinates)
                    elif key == "GD1":
                        self._red_pieces.update(GD1=to_coordinates)
                    elif key == "GN":
                        self._red_pieces.update(GN=to_coordinates)
                    elif key == "CA":
                        self._red_pieces.update(CA=to_coordinates)
                    elif key == "CA1":
                        self._red_pieces.update(CA1=to_coordinates)
                    elif key == "SD":
                        self._red_pieces.update(SD=to_coordinates)
                    elif key == "SD1":
                        self._red_pieces.update(SD1=to_coordinates)
                    elif key == "SD2":
                        self._red_pieces.update(SD2=to_coordinates)
                    elif key == "SD3":
                        self._red_pieces.update(SD3=to_coordinates)
                    elif key == "SD4":
                        self._red_pieces.update(SD4=to_coordinates)

                # Removes the piece that has been captured, if one has been captured
            self._blue_pieces = {key: value for key, value in self._blue_pieces.items() if value != to_coordinates}

        return

    ################################ CHECK ########################################
    def is_in_check(self, player):
        """
        Takes either the red or blue player as a parameter and returns True if the player
        is in check. Otherwise, returns False.
        A general is in check if it could be captured during the opposing player's next move
        This method will check for checkmate and will interact with the enemy_legal_moves method as well as
        the general_legal_moves method. This is to see if the general has any valid moves. If the general has valid
        moves, it will call the checkmate function to see if any of the valid moves are moves that the other player could make.
        If it turns out that the general has valid moves, it will return that the player is in check
        """
        general_coordinates = []
        general_legal_moves = []
        enemy_legal_moves = []

        # Searches for the general's coordinates then calls the enemy_legal_moves method
        if player == "blue":
            for key, value in self._blue_pieces.items():
                if key == "GN":
                    general_coordinates = value
                    self.enemy_legal_moves("red", enemy_legal_moves)

        if player == "red":
            for key, value in self._red_pieces.items():
                if key == "GN":
                    general_coordinates = value
                    self.enemy_legal_moves("blue", enemy_legal_moves)

        # Checks to find out what the general's legal moves are
        self.general_possible(general_coordinates, player, general_legal_moves)

        # Checks to see if the player is in checkmate
        self.checkmate(general_legal_moves, general_coordinates, enemy_legal_moves, player)

        # If the general's coordinates are in the list of enemy moves, then the player is in check
        if general_coordinates in enemy_legal_moves:
            self._in_check = player
            return True
        else:
            return False        # The player is not in check

    def enemy_legal_moves(self, player, enemy_legal_moves):
        """
        The method is called by the is_in_check method. It takes the player and the empty enemy_legal_moves list.
        It will search through the player's piece dictionary for each piece. It will initiate the coordinates list as
        the value the current piece has in the dictionary. It will then call the possible move method for each piece to
        see what their possible moves are. It will repeat until it has gathered all possible moves for all pieces on the
        player's team. Then it will return the enemy_legal_moves list to the is_in_check method
        """
        coordinates = []

        if player == "blue":
            for key, value in list(self._blue_pieces.items()):
                if key == "CH" or key == "CH1":
                    coordinates = value
                    self.chariot_possible(coordinates, enemy_legal_moves, player)

                if key == "EL" or key == "EL1":
                    coordinates = value
                    self.elephant_possible(coordinates, enemy_legal_moves, player)

                if key == "HR" or key == "HR1":
                    coordinates = value
                    self.horse_possible(coordinates, enemy_legal_moves, player)

                if key == "GD" or key == "GD1":
                    coordinates = value
                    self.guard_possible(coordinates, enemy_legal_moves, player)

                if key == "CA" or key == "CA1":
                    coordinates = value
                    self.cannon_possible(coordinates, enemy_legal_moves, player)

                if key == "SD" or key == "SD1" or key == "SD2" or key == "SD3" or key == "SD4":
                    coordinates = value
                    self.soldier_possible(coordinates, enemy_legal_moves, player)

        if player == "red":
            for key, value in list(self._red_pieces.items()):
                if key == "CH" or key == "CH1":
                    coordinates = value
                    self.chariot_possible(coordinates, enemy_legal_moves, player)

                if key == "EL" or key == "EL1":
                    coordinates = value
                    self.elephant_possible(coordinates, enemy_legal_moves, player)

                if key == "HR" or key == "HR1":
                    coordinates = value
                    self.horse_possible(coordinates, enemy_legal_moves, player)

                if key == "GD" or key == "GD1":
                    coordinates = value
                    self.guard_possible(coordinates, enemy_legal_moves, player)

                if key == "CA" or key == "CA1":
                    coordinates = value
                    self.cannon_possible(coordinates, enemy_legal_moves, player)

                if key == "SD" or key == "SD1" or key == "SD2" or key == "SD3" or key == "SD4":
                    coordinates = value
                    self.soldier_possible(coordinates, enemy_legal_moves, player)

        return enemy_legal_moves

    def move_out_check(self, from_coordinates, to_coordinates, player):
        """
        Forces player that is currently in check to move a piece to take their general out of check. Will temporarily
        move the piece to the to coordinates to then run the enemy_legal_moves method to see if the move successfully
        takes the general out of check. This method is called by the make_move method. If the move does not take the
        player out of check, it will return False
        """
        enemy_legal_moves = []
        general_legal_moves = []

        # Checks the general's coordinates and the list of enemy legal moves. If the general is moving, it will temporarily
        # move the general on the board to see if it is a valid move
        if player == "blue":
            for key, value in self._blue_pieces.items():
                if key == "GN":
                    general_coordinates = value
                    if general_coordinates == from_coordinates:
                        general_coordinates = to_coordinates

                    self._board[to_coordinates[0]][to_coordinates[1]] = self._board[from_coordinates[0]][from_coordinates[1]]
                    self._board[from_coordinates[0]][from_coordinates[1]] = ' | '
                    self.enemy_legal_moves("red", enemy_legal_moves)

        if player == "red":
            for key, value in self._red_pieces.items():
                if key == "GN":
                    general_coordinates = value
                    if general_coordinates == from_coordinates:
                        general_coordinates = to_coordinates
                    self._board[to_coordinates[0]][to_coordinates[1]] = self._board[from_coordinates[0]][from_coordinates[1]]
                    self._board[from_coordinates[0]][from_coordinates[1]] = ' | '
                    self.enemy_legal_moves("blue", enemy_legal_moves)

        # Calls the general legal moves method to see if the move is valid
        self.general_possible(general_coordinates, player, general_legal_moves)

        # if the player is still in check, it will move the general back (if applicable) and will return False
        if general_coordinates in enemy_legal_moves:
            if general_coordinates == to_coordinates:
                self._board[from_coordinates[0]][from_coordinates[1]] = self._board[to_coordinates[0]][to_coordinates[1]]
                self._board[to_coordinates[0]][to_coordinates[1]] = ' | '
            return False

        # It will check change the in check to None and will check to see if the general was the one that moved. If it was
        # then it will update the board and return True
        else:
            self._in_check = None
            self._board[from_coordinates[0]][from_coordinates[1]] = self._board[to_coordinates[0]][to_coordinates[1]]
            self._board[to_coordinates[0]][to_coordinates[1]] = ' | '
            return True

    def checkmate(self, general_legal_moves, general_current, enemy_legal_moves, player):
        """
        This is called on in the is_in_check method. It takes the list of the general's legal moves, the general's current
        move, the list of enemy legal moves and the player. It will append the checkmate list with all of the coordinates
        in the general legal moves list and in the enemy legal moves list. If the checkmate list and legal moves list
        are exactly the same, then a checkmate happens and the game is over. It will update the game state and return
        """
        checkmate = []

        general_legal_moves.append(general_current)

        for item in general_legal_moves:
            if item in enemy_legal_moves:
                checkmate.append(item)

        if checkmate == general_legal_moves:
            if player == "blue":
                self._game_state = "RED_WON"
            if player == "red":
                self._game_state = "BLUE_WON"
            else:
                return

    ################################ CHECK MOVES ##################################

    def general_possible(self, general_coordinates, player, general_legal_moves):
        """
        This is called on from the is_in_check method. It takes the general's coordinates, the player and the empty
        list of the general's legal moves. The method checks a range of values to see what valid moves that the general
        currently has. It returns the list of general_legal_moves
        """

        for column in range(-1, 2):
            for row in range(-1, 2):
                new_column = general_coordinates[0] + column
                new_row = general_coordinates[1] + row
                valid_move = [new_column, new_row]              # The valid move that is being tested

                # Starts by indicating the move is valid, this will change to False if it finds a point where it is not valid
                valid = True

                if not self.on_board(valid_move[0], valid_move[1]):
                    valid = False

                if not self.within_palace(valid_move[0], valid_move[1]):
                    valid = False

                if valid_move == general_coordinates:
                    valid = False

                if valid:
                    if self._board[valid_move[0]][valid_move[1]] != ' | ':
                        if player == "blue":
                            for key, value in self._blue_pieces.items():
                                if value == valid_move:
                                    valid = False

                        if player == "red":
                            for key, value in self._red_pieces.items():
                                if value == valid_move:
                                    valid = False

                # If the move is valid, it will append the general_legal_moves list, else it will loop back to the top
                if valid:
                    general_legal_moves.append(valid_move)

        return general_legal_moves

    def chariot_possible(self, coordinates, enemy_legal_moves, player):
        """
        This is called on from the is_in_check method. It takes the chariot's coordinates, the player and the
        list of the enemy's legal moves. The method checks a range of values to see what valid moves that the chariot
        currently has. It returns the appended list of enemy_legal_moves
        """
        for column in range(-9, 9):
            for row in range(-9, 9):
                new_column = coordinates[0] + column
                new_row = coordinates[1] + row
                valid_move = [new_column, new_row]

                # Starts by indicating the move is valid, this will change to False if it finds a point where it is not valid
                valid = True

                if not self.on_board(valid_move[0], valid_move[1]):
                    valid = False

                if valid_move == coordinates:
                    valid = False

                if valid:
                    if player == "blue" and self._board[coordinates[0]][coordinates[1]] != ' | ':
                        for key, value in self._blue_pieces.items():
                            if value == valid_move:
                                valid = False

                    if player == "red" and self._board[coordinates[0]][coordinates[1]] != ' | ':
                        for key, value in self._red_pieces.items():
                            if value == valid_move:
                                valid = False

                if valid:
                    if not self.chariot_valid_moves(coordinates, valid_move):
                        valid = False

                if valid_move in enemy_legal_moves:
                    valid = False

            # If the move is deemed valid and legal, it will be added to the enemy_legal moves list
                if valid:
                    enemy_legal_moves.append(valid_move)

        return enemy_legal_moves

    def elephant_possible(self, coordinates, enemy_legal_moves, player):
        """
        This is called on from the is_in_check method. It takes the elephant's coordinates, the player and the
        list of the enemy's legal moves. The method checks a range of values to see what valid moves that the elephant
        currently has. It returns the appended list of enemy_legal_moves
        """
        for column in range(-2, 3):
            for row in range(-4, 4):
                new_column = coordinates[0] + column
                new_row = coordinates[1] + row
                valid_move = [new_column, new_row]

                # Starts by indicating the move is valid, this will change to False if it finds a point where it is not valid
                valid = True

                if not self.on_board(valid_move[0], valid_move[1]):
                    valid = False

                if valid_move == coordinates:
                    valid = False

                if valid:
                    if player == "blue" and self._board[coordinates[0]][coordinates[1]] != ' | ':
                        for key, value in self._blue_pieces.items():
                            if value == valid_move:
                                valid = False

                    if player == "red" and self._board[coordinates[0]][coordinates[1]] != ' | ':
                        for key, value in self._red_pieces.items():
                            if value == valid_move:
                                valid = False

                if valid:
                    if not self.elephant_valid_moves(coordinates, valid_move):
                        valid = False

                if valid_move in enemy_legal_moves:
                    valid = False

                if valid:
                    enemy_legal_moves.append(valid_move)
        return enemy_legal_moves

    def horse_possible(self, coordinates, enemy_legal_moves, player):
        """
        This is called on from the is_in_check method. It takes the horse's coordinates, the player and the
        list of the enemy's legal moves. The method checks a range of values to see what valid moves that the horse
        currently has. It returns the appended list of enemy_legal_moves
        """
        for column in range(-3, 3):
            for row in range(-3, 3):
                new_column = coordinates[0] + column
                new_row = coordinates[1] + row
                valid_move = [new_column, new_row]

                # Starts by indicating the move is valid, this will change to False if it finds a point where it is not valid
                valid = True

                if not self.on_board(valid_move[0], valid_move[1]):
                    valid = False

                if valid_move == coordinates:
                    valid = False

                if valid:
                    if player == "blue" and self._board[coordinates[0]][coordinates[1]] != ' | ':
                        for key, value in self._blue_pieces.items():
                            if value == valid_move:
                                valid = False

                    if player == "red" and self._board[coordinates[0]][coordinates[1]] != ' | ':
                        for key, value in self._red_pieces.items():
                            if value == valid_move:
                                valid = False

                if valid:
                    if not self.horse_valid_moves(coordinates, valid_move):
                        valid = False

                if valid_move in enemy_legal_moves:
                    valid = False

                if valid:
                    enemy_legal_moves.append(valid_move)
        return enemy_legal_moves

    def guard_possible(self, coordinates, enemy_legal_moves, player):
        """
        This is called on from the is_in_check method. It takes the guard's coordinates, the player and the
        list of the enemy's legal moves. The method checks a range of values to see what valid moves that the guard
        currently has. It returns the appended list of enemy_legal_moves
        """
        for column in range(-1, 2):
            for row in range(-1, 2):
                new_column = coordinates[0] + column
                new_row = coordinates[1] + row
                valid_move = [new_column, new_row]

                # Starts by indicating the move is valid, this will change to False if it finds a point where it is not valid
                valid = True

                if not self.on_board(valid_move[0], valid_move[1]):
                    valid = False

                if valid_move == coordinates:
                    valid = False

                if valid:
                    if player == "blue" and self._board[coordinates[0]][coordinates[1]] != ' | ':
                        for key, value in self._blue_pieces.items():
                            if value == valid_move:
                                valid = False

                    if player == "red" and self._board[coordinates[0]][coordinates[1]] != ' | ':
                        for key, value in self._red_pieces.items():
                            if value == valid_move:
                                valid = False
                if valid:
                    if not self.guard_valid_moves(coordinates, valid_move):
                        valid = False

                if valid_move in enemy_legal_moves:
                    valid = False

                if valid:
                    enemy_legal_moves.append(valid_move)
        return enemy_legal_moves

    def soldier_possible(self, coordinates, enemy_legal_moves, player):
        """
        This is called on from the is_in_check method. It takes the soldier's coordinates, the player and the
        list of the enemy's legal moves. The method checks a range of values to see what valid moves that the soldier
        currently has. It returns the appended list of enemy_legal_moves
        """
        for column in range(-1, 2):
            for row in range(-1, 2):
                new_column = coordinates[0] + column
                new_row = coordinates[1] + row
                valid_move = [new_column, new_row]

                # Starts by indicating the move is valid, this will change to False if it finds a point where it is not valid
                valid = True

                if not self.on_board(valid_move[0], valid_move[1]):
                    valid = False

                if valid_move == coordinates:
                    valid = False

                if valid:
                    if player == "blue" and self._board[coordinates[0]][coordinates[1]] != ' | ':
                        for key, value in self._blue_pieces.items():
                            if value == valid_move:
                                valid = False

                    if player == "red" and self._board[coordinates[0]][coordinates[1]] != ' | ':
                        for key, value in self._red_pieces.items():
                            if value == valid_move:
                                valid = False

                    if valid:
                        if not self.soldier_valid_moves(coordinates, valid_move, player):
                            valid = False

                if valid_move in enemy_legal_moves:
                    valid = False

                if valid:
                    enemy_legal_moves.append(valid_move)
        return enemy_legal_moves

    def cannon_possible(self, coordinates, enemy_legal_moves, player):
        """
        This is called on from the is_in_check method. It takes the cannon's coordinates, the player and the
        list of the enemy's legal moves. The method checks a range of values to see what valid moves that the cannon
        currently has. It returns the appended list of enemy_legal_moves
        """
        for column in range(-9, 9):
            for row in range(-9, 9):
                new_column = coordinates[0] + column
                new_row = coordinates[1] + row
                valid_move = [new_column, new_row]

                # Starts by indicating the move is valid, this will change to False if it finds a point where it is not valid
                valid = True

                if not self.on_board(valid_move[0], valid_move[1]):
                    valid = False

                if valid_move == coordinates:
                    valid = False

                if valid:
                    if player == "blue" and self._board[coordinates[0]][coordinates[1]] != ' | ':
                        for key, value in self._blue_pieces.items():
                            if value == valid_move:
                                valid = False

                    if player == "red" and self._board[coordinates[0]][coordinates[1]] != ' | ':
                        for key, value in self._red_pieces.items():
                            if value == valid_move:
                                valid = False

                if valid:
                    if not self.cannon_valid_moves(coordinates, valid_move):
                        valid = False

                if valid_move in enemy_legal_moves:
                    valid = False

                if valid:
                    enemy_legal_moves.append(valid_move)
        return enemy_legal_moves

    ################################ PIECES #######################################

    def chariot_valid_moves(self, from_coordinates, to_coordinates):
        """
        Take the from_coordinates of the piece and the to_coordinates of the piece and will check to see if the move
        is valid. This method will be called within the make_move method. They are able to move either horizontally or
        vertically. Within the palace, they are able to move along the diagonal line. They can move as far as they want
        across the board as long as there is no one in the way between the from and to coordinates.
        """
        # It will loop through all the spaces from the starting point to the ending point. If
        # it is all clear, it is a valid move. If one space before the ending point is taken, it will return false

        # If moving vertically
        if from_coordinates[0] == to_coordinates[0] and from_coordinates[1] > to_coordinates[1]:
            for index in range(0, from_coordinates[1] + 1):
                if self.on_board(from_coordinates[0], from_coordinates[1] - index):
                    if self._board[from_coordinates[0]][from_coordinates[1] - index] != ' | ':
                        if [from_coordinates[0], from_coordinates[1] - index] == from_coordinates:
                            continue
                        elif [from_coordinates[0], from_coordinates[1] - index] == to_coordinates:
                            return True
                        else:
                            return False
                    if [from_coordinates[0], from_coordinates[1] - index] == to_coordinates:
                        return True
            return True

        elif from_coordinates[0] == to_coordinates[0] and from_coordinates[1] < to_coordinates[1]:
            for index in range(0, to_coordinates[1] + 1):
                if self.on_board(from_coordinates[0], from_coordinates[1] + index):
                    if self._board[from_coordinates[0]][from_coordinates[1] + index] != ' | ':
                        if [from_coordinates[0], from_coordinates[1] + index] == from_coordinates:
                            continue
                        elif [from_coordinates[0], from_coordinates[1] + index] == to_coordinates:
                            return True
                        else:
                            return False
                    if [from_coordinates[0], from_coordinates[1] + index] == to_coordinates:
                        return True
            return True

        # If moving horizontally
        elif from_coordinates[1] == to_coordinates[1] and from_coordinates[0] < to_coordinates[0]:
            for index in range(0, to_coordinates[0] + 1):
                if self.on_board(from_coordinates[0] + index, from_coordinates[1]):
                    if self._board[from_coordinates[0] + index][from_coordinates[1]] != ' | ':
                        if [from_coordinates[0] + index, from_coordinates[1]] == from_coordinates:
                            continue
                        if [from_coordinates[0] + index, from_coordinates[1]] == to_coordinates:
                            return True
                        else:
                            return False
                    if [from_coordinates[0] + index, from_coordinates[1]] == to_coordinates:
                        return True
            return True

        elif from_coordinates[1] == to_coordinates[1] and to_coordinates[0] < from_coordinates[0]:
            for index in range(0, from_coordinates[0] + 1):
                if self.on_board(from_coordinates[0] - index, from_coordinates[1]):
                    if self._board[from_coordinates[0] - index][from_coordinates[1]] != ' | ':
                        if [from_coordinates[0] - index, from_coordinates[1]] == from_coordinates:
                            continue
                        if [from_coordinates[0] - index, from_coordinates[1]] == to_coordinates:
                            return True
                        else:
                            return False
                    if [from_coordinates[0] - index, from_coordinates[1]] == to_coordinates:
                        return True
            return True

        elif self.within_palace(from_coordinates[0], from_coordinates[1]) and self.within_palace(to_coordinates[0], to_coordinates[1]):
            # If within the red palace
            if [from_coordinates[0] + 1, from_coordinates[1] + 1] == to_coordinates:
                return True
            if [from_coordinates[0] + 2, from_coordinates[1] + 2] == to_coordinates:
                return True
            if [from_coordinates[0] - 1, from_coordinates[1] + 1] == to_coordinates:
                return True
            if [from_coordinates[0] - 2, from_coordinates[1] + 2] == to_coordinates:
                return True

            # if within the blue palace
            if [from_coordinates[0] - 1, from_coordinates[1] - 1] == to_coordinates:
                return True
            if [from_coordinates[0] - 2, from_coordinates[1] - 2] == to_coordinates:
                return True
            if [from_coordinates[0] + 1, from_coordinates[1] - 1] == to_coordinates:
                return True
            if [from_coordinates[0] + 2, from_coordinates[1] - 2] == to_coordinates:
                return True

            return False
        else:
            return False

    def general_valid_moves(self, from_coordinates, to_coordinates):
        """
        The general_valid_moves function will take the from_coordinates of the piece and the to_coordinates of the piece and
        will check to see if the move is valid. This method will be called within the make_move method. They are able to
        move either horizontally or vertically within the palace. They are also able to move along the diagonal line in
        the palace.
        """

        if not self.within_palace(to_coordinates[0], to_coordinates[1]):
            return False

        # Validating that the move is within one spot from their current position
        if [from_coordinates[0] + 1, from_coordinates[1]] == to_coordinates:
            return True
        elif [from_coordinates[0] - 1, from_coordinates[1]] == to_coordinates:
            return True
        elif [from_coordinates[0], from_coordinates[1] + 1] == to_coordinates:
            return True
        elif [from_coordinates[0], from_coordinates[1] - 1] == to_coordinates:
            return True
        elif [from_coordinates[0] + 1, from_coordinates[1] + 1] == to_coordinates:
            return True
        elif [from_coordinates[0] + 1, from_coordinates[1] - 1] == to_coordinates:
            return True
        elif [from_coordinates[0] - 1, from_coordinates[1] + 1] == to_coordinates:
            return True
        elif [from_coordinates[0] - 1, from_coordinates[1] - 1] == to_coordinates:
            return True
        else:
            return False

    def elephant_valid_moves(self, from_coordinates, to_coordinates):
        """
        The elephant_valid_moves function will take the from_coordinates of the piece and the to_coordinates of the piece and
        will check to see if the move is valid. This method will be called within the make_move method. They are able
        to move either horizontally or vertically. The piece can move one step and then two steps diagonal
        from the starting position. It will check each spot en route to the to coordinates to make sure
        no piece is blocking the way
        """
        # If the first move is vertical
        if [from_coordinates[0] - 2, from_coordinates[1] - 3] == to_coordinates:
            if self._board[from_coordinates[0]][from_coordinates[1] - 1] != ' | ':
                return False
            if self._board[from_coordinates[0] - 1][from_coordinates[1] - 1] != ' | ':
                return False
            if self._board[from_coordinates[0] - 1][from_coordinates[1] - 2] != ' | ':
                return False
            else:
                return True

        if [from_coordinates[0] - 2, from_coordinates[1] + 3] == to_coordinates:
            if self._board[from_coordinates[0]][from_coordinates[1] + 1] != ' | ':
                return False
            if self._board[from_coordinates[0] + 1][from_coordinates[1] + 1] != ' | ':
                return False
            if self._board[from_coordinates[0] - 1][from_coordinates[1] + 2] != ' | ':
                return False
            else:
                return True

        if [from_coordinates[0] + 2, from_coordinates[1] - 3] == to_coordinates:
            if self._board[from_coordinates[0]][from_coordinates[1] - 1] != ' | ':
                return False
            if self._board[from_coordinates[0] + 1][from_coordinates[1] - 1] != ' | ':
                return False
            if self._board[from_coordinates[0] + 1][from_coordinates[1] - 2] != ' | ':
                return False
            else:
                return True

        if [from_coordinates[0] + 2, from_coordinates[1] + 3] == to_coordinates:
            if self._board[from_coordinates[0]][from_coordinates[1] + 1] != ' | ':
                return False
            if self._board[from_coordinates[0] + 1][from_coordinates[1] + 1] != ' | ':
                return False
            if self._board[from_coordinates[0] + 1][from_coordinates[1] + 2] != ' | ':
                return False
            else:
                return True

            # if the first move is horizontal
        if [from_coordinates[0] - 3, from_coordinates[1] - 2] == to_coordinates:
            if self._board[from_coordinates[0] - 1][from_coordinates[1]] != ' | ':
                return False
            if self._board[from_coordinates[0] - 2][from_coordinates[1] - 1] != ' | ':
                return False
            if self._board[from_coordinates[0] - 3][from_coordinates[1] - 2] != ' | ':
                return False
            else:
                return True

        if [from_coordinates[0] + 3, from_coordinates[1] - 2] == to_coordinates:
            if self._board[from_coordinates[0] + 1][from_coordinates[1]] != ' | ':
                return False
            if self._board[from_coordinates[0] + 2][from_coordinates[1] - 1] != ' | ':
                return False
            if self._board[from_coordinates[0] + 3][from_coordinates[1] - 2] != ' | ':
                return False
            else:
                return True

        if [from_coordinates[0] - 3, from_coordinates[1] + 2] == to_coordinates:
            if self._board[from_coordinates[0] - 1][from_coordinates[1]] != ' | ':
                return False
            if self._board[from_coordinates[0] - 2][from_coordinates[1] + 1] != ' | ':
                return False
            if self._board[from_coordinates[0] - 3][from_coordinates[1] + 2] != ' | ':
                return False
            else:
                return True

        if [from_coordinates[0] + 3, from_coordinates[1] + 2] == to_coordinates:
            if self._board[from_coordinates[0] + 1][from_coordinates[1]] != ' | ':
                return False
            if self._board[from_coordinates[0] + 2][from_coordinates[1] + 1] != ' | ':
                return False
            if self._board[from_coordinates[0] + 3][from_coordinates[1] + 2] != ' | ':
                return False
            else:
                return True

        else:
            return False

    def guard_valid_moves(self, from_coordinates, to_coordinates):
        """
        The guard_valid_moves function will take the from_coordinates of the piece and the to_coordinates of the piece and
        will check to see if the move is valid. This method will be called within the make_move method. They are able
        to move either horizontally or vertically within the palace. They are also able to move along
        the diagonal line.
        """
        if not self.within_palace(to_coordinates[0], to_coordinates[1]):
            return False

        if [from_coordinates[0] + 1, from_coordinates[1]] == to_coordinates:
            return True
        elif [from_coordinates[0] - 1, from_coordinates[1]] == to_coordinates:
            return True
        elif [from_coordinates[0], from_coordinates[1] + 1] == to_coordinates:
            return True
        elif [from_coordinates[0], from_coordinates[1] - 1] == to_coordinates:
            return True
        elif [from_coordinates[0] + 1, from_coordinates[1] + 1] == to_coordinates:
            return True
        elif [from_coordinates[0] + 1, from_coordinates[1] - 1] == to_coordinates:
            return True
        elif [from_coordinates[0] - 1, from_coordinates[1] + 1] == to_coordinates:
            return True
        elif [from_coordinates[0] - 1, from_coordinates[1] - 1] == to_coordinates:
            return True
        else:
            return False

    def cannon_valid_moves(self, from_coordinates, to_coordinates):
        """
        The cannon_valid_moves function will take the from_coordinates of the piece and the to_coordinates of the piece and
        will check to see if the move is valid. This method will be called within the make_move method of the JanggiGame
        class. They are able to move either horizontally or vertically. Within the palace, they are able to move along
        the diagonal line. In order to move, they have to jump over a piece. They do not capture the piece they jump
        over, but can capture another piece after they jump. They are not able to capture or jump over another cannon
        """
        counter = 0         # Counter to see how many pieces between the from and to coordinates
        indexes = []        # list to hold the coordinates of the piece they will have to jump over
        cannon_coordinates = []
        general_coordinates = []

        # Moving vertically
        if from_coordinates[0] == to_coordinates[0] and from_coordinates[1] > to_coordinates[1]:
            for index in range(0, from_coordinates[1]):
                if self.on_board(from_coordinates[0], from_coordinates[1] - index):
                    if self._board[from_coordinates[0]][from_coordinates[1] - index] != ' | ':
                        if (from_coordinates[1] - index) < to_coordinates[1]:
                            counter += 0
                        elif (from_coordinates[1] - index) == from_coordinates[1]:
                            counter += 0
                        elif (from_coordinates[1] - index) == to_coordinates[1]:
                            counter += 0
                        else:
                            counter += 1
                            indexes.append([from_coordinates[0], from_coordinates[1] - index])

        elif from_coordinates[0] == to_coordinates[0] and to_coordinates[1] > from_coordinates[1]:
            for index in range(0, to_coordinates[1]):
                if self.on_board(from_coordinates[0], from_coordinates[1] + index):
                    if self._board[from_coordinates[0]][from_coordinates[1] + index] != ' | ':
                        if (from_coordinates[1] + index) > to_coordinates[1]:
                            counter += 0
                        elif (from_coordinates[1] + index) == from_coordinates[1]:
                            counter += 0
                        elif (from_coordinates[1] + index) == to_coordinates[1]:
                            counter += 0
                        else:
                            counter += 1
                            indexes.append([from_coordinates[0], from_coordinates[1] + index])

        # If moving horizontally
        elif from_coordinates[1] == to_coordinates[1] and from_coordinates[0] > to_coordinates[0]:
            for index in range(0, from_coordinates[0]):
                if self.on_board(from_coordinates[0] - index, from_coordinates[1]):
                    if self._board[from_coordinates[0] - index][from_coordinates[1]] != ' | ':
                        if (from_coordinates[0] - index) < to_coordinates[0]:
                            counter += 0
                        elif (from_coordinates[0] - index) == from_coordinates[0]:
                            counter += 0
                        elif (from_coordinates[0] - index) == to_coordinates[0]:
                            counter += 0
                        else:
                            counter += 1
                            indexes.append([from_coordinates[0] - index, from_coordinates[1]])

        elif from_coordinates[1] == to_coordinates[1] and to_coordinates[0] > from_coordinates[0]:
            for index in range(0, to_coordinates[0]):
                if self.on_board(from_coordinates[0] + index, from_coordinates[1]):
                    if self._board[from_coordinates[0] + index][from_coordinates[1]] != ' | ':
                        if (from_coordinates[0] + index) > to_coordinates[0]:
                            counter += 0
                        elif (from_coordinates[0] + index) == from_coordinates[0]:
                            counter += 0
                        elif (from_coordinates[0] + index) == to_coordinates[0]:
                            counter += 0
                        else:
                            counter += 1
                            indexes.append([from_coordinates[0] + index, from_coordinates[1]])

        elif self.within_palace(from_coordinates[0], from_coordinates[1]) and self.within_palace(to_coordinates[0], to_coordinates[1]):
            if [from_coordinates[0] + 2, from_coordinates[1] + 2] == to_coordinates:
                if [from_coordinates[0] + 1, from_coordinates[1] + 1] != ' | ':
                    counter += 1
                    indexes.append([from_coordinates[0] + 1, from_coordinates[1] + 1])
                else:
                    counter += 0

            if [from_coordinates[0] + 2, from_coordinates[1] - 2] == to_coordinates:
                if [from_coordinates[0] + 1, from_coordinates[1] - 1] != ' | ':
                    counter += 1
                    indexes.append([from_coordinates[0] + 2, from_coordinates[1] - 2])
                else:
                    counter += 0

            if [from_coordinates[0] - 2, from_coordinates[1] + 2] == to_coordinates:
                if [from_coordinates[0] - 1, from_coordinates[1] + 1] != ' | ':
                    counter += 1
                    indexes.append([from_coordinates[0] - 2, from_coordinates[1] + 2])
                else:
                    counter += 0

            if [from_coordinates[0] - 2, from_coordinates[1] - 2] == to_coordinates:
                if [from_coordinates[0] - 1, from_coordinates[1] - 1] != ' | ':
                    counter += 1
                    indexes.append([from_coordinates[0] - 2, from_coordinates[1] - 2])
                else:
                    counter += 0

        # After determining that the move is valid, it will compare the coordinates in the indexes to make sure that
        # they are not jumping over or capturing a cannon. If it is a cannon, it will return False.
        for key, value in list(self._blue_pieces.items()):
            if key == "CA" or key == "CA1":
                cannon_coordinates = value
                if cannon_coordinates in indexes or cannon_coordinates == to_coordinates:
                    return False

        # After determining that the move is valid, it will compare the coordinates in the indexes to make sure that
        # they are not jumping over or capturing a cannon. If it is a cannon, it will return False.
        for key, value in list(self._red_pieces.items()):
            if key == "CA" or key == "CA1":
                cannon_coordinates = value
                if cannon_coordinates in indexes or cannon_coordinates == to_coordinates:
                    return False

        #  Will make sure that it is not capturing the general
            if key == "GN":
                general_coordinates = value
                if general_coordinates == to_coordinates:
                    return False

        if counter == 1:
            return True
        else:
            return False

    def soldier_valid_moves(self, from_coordinates, to_coordinates, player):
        """
        The soldier_valid_moves function will take the from_coordinates of the piece and the to_coordinates of the piece and
        will check to see if the move is valid. This method will be called within the make_move method. They are able to
         move either horizontally or forward. Within the palace, they are able to move along the diagonal line. They are
         not able to move backward.
        """

        if player == "blue":
            if [from_coordinates[0] + 1, from_coordinates[1]] == to_coordinates:
                return True
            elif [from_coordinates[0] - 1, from_coordinates[1]] == to_coordinates:
                return True
            elif [from_coordinates[0], from_coordinates[1] - 1] == to_coordinates:
                return True
            elif self.within_palace(from_coordinates[0], from_coordinates[1]) and self.within_palace(to_coordinates[0], to_coordinates[1]):
                if [from_coordinates[0] - 1, from_coordinates[1] - 1]:
                    return True
            elif self.within_palace(from_coordinates[0], from_coordinates[1]) and self.within_palace(to_coordinates[0], to_coordinates[1]):
                if [from_coordinates[0] + 1, from_coordinates[1] - 1]:
                    return True
            else:
                return False

        if player == "red":
            if [from_coordinates[0] + 1, from_coordinates[1]] == to_coordinates:
                return True
            elif [from_coordinates[0] - 1, from_coordinates[1]] == to_coordinates:
                return True
            elif [from_coordinates[0], from_coordinates[1] + 1] == to_coordinates:
                return True
            elif self.within_palace(from_coordinates[0], from_coordinates[1]) and self.within_palace(to_coordinates[0], to_coordinates[1]):
                if [from_coordinates[0] - 1, from_coordinates[1] + 1]:
                    return True
            elif self.within_palace(from_coordinates[0], from_coordinates[1]) and self.within_palace(to_coordinates[0], to_coordinates[1]):
                if [from_coordinates[0] + 1, from_coordinates[1] + 1]:
                    return True
            else:
                return False

    def horse_valid_moves(self, from_coordinates, to_coordinates):
        """
        The horse_valid_moves function will take the from_coordinates of the piece and the to_coordinates of the piece and
        will check to see if the move is valid. This method will be called within the make_move method. They are able
        to move either horizontally or vertically. The piece can move one step and then one step diagonal
        from the starting position. It will check each spot en route to the to coordinates to make sure
        no piece is blocking the way
        """
        # if moving vertically
        if [from_coordinates[0] - 1, from_coordinates[1] + 2] == to_coordinates:
            if self._board[from_coordinates[0]][from_coordinates[1] + 1] != ' | ':
                return False
            else:
                return True

        if [from_coordinates[0] + 1, from_coordinates[1] - 2] == to_coordinates:
            if self._board[from_coordinates[0]][from_coordinates[1] - 1] != ' | ':
                return False
            else:
                return True

        if [from_coordinates[0] + 1, from_coordinates[1] + 2] == to_coordinates:
            if self._board[from_coordinates[0]][from_coordinates[1] + 1] != ' | ':
                return False
            else:
                return True

        if [from_coordinates[0] - 1, from_coordinates[1] - 2] == to_coordinates:
            if self._board[from_coordinates[0]][from_coordinates[1] - 1] != ' | ':
                return False
            else:
                return True

        # If moving horizontally
        if [from_coordinates[0] + 2, from_coordinates[1] - 1] == to_coordinates:
            if self._board[from_coordinates[0] + 1][from_coordinates[1]] != ' | ':
                return False
            else:
                return True

        if [from_coordinates[0] + 2, from_coordinates[1] + 1] == to_coordinates:
            if self._board[from_coordinates[0] + 1][from_coordinates[1]] != ' | ':
                return False
            else:
                return True

        if [from_coordinates[0] - 2, from_coordinates[1] - 1] == to_coordinates:
            if self._board[from_coordinates[0] - 1][from_coordinates[1]] != ' | ':
                return False
            else:
                return True

        if [from_coordinates[0] - 2, from_coordinates[1] + 1] == to_coordinates:
            if self._board[from_coordinates[0] - 1][from_coordinates[1]] != ' | ':
                return False
            else:
                return True
        else:
            return False

    ################################ BOARD #######################################

    def on_board(self, column, row):
        """
        Method to indicate the edges of the board. If a move is within the row and column parameters, then it will return
        True. Otherwise it will return False and the move is invalid
        """
        if (0 <= row <= 9) and (0 <= column <= 8):
            return True
        else:
            return False

    def within_palace(self, column, row):
        """
        Method to indicate the edges of the palaces. If a move is within the palace, then it will return True. Otherwise
        it will return False
        """
        if (9 >= row >= 7) and (3 <= column <= 5):  # blue palace
            return True
        if (0 <= row <= 2) and (3 <= column <= 5):  # red palace
            return True
        else:
            return False

    def create_board(self):
        """
        Method to set up the parameters of the game board. Sets up the size, icon for empty squares and
        initializes the pieces with their color and abbreviation
        """
        game_board = []
        for column in range(9):
            board_row = []
            for row in range(10):
                board_row.append(' | ')

            game_board.append(board_row)
        game_board[0][0] = colored('CH ', 'red')
        game_board[1][0] = colored('EL ', 'red')
        game_board[2][0] = colored('HR ', 'red')
        game_board[1][2] = colored('GD ', 'red')
        game_board[5][2] = colored('GD ', 'red')
        game_board[6][0] = colored('EL ', 'red')
        game_board[7][0] = colored('HR ', 'red')
        game_board[8][0] = colored('CH ', 'red')
        game_board[4][1] = colored('GN ', 'red')

        game_board[3][2] = colored('CA ', 'red')
        game_board[7][2] = colored('CA ', 'red')
        game_board[0][3] = colored('SD ', 'red')
        game_board[2][3] = colored('SD ', 'red')
        game_board[4][3] = colored('SD ', 'red')
        game_board[6][3] = colored('SD ', 'red')
        game_board[8][3] = colored('SD ', 'red')

        game_board[0][9] = colored('CH ', 'blue')
        game_board[1][9] = colored('EL ', 'blue')
        game_board[2][9] = colored('HR ', 'blue')
        game_board[3][7] = colored('GD ', 'blue')
        game_board[5][7] = colored('GD ', 'blue')
        game_board[6][9] = colored('EL ', 'blue')
        game_board[7][9] = colored('HR ', 'blue')
        game_board[8][9] = colored('CH ', 'blue')
        game_board[4][8] = colored('GN ', 'blue')
        game_board[1][7] = colored('CA ', 'blue')
        game_board[7][7] = colored('CA ', 'blue')
        game_board[0][6] = colored('SD ', 'blue')
        game_board[2][6] = colored('SD ', 'blue')
        game_board[4][6] = colored('SD ', 'blue')
        game_board[6][6] = colored('SD ', 'blue')
        game_board[8][6] = colored('SD ', 'blue')
        return game_board

    def display(self):
        """
        Method to display the game board to the console.
        """
        counter = 0
        print(' a ', ' b ', ' c ', ' d ', ' e ', ' f ', ' g ', ' h ', ' i ')
        for index in range(10):
            for index1 in range(9):
                print(self._board[index1][index], end=' ')
            counter += 1
            print(counter)
