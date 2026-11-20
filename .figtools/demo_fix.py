# -*- coding: utf-8 -*-
"""重绘两张示例样张，严格对齐原图（图 2.5、图 6.12）。输出到 D:\\Note\\.svg_work。"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import Fig  # noqa: E402

WORK = r"D:\Note\.svg_work"
OUT = os.path.join(WORK, "preview")
SVG_DIR = os.path.join(WORK, "out")


# ---------------------------------------------------------------- 图 2.5 单链表
def fig_single_list(C=Fig):
    f = C(660, 140)
    y, h = 36, 40
    dw, pw = 38, 28
    w = dw + pw
    cy = y + h / 2

    f.text(12, cy, "first", 17, anchor="start")
    f.arrow(54, cy, 76, cy)

    xs = [80, 186, 292, 436]
    labels = [("a", "1"), ("a", "2"), ("a", "3"), ("a", "n")]
    for i, (x, (m, s)) in enumerate(zip(xs, labels)):
        f.rect(x, y, w, h)
        f.line(x + dw, y, x + dw, y + h)
        f.sub_text(x + dw / 2, cy, m, s, 17)
        if i == len(xs) - 1:
            f.text(x + dw + pw / 2, cy, "∧", 15)

    for i in range(len(xs) - 1):
        x1, x2 = xs[i] + w, xs[i + 1]
        if i == 2:                       # a3 → an 之间断开，画省略号
            f.arrow(x1, cy, x1 + 24, cy)
            f.text((x1 + x2) / 2, cy - 1, "⋯", 16)
            f.arrow(x2 - 26, cy, x2, cy)
        else:
            f.arrow(x1, cy, x2, cy)

    f.text(330, 118, "图 2.5  单链表结构", 14, color="#444")
    return f


# ---------------------------------------------------------------- 图 6.12 跳表
SLOT = 18
DW, PW = 30, 24
NW = DW + PW
STEP = NW + 24
X_SENT = 26


def _skip_panel(f, bottom, levels, caption_y, caption):
    """levels: [(label, lvl), ...]；左右哨兵各占 levels_max+1 个槽。"""
    lmax = max([l for _, l in levels] + [0])

    def box(x, lv, label):
        hh = SLOT * (lv + 1)
        top = bottom - hh
        f.rect(x, top, NW, hh)
        for i in range(1, lv + 1):
            f.line(x, bottom - SLOT * i, x + NW, bottom - SLOT * i)
        f.line(x + DW, bottom - SLOT, x + DW, bottom)   # 仅底层分数据域/指针域
        if label:
            f.text(x + DW / 2, bottom - SLOT / 2, label, 14)

    left_x = X_SENT
    box(left_x, lmax, None)
    xs = []
    for i, (lab, lv) in enumerate(levels):
        x = X_SENT + NW + 30 + i * STEP
        box(x, lv, lab)
        xs.append((x, lv))
    tail_x = X_SENT + NW + 30 + len(levels) * STEP
    box(tail_x, lmax, None)

    for lv in range(lmax + 1):
        yline = bottom - SLOT * lv - SLOT / 2
        chain = [left_x] + [x for x, l in xs if l >= lv] + [tail_x]
        for a, b in zip(chain, chain[1:]):
            f.arrow(a + NW, yline, b, yline, head=7)

    f.text(348, caption_y, caption, 14, color="#333")
    return tail_x + NW


def fig_skip_list(C=Fig):
    f = C(736, 520)
    base = [("10", 0), ("20", 0), ("30", 0), ("40", 0), ("50", 0), ("60", 0), ("70", 0)]

    _skip_panel(f, 76, base, 104, "(a) 带有附加头结点和尾结点的有序链表")

    b = [(l, 1 if l == "40" else 0) for l, _ in base]
    _skip_panel(f, 236, b, 264, "(b) 在链表中部增加一个链接指针")

    c = [(l, 2 if l == "40" else (1 if l in ("20", "60") else 0)) for l, _ in base]
    _skip_panel(f, 416, c, 444, "(c) 在前半部分和后半部分中部各增加一个链接指针")

    f.text(348, 492, "图 6.12  跳表的结构", 14, color="#444")
    return f


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(SVG_DIR, exist_ok=True)
    jobs = [("示例-单链表", fig_single_list), ("示例-跳表", fig_skip_list)]
    for name, fn in jobs:
        f = fn()
        svg = os.path.join(SVG_DIR, name + ".svg")
        png = os.path.join(OUT, name + ".png")
        f.save(svg)
        f.scale = 1.6
        f.preview(png)
        print(f"{name}: svg={os.path.getsize(svg)}B  png={os.path.getsize(png)}B")
