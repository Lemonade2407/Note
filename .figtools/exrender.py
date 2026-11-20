# -*- coding: utf-8 -*-
"""把 .excalidraw 场景用 Pillow 画出来，用于自检（本机无法渲染 Excalidraw）。"""

import json
import os

from PIL import Image, ImageDraw, ImageFont


def _font(size):
    for p in (r"C:\Windows\Fonts\simsun.ttc", r"C:\Windows\Fonts\arial.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, max(8, int(size)))
    return ImageFont.load_default()


def render(path, out_png, scale=1.6, pad=12):
    with open(path, encoding="utf-8") as fh:
        scene = json.load(fh)
    els = scene["elements"]
    xs, ys = [], []
    for e in els:
        xs += [e["x"], e["x"] + e.get("width", 0)]
        ys += [e["y"], e["y"] + e.get("height", 0)]
        if e["type"] in ("line", "arrow"):
            for px, py in e.get("points", []):
                xs.append(e["x"] + px)
                ys.append(e["y"] + py)
    minx, miny = min(xs) - pad, min(ys) - pad
    w = int((max(xs) - minx + pad) * scale)
    h = int((max(ys) - miny + pad) * scale)
    img = Image.new("RGB", (w, h), "#ffffff")
    d = ImageDraw.Draw(img)

    def T(x, y):
        return ((x - minx) * scale, (y - miny) * scale)

    for e in els:
        col = e.get("strokeColor", "#1e1e1e")
        sw = max(1, int(round(e.get("strokeWidth", 1) * scale)))
        t = e["type"]
        if t == "rectangle":
            x, y = T(e["x"], e["y"])
            d.rectangle(
                [x, y, x + e["width"] * scale, y + e["height"] * scale],
                outline=col,
                width=sw,
            )
        elif t in ("line", "arrow"):
            pts = [T(e["x"] + px, e["y"] + py) for px, py in e["points"]]
            for a, b in zip(pts, pts[1:]):
                d.line([a, b], fill=col, width=sw)
            if e.get("endArrowhead"):
                (x1, y1), (x2, y2) = pts[-2], pts[-1]
                dx, dy = x2 - x1, y2 - y1
                dist = (dx * dx + dy * dy) ** 0.5 or 1
                ux, uy = dx / dist, dy / dist
                hx, hy = x2 - ux * 9 * scale, y2 - uy * 9 * scale
                px, py = -uy, ux
                d.polygon(
                    [(x2, y2), (hx + px * 3.4 * scale, hy + py * 3.4 * scale),
                     (hx - px * 3.4 * scale, hy - py * 3.4 * scale)],
                    fill=col,
                )
        elif t == "ellipse":
            x, y = T(e["x"], e["y"])
            d.ellipse(
                [x, y, x + e["width"] * scale, y + e["height"] * scale],
                outline=col,
                width=sw,
            )
        elif t == "text":
            x, y = T(e["x"], e["y"])
            d.text(
                (x, y + e.get("height", 0) * scale * 0.5),
                e.get("text", ""),
                font=_font(e.get("fontSize", 17) * scale),
                fill=col,
                anchor="lm",
            )
    img.save(out_png)
    return out_png, w, h
