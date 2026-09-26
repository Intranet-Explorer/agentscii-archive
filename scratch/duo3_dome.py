"""duo3 session 8, defect 2: the cranium is a DOME WITH A LIGHT ON IT.

The review: "Rows 4-9, cols ~26-50: the entire cranium is near-uniform
brown with almost no value break. It's a filled zone, not a shaded one.
The transition at row 10 is abrupt, not a gradient." (Their rows are
1-indexed; mine are 3-8, and their row 10 is my row 9, the brow crest.)

WHY IT CAME OUT FLAT, which is not the reason I expected.

The cranium is entirely inside the 'dark' band -- fg 3 over bg 0 or 1 --
and the ten rungs collapse six-to-one onto it:

    rung   0  1  2  3  4  5  6   7    8  9
    glyph  .  .  #  #  %  %  @  %/1   &  &
           ·  ·  ░  ░  ▒  ▒  ▓  ▒bg1  █  █

Rungs 2 and 3 are the same cell. So are 4 and 5, and 8 and 9. A dome
written as a polite one-rung-per-cell ramp -- which is what a dome IS --
renders as ░░░░▒▒▒▒: two plateaus with a step between them. Row 3 came
out as eight identical ▒ from x37 to x44. The previous pass DID author a
gradient. The medium quantised it into a fill.

Six usable levels across twenty columns is three-and-a-bit cells per
level, so authoring in value alone cannot do better than runs of three
whatever I write. That is a floor of the medium, not a failure of care.

WHAT GETS UNDER IT. Measured, not assumed:

    ░ 0.12    ▒ 0.24    ▓ 0.36    █ 0.48
              ▄ 0.24    ▀ 0.24    ▌ 0.24    ▐ 0.24

Five glyphs share one value. So the plateau can be broken WITHOUT moving
the value -- which is my own outstanding NEXT line from last session,
and it turns out to be arithmetic rather than aspiration. A ▄ says the
lit half of this cell is its BOTTOM half. On a dome above a fire that is
the true statement wherever the surface is falling away fast as it goes
up, and it is a lie where the surface is flat.

THE LIGHT. The same ember at (47, 13), and the thing to get straight: it
is BELOW the cranium. Every cell here is above y=13. So the top of the
skull is not "less lit", it is turned away the way the far side is, and
it falls off that hard. Value runs downhill from the frontal plane at
x40-43 row 8 -- where the forehead stands most square to a fire that is
down and to the right -- to a vertex at row 3 that is nearly out of
light, and downhill again to the left, into the temporal fossa.

FOUR THINGS ARE DRAWN. Everything in the grid is one of them.

1. THE FALL TO THE VERTEX. Down each column, rung 6-7 at row 8 to rung
   1-2 at row 3. This is the dome, and it is the whole answer to "filled
   zone, not shaded one".

2. THE SUPERIOR TEMPORAL LINE. The ridge where the flat side plane of
   the skull turns hard away to the left. It runs from the brow's
   lateral end up and BACK: x30 at row 9, x29 at row 8, x28 at rows 6-7,
   and by row 5 it has reached the silhouette and stops being a separate
   mark. Left of it the value DROPS two rungs in ONE cell -- a step, not
   a fade, because a ridge is a step -- and the ridge cell is a landed
   ▐: fossa on the left half of the cell, frontal plane on the right.
   Below row 7 the fossa finally opens to three cells wide, which is
   why the temple only reads as a hollow at the bottom of this region.

3. THE FRONTAL EMINENCE. The near-side boss, x36-37 at rows 6-7, one
   rung proud, with the metopic flattening at x38-39 one rung back down
   before the surface rises again toward the terminator. Two bosses and
   a hollow between them is what a forehead is; one smooth sheet is what
   a balloon is.

4. THE SUPRAORBITAL SULCUS, row 8, x36-38. The shallow groove above the
   brow ridge, and the reason the review's "abrupt transition at row 10"
   is a fix rather than a softening job. The brow at row 9 is rung 7-8.
   If row 8 simply ramps up to meet it, the brow stops being a ridge and
   becomes the top of a slope. A ridge reads as a ridge because there is
   a GROOVE BEHIND IT. So row 8 dips where row 7 is high, and the jump
   into row 9 is no longer a seam between two fills -- it is the brow
   standing up out of its own shadow.

THE GLYPH LAYER, and the one thing in this file that is derived rather
than authored. ▄ goes where the value picture ALREADY says the surface
is falling away fast upward -- a two-rung drop between this cell and the
one above it. That is not a rule over a region: it is read off the
authored dome, so it comes out as a diagonal band following the
terminator, high on the left where the skull turns early and low on the
right where the fire holds on. A horizontal stripe of ▄ would mean the
value picture had a horizontal stripe in it, and the check below is what
says it does not. Everything else landed -- the contour, the temporal
line, the sulcus lip, the crown -- is authored in LAND, one entry per
cell, because those are boundaries anatomy puts there and not ones the
value picture can know about.

THE REGION THIS PASS OWNS: rows 3-8, x <= 46. Stated once, used for both
the clear and the write. x47 and out on these rows is duo3_shadow's far
contour -- the parietal turning over into black -- which the review did
not fault and which this pass does not touch. The seam is checked.
"""
import sys
sys.path.insert(0, '/Users/octo/agentscii/workspace/scratch')
sys.path.insert(0, '/Users/octo/agentscii')
import canvas_tools as ct
import duo3_tools as t

X0, Y0, X1 = 25, 3, 46
W = X1 - X0 + 1                          # x25 .. x46

# The dome, in rungs. One block, one place. A row whose width drifts
# shifts the whole cranium a cell sideways and renders completely
# convincingly, so the assert below is the only thing standing between
# that and a plausible wrong picture.
#
# Read it as bands and they run DIAGONALLY, which is the point: a band
# of constant value is what a shaded dome is made of, and the review's
# complaint was that these ones were horizontal. The bright pole is the
# frontal plane at x40-43 row 7-8, square to a fire that is down and to
# the right, and the bands arc up and away from it to a vertex at row 3
# that is nearly out of light.
V = [
    #  x25   x30   x35   x40   x45
    #  |     |     |     |     |
    '........1112222444211',    # 3  the crown, grazing the light at best
    '.....1122224422444222 1',  # 4  placeholder; re-stated below
]
V = [
    #  x25   x30   x35   x40   x45
    #  |     |     |     |     |
    '........222244444421..',   # 3  crown; brightest at x40-42, not at the crest
    '.....11222244224442221',   # 4  the METOPIC GROOVE opens at x38-39
    '...2244446666446664421',   # 5
    '..24446666777667766421',   # 6  the FRONTAL EMINENCE, x35-37
    '1224466677777667777422',   # 7
    '1122446677644467776422',   # 8  the SUPRAORBITAL SULCUS, x36-38
]
assert all(len(r) == W for r in V), [len(r) for r in V]

# Cells whose glyph is decided by where a boundary falls, not by value.
# t.land_lit() then picks the colour pair in that cell's heat band that
# comes closest to the authored value, so a landed cell costs no
# brightness -- ▒ ▄ ▀ ▌ ▐ are all 0.24 over black here.
#
#   ▄  the crown's top edge crossing the cell horizontally, and the
#      sulcus' lower lip, which crosses the same way for the same reason.
#   ▌  the crown turning over to the RIGHT past the terminator: the
#      boundary in these cells is vertical, not horizontal.
#   ▐  the superior temporal line, and the left contour: fossa (or
#      black) on the left half, frontal plane on the right.
#   ▓  the sagittal crest at x37-39 row 3, where the skull's top is flat
#      across the cell so the cell is FULL and nothing is landed.
LAND = {
    # ROW 3, THE CROWN. This row is the top silhouette, so a boundary
    # crosses every cell in it -- but the crown is rung 1-2 and a
    # half-block's floor in this band is 0.24, so most of it CANNOT
    # carry a landed edge (METHOD, session 7: the darkest cells in a
    # piece cannot carry one; their edge is drawn on the lit cell
    # beside them). Only the four cells at rung 4 can, and they are the
    # ones where the crown is brightest anyway.
    (40, 3): '\u2584', (41, 3): '\u2584', (42, 3): '\u2584',
    # the left contour: black on the left half of the cell, skull on the
    # right. Not a bright rim -- the fire is in FRONT of the head, so
    # this edge is the part turned furthest from it.
    (30, 4): '\u2590', (28, 5): '\u2590', (27, 6): '\u2590',
    (25, 7): '\u2590', (25, 8): '\u2590',
    # THE SUPERIOR TEMPORAL LINE: fossa left, frontal plane right.
    (28, 6): '\u2590', (28, 7): '\u2590', (29, 8): '\u2590',
    # THE SUPRAORBITAL SULCUS' lower lip, crossing these cells
    # horizontally: groove above, the brow rising out of it below.
    (36, 8): '\u2584', (37, 8): '\u2584', (38, 8): '\u2584',
    # the far crown turning over to the right, where the boundary in the
    # cell is vertical rather than horizontal.
    (44, 5): '\u258c', (44, 6): '\u258c',
}


def owns(x, y):
    return Y0 <= y <= Y0 + len(V) - 1 and X0 <= x <= X1


def _v(y, x):
    if not owns(x, y):
        return None
    ch = V[y - Y0][x - X0]
    return None if ch in '. ' else int(ch)


def glyph_of(x, y):
    """Landed ONLY where anatomy puts a boundary. Nothing derived.

    REJECTED, and it is the main thing this pass learned. The first
    version of this function landed a half-block wherever the authored
    value picture said the surface was turning fastest -- ▄ where the
    vertical rung step across the cell beat the horizontal one, ▐/▌
    where it lost. The argument for it was that it is read off the
    picture rather than off a coordinate, so it would follow the
    terminator and come out diagonal.

    It came out as row 5 spelled ▄ twelve times in a row. Of course it
    did: row 5 IS the terminator band, so the criterion is true of every
    cell in it, and a criterion true of every cell in a region is a
    region rule no matter what it is derived from. It is the same shape
    of mistake as session 7's ruler line, and it would have shipped as
    "horizontal stripes laid across the form" -- the exact defect it was
    written to fix.

    The brief's wording is the correction: make the glyph carry where
    the surface crosses the cell "so brow, arch and jaw read as RIDGES
    SEEN EDGE-ON rather than as bars". A half-block is for a ridge, an
    edge, a lip. Smooth dome is what the shade ramp is FOR, and a dome
    reads as a dome because its bands curve -- which they do here, and
    check 6 is what says they do.
    """
    return LAND.get((x, y))

def cells():
    out = []
    for r, row in enumerate(V):
        y = Y0 + r
        for i, ch in enumerate(row):
            if ch in '. ':
                continue
            x = X0 + i
            v = t.RUNG[int(ch)]
            g = glyph_of(x, y)
            out.append((x, y, *(t.land_lit(v, x, y, g) if g
                                else t.spell_lit(v, x, y))))
    return out


def clear(slug=t.SLUG):
    d = ct.load_canvas(t.W, slug)
    for key in [k for k in d['glyph_override']
                if owns(int(k.split(',')[1]), int(k.split(',')[0]))]:
        del d['glyph_override'][key]
    for py, row in enumerate(d['pixels']):
        for x in range(d['w']):
            if owns(x, py // 2):
                row[x] = 0
    ct.save_canvas(t.W, slug, d)


def spelled():
    """The region as it will render, one char per cell. The dump METHOD
    says to read before looking -- three identical rows are invisible in
    a picture and obvious here."""
    out = []
    for r, row in enumerate(V):
        y = Y0 + r
        s = ''
        for i, ch in enumerate(row):
            if ch in '. ':
                s += ' '
                continue
            x = X0 + i
            g = glyph_of(x, y)
            s += (t.land_lit(t.RUNG[int(ch)], x, y, g) if g
                  else t.spell_lit(t.RUNG[int(ch)], x, y))[0]
        out.append(s)
    return out


def _triples():
    """Every owned cell as it will actually render. The blob check has
    to compare the full (glyph, fg, bg): rung 4 and rung 6 both spell ▄
    under land_lit but land on different grounds, so two cells with the
    same glyph can be plainly different cells."""
    out = {}
    for r, row in enumerate(V):
        y = Y0 + r
        for i, ch in enumerate(row):
            if ch in '. ':
                continue
            x = X0 + i
            g = glyph_of(x, y)
            out[(x, y)] = (t.land_lit(t.RUNG[int(ch)], x, y, g) if g
                           else t.spell_lit(t.RUNG[int(ch)], x, y))
    return out


def _uniform_square(x, y, n):
    """Is the n x n block with this cell at its top-left all one cell?"""
    c = _triples()
    v = c.get((x, y))
    return v is not None and all(c.get((x + dx, y + dy)) == v
                                 for dx in range(n) for dy in range(n))


def _largest_blob():
    """The biggest connected run of identical cells in the region."""
    cell = _triples()
    seen, best = set(), 0
    for k in cell:
        if k in seen:
            continue
        stack, n = [k], 0
        seen.add(k)
        while stack:
            x, y = stack.pop()
            n += 1
            for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if q not in seen and cell.get(q) == cell[k]:
                    seen.add(q)
                    stack.append(q)
        best = max(best, n)
    return best


def _check():
    # 1. THE DOME FALLS TO THE VERTEX. Every column of the cranium
    #    loses at least three rungs on the way up to row 3 and never
    #    gains one going up. This is the sentence "the top of the skull
    #    is turned away from a light that is below it"; if a later edit
    #    flattens it back into a fill this is what fails. Rows 3-7 only:
    #    row 8 is the SULCUS and is meant to fall, which is check 3.
    #    x38-39 is excluded because it is the METOPIC GROOVE and is the
    #    one place up here that genuinely is not a simple dome -- it is
    #    checked as a groove instead, in check 4b. Excluding it is the
    #    honest move; loosening check 1 until the groove fit through
    #    would have let a flattened dome through with it.
    for x in list(range(33, 38)) + list(range(40, 44)):
        col = [_v(y, x) for y in range(3, 8) if _v(y, x) is not None]
        assert col[0] + 3 <= col[-1], (x, col, 'no fall to the vertex')
        assert col == sorted(col), (x, col, 'the dome gains light going up')

    # 2. THE TEMPORAL LINE IS A STEP, two rungs in one cell, fossa left.
    for (x, y) in [(28, 6), (28, 7), (29, 8)]:
        assert _v(y, x - 1) + 2 <= _v(y, x + 1), (x, y, 'the ridge is a fade')

    # 3. THE SULCUS IS BEHIND THE BROW, not a ramp up to it. Row 8 must
    #    sit BELOW row 7 across the groove, or the brow at row 9 is
    #    merely the top of a slope and the "abrupt transition" is real.
    for x in (36, 37, 38):
        assert _v(8, x) < _v(7, x), (x, 'the sulcus does not dip')

    # 4. THE FRONTAL EMINENCE IS PROUD OF THE METOPIC DIP BESIDE IT.
    for y in (6, 7):
        assert _v(y, 37) > _v(y, 38), (y, 'the forehead is one sheet')

    # 4b. THE METOPIC GROOVE IS A GROOVE, down its whole length: lower
    #     than the frontal eminence on its left AND than the plane on
    #     its right, every row it is drawn on. Two bosses and a hollow
    #     between them is a forehead; one smooth sheet is a balloon.
    for y in range(4, 8):
        for x in (38, 39):
            assert _v(y, x) < _v(y, 37) and _v(y, x) < _v(y, 40), \
                (y, x, 'the metopic groove has filled in')

    # 5. THE CONTOUR IS NOT A WIRE. The leftmost inked cell of a row is
    #    never the brightest thing in that row -- the defect session 5
    #    took out of the jaw, which this pass could hand straight back.
    for r, row in enumerate(V):
        y = Y0 + r
        vals = [_v(y, X0 + i) for i, ch in enumerate(row) if ch not in '. ']
        assert vals[0] < max(vals), (y, vals, 'the contour is a wire')

    # 6. IT IS A DOME, NOT A FILLED ZONE -- and this is the one check
    #    in the file with a number in it, because the review's charge
    #    was itself a measurement: "near-uniform brown with almost no
    #    value break ... a filled zone, not a shaded one."
    #
    #    Measured on the version this pass replaces: of 113 inked cells
    #    in rows 3-8 x25-46, FIFTY-ONE were a single connected blob of
    #    identical (glyph, fg, bg). Forty-five per cent of the cranium
    #    was one cell repeated. That is the defect, stated as a number,
    #    and it is a detector of absence rather than a target -- the
    #    way to satisfy it uniformly is dither, which the brief names
    #    as the same defect in a different coat, so check 6b guards the
    #    other side of it.
    #    Blob size alone is the wrong number, and finding that out was
    #    worth the detour: the largest blob in the version below is 13
    #    cells, and it is a stair-stepped DIAGONAL running from (34,5)
    #    to (31,8) -- a value band on a dome, which is the thing I am
    #    trying to draw. Thresholding size would have failed the fix.
    #
    #    What separates a band from a fill is THICKNESS. A band is
    #    everywhere one or two cells deep, because the value is changing
    #    across the curve; a filled zone is deep in both directions at
    #    once. So: no run of identical cells is ever three cells thick
    #    in both directions. Measured across the same region,
    #
    #        before   113 cells, largest blob 51, 3x3 solid present
    #        after    112 cells, largest blob 13, none
    #
    solid = [(x, y) for (x, y) in _triples()
             if _uniform_square(x, y, 3)]
    assert not solid, (solid[:3], 'the cranium is still a filled zone')
    # 6b. AND NOT NOISE. The cheapest way to pass check 6 is to make
    #     every cell differ from its neighbours, which would score
    #     perfectly and read as static. A dome reads as a dome because
    #     its value changes ACROSS THE CURVE, so most cells SHOULD match
    #     a neighbour: bands are the thing being drawn.
    sp = _triples()
    same = sum(1 for (x, y), v in sp.items()
               if any(sp.get(n) == v for n in ((x + 1, y), (x - 1, y),
                                               (x, y + 1), (x, y - 1))))
    assert same >= 0.75 * len(sp), (same, len(sp), 'the dome is dither')

    # 7. NO HORIZONTAL STRIPE. Blobs are fine and bars are not, and the
    #    difference is orientation: the review said "horizontal stripes
    #    LAID ACROSS the form". Four wide and two tall is a bar.
    for (x, y), v in sp.items():
        if all(sp.get((x + c, y + r)) == v for r in (0, 1) for c in range(4)):
            raise AssertionError((y, x, v, 'horizontal stripe'))

    # 8. THE SEAM at x46/x47. x47 out is duo3_shadow's far contour; two
    #    passes, one skull. A jump here is a visible vertical join.
    import duo3_shadow as s
    for y in range(Y0, Y0 + len(V)):
        a = _v(y, X1)
        b = s._v(y, X1 + 1)
        if a is None or b is None:
            continue
        assert abs(a - b) <= 2, (y, a, b, 'the seam jumps')


if __name__ == '__main__':
    for y, s in zip(range(Y0, Y0 + len(V)), spelled()):
        print(f'{y:3d}  {s}')
    _check()
    clear()
    print('checks passed; dome painted', t.paint(cells()), 'cells')
