import itertools
from PIL import Image
from rich_img.image import get_cell
from rich.segment import Segment, SegmentLines
from rich.style import Style
from rich.color import Color, ColorType
from rich.color_triplet import ColorTriplet
from rich.console import Console
from typing import Tuple, Mapping

Pixel = Tuple[int, int, int]
Coordinate = Tuple[int, int]
PixelAccessor = Mapping[Coordinate, Pixel]

with Image.open("./tests/img/island.jpg") as file:
    img_size = file.size
    pix: PixelAccessor = file.load()  # type: ignore

print(img_size)

to_render = []
for y in range(0, img_size[1]-8, 8):
    li = []
    for x in range(0, img_size[0]-4, 4):
        pixels = [pix[(x, y)]
                  for y, x in itertools.product(range(y, y+8), range(x, x+4))]
        cell = get_cell(pixels)

        seg = Segment(
            cell.char,
            Style(
                bgcolor=Color('bg', type=ColorType(3),
                              triplet=ColorTriplet(*cell.bg_color)),
                color=Color("fg", type=ColorType(3),
                            triplet=ColorTriplet(*cell.fg_color))
            )
        )

        li.append(seg)
    to_render.append(li)

rend = SegmentLines(to_render, new_lines=True)

c = Console()
c.print(rend)
c.print('\n')
