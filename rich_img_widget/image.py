from typing import Sequence, Tuple
from typing import NamedTuple
from .block_chars import BLOCKCHARS


class RasterCell(NamedTuple):
    '''
    Represents equivalent cell to a 4 by 8 pixels region as foreground color,
    background color and character
    '''
    fg_color: Tuple[int, int, int]
    bg_color: Tuple[int, int, int]
    char: str


def get_color_avg(pixels: Sequence[Tuple[int, int, int]]) -> Tuple[int, int, int]:
    """Returns average color of a grup of pixels represented by rgb 3tuple"""
    size = len(pixels)
    red_total, green_total, blue_total = 0, 0, 0
    for red, green, blue in pixels:
        red_total += red
        green_total += green
        blue_total += blue

    return (red_total // size, green_total // size, blue_total // size)


def get_hi_flags(pixels: Sequence[Tuple[int, int, int]]) -> int:
    """
    Returns a tuple of booleans from a flattened pixel region which describes pixels
    that higher than or equal to the average of that region.
    """

    def get_pixel_vec_square(pixel: Tuple[int, int, int]) -> int:
        """
        gets and sums the three components of pixel to get a scalar value
        of the pixel's color "vector". It is purely for comparison purposes.
        """
        return sum((component**2 for component in pixel))

    avg_vec_sqr = get_pixel_vec_square(get_color_avg(pixels))

    hi_flags = 0

    for pixel in pixels:
        hi_flags <<= 1
        if get_pixel_vec_square(pixel) >= avg_vec_sqr:
            hi_flags |= 1

    return hi_flags


def diff_from_charflags(
        hi_flags: int,
        char_flags: int) -> int:
    '''
    Finds how many pixels' high values are different than given char_flag integer.
    with an XOR operation difference in bit flags obtained and count
    returned with int.bit_count()
    '''
    masked = hi_flags ^ char_flags
    return masked.bit_count()


def get_block_char(hi_flags: int) -> Tuple[int, bool]:
    """
    returns block char with closest charflag to the hi_flags of the cell and
    whether it is inverted or not
    """

    min_diff = 0xffffffff  # initially set to max value
    inverted = False       # sensible default

    code = 0x00a0  # space

    for char_flags, char_code in BLOCKCHARS.items():
        diff = diff_from_charflags(hi_flags, char_flags)

        if diff == 0:  # checks for exact match

            code = char_code
            break

        elif diff == 32:  # checks for inverted match

            code, inverted = char_code, True
            break

        elif diff <= min_diff:  # closest char

            min_diff = diff
            code = char_code

        elif (d := 32-diff) <= min_diff:  # closest inverse char
            min_diff = d
            code = char_code
            inverted = True

    return code, inverted


# def get_cell(pixels: Sequence[Tuple[int, int, int]]) -> RasterCell:
#     pass
