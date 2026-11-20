# -*- coding: utf-8 -*-
"""第 3 批：循环队列、双端队列、十字链表的节点（图 3.20 / 3.25 / 4.10）。"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import Fig  # noqa: E402


# ------------------------------------------------------------------ 图 3.20
def _ring(f, cx, cy, r_out, r_in, sector_letters, front, rear):
    f.ellipse(cx, cy, r_out, r_out)
    f.ellipse(cx, cy, r_in, r_in)
    for k in range(8):
        a = math.radians(-90 + 45 * k)          # 0 在正上方，顺时针
        f.line(cx + r_in * math.cos(a), cy + r_in * math.sin(a),
               cx + r_out * math.cos(a), cy + r_out * math.sin(a))
        # 编号写在分隔线外侧
        lx = cx + (r_out + 16) * math.cos(a)
        ly = cy + (r_out + 16) * math.sin(a)
        f.text(lx, ly, str(k), 13)

    rm = (r_out + r_in) / 2
    for k, s in enumerate(sector_letters):
        if not s:
            continue
        a = math.radians(-90 + 45 * k + 22.5)
        f.text(cx + rm * math.cos(a), cy + rm * math.sin(a), s, 13)

    for idx, lab in ((front, "front"), (rear, "rear")):
        a = math.radians(-90 + 45 * idx)
        ca, sa = math.cos(a), math.sin(a)
        x1 = cx + (r_out + 30) * ca
        y1 = cy + (r_out + 30) * sa
        x2 = cx + (r_out + 2) * ca
        y2 = cy + (r_out + 2) * sa
        f.arrow(x1, y1, x2, y2, head=7)
        f.text(x1 + 14 * ca, y1 + 14 * sa, lab, 12)


def f_circ_queue(C=Fig):
    f = C(1120, 300)
    cy, r_out, r_in = 116, 62, 26
    panels = [
        (["", "", "", "", "", "", "", ""], 0, 0, "(a) 空队列"),
        (["A", "", "", "", "", "", "", ""], 0, 1, "(b) A 进队"),
        (["A", "B", "C", "D", "", "", "", ""], 0, 4, "(c) B、C、D 进队"),
        (["", "B", "C", "D", "", "", "", ""], 1, 4, "(d) A 出队"),
        (["", "B", "C", "D", "E", "F", "G", "H"], 1, 0, "(e) E、F、G、H 进队"),
    ]
    x = 96
    for letters, fr, rr, cap in panels:
        _ring(f, x, cy, r_out, r_in, letters, fr, rr)
        f.text(x, 238, cap, 13, color="#333")
        x += 208
    f.text(560, 288, "图 3.20  循环队列的插入和删除", 14, color="#444")
    return f


# ------------------------------------------------------------------ 图 3.25
def f_deque(C=Fig):
    f = C(1000, 300)
    w, h = 36, 26
    panels = [
        # (values, 操作端("left"/"right"/None), 说明, 列, 行)
        (["1", "4", "2", ""], None, "Initialization", 0, 0),
        (["3", "1", "4", "2"], "left", "EnQueueHead(3)", 1, 0),
        (["3", "1", "4", "2", "5"], "right", "EnQueueTail(5)", 2, 0),
        (["1", "4", "2", "5"], "left", "DeQueueHead() → 3", 3, 0),
        (["1", "4", "2"], "right", "DeQueueTail() → 5", 0, 1),
        (["1", "4", "2"], "left", "getHead() → 1", 1, 1),
        (["1", "4", "2"], "right", "getTail() → 2", 2, 1),
    ]
    for values, side, cap, col, row in panels:
        x0 = 60 + col * 240
        y0 = 54 + row * 118
        for i, s in enumerate(values):
            f.rect(x0 + i * w, y0, w, h)
            if s:
                f.text(x0 + i * w + w / 2, y0 + h / 2, s, 13)
        if side == "left":
            f.poly([(x0 - 6, y0 + h / 2 - 7), (x0 - 6, y0 + h / 2 + 7), (x0 - 17, y0 + h / 2)])
        elif side == "right":
            xe = x0 + len(values) * w
            f.poly([(xe + 6, y0 + h / 2 - 7), (xe + 6, y0 + h / 2 + 7), (xe + 17, y0 + h / 2)])
        f.text(x0, y0 + h + 20, cap, 12, color="#333", anchor="start")

    f.text(500, 278, "图 3.25  双端队列的基本操作", 14, color="#444")
    return f


# ------------------------------------------------------------------ 图 4.10
def f_olnode(C=Fig):
    f = C(760, 220)
    hh = 34
    # (a) 附头结点：head|next / down|right
    x, y, cw = 60, 50, 62
    cells = [["head", "next"], ["down", "right"]]
    for r, row in enumerate(cells):
        for c, s in enumerate(row):
            f.rect(x + c * cw, y + r * hh, cw, hh)
            f.text(x + c * cw + cw / 2, y + r * hh + hh / 2, s, 12)
    f.text(x + cw, y + 2 * hh + 18, "(a) 附头结点", 12, color="#333")

    # (b) 非零元素结点
    x2, cw2 = 250, 58
    cells2 = [["head", "row", "col"], ["down", "value", "right"]]
    for r, row in enumerate(cells2):
        for c, s in enumerate(row):
            f.rect(x2 + c * cw2, y + r * hh, cw2, hh)
            f.text(x2 + c * cw2 + cw2 / 2, y + r * hh + hh / 2, s, 12)
    f.text(x2 + 1.5 * cw2, y + 2 * hh + 18, "(b) 非零元素结点", 12, color="#333")

    # (c) 建立 a[i][j] 结点
    x3, cw3 = 540, 58
    f.rect(x3, y, cw3, hh)
    f.rect(x3 + cw3, y, cw3, hh)
    f.rect(x3 + 2 * cw3, y, cw3, hh)
    f.text(x3 + cw3 / 2, y + hh / 2, "false", 12)
    f.text(x3 + cw3 * 1.5, y + hh / 2, "i", 13, italic=True)
    f.text(x3 + cw3 * 2.5, y + hh / 2, "j", 13, italic=True)
    f.rect(x3, y + hh, cw3 * 2, hh)
    f.text(x3 + cw3, y + hh + hh / 2, "a[i][j]", 12)
    f.arrow(x3 + cw3 * 2, y + hh + hh / 2, x3 + cw3 * 2 + 26, y + hh + hh / 2)
    f.text(x3 + 1.5 * cw3, y + 2 * hh + 18, "(c) 建立 a[i][j] 结点", 12, color="#333")

    f.text(380, 200, "图 4.10  十字链表表示中的结点", 14, color="#444")
    return f
