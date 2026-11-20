# -*- coding: utf-8 -*-
"""极简 SVG 生成器 + Pillow 预览渲染器（用于自检排版：SVG 无法在本机渲染）。

用法：
    f = Fig(760, 200)
    f.rect(10, 10, 100, 40)
    f.text(60, 30, "a1")
    f.save("xxx.svg")          # 写 SVG
    f.preview("_preview/xxx.png")  # 写一张位图预览，供人工/模型核对
"""

import os

from PIL import Image, ImageDraw, ImageFont

FONT_SVG = "SimSun, 'Microsoft YaHei', serif"
INK = "#2b2b2b"

_FONT_CACHE = {}


def _font(size):
    if size in _FONT_CACHE:
        return _FONT_CACHE[size]
    for path in (
        r"C:\Windows\Fonts\simsun.ttc",
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\arial.ttf",
    ):
        if os.path.exists(path):
            try:
                _FONT_CACHE[size] = ImageFont.truetype(path, size)
                return _FONT_CACHE[size]
            except Exception:
                pass
    _FONT_CACHE[size] = ImageFont.load_default()
    return _FONT_CACHE[size]


def _dash_coords(x1, y1, x2, y2, on=6, off=5):
    """把一条线段切成若干虚线段。"""
    dx, dy = x2 - x1, y2 - y1
    dist = (dx * dx + dy * dy) ** 0.5
    if dist == 0:
        return []
    ux, uy = dx / dist, dy / dist
    segs, pos = [], 0.0
    while pos < dist:
        end = min(pos + on, dist)
        segs.append((x1 + ux * pos, y1 + uy * pos, x1 + ux * end, y1 + uy * end))
        pos = end + off
    return segs


class Fig:
    def __init__(self, w, h, scale=1.0):
        self.w, self.h = w, h
        self.scale = scale
        self.ops = []

    # ---------------- 图元 ----------------
    def rect(self, x, y, w, h, fill="none", sw=1.3, dash=None, rx=0, stroke=None):
        self.ops.append(
            ("rect", (float(x), float(y), float(w), float(h), fill, sw, dash, rx, stroke))
        )

    def line(self, x1, y1, x2, y2, sw=1.3, dash=None):
        self.ops.append(("line", (float(x1), float(y1), float(x2), float(y2), sw, dash)))

    def arrow(self, x1, y1, x2, y2, sw=1.3, dash=None, head=8.0):
        self.ops.append(("arrow", (float(x1), float(y1), float(x2), float(y2), sw, dash, head)))

    def poly(self, pts, sw=1.3, dash=None, head=None, fill="none"):
        self.ops.append(("poly", ([tuple(map(float, p)) for p in pts], sw, dash, head, fill)))

    def text(self, x, y, s, size=17, anchor="middle", italic=False, bold=False, color=None):
        self.ops.append(
            ("text", (float(x), float(y), s, size, anchor, italic, bold, color or INK))
        )

    def circle(self, cx, cy, r, fill="none", sw=1.3):
        self.ops.append(("circle", (float(cx), float(cy), float(r), fill, sw)))

    def ellipse(self, cx, cy, rx, ry, fill="none", sw=1.3):
        self.ops.append(("ellipse", (float(cx), float(cy), float(rx), float(ry), fill, sw)))

    def sub_text(self, cx, cy, main, sub, size=17, italic=True, anchor="middle"):
        """带下标的文字，如 a₁（用两个 text 拼，避免字体缺字形）。"""
        mw = size * 0.60 * len(main)
        sw = size * 0.42 * len(sub)
        total = mw + sw
        if anchor == "middle":
            x = cx - total / 2
        elif anchor == "end":
            x = cx - total
        else:
            x = cx
        self.text(x, cy, main, size, anchor="start", italic=italic)
        self.text(x + mw, cy + size * 0.24, sub, size * 0.70, anchor="start", italic=italic)

    # ---------------- 组合图元 ----------------
    def row_cells(self, x, y, widths, h=40, labels=None, fills=None, sw=1.3, size=17):
        """一排相邻的方格，返回每个格子的 (cx, cy)。"""
        labels = labels or []
        fills = fills or {}
        centres, cx = [], x
        for i, w in enumerate(widths):
            self.rect(cx, y, w, h, fill=fills.get(i, "none"), sw=sw)
            if i < len(labels) and labels[i]:
                self.text(cx + w / 2, y + h / 2, labels[i], size=size)
            centres.append((cx + w / 2, y + h / 2, cx, cx + w))
            cx += w
        return centres, cx

    def node2(self, x, y, label, w1=44, w2=16, h=40, size=17):
        """单链表结点：数据域 + 指针域。返回 (链路起点x, 链路终点x, 中心y)。"""
        self.rect(x, y, w1, h)
        self.rect(x + w1, y, w2, h)
        self.text(x + w1 / 2, y + h / 2, label, size=size)
        return x - 0, x + w1 + w2, y + h / 2

    def table(self, x, y, col_ws, row_hs, cells, sw=1.3, size=17, header_bold=False):
        """画网格表。cells: {(row, col): str}，col_ws/row_hs 为每列宽/每行高。"""
        tot_w, tot_h = sum(col_ws), sum(row_hs)
        cx = [x]
        for w in col_ws:
            cx.append(cx[-1] + w)
        cy = [y]
        for hh in row_hs:
            cy.append(cy[-1] + hh)
        self.rect(x, y, tot_w, tot_h, sw=sw)
        for i in range(1, len(col_ws)):
            self.line(cx[i], y, cx[i], y + tot_h, sw=sw)
        for j in range(1, len(row_hs)):
            self.line(x, cy[j], x + tot_w, cy[j], sw=sw)
        for (r, c), s in cells.items():
            if s:
                self.text(
                    (cx[c] + cx[c + 1]) / 2,
                    (cy[r] + cy[r + 1]) / 2,
                    s,
                    size=size,
                    bold=(header_bold and r == 0),
                )
        return cx, cy

    # ---------------- 输出 ----------------
    def _svg(self):
        out = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}">',
            '<defs><marker id="ah" viewBox="0 0 10 10" refX="9.2" refY="5" markerWidth="6.5" '
            'markerHeight="6.5" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>',
            f'<rect x="0" y="0" width="{self.w}" height="{self.h}" fill="#ffffff"/>',
            f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-linejoin="round">',
        ]
        texts = []
        for kind, a in self.ops:
            if kind == "rect":
                x, y, w, h, fill, sw, dash, rx, stroke = a
                d = f' stroke-dasharray="{dash}"' if dash else ""
                r = f' rx="{rx}"' if rx else ""
                sc = f' stroke="{stroke}"' if stroke else ""
                out.append(
                    f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
                    f'stroke-width="{sw}" fill="{fill}"{d}{r}{sc}/>'
                )
            elif kind == "line":
                x1, y1, x2, y2, sw, dash = a
                d = f' stroke-dasharray="{dash}"' if dash else ""
                out.append(
                    f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'stroke-width="{sw}"{d}/>'
                )
            elif kind == "arrow":
                x1, y1, x2, y2, sw, dash, head = a
                d = f' stroke-dasharray="{dash}"' if dash else ""
                out.append(
                    f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'stroke-width="{sw}"{d} marker-end="url(#ah)"/>'
                )
            elif kind == "poly":
                pts, sw, dash, head, fill = a
                p = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
                d = f' stroke-dasharray="{dash}"' if dash else ""
                m = ' marker-end="url(#ah)"' if head else ""
                out.append(
                    f'<polyline points="{p}" stroke-width="{sw}" fill="{fill}"{d}{m}/>'
                )
            elif kind == "circle":
                cx, cy, r, fill, sw = a
                out.append(
                    f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
                    f'stroke-width="{sw}" fill="{fill}"/>'
                )
            elif kind == "ellipse":
                cx, cy, rx, ry, fill, sw = a
                out.append(
                    f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
                    f'stroke-width="{sw}" fill="{fill}"/>'
                )
            elif kind == "text":
                x, y, s, size, anchor, italic, bold, color = a
                ta = {"start": "start", "middle": "middle", "end": "end"}[anchor]
                it = ' font-style="italic"' if italic else ""
                bd = ' font-weight="bold"' if bold else ""
                s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                texts.append(
                    f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT_SVG}" font-size="{size}" '
                    f'text-anchor="{ta}" dominant-baseline="central" fill="{color}"{it}{bd}>{s}</text>'
                )
        out.append("</g>")
        out.extend(texts)
        out.append("</svg>")
        return "\n".join(out) + "\n"

    def save(self, path):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(self._svg())
        return path

    def preview(self, path, bg="#ffffff"):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        s = self.scale
        img = Image.new("RGB", (int(self.w * s), int(self.h * s)), bg)
        d = ImageDraw.Draw(img)
        col = "#2b2b2b"
        for kind, a in self.ops:
            if kind == "rect":
                x, y, w, h, fill, sw, dash, rx, stroke = a
                box = [x * s, y * s, (x + w) * s, (y + h) * s]
                f = None
                if fill != "none":
                    f = "#dcdcdc" if fill in ("#eee", "#e8e8e8", "#f2f2f2") else fill
                if dash:
                    for seg in (
                        (box[0], box[1], box[2], box[1]),
                        (box[2], box[1], box[2], box[3]),
                        (box[2], box[3], box[0], box[3]),
                        (box[0], box[3], box[0], box[1]),
                    ):
                        for dseg in _dash_coords(*seg):
                            d.line([c * s for c in dseg], fill=col, width=max(1, round(sw * s)))
                else:
                    d.rectangle(box, outline=col, fill=f, width=max(1, round(sw * s)))
            elif kind == "line":
                x1, y1, x2, y2, sw, dash = a
                if dash:
                    for seg in _dash_coords(x1, y1, x2, y2):
                        d.line([c * s for c in seg], fill=col, width=max(1, round(sw * s)))
                else:
                    d.line([x1 * s, y1 * s, x2 * s, y2 * s], fill=col, width=max(1, round(sw * s)))
            elif kind == "arrow":
                x1, y1, x2, y2, sw, dash, head = a
                segs = _dash_coords(x1, y1, x2, y2) if dash else [(x1, y1, x2, y2)]
                for seg in segs:
                    d.line([c * s for c in seg], fill=col, width=max(1, round(sw * s)))
                # 箭头三角
                dx, dy = x2 - x1, y2 - y1
                dist = (dx * dx + dy * dy) ** 0.5 or 1
                ux, uy = dx / dist, dy / dist
                hx, hy = x2 - ux * head, y2 - uy * head
                px, py = -uy, ux
                d.polygon(
                    [
                        (x2 * s, y2 * s),
                        ((hx + px * head * 0.38) * s, (hy + py * head * 0.38) * s),
                        ((hx - px * head * 0.38) * s, (hy - py * head * 0.38) * s),
                    ],
                    fill=col,
                )
            elif kind == "poly":
                pts, sw, dash, head, fill = a
                for i in range(len(pts) - 1):
                    (x1, y1), (x2, y2) = pts[i], pts[i + 1]
                    segs = _dash_coords(x1, y1, x2, y2) if dash else [(x1, y1, x2, y2)]
                    for seg in segs:
                        d.line([c * s for c in seg], fill=col, width=max(1, round(sw * s)))
                if head:
                    (x1, y1), (x2, y2) = pts[-2], pts[-1]
                    dx, dy = x2 - x1, y2 - y1
                    dist = (dx * dx + dy * dy) ** 0.5 or 1
                    ux, uy = dx / dist, dy / dist
                    hx, hy = x2 - ux * head, y2 - uy * head
                    px, py = -uy, ux
                    d.polygon(
                        [
                            (x2 * s, y2 * s),
                            ((hx + px * head * 0.38) * s, (hy + py * head * 0.38) * s),
                            ((hx - px * head * 0.38) * s, (hy - py * head * 0.38) * s),
                        ],
                        fill=col,
                    )
            elif kind == "circle":
                cx, cy, r, fill, sw = a
                d.ellipse(
                    [(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s],
                    outline=col,
                    fill=None if fill == "none" else fill,
                    width=max(1, round(sw * s)),
                )
            elif kind == "ellipse":
                cx, cy, rx, ry, fill, sw = a
                d.ellipse(
                    [(cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s],
                    outline=col,
                    fill=None if fill == "none" else fill,
                    width=max(1, round(sw * s)),
                )
            elif kind == "text":
                x, y, txt, size, anchor, italic, bold, color = a
                amap = {"start": "lm", "middle": "mm", "end": "rm"}
                d.text(
                    (x * s, y * s),
                    txt,
                    font=_font(max(8, round(size * s))),
                    fill=color,
                    anchor=amap[anchor],
                )
        img.save(path)
        return path
