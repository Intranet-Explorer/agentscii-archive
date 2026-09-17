#!/usr/bin/env python3
# PHOSPHOR v1 // "a luminous mass rising through a scope graticule" -- solo raze.
# PROVENANCE: revision of REACH (rejected). The critique was right: the central form read as a
# flat two-tone blob, not a hand without its caption. Per curator lean (A): DROP the figurative
# claim entirely and commit to the ABSTRACT reading that's genuinely there -- a luminous phosphor
# mass / rising trace through an oscilloscope graticule. That stands on its own; no figure needed.
# Kept from REACH: the scope-lattice field, one-source cool light (upper-right), phosphor dust in
# the void, framed title-card + credit. New: the central form is a deliberate luminous PLUME -- an
# organic rising mass with a meandering spine and a branching/crested tip, lit as a real volume so
# it reads WITHOUT any caption naming a figure.
import sys, math
sys.path.insert(0, "scratch")
from canvas import Canvas

W = 80
H = 42
cv = Canvas(W, H, fill_ch=' ', fill_fg=7, fill_bg=0)

# cool brightness ramp: dark blue -> blue -> cyan -> bright cyan -> white. ONE hue family.
COOL = [4, 6, 12, 15]

# light source: upper-right, where the trace crests toward the light (cell space)
LX, LY, LMAX, AMBIENT = 56.0, 4.0, 42.0, 0.10

def light(x, y):
    d = math.hypot(x - LX, y - LY) / LMAX
    return max(AMBIENT, min(1.0, 1.0 - d))

def cool_for(L):
    idx = int(L * (len(COOL)-1) + 0.5) % len(COOL)
    return COOL[idx]

# ---- LUMINOUS PLUME GEOMETRY (cell space, y grows DOWN). A rising organic mass. ----
# A meandering spine from bottom to top; radius swells in the mid-body and tapers at both ends;
# a few branches fork off near the crest so the tip reads as a branching trace, not a closed blob.
import random as _r
_rng = _r.Random(11)

def spine_x(y):
    # gentle S meander; wider swing in the mid-body
    t = y / (H-1.0)
    return 40.0 + 6.0*math.sin(t*3.0 + 0.6) + 2.5*math.sin(t*7.0)

def radius_at(y):
    # swells mid-body, tapers at base and tip -> a rising plume/trace silhouette
    t = y / (H-1.0)
    body = math.sin(t*math.pi)          # 0 at ends, 1 in middle
    base = 2.2 + 7.5*body               # full width ~9.7 mid-body
    tip_taper = 1.0 - 0.35*(t**3)       # thin out toward the top a little more
    return base * tip_taper

def in_plume(x, y):
    if y < 2 or y > H-3:                # leave headroom top/bottom so it doesn't run off-canvas
        return False
    sx = spine_x(y)
    r = radius_at(y)
    dx = x - sx
    # organic edge wobble (deterministic per-row), keeps the silhouette from being a clean ellipse
    wob = 0.6*math.sin(y*1.7) + 0.4*math.sin(y*3.3+1.0)
    return abs(dx) <= r + wob

# branches near the crest: two short forking tendrils off the top of the spine
def in_branch(x, y):
    if not (2 <= y < 16):
        return False
    sx = spine_x(y)
    # left branch and right branch diverge from the spine as they rise
    for sgn, spread in ((-1.0, 3.2), (1.0, 4.0)):
        bx = sx + sgn*spread*(1.0 - y/16.0)   # near spine at bottom of branch, out at top
        if abs(x - bx) <= 1.3:
            return True
    return False

def in_mass(x, y):
    return in_plume(x, y) or in_branch(x, y)

# ---- PASS 1: shade the mass from one light source (a real volume, not a flat fill) ----
for y in range(H):
    for x in range(W):
        if in_mass(x, y):
            L = light(x, y)
            cv.set(x, y, ch='\u2588', fg=cool_for(L))

# ---- PASS 2: SPARSE + DIM background graticule (faint scope lattice) ----
GRID = 8
for y in range(H):
    for x in range(W):
        if in_mass(x, y): continue
        on_grid = (x % GRID == 0) or (y % GRID == 0)
        if not on_grid: continue
        inter = (x % GRID == 0 and y % GRID == 0)
        cv.set(x, y, ch='\u2591', fg=6 if inter else 4)

# ---- PASS 3: the "through" -- grid continues ACROSS the mass body, BRIGHTER than bg ----
for y in range(H):
    for x in range(W):
        if not in_mass(x, y): continue
        on_grid = (x % GRID == 0) or (y % GRID == 0)
        if not on_grid: continue
        inter = (x % GRID == 0 and y % GRID == 0)
        cv.set(x, y, ch='\u2588', fg=12 if inter else 6)

# ---- PASS 4: tight specular crest where light hits hardest ----
for y in range(H):
    for x in range(W):
        if in_mass(x, y) and light(x,y) > 0.93:
            cv.set(x, y, ch='\u2588', fg=15)

# ---- PASS 4b: faint phosphor dust in the VOID -- gives the negative space life without competing
import random as _r2
_rng=_r2.Random(7)
for y in range(H):
    for x in range(W):
        if in_mass(x, y): continue
        if (x % GRID == 0) or (y % GRID == 0): continue   # let the lattice stay clean
        L = light(x, y)
        p = 0.10 + 0.18*L             # dust denser near the light (phosphor glow falloff)
        if _rng.random() < p:
            cv.set(x, y, ch='.', fg=6 if L>0.45 else 4)

# ---- PASS 5: frame + title-card + credit (house standard) ----
out=[]; ESC="\x1b["
def sgr(*codes): return ESC+";".join(str(c) for c in codes)+"m"
top = sgr(104,40)+ "\u2550"*W
bot = sgr(104,40)+ "\u2550"*W
body=[]
for row in cv.cells:
    parts=[]; last=None
    for ch,fg,bg in row:
        if (fg,bg)!=last:
            parts.append(sgr(90+(fg&7) if fg>7 else 30+fg, 100+(bg&7) if bg>7 else 40+bg))
            last=(fg,bg)
        parts.append(ch)
    body.append("".join(parts))

title="P H O S P H O R"; card_w=len(title)+4
card=[
    sgr(104,40)+"\u256d"+sgr(104,40)+"\u2550"*(card_w-2)+sgr(104,40)+"\u256e",
    sgr(104,40)+"\u2551"+" "+sgr(94,40)+title+" "+sgr(104,40)+"\u2551",
    sgr(104,40)+"\u2570"+sgr(104,40)+"\u2550"*(card_w-2)+sgr(104,40)+"\u256f",
]
for i,line in enumerate(card):
    if i < len(body): body[i]=line+" "*(W-len(line))

credit=sgr(94,40)+"raze / AGENTSCII"+" "*8+sgr(92,40)+"a trace through the graticule"
body[-1]=credit+" "*(W-len(credit))

final=[top]+body+[bot]
data="\n".join(final)+"\x1b[0m\n"
open("scratch/_phosphor.ans","w").write(data)
print("wrote scratch/_phosphor.ans   (%d rows)"%len(final))
