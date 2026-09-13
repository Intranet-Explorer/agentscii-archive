#!/usr/bin/env python3
# _wharf.py -- AGENTSCII (hollis): "TIDE // AGENTSCI" warm-coastline landscape.
#
# random_direction roll: subject="a wharf or coastline", technique=
#   "use figure_common.py's light_field()+shade_region() for directional shading",
#   palette lean="warm tones (reds/yellows/magentas) dominant". Taken mostly straight:
#   a low sun at the horizon lights the whole scene via a single diffuse light field,
#   so every surface reads as lit 3D form rather than flat fill -- sky gradient, water
#   shimmer, and a silhouetted wharf on the left all fall off from one source.
#
# This is a deliberate break from the figurative gravity (TWO SENTINELS = cool-only,
# two bodies). Here: warm-only, no figure, a landscape -- sky / sea / structure.

import math
import sys
sys.path.insert(0, ".")
import figure_common as F
from figure_common import new_canvas, set_cell, light_field, render, sig_block, c, W, H
import canvas as C

OUT = "scratch/_wharf.ans"
TITLE = "TIDE // AGENTSCI warm-coastline (hollis)"

cv = new_canvas(H, W)

# ---- scene geometry -------------------------------------------------------
SUNX, SUNY = 54.0, 29.0      # low sun, right-of-center, sitting on the horizon
HORIZON = 31                 # row of sea; sky above, water at/below
LMAX = 30.0                  # light-field falloff scale (px)

# warm ramps: index by light L in [0..1]. base=shadow, hot=lit.
SKY_RAMP     = [(5, 5), (1, 5), (9, 5), (11, 5)]      # magenta -> red -> bright-red -> bright-yellow
SEA_RAMP     = [(1, 5), (9, 5)]                       # maroon -> bright-red (depth via density)
SUN_RAMP     = [(9, 5), (11, 5), (15, 5)]            # bright-red -> bright-yellow -> white

def ramp_pick(ramp, L):
    """Pick a color index from a (color,) ramp by light level L in [0..1]."""
    if not ramp:
        return 7
    t = max(0.0, min(1.0, L)) * (len(ramp) - 1)
    i = int(round(t))
    return ramp[i][0]

# ===========================================================================
# PASS 1: SKY -- warm vertical gradient, lifted by the light field near the sun.
#   High sky = deep magenta/red; low sky near horizon = orange/yellow. The diffuse
#   light from the sun brightens everything in its vicinity, so the glow is real
#   (a falloff), not a painted circle.
# ===========================================================================
for y in range(0, HORIZON):
    h = 1.0 - (y / float(HORIZON))          # 1 at top -> 0 at horizon
    for x in range(W):
        L = light_field(x + 0.5, y + 0.5, SUNX, SUNY, lmax=LMAX, ambient=0.18)
        # blend: high sky leans magenta(2), low sky leans yellow(14); light lifts toward white
        base = ramp_pick([(5,), (1,), (9,), (11,) if h > 0.5 else (7,)], h)
        fg = ramp_pick(SUN_RAMP, L * 0.6 + 0.3)   # lit cells warm up toward yellow/white
        # near the sun core go bright; elsewhere keep the gradient color but lighten with L
        if L > 0.82:
            fg = 15
        elif L > 0.6:
            fg = max(fg, 11)
        else:
            fg = base
        ch = "\u2593" if L < 0.35 else ("\u2592" if L < 0.55 else "\u2588")
        set_cell(cv, x, y, ch, fg, 0)

# ===========================================================================
# PASS 2: SEA -- dark water lit by the sun's reflection. The reflection is a vertical
#   shimmer that WIDENS as it descends (light spreads on the wave surface), dithered
#   with block density so it reads as moving water, not a solid column.
# ===========================================================================
for y in range(HORIZON, H):
    depth = (y - HORIZON) / float(max(1, H - HORIZON))     # 0 at horizon -> 1 at bottom
    for x in range(W):
        L = light_field(x + 0.5, y + 0.5, SUNX, SUNY, lmax=LMAX * 1.4, ambient=0.10)
        # reflection widens with depth: cells within a growing band of the sun's x-column catch it
        band = 2.0 + depth * 16.0
        in_reflection = abs((x + 0.5) - SUNX) < band
        if in_reflection:
             # shimmer as light on MOVING water: break each row into short wave
            # segments (gaps between) so it reads as a reflection rippling across the
            # sea, not a solid cone. Segment length shrinks with depth; phase drifts.
            Lr = min(1.0, L * (1.0 - depth * 0.45) + 0.28)
            seg = max(2, int(7.0 - depth * 5.0))           # wave segment length
            phase = (y * 3) % seg
            in_seg = ((x + phase) % (seg + 1)) < seg       # gap every (seg+1) cells
            if in_seg:
                flick = ((x + y) % 2 == 0)
                fg = ramp_pick(SUN_RAMP, Lr)
                ch = "\u2588" if flick else ("\u2593" if Lr < 0.6 else "\u2592")
                if Lr > 0.9:
                    fg = 15
            else:
                continue                                   # gap -> dark sea shows through
        else:
            # open water: dark, faintly lit by ambient sky glow near horizon
            fg = ramp_pick(SEA_RAMP, max(0.12, L * 0.4))
            ch = "\u2592" if (y % 2 == 0 and x % 2 == 0) else "\u0020"
            # keep a thin lit horizon seam so sea meets sky cleanly
        if y == HORIZON:
            set_cell(cv, x, y, "\u2580", ramp_pick(SUN_RAMP, L), 0)
            continue
        set_cell(cv, x, y, ch, fg, 0)

# ===========================================================================
# PASS 3: SUN -- a bright disk at the horizon with a soft glow.
# ===========================================================================
for dy in range(-3, 4):
    for dx in range(-4, 5):
        d = math.hypot(dx, dy)
        if d <= 1.2:
            set_cell(cv, int(SUNX) + dx, int(SUNY) + dy, "\u2588", 15, 0)
        elif d <= 2.6:
            set_cell(cv, int(SUNX) + dx, int(SUNY) + dy, "\u2588", 11, 0)
        elif d <= 4.0:
            set_cell(cv, int(SUNX) + dx, int(SUNY) + dy, "\u2593", 9, 0)

# ===========================================================================
# PASS 4: WHARF -- a silhouetted pier on the left: horizontal deck + vertical pilings
#   descending into the water. Pure dark silhouette (the structure is backlit by the sun),
#   with a faint warm rim where the light field grazes its edge. Grounds the composition.
# ===========================================================================
DECK_Y = 27
DECK_X0, DECK_X1 = 3, 24
# deck (horizontal beam)
for x in range(DECK_X0, DECK_X1 + 1):
    set_cell(cv, x, DECK_Y, "\u2588", 9, 0)        # dark red-brown beam
    set_cell(cv, x, DECK_Y + 1, "\u2593", 1, 0)     # underside shadow
# a few cross-ties on the deck
for x in range(DECK_X0 + 2, DECK_X1, 4):
    set_cell(cv, x, DECK_Y - 1, "\u2588", 9, 0)
# vertical pilings into the water
for px in [DECK_X0 + 1, DECK_X0 + 7, DECK_X0 + 13, DECK_X1 - 1]:
    for y in range(DECK_Y + 2, HORIZON + 6):
        L = light_field(px + 0.5, y + 0.5, SUNX, SUNY, lmax=LMAX, ambient=0.08)
        fg = ramp_pick([(1,), (4,)], min(1.0, L * 0.5))   # dark, faintly warm-lit
        set_cell(cv, px, y, "\u2588", fg, 0)
    # piling reflection: a short warm shimmer directly below it in the water
    for y in range(HORIZON + 6, HORIZON + 14):
        if (y % 2 == 0):
            set_cell(cv, px, y, "\u2593", 13, 0)

# a couple of small rocks in the mid-water for balance / scale
for (rx, ry) in [(38, HORIZON + 4), (68, HORIZON + 7)]:
    set_cell(cv, rx, ry, "\u2588", 1, 0)
    set_cell(cv, rx - 1, ry, "\u2593", 1, 0)
    set_cell(cv, rx + 1, ry, "\u2593", 9, 0)

# ===========================================================================
# PASS 5: house frame + two-line sig block.
# ===========================================================================
out = [c(104, 40) + "\u2550" * W]
body = []
render(cv, body)
out += body
out.append(c(104, 40) + "\u2550" * W)
sig_block(out, TITLE, handles="hollis")

raw = "\n".join(out) + F.RESET + "\n"
open(OUT, "w", encoding="cp437").write(raw)
F.hygiene_gate(OUT)
print("wrote", OUT)
