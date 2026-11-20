# -*- coding: utf-8 -*-
"""数字逻辑笔记插图：正式风格（直线、标准符号、真实文字）。"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import Fig  # noqa: E402

INK = "#2b2b2b"
FILL = "#f7f7f7"


# ---------------- 基本图元 ----------------
def pin_left(f, bx, y, label, bubble=False, wire=30, size=15, sub=None):
    """左侧引脚：导线 + 可选反相圈 + 框内标号。"""
    x0 = bx - wire
    if bubble:
        f.circle(bx - 5, y, 5)
        f.line(x0, y, bx - 10, y)
    else:
        f.line(x0, y, bx, y)
    if sub:
        f.sub_text(bx + 12, y, label, sub, size=size, anchor="start")
    else:
        f.text(bx + 12, y, label, size, anchor="start")
    return x0


def pin_right(f, bx, y, label, bubble=False, wire=30, size=15, sub=None):
    x0 = bx + wire
    if bubble:
        f.circle(bx + 5, y, 5)
        f.line(bx + 10, y, x0, y)
    else:
        f.line(bx, y, x0, y)
    if sub:
        f.sub_text(bx - 12, y, label, sub, size=size, anchor="end")
    else:
        f.text(bx - 12, y, label, size, anchor="end")
    return x0


def pin_bottom(f, x, by, label, bubble=False, wire=26, size=15):
    if bubble:
        f.circle(x, by + 5, 5)
        f.line(x, by + 10, x, by + wire)
    else:
        f.line(x, by, x, by + wire)
    f.text(x, by - 12, label, size, anchor="middle")


def pin_top(f, x, by, label, bubble=False, wire=26, size=15, sub=None):
    if bubble:
        f.circle(x, by - 5, 5)
        f.line(x, by - 10, x, by - wire)
    else:
        f.line(x, by, x, by - wire)
    if sub:
        f.sub_text(x, by + 12, label, sub, size=size)
    else:
        f.text(x, by + 12, label, size, anchor="middle")


def clock(f, bx, y, wire=30, edge="rise"):
    """时钟输入：导线 + 框内三角。"""
    f.line(bx - wire, y, bx, y)
    f.poly([(bx, y - 7), (bx + 8, y), (bx, y + 7)], sw=1.2)
    if edge == "fall":
        f.circle(bx - 5, y, 5)
        f.line(bx - wire, y, bx - 10, y)
    f.text(bx + 12, y, "CP", 14, anchor="start")


# ---------------- 门电路符号 ----------------
def gate_and(f, x, y, w=46, h=36, out_bubble=False):
    """与门：左边竖线 + 右半圆。返回输出点。"""
    r = h / 2
    f.poly([(x, y - r), (x, y + r)], sw=1.3)
    f.line(x, y - r, x + w - r, y - r)
    f.line(x, y + r, x + w - r, y + r)
    pts = [(x + w - r + r * math.cos(a), y + r * math.sin(a))
           for a in [math.pi * i / 18 for i in range(-9, 10)]]
    f.poly(pts, sw=1.3)
    ox = x + w
    if out_bubble:
        f.circle(ox + 5, y, 5)
        ox += 10
    f.line(x + w, y, ox, y)
    return ox


def _or_shape(f, x, y, w, h, sw=1.3):
    r = h / 2
    left = [(x + 6 * math.sin(a), y + r * math.cos(a))
            for a in [math.pi * i / 18 for i in range(-9, 10)]]
    f.poly(left, sw=sw)
    top = [(x + 6 * math.sin(a), y - r * math.cos(a)) for a in
           [math.pi * i / 18 for i in range(-9, 10)]]
    f.poly([(px + (w - 6) * (i / 18.0) ** 1.0, py) for i, (px, py) in enumerate(top)], sw=sw)


def _bez2(p0, c, p1, n=24):
    out = []
    for i in range(n + 1):
        t = i / float(n)
        out.append(((1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * c[0] + t * t * p1[0],
                    (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * c[1] + t * t * p1[1]))
    return out


def gate_or(f, x, y, w=50, h=36, out_bubble=False, xor=False):
    """或门：左凸弧 + 上下两条汇向尖端的曲线。"""
    r = h / 2
    back = [(x - 14 * math.sin(math.pi * i / 24), y - r * math.cos(math.pi * i / 24))
            for i in range(25)]
    f.poly(back, sw=1.3)
    if xor:
        f.poly([(px - 7, py) for px, py in back], sw=1.3)
    top = _bez2((x, y - r), (x + w * 0.52, y - r * 0.92), (x + w, y))
    bot = _bez2((x, y + r), (x + w * 0.52, y + r * 0.92), (x + w, y))
    f.poly(top, sw=1.3)
    f.poly(bot, sw=1.3)
    ox = x + w
    if out_bubble:
        f.circle(ox + 5, y, 5)
        ox += 10
    f.line(x + w, y, ox, y)
    return ox


def gate_not(f, x, y, w=40, h=36):
    r = h / 2
    f.poly([(x, y - r), (x + w, y), (x, y + r), (x, y - r)], sw=1.3)
    f.circle(x + w + 5, y, 5)
    f.line(x + w + 10, y, x + w + 20, y)
    return x + w + 20


# ---------------- 触发器 / 芯片外框 ----------------
def ff_box(f, x, y, w, h, left, right, clock_y=None, edge="rise", title=None):
    f.rect(x, y, w, h, fill=FILL, sw=1.4)
    for label, dy, bub in left:
        if clock_y is not None and abs(dy - clock_y) < 0.1:
            continue
        pin_left(f, x, y + dy, label, bubble=bub)
    for label, dy, bub in right:
        pin_right(f, x + w, y + dy, label, bubble=bub)
    if clock_y is not None:
        clock(f, x, y + clock_y, edge=edge)
    if title:
        f.text(x + w / 2, y + h + 22, title, 13, color="#555")


def chip(f, x, y, w, h, left, right, bottom, top, name):
    f.rect(x, y, w, h, fill="#ffffff", sw=1.4)
    f.text(x + w / 2, y + h / 2 - 6, name, 16, bold=True)
    f.line(x + 10, y + h / 2 + 6, x + w - 10, y + h / 2 + 6, sw=0.8)
    for label, dy, bub in left:
        pin_left(f, x, y + dy, label, bubble=bub)
    for label, dy, bub in right:
        pin_right(f, x + w, y + dy, label, bubble=bub)
    for label, dx, bub in bottom:
        pin_bottom(f, x + dx, y + h, label, bubble=bub)
    for label, dx, bub in top:
        pin_top(f, x + dx, y, label, bubble=bub)
