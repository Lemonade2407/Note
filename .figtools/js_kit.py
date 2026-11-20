# -*- coding: utf-8 -*-
r"""计组插图重绘公共库：在 svgkit.Fig 之上提供常用图元与批量构建。

用法见 D:\Note\.figtools\js_README.md。
"""

import os
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import svgkit  # noqa: E402
from svgkit import Fig  # noqa: E402,F401

svgkit.FONT_SVG = "'Microsoft YaHei', 'SimHei', sans-serif"

INK = "#2b2b2b"
BOXF = "#ededed"      # 浅灰填充
BOXW = "#ffffff"      # 白填充
SOFT = "#f7f7f7"
BLUE = "#dce6f3"
GREEN = "#d9e3cc"
YELLOW = "#fdf3cf"
PINK = "#f2d7d3"
RED = "#c00000"
GRAY = "#cccccc"

PIC = r"D:\Note\计算机基础知识\计算机组成原理\插图"
WORK = r"D:\Note\.svg_work\js"

__all__ = ["Fig", "svgkit", "INK", "BOXF", "BOXW", "SOFT", "BLUE", "GREEN",
           "YELLOW", "PINK", "RED", "GRAY", "PIC", "WORK",
           "box", "plain", "shell", "dia", "cells", "row", "adown", "aright",
           "textof", "brace", "dashed", "gridbox", "wave"]


# ---------------------------------------------------------------- 图元

def box(f, x, y, w, h, lines, size=16, fill=BOXF, sw=1.5, rx=3, lh=1.35,
        bold=False, dash=None):
    """带文字（可多行，字符串或列表）的矩形。"""
    f.rect(x, y, w, h, fill=fill, sw=sw, rx=rx, dash=dash)
    if isinstance(lines, str):
        lines = [lines]
    n = len(lines)
    step = size * lh
    y0 = y + h / 2 - step * (n - 1) / 2
    for i, s in enumerate(lines):
        f.text(x + w / 2, y0 + i * step, s, size=size, bold=bold)
    return (x, y, w, h)


def plain(f, x, y, w, h, lines, size=16, sw=1.5, rx=0, lh=1.35, bold=False):
    """白底黑框矩形。"""
    return box(f, x, y, w, h, lines, size=size, fill=BOXW, sw=sw, rx=rx,
               lh=lh, bold=bold)


def shell(f, x, y, w, h, size=16, sw=1.5, rx=0, dash=None):
    """空框（无文字）。"""
    f.rect(x, y, w, h, fill=BOXW, sw=sw, rx=rx, dash=dash)


def dia(f, cx, cy, w, h, s, size=16, sw=1.5, fill=BOXW):
    """菱形判断框。"""
    pts = [(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)]
    pts.append(pts[0])
    f.poly(pts, sw=sw, fill=fill)
    if s:
        f.text(cx, cy, s, size=size)
    return (cx, cy)


def cells(f, x, y, widths, h, labels, size=15, sw=1.4, fill=BOXW, bold=False):
    """一行等高的单元格（表格一行），返回总宽度。"""
    cx = x
    for w, s in zip(widths, labels):
        f.rect(cx, y, w, h, fill=fill, sw=sw)
        if s:
            f.text(cx + w / 2, y + h / 2, s, size=size, bold=bold)
        cx += w
    return cx - x


def row(f, x, y, widths, h, labels, **kw):
    return cells(f, x, y, widths, h, labels, **kw)


def adown(f, x, y1, y2, sw=1.5, head=9):
    f.arrow(x, y1, x, y2, sw=sw, head=head)


def aright(f, x1, y, x2, sw=1.5, head=9):
    f.arrow(x1, y, x2, y, sw=sw, head=head)


def textof(f, x, y, s, size=15, anchor="middle", bold=False, color=INK):
    f.text(x, y, s, size=size, anchor=anchor, bold=bold, color=color)


def brace(f, x, y1, y2, w=12, sw=1.4, side=1):
    """竖直方括号（side=1 向右，-1 向左）。"""
    xm = x + side * w / 2
    f.poly([(x, y1), (xm, y1), (xm, y2), (x, y2)], sw=sw)
    ym = (y1 + y2) / 2
    f.line(x, y1, xm, y1, sw=sw)
    f.line(x, y2, xm, y2, sw=sw)
    f.line(xm, ym, x + side * (w + 6), ym, sw=sw)


def dashed(f, x1, y1, x2, y2, sw=1.2, dash="5,4"):
    f.line(x1, y1, x2, y2, sw=sw, dash=dash)


def gridbox(f, x, y, w, h, rows, cols, size=14, sw=1.4, fill=BOXW, head=None):
    """rows×cols 网格（第一行可作表头）。"""
    cw, ch = w / cols, h / rows
    for i in range(rows):
        for j in range(cols):
            f.rect(x + j * cw, y + i * ch, cw, ch, fill=fill, sw=sw)
            if head and i == 0 and j < len(head):
                f.text(x + j * cw + cw / 2, y + i * ch + ch / 2, head[j], size=size)
    return cw, ch


def wave(f, x0, y0, width, hi, lo, bits, sw=1.6, color=INK, dash_each=True):
    """画一条数字波形：bits 为 0/1 序列，每个码元宽度 width/len(bits)。"""
    n = len(bits)
    cw = width / n
    pts = []
    for i, b in enumerate(bits):
        y = hi if b else lo
        if not pts:
            pts.append((x0, y))
        else:
            pts.append((x0 + i * cw, pts[-1][1]))
            pts.append((x0 + i * cw, y))
    pts.append((x0 + width, pts[-1][1]))
    f.poly(pts, sw=sw)
    if dash_each:
        for i in range(n + 1):
            f.line(x0 + i * cw, lo - 6, x0 + i * cw, hi + 6, sw=0.8, dash="3,3")
    return cw


# ---------------------------------------------------------------- 构建

def _figs():
    """收集 figs_js1..figs_js9 中的 FIGS 列表。"""
    out = []
    for i in range(1, 10):
        mod = "figs_js%d" % i
        try:
            m = __import__(mod)
        except ImportError:
            continue
        for name, fn in getattr(m, "FIGS", []):
            out.append((name, fn))
    return out


def registry():
    return dict(_figs())


def build(names=None, preview=True):
    import subprocess  # noqa: F401  (保持与其它脚本一致的依赖关系)
    from PIL import Image
    svg_dir = os.path.join(WORK, "svg")
    pre_dir = os.path.join(WORK, "preview")
    cmp_dir = os.path.join(WORK, "cmp")
    for d in (svg_dir, pre_dir, cmp_dir):
        os.makedirs(d, exist_ok=True)
    reg = registry()
    todo = names or list(reg)
    done = []
    for name in todo:
        if name not in reg:
            print("!! 未找到图:", name)
            continue
        fig = reg[name](Fig)
        sp = fig.save(os.path.join(svg_dir, name + ".svg"))
        ET.parse(sp)  # 语法自检
        png = fig.preview(os.path.join(pre_dir, name + ".png"), bg="#ffffff")
        line = "%-24s %4dx%-4d %6dB" % (name, fig.w, fig.h, os.path.getsize(sp))
        orig = os.path.join(PIC, name + ".png")
        if preview and os.path.exists(orig):
            o = Image.open(orig).convert("RGB")
            m = Image.open(png).convert("RGB")
            w = max(o.width, m.width)
            canvas = Image.new("RGB", (w, o.height + m.height + 30), "#ffffff")
            canvas.paste(o, ((w - o.width) // 2, 0))
            canvas.paste(m, ((w - m.width) // 2, o.height + 30))
            cp = os.path.join(cmp_dir, name + "_cmp.png")
            canvas.save(cp)
            line += "  cmp"
        done.append(name)
        print(line)
    return done


if __name__ == "__main__":
    build(sys.argv[1:] or None)
