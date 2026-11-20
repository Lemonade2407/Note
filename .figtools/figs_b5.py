# -*- coding: utf-8 -*-
"""第 5 批：二叉树静态链表、线索二叉树、Huffman 构建过程。"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import Fig  # noqa: E402


def _c(f, x, y, label="", r=14):
    f.circle(x, y, r, fill="#fff")
    if label:
        f.text(x, y, label, 14)


# ---------------------------------------------------------------- 图 5.12
def f_bt_static(C=Fig):
    f = C(880, 360)
    pos = {"A": (150, 40), "B": (110, 100), "C": (60, 160),
           "D": (150, 160), "E": (110, 220), "F": (200, 220), "G": (150, 280)}
    edges = [("A", "B"), ("B", "C"), ("B", "D"), ("D", "E"), ("D", "F"), ("E", "G")]
    for a, b in edges:
        f.line(pos[a][0], pos[a][1] + 14, pos[b][0], pos[b][1] - 14)
    for k, (x, y) in pos.items():
        _c(f, x, y, k)
    f.arrow(150, 12, 150, 26)
    f.text(160, 14, "root", 12, anchor="start")

    # 右侧静态链表
    tx, ty = 380, 50
    cw, rh = 86, 30
    heads = ["data", "parent", "leftChild", "rightChild"]
    for i, s in enumerate(heads):
        f.text(tx + 40 + i * cw + cw / 2, ty - 14, s, 13)
    rows = [("A", "-1", "1", "-1"), ("B", "0", "2", "3"), ("C", "1", "-1", "-1"),
            ("D", "1", "4", "5"), ("E", "3", "-1", "6"), ("F", "3", "-1", "-1"),
            ("G", "4", "-1", "-1")]
    for r, row in enumerate(rows):
        y = ty + r * rh
        f.text(tx + 26, y + rh / 2, str(r), 13, anchor="end")
        for c, s in enumerate(row):
            f.rect(tx + 40 + c * cw, y, cw, rh)
            f.text(tx + 40 + c * cw + cw / 2, y + rh / 2, s, 13)

    f.text(440, 330, "图 5.12  二叉树的静态链表表示", 14, color="#444")
    return f


# ---------------------------------------------------------------- 图 5.28
def f_threaded(C=Fig):
    f = C(900, 400)
    # 顶部结点结构
    x, y, cw, h = 120, 26, 78, 28
    for i, s in enumerate(["leftChild", "ltag", "data", "rtag", "rightChild"]):
        f.rect(x + i * cw, y, cw, h)
        f.text(x + i * cw + cw / 2, y + h / 2, s, 12)

    # 左：中序线索树
    pos = {"A": (180, 120), "B": (120, 190), "C": (250, 190),
           "D": (80, 260), "E": (160, 260)}
    for a, b in (("A", "B"), ("A", "C"), ("B", "D"), ("B", "E")):
        f.line(pos[a][0], pos[a][1] + 14, pos[b][0], pos[b][1] - 14)
    for k, (px, py) in pos.items():
        _c(f, px, py, k)
    # 中序：D B E A C —— 虚线表示线索（后继）
    import math
    for a, b in (("D", "B"), ("B", "E"), ("E", "A"), ("A", "C")):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy) or 1
        ux, uy = dx / d, dy / d
        sx, sy = x1 + ux * 16, y1 + uy * 16
        ex, ey = x2 - ux * 18, y2 - uy * 18
        f.line(sx, sy, ex, ey, dash=True)
        px, py = -uy, ux
        f.poly([(ex + ux * 8, ey + uy * 8),
                (ex + px * 4.5, ey + py * 4.5),
                (ex - px * 4.5, ey - py * 4.5)])

    # 右：二叉链表表示（每个结点 5 格）
    bx, by, bw, bh = 470, 110, 44, 26
    nodes = [("A", "^", "0", "0", ""), ("B", "1", "1", "0", ""),
             ("C", "0", "0", "1", "^"), ("D", "1", "1", "1", ""),
             ("E", "1", "1", "1", "^")]
    for i, (a, lc, lt, rt, rc) in enumerate(nodes):
        yy = by + i * 42
        vals = [lc, lt, a, rt, rc]
        for j, s in enumerate(vals):
            f.rect(bx + j * bw, yy, bw, bh)
            f.text(bx + j * bw + bw / 2, yy + bh / 2, s, 12)
        # 表示指向下一层的指针
        if i in (0, 1, 3):
            f.arrow(bx + bw * 0.5, yy + bh, bx + bw * 0.5, yy + bh + 16)
    f.text(470, 96, "中序线索二叉链表", 12, anchor="start", color="#333")

    f.text(440, 366, "图 5.28  中序线索二叉树及其二叉链表表示", 14, color="#444")
    return f


# ---------------------------------------------------------------- 图 5.50
def f_huffman(C=Fig):
    f = C(1020, 380)
    # (a) 初始：7 5 2 4
    def box(x, y, s, w=28, h=26):
        f.rect(x, y, w, h, fill="#fff")
        f.text(x + w / 2, y + h / 2, s, 13)

    f.text(70, 130, "F：{7}{5}{2}{4}", 13, anchor="start")
    for i, s in enumerate(["7", "5", "2", "4"]):
        box(70 + i * 34, 160, s)
    f.text(120, 210, "(a) 初始", 13, color="#333")

    # (b) 合并 2、4 → 6
    f.text(300, 100, "F：{7}{5}{6}", 13, anchor="start")
    _c(f, 410, 150, "6")
    for dx, s in ((-16, "2"), (16, "4")):
        f.line(410, 164, 410 + dx, 186)
        box(410 + dx - 10, 188, s, 20, 20)
    for i, s in enumerate(["7", "5"]):
        box(296 + i * 34, 190, s, 26, 24)
    f.text(350, 240, "(b) 合并 {2}{4}", 13, color="#333")

    # (c) 合并 5、6 → 11
    f.text(520, 80, "F：{7}{11}", 13, anchor="start")
    _c(f, 560, 120, "11")
    f.line(560, 134, 540, 156)
    box(530, 158, "5", 20, 20)
    f.line(560, 134, 580, 156)
    _c(f, 580, 168, "6", r=12)
    for dx, s in ((-10, "2"), (10, "4")):
        f.line(580, 180, 580 + dx, 196)
        box(580 + dx - 8, 198, s, 16, 18)
    box(500, 220, "7", 24, 22)
    f.text(560, 250, "(c) 合并 {5}{6}", 13, color="#333")

    # (d) 合并 7、11 → 18
    f.text(760, 60, "F：{18}", 13, anchor="start")
    _c(f, 800, 96, "18")
    f.line(800, 110, 770, 134)
    box(752, 136, "7", 24, 22)
    f.line(800, 110, 830, 134)
    _c(f, 830, 146, "11", r=12)
    f.line(830, 158, 812, 176)
    box(800, 178, "5", 20, 20)
    f.line(830, 158, 848, 176)
    _c(f, 848, 190, "6", r=11)
    for dx, s in ((-8, "2"), (8, "4")):
        f.line(848, 201, 848 + dx, 214)
        box(848 + dx - 7, 216, s, 14, 16)
    f.text(800, 246, "(d) 合并 {7}{11}", 13, color="#333")

    f.text(500, 330, "图 5.50  Huffman 树的构造过程", 14, color="#444")
    return f
