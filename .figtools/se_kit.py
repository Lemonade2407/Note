# -*- coding: utf-8 -*-
r"""软件工程导论插图重绘：复用 js_kit 的图元，只换目录与模块前缀。

构建：python se_kit.py [图名 ...]
输出：D:\Note\.svg_work\se\svg\<图名>.svg
      D:\Note\.svg_work\se\preview\<图名>.png
      D:\Note\.svg_work\se\cmp\<图名>_cmp.png   （上=原图，下=重绘）
"""

import os
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import js_kit as K  # noqa: E402
from js_kit import Fig  # noqa: E402,F401
from js_kit import (INK, BOXF, BOXW, SOFT, BLUE, GREEN, YELLOW, PINK, RED,  # noqa: E402,F401
                    GRAY, box, plain, shell, dia, cells, row, adown, aright,
                    textof, brace, dashed, gridbox, wave)

PIC = r"D:\Note\计算机基础知识\软件工程导论\图片"
WORK = r"D:\Note\.svg_work\se"


def _figs():
    out = []
    for i in range(1, 10):
        mod = "figs_se%d" % i
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
        ET.parse(sp)
        png = fig.preview(os.path.join(pre_dir, name + ".png"), bg="#ffffff")
        line = "%-22s %4dx%-4d %6dB" % (name, fig.w, fig.h, os.path.getsize(sp))
        for ext in (".png", ".jpg"):
            orig = os.path.join(PIC, name + ext)
            if os.path.exists(orig):
                o = Image.open(orig).convert("RGB")
                m = Image.open(png).convert("RGB")
                w = max(o.width, m.width)
                canvas = Image.new("RGB", (w, o.height + m.height + 30), "#ffffff")
                canvas.paste(o, ((w - o.width) // 2, 0))
                canvas.paste(m, ((w - m.width) // 2, o.height + 30))
                canvas.save(os.path.join(cmp_dir, name + "_cmp.png"))
                line += "  cmp"
                break
        done.append(name)
        print(line)
    return done


if __name__ == "__main__":
    build(sys.argv[1:] or None)
