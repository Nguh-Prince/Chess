import pygame
import os

letters_to_numbers = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
numbers_to_letters = { v: k for k, v in letters_to_numbers.items() }

PIECES_FOLDER = r"E:\personal_projects\chess\chess pieces"

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
    def __init__(self, color: int, square:Square, image:str) -> None:
        """
        the image string must be a path to a valid image file
        """
        if not os.path.exists(image):
            raise FileNotFoundError
        self.square = square
        self.image = pygame.image.load(image)
        self.color = color
        self.name = ''

    def king(self):
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
        pieces_in_the_way = []

        # piece can only be pinned if it is on the same file / rank or diagonal as the king
        if abs(relative_coordinates_from_king[0]) != abs(relative_coordinates_from_king[1]) and relative_coordinates_from_king[0] != and relative_coordinates_from_king[1] != 0:
            return False
        elif abs(relative_coordinates_from_king[0]) == abs(relative_coordinates_from_king[1]): # same diagonal as king
            attacking_piece = [  ]
        elif relative_coordinates_from_king[0] == 0 or relative_coordinates_from_king[1] == 1:
            attacking_piece = [ f for f in self.square.board if isinstance(f, Rook) and self.square in f.possibleMoves() and self.square.file == f.square.file ] if relative_coordinates_from_king[0] == 0 else [ f for f in self.square.board if isinstance(f, Rook) and self.square in f.possibleMoves() and self.rank == f.rank ]

            if len(attacking_piece) < 0:
                return False
            else:
                attacking_piece = attacking_piece[0]
                # check if there are any pieces between this one and the king
                if relative_coordinates_from_king[0] == 0:
                    pieces_in_the_way = [ f for f in self.square.board.pieces if f.square.file == king.square.file and king.square.rank - f.square.rank < relative_coordinates_from_king[1] ] if relative_coordinates_from_king[1] < 0 else [ f for f in self.square.board.pieces if f.square.file == king.square.file and king.square.rank - f.square.rank > relative_coordinates_from_king[1] ]
                else:
                    pieces_in_the_way = [ f for f in self.square.board.pieces if f.square.rank == king.square.rank and king.square.file - f.square.file < relative_coordinates_from_king[0] ] if relative_coordinates_from_king[0] < 0 else [ f for f in self.square.board.pieces if f.square.rank == king.square.square.rank and king.square.file - f.square.file > relative_coordinates_from_king[0] ]
        
        return len(pieces_in_the_way) < 1

class Pawn(Piece):
    def __init__(self, color: int, square: Square, image: str):
        super().__init__(color, square, image)
        self.name = "Pawn"

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

class Knight(Piece):
    def __init__(self, color: int, square: Square, image: str) -> None:
        super().__init__(color, square, image)
        self.name = "Knight"

class Bishop(Piece):
    def __init__(self, color: int, square: Square, image: str) -> None:
        super().__init__(color, square, image)
        self.name = "Bishop"

class Rook(Piece):
    def __init__(self, color: int, square: Square, image: str) -> None:
        super().__init__(color, square, image)
        self.name = "Rook"

class Queen(Bishop, Rook):
    def __init__(self, color: int, square: Square, image: str) -> None:
        super().__init__(color, square, image)
        self.name = "Queen"

class King(Piece):
    def __init__(self, color: int, square: Square, image: str) -> None:
        super().__init__(color, square, image)
        self.name = "King"

class Board(pygame.Rect):
    def __init__(self, topLeft, cellSize) -> None:
        super.__init__(topLeft, cellSize*8, cellSize*8)
        self.ranks = []
        self.files = []
        self.squares = []
        self.__flipped = False # true if the board is flipped, i.e topLeft square is h1 instead of a8
        self.pieces = []

        # create 8 ranks and 8 files
        for i in range(8):
            self.ranks.append( Rank(self.topleft[1] + (7 - i) * cellSize, i+1) )  # puts the 8th rank closest to the topleft of the board
            self.files.append( File(self.topleft[0] + cellSize), numbers_to_letters[i+1].upper() )

        # create the squares and automatically place pieces on them
        for file in self.files:
            for rank in self.ranks:
                square = Square(file, rank, self)
                self.squares.append( square )

                if rank.number in [2, 7]:  # create pawns
                    self.pieces.append( Pawn(0, square, os.path.join(PIECES_FOLDER, 'light', 'Pawn.png') ) if rank.number == 2 else Pawn(1, square, os.path.join(PIECES_FOLDER, 'dark', 'Pawn.png') ) )
                
                elif rank.number in [1, 8]:
                    if file.number in [1, 8]: # rooks
                        self.pieces.append( Rook(0, square, os.path.join(PIECES_FOLDER, 'light', 'Rook.png') ) if rank.number == 1 else Rook(1, square, os.path.join(PIECES_FOLDER, 'dark', 'Rook.png')) )
                    elif file.number in [2, 7]:
                        self.pieces.append( Knight(0, square, os.path.join(PIECES_FOLDER, 'light', 'Knight.png') ) if rank.number == 1 else Knight(1, square, os.path.join(PIECES_FOLDER, 'dark', 'Knight.png')) )
                    elif file.number in [3, 6]:
                        self.pieces.append( Bishop(0, square, os.path.join(PIECES_FOLDER, 'light', 'Bishop.png') ) if rank.number == 1 else Bishop(1, square, os.path.join(PIECES_FOLDER, 'dark', 'Bishop.png')) )
                    elif file.number == 4:
                        self.pieces.append( Queen(0, square, os.path.join(PIECES_FOLDER, 'light', 'Queen.png') ) if rank.number == 1 else Queen(1, square, os.path.join(PIECES_FOLDER, 'dark', 'Queen.png')) )
                    elif file.number == 5:
                        self.pieces.append( King(0, square, os.path.join(PIECES_FOLDER, 'light', 'King.png') ) if rank.number == 1 else King(1, square, os.path.join(PIECES_FOLDER, 'dark', 'King.png')) )

    def flip(self) -> None:
        pass