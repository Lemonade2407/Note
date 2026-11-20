# -*- coding: utf-8 -*-
"""极简 Excalidraw 场景生成器，接口与 svgkit.Fig 对齐，可直接复用同一套排版代码。

保真关键：roughness=0（architect 直线）、strokeStyle solid、backgroundColor transparent、
roundness=None、fontFamily=2（Helvetica 正文体），这样画出来是教科书式的干净线条，
而不是手绘风。
"""

import json
import os
import uuid

INK = "#1e1e1e"


def _measure(s, size):
    w = 0.0
    for ch in s:
        w += size * (1.0 if ord(ch) > 0x2E80 else 0.52)
    return w


class Exc:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.elements = []

    # ---------------- 元素构造 ----------------
    def _base(self, etype, x, y, w, h, **kw):
        el = {
            "id": uuid.uuid4().hex[:16],
            "type": etype,
            "x": round(x, 2),
            "y": round(y, 2),
            "width": round(w, 2),
            "height": round(h, 2),
            "angle": 0,
            "strokeColor": kw.get("color", INK),
            "backgroundColor": kw.get("bg", "transparent"),
            "fillStyle": "solid",
            "strokeWidth": kw.get("sw", 1),
            "strokeStyle": kw.get("dash", "solid"),
            "roughness": 0,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "roundness": None,
            "seed": abs(hash((x, y, w, h))) % 2000000000,
            "version": 1,
            "versionNonce": abs(hash((etype, x, y))) % 2000000000,
            "isDeleted": False,
            "boundElements": [],
            "updated": 1,
            "link": None,
            "locked": False,
        }
        el.update(kw.get("extra", {}))
        return el

    # ---------------- 图元 ----------------
    def rect(self, x, y, w, h, fill="none", sw=1, dash=None, rx=0):
        self.elements.append(
            self._base(
                "rectangle", x, y, w, h,
                bg="transparent" if fill == "none" else fill,
                sw=sw,
                dash="dashed" if dash else "solid",
            )
        )

    def line(self, x1, y1, x2, y2, sw=1, dash=None):
        self.elements.append(
            self._base(
                "line", x1, y1, abs(x2 - x1), abs(y2 - y1),
                sw=sw,
                dash="dashed" if dash else "solid",
                extra={
                    "points": [[0, 0], [round(x2 - x1, 2), round(y2 - y1, 2)]],
                    "lastCommittedPoint": None,
                    "startBinding": None,
                    "endBinding": None,
                    "startArrowhead": None,
                    "endArrowhead": None,
                },
            )
        )

    def arrow(self, x1, y1, x2, y2, sw=1, dash=None, head=8):
        self.elements.append(
            self._base(
                "arrow", x1, y1, abs(x2 - x1), abs(y2 - y1),
                sw=sw,
                dash="dashed" if dash else "solid",
                extra={
                    "points": [[0, 0], [round(x2 - x1, 2), round(y2 - y1, 2)]],
                    "lastCommittedPoint": None,
                    "startBinding": None,
                    "endBinding": None,
                    "startArrowhead": None,
                    "endArrowhead": "arrow",
                    "elbowed": False,
                },
            )
        )

    def poly(self, pts, sw=1, dash=None, head=None, fill="none"):
        if len(pts) < 2:
            return
        x0, y0 = pts[0]
        bw = max(px for px, _ in pts) - min(px for px, _ in pts)
        bh = max(py for _, py in pts) - min(py for _, py in pts)
        self.elements.append(
            self._base(
                "line", x0, y0, bw, bh,
                sw=sw,
                dash="dashed" if dash else "solid",
                extra={
                    "points": [[0, 0]]
                    + [[round(px - x0, 2), round(py - y0, 2)] for px, py in pts[1:]],
                    "lastCommittedPoint": None,
                    "startBinding": None,
                    "endBinding": None,
                    "startArrowhead": None,
                    "endArrowhead": "arrow" if head else None,
                },
            )
        )

    def circle(self, cx, cy, r, fill="none", sw=1.3):
        self.ellipse(cx, cy, r, r, fill=fill, sw=sw)

    def ellipse(self, cx, cy, rx, ry, fill="none", sw=1.3):
        self.elements.append(
            self._base(
                "ellipse", cx - rx, cy - ry, rx * 2, ry * 2,
                bg="transparent" if fill == "none" else fill, sw=sw,
            )
        )

    def text(self, x, y, s, size=17, anchor="middle", italic=False, bold=False, color=None):
        w = _measure(s, size)
        h = size * 1.25
        if anchor == "middle":
            x0 = x - w / 2
        elif anchor == "end":
            x0 = x - w
        else:
            x0 = x
        self.elements.append(
            self._base(
                "text", x0, y - h / 2, w, h,
                color=color or INK,
                extra={
                    "text": s,
                    "originalText": s,
                    "fontSize": size,
                    "fontFamily": 2,
                    "textAlign": "left",
                    "verticalAlign": "top",
                    "containerId": None,
                    "lineHeight": 1.25,
                    "baseline": round(size * 0.8, 2),
                    "autoResize": True,
                },
            )
        )

    def sub_text(self, cx, cy, main, sub, size=17, italic=True, anchor="middle"):
        mw = size * 0.60 * len(main)
        sw = size * 0.42 * len(sub)
        total = mw + sw
        x = cx - total / 2 if anchor == "middle" else (cx - total if anchor == "end" else cx)
        self.text(x, cy, main, size, anchor="start")
        self.text(x + mw, cy + size * 0.24, sub, size * 0.70, anchor="start")

    # ---------------- 输出 ----------------
    def scene(self):
        return {
            "type": "excalidraw",
            "version": 2,
            "source": "https://github.com/excalidraw/excalidraw",
            "elements": self.elements,
            "appState": {
                "gridSize": None,
                "viewBackgroundColor": "#ffffff",
                "currentItemStrokeColor": INK,
                "currentItemFontFamily": 2,
            },
            "files": {},
        }

    def save(self, path):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(self.scene(), fh, ensure_ascii=False, indent=None, separators=(",", ":"))
        return path

    def save_md(self, path, title="Excalidraw"):
        """Obsidian Excalidraw 插件的 .excalidraw.md 包装格式（json 代码块）。"""
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        body = json.dumps(self.scene(), ensure_ascii=False, separators=(",", ":"))
        md = (
            "---\n"
            "excalidraw-plugin: parsed\n"
            "tags: [excalidraw]\n"
            "---\n"
            "\n"
            "# " + title + "\n"
            "\n"
            "```json\n"
            + body
            + "\n```\n"
        )
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(md)
        return path
