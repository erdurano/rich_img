from typing import Sequence, Tuple
from typing import NamedTuple
from .block_chars import BLOCKCHARS
from collections import Counter


Pixel = Tuple[int, int, int]


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
    if not pixels:
        return (0, 0, 0)
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


def get_split_flags(pixels: Sequence[Tuple[int, int, int]]) -> int:

    counter = Counter(pixels).most_common()

    if len(counter) == 1:
        return 0xffffffff
    if (len(counter) > 2) & (sum(count[1] for count in counter[:2]) > 16):

        color1 = counter[0]
        color2 = counter[1]
        flags = 0
        for pixel in pixels:
            flags <<= 1
            diff1 = 0
            diff2 = 0
            for index, channel in enumerate(pixel):
                diff1 += (color1[0][index] - channel) ** 2
                diff2 += (color2[0][index] - channel) ** 2
            if diff1 > diff2:
                flags |= 1
        return flags

    else:

        channels = tuple(zip(*pixels))
        split_r = max(channels[0]) - min(channels[0])
        split_g = max(channels[1]) - min(channels[1])
        split_b = max(channels[2]) - min(channels[2])
        split_channels = (split_r, split_b, split_g)
        max_split = max(split_channels)
        split_index = split_channels.index(max_split)
        split_value = min(channels[split_index]) + max_split/2

        split_flags = 0
        for pix in pixels:
            split_flags <<= 1
            if pix[split_index] > split_value:
                split_flags |= 1

        return split_flags


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


def get_block_char(hi_flags: int) -> Tuple[int, int, bool]:
    """
    returns block char with closest charflag to the hi_flags of the cell and
    whether it is inverted or not
    """

    min_diff = 0xffffffff  # initially set to max value
    inverted = False       # sensible default

    code = 0x00a0  # space
    flags = 0x00000000

    for char_flags, char_code in BLOCKCHARS.items():
        diff = diff_from_charflags(hi_flags, char_flags)

        if diff == 0:  # checks for exact match

            code = char_code
            flags = char_flags
            break

        elif diff == 32:  # checks for inverted match

            flags, code, inverted = char_flags, char_code, True
            break

        elif diff <= min_diff:  # closest char

            min_diff = diff
            code = char_code
            flags = char_flags

        elif (d := 32-diff) <= min_diff:  # closest inverse char
            min_diff = d
            code = char_code
            flags = char_flags
            inverted = True

    return flags, code, inverted


def get_cell_from_pattern(pixels: Sequence[Pixel],
                          codepoint: int = 0x2584,
                          pattern: int = 0x0000ffff) -> RasterCell:
    """
    Returns a raster cell from flattend pixel sequence with a
    code point with a specified pattern. Defaults to half block.
    """

    mask = 0x80000000
    fg_pixels = []
    bg_pixels = []
    for pixel in pixels:
        if mask & pattern:
            fg_pixels.append(pixel)
        else:
            bg_pixels.append(pixel)
        mask >>= 1
    fg_color = get_color_avg(fg_pixels)
    bg_color = get_color_avg(bg_pixels)

    return RasterCell(fg_color, bg_color, chr(codepoint))


def get_cell(pixels: Sequence[Tuple[int, int, int]]) -> RasterCell:
    hi_flags = get_split_flags(pixels)
    char_flags, charcode, invert = get_block_char(hi_flags)

    hi_cells = []
    lo_cells = []
    fg_cells = []
    bg_cells = []
    mask = 1 << 31
    for pixel in pixels:
        if hi_flags & mask:
            hi_cells.append(pixel)
        else:
            lo_cells.append(pixel)

        if char_flags & mask:
            fg_cells.append(pixel)
        else:
            bg_cells.append(pixel)
        mask >>= 1
    fg_color = get_color_avg(fg_cells)
    bg_color = get_color_avg(bg_cells)
    # if invert:
    #     fg_color, bg_color = bg_color, fg_color

    return RasterCell(fg_color, bg_color, chr(charcode))
