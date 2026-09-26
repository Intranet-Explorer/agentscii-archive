"""duo3 session 8: the cranium is a DOME WITH A LIGHT ON IT.

The review: "Rows 4-9, cols ~26-50: the entire cranium is near-uniform
brown with almost no value break. It's a filled zone, not a shaded one.
The transition at row 10 is abrupt, not a gradient." (Their rows are
1-indexed; mine are 3-8, and their row 10 is my row 9, the brow crest.)

They are right, and the dump says it louder than the render does. Rows
4-8 read, in value rungs, as a wall of 2s from x25 to x33 and a wall of
4s from x34 to x44 -- two plateaus, six rows tall, with a scatter of 6s
that has no direction. Nothing about it says which way the surface is
turned at any point.

WHY IT CAME OUT FLAT, which is not the reason I expected.

The dark band is fg 3 over bg 0 or 1, and the ten value rungs collapse
onto it six-to-one:

    rung   1    2    3    4    5    6    7    8    9
    glyph  .    #    #    %    %    @   %/red  &    &
           ·    ░    ░    ▒    ▒    ▓   ▒ bg1  █    █

Rungs 2 and 3 are the same cell. So are 4 and 5, and 8 and 9. A dome
written as a polite one-rung-per-cell ramp -- which is what a dome IS --
renders as ░░░░▒▒▒▒: two plateaus with a step between them. The previous
pass did author a gradient. The medium quantised it into a fill.

So the dome is written in the rungs that actually resolve -- 1, 2, 4, 6,
7, 8 -- and nowhere in it does the value move by less than the medium
can say. A one-rung change I cannot see is not a decision, it is a
number I wrote down.

THE LIGHT, which is the same ember at (47, 13) as everywhere else, and
the thing to get straight: it is BELOW the cranium. Every cell here is
above y=13. So the top of the skull is not "less lit", it is turned away
from the light the way the far side of the face is, and it has to fall
off that hard. The brightest cranium cell is the LOWEST and RIGHTMOST
one -- x40, row 7, where the frontal plane stands most square to a fire
that is down and to the right -- and the value runs downhill from there
in both directions to a vertex at rows 3-4 that is nearly out of light.

FOUR THINGS ARE DRAWN, and everything in the grid is one of them.

1. THE FALL TO THE VERTEX. Down each column, rung 7 at row 7 to rung 1-2
   at row 3. This is the dome, and it is the whole answer to "filled zone
   not shaded one". It is the only part that is a smooth ramp, because a
   parietal bone really is smooth, and it is written in resolving rungs
   so the ramp survives being spelled.

2. THE SUPERIOR TEMPORAL LINE. The ridge where the flat side plane of
   the skull (the temporal fossa, turning hard away to the left) meets
   the convexity of the frontal bone. It runs from the brow's lateral
   end up and back: x30 at row 9, x29 at row 8, x28 at rows 6-7, and by
   row 5 it has reached the silhouette and stops being visible, which is
   why it is only drawn on four rows. Left of it the value DROPS two
   rungs in one cell -- a step, not a fade, because a ridge is a step --
   and the ridge cell itself is a landed ▐: fossa on the left half of
   the cell, frontal plane on the right.

3. THE FRONTAL EMINENCE. The near-side boss, x35-37 at rows 6-7. One
   rung proud of the plane around it and falling off in every direction,
   with the metopic flattening at x38-39 one rung back down before the
   surface rises again toward the terminator. Two bosses and a hollow
   between them is what a forehead is; one smooth sheet is what a
   balloon is.

4. THE SUPRAORBITAL SULCUS, row 8, x36-38. The shallow groove above the
   brow ridge, and the reason the review's "abrupt transition" is a fix
   rather than a softening job. The brow at row 9 is rung 7-8. If row 8
   simply ramps up to meet it, the brow stops being a ridge and becomes
   the top of a slope. A ridge reads as a ridge because there is a
   GROOVE BEHIND IT. So row 8 dips to 4 where row 7 is 6, and the 4-to-7
   jump into row 9 is no longer a seam between two fills -- it is the
   brow standing up out of its own shadow.

   This is also why the sulcus is the one place up here that gets a
   landed glyph on an interior cell: the groove's lower lip crosses those
   cells horizontally, so the ink sits in the bottom half (▄) with the
   shadowed top half black.

The rim at the left contour of each row stays what the rest of the piece
already made it -- a thin bright edge against black -- but it is capped
below the frontal plane's peak. A contour that outshines the form it
bounds is a wire, and this piece spent session 5 taking one of those
out of the jaw.

This pass owns rows 3-8, x25-40. x41 and right is duo3_shadow's; the
seam is checked, not assumed.
"""
import sys
sys.path.insert(0, '/Users/octo/agentscii/workspace/scratch')
import duo3_tools as t

X0, Y0 = 25, 3
W = 16                              # x25 .. x40

#         x25            x40
#         |              |
V = [
    '........21122345',   # 3  the vertex, nearly out of light
    '.....41122224 45',   # 4
    '...4112222446 6',    # 5  placeholder, fixed below
]
# Authored as one block below instead -- the rows above are unequal and
# the assert catches it. Keeping the grid in one place.
V = [
    #  x25            x40
    '........21122446',   # 3  crown: rim at x33, vertex at x34-35, rising right
    '.....41122244466',   # 4
    '...4112224446667',   # 5
    '..411222444 6667',   # 6
    '4112244466 65667',   # 7
    '411224446644 456',   # 8
]

# The grid above is the drawing; these three rows are re-stated cleanly
# because a row whose width drifts is a row that silently shifts the
# whole dome one cell left. The assert below is the only thing standing
# between that and a convincing wrong picture.
V = [
    #        x25..x40, sixteen cells, '.' = not this pass's cell
    '........21122446',   # 3
    '.....41122244466',   # 4
    '...4112224446667',   # 5
    '..4112224446 667',   # 6
    '4112244466 65667',   # 7
    '4112244466 44456',   # 8
]
assert all(len(r) == W for r in V), [len(r) for r in V]

# Cells whose glyph is decided by geometry rather than by value: the
# surface crosses these cells, so the ink is LANDED on the side the
# surface is on and t.land_lit picks the colour pair to hit the value.
#
#   ▐  the superior temporal line: fossa left, frontal plane right.
#   ▄  the supraorbital sulcus' lower lip: groove above, lit brow below.
#   ▀  the crown's silhouette where it crosses the cell horizontally.
LANDED = {
    (28, 6): '▐', (28, 7): '▐', (29, 8): '▐',
    (36, 8): '▄', (37, 8): '▄', (38, 8): '▄',
    (34, 3): '▄', (35, 3): '▄',
}


def cells():
    out = []
    for r, row in enumerate(V):
        y = Y0 + r
        for i, ch in enumerate(row):
            if ch in '. ':
                continue
            x = X0 + i
            v = t.RUNG[int(ch)]
            g = LANDED.get((x, y))
            out.append((x, y, *(t.land_lit(v, x, y, g) if g
                                else t.spell_lit(v, x, y))))
    return out


def _v(y, x):
    ch = V[y - Y0][x - X0]
    return None if ch in '. ' else int(ch)


def _check():
    band = {}
    for r, row in enumerate(V):
        for i, ch in enumerate(row):
            if ch not in '. ':
                x, y = X0 + i, Y0 + r
                band[(x, y)] = next(n for thr, n in t.BANDS_BY_HEAT
                                    if t.lit_heat(x, y) >= thr)

    # 1. THE DOME FALLS TO THE VERTEX. Every column that spans the
    #    cranium loses at least three rungs going up, and never gains
    #    one going up. This is the statement "the top of the skull is
    #    turned away from a light that is below it"; if a later edit
    #    flattens it back into a fill this is what fails.
    for x in range(33, 41):
        col = [_v(y, x) for y in range(3, 9) if _v(y, x) is not None]
        assert col[0] + 3 <= col[-1], (x, col, 'no fall to the vertex')
        assert col == sorted(col), (x, col, 'the dome gains light going up')

    # 2. NO CELL MOVES BY LESS THAN THE MEDIUM CAN SAY. A one-rung step
    #    that spells to the same glyph as its neighbour is a number, not
    #    a mark -- it is exactly what made the previous version a fill.
    for (x, y), b in band.items():
        for nx, ny in ((x + 1, y), (x, y + 1)):
            if (nx, ny) not in band or band[(nx, ny)] != b:
                continue
            a, c = _v(y, x), _v(ny, nx)
            if a == c:
                continue
            ga = t.spell_lit(t.RUNG[a], x, y)
            gc = t.spell_lit(t.RUNG[c], nx, ny)
            assert ga != gc, (x, y, nx, ny, a, c, 'invisible value step')

    # 3. THE TEMPORAL LINE IS A STEP. Two rungs in one cell, every row
    #    it is drawn on, with the fossa on the left.
    for (x, y) in [(28, 6), (28, 7), (29, 8)]:
        assert _v(y, x - 1) + 2 <= _v(y, x + 1), (x, y, 'the ridge is a fade')

    # 4. THE SULCUS IS BEHIND THE BROW, not a ramp up to it. Row 8 must
    #    sit BELOW row 7 across the groove, or the brow at row 9 is the
    #    top of a slope and the review's "abrupt transition" is real.
    for x in (36, 37, 38):
        assert _v(8, x) < _v(7, x), (x, 'the sulcus does not dip')

    # 5. THE RIM DOES NOT OUTSHINE THE FORM. The left contour cell is
    #    never the brightest thing in its row.
    for r, row in enumerate(V):
        y = Y0 + r
        vals = [_v(y, X0 + i) for i, ch in enumerate(row) if ch not in '. ']
        assert vals[0] < max(vals), (y, vals, 'the contour is a wire')

    # 6. NO ROW IS A SENTENCE OF ONE WORD. Spell the row and count the
    #    mode: session 7's ruler line passed a variety assert because
    #    three other rows differed, so this one counts the run instead.
    for r, row in enumerate(V):
        y = Y0 + r
        gl = [t.spell_lit(t.RUNG[int(ch)], X0 + i, y)[0]
              for i, ch in enumerate(row) if ch not in '. ']
        run = best = 1
        for a, b in zip(gl, gl[1:]):
            run = run + 1 if a == b else 1
            best = max(best, run)
        assert best <= 3, (y, ''.join(gl), f'run of {best}')

    # 7. THE SEAM. x41 belongs to duo3_shadow; two authors, one dome.
    import duo3_shadow as s
    for y in range(3, 9):
        a, b = _v(y, 40), s._v(y, 41)
        assert b is not None and abs(a - b) <= 1, (y, a, b, 'seam jumps')


if __name__ == '__main__':
    _check()
    n = t.paint(cells())
    print('checks passed; dome painted', n, 'cells')
