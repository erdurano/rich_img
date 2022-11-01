"""
A dictionary constructed from cell "bitmap" and unicode char codes that corresponds to
that bitmap structure. Initially directly taken from
github.com/stefanhaustein/TerminalImageViewer.
Key of the dictionary signifies the bitmap of an 4 by 8 cell area
each hex digit (hexit?) signifies a row such that if hex digit is converted to a binary,
each bit represent high state on the hi_lo_bitmap.
"""


BLOCKCHARS = {
    0x00000000: 0x00a0,     # space
    # 0xffff0000, 0x2580,  # upper 1/2, redundant with inverse lower 1/2
    0x0000000f: 0x2581,  # lower 1/8
    0x000000ff: 0x2582,  # lower 1/4
    0x00000fff: 0x2583,
    0x0000ffff: 0x2584,  # lower 1/2
    0x000fffff: 0x2585,
    0x00ffffff: 0x2586,  # lower 3/4
    0x0fffffff: 0x2587,
    # 0xffffffff, 0x2588,  # full, redundant with inverse space
    0xeeeeeeee: 0x258a,  # left 3/4
    0xcccccccc: 0x258c,  # left 1/2
    0x88888888: 0x258e,  # left 1/4
    0x0000cccc: 0x2596,  # quadrant lower left
    0x00003333: 0x2597,  # quadrant lower right
    0xcccc0000: 0x2598,  # quadrant upper left
    # 0xccccffff, 0x2599,  # 3/4 redundant with inverse 1/4
    0xcccc3333: 0x259a,  # diagonal 1/2
    # 0xffffcccc, 0x259b,  # 3/4 redundant
    # 0xffff3333, 0x259c,  # 3/4 redundant
    0x33330000: 0x259d,  # quadrant upper right
    # 0x3333cccc, 0x259e,  # 3/4 redundant
    # 0x3333ffff, 0x259f,  # 3/4 redundant
    # Line drawing subset: no double lines, no complex light lines
    0x000ff000: 0x2501,  # Heavy horizontal
    0x66666666: 0x2503,  # Heavy vertical
    0x00077666: 0x250f,  # Heavy down and right
    0x000ee666: 0x2513,  # Heavy down and left
    0x66677000: 0x2517,  # Heavy up and right
    0x666ee000: 0x251b,  # Heavy up and left

    0x66677666: 0x2523,  # Heavy vertical and right
    0x666ee666: 0x252b,  # Heavy vertical and left
    0x000ff666: 0x2533,  # Heavy down and horizontal
    0x666ff000: 0x253b,  # Heavy up and horizontal
    0x666ff666: 0x254b,  # Heavy cross

    0x000cc000: 0x2578,  # Bold horizontal left
    0x66660000: 0x2579,  # Bold horizontal up
    0x00033000: 0x257a,  # Bold horizontal right
    0x00006666: 0x257b,  # Bold horizontal down

    0x06600660: 0x254f,  # Heavy double dash vertical

    0x000f0000: 0x2500,  # Light horizontal
    0x0000f000: 0x2500,  #
    0x44444444: 0x2502,  # Light vertical
    0x22222222: 0x2502,

    0x000e0000: 0x2574,  # light left
    0x0000e000: 0x2574,  # light left
    0x44440000: 0x2575,  # light up
    0x22220000: 0x2575,  # light up
    0x00030000: 0x2576,  # light right
    0x00003000: 0x2576,  # light right
    0x00004444: 0x2577,  # light down
    0x00002222: 0x2577,  # light down

    # Misc technical
    0x0f000000: 0x23ba,  # Horizontal scanline 1
    0x00f00000: 0x23bb,  # Horizontal scanline 3
    0x00000f00: 0x23bc,  # Horizontal scanline 7
    0x000000f0: 0x23bd,  # Horizontal scanline 9

    # Geometrical shapes. Tricky because some of them are too wide.

    0x00ffff00: 0x25fe,  # Black medium small square
    0x00066000: 0x25aa,  # Black small square

    0x11224488: 0x2571,  # diagonals
    0x88442211: 0x2572,
    0x99666699: 0x2573,
    0x000137f0: 0x25e2,  # Triangles
    0x0008cef0: 0x25e3,
    0x000fec80: 0x25e4,
    0x000f7310: 0x25e5,
}
