#!/usr/bin/env python3
# raze -- MOTION SEED // AGENTSCI  (WIP, NOT finished)
# hollis's planted idea for a 4th suite piece: motion THROUGH the world. The trio is
# crowd / face / world; what's missing is movement across THE HORIZON's lit band.
# This seed = ONE long panel showing the procession MID-STRIDE at staggered x-positions,
# legs alternating (walk cycle), each figure backlit by the same CYAN sun as THE HORIZON.
# Bounded: a single static "filmstrip" panel for now; could become N frames later.
# Reuses make_horizon's light field + figure() so it shares the world, not just the palette.

import sys
sys.path.insert(0, 'scratch')
from canvas import Canvas, dither_region  # house primitives
W = 80
H = 46
cv = Canvas(W, H)

# --- reuse THE HORIZON's exact light field so it reads as the SAME world ---
SUNX, SUNY, SUNR = 53.0, 12.0, 3.0   # sun high in this wide panel (figures walk below it)
HORIZON = 34
def sun_glow(x, y):
    d = ((x - SUNX)**2 + (y - SUNY)**2) ** 0.5
    t = max(0.0, 1.0 - d/5.0)
    return t*t

# neutral-gray sky -> black ground, cyan light source (matches accepted THE HORIZON)
for y in range(H):
    for x in range(W):
        if y < HORIZON:
            g = sun_glow(x, y) * 0.35 + 0.04
            ch = '\u2591' if g > 0.18 else ' '
            fg = 94 if g > 0.35 else (7 if g > 0.12 else 8)
            cv.set(x, y, ch=ch, fg=fg, bg=0)
        else:
            cv.set(x, y, ch=' ', fg=0, bg=0)

# lit dusk band at the horizon (cyan, brightest under sun)
for x in range(W):
    g = sun_glow(x, HORIZON) * 1.3 + 0.25
    if g > 0.1:
        cv.set(x, HORIZON, ch='\u2593', fg=96, bg=0)

# --- the WALK CYCLE: a figure with two legs at different x = mid-stride ---
def walker(cx, base_y, h, phase):
    """phase 0/1 selects which leg is forward -> alternating stance reads as walking."""
    # body column
    for dy in range(2, h):
        y = base_y - dy
        if cv.in_bounds(cx, y):
            cv.set(cx, y, ch='\u2588', fg=0, bg=0)
    # head
    for dy in range(2):
        y = base_y - (h - 1 - dy)
        if cv.in_bounds(cx, y):
            cv.set(cx, y, ch='\u2588', fg=0, bg=0)
    # two legs at the feet, offset by phase -> stride
    leg_dx = [(-1, 0), (0, 1)] if phase == 0 else [(0, 1), (-1, 0)]
    for a, b in leg_dx:
        lx = cx + a
        ly = base_y - 1
        if cv.in_bounds(lx, ly):
            cv.set(lx, ly, ch='\u2588', fg=0, bg=0)
    # backlit cyan rim on sun-facing side
    rim_x = cx + 1 if SUNX >= cx else cx - 1
    for dy in range(2, h):
        y = base_y - dy
        if cv.in_bounds(rim_x, y):
            cur = cv.get(rim_x, y)
            if cur[0] != '\u2588':
                cv.set(rim_x, y, ch='\u2591', fg=96, bg=0)

# procession mid-stride: staggered x, alternating phase -> reads as a walking line
xs = [10, 18, 26, 34, 42, 50, 58, 66]
for i, cxp in enumerate(xs):
    walker(cxp, HORIZON, 7 + (i % 3), phase=i % 2)

# sun disc: cyan ring -> white core
for y in range(int(SUNY-SUNR)-1, int(SUNY+SUNR)+2):
    for x in range(int(SUNX-SUNR)-1, int(SUNX+SUNR)+2):
        d = ((x-SUNX)**2 + (y-SUNY)**2)**0.5
        if d <= SUNR:
            core = d <= SUNR*0.45
            cv.set(x, y, ch='\u2588', fg=15 if core else 96, bg=0)

# tagline
def put_centered(s, y):
    x = (W - len(s)) // 2
    for i, ch in enumerate(s):
        cv.set(x+i, y, ch=ch, fg=94, bg=0)
put_centered("// the procession, walking //", 3)

rows=[]
cv.render(rows)
lines=[r+chr(10) for r in rows]
open('_motion_seed.ans','w').write(chr(27)+'0m'+''.join(lines)+chr(27)+'0m')
print('wrote scratch/_motion_seed.ans -- WIP seed for hollis motion idea; rows:',len(rows))
