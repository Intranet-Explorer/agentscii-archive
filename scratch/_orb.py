import sys, math, random; sys.path.insert(0,"scratch")
from halfblock import HalfBlockCanvas

# ORB v5 -- "THE WATCHER": a single CONSTRUCTED EYE at half-block resolution.
#
# v4 (rejected by blind second opinion) read as a flat disc/donut/target, not an eye:
#   (a) no almond/eyelid outline -> symmetric circle reads as a target;
#   (b) iris was four flat pie-wedges with stair-stepped seams, not radial fibers;
#   (c) the grey speckle field was too heavy and competed with the subject.
# v5 fixes all three, in order, on HalfBlockCanvas (2 px/cell via U+2580):
#   PASS 1 socket/crease shadow   -> depth behind the eye
#   PASS 2 almond opening mask     -> non-circular lens shape (the read as "eye")
#   PASS 3 sclera                 -> white->grey, lit upper-left, clipped to the almond
#   PASS 4 iris                   -> ONE amber family, RADIAL fibers from pupil + collarette/limbal rings
#   PASS 5 pupil + glint          -> black void + one white glint
#   PASS 6 upper/lower eyelids    -> lit brow arc + flatter lower lid, meeting at sharp canthi
#   PASS 7 sparse grey void       -> dialled DOWN so it doesn't fight the form
#   PASS 8 frame + sig block      -> house convention
W=80; H=52
cv=HalfBlockCanvas(W,H,bg=0)
ph=cv.ph                       # pixel-space height = 104 (square-ish with W=80)
cx=W//2; cy=ph//2             # eye center in pixel space

# --- almond geometry: opening is a LENS, not a circle. Narrower vertically than
#     horizontally, pinched at the canthi (corners). This is THE fix for "reads as
#     a disc": a symmetric circle is a target; an asymmetric lens with lids is an eye.
half_w = 42
h_upper = 21
h_lower = 14
exp_u, exp_l = 0.46, 0.38

def opening_half_h(u):
    """Vertical half-height of the eye opening at normalized x u in [-1,1]."""
    a=abs(u)
    if a>=1.0: return (0.0,0.0)
    up = h_upper*(1.0-u*u)**exp_u
    lo = h_lower*(1.0-u*u)**exp_l
    return up, lo

def in_opening(px,py):
    u=(px-cx)/half_w
    if abs(u)>=1.0: return False
    up,lo=opening_half_h(u)
    dy=py-cy
    return -up <= dy <= lo

sclera_r = 34                 # sclera fills the opening (used for iris/pupil radii ref)
iris_r    = 19
pupil_r   = 11
socket_r = half_w + 8         # socket/crease ring outside the opening

lx, ly = cx-26, cy-34         # single light source, upper-left
def L(px,py):
    d=math.hypot(px-lx, py-ly)
    return max(0.03, 1.0 - d/78.0)

# brightness ramp within ONE hue family: hot -> mid -> cold (same hue, brightness only)
def ramp(l, hot, mid, cold):
    if l>0.60: return hot
    if l>0.34: return mid
    return cold

# fine 4-stop amber family for the iris -- brown(3) is a dark amber, NOT a new hue.
def aramp(l):
    if l>0.62: return 11     # bright yellow (lit)
    if l>0.40: return 9      # bright red
    if l>0.22: return 1      # red
    return 3                 # brown / dark amber (shadow)

# --- PASS 1: socket wall + crease shadow -- grey family, lit upper-left, behind the eye
for py in range(ph):
    for px in range(W):
        u=(px-cx)/half_w
        if abs(u)<1.05:
            up,lo=opening_half_h(u)
            # a soft crease band just ABOVE the upper lid (the eyelid fold / socket shadow)
            dy=py-cy
            if -up-6 <= dy < -up+1:
                cv.set_pixel(px,py, ramp(L(px,py), 8, 0, 0))

# --- PASS 2/3: sclera -- white->grey lit eyeball, CLIPPED to the almond opening
for py in range(ph):
    for px in range(W):
        if in_opening(px,py):
            cv.set_pixel(px,py, ramp(L(px,py), 15, 7, 8))

# --- PASS 4: iris -- ONE amber family + RADIAL fibers running FROM the pupil.
#     The v4 defect was flat pie-wedges (stair-stepped seams). Here the striation
#     modulates by ANGLE (spokes radiating from center) with a slight twist, plus a
#     collarette ring near the pupil and a dark limbal ring at the iris edge -- all
#     within the amber/brown family, no cyan, no new hue.
for py in range(ph):
    for px in range(W):
        if not in_opening(px,py): continue
        dx=px-cx; dy=py-cy
        d=math.hypot(dx,dy); ang=math.atan2(dy,dx)
        if d < iris_r:
            t=(d-pupil_r)/(iris_r-pupil_r)          # 0 at pupil edge -> 1 at iris edge
            l=L(px,py)*(1.0-0.28*t)                 # cool slightly outward (falloff)
            col=aramp(l)
            # radial fibers: angle-dependent modulation => spokes from the center
            fiber=math.sin(ang*46.0 + t*3.5)
            if fiber>0.86:
                col = 1 if l>0.34 else 3            # darken within amber family (shadowed fiber)
            elif fiber<-0.92:
                col = 11                            # catch a lit fiber highlight
            cv.set_pixel(px,py,col)
        # collarette ring just outside the pupil -- subtle darker amber band
        if iris_r-3 <= d < iris_r-1:
            pass
    # limbal ring at the outer iris edge -- thin dark amber, separates iris from sclera
for py in range(ph):
    for px in range(W):
        if not in_opening(px,py): continue
        dx=px-cx; dy=py-cy; d=math.hypot(dx,dy)
        if iris_r-1 <= d < iris_r+0.5:
            cv.set_pixel(px,py, 3)                 # dark amber limbal ring

# --- PASS 5: pupil -- black void + one lit glint upper-left (single accent, not a hue fight)
cv.fill_circle(cx, cy, pupil_r, 0)
cv.fill_circle(cx-3.2, cy-3.4, 2.6, 15)

# --- PASS 6: eyelids -- THE almond read. A crisp DARK contour traces the opening
#     boundary (the eyelid edge) so the shape reads as an EYE, not a disc; above it a
#     lit brow band, below it a flatter lower lid, both pinching to sharp canthi at |u|=1.
for py in range(ph):
    for px in range(W):
        u=(px-cx)/half_w
        if abs(u)>=1.0: continue
        up,lo=opening_half_h(u)
        dy=py-cy
        # (a) crisp dark almond contour -- the eyelid edge, ~2px thick, black for max contrast
        if -up-1.5 <= dy < -up+0.5 or lo-0.5 <= dy < lo+1.5:
            cv.set_pixel(px,py, 0)
        # (b) lit upper brow band just above the contour, thick at center -> thin at canthi
        lid_thick = 3.0*(1.0-u*u)+0.8
        if -up-lid_thick-1.5 <= dy < -up-1.5:
            cv.set_pixel(px,py, ramp(L(px,py), 15, 7, 8))
        # (c) flatter lower lid just below the contour
        ll = 2.0*(1.0-u*u)+0.5
        if lo+1.5 <= dy < lo+1.5+ll:
            cv.set_pixel(px,py, ramp(L(px,py), 7, 8, 0))

# --- PASS 7: sparse grey void texture -- DIALLED DOWN (v4 was 0.10 and fought the form).
#     A faint depth field that reads as a textured void-face without competing with the eye.
random.seed(11)
for py in range(ph):
    for px in range(W):
        if cv.get_pixel(px,py)==0 and random.random()<0.035:
            cv.set_pixel(px,py, 8)

rows=cv.render()

# --- PASS 8: FRAME + SIG BLOCK (house convention; inspect_piece flags NO FRAME otherwise)
def c(fg,bg,ch):
    f=(90+(fg&7)) if fg>7 else (30+fg)
    b=(100+(bg&7)) if bg>7 else (40+bg)
    return f"\x1b[{f};{b}m"
frame=[]
for r in rows:
    frame.append(c(8,0,"║")+r+c(8,0,"║"))
title=" THE WATCHER // a constructed eye at half-block resolution "
title=title.ljust(W)[:W]
frame.insert(0, c(7,0,"")+"═"*W)
frame.insert(1, c(15,0,"")+title.center(W))
sig=" raze / AGENTSCI // THE WATCHER // 2026-09 "
sig=sig.ljust(W)[:W]
frame.append(c(15,0,"")+sig.center(W))
frame.append(c(7,0,"")+"═"*W)

out="\n".join(frame)+"\x1b[0m\n"
open("scratch/_orb.ans","w").write(out)
print("orb v5", len(frame),"rows")
