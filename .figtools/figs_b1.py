# -*- coding: utf-8 -*-
"""第 1 批：顺序表、单链表、循环单链表、双向循环链表（对应图 2.1 / 2.5 / 2.12 / 2.16）。"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import Fig  # noqa: E402


# ------------------------------------------------------------------ 图 2.1
def f_seqlist(C=Fig):
    f = C(900, 156)
    widths = [58, 58, 40, 62, 58, 40, 58, 40, 66]
    cells = [("a", "1"), ("a", "2"), None, ("a", "i-1"), ("a", "i"), None,
             ("a", "n"), None, None]
    idx = ["0", "1", "⋯", "i-1", "i", "⋯", "n-1", "⋯", "maxSize"]
    x0, y, h = 216, 74, 42

    f.text(206, 52, "下标位置", 15, anchor="end")
    f.text(206, 96, "数组（线性表）存储空间", 15, anchor="end")

    cx = x0
    for i, w in enumerate(widths):
        f.rect(cx, y, w, h)
        if idx[i]:
            f.text(cx + w / 2, 52, idx[i], 14)
        if cells[i]:
            f.sub_text(cx + w / 2, y + h / 2, cells[i][0], cells[i][1], 16)
        elif cells[i] is None and i in (2, 5, 7):
            f.text(cx + w / 2, y + h / 2, "⋯", 16)
        cx += w

    f.text(450, 142, "图 2.1  顺序表的示意图", 14, color="#444")
    return f


# ------------------------------------------------------------------ 图 2.5
NODE_DW, NODE_PW = 38, 28
NODE_W = NODE_DW + NODE_PW


def _node(f, x, y, h, sub, tail=False):
    f.rect(x, y, NODE_W, h)
    f.line(x + NODE_DW, y, x + NODE_DW, y + h)
    f.sub_text(x + NODE_DW / 2, y + h / 2, "a", sub, 17)
    if tail:
        f.text(x + NODE_DW + NODE_PW / 2, y + h / 2, "∧", 15)


def f_single_list(C=Fig):
    f = C(660, 140)
    y, h = 36, 40
    cy = y + h / 2
    f.text(12, cy, "first", 17, anchor="start")
    f.arrow(54, cy, 76, cy)
    xs = [80, 186, 292, 436]
    subs = ["1", "2", "3", "n"]
    for i, x in enumerate(xs):
        _node(f, x, y, h, subs[i], tail=(i == 3))
    for i in range(3):
        x1, x2 = xs[i] + NODE_W, xs[i + 1]
        if i == 2:
            f.arrow(x1, cy, x1 + 24, cy)
            f.text((x1 + x2) / 2, cy - 1, "⋯", 16)
            f.arrow(x2 - 26, cy, x2, cy)
        else:
            f.arrow(x1, cy, x2, cy)
    f.text(330, 118, "图 2.5  单链表结构", 14, color="#444")
    return f


# ------------------------------------------------------------------ 图 2.12
def f_circ_single(C=Fig):
    f = C(680, 170)
    y, h = 58, 40
    cy = y + h / 2
    f.text(12, cy, "first", 17, anchor="start")
    f.arrow(54, cy, 76, cy)
    xs = [80, 190, 300, 450]
    subs = ["1", "2", "3", "n"]
    for i, x in enumerate(xs):
        f.rect(x, y, NODE_W, h)
        f.line(x + NODE_DW, y, x + NODE_DW, y + h)
        f.sub_text(x + NODE_DW / 2, cy, "a", subs[i], 17)
    for i in range(3):
        x1, x2 = xs[i] + NODE_W, xs[i + 1]
        if i == 2:
            f.arrow(x1, cy, x1 + 26, cy)
            f.text((x1 + x2) / 2, cy - 1, "⋯", 16)
            f.arrow(x2 - 28, cy, x2, cy)
        else:
            f.arrow(x1, cy, x2, cy)

    # 尾结点指针回绕到 a1：从 a_n 指针域右侧上行，绕到 a1 上方再下来
    right = xs[3] + NODE_W
    f.poly([[right, cy], [right + 22, cy], [right + 22, 30], [xs[0] + 12, 30],
            [xs[0] + 12, y]], head=8)

    f.text(340, 148, "图 2.12  循环单链表的示意图", 14, color="#444")
    return f


# ------------------------------------------------------------------ 图 2.16
def f_circ_double(C=Fig):
    f = C(820, 380)
    h = 38
    w = 54

    # (a) 非空表
    ya = 90
    cya = ya + h / 2
    sent, a1, an = 100, 196, 470
    for x, shaded in ((sent, True), (a1, False), (an, False)):
        f.rect(x, ya, w, h, fill="#d8d8d8" if shaded else "none")
    f.sub_text(a1 + w / 2, cya, "a", "1", 16)
    f.sub_text(an + w / 2, cya, "a", "n", 16)

    # 前向（上）/后向（下）
    f.arrow(sent + w, cya - 9, a1, cya - 9)
    f.arrow(a1 + w, cya - 9, a1 + w + 34, cya - 9)
    f.text((a1 + w + an) / 2 + 14, cya - 24, "⋯", 15)
    f.arrow(an - 34, cya - 9, an, cya - 9)
    f.arrow(an, cya + 9, an - 34, cya + 9)
    f.arrow((a1 + w + an) / 2 + 34, cya + 9, a1 + w, cya + 9)
    f.arrow(a1, cya + 9, sent + w, cya + 9)

    # 两条回环（上、下）
    f.poly([[an + w, cya - 9], [an + w + 20, cya - 9], [an + w + 20, ya - 18],
            [sent - 18, ya - 18], [sent - 18, cya - 9], [sent, cya - 9]], head=8)
    f.poly([[sent, cya + 9], [sent - 18, cya + 9], [sent - 18, ya + h + 18],
            [an + w + 20, ya + h + 18], [an + w + 20, cya + 9], [an + w, cya + 9]],
           head=8)
    f.text(370, ya - 30, "⋯", 15)
    f.text(370, ya + h + 30, "⋯", 15)

    # first 指针：从左下方指入哨兵
    f.text(64, ya + h + 44, "first", 15, anchor="middle")
    f.arrow(64, ya + h + 34, sent + 20, ya + h + 2)
    f.text(310, 230, "(a) 非空表", 14, color="#333")

    # (b) 空表
    yb, xb = 258, 640
    cyb = yb + h / 2
    f.rect(xb, yb, w, h, fill="#d8d8d8")
    f.poly([[xb + w, cyb - 9], [xb + w + 16, cyb - 9], [xb + w + 16, yb - 18],
            [xb - 16, yb - 18], [xb - 16, cyb - 9], [xb, cyb - 9]], head=8)
    f.poly([[xb, cyb + 9], [xb - 16, cyb + 9], [xb - 16, yb + h + 18],
            [xb + w + 16, yb + h + 18], [xb + w + 16, cyb + 9], [xb + w, cyb + 9]],
           head=8)
    f.text(xb - 22, yb + h + 44, "first", 15, anchor="middle")
    f.arrow(xb - 22, yb + h + 34, xb + 12, yb + h + 2)
    f.text(xb + 40, yb + h + 62, "(b) 空表", 14, color="#333")

    f.text(400, 396, "图 2.16  带附加头结点的循环双链表", 14, color="#444")
    return f
