"""duo3 pass 7: background base tone, plus embers off the dissolve.

STYLE.md's rule for backgrounds is base tone first, texture on top --
marks straight onto black read as streaks on black, not as air. So this
pass is the base tone only, and it is the one place in the piece where a
computed field is the right tool: the light falls off from the burning
side the way light does, and hand-placing 500 background cells to
approximate an inverse-square would be worse, not more authored.

The first version of this covered the whole canvas in a lavender oval
that competed with the face -- a computed field is the right tool only
while it stays a base TONE, and that one had become a second subject.
It is much tighter now, and it does not exist at all on the dark side.

Two things keep it from being a clean set of rings:
  - the head OCCLUDES it. Cells to the left of the face get knocked
    down a band, because the head is between them and the only light
    source in the picture.
  - the embers are hand-placed, not scattered by the field. They rise
    and drift right off the temple, which is where the dissolve is
    actually shedding, and they thin out with height.

Only cells that are still empty black get written, so nothing here can
touch the face.
"""
import math
import sys
sys.path.insert(0, '/Users/octo/agentscii/workspace/scratch')
import duo3_tools as t

EMBER_X, EMBER_Y = 47.0, 13.0      # the socket -- the piece's only light
HEAD_L, HEAD_R = 24, 52

def _mine(x, y):
    """Is this cell this pass's territory at all?

    Session 6 made the answer matter. The two guards below used to sit
    inside a one-shot write into cells that were already empty, which
    meant re-running the pass after the head changed shape LAYERED a new
    halo over the old one instead of replacing it. The first time I
    pulled the dissolve in, every cell it vacated kept its old glow and
    the new glow went on top, and the render came back showing more of
    the exact wash the reviewer had complained about. Territory is stated
    once now, cleared, and redrawn.
    """
    if x < HEAD_L + 16 and 1 <= y <= 26:
        # The head is between this light and everything on its far side,
        # so there is no glow over there at all -- the intact half keeps
        # the dark it was modelled against.
        return False
    if 3 <= y <= 24 and x <= t.reach(y) + 2:
        # AND no glow anywhere inside the dissolve. The field has to end
        # against black or its gaps are not gaps, they are a slightly
        # darker ground, and the face fades into the air it is supposed
        # to be leaving -- which is what session 2's version did.
        return False
    return True


# SESSION 6, the falloff itself. This was three rings measured from the
# ember, out to d<22, and the reviewer has now called the right third "a
# structureless wash" three times in three sessions. The rings were not
# the whole of what that meant, but they were the part that GREW: when
# this session cut the front back to the skull, reach() came in with it,
# and every cell the dissolve gave up was claimed by a field that had no
# opinion about where the head was. A background that expands to fill
# whatever the drawing vacates is not a background. It is the absence of
# one, wearing a gradient.
#
# The distance that decides a cell is MARGIN now -- how far past the
# burning edge OF THIS ROW it sits -- and the glow is nine cells of that
# at its deepest and then black. Air lit by a fire is brightest against
# the thing that is burning; it does not go on being lit twenty cells
# away. Ember distance stays in as the second term, so the halo is deep
# beside the orbit and thins to nothing at the crown and the jaw.
cells = [(x, y, ' ', 0, 0) for y in range(28) for x in range(80)
         if _mine(x, y)]
for y, row in enumerate(t.grid(0, 0, 80, 28)):
    for x, (ch, fg, bg) in enumerate(row):
        if not _mine(x, y):
            continue
        m = x - (t.reach(y) if 3 <= y <= 24 else HEAD_R)
        if m < 0:
            continue
        # cells are about twice as tall as wide, so vertical distance
        # counts double or the falloff comes out as an ellipse
        d = math.hypot(x - EMBER_X, 2 * (y - EMBER_Y))
        depth = 9 - int(d / 4)
        if m > depth:
            continue
        if m <= depth / 3:
            cells.append((x, y, '\u2592', 1, 0))
        elif m <= 2 * depth / 3:
            cells.append((x, y, '\u2591', 1, 0))
        elif (x + y) % 2 == 0:
            # The outermost band is thinned on a checker AND spelled in
            # the dimmest glyph there is: a middot over black is four
            # percent ink, a sixth of the light shade, so it is a real
            # step further out without being a step into another hue.
            cells.append((x, y, '\u00b7', 1, 0))


# Embers off the temple: a plume, not a scatter. Bright and dense where
# they leave the face, cooling and thinning as they rise.
# Session 6: pulled in from x64 to x59 and clustered. Spread over
# twenty-four columns these were single cells with four columns of black
# between them, and the control run's review named the result exactly:
# "isolated debris, reads as noise, not embers -- nothing connects them
# to the mass." An ember is only an ember if you can see where it came
# from, so the plume starts ON the burning edge at the orbit and at the
# temple, the two places actually shedding, and every cell in it has a
# neighbour.
EMBERS = [
    (51, 10, '▒', 11), (52, 9, '░', 9), (53, 8, '▒', 9),
    (52, 7, '░', 9), (54, 7, '░', 9), (53, 6, '▒', 9),
    (55, 6, '░', 1), (54, 5, '░', 9), (56, 5, '░', 1),
    (55, 4, '░', 1), (57, 4, '\u00b7', 9), (56, 3, '░', 1),
    (58, 3, '\u00b7', 1), (57, 2, '\u00b7', 1),
    (51, 13, '▓', 11), (52, 12, '▒', 11), (53, 12, '░', 9),
    (53, 11, '▒', 9), (54, 10, '░', 9), (55, 9, '░', 1),
    (54, 14, '░', 9), (55, 13, '▒', 9), (56, 12, '░', 1),
    (57, 11, '░', 1), (58, 10, '\u00b7', 1), (59, 9, '\u00b7', 1),
    (52, 17, '▒', 9), (53, 16, '░', 9), (54, 16, '░', 1),
    (54, 18, '░', 1), (55, 17, '\u00b7', 1),
]
cells += [(x, y, ch, fg, 0) for x, y, ch, fg in EMBERS]

t.paint(cells)
print('cells', len(cells))
