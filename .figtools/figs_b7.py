# -*- coding: utf-8 -*-
"""第 7 批：稀疏矩阵十字链表示例（图 4.11）。"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import Fig  # noqa: E402

CELL_W, CELL_H = 30, 20


def _cellnode(f, x, y, r, c, val):
    """非零元素结点：上排 F|r|c，下排 down|value|right。"""
    tops = ["F", str(r), str(c)]
    bots = ["", val, ""]
    for i, s in enumerate(tops):
        f.rect(x + i * CELL_W, y, CELL_W, CELL_H)
        if s:
            f.text(x + i * CELL_W + CELL_W / 2, y + CELL_H / 2, s, 11)
    for i, s in enumerate(bots):
        f.rect(x + i * CELL_W, y + CELL_H, CELL_W, CELL_H)
        if s:
            f.text(x + i * CELL_W + CELL_W / 2, y + CELL_H + CELL_H / 2, s, 11)
    return (x, y)


def f_olist(C=Fig):
    f = C(960, 470)
    cols = 7
    rows = 6
    gx, gy = 150, 90                      # 网格左上
    cw, ch = 200, 56                      # 每行/列的间距

    # headnode
    f.rect(30, 20, 44, 34, fill="#fff")
    f.text(52, 30, "6", 11)
    f.text(52, 44, "7", 11)
    f.line(30, 37, 74, 37)
    f.line(52, 20, 52, 54)
    f.text(52, 12, "headnode", 11)
    f.arrow(76, 30, gx - 20, gy - 46, head=7)

    # 列头
    for c in range(cols):
        x = gx + c * cw
        f.text(x + 30, gy - 62, "H%d" % c, 11)
        f.rect(x, gy - 50, 60, 34, fill="#fff")
        f.text(x + 30, gy - 42, "T", 11)
        f.text(x + 30, gy - 24, "-", 11)
        f.line(x, gy - 33, x + 60, gy - 33)
        # 列头之间的横向指针
        if c < cols - 1:
            f.arrow(x + 60, gy - 45, x + cw, gy - 45, head=6)

    # 行头 + 网格
    elems = {(0, 2): "11", (0, 5): "13", (1, 0): "12", (1, 6): "14",
             (2, 1): "-4", (2, 5): "-8", (5, 1): "-9"}
    for r in range(rows):
        y = gy + r * ch
        f.text(gx - 96, y + 20, "H%d" % r, 11, anchor="end")
        f.rect(gx - 88, y, 60, 34, fill="#fff")
        f.text(gx - 58, y + 9, "T", 11)
        f.text(gx - 58, y + 26, "-", 11)
        f.line(gx - 88, y + 17, gx - 28, y + 17)
        # 行头之间的纵向指针
        if r:
            f.arrow(gx - 58, y - ch + 34, gx - 58, y, head=6)
        # 该行的非零元
        prev = gx - 28
        for c in range(cols):
            if (r, c) not in elems:
                continue
            x = gx + c * cw
            _cellnode(f, x, y, r, c, elems[(r, c)])
            f.arrow(prev, y + 10, x, y + 10, head=6)
            prev = x + 3 * CELL_W
    f.text(gx - 58, gy + rows * ch + 14, "指向 H6", 11)

    # 矩阵
    mx, my = 700, 400
    mat = [[0, 0, 11, 0, 0, 13, 0], [12, 0, 0, 0, 0, 0, 14],
           [0, -4, 0, 0, 0, -8, 0], [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0], [0, -9, 0, 0, 0, 0, 0]]
    for r in range(rows):
        f.text(mx, my + r * 20, "  ".join("%3d" % v for v in mat[r]), 11, anchor="start")

    f.text(430, 448, "图 4.11  稀疏矩阵的十字链表表示的示例", 14, color="#444")
    return f
