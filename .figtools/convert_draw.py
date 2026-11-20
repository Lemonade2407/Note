# -*- coding: utf-8 -*-
"""把 Excalidraw 场景里的手绘笔迹转成 SVG（freedraw → polyline path），并出 PNG 预览。"""

import glob
import io
import json
import os
import sys

from PIL import Image, ImageDraw

SRC = r"D:\Note\.figwork\json"
OUT = r"D:\Note\.figwork\svg"
PRE = r"D:\Note\.figwork\preview"
NAMES = {
    "f00": "Moore状态图", "f01": "SR锁存器", "f02": "mealy状态图",
    "f03": "上升沿JK触发器", "f04": "上升沿T触发器", "f05": "下降沿D触发器",
    "f06": "加法器74LS283", "f07": "数值比较器74LS85", "f08": "数据选择器74LS151",
    "f09": "移位寄存器74LS194", "f10": "计数器74LS163", "f11": "译码器74LS138",
    "f12": "逻辑代数基本运算", "f13": "逻辑代数复合运算",
}
PAD = 8
LW = 1.6


def elements(scene):
    return [e for e in scene.get("elements", []) if not e.get("isDeleted")]


def points_of(e):
    if e.get("type") == "freedraw":
        return [(e["x"] + p[0], e["y"] + p[1]) for p in e["points"]]
    if e.get("type") == "line":
        return [(e["x"] + p[0], e["y"] + p[1]) for p in e["points"]]
    return []


def bbox(els):
    xs, ys = [], []
    for e in els:
        for x, y in points_of(e):
            xs.append(x)
            ys.append(y)
    if not xs:
        return 0, 0, 1, 1
    return min(xs), min(ys), max(xs), max(ys)


def to_svg(scene):
    els = elements(scene)
    x0, y0, x1, y1 = bbox(els)
    w = max(1.0, x1 - x0 + 2 * PAD)
    h = max(1.0, y1 - y0 + 2 * PAD)
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%.0f" height="%.0f" '
           'viewBox="0 0 %.0f %.0f">' % (w, h, w, h),
           '  <g fill="none" stroke="#1e1e1e" stroke-width="%s" '
           'stroke-linecap="round" stroke-linejoin="round" '
           'transform="translate(%.2f,%.2f)">' % (LW, PAD - x0, PAD - y0)]
    for e in els:
        pts = points_of(e)
        if len(pts) < 2:
            continue
        d = "M%.2f %.2f" % pts[0] + "".join(" L%.2f %.2f" % p for p in pts[1:])
        out.append('    <path d="%s"/>' % d)
    out.append("  </g>")
    out.append("</svg>")
    return "\n".join(out), (w, h, els)


def preview(els, w, h, x0, y0, path):
    s = 1.0
    img = Image.new("RGB", (int(w * s) + 1, int(h * s) + 1), "white")
    d = ImageDraw.Draw(img)
    for e in els:
        pts = [(x - x0 + PAD, y - y0 + PAD) for x, y in points_of(e)]
        if len(pts) < 2:
            continue
        d.line(pts, fill=(30, 30, 30), width=2, joint="curve")
    img.save(path)


def main():
    for d in (OUT, PRE):
        os.makedirs(d, exist_ok=True)
    for p in sorted(glob.glob(os.path.join(SRC, "f*.json"))):
        key = os.path.basename(p)[:-5]
        name = NAMES.get(key, key)
        with io.open(p, encoding="utf-8") as fh:
            scene = json.load(fh)
        svg, (w, h, els) = to_svg(scene)
        with io.open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8") as fh:
            fh.write(svg)
        x0, y0, _, _ = bbox(els)
        preview(els, w, h, x0, y0, os.path.join(PRE, name + ".png"))
        print("%s: %d 笔, %.0fx%.0f" % (name, len(els), w, h))


if __name__ == "__main__":
    main()
