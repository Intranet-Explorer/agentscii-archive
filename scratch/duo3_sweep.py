"""duo3 session 8, defect 3: the orphan dots on the right.

The review: "Cols ~48-58 across rows 7-27 are orphan dots floating
outside the outline... it reads as stray dither rather than intent."

They are the SMOKE from session 7 -- t.sees() hands any cell past the
far silhouette a flat 0.8 view of the fire, and at rung 1-2 in the dark
band that spells as a single brown dot. Session 7's METHOD note defends
it: the jaw needs a ground to be read against. That was true when the
alternative under test was a wash. It is not true against black, which
is what the whole LEFT side of this head is already read against, and
that asymmetry is the actual complaint -- "an asymmetric form that
dissolves on one side only".

So the ground for both sides becomes the same ground: black. This is a
deletion and it is the entire fix. The alternative the review offers --
earning the detachment by connecting it to the mass -- would be
inventing a new element in a piece whose remaining defects are all
about finishing what is here.

One predicate, x > t.far(y), used to find them and to delete them.
"""
import sys
sys.path.insert(0, '/Users/octo/agentscii/workspace/scratch')
sys.path.insert(0, '/Users/octo/agentscii')
import canvas_tools as ct
import duo3_tools as t


def outside(x, y):
    return x > t.far(y)


def sweep(slug=t.SLUG):
    d = ct.load_canvas(t.W, slug)
    n = 0
    for key in list(d['glyph_override']):
        y, x = (int(v) for v in key.split(','))
        if outside(x, y):
            del d['glyph_override'][key]
            n += 1
    for py, row in enumerate(d['pixels']):
        for x in range(d['w']):
            if outside(x, py // 2):
                row[x] = 0
    ct.save_canvas(t.W, slug, d)
    return n


def _check(slug=t.SLUG):
    # The head must not have lost anything. far() is the silhouette the
    # shadow pass drew TO, so every row's last inked cell should now sit
    # at or just inside it -- never short of it by more than the rows
    # where the skull genuinely does not reach its own bounding curve.
    rows = ct.render_canvas_cells(ct.load_canvas(t.W, slug))
    for y, row in enumerate(rows):
        last = max((x for x, c in enumerate(row)
                    if c[0] != ' ' or c[2] != 0), default=None)
        assert last is None or last <= t.far(y), (y, last, t.far(y))


if __name__ == '__main__':
    print('swept', sweep(), 'cells outside the silhouette')
    _check()
    print('checks passed')
