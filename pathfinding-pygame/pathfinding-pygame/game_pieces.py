import pygame as pg

from typing import Tuple

from utils import Dimension

class Chip:
    """
    Class for representing chips on the board
    """
    def __init__(self, x: int, y: int):
        """
         Creates a new ``Chip`` instance.
        """
        self.x, self.y = x, y
        self.angle = 0
        self.speed = 0

    @property
    def window_coordinates(self) -> Tuple[int, int]:
        """
        Transform board coordinates of chip to window coordinates

        :return: coordinates of top left corner of chip
        """
        return self.x * Dimension.SQUARE_WIDTH.value, self.y * Dimension.SQUARE_HEIGHT.value

    @property
    def movement_vector(self) -> Tuple[int, int]:
        """
        Returns movement vector(direction) of chip

        :return: movement vector of chip
        """
        return self.angle, self.speed

    @staticmethod
    def convert_to_board_coordinates(clicked_position: Tuple[int, int]) -> Tuple[int, int]:
        x, y = clicked_position
        x = min(x // Dimension.SQUARE_WIDTH.value, Dimension.board_width() - 1)
        y = min(y // Dimension.SQUARE_HEIGHT.value, Dimension.board_height() - 1)

        return x, y

    @property
    def board_coordinates(self) -> Tuple[int, int]:
        return self.x, self.y

    def draw(self, window: pg.Surface, color: Tuple[int, int, int]):
        """
        Full fill chip with given color.

        :param window: window created by pygame
        :param color: color in RGB format
        :return: None
        """
        shifted_window_coordinates = tuple(coord + 1 for coord in self.window_coordinates)
        rect = (shifted_window_coordinates, (Dimension.SQUARE_WIDTH.value - 1, Dimension.SQUARE_HEIGHT.value - 1))
        pg.draw.rect(window, color, rect)

        pg.display.update(rect)

    def __eq__(self, other):
        if isinstance(other, Chip):
            return self.board_coordinates == other.board_coordinates
        return NotImplemented

    def __hash__(self):
        return hash(self.board_coordinates)

    def draw_chips(self):
        """
        Draws game pieces on the board.

        :return: None
        """
        for chip in Chip.chips:
            chip.draw(self.window)

    def update(self):
        """
        Updates game pieces.

        :return: None
        """
        