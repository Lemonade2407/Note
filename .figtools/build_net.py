# -*- coding: utf-8 -*-
"""构建计算机网络笔记的示意图：svg + preview + 拼图。"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import Image  # noqa: E402

import figs_net  # noqa: E402

WORK = r"D:\Note\.svg_work"
SVG = os.path.join(WORK, "svg")
PRE = os.path.join(WORK, "preview")


def sheet(names, out):
    imgs = [Image.open(os.path.join(PRE, n + ".png")).convert("RGB") for n in names]
    w = max(i.width for i in imgs) + 20
    h = sum(i.height for i in imgs) + 30 * len(imgs) + 20
    canvas = Image.new("RGB", (w, h), "#ffffff")
    y = 10
    for i in imgs:
        canvas.paste(i, (10, y))
        y += i.height + 30
    canvas.save(out)
    return out


def main():
    for d in (SVG, PRE):
        os.makedirs(d, exist_ok=True)
    names = sys.argv[1:] or [n for n, _ in figs_net.FLOW]
    for name, fn in figs_net.FLOW:
        if name not in names:
            continue
        fig = fn(figs_net.svgkit.Fig)
        p = fig.save(os.path.join(SVG, name + ".svg"))
        png = fig.preview(os.path.join(PRE, name + ".png"), bg="#ffffff")
        print("%-24s %4dx%-4d svg=%6d" % (name, fig.w, fig.h, os.path.getsize(p)))
    if not sys.argv[1:]:
        allnames = [n for n, _ in figs_net.FLOW]
        print(sheet(allnames[:6], os.path.join(WORK, "netsheet1.png")))
        print(sheet(allnames[6:], os.path.join(WORK, "netsheet2.png")))


if __name__ == "__main__":
    main()
