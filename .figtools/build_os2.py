# -*- coding: utf-8 -*-
"""构建 figs_os2.py 里的新增示意图：输出 svg + 预览 + 拼版。"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import Image, ImageDraw  # noqa: E402

import figs_os2  # noqa: E402

WORK = r"D:\Note\.svg_work"
SVG = os.path.join(WORK, "svg")
PRE = os.path.join(WORK, "preview")


def sheet(names, out, cols=1):
    imgs = [(n, Image.open(os.path.join(PRE, n + ".png"))) for n in names]
    w = max(i.width for _, i in imgs)
    h = sum(i.height + 26 for _, i in imgs) + 10
    cv = Image.new("RGB", (w, h), "#ffffff")
    d = ImageDraw.Draw(cv)
    y = 6
    for n, im in imgs:
        d.text((6, y + 8), n, fill="#000000")
        cv.paste(im, (0, y + 24))
        y += im.height + 26
    cv.save(out)
    return out


def main():
    for d in (SVG, PRE):
        os.makedirs(d, exist_ok=True)
    names = sys.argv[1:]
    made = []
    for name, fn in figs_os2.FLOW:
        if names and name not in names:
            continue
        fig = getattr(figs_os2, fn)(figs_os2.Fig)
        p = fig.save(os.path.join(SVG, name + ".svg"))
        fig.preview(os.path.join(PRE, name + ".png"), bg="#ffffff")
        made.append(name)
        print("%-14s %4dx%-4d %6dB" % (name, fig.w, fig.h, os.path.getsize(p)))
    if not names:
        half = (len(made) + 1) // 2
        print(sheet(made[:half], os.path.join(WORK, "sheet1.png")))
        print(sheet(made[half:], os.path.join(WORK, "sheet2.png")))


if __name__ == "__main__":
    main()
