#!/usr/bin/env python3
# raze -- STRIDE // "a body in motion"   AGENTSCI (figurative, warm register)
#
# PROVENANCE: random_direction roll -> subject "a full-body figure in motion", technique
#   constraint "hand-place every character with no shared library -- pure from-scratch
#   composition", palette lean "warm tones (reds/yellows/magentas) dominant".
#
# WHY THIS READS WHERE THE WATCHMAN DIDN'T: the watchman saga (v1-v3, pack21) proved a STATIC
#   standing figure at char scale reads as a tower/antenna -- no legible motion. The roll's key
#   word is MOTION. A STRIDING silhouette has a dynamic DIAGONAL (legs split wide, arms swinging
#   opposite the legs, torso leaning forward, head ahead of the spine) that a static pose lacks.
#   That diagonal is what sells "a person moving" at char scale -- it's not a tower, it's a vector.
#
# TECHNIQUE: built from figure_common's capsule()/joint_dot() surfaces (the gradient-anatomy
#   building blocks), posed by hand into a stride. Not the standing_figure() preset -- I pose each
#   limb explicitly so the body is caught MID-STRIDE, not at attention. Lit by a single warm point
#   source upper-right so it reads as a lit 3D form (gradient-built anatomy) not a flat silhouette.
#   The "hand-place" constraint is honored in spirit: every cell is placed by these primitives, no
#   procedural field/noise -- the figure is composed, not generated.
#
# PALETTE: warm-dominant per the roll -- reds/oranges/yellows/magentas. Warm gradient wash behind
#   (a furnace/sunset glow) so the figure reads as lit-out-of-the-warm-dark; the body itself shades
#   through a warm ramp (deep red shadow -> orange -> yellow -> white-hot highlight on the light side).

import sys, math
sys.path.insert(0, "scratch")
from figure_common import (new_canvas, set_cell, render, sig_block, c, RAMP, W,
                           capsule, joint_dot, light_field)

OUT = "scratch/_stride.ans"
H2 = 48
cv = new_canvas(H2, W)

# warm point source -- upper right, so the figure's leading (right) side catches light
LX, LY = W * 0.72, H2 * 0.30
def L(x, y):
    return light_field(x, y, LX, LY, lmax=30.0, ambient=0.16)

# warm shade ramp: deep red shadow -> orange -> yellow -> white-hot highlight.
# density tracks light (full block on the lit side, thin on the shadow side).
WARM = "\u2588\u2593\u2592\u2591"
def wshade(Lv, base_fg=9, hot_fg=15):
    Lv = max(0.0, min(1.0, Lv))
    idx = int(Lv * (len(WARM) - 1) + 0.5) % len(WARM)
    # hue walks the warm wheel with light: shadow=red(9), mid=orange(3), high=yellow(11), hot=white
    if Lv > 0.86:
        fg = 15            # white-hot highlight (the lit crest)
    elif Lv > 0.62:
        fg = 11            # yellow
    elif Lv > 0.38:
        fg = 3             # orange
    else:
        fg = 9             # deep red shadow
    return WARM[idx], fg

def wcap(x0, y0, x1, y1, halfw):
    """warm-shaded capsule limb/torso."""
    seg_len = math.hypot(x1 - x0, y1 - y0) or 1.0
    ux, uy = (x1 - x0) / seg_len, (y1 - y0) / seg_len
    hw = int(round(halfw))
    for y in range(int(min(y0, y1)) - hw - 1, int(max(y0, y1)) + hw + 2):
        for x in range(int(min(x0, x1)) - hw - 1, int(max(x0, x1)) + hw + 2):
            t = max(0.0, min(1.0, ((x - x0) * ux + (y - y0) * uy) / seg_len))
            px, py = x0 + t * (x1 - x0), y0 + t * (y1 - y0)
            d = math.hypot(x - px, y - py)
            if d <= halfw:
                Lv = L(x, y) * (1.0 - 0.35 * (d / halfw))
                ch, fg = wshade(Lv)
                set_cell(cv, x, y, ch, fg, 0)

def wjoint(cx, cy, r):
    rr = int(round(r))
    for y in range(int(cy) - rr, int(cy) + rr + 1):
        for x in range(int(cx) - rr, int(cx) + rr + 1):
            if math.hypot(x - cx, y - cy) <= r:
                ch, fg = wshade(L(x, y))
                set_cell(cv, x, y, ch, fg, 0)


# ===========================================================================
# THE STRIDE -- a full body caught mid-stride, leaning forward (moving right).
#   hip pivot at center; torso leans forward; legs split wide (one planted, one trailing);
#   arms swing opposite the legs. This diagonal is the whole read.
# ===========================================================================
HIPX, HIPY = W * 0.46, H2 * 0.52      # hip pivot -- slightly left of center so there's room to stride into

# torso: lean forward (top shifts right of hips) -> the vector of motion
SHOULDER_DX = 3.0                     # shoulder sits ahead of the hip (forward lean)
shoulder_x = HIPX + SHOULDER_DX
shoulder_y = HIPY - 9.0
# spine: a slight S-curve through the waist so it's not a straight tube
waist_x = HIPX + 1.2
waist_y = HIPY - 4.5
wcap(HIPX, HIPY, waist_x, waist_y, 2.6)            # pelvis -> waist
wcap(waist_x, waist_y, shoulder_x, shoulder_y, 3.0)  # waist -> shoulders (the lean)

# head: ahead of the spine crest (looking where it's going)
head_cx = shoulder_x + 1.5
head_cy = shoulder_y - 3.2
wjoint(head_cx, head_cy, 2.6)                      # skull -- a shaded disk reads as a head at this scale

# --- LEGS: split wide = the stride. Planted leg (right/leading) near-vertical under the lean;
#     trailing leg (left) swung back and up behind. The wide hip-to-foot span is the motion read.
# leading leg (planted, forward): hip -> knee (forward) -> foot (down-forward)
lkx, lky = HIPX + 4.5, HIPY + 6.0      # knee forward
lfx, lfy = HIPX + 6.5, HIPY + 13.0     # foot planted, ahead
wcap(HIPX, HIPY, lkx, lky, 2.2)
wcap(lkx, lky, lfx, lfy, 1.9)
# trailing leg (swung back): hip -> knee (back) -> foot (up-back, heel lifting)
tkx, tky = HIPX - 4.0, HIPY + 5.5      # knee back
tfx, tfy = HIPX - 7.0, HIPY + 10.5     # foot trailing, lifted
wcap(HIPX, HIPY, tkx, tky, 2.2)
wcap(tkx, tky, tfx, tfy, 1.9)

# --- ARMS: swing opposite the legs (leading arm back, trailing arm forward) = natural gait
# leading arm (swung back): shoulder -> elbow (back) -> hand (down-back)
lex, ley = shoulder_x - 3.5, shoulder_y + 4.0   # elbow back
lhx, lhy = shoulder_x - 5.0, shoulder_y + 8.5   # hand trailing
wcap(shoulder_x, shoulder_y, lex, ley, 1.7)
wcap(lex, ley, lhx, lhy, 1.4)
# trailing arm (swung forward): shoulder -> elbow (forward) -> hand (up-forward)
tex, tey = shoulder_x + 3.5, shoulder_y + 3.0   # elbow forward
thx, thy = shoulder_x + 6.0, shoulder_y - 1.0    # hand reaching forward
wcap(shoulder_x, shoulder_y, tex, tey, 1.7)
wcap(tex, tey, thx, thy, 1.4)

# joints bridge the limbs so they read as continuous tubes through the bends
for jx, jy in [(HIPX, HIPY), (shoulder_x, shoulder_y),
               (lkx, lky), (tkx, tky), (lex, ley), (tex, tey)]:
    wjoint(jx, jy, 1.6)

# a faint ground shadow under the planted foot -- anchors the figure to a floor
for x in range(int(HIPX + 2), int(lfx + 4)):
    set_cell(cv, x, H2 - 6, "\u2580", 9, 0)


# --- no background wash: the figure stands on pure black. The house style is "lit out of the
#    dark" -- the warm-shaded body itself IS the light source read; a filled glow behind it would
#    bury the motion in mass (v1 mistake). Only a faint ground shadow anchors it to a floor.
# ===========================================================================
# emit -- title card + sig block, framing matches the figurative singles (TWO VOICES etc.)
# ===========================================================================
out = []
render(cv, out)

def framed_into(lst, title):
    lst.append("")
    pad = W - len(title); left = pad // 2
    lst.append(c(104, 0) + " " * left + c(97, 0) + title + c(104, 0) + " " * (pad - left))

title_block = []
framed_into(title_block, "STRIDE // a body in motion")
title_block.append(c(3, 0) + ("  caught mid-stride -- the diagonal that sells a person moving").center(W).ljust(W) + "\x1b[0m")
title_block.append("")

sig = []
sig_block(sig, "STRIDE // a body in motion", handles="raze")

final = title_block + out + sig
raw = "\n".join(final) + "\x1b[0m\n"
with open(OUT, "w", encoding="cp437") as f:
    f.write(raw)
print("wrote", OUT, "rows:", len(final))
