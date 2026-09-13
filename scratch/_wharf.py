#!/usr/bin/env python3
# _wharf.py -- AGENTSCII "LOW TIDE // the wharf at dusk"   (raze, solo)  v5
#
# random_direction roll: subject "a wharf or coastline", technique "hand-place every
#   character with no shared library -- pure from-scratch composition", palette lean
#   "muted/dim, low-saturation throughout". SUBJECT + PALETTE taken straight; TECHNIQUE
#   read as deliberate hand-placement of structure. Noted for honesty.
#
# v5 REDESIGN (v4 still had TWO failures: a bright yellow "sun" block upper-right that
#    competed with the lamp and broke the muted lean; and the pier read as disconnected
#    staircase blocks, not one walkway -- 3D perspective-in-2D kept fighting me). Fixes:
#      * DROP the sun entirely. Dusk = a dim overcast sky + calm dark water; no bright source.
#      * PIER = FLAT ICONIC SIDE-VIEW: ONE continuous horizontal deck (a long walkway band)
#       with evenly-spaced vertical PILINGS dropping from it into the water below -- reads
#        instantly as a wharf/pier, unambiguous, no staircase ambiguity. A gentle perspective
#         hint: pilings on the far (right) end are shorter + slightly closer-spaced.
#      * WATER = mostly black with sparse dim-blue/grey ripples; calm, recedes into quiet.
#      * ONE small warm lamp at the near (left) end of the deck = the single accent.
#   Counterweight to lit-out-of-the-dark creatures + molten fields: a quiet maritime scene.
#
# TECHNIQUE: canvas.py primitives -- Canvas+set(), line()/rect() for deck/pilings/boat,
#   ellipse() for lamp glow. Structure hand-placed by math (even piling spacing, perspective
#   compression on the far end), not a noise field.

import sys, math, random
sys.path.insert(0, "scratch")
import canvas as C

random.seed(9)
W = 80
H = 46                          # art area; sig block appended by write_ans

# ---- muted / dim / low-saturation palette (NO bright colors in the scene) ----
SKY_GREY    = 8                 # faint dim-grey overcast texture
SEA         = 4               # dark blue ripple ticks (sparse, on black)
SEA_RIP     = 8             # grey ripple ticks (sparse)
MUD         = 3           # dim brown mudflat (low tide, far shore)
WOOD        = 3        # dim yellow/brown plank (near deck)
WOOD_DK     = 8      # shaded wood / far piling (greyed by distance)
BOAT        = 0 # boat silhouette (near-black)
LAMP        = 11      # amber lamp -- the ONE accent, kept to a few cells
LAMP_HI     = 7       # white-hot lamp core (single cell)

cv = C.Canvas(W, H, fill_ch=' ', fill_fg=0, fill_bg=0)

HORIZON = 20               # row of the sea/horizon line (high -> water fills most of frame)
DECK_Y   = 26             # the wharf deck sits on the water, below the horizon

# ---- PASS 1: overcast sky -- faint dim-grey texture on black (deliberate negative space)
for y in range(HORIZON):
    for x in range(W):
        if (x * 7 + y * 3) % 13 < 1:              # sparse faint grey specks -> overcast, not dead
            cv.set(x, y, C.RAMP[3], SKY_GREY, 0)

# a few dim birds high in the sky -- small V marks (not literal letters)
for bx in (18, 24, 60):
    by = 5 + (bx % 3)
    cv.set(bx, by, '/', 8, 0); cv.set(bx + 1, by - 1, '\\', 8, 0)

# ---- PASS 2: calm sea -- mostly BLACK, sparse dim-blue/grey ripple ticks only
SEA_TOP = HORIZON
SEA_BOT = H - 1
for y in range(SEA_TOP, SEA_BOT):
    for x in range(0, W, 3):
         # sparse ripples; a touch denser lower (nearer), dimmer up toward the horizon
        if (x + y * 5) % 7 < 2 and random.random() < 0.4:
            fg = SEA if y > HORIZON + 6 else SEA_RIP
            cv.set(x, y, C.RAMP[1], fg, 0)

# ---- PASS 3: low-tide mudflat -- a narrow exposed band just below the horizon (far shore)
MUD_Y0 = HORIZON
for y in range(MUD_Y0, MUD_Y0 + 2):
    for x in range(W):
        n = math.sin(x * 0.4 + y * 0.5) * 0.5 + 0.5
        cv.set(x, y, C.RAMP[3] if n > 0.6 else C.RAMP[2], MUD, 0)

# ---- PASS 4: the WHARF -- ONE continuous horizontal deck + evenly-spaced vertical pilings
DECK_X0, DECK_X1 = 6, 73          # the walkway runs most of the width (a long pier)
DECK_THICK = 2                    # 2-row deck band (the walkway surface)
# continuous deck: a horizontal band of planks
for y in range(DECK_Y, DECK_Y + DECK_THICK):
    for x in range(DECK_X0, DECK_X1 + 1):
        cv.set(x, y, C.RAMP[1], WOOD if x < (DECK_X0 + DECK_X1) / 2 else WOOD_DK, 0)

# pilings: evenly-spaced vertical posts dropping from the deck into the water;
# far (right) end shorter + closer-spaced -> gentle perspective compression.
N = 11
for i in range(N):
    t = i / (N - 1)
    px = int(DECK_X0 + t * (DECK_X1 - DECK_X0))
    far = t                       # 0 near(left) -> 1 far(right)
    post_h = int(7 - 3 * far)     # tall near -> short far
    for dy in range(post_h):
        y = DECK_Y + DECK_THICK + dy
        if not cv.in_bounds(px, y):
            continue
        wet = dy / max(1, post_h)
        ch = C.RAMP[0] if wet < 0.5 else (C.RAMP[2] if wet < 0.8 else C.RAMP[3])
        fg = WOOD if far < 0.5 else WOOD_DK            # greyed by distance
           # water tint where a post crosses the open sea band
        if y > MUD_Y0 + 1 and random.random() < 0.3:
            cv.set(px, y, C.RAMP[2], SEA_RIP, 0)
        else:
            cv.set(px, y, ch, fg, 0)

# ---- PASS 5: a moored boat -- small silhouette tied to the deck's near end
bx0, by0 = DECK_X0 + 14, DECK_Y + DECK_THICK + 3
for x in range(bx0 - 5, bx0 + 6):
    dx = abs(x - bx0)
    depth = 1 if dx <= 4 else 2
    for dy in range(depth):
        cv.set(x, by0 + dy, C.RAMP[0], BOAT, 0)
cv.set(bx0 - 1, by0 - 1, C.RAMP[0], BOAT, 0); cv.set(bx0, by0 - 1, C.RAMP[0], BOAT, 0)
C.line(cv, bx0, by0 - 1, bx0, by0 - 4, ch='|', fg=WOOD_DK, bg=0)      # mast

# ---- PASS 6: ONE small warm lamp at the near (left) end of the deck -- the single accent
LX, LY = DECK_X0 + 1, DECK_Y - 5
C.line(cv, LX, LY, LX, DECK_Y, ch='|', fg=WOOD_DK, bg=0)              # lamp post on the deck
cv.set(LX, LY, C.RAMP[0], LAMP_HI, 0)                                 # white-hot core (1 cell)
for dx in (-1, 0, 1):                                                # tiny amber glow
    for dy in (-1, 0, 1):
        if abs(dx) + abs(dy) == 1:
            cv.set(LX + dx, LY + dy, C.RAMP[3], LAMP, 0)

out = []
cv.render(out)
C.write_ans("scratch/_wharf.ans", out, title="LOW TIDE // the wharf at dusk v5.0",
            handles="raze")
