# -*- coding: utf-8 -*-
"""批量生成脚本：把每张图同时输出 SVG（自检用）与 Excalidraw 场景。"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exrender  # noqa: E402
from exkit import Exc  # noqa: E402
from svgkit import Fig  # noqa: E402

WORK = r"D:\Note\.svg_work"


def build(jobs, outdir=None, preview=True):
    """jobs: [(文件名, 函数)]；函数接受后端类作为唯一参数。"""
    outdir = outdir or os.path.join(WORK, "out")
    svgdir = os.path.join(WORK, "svg")
    prevdir = os.path.join(WORK, "preview")
    for d in (outdir, svgdir, prevdir):
        os.makedirs(d, exist_ok=True)
    result = []
    for name, fn in jobs:
        e = fn(Exc)
        p = e.save(os.path.join(outdir, name + ".excalidraw"))
        f = fn(Fig)
        f.save(os.path.join(svgdir, name + ".svg"))
        png = None
        if preview:
            png, w, h = exrender.render(p, os.path.join(prevdir, name + ".png"), scale=1.5)
        result.append((name, len(e.elements), os.path.getsize(p), png))
        print(f"{name}: {len(e.elements)} 元素, {os.path.getsize(p)}B -> {png}")
    return result
