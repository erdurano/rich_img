from typing import Sequence, Tuple


def get_cell_avg(pixels: Sequence[Tuple[int, int, int]]) -> Tuple[int, int, int]:
    size = len(pixels)
    red_total, green_total, blue_total = 0, 0, 0
    for red, green, blue in pixels:
        red_total += red
        green_total += green
        blue_total += blue

    return (int(red_total / size), int(green_total / size), int(blue_total / size))


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

    avg_vec_sqr = get_pixel_vec_square(get_cell_avg(pixels))

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
