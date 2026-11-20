# -*- coding: utf-8 -*-
"""数字逻辑笔记插图：正式风格（表格 / 芯片框 / 状态图）。"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figs_logic as H  # noqa: E402
from svgkit import Fig  # noqa: E402

INK = "#2b2b2b"
FILL = "#ffffff"


# ---------- 门电路单元：输入 A/B，输出 Y ----------
def _inputs(f, x, y, names=("A", "B"), span=22):
    ys = []
    n = len(names)
    for i, nm in enumerate(names):
        yy = y - span * (n - 1) / 2 + i * span
        f.line(x - 26, yy, x, yy)
        f.text(x - 30, yy, nm, 13, anchor="end")
        ys.append(yy)
    return ys


def gate(f, cx, cy, kind, size=1.0):
    """国标（IEC 矩形）逻辑符号：& / ≥1 / 1 / =1，输出圈表示取反。"""
    w, h = 52 * size, 34 * size
    x, y = cx - w / 2, cy
    sym = {"and": "&", "nand": "&", "or": "≥1", "nor": "≥1",
           "not": "1", "xor": "=1", "xnor": "=1"}.get(kind)
    names = ("A",) if kind == "not" else ("A", "B")
    ys = []
    n = len(names)
    for i, nm in enumerate(names):
        yy = y - 11 * (n - 1) + i * 22 * (1 if n > 1 else 0)
        f.line(x - 28, yy, x, yy)
        f.text(x - 32, yy, nm, 13, anchor="end")
        ys.append(yy)
    if kind == "aoi":
        a1 = _iec_box(f, x - 56, y - 30, 46, 26, "&")
        a2 = _iec_box(f, x - 56, y + 4, 46, 26, "&")
        for i, (yy, nm) in enumerate(zip((-22, -8), ("A", "B"))):
            f.line(x - 112, y + yy, x - 56, y + yy)
            f.text(x - 116, y + yy, nm, 12, anchor="end")
        for i, (yy, nm) in enumerate(zip((12, 26), ("C", "D"))):
            f.line(x - 112, y + yy, x - 56, y + yy)
            f.text(x - 116, y + yy, nm, 12, anchor="end")
        f.line(a1, y - 17, x - 6, y - 17)
        f.line(a2, y + 17, x - 6, y + 17)
        f.line(x - 6, y - 17, x - 6, y + 17)
        f.line(x - 6, y, x, y)
        f.rect(x, y - 17, 46, 34)
        f.text(x + 23, y, "≥1", 14)
        f.circle(x + 51, y, 5)
        f.line(x + 56, y, x + 78, y)
        f.text(x + 84, y, "Y", 13, anchor="start")
        return
    f.rect(x, y - h / 2, w, h)
    f.text(x + w / 2, y, sym, 14)
    ox = x + w
    if kind in ("nand", "nor", "xnor", "not"):
        f.circle(ox + 5, y, 5)
        ox += 10
    f.line(ox, y, ox + 22, y)
    f.text(ox + 28, y, "Y", 13, anchor="start")


def _iec_box(f, x, y, w, h, sym):
    f.rect(x, y, w, h)
    f.text(x + w / 2, y + h / 2, sym, 13)
    return x + w


def _table_frame(f, x, y, col_ws, row_hs):
    cx = [x]
    for w in col_ws:
        cx.append(cx[-1] + w)
    cy = [y]
    for hh in row_hs:
        cy.append(cy[-1] + hh)
    f.rect(x, y, sum(col_ws), sum(row_hs), sw=1.4)
    for i in range(1, len(col_ws)):
        f.line(cx[i], y, cx[i], cy[-1], sw=1.2)
    for j in range(1, len(row_hs)):
        f.line(x, cy[j], cx[-1], cy[j], sw=1.2)
    return cx, cy


ROWS = [
    ("与\nAND", "A·B", "and", "全 1 为 1，否则为 0"),
    ("或\nOR", "A+B", "or", "全 0 为 0，否则为 1"),
    ("非\nNOT", "A′", "not", "取反，1→0，0→1"),
]

ROWS2 = [
    ("与非\nNAND", "(AB)′", "nand", "全 1 时为 0"),
    ("或非\nNOR", "(A+B)′", "nor", "全 0 时为 1"),
    ("与或非\nAOI", "(AB+CD)′", "aoi", "两组与项再取或非"),
    ("异或\nXOR", "A⊕B", "xor", "相异为 1，相同为 0"),
    ("同或\nXNOR", "A⊙B", "xnor", "相同为 1，相异为 0"),
]


def _logic_table(rows, out_w=880, title=None):
    col_ws = [104, 150, 250, 250]
    row_h = [38] + [74] * len(rows)
    pad = 16
    f = Fig(out_w, sum(row_h) + 2 * pad + (24 if title else 0))
    cx, cy = _table_frame(f, pad, pad + (24 if title else 0), col_ws, row_h)
    heads = ["运算", "表达式", "逻辑符号（国标）", "意义"]
    for i, s in enumerate(heads):
        f.text((cx[i] + cx[i + 1]) / 2, cy[0] + 19, s, 15, bold=True)
    for r, (name, expr, kind, meaning) in enumerate(rows):
        y0, y1 = cy[r + 1], cy[r + 2]
        mid = (y0 + y1) / 2
        lines = name.split("\n")
        f.text((cx[0] + cx[1]) / 2, mid - 9, lines[0], 15)
        if len(lines) > 1:
            f.text((cx[0] + cx[1]) / 2, mid + 13, lines[1], 12, color="#555")
        f.text((cx[1] + cx[2]) / 2, mid, expr, 16)
        gate(f, (cx[2] + cx[3]) / 2 - 10, mid, kind, size=1.0)
        f.text((cx[3] + cx[4]) / 2, mid, meaning, 14)
    if title:
        f.text(out_w / 2, 18, title, 15, bold=True)
    return f


def f_logic_basic(C=Fig):
    return _logic_table(ROWS, out_w=890)


def f_logic_compound(C=Fig):
    return _logic_table(ROWS2, out_w=890)
