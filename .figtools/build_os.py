# -*- coding: utf-8 -*-
"""生成 svg、位图预览，并与原截图上下拼接成对比图。"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import Image  # noqa: E402

import figs_os  # noqa: E402

PIC = r"D:\Note\计算机基础知识\操作系统\插图"
WORK = r"D:\Note\.svg_work"
SVG = os.path.join(WORK, "svg")
PRE = os.path.join(WORK, "preview")
CMP = os.path.join(WORK, "cmp")

JOBS = [
    ("进程五状态转换图", "f_states"),
    ("进程切换模型", "f_switch"),
    ("进程切换模型2", "f_switch2"),
    ("进程的上下文切换", "f_context"),
    ("批处理系统的三级调度", "f_sched3"),
    ("一对一模型", "f_one2one"),
    ("多对一模型", "f_many2one"),
    ("多对多模型", "f_many2many"),
]


def montage(name, prev_png):
    orig = Image.open(os.path.join(PIC, name + ".png")).convert("RGB")
    mine = Image.open(prev_png).convert("RGB")
    w = max(orig.width, mine.width)
    h = orig.height + mine.height + 34
    canvas = Image.new("RGB", (w, h), "#ffffff")
    canvas.paste(orig, ((w - orig.width) // 2, 0))
    canvas.paste(mine, ((w - mine.width) // 2, orig.height + 34))
    out = os.path.join(CMP, name + "_cmp.png")
    canvas.save(out)
    return out


def main():
    for d in (SVG, PRE, CMP):
        os.makedirs(d, exist_ok=True)
    names = sys.argv[1:] or [n for n, _ in JOBS]
    for name, fn in JOBS:
        if name not in names:
            continue
        fig = getattr(figs_os, fn)(figs_os.Fig)
        p = fig.save(os.path.join(SVG, name + ".svg"))
        png = fig.preview(os.path.join(PRE, name + ".png"), bg="#ffffff")
        m = montage(name, png)
        print("%-12s %5dx%-4d svg=%6d  %s" % (name, fig.w, fig.h, os.path.getsize(p), m))


if __name__ == "__main__":
    main()
