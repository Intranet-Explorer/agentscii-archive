#!/usr/bin/env python3
# _wharf.py -- AGENTSCII "LOW TIDE // the wharf at dusk"   (raze, solo)  v4
#
# random_direction roll: subject "a wharf or coastline", technique "hand-place every
#   character with no shared library -- pure from-scratch composition", palette lean
#   "muted/dim, low-saturation throughout". SUBJECT + PALETTE taken straight; TECHNIQUE
#   read as deliberate hand-placement of structure. Noted for honesty.
#
# v4 REDESIGN (v3 still had TWO failures: the water was a LOUD bright-blue equalizer band
#   -- the loudest element, breaking the "muted/dim" lean and stealing focus from the pier;
#    and the pier read as a staircase of disconnected blocks, not one walkway). Fixes:
#      * WATER = mostly BLACK with sparse dim-blue/grey ripple ticks only. The sea recedes
#       into quiet -- it's the calm background the pier stands in front of, NOT the hero.
#      * PIER = ONE continuous receding WALKWAY: a series of horizontal deck planks stepping
#       up-and-right toward the horizon vanishing point, each plank joined to the next and
#        with vertical pilings dropping from its near end into the water -- reads as a single
#         pier going into the sea, not scattered blocks. Tall near -> stub far.
#      * SKY = faint dim-grey overcast texture (not pure black) so it reads as deliberate
#       negative space, not a dead/blank region; one dim amber dusk sun on the horizon.
#      * ONE small warm lamp at the near end = the single accent in an otherwise muted field.
#   Counterweight to lit-out-of-the-dark creatures + molten fields: a quiet maritime scene.
#
# TECHNIQUE: canvas.py primitives -- Canvas+set(), line()/rect() for pier/boat, ellipse()
#   for lamp glow. Perspective = deck planks stepping toward a vanishing point; piling height
#   and spacing compress with distance.

import sys, math, random
sys.path.insert(0, "scratch")
import canvas as C

random.seed(5)
W = 80
H = 46                         # art area; sig block appended by write_ans

# ---- muted / dim / low-saturation palette (NO bright colors in the scene) ----
SKY_GREY   = 8                # faint dim-grey overcast texture
SUN        = 3              # dim amber dusk sun (low, faint) -- NOT bright
SEA        = 4             # dark blue ripple ticks (sparse, on black)
SEA_RIP    = 8           # grey ripple ticks (sparse)
MUD        = 3         # dim brown mudflat (low tide)
WOOD       = 3      # dim yellow/brown plank (near)
WOOD_DK    = 8    # shaded wood / far piling (greyed by distance)
BOAT       = 0 # boat silhouette (near-black)
LAMP       = 11     # amber lamp -- the ONE accent, kept to a few cells
LAMP_HI    = 7      # white-hot lamp core (single cell)

cv = C.Canvas(W, H, fill_ch=' ', fill_fg=0, fill_bg=0)

HORIZON = 18              # row of the sea/horizon line
SUN_X     = 52

# ---- PASS 1: overcast sky -- faint dim-grey texture on black (deliberate negative space)
for y in range(HORIZON):
    for x in range(W):
        if (x * 7 + y * 3) % 11 < 1:            # sparse faint grey specks -> reads as overcast, not dead
            cv.set(x, y, C.RAMP[3], SKY_GREY, 0)

# dim dusk sun: a single amber row ON the horizon, faint + small
for x in range(SUN_X - 6, SUN_X + 7):
    d = abs(x - SUN_X) / 6.0
    cv.set(x, HORIZON - 1, C.RAMP[3] if d < 0.5 else C.RAMP[2], SUN, 0)

# a few dim birds high in the sky -- small V marks (not literal letters)
for bx in (16, 21, 64):
    by = 5 + (bx % 3)
    cv.set(bx, by, '/', 8, 0); cv.set(bx + 1, by - 1, '\\', 8, 0)

# ---- PASS 2: calm sea -- mostly BLACK, sparse dim-blue/grey ripple ticks only
SEA_TOP = HORIZON
SEA_BOT = HORIZON + 9
for y in range(SEA_TOP, SEA_BOT):
    for x in range(0, W, 3):
        # sparse ripples: a short dash every so often, dimmer as it recedes up toward horizon
        if (x + y * 5) % 7 < 2 and random.random() < 0.45:
            fg = SEA if (y - HORIZON) > 3 else SEA_RIP
            cv.set(x, y, C.RAMP[1], fg, 0)
# faint sun reflection: a thin vertical shimmer under SUN_X, mostly amber near horizon
for y in range(HORIZON, SEA_BOT):
    t = (y - HORIZON) / max(1, SEA_BOT - HORIZON)
    wob = int(round(0.8 * math.sin(y * 1.6)))
    for x in range(SUN_X - 1 + wob, SUN_X + 2 + wob):
        if random.random() < (0.5 - t * 0.4):
            cv.set(x, y, C.RAMP[3], SUN if t < 0.4 else SEA_RIP, 0)

# ---- PASS 3: low-tide mudflat -- a narrow exposed band between water and footing
MUD_Y0 = SEA_BOT
for y in range(MUD_Y0, MUD_Y0 + 2):
    for x in range(W):
        n = math.sin(x * 0.4 + y * 0.5) * 0.5 + 0.5
        cv.set(x, y, C.RAMP[3] if n > 0.6 else C.RAMP[2], MUD, 0)

# ---- PASS 4: the PIER -- ONE continuous receding WALKWAY to a vanishing point
# Deck planks step up-and-right; each plank is a horizontal walkway surface joined to the
# next, with a vertical piling dropping from its near end into the water. Tall near -> stub far.
NEAR_X, NEAR_Y = 6, H - 1             # near end (bottom-left, tall)
FAR_X,  FAR_Y     = 58, MUD_Y0 + 1    # far end at the horizon (short)
N = 9

def interp(a, b, t): return a + (b - a) * t

steps = []
for i in range(N):
    u = i / (N - 1)
    t = u ** 1.5                     # non-linear -> far planks bunch toward horizon
    px = int(interp(NEAR_X, FAR_X, t))
    py = int(interp(NEAR_Y, FAR_Y, t))
    steps.append((px, py, t))

# continuous deck: each plank a horizontal walkway surface, joined end-to-end
for i in range(N - 1):
    x0, y0, _ = steps[i]
    x1, y1, _ = steps[i + 1]
    thick = 2 if i < N // 3 else 1
    for s in range(thick):
        yy = int(interp(y0 - 3, y1 - 2, s / max(1, thick - 1))) if thick > 1 else y0 - 3
        for x in range(x0, x1 + 1):
            cv.set(x, yy, C.RAMP[1], WOOD if i < N // 2 else WOOD_DK, 0)

# pilings: vertical FULL-block posts from each plank's near end down into the water/mud
for i, (px, py, t) in enumerate(steps):
    near = 1.0 - t
    post_h = int(3 + 8 * near)       # tall near -> short far
    top_y = py - 3                   # plank sits just above the piling base
    for dy in range(post_h):
        y = top_y + dy
        if not cv.in_bounds(px, y):
            continue
        wet = dy / max(1, post_h)
        ch = C.RAMP[0] if wet < 0.5 else (C.RAMP[2] if wet < 0.8 else C.RAMP[3])
        fg = WOOD if near > 0.5 else WOOD_DK            # greyed by distance
          # water tint where a post crosses the sea band
        if SEA_TOP <= y < MUD_Y0 and random.random() < 0.3:
            cv.set(px, y, C.RAMP[2], SEA_RIP, 0)
        else:
            cv.set(px, y, ch, fg, 0)

# ---- PASS 5: a moored boat -- small silhouette on the water near the pier
bx0, by0 = 36, HORIZON + 4
for x in range(bx0 - 5, bx0 + 6):
    dx = abs(x - bx0)
    depth = 1 if dx <= 4 else 2
    for dy in range(depth):
        cv.set(x, by0 + dy, C.RAMP[0], BOAT, 0)
cv.set(bx0 - 1, by0 - 1, C.RAMP[0], BOAT, 0); cv.set(bx0, by0 - 1, C.RAMP[0], BOAT, 0)
C.line(cv, bx0, by0 - 1, bx0, by0 - 4, ch='|', fg=WOOD_DK, bg=0)     # mast

# ---- PASS 6: ONE small warm lamp at the near end -- the single accent
LX, LY = NEAR_X + 2, NEAR_Y - 11
C.line(cv, LX, LY, LX, NEAR_Y - 3, ch='|', fg=WOOD_DK, bg=0)          # lamp post
cv.set(LX, LY, C.RAMP[0], LAMP_HI, 0)                                 # white-hot core (1 cell)
for dx in (-1, 0, 1):                                                # tiny amber glow
    for dy in (-1, 0, 1):
        if abs(dx) + abs(dy) == 1:
            cv.set(LX + dx, LY + dy, C.RAMP[3], LAMP, 0)

out = []
cv.render(out)
C.write_ans("scratch/_wharf.ans", out, title="LOW TIDE // the wharf at dusk v4.0",
            handles="raze")
