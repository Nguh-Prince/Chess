import pygame
import os

letters_to_numbers = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}

class Board:
    def __init__(self):
        self.ranks = []
        self.files = []
        self.squares = []

class Rank:
    def __init__(self, ycoord, number:int):
        self.ycoord = ycoord
        self.number = number
    
    def __str__(self):
        return f"{number}"

    def __add__(self, other: Rank):
        return self.number + other.number
    
    def __sub__(self, other: Rank):
        return self.number - other.number

class File:
    def __init__(self, xcoord:float, letter:str):
        self.letter = letter
        self.number = letters_to_numbers[ letter.lower() ]
    
    def __str__(self):
        return f"{self.letter.lower()}"
    
    def __add__(self, other: Rank):
        return self.number + other.number
    
    def __sub__(self, other: Rank):
        return self.number - other.number

class Square:
    def __init__(self, file:File, rank:Rank, board):
        self.file = file
        self.piece = None
        self.rank = rank
        self.board = board

    def __str__(self):
        return f"{file.__str__()}{rank.__str__()} - {self.piece.__str__()}"

    def isDark(self) -> bool:
        return ( self.rank.number + letters_to_numbers[self.file.letter.lower()] ) % 2 == 0

class Piece:
    def __init__(self, color: int,square:Square, image:str):
        """
        the image string must be a path to a valid image file
        """
        if not os.path.exists(image):
            raise FileNotFoundError
        self.square = square
        self.image = pygame.image.load(image)
        self.color = color

    def king(self) -> King:
        try:
            king = [ f for f in self.square.board if isinstance(f, King) and f.color == self.color ][0]
            return king
        except IndexError as e:
            raise e
        
    def moveIsValid(self, destination:Square):
        return True
    
    def move(self, destination: Square):
        if self.moveIsValid():
            self.square.piece = None
            self.square = destination
            destination.piece = self
            return True

    def possibleMoves(self):
        king = self.king()

        if king.isPinned():
            return []
        else:
            moves = [ f for f in self.square.board.squares if self.moveIsValid(f) ]

            # check if piece is pinned and remove the moves accordingly
            return moves

    def squaresAttacked(self):
        return self.possibleMoves()

    def isPinned(self):
        king = self.king()

        relative_coordinates_from_king = (king.square.file - self.square.file, king.square.rank - self.square.rank)

        # piece can only be pinned if it is on the same file / rank or diagonal as the king
        if abs(relative_coordinates_from_king[0]) != abs(relative_coordinates_from_king[1]) and relative_coordinates_from_king[0] != and relative_coordinates_from_king[1] != 0:
            return False
        elif abs(relative_coordinates_from_king[0]) == abs(relative_coordinates_from_king[1]): # same diagonal as king
            pass
        elif relative_coordinates_from_king[0] == 0 or relative_coordinates_from_king[1] == 1:
            attacking_piece = [ f for f in self.square.board if isinstance(f, Rook) and self.square in f.possibleMoves() and self.file == f.file ] if relative_coordinates_from_king[0] == 0 else [ f for f in self.square.board if isinstance(f, Rook) and self.square in f.possibleMoves() and self.rank == f.rank ]

            if len(attacking_piece) < 0:
                return False
            else:
                attacking_piece = attacking_piece[0]
                
        pass

class Pawn(Piece):
    def moveIsValid(self, destination:Square):
        king = self.king()

        if king.isChecked():
            pass
        else:
            delta_x = destination.square.file - self.square.file
            delta_y = destination.square.rank - self.square.rank

            if (self.color and not delta_y) or (not self.color and delta_y): # white pawn does not move toward 1st rank, black does not move toward 8th rank
                return False

            if abs(delta_x) <= 1:
                if abs(delta_x) == 1:
                    # pawn capture
                    return True if destination.piece else return False

                elif delta_x == 0:
                    if abs(delta_y) > 2:
                        return False
                    if abs(delta_y) == 2 and (self.color and self.square.rank.number == 2) or (not self.color and self.square.rank.number == 7):
                        return True
                    else:
                        return False

            else:
                return False