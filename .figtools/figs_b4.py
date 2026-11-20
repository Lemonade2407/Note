# -*- coding: utf-8 -*-
"""第 4 批：广义表示意图、广义表的存储表示、满/完全二叉树、二叉树链接存储。"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import Fig  # noqa: E402


def _circle(f, x, y, label="", r=13, size=13):
    f.circle(x, y, r, fill="#fff")
    if label:
        f.text(x, y, label, size)


def _atom(f, x, y, label="", w=26, h=20):
    f.rect(x - w / 2, y - h / 2, w, h, fill="#fff")
    if label:
        f.text(x, y, label, 13)


# ---------------------------------------------------------------- 图 4.21
def f_glists(C=Fig):
    f = C(940, 300)
    top = 70
    # A 空表
    _circle(f, 50, top)
    _atom(f, 50, top + 46)
    f.arrow(50, top + 22, 50, top + 33)
    f.text(50, top + 82, "空表", 12, color="#333")

    # B 线性表
    _circle(f, 140, top)
    for dx, lab in ((-20, "a"), (20, "b")):
        _atom(f, 140 + dx, top + 46, lab)
        f.arrow(140 + dx * 0.5, top + 16, 140 + dx, top + 33)
    f.text(140, top + 82, "线性表", 12, color="#333")

    # C 纯表
    _circle(f, 250, top)
    _atom(f, 236, top + 46, "c")
    _circle(f, 276, top + 46, r=12)
    f.arrow(244, top + 14, 236, top + 33)
    f.arrow(256, top + 14, 274, top + 33)
    for dx, lab in ((-22, "d"), (0, "e"), (22, "f")):
        _atom(f, 276 + dx, top + 92, lab, w=22, h=18)
        f.arrow(276 + dx * 0.4, top + 58, 276 + dx, top + 82)
    f.text(252, top + 130, "纯表", 12, color="#333")

    # D 再入表
    _circle(f, 400, top)
    _circle(f, 360, top + 50, r=12)
    _circle(f, 420, top + 50, r=12)
    _circle(f, 468, top + 50, r=12)
    f.arrow(392, top + 12, 364, top + 37)
    f.arrow(400, top + 14, 418, top + 37)
    f.arrow(410, top + 12, 462, top + 37)
    for dx, lab in ((-14, "a"), (0, "b"), (14, "c")):
        _atom(f, 360 + dx, top + 92, lab, w=20, h=18)
        f.arrow(360 + dx * 0.3, top + 63, 360 + dx, top + 82)
    _atom(f, 420, top + 92, "", w=22, h=18)
    f.arrow(420, top + 63, 420, top + 82)
    f.text(400, top + 130, "再入表", 12, color="#333")

    # E 再入表（引用 B、D 的结构）
    _circle(f, 610, top)
    _circle(f, 566, top + 50, r=12)
    _circle(f, 620, top + 50, r=12)
    _circle(f, 674, top + 50, r=12)
    f.arrow(596, top + 14, 570, top + 37)
    f.arrow(610, top + 14, 618, top + 37)
    f.arrow(624, top + 14, 668, top + 37)
    for dx, lab in ((-14, "a"), (0, "b")):
        _atom(f, 566 + dx, top + 94, lab, w=20, h=18)
        f.arrow(566 + dx * 0.3, top + 63, 566 + dx, top + 84)
    _circle(f, 620, top + 92, r=10)
    f.arrow(620, top + 63, 620, top + 81)
    for dx, lab in ((-18, "c"), (0, "d")):
        _atom(f, 620 + dx, top + 132, lab, w=20, h=18)
        f.arrow(620 + dx * 0.3, top + 102, 620 + dx, top + 122)
    _atom(f, 674, top + 94, "", w=22, h=18)
    f.arrow(674, top + 63, 674, top + 84)
    f.text(610, top + 168, "再入表", 12, color="#333")

    # F 递归表
    _circle(f, 820, top)
    _atom(f, 800, top + 50, "h")
    f.arrow(810, top + 14, 800, top + 38)
    f.line(806, top - 6, 878, top - 6)
    f.line(878, top - 6, 878, top + 6)
    f.arrow(878, top + 6, 833, top + 4)
    f.text(820, top + 86, "递归表", 12, color="#333")

    f.text(470, 274, "图 4.21  各种广义表的示意图", 14, color="#444")
    return f


# ---------------------------------------------------------------- 广义表存储
def _gnode(f, x, y, tag, val, nxt, cw=34, h=26, shade=False):
    for i in range(3):
        fill = "#d9d9d9" if (i == 0 and shade) else "none"
        f.rect(x + i * cw, y, cw, h, fill=fill)
    f.text(x + cw / 2, y + h / 2, tag, 13)
    if val:
        f.text(x + cw * 1.5, y + h / 2, val, 13)
    f.text(x + cw * 2.5, y + h / 2, nxt, 13)
    return x + 3 * cw


def f_glist_store(C=Fig):
    f = C(900, 480)
    cw, h = 34, 26
    # A
    x = 130
    f.text(96, 30, "A", 13, anchor="end")
    f.arrow(100, 30, x, 30)
    _gnode(f, x, 17, "0", "1", "∧", cw, h, shade=True)

    # B：0|2|→ 1|a|→ 1|b|∧
    yb = 92
    f.text(96, yb + h / 2, "B", 13, anchor="end")
    f.arrow(100, yb + h / 2, 130, yb + h / 2)
    e = _gnode(f, 130, yb, "0", "2", "", cw, h, shade=True)
    f.arrow(e, yb + h / 2, e + 10, yb + h / 2)
    e2 = _gnode(f, e + 10, yb, "1", "a", "", cw, h)
    f.arrow(e2, yb + h / 2, e2 + 10, yb + h / 2)
    _gnode(f, e2 + 10, yb, "1", "b", "∧", cw, h)

    # D：0|1|→ 2| |→ 2| |→ 2| |∧
    yd = 168
    f.text(96, yd + h / 2, "D", 13, anchor="end")
    f.arrow(100, yd + h / 2, 130, yd + h / 2)
    e = _gnode(f, 130, yd, "0", "1", "", cw, h, shade=True)
    f.arrow(e, yd + h / 2, e + 10, yd + h / 2)
    e2 = _gnode(f, e + 10, yd, "2", "", "", cw, h)
    f.arrow(e2, yd + h / 2, e2 + 10, yd + h / 2)
    e3 = _gnode(f, e2 + 10, yd, "2", "", "", cw, h)
    f.arrow(e3, yd + h / 2, e3 + 10, yd + h / 2)
    _gnode(f, e3 + 10, yd, "2", "", "∧", cw, h)

    # C：0|1|→ 1|c|→ 2| |∧ ；再挂 0|1|→ 1|d|→ 1|e|→ 1|f|∧
    yc = 250
    f.text(96, yc + h / 2, "C", 13, anchor="end")
    f.arrow(100, yc + h / 2, 130, yc + h / 2)
    e = _gnode(f, 130, yc, "0", "1", "", cw, h, shade=True)
    f.arrow(e, yc + h / 2, e + 10, yc + h / 2)
    e2 = _gnode(f, e + 10, yc, "1", "c", "", cw, h)
    f.arrow(e2, yc + h / 2, e2 + 10, yc + h / 2)
    e3 = _gnode(f, e2 + 10, yc, "2", "", "∧", cw, h)

    yd2 = 336
    e4 = _gnode(f, 320, yd2, "0", "1", "", cw, h, shade=True)
    f.arrow(e3 + 2.5 * cw, yc + h, 320 + cw / 2, yd2)
    f.arrow(e4, yd2 + h / 2, e4 + 10, yd2 + h / 2)
    e5 = _gnode(f, e4 + 10, yd2, "1", "d", "", cw, h)
    f.arrow(e5, yd2 + h / 2, e5 + 10, yd2 + h / 2)
    e6 = _gnode(f, e5 + 10, yd2, "1", "e", "", cw, h)
    f.arrow(e6, yd2 + h / 2, e6 + 10, yd2 + h / 2)
    _gnode(f, e6 + 10, yd2, "1", "f", "∧", cw, h)

    # E：0|0|→ 2| |→ 2| |∧
    ye = 410
    f.text(96, ye + h / 2, "E", 13, anchor="end")
    f.arrow(100, ye + h / 2, 130, ye + h / 2)
    e = _gnode(f, 130, ye, "0", "0", "", cw, h, shade=True)
    f.arrow(e, ye + h / 2, e + 10, ye + h / 2)
    e2 = _gnode(f, e + 10, ye, "2", "", "", cw, h)
    f.arrow(e2, ye + h / 2, e2 + 10, ye + h / 2)
    _gnode(f, e2 + 10, ye, "2", "", "∧", cw, h)

    # F：0|1|→ 1|h|→ 2| |∧
    yf = 470
    f.text(96, yf + h / 2, "F", 13, anchor="end")
    f.arrow(100, yf + h / 2, 130, yf + h / 2)
    e = _gnode(f, 130, yf, "0", "1", "", cw, h, shade=True)
    f.arrow(e, yf + h / 2, e + 10, yf + h / 2)
    e2 = _gnode(f, e + 10, yf, "1", "h", "", cw, h)
    f.arrow(e2, yf + h / 2, e2 + 10, yf + h / 2)
    _gnode(f, e2 + 10, yf, "2", "", "∧", cw, h)

    f.text(450, 516, "图 4.22  广义表的存储表示", 14, color="#444")
    return f


# ---------------------------------------------------------------- 满/完全二叉树
def f_bintree_kind(C=Fig):
    f = C(820, 290)
    r = 13
    # 满二叉树：(a)
    xs = {1: 200, 2: 120, 3: 280, 4: 80, 5: 160, 6: 240, 7: 320,
          8: 60, 9: 100, 10: 140, 11: 180, 12: 220, 13: 260, 14: 300, 15: 340}
    ys = {1: 44, 2: 96, 3: 96, 4: 148, 5: 148, 6: 148, 7: 148,
          8: 200, 9: 200, 10: 200, 11: 200, 12: 200, 13: 200, 14: 200, 15: 200}
    for i in range(1, 16):
        p = i // 2
        if p:
            f.line(xs[p], ys[p] + r, xs[i], ys[i] - r)
    for i in range(1, 16):
        _circle(f, xs[i], ys[i], str(i), r)
    f.text(200, 236, "(a) 满二叉树", 13, color="#333")

    # 完全二叉树：(b)
    xs2 = {1: 620, 2: 540, 3: 700, 4: 500, 5: 580, 6: 660, 7: 740}
    ys2 = {1: 44, 2: 96, 3: 96, 4: 148, 5: 148, 6: 148, 7: 148}
    for i in range(1, 8):
        p = i // 2
        if p:
            f.line(xs2[p], ys2[p] + r, xs2[i], ys2[i] - r)
    for i in range(1, 8):
        _circle(f, xs2[i], ys2[i], str(i), r)
    f.text(620, 196, "(b) 完全二叉树", 13, color="#333")

    f.text(420, 272, "图 5.3  满二叉树与完全二叉树", 14, color="#444")
    return f


# ---------------------------------------------------------------- 图 5.10
def f_bintree_link(C=Fig):
    f = C(760, 320)
    h = 26
    # (a) 二叉链表
    x, y = 60, 40
    cells = ["leftChild", "data", "rightChild"]
    cw = 62
    for i, s in enumerate(cells):
        f.rect(x + i * cw, y, cw, h)
        f.text(x + i * cw + cw / 2, y + h / 2, s, 12)
    f.rect(x + cw, y + 66, cw, h, fill="#c9c9c9")
    f.text(x + cw * 1.5, y + 66 + h / 2, "data", 12)
    f.arrow(x + cw * 0.2, y + h, x + cw * 0.8, y + 66)
    f.arrow(x + cw * 2.8, y + h, x + cw * 2.2, y + 66)
    f.text(x - 6, y + 66 + h + 16, "leftChild", 12, anchor="start")
    f.text(x + cw * 2 + 8, y + 66 + h + 16, "rightChild", 12, anchor="start")
    f.text(x + cw * 1.5, y + 140, "(a) 二叉链表", 13, color="#333")

    # (b) 三叉链表
    x2, cw2 = 400, 58
    cells2 = ["leftChild", "data", "parent", "rightChild"]
    for i, s in enumerate(cells2):
        f.rect(x2 + i * cw2, y, cw2, h)
        f.text(x2 + i * cw2 + cw2 / 2, y + h / 2, s, 11)
    f.rect(x2 + cw2, y + 66, cw2, h, fill="#c9c9c9")
    f.text(x2 + cw2 * 1.5, y + 66 + h / 2, "data", 12)
    f.arrow(x2 + cw2 * 0.2, y + h, x2 + cw2 * 0.8, y + 66)
    f.arrow(x2 + cw2 * 3.8, y + h, x2 + cw2 * 3.2, y + 66)
    f.arrow(x2 + cw2 * 2, y + h, x2 + cw2 * 2, y + 66)
    f.text(x2 + cw2 * 2, y + h - 6, "parent", 11)
    f.text(x2 - 2, y + 66 + h + 16, "leftChild", 12, anchor="start")
    f.text(x2 + cw2 * 3 + 2, y + 66 + h + 16, "rightChild", 12, anchor="start")
    f.text(x2 + cw2 * 2, y + 140, "(b) 三叉链表", 13, color="#333")

    f.text(380, 300, "图 5.10  二叉树的链接存储表示", 14, color="#444")
    return f
