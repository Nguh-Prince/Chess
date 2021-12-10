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
        
    def moveIsValid(self, destination:Square):
        return True
    
    def move(self, destination: Square):
        if self.moveIsValid():
            self.square.piece = None
            self.square = destination
            destination.piece = self
            return True

class Pawn(Piece):
    def moveIsValid(self, destination:Square):
        try:
            king = [ f for f in self.square.board.pieces if f.color == self.color and isinstance(f, King) ][0]
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
        except IndexError as e:
            # no king
            raise e

    def possibleMoves(self, destination: Square):
        
        pass