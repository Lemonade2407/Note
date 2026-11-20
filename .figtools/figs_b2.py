# -*- coding: utf-8 -*-
"""第 2 批：静态链表、栈、活动记录、队列（图 2.23 / 3.1 / 3.12 / 3.19）。"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import Fig  # noqa: E402


# ------------------------------------------------------------------ 图 2.23
def f_static_list(C=Fig):
    f = C(900, 320)
    # (a) 动态链表
    y, h, w = 44, 34, 52
    cy = y + h / 2
    f.text(14, cy, "first", 15, anchor="start")
    f.arrow(52, cy, 74, cy)
    vals = ["25", "49", "92", "57", "11", "36", "78"]
    xs = [78 + i * 80 for i in range(len(vals))]
    for i, (x, v) in enumerate(zip(xs, vals)):
        f.rect(x, y, w, h)
        f.line(x + w - 18, y, x + w - 18, y + h)
        f.text(x + (w - 18) / 2, cy, v, 15)
        if i == len(vals) - 1:
            f.text(x + w - 9, cy, "∧", 14)
    for i in range(len(xs) - 1):
        f.arrow(xs[i] + w, cy, xs[i + 1], cy)
    f.text(360, 100, "(a) 动态链表", 14, color="#333")

    # (b) 静态链表
    tx, ty = 220, 138
    cw, hh = 42, 30
    f.text(tx - 16, ty + hh / 2, "data", 14, anchor="end")
    f.text(tx - 16, ty + hh + hh / 2, "link", 14, anchor="end")

    data = ["", "25", "92", "57", "36", "78", "11", "49"]
    link = ["1", "7", "3", "6", "5", "-1", "4", "2"]
    for r, row in enumerate((data, link)):
        for c, s in enumerate(row):
            f.rect(tx + cw * c, ty + hh * r, cw, hh)
            if s:
                f.text(tx + cw * c + cw / 2, ty + hh * r + hh / 2, s, 14)
    f.text(360, ty + 2 * hh + 34, "(b) 静态链表", 14, color="#333")
    f.text(450, ty + 2 * hh + 74, "图 2.23  静态链表结构", 14, color="#444")
    return f


# ------------------------------------------------------------------ 图 3.1
def f_stack(C=Fig):
    f = C(360, 330)
    x, y, w, h = 150, 74, 130, 34
    labels = ["aₙ", "aₙ₋₁", "", "a₂", "a₁"]
    for i in range(5):
        f.rect(x, y + i * h, w, h)
    f.sub_text(x + w / 2, y + h / 2, "a", "n", 16)
    f.sub_text(x + w / 2, y + 1.5 * h, "a", "n-1", 16)
    f.text(x + w / 2, y + 2.5 * h, "⋮", 15)
    f.sub_text(x + w / 2, y + 3.5 * h, "a", "2", 16)
    f.sub_text(x + w / 2, y + 4.5 * h, "a", "1", 16)

    f.text(96, y + h / 2, "top", 15, anchor="end")
    f.arrow(100, y + h / 2, x, y + h / 2)
    f.text(84, y + 4.5 * h, "bottom", 15, anchor="end")
    f.arrow(88, y + 4.5 * h, x, y + 4.5 * h)

    f.text(120, 40, "退栈（弹出）", 15, anchor="middle")
    f.arrow(130, 54, 176, 70)
    f.text(268, 40, "进栈（压入）", 15, anchor="middle")
    f.arrow(258, 56, 214, 70)

    f.text(180, 312, "图 3.1  栈", 14, color="#444")
    return f


# ------------------------------------------------------------------ 图 3.12
def f_activation(C=Fig):
    f = C(760, 320)
    # 左：调用模块 / 被调用函数模块
    f.rect(60, 40, 230, 104)
    f.text(175, 62, "call Function（<参数表>）", 14)
    f.text(175, 90, "〈下一条指令〉", 14)
    f.rect(60, 186, 230, 96)
    f.text(175, 210, "Function（<参数表>）", 14)
    f.text(175, 240, "⋮", 15)
    f.text(175, 266, "return", 14)

    f.text(28, 130, "调用模块", 14, anchor="middle")
    f.poly([[46, 96], [30, 96], [30, 196], [56, 196]], head=8)
    f.text(120, 300, "被调用函数模块", 13, anchor="middle")

    # 调用与返回虚线
    f.poly([[290, 88], [330, 88], [330, 240], [292, 240]], dash="5 4")
    f.arrow(330, 240, 292, 240, dash="5 4")
    f.text(392, 300, "函数调用与返回", 13, anchor="middle")

    # 右：活动记录
    rx, ry, rw = 470, 60, 240
    rows = ["返回地址（递归调用的下一条指令）", "局部变量值", "参数的副本空间"]
    hs = [44, 34, 34]
    cy = ry
    for s, hh in zip(rows, hs):
        f.rect(rx, cy, rw, hh)
        f.text(rx + rw / 2, cy + hh / 2, s, 13)
        cy += hh
    f.text(rx + rw / 2, cy + 26, "活动记录（递归工作记录）", 13, color="#333")

    f.text(380, 308, "图 3.12  函数递归调用时的活动记录", 14, color="#444")
    return f


# ------------------------------------------------------------------ 图 3.19
def _queue_panel(f, x, bottom, cells, front, rear, caption):
    h, w = 26, 54
    n = 7
    for i in range(n):
        f.rect(x, bottom - (i + 1) * h, w, h)
    for i, s in enumerate(cells):
        if s:
            f.text(x + w / 2, bottom - i * h - h / 2, s, 14)

    def marker(row, label, side="left"):
        yy = bottom - row * h - h / 2
        if side == "left":
            f.text(x - 56, yy, label, 13, anchor="start")
            f.arrow(x - 8, yy, x, yy)
        else:
            f.text(x + w + 8, yy, label, 13, anchor="start")
            f.arrow(x + w + 8, yy, x + w + 2, yy)

    marker(front, "front", "left")
    marker(rear, "rear", "right" if rear >= n - 1 else "right")
    f.text(x + w / 2, bottom + 20, caption, 13, color="#333")


def f_queue(C=Fig):
    f = C(980, 320)
    bottom = 224
    panels = [
        (["", "", "", "", "", "", ""], 0, 0, "(a) 空队列"),
        (["A", "", "", "", "", "", ""], 0, 1, "(b) A 进队"),
        (["A", "B", "C", "", "", "", ""], 0, 3, "(c) B、C 进队"),
        (["", "B", "C", "", "", "", ""], 1, 3, "(d) A 出队"),
        (["", "", "C", "", "", "", ""], 2, 3, "(e) B 出队"),
        (["", "", "C", "D", "E", "F", "", ], 2, 6, "(f) D、E、F 进队"),
    ]
    x = 116
    for cells, fr, rr, cap in panels:
        _queue_panel(f, x, bottom, cells, fr, rr, cap)
        x += 160
    f.text(490, 300, "图 3.19  队列的插入和删除", 14, color="#444")
    return f
