import sys, math, random; sys.path.insert(0,"scratch")
from halfblock import HalfBlockCanvas

# ORB v4 -- "THE WATCHER": a single CONSTRUCTED EYE at half-block resolution.
# v3 read as an abstract multi-color target (yellow/green/brown iris sectors fighting
# white sclera + blue pupil). v4 enforces the discipline the script CLAIMS: ONE hue
# family per region, light carried by BRIGHTNESS within that family, lit from one
# upper-left source. Adds the two passes inspect_piece flags: a FRAME and a SIG BLOCK.
W=80; H=52
cv=HalfBlockCanvas(W,H,bg=0)
ph=cv.ph
cx=W//2; cy=ph//2

sclera_r = 34
iris_r   = 20
pupil_r  = 11
socket_r = sclera_r + 6

lx, ly = cx-24, cy-30            # single light source, upper-left
def L(px,py):
    d=math.hypot(px-lx, py-ly)
    return max(0.03, 1.0 - d/70.0)

# brightness ramp within ONE hue family: hot -> mid -> cold (same hue, brightness only)
def ramp(l, hot, mid, cold):
    if l>0.60: return hot
    if l>0.34: return mid
    return cold

# fine 4-stop amber family for the iris shadow side -- brown(3) is a dark amber, not a new hue
def aramp(l):
    if l>0.62: return 11    # bright yellow (lit)
    if l>0.40: return 9     # bright red
    if l>0.22: return 1     # red
    return 3                # brown / dark amber (shadow)

# --- PASS 1: socket wall -- dark grey ring, eye set into a void-face (grey family)
for py in range(ph):
    for px in range(W):
        d=math.hypot(px-cx,py-cy)
        if socket_r-2 <= d <= socket_r+3:
            cv.set_pixel(px,py, ramp(L(px,py), 7, 8, 0))

# --- PASS 2: sclera -- light eyeball, white->grey (white family), lit upper-left
for py in range(ph):
    for px in range(W):
        if math.hypot(px-cx,py-cy)<=sclera_r:
            cv.set_pixel(px,py, ramp(L(px,py), 15, 7, 8))

# --- PASS 3: iris -- ONE amber family (bright yellow -> bright red -> dark red) + striations
for py in range(ph):
    for px in range(W):
        d=math.hypot(px-cx,py-cy)
        if iris_r-1 <= d <= sclera_r-1:
            l=L(px,py)*(1.0-0.32*((d-(iris_r-1))/(sclera_r-iris_r)))   # cool slightly outward
            cv.set_pixel(px,py, aramp(l))            # bright yellow -> bright red -> red -> brown (fine amber falloff, NO cyan)
        if iris_r <= d <= sclera_r-2:
            ang=math.atan2(py-cy,px-cx)
            if math.sin(ang*70.0) > 0.94:
                cv.set_pixel(px,py, 1)                     # red striation, same amber family

# --- PASS 4: pupil -- deep blue-black void + lit glint upper-left (one accent, not a hue fight)
for py in range(ph):
    for px in range(W):
        if math.hypot(px-cx,py-cy)<=pupil_r:
            cv.set_pixel(px,py,0)                             # deep black void pupil -- contrasts the amber iris
cv.fill_circle(cx-3.5, cy-3.5, 2.8, 15)

# --- PASS 5: orbital ridge / brow -- lit arc hugging socket top (white family, connected)
for py in range(ph):
    for px in range(W):
        dx=px-cx
        if abs(dx)<socket_r+1:
            arc_y = cy - math.sqrt(max(0,(socket_r+2)**2 - dx*dx))
            if abs(py-arc_y)<2.5:
                cv.set_pixel(px,py, ramp(L(px,py), 15, 7, 8))

# --- PASS 6: void texture -- sparse grey depth (NOT bright noise), denser than v3 so the
#     negative space reads as a textured void-face, not flat black. Methodology Pass 5.
random.seed(11)
for py in range(ph):
    for px in range(W):
        if cv.get_pixel(px,py)==0 and random.random()<0.10:
            cv.set_pixel(px,py, 8)

rows=cv.render()

# --- PASS 7: FRAME + SIG BLOCK (Methodology Pass 6 -- inspect_piece flags NO FRAME)
def c(fg,bg,ch):
    f=(90+(fg&7)) if fg>7 else (30+fg)
    b=(100+(bg&7)) if bg>7 else (40+bg)
    return f"\x1b[{f};{b}m"
frame=[]
top = c(7,0,"") + "═"*W
bot = c(7,0,"") + "═"*W
for r in rows:
    # left/right border columns over the pixel rows
    frame.append(c(8,0,"║")+r+c(8,0,"║"))
# title card top band
title=" THE WATCHER // a constructed eye at half-block resolution "
title=title.ljust(W)[:W]
frame.insert(0, c(7,0,"")+"═"*W)
frame.insert(1, c(15,0,"")+title.center(W))
# sig block bottom band (house convention: handle + tag + title + date)
sig=" raze / AGENTSCI // THE WATCHER // 2026-09 "
sig=sig.ljust(W)[:W]
frame.append(c(15,0,"")+sig.center(W))
frame.append(c(7,0,"")+"═"*W)

out="\n".join(frame)+"\x1b[0m\n"
open("scratch/_orb.ans","w").write(out)
print("orb v4", len(frame),"rows")
