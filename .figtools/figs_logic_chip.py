# -*- coding: utf-8 -*-
"""数字逻辑：触发器符号、74LS 芯片框、状态图。"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figs_logic as H  # noqa: E402
from svgkit import Fig  # noqa: E402

FILL = "#ffffff"
BOX = "#f4f6f8"


def _wire_note(f, x, y, s, size=12, anchor="middle"):
    f.text(x, y, s, size, color="#666", anchor=anchor)


# ---------------- 触发器 ----------------
def _ff(left, right, clock_y, edge, w=190, h=150, caption=None, sub=None):
    f = Fig(w + 150, h + 60)
    x0 = 62
    y0 = 26
    H.ff_box(f, x0, y0, w, h, left, right, clock_y=clock_y, edge=edge)
    if sub:
        _wire_note(f, w / 2 + 50, h + 46, sub)
    return f


def f_sr_latch(C=Fig):
    f = Fig(370, 250)
    x, y, w, h = 96, 30, 180, 160
    H.ff_box(f, x, y, w, h, [("S", 40, False), ("EN", 85, False), ("R", 130, False)],
             [("Q", 45, False), ("Q′", 115, True)])
    return f


def f_dff_fall(C=Fig):
    f = Fig(370, 250)
    x, y, w, h = 96, 35, 180, 155
    H.ff_box(f, x, y, w, h, [("D", 45, False)], [("Q", 50, False), ("Q′", 110, True)],
             clock_y=115, edge="fall")
    return f


def f_jkff(C=Fig):
    f = Fig(370, 250)
    x, y, w, h = 96, 35, 180, 155
    H.ff_box(f, x, y, w, h, [("J", 45, False), ("K", 115, False)],
             [("Q", 50, False), ("Q′", 110, True)], clock_y=82, edge="rise")
    f.text(190, 205, "上升沿触发", 13, color="#555")
    return f


def f_tff(C=Fig):
    f = Fig(370, 250)
    x, y, w, h = 96, 35, 180, 155
    H.ff_box(f, x, y, w, h, [("T", 45, False)], [("Q", 50, False), ("Q′", 110, True)],
             clock_y=115, edge="rise")
    f.text(190, 205, "T=1 时翻转", 13, color="#555")
    return f


# ---------------- 74LS 芯片 ----------------
def _chip(w, h, left, right, bottom, top, name, pad_l=70, pad_r=110, pad_b=46, pad_t=44):
    f = Fig(w + pad_l + pad_r, h + pad_b + pad_t)
    x, y = pad_l, pad_t
    f.rect(x, y, w, h, fill=BOX, sw=1.5)
    f.text(x + w / 2, y + h / 2, name, 15, bold=True)
    for label, dy, bub in left:
        H.pin_left(f, x, y + dy, label, bubble=bub)
    for label, dy, bub in right:
        H.pin_right(f, x + w, y + dy, label, bubble=bub)
    for label, dx, bub in bottom:
        H.pin_bottom(f, x + dx, y + h, label, bubble=bub)
    for label, dx, bub in top:
        H.pin_top(f, x + dx, y, label, bubble=bub)
    return f


def f_138(C=Fig):
    left = [("C", 46, False), ("B", 86, False), ("A", 126, False),
            ("G1", 196, False), ("G2A", 236, True), ("G2B", 276, True)]
    right = [("Y%d" % i, 40 + i * 32, True) for i in range(8)]
    return _chip(170, 330, left, right, [], [], "74LS138", pad_l=80, pad_r=100,
                 pad_b=40, pad_t=40)


def f_151(C=Fig):
    left = [("X2", 40, False), ("X1", 80, False), ("X0", 120, False), ("EN", 165, True)]
    bottom = [("D%d" % i, 120 + i * 46, False) for i in range(8)]
    top = [("Y", 420, False)]
    return _chip(560, 210, left, [], bottom, top, "74LS151", pad_l=70, pad_r=60,
                 pad_b=60, pad_t=50)


def f_283(C=Fig):
    left = []
    bottom = [("A3", 70, False), ("A2", 120, False), ("A1", 170, False), ("A0", 220, False),
              ("B3", 330, False), ("B2", 380, False), ("B1", 430, False), ("B0", 480, False),
              ("Ci", 590, False)]
    top = [("Co", 70, False), ("S3", 250, False), ("S2", 320, False),
           ("S1", 390, False), ("S0", 460, False)]
    return _chip(650, 170, left, [], bottom, top, "74LS283", pad_l=50, pad_r=50,
                 pad_b=56, pad_t=50)


def f_85(C=Fig):
    left = [("A3", 40, False), ("A2", 70, False), ("A1", 100, False), ("A0", 130, False),
            ("I(A<B)", 200, False), ("I(A=B)", 230, False), ("I(A>B)", 260, False),
            ("B3", 320, False), ("B2", 350, False), ("B1", 380, False), ("B0", 410, False)]
    right = [("Y(A<B)", 200, False), ("Y(A=B)", 230, False), ("Y(A>B)", 260, False)]
    return _chip(220, 430, left, right, [], [], "74LS85", pad_l=105, pad_r=120,
                 pad_b=40, pad_t=40)


def f_194(C=Fig):
    left = [("CLK", 40, False), ("CLR", 80, True), ("S1", 120, False), ("S0", 160, False),
            ("Rin", 200, False), ("A", 250, False), ("B", 290, False), ("C", 330, False),
            ("D", 370, False), ("Lin", 415, False)]
    right = [("QA", 130, False), ("QB", 175, False), ("QC", 220, False), ("QD", 265, False)]
    return _chip(180, 450, left, right, [], [], "74LS194", pad_l=105, pad_r=100,
                 pad_b=40, pad_t=40)


def f_163(C=Fig):
    left = [("CLK", 40, False), ("CLR", 85, True), ("LD", 125, True),
            ("ENT", 175, False), ("ENP", 215, False),
            ("A", 270, False), ("B", 305, False), ("C", 340, False), ("D", 375, False)]
    right = [("QA", 100, False), ("QB", 145, False), ("QC", 190, False),
             ("QD", 235, False), ("RCO", 380, False)]
    return _chip(180, 420, left, right, [], [], "74LS163", pad_l=105, pad_r=105,
                 pad_b=40, pad_t=40)


# ---------------- 状态图 ----------------
def _state_pair(f, cx1, cx2, cy, r, lab1, lab2, up, down, title):
    f.circle(cx1, cy, r, fill="#eef3fa", sw=1.5)
    f.circle(cx2, cy, r, fill="#eef3fa", sw=1.5)
    f.text(cx1, cy + 5, lab1, 14)
    f.text(cx2, cy + 5, lab2, 14)
    # 上弧：A → B
    f.arrow(cx1 + r * 0.55, cy - r * 0.85, cx2 - r * 0.55, cy - r * 0.85, head=9)
    f.text((cx1 + cx2) / 2, cy - r * 0.95 - 10, up, 14)
    # 下弧：B → A
    f.arrow(cx2 - r * 0.55, cy + r * 0.85, cx1 + r * 0.55, cy + r * 0.85, head=9)
    f.text((cx1 + cx2) / 2, cy + r * 0.95 + 22, down, 14)
    f.text((cx1 + cx2) / 2, cy + r + 52, title, 13, color="#555")


def f_mealy(C=Fig):
    f = Fig(500, 260)
    _state_pair(f, 110, 390, 110, 56, "A", "B", "x / y", "x′ / y′", "Mealy：输出写在转移弧上")
    return f


def f_moore(C=Fig):
    f = Fig(500, 260)
    _state_pair(f, 110, 390, 110, 64, "A / y1", "B / y2", "x", "x′",
                "Moore：输出写在状态圈内")
    return f
