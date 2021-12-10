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

class File:
    def __init__(self, xcoord:float, letter:str):
        self.letter = letter
        self.number = number
    
    def __str__(self):
        return f"{self.letter.lower()}"

class Square:
    def __init__(self, file:File, rank:Rank, board):
        self.file = file
        self.piece = None
        self.rank = rank

    def __str__(self):
        return f"{file.__str__()}{rank.__str__()} - {self.piece.__str__()}"

    def isDark(self) -> bool:
        pass

class Piece:
    def __init__(self, square:Square, image:str):
        """
        the image string must be a path to a valid image file
        """
        if not os.path.exists(image):
            raise FileNotFoundError
        self.square = square
        self.image = pygame.image.load(image)
        
    def moveIsValid(self, destination:Square):
        return True
    
    def move(self, destination):
        pass

class Pawn(Piece):
    def moveIsValid(self, destination):
        king = [ f for f in self.square.board.pieces ]