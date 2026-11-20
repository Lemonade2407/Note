# -*- coding: utf-8 -*-
"""软件工程导论插图 SVG 重绘 —— 第 3 批（UML / 架构 / 模块 / 数据流）"""
import math

import se_kit as K
from se_kit import Fig, INK, BOXF, BOXW, BLUE, GREEN, YELLOW, PINK, RED, GRAY

DASH = "5,4"
DASH2 = "9,6"
TEAL = "#40afca"
TITLE = "#17809b"
NVY = "#1b1b8c"
GRN = "#2d6e21"
DKR = "#a52a1a"
BAR = "#d9d9d9"
PALE = "#e8eefc"


# ---------------------------------------------------------------- 通用图元

def arc(f, cx, cy, rx, ry, a0, a1, n=18, sw=2.5):
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    f.poly(pts, sw=sw)


def dbl_h(f, x1, x2, y, sw=2.6, head=18):
    f.arrow(x1, y, x2, y, sw=sw, head=head)
    f.arrow(x2, y, x1, y, sw=sw, head=head)


def diamond(f, cx, cy, w, h, fill=TEAL, sw=2.5):
    f.fpoly([(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)],
            fill=fill, sw=sw)


def cyl(f, cx, ytop, w, h, sw=2.4, fill=BOXW):
    """数据库圆柱：cx 中心，ytop 顶，w 宽，h 总高。"""
    rx, ry = w / 2, 18
    f.ellipse(cx, ytop + ry, rx, ry, fill=fill, sw=sw)
    for s in (-1, 1):
        f.line(cx + s * rx, ytop + ry, cx + s * rx, ytop + h - ry, sw=sw)
    arc(f, cx, ytop + h - ry, rx, ry, 0, 180, sw=sw)


def person(f, cx, cy, r=22, sw=2.6):
    """简笔人：头 + 肩弧，cy 为头圆心。"""
    f.circle(cx, cy, r, fill=BOXW, sw=sw)
    arc(f, cx, cy + 2.3 * r, 1.4 * r, 1.3 * r, 180, 360, sw=sw)


def tri(f, tip, ang, L=13, W=10, fill=BOXW, sw=1.4):
    """沿 ang 方向（指向 tip）的空心三角箭头。"""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    bx, by = tip[0] - ux * L, tip[1] - uy * L
    f.fpoly([tip, (bx + px * W, by + py * W), (bx - px * W, by - py * W)],
            fill=fill, sw=sw)


def header(f, title, W):
    """幻灯片页眉：双箭头 + 标题 + 校徽（坐标按 1024 宽原图实测）。"""
    for x in (46, 78):
        f.fpoly([(x, 30), (x + 46, 55), (x, 80), (x + 16, 55)], fill=TEAL, sw=1)
    f.text(150, 53, title, size=42, anchor="start", bold=True, color=TITLE)
    f.circle(765, 37, 28, fill="#2e93b5", sw=1.5)
    f.circle(765, 37, 22, fill="#ffffff", sw=1)
    f.text(765, 34, "B", size=26, color="#2e93b5", bold=True)
    f.text(765, 52, "BJUT 1960", size=5.2, color="#2e93b5", bold=True)
    f.text(806, 38, "北京工业大学", size=27, anchor="start", color="#3aa8c8", bold=True)
    f.text(806, 66, "BEIJINGUNIVERSITYOFTECHNOLOGY", size=7.6,
           anchor="start", color="#3aa8c8", bold=True)


class RFig(Fig):
    """补充：彩色描边、填充多边形、竖排（旋转 90°）文字。"""

    def fpoly(self, pts, fill=BOXW, sw=2.5, stroke=None):
        """闭合填充多边形：走原生 poly 通道，SVG 里按序绘制、文字始终在最上层。"""
        p = [tuple(map(float, q)) for q in pts]
        self.ops.append(("poly", (p + [p[0]], sw, None, False, fill)))

    def vtext(self, x, y, s, size=15, color=INK, bold=False, ang=90):
        self.ops.append(("vt", (float(x), float(y), s, size, ang, color, bold)))

    def _svg(self):
        import svgkit as _sk
        svg = super()._svg()
        extra = []
        for kind, a in self.ops:
            if kind == "vt":
                x, y, s, size, ang, color, bold = a
                bd = ' font-weight="bold"' if bold else ""
                extra.append(
                    '<text x="%.1f" y="%.1f" font-family="%s" font-size="%s" text-anchor="middle" '
                    'dominant-baseline="central" fill="%s" transform="rotate(%s %.1f %.1f)"%s>%s</text>'
                    % (x, y, _sk.FONT_SVG, size, color, ang, x, y, bd, s))
        if extra:
            svg = svg.replace("</svg>", "\n".join(extra) + "\n</svg>")
        return svg

    def preview(self, path, bg="#ffffff"):
        """自带预览：支持彩色描边、圆角、多边形填充与竖排文字。"""
        import os as _os
        from PIL import Image, ImageDraw
        import svgkit as sk
        _os.makedirs(_os.path.dirname(path) or ".", exist_ok=True)
        s = self.scale
        img = Image.new("RGB", (int(self.w * s), int(self.h * s)), bg)
        d = ImageDraw.Draw(img)

        def seg(x1, y1, x2, y2, sw, dash, col):
            if dash:
                on, off = (float(v) for v in dash.split(","))
                for q in sk._dash_coords(x1, y1, x2, y2, on, off):
                    d.line([c * s for c in q], fill=col, width=max(1, round(sw * s)))
            else:
                d.line([x1 * s, y1 * s, x2 * s, y2 * s], fill=col,
                       width=max(1, round(sw * s)))

        def head(x1, y1, x2, y2, h, col):
            dx, dy = x2 - x1, y2 - y1
            dist = (dx * dx + dy * dy) ** 0.5 or 1
            ux, uy = dx / dist, dy / dist
            hx, hy = x2 - ux * h, y2 - uy * h
            px, py = -uy, ux
            d.polygon([(x2 * s, y2 * s),
                       ((hx + px * h * 0.38) * s, (hy + py * h * 0.38) * s),
                       ((hx - px * h * 0.38) * s, (hy - py * h * 0.38) * s)], fill=col)

        for kind, a in self.ops:
            if kind == "rect":
                x, y, w, h, fill, sw, dash, rx, stroke = a
                col = stroke or "#2b2b2b"
                box = [x * s, y * s, (x + w) * s, (y + h) * s]
                f = "#dcdcdc" if fill in ("#eee", "#e8e8e8", "#f2f2f2") else (
                    fill if fill != "none" else None)
                if rx:
                    d.rounded_rectangle(box, radius=rx * s, outline=col, fill=f,
                                        width=max(1, round(sw * s)))
                elif dash:
                    for q in ((box[0], box[1], box[2], box[1]), (box[2], box[1], box[2], box[3]),
                              (box[2], box[3], box[0], box[3]), (box[0], box[3], box[0], box[1])):
                        on, off = (float(v) for v in dash.split(","))
                        for z in sk._dash_coords(q[0] / s, q[1] / s, q[2] / s, q[3] / s, on, off):
                            d.line([c * s for c in z], fill=col, width=max(1, round(sw * s)))
                else:
                    d.rectangle(box, outline=col, fill=f, width=max(1, round(sw * s)))
            elif kind == "line":
                x1, y1, x2, y2, sw, dash = a
                seg(x1, y1, x2, y2, sw, dash, "#2b2b2b")
            elif kind == "arrow":
                x1, y1, x2, y2, sw, dash, hd = a
                seg(x1, y1, x2, y2, sw, dash, "#2b2b2b")
                head(x1, y1, x2, y2, hd, "#2b2b2b")
            elif kind == "poly":
                pts, sw, dash, hd, fill = a
                if fill and fill != "none":
                    d.polygon([(p[0] * s, p[1] * s) for p in pts], fill=fill)
                for i in range(len(pts) - 1):
                    seg(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], sw, dash, "#2b2b2b")
                if hd:
                    head(pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1], hd, "#2b2b2b")
            elif kind == "circle":
                cx, cy, r, fill, sw = a
                d.ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s],
                          outline="#2b2b2b", fill=(None if fill == "none" else fill),
                          width=max(1, round(sw * s)))
            elif kind == "ellipse":
                cx, cy, rx, ry, fill, sw = a
                d.ellipse([(cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s],
                          outline="#2b2b2b", fill=(None if fill == "none" else fill),
                          width=max(1, round(sw * s)))
            elif kind == "text":
                x, y, txt, size, anchor, italic, bold, color = a
                font = sk._font(max(7, int(round(size * s))))
                anc = {"start": "lm", "middle": "mm", "end": "rm"}[anchor]
                d.text((x * s, y * s), txt, font=font, fill=color, anchor=anc)
            elif kind == "vt":
                x, y, txt, size, ang, color, bold = a
                font = sk._font(max(8, int(round(size * s))))
                tw = int(font.getlength(txt)) + 6
                th = int(size * 1.6 * s)
                tmp = Image.new("RGBA", (tw, th), (255, 255, 255, 0))
                ImageDraw.Draw(tmp).text((tw / 2, th / 2), txt, font=font,
                                         fill=color, anchor="mm")
                tmp = tmp.rotate(-ang, expand=True, resample=Image.BICUBIC)
                img.paste(tmp, (int(x * s - tmp.width / 2), int(y * s - tmp.height / 2)), tmp)
        img.save(path)
        return path


def klass(f, x, y, w, hs, cells, size=12.5, name_size=14, pad=6):
    """UML 类框：hs 为各分隔高度，cells 为每段文字（可多行）。"""
    yy = y
    for i, h in enumerate(hs):
        f.rect(x, yy, w, h, fill=BOXW, sw=1.4)
        lines = cells[i] if i < len(cells) else None
        if lines:
            if i == 0:
                for j, s in enumerate(lines):
                    f.text(x + w / 2, yy + h / 2 + (j - (len(lines) - 1) / 2) * 17, s,
                           size=name_size)
            else:
                for j, s in enumerate(lines):
                    f.text(x + pad, yy + 13 + j * 17, s, size=size, anchor="start")
        yy += h


# ---------------------------------------------------------------- 设计流程

def f_design_flow(Fig):
    f = RFig(2744, 1488)
    S = 54
    f.rect(432, 276, 456, 188, fill=TEAL, sw=2.5)
    f.text(660, 370, "架构设计", size=58, bold=True)
    f.rect(1444, 764, 456, 188, fill=TEAL, sw=2.5)
    f.text(1672, 858, "详细设计", size=58, bold=True)
    diamond(f, 1674, 370, 524, 276)
    f.text(1674, 370, "评审", size=58, bold=True)
    diamond(f, 1670, 1308, 516, 280)
    f.text(1670, 1308, "评审", size=58, bold=True)

    f.text(165, 115, "需求规格", size=S, bold=True)
    f.text(165, 195, "说明", size=S, bold=True)
    f.text(770, 205, "软件架构", size=S, bold=True)
    f.text(1155, 60, "退改", size=S, bold=True)
    f.text(1815, 620, "通过", size=S, bold=True)
    f.text(1875, 1075, "构件规格", size=S, bold=True)
    f.text(1180, 1040, "退改", size=S, bold=True)
    f.text(2270, 1385, "通过", size=S, bold=True)
    f.text(2600, 1155, "软件设计", size=S, bold=True)
    f.text(2600, 1235, "说明书", size=S, bold=True)

    f.arrow(48, 370, 432, 370, sw=4, head=26)
    f.arrow(888, 370, 1412, 370, sw=4, head=26)
    f.poly([(1674, 232), (1674, 108), (640, 108), (640, 276)], sw=4, head=24)
    f.arrow(1674, 508, 1674, 764, sw=4, head=26)
    f.arrow(1672, 952, 1670, 1166, sw=4, head=26)
    f.poly([(1412, 1308), (1340, 1308), (1340, 860), (1444, 860)], sw=4, head=24)
    f.arrow(1928, 1308, 2390, 1308, sw=4, head=26)
    return f


# ---------------------------------------------------------------- 分层架构模式

def f_layers(Fig):
    f = RFig(1279, 1154)
    f.rect(102, 85, 625, 174, fill=BOXW, sw=3.4, stroke=DKR)
    f.text(414, 172, "Layer n", size=74, color=DKR)
    f.rect(102, 421, 622, 173, fill=BOXW, sw=3.4, stroke=GRN)
    f.text(413, 507, "Layer n-1", size=74, color=GRN)
    f.rect(102, 923, 625, 174, fill=BOXW, sw=3.4, stroke=NVY)
    f.text(414, 1010, "Layer 1", size=74, color=NVY)

    f.arrow(414, 259, 414, 421, sw=3.4, head=22)
    f.line(414, 594, 414, 898, sw=3.4, dash="12,9")
    f.fpoly([(414, 923), (400, 894), (428, 894)], fill=INK, sw=1)

    for i, s in enumerate(["UI展示层", "应用层", "业务层", "数据层"]):
        y = 346 + i * 127
        f.circle(825, y, 10, fill=INK, sw=1)
        f.text(895, y, s, size=66, anchor="start")
    return f


# ---------------------------------------------------------------- 体系结构设计

def f_arch_design(Fig):
    f = RFig(1769, 1212)
    S = 46
    f.rect(525, 459, 600, 301, fill=BOXW, sw=3)
    f.text(825, 600, "目标系统", size=S)
    for (x, y) in ((614, 113), (884, 113)):
        f.rect(x, y, 151, 142, fill=BOXW, sw=3)
        f.text(x + 75, y + 44, "上级", size=S)
        f.text(x + 75, y + 100, "系统", size=S)
    for (x, y) in ((614, 963), (884, 963)):
        f.rect(x, y, 151, 143, fill=BOXW, sw=3)
        f.text(x + 75, y + 45, "下级", size=S)
        f.text(x + 75, y + 101, "系统", size=S)
    f.rect(119, 499, 152, 72, fill=BOXW, sw=3)
    f.text(195, 535, "人", size=S)
    f.rect(119, 639, 152, 89, fill=BOXW, sw=3)
    f.text(195, 684, "硬件", size=S)
    for y in (499, 632):
        f.rect(1363, y, 242, 72, fill=BOXW, sw=3)
        f.text(1484, y + 36, "同级系统", size=S)

    for (x, y, w, h) in ((614, 441, 151, 39), (884, 441, 151, 39),
                         (614, 736, 151, 39), (884, 736, 151, 39),
                         (513, 496, 28, 77), (513, 646, 28, 77),
                         (1113, 496, 27, 77), (1113, 630, 27, 77)):
        f.rect(x, y, w, h, fill=BAR, sw=2.6)

    f.arrow(689, 255, 689, 441, sw=2.8, head=18)
    f.arrow(959, 255, 959, 441, sw=2.8, head=18)
    f.arrow(689, 775, 689, 963, sw=2.8, head=18)
    f.arrow(959, 775, 959, 963, sw=2.8, head=18)
    dbl_h(f, 271, 513, 535, sw=2.8, head=18)
    dbl_h(f, 271, 513, 684, sw=2.8, head=18)
    dbl_h(f, 1140, 1363, 535, sw=2.8, head=18)
    dbl_h(f, 1140, 1363, 669, sw=2.8, head=18)

    f.text(568, 340, "调用", size=44)
    f.text(352, 505, "使用", size=44)
    f.text(1245, 505, "使用", size=44)
    f.text(1024, 822, "调用", size=44)
    f.poly([(1035, 441), (1183, 236), (1259, 236)], sw=2.6)
    f.text(1315, 236, "接口", size=44)
    return f


# ---------------------------------------------------------------- 事件驱动

def f_event(Fig):
    f = RFig(1813, 1034)
    S = 56
    rrect(f, 353, 84, 400, 174, 22, DKR, 3.4)
    f.text(553, 173, "Source 1", size=S, color=DKR)
    rrect(f, 950, 84, 405, 174, 22, DKR, 3.4)
    f.text(1153, 173, "Source 2", size=S, color=DKR)

    f.rect(123, 424, 1646, 224, fill=BOXW, sw=2.6)
    f.rect(292, 464, 519, 143, fill=BOXW, sw=3.4, stroke=NVY)
    f.text(551, 536, "Channel 1", size=S, color=NVY)
    f.rect(890, 464, 520, 143, fill=BOXW, sw=3.4, stroke=NVY)
    f.text(1150, 536, "Channel 2", size=S, color=NVY)
    f.text(1660, 536, "Bus", size=50)

    rrect(f, 351, 786, 403, 166, 22, GRN, 3.4)
    f.text(551, 871, "Listener 1", size=50, color=GRN)
    rrect(f, 949, 783, 403, 167, 22, GRN, 3.4)
    f.text(1150, 868, "Listener 2", size=50, color=GRN)

    f.arrow(551, 258, 551, 462, sw=3.6, head=20)
    f.arrow(1150, 258, 1150, 462, sw=3.6, head=20)
    f.arrow(551, 607, 551, 784, sw=3.6, head=20)
    f.arrow(1151, 607, 1151, 781, sw=3.6, head=20)
    f.arrow(1048, 570, 668, 774, sw=3.6, head=20)
    return f


def rrect(f, x, y, w, h, r, stroke, sw):
    """圆角矩形（原生 rect + rx，SVG/预览一致）。"""
    f.rect(x, y, w, h, fill=BOXW, sw=sw, rx=r, stroke=stroke)


# ---------------------------------------------------------------- 微服务模式

def f_micro(Fig):
    f = RFig(2169, 1002)
    f.rect(78, 48, 392, 852, fill=BOXW, sw=3, dash="16,11")
    f.text(240, 106, "Client Apps", size=48, bold=True)
    f.rect(520, 45, 1590, 855, fill=BOXW, sw=3, dash="16,11")
    f.text(1240, 106, "Microservices", size=50, bold=True)

    person(f, 272, 300, r=26)
    f.rect(270, 400, 135, 100, fill=BOXW, sw=3, rx=14)
    f.text(337, 452, "Web", size=42, bold=True)
    person(f, 250, 620, r=26)
    f.rect(280, 745, 125, 100, fill=BOXW, sw=3, rx=14)
    f.text(342, 797, "Mobile", size=38, bold=True)

    svc = [("Catalog", 148), ("Shopping", 350), ("Discount", 550), ("Ordering", 750)]
    for name, y in svc:
        f.rect(1092, y, 342, 178, fill=PALE, sw=2.6, stroke="#5a7ac8")
        if name == "Shopping":
            f.text(1263, y + 64, "Shopping", size=50, bold=True)
            f.text(1263, y + 114, "Cart", size=50, bold=True)
        else:
            f.text(1263, y + 89, name, size=50, bold=True)

    for name, y in svc:
        cyl(f, 1697, y - 5, 102, 190, sw=2.4, fill="#fbf2f1")
        f.text(1697, y + 104, "DB", size=40, bold=True, color=DKR)
        f.arrow(1436, y + 89, 1644, y + 89, sw=3, head=18)

    f.arrow(405, 430, 1090, 200, sw=2.6, head=18)
    f.arrow(405, 458, 1090, 432, sw=2.6, head=18)
    f.arrow(405, 480, 1090, 830, sw=2.6, head=18)
    f.arrow(405, 775, 1090, 452, sw=2.6, head=18)
    f.arrow(405, 800, 1090, 640, sw=2.6, head=18)
    return f


# ---------------------------------------------------------------- 类图

def f_class(Fig):
    f = RFig(1024, 724)
    header(f, "建立对象模型", 1024)
    f.rect(38, 125, 944, 563, fill="#f2f2f2", sw=0)

    # 类框
    klass(f, 411, 131, 176, [33, 33, 34], [["动物"], ["生命"], ["新陈代谢(氧气，水：void)"]])
    klass(f, 255, 180, 81, [33, 26, 27], [["氧气"], [], []])
    klass(f, 255, 297, 81, [33, 31, 22], [["水"], [], []])
    klass(f, 441, 268, 136, [33, 60, 30], [["鸟"], ["羽毛", "有角质喙没有牙齿"], []])
    klass(f, 665, 297, 81, [33, 31, 22], [["翅膀"], [], []])
    klass(f, 80, 435, 116, [32, 26, 56], [["大雁群"], [], ["排人字()", "排一字()"]])
    klass(f, 275, 444, 114, [32, 26, 34], [["大雁"], [], ["飞行()"]])
    klass(f, 441, 444, 114, [32, 26, 34], [["鸭子"], [], ["下蛋()"]])
    klass(f, 616, 444, 114, [32, 26, 34], [["企鹅"], [], ["下蛋()"]])
    klass(f, 811, 444, 81, [32, 26, 28], [["气候"], [], []])
    klass(f, 450, 561, 81, [33, 26, 28], [["唐老鸭"], [], []])
    klass(f, 636, 561, 113, [44, 25, 48],
          [["<<interface>>", "表达"], [], ["说人话()", "说鸭话()"]], size=12)

    # 泛化
    f.line(510, 268, 510, 246, sw=1.4)
    tri(f, (510, 231), -90, L=15, W=12)
    for (x1, y1, tip) in ((330, 444, (437, 391)), (498, 444, (510, 391)), (673, 444, (583, 391))):
        ang = math.degrees(math.atan2(tip[1] - y1, tip[0] - x1))
        f.line(x1, y1, tip[0] - math.cos(math.radians(ang)) * 14,
               tip[1] - math.sin(math.radians(ang)) * 14, sw=1.4)
        tri(f, tip, ang, L=15, W=12)
    f.line(490, 561, 490, 552, sw=1.4)
    tri(f, (490, 536), -90, L=15, W=12)

    # 组合：鸟 1 -- 2 翅膀
    f.line(601, 337, 665, 337, sw=1.4)
    f.fpoly([(577, 337), (589, 329), (601, 337), (589, 345)], fill=INK, sw=1)
    f.text(606, 317, "1", size=13)
    f.text(641, 313, "2", size=13)

    # 聚合：大雁群 1 -- 0..* 大雁
    f.line(218, 493, 275, 493, sw=1.4)
    f.fpoly([(196, 493), (207, 486), (218, 493), (207, 500)], fill=BOXW, sw=1.4)
    f.text(215, 475, "1", size=13)
    f.text(248, 475, "0..*", size=13)

    # 关联：企鹅 1 -- 1 气候
    f.line(730, 483, 811, 483, sw=1.4)
    f.text(752, 467, "1", size=13)
    f.text(790, 467, "1", size=13)

    # 实现：唐老鸭 .. 表达
    f.line(531, 600, 626, 600, sw=1.4, dash=DASH)
    tri(f, (636, 600), 0, L=12, W=9)

    # 依赖：鸟 .. 氧气 / 水
    f.line(441, 300, 342, 268, sw=1.4, dash=DASH)
    tri(f, (337, 265), 197, L=10, W=8)
    f.line(441, 352, 342, 352, sw=1.4, dash=DASH)
    tri(f, (337, 352), 180, L=10, W=8)
    f.text(588, 588, "<<realize>>", size=11)

    # 图例
    f.rect(822, 88, 146, 312, fill=BOXW, sw=1.2)
    legend = ["依赖（Dependency）", "关联（Association）", "聚合（Aggregation）",
              "组合（Composition）", "泛化（Generalization）", "实现（Realization）"]
    for i, s in enumerate(legend):
        y = 88 + i * 52
        if i:
            f.line(822, y, 968, y, sw=1)
        f.text(828, y + 18, s, size=11, anchor="start")
        sy = y + 38
        if i == 0:
            f.line(833, sy, 912, sy, sw=1.2, dash="4,3")
            tri(f, (918, sy), 0, L=8, W=6, sw=1.1)
        elif i == 1:
            f.line(833, sy, 880, sy, sw=1.4)
        elif i == 2:
            f.fpoly([(833, sy), (843, sy - 5), (853, sy), (843, sy + 5)], fill=BOXW, sw=1.2)
            f.line(853, sy, 880, sy, sw=1.4)
        elif i == 3:
            f.fpoly([(833, sy), (843, sy - 5), (853, sy), (843, sy + 5)], fill=INK, sw=1)
            f.line(853, sy, 880, sy, sw=1.4)
        elif i == 4:
            f.line(833, sy, 872, sy, sw=1.4)
            tri(f, (880, sy), 0, L=9, W=7, sw=1.1)
        else:
            f.line(833, sy, 872, sy, sw=1.2, dash="4,3")
            tri(f, (880, sy), 0, L=9, W=7, sw=1.1)
    return f


# ---------------------------------------------------------------- 顺序图

def f_seq(Fig):
    f = RFig(1024, 724)
    header(f, "建立交互模型", 1024)
    f.text(120, 190, "顺序图-还书：", size=21, anchor="start", bold=True)

    # 参与者
    f.circle(157, 245, 14, fill=BOXW, sw=1.4)
    f.line(157, 259, 157, 300, sw=1.4)
    f.line(140, 272, 174, 272, sw=1.4)
    f.line(157, 300, 140, 325, sw=1.4)
    f.line(157, 300, 174, 325, sw=1.4)
    f.text(157, 367, "读者", size=13)

    objs = [(273, 104, "还书Form", 325), (473, 100, "系统Server", 523),
            (650, 103, "借阅Object", 701), (767, 123, "单本图书Object", 828)]
    for (x, w, s, cx) in objs:
        f.rect(x, 293, w, 44, fill=BOXW, sw=1.4)
        f.text(x + w / 2, 315, s, size=13)
        f.line(cx, 337, cx, 663, sw=1.2, dash=DASH)
    f.line(157, 378, 157, 663, sw=1.2, dash=DASH)

    # 激活条
    for (x, y1, y2) in ((313, 400, 600), (513, 393, 593), (699, 463, 490),
                        (820, 517, 583), (150, 390, 417), (150, 593, 617)):
        f.rect(x, y1, 17, y2 - y1, fill=BOXW, sw=1.3)

    msgs = [
        (167, 313, 420, "1.扫描图书条码", False),
        (330, 513, 420, "2.检查是否超期未交罚款", False),
        (513, 330, 457, "3.检查通过", True),
        (530, 699, 478, "4.修改借阅信息为已还", False),
        (699, 530, 515, "5.返回成功", True),
        (530, 820, 552, "6.修改图书状态为未借出", False),
        (820, 700, 593, "7.返回成功", True),
        (513, 330, 610, "8.显示还书信息", False),
        (313, 167, 623, "9.还书信息", False),
    ]
    for (x1, x2, y, s, dashed) in msgs:
        f.line(x1, y, x2, y, sw=1.3, dash=(DASH if dashed else None))
        tri(f, (x2, y), 180 if x2 < x1 else 0, L=9, W=7, fill=INK, sw=1)
        f.text(min(x1, x2) + 6, y - 12, s, size=13, anchor="start")
    return f


# ---------------------------------------------------------------- 活动图

def f_activity(Fig):
    f = RFig(1024, 724)
    header(f, "建立交互模型", 1024)
    f.text(130, 130, "活动图-还书", size=22, anchor="start", bold=True)

    f.rect(195, 201, 659, 423, fill=BOXW, sw=1.4)
    f.line(195, 240, 854, 240, sw=1.4)
    for x in (333, 530, 649):
        f.line(x, 201, x, 624, sw=1.4)
    f.text(263, 212, "用户接口", size=12)
    f.text(263, 231, "（FormObject）", size=12)
    f.text(431, 221, "业务逻辑接口（ControlObject）", size=12)
    f.text(589, 212, "第三方支付", size=12)
    f.text(589, 231, "接口（Payment）", size=12)
    f.text(751, 221, "数据库接口（DB）", size=12)

    # 起点
    f.circle(214, 267, 12, fill=INK, sw=1)
    rrect(f, 246, 250, 87, 37, 17, INK, 1.4)
    f.text(289, 260, "扫描图书", size=11)
    f.text(289, 277, "条形码", size=11)
    rrect(f, 361, 250, 147, 37, 17, INK, 1.4)
    f.text(434, 269, "检查是否超期未交罚款", size=11)

    f.fpoly([(453, 318), (471, 335), (453, 352), (435, 335)], fill=BOXW, sw=1.4)
    f.text(484, 326, "否", size=12)
    f.text(442, 368, "是", size=12)

    rrect(f, 386, 421, 94, 35, 17, INK, 1.4)
    f.text(433, 439, "计算罚款金额", size=11)
    rrect(f, 555, 421, 56, 35, 17, INK, 1.4)
    f.text(583, 439, "支付罚款", size=11)

    rrect(f, 707, 288, 96, 43, 20, INK, 1.4)
    f.text(755, 301, "修改借阅信息", size=11)
    f.text(755, 319, "为已还书", size=11)
    rrect(f, 707, 346, 96, 46, 20, INK, 1.4)
    f.text(755, 360, "修改图书状态", size=11)
    f.text(755, 379, "为未借出", size=11)
    rrect(f, 715, 422, 90, 45, 20, INK, 1.4)
    f.text(760, 435, "修改借阅信息", size=11)
    f.text(760, 454, "为已交罚款", size=11)

    rrect(f, 208, 471, 91, 33, 16, INK, 1.4)
    f.text(253, 488, "显示还书信息", size=11)
    rrect(f, 214, 527, 78, 32, 16, INK, 1.4)
    f.text(253, 544, "退出", size=11)
    f.circle(249, 590, 13, fill=BOXW, sw=1.4)
    f.circle(249, 590, 7, fill=INK, sw=1)

    # 汇合/分叉
    f.rect(671, 305, 7, 66, fill="#8c8c8c", sw=1)
    f.rect(836, 305, 7, 66, fill="#8c8c8c", sw=1)

    f.arrow(226, 267, 244, 267, sw=1.3, head=8)
    f.arrow(333, 267, 359, 267, sw=1.3, head=8)
    f.arrow(453, 287, 453, 316, sw=1.3, head=8)
    f.arrow(453, 352, 453, 419, sw=1.3, head=8)
    f.arrow(480, 438, 553, 438, sw=1.3, head=8)
    f.arrow(611, 438, 713, 438, sw=1.3, head=8)
    f.arrow(471, 335, 669, 335, sw=1.3, head=8)
    f.line(674, 330, 705, 309, sw=1.3)
    tri(f, (707, 308), math.degrees(math.atan2(309 - 330, 705 - 674)), L=9, W=7, fill=INK, sw=1)
    f.line(674, 344, 705, 369, sw=1.3)
    tri(f, (707, 370), math.degrees(math.atan2(370 - 344, 705 - 674)), L=9, W=7, fill=INK, sw=1)
    f.line(803, 309, 834, 322, sw=1.3)
    tri(f, (836, 322), math.degrees(math.atan2(322 - 309, 834 - 803)), L=9, W=7, fill=INK, sw=1)
    f.line(803, 369, 834, 355, sw=1.3)
    tri(f, (836, 355), math.degrees(math.atan2(355 - 369, 834 - 803)), L=9, W=7, fill=INK, sw=1)
    # 合流后 → 显示还书信息
    f.poly([(843, 336), (846, 336), (846, 484), (303, 484)], sw=1.3, head=8)
    # 已交罚款返回
    f.poly([(756, 422), (756, 406), (680, 406)], sw=1.3)
    f.poly([(653, 406), (653, 338), (669, 338)], sw=1.3)
    f.line(680, 406, 653, 406, sw=1.3)
    f.arrow(253, 504, 253, 525, sw=1.3, head=8)
    f.arrow(253, 559, 253, 577, sw=1.3, head=8)
    return f


# ---------------------------------------------------------------- 功能模块图

def f_modchart(Fig):
    f = RFig(1863, 947)
    BW, BH = 94, 60
    pos = {
        "M": (856, 47), "A": (565, 214), "B": (856, 214), "C": (1150, 214),
        "D": (475, 381), "E": (656, 381), "K": (856, 381), "L": (1059, 381), "N": (1240, 381),
        "F": (382, 548), "G": (565, 548), "H": (746, 548),
        "P": (1057, 548), "Q": (1194, 548), "R": (1331, 548), "S": (1467, 548),
        "I": (565, 717), "J": (745, 717), "T": (1263, 717),
    }
    edges = [("M", "A"), ("M", "B"), ("M", "C"), ("A", "D"), ("A", "E"), ("B", "K"),
             ("C", "L"), ("C", "N"), ("D", "F"), ("D", "G"), ("E", "G"), ("E", "H"),
             ("N", "P"), ("N", "Q"), ("N", "R"), ("N", "S"),
             ("F", "I"), ("G", "I"), ("H", "I"), ("H", "J"),
             ("P", "T"), ("Q", "T"), ("R", "T"), ("S", "T")]

    def edge(p, q):
        (x1, y1), (x2, y2) = p, q
        # 从父框底边中点沿直线到子框顶边中点
        ax, ay = x1 + BW / 2, y1 + BH
        bx, by = x2 + BW / 2, y2
        if abs(bx - ax) < 3:
            f.line(ax, ay, bx, by, sw=2.6)
            f.arrow(ax, ay, bx, by, sw=2.6, head=16)
        else:
            f.line(ax, ay, bx, by, sw=2.6)
            f.arrow(ax, ay, bx, by, sw=2.6, head=16)

    for a, b in edges:
        edge(pos[a], pos[b])
    for k, (x, y) in pos.items():
        f.rect(x, y, BW, BH, fill=BOXW, sw=2.6)
        f.text(x + BW / 2, y + BH / 2, k, size=42)

    # 扇出标记
    arc(f, 790, 140, 15, 15, 90, 270, sw=2.6)
    arc(f, 1037, 140, 15, 15, 270, 450, sw=2.6)
    f.line(790, 155, 1037, 155, sw=2.6)
    f.line(1052, 140, 1352, 152, sw=2.6)
    f.text(1362, 150, "扇出", size=32, anchor="start")
    # 扇入标记
    arc(f, 1186, 670, 15, 15, 90, 270, sw=2.6)
    arc(f, 1419, 670, 15, 15, 270, 450, sw=2.6)
    f.line(1186, 685, 1419, 685, sw=2.6)
    f.line(1434, 672, 1630, 704, sw=2.6)
    f.text(1640, 706, "扇入", size=32, anchor="start")

    # 深度（纵向双箭头）
    f.arrow(186, 48, 186, 786, sw=2.6, head=16)
    f.arrow(186, 786, 186, 48, sw=2.6, head=16)
    f.line(161, 48, 210, 48, sw=2.6)
    f.line(161, 786, 210, 786, sw=2.6)
    f.vtext(150, 400, "深度", size=32)
    # 宽度（横向双箭头）
    f.arrow(383, 861, 1552, 861, sw=2.6, head=16)
    f.arrow(1552, 861, 383, 861, sw=2.6, head=16)
    f.line(383, 834, 383, 887, sw=2.6)
    f.line(1552, 834, 1552, 887, sw=2.6)
    f.text(905, 826, "宽度", size=32)

    # 主宰 / 从属 细长箭头
    def curved_arrow(x0, y0, x1, y1, bend, tip, halfw, label, lx, ly, hw=40):
        pts = []
        for i in range(9):
            t = i / 8.0
            x = x0 + (x1 - x0) * t + bend * (4 * t * (1 - t))
            y = y0 + (y1 - y0) * t
            pts.append((x, y))
        left = [(x - halfw, y) for x, y in pts]
        right = [(x + halfw, y) for x, y in pts]
        poly = left + [(x1 - hw, y1), tip, (x1 + hw, y1)] + right[::-1]
        f.fpoly(poly, fill=BOXW, sw=2.6)
        f.vtext(lx, ly, label, size=32)

    curved_arrow(352, 96, 316, 500, -14, (309, 614), 10, "主宰", 390, 348, 46)
    curved_arrow(1672, 604, 1696, 268, 12, (1694, 152), 10, "从属", 1782, 430, 46)
    return f


# ---------------------------------------------------------------- 功能模块设计

MODDESIGN = [
    # (x, y, w, h, text, 竖排?)
    (104, 277, 42, 270, "借书事务", 1),
    (159, 277, 42, 270, "续借事务", 1),
    (214, 277, 41, 270, "还书事务", 1),
    (268, 277, 42, 270, "读者查询事务", 1),
    (323, 277, 42, 270, "管理员查询事务", 1),
    (379, 369, 38, 217, "输入读者号", 1),
    (431, 369, 40, 230, "超期检查", 1),
    (522, 369, 42, 230, "借书量检查", 1),
    (581, 369, 41, 240, "输入图书条码号", 1),
    (632, 369, 38, 412, "生成借阅信息修改图书状态", 1),
    (680, 369, 42, 240, "显示借阅信息", 1),
    (734, 369, 42, 240, "选择续借图书", 1),
    (786, 369, 46, 240, "写入续借信息", 1),
    (842, 369, 42, 240, "显示续借信息", 1),
    (900, 369, 42, 268, "输入图书条码号", 1),
    (954, 369, 42, 345, "检查是否超期未交罚款", 1),
    (1062, 369, 41, 173, "交款处理", 1),
    (1168, 369, 41, 412, "记录还书信息修改图书状态", 1),
    (1222, 369, 41, 211, "显示还书信息", 1),
    (1276, 372, 41, 292, "查询读者个人信息", 1),
    (1329, 377, 42, 287, "查询个人借阅信息", 1),
    (1390, 377, 45, 287, "查询个人罚款信息", 1),
    (1450, 525, 43, 205, "按书号查询", 1),
    (1515, 529, 43, 201, "按作者查询", 1),
    (1579, 534, 42, 202, "按书名查询", 1),
    (1641, 533, 41, 203, "按类别查询", 1),
    (1696, 532, 41, 239, "按读者号查询", 1),
    (1754, 534, 41, 237, "按身份证号查询", 1),
    (1805, 541, 42, 237, "按书号查询", 1),
    (1859, 539, 42, 239, "查询超期记录", 1),
    (1916, 541, 44, 237, "按读者号查询", 1),
    (1969, 385, 41, 243, "查询罚款信息", 1),
    (2024, 541, 40, 208, "按日期统计", 1),
    (2075, 544, 41, 205, "按书号统计", 1),
    (1004, 579, 42, 231, "计算罚款金额", 1),
    (1063, 580, 40, 230, "支付罚款", 1),
    (1104, 581, 41, 227, "记录已交罚款", 1),
    (406, 646, 39, 384, "检验是否有超期未还图书", 1),
    (452, 646, 41, 231, "显示超期信息", 1),
    (502, 646, 38, 245, "验证借书量上限", 1),
    (551, 644, 39, 290, "显示无法借阅原因", 1),
]

MODTOP = [
    (601, 44, 216, 58, ("图书借阅系统",)),
    (153, 159, 162, 57, ("输入事务",)),
    (1099, 159, 158, 57, ("调度",)),
    (497, 262, 110, 68, ("借书",)),
    (754, 262, 109, 68, ("续借",)),
    (1040, 262, 110, 68, ("还书",)),
    (1352, 268, 145, 67, ("读者的", "信息查询")),
    (1809, 268, 141, 67, ("管理员的", "信息查询")),
    (1466, 377, 200, 86, ("查询图书信息",)),
    (1687, 383, 108, 96, ("查询读", "者信息")),
    (1821, 383, 117, 96, ("查询借", "阅信息")),
    (2019, 386, 100, 96, ("统计借", "阅信息")),
]


def f_moddesign(Fig):
    f = RFig(2173, 1054)
    for (x, y, w, h, lines) in MODTOP:
        f.rect(x, y, w, h, fill=BOXW, sw=1.6)
        if len(lines) == 1:
            f.text(x + w / 2, y + h / 2, lines[0], size=30)
        else:
            for i, s in enumerate(lines):
                f.text(x + w / 2, y + h / 2 + (i - 0.5) * 27, s, size=26)

    for (x, y, w, h, s, vert) in MODDESIGN:
        f.rect(x, y, w, h, fill=BOXW, sw=1.6)
        f.vtext(x + w / 2, y + h / 2, s, size=27)

    def bus(px, py, kids, by):
        f.line(px, py, px, by, sw=1.6)
        f.line(kids[0], by, kids[-1], by, sw=1.6)
        for kx in kids:
            cand = [(r[1], r[2]) for r in MODDESIGN if abs(r[0] + r[2] / 2 - kx) < 4]
            cand += [(r[1], r[2]) for r in MODTOP if abs(r[0] + r[2] / 2 - kx) < 4]
            below = [c[0] for c in cand if c[0] > by + 2]
            ty = min(below) if below else by
            f.line(kx, by, kx, ty, sw=1.6)

    kids_y = {r[0] + r[2] / 2: r[1] for r in MODDESIGN}
    # 一级
    f.line(709, 102, 709, 128, sw=1.6)
    f.line(234, 128, 1178, 128, sw=1.6)
    f.line(234, 128, 234, 159, sw=1.6)
    f.line(1178, 128, 1178, 159, sw=1.6)
    # 输入事务 → 5 个事务
    f.line(234, 216, 234, 250, sw=1.6)
    f.line(125, 250, 344, 250, sw=1.6)
    for x in (125, 180, 234, 289, 344):
        f.line(x, 250, x, 277, sw=1.6)
    # 调度 → 5 个功能
    f.line(1178, 216, 1178, 242, sw=1.6)
    f.line(552, 242, 1879, 242, sw=1.6)
    for x, y in ((552, 262), (808, 262), (1095, 262), (1424, 268), (1879, 268)):
        f.line(x, 242, x, y, sw=1.6)
    # 借书
    bus(552, 330, [398, 451, 543, 601, 651, 701], 345)
    # 续借
    bus(808, 330, [755, 809, 863], 345)
    # 还书
    bus(1095, 330, [921, 975, 1083, 1189, 1243], 350)
    # 读者的信息查询
    bus(1424, 335, [1296, 1350, 1412], 352)
    # 管理员的信息查询
    bus(1879, 335, [1566, 1741, 1879, 1989, 2069], 355)
    # 二级横向功能
    bus(1566, 463, [1471, 1536, 1600, 1662], 492)
    bus(1741, 479, [1716, 1774], 505)
    bus(1879, 479, [1826, 1880, 1938], 512)
    bus(2069, 482, [2044, 2095], 512)
    # 交款处理
    bus(1083, 542, [1025, 1083, 1124], 562)
    # 超期检查 / 借书量检查
    bus(451, 599, [425, 472], 622)
    bus(543, 599, [521, 570], 622)
    return f


def f_dfd(Fig):
    """数据流图：加工(椭圆+编号弦)、外部实体(矩形)、数据存储(双横线)。"""
    f = RFig(2013, 790)
    INK2 = "#2b2b2b"

    def proc(cx, cy, rx, ry, y0, num, rows):
        f.ellipse(cx, cy, rx, ry, fill=BOXW, sw=1.6)
        k = max(0.0, 1 - ((y0 - cy) / ry) ** 2) ** 0.5
        hw = rx * k
        f.line(cx - hw, y0, cx + hw, y0, sw=1.3)
        f.text(cx, (y0 + cy - ry) / 2.0, num, size=26)
        for s, yy in rows:
            f.text(cx, yy, s, size=33)

    def dstore(x1, x2, y, label, lx=None):
        f.line(x1, y, x2, y, sw=1.5)
        f.line(x1, y + 18, x2, y + 18, sw=1.5)
        f.text(lx if lx is not None else (x1 + x2) / 2.0, y - 22, label, size=33)

    def xor(cx, cy, r=12):
        f.circle(cx, cy, r, fill=BOXW, sw=1.3)
        f.line(cx - r, cy, cx + r, cy, sw=1.3)
        f.line(cx, cy - r, cx, cy + r, sw=1.3)

    def star(x, y):
        f.text(x, y, "*", size=30, bold=True)

    def stack(cx, cy, s, size):
        n = len(s)
        for i, ch in enumerate(s):
            f.text(cx, cy + (i - (n - 1) / 2.0) * size * 1.15, ch, size=size)

    # ---- 虚线系统边界（上下被画布裁掉，只画两条可见弧）----
    f.poly([(272, 52), (300, 150), (338, 250), (348, 350), (300, 460),
            (238, 570), (188, 660), (150, 742)], sw=1.6, dash="9,7")
    f.poly([(1238, 0), (1258, 120), (1276, 230), (1310, 350),
            (1360, 470), (1428, 580), (1500, 650), (1560, 700)],
           sw=1.6, dash="9,7")

    # ---- 外部实体 ----
    f.rect(45, 190, 80, 190, fill=BOXW, sw=1.6)
    stack(85, 285, "读者", 36)
    f.rect(1830, 70, 85, 620, fill=BOXW, sw=1.6)
    stack(1872, 380, "读者", 36)

    # ---- 加工 ----
    proc(550, 172, 160, 102, 117, "3.1",
         [("检验是否有", 158), ("超期未还图书", 208)])
    proc(1135, 335, 105, 90, 300, "3.2",
         [("检查借书量", 336), ("上限", 383)])
    proc(600, 570, 130, 120, 505, "3.3",
         [("生成借阅信息", 548), ("修改图书状态", 612)])
    proc(1362, 143, 112, 106, 100, "3.4",
         [("显示超期", 150), ("信息", 198)])
    proc(1500, 412, 115, 107, 375, "3.5",
         [("显示无法", 417), ("借阅", 465)])

    # ---- 数据存储 ----
    dstore(400, 505, 345, "借阅信息", 452)
    dstore(520, 830, 348, "读者信息", 668)
    dstore(940, 1160, 520, "借阅信息", 1050)
    dstore(940, 1160, 700, "图书信息", 1050)

    # ---- 数据流 ----
    f.arrow(125, 285, 388, 182, sw=1.3, head=12)
    f.text(215, 197, "读者号", size=33)
    f.arrow(125, 345, 468, 578, sw=1.3, head=12)
    f.text(180, 458, "欲借书条码号", size=33)
    # 数据存储 → 3.1
    f.arrow(462, 345, 462, 276, sw=1.3, head=12)
    star(432, 222)
    # 3.1 → 3.4 / 3.2
    f.arrow(710, 145, 1248, 145, sw=1.3, head=12)
    f.text(968, 125, "是", size=33)
    f.arrow(708, 212, 1042, 272, sw=1.3, head=12)
    f.text(845, 205, "否", size=33)
    xor(815, 158)
    # 读者信息 → 3.2
    f.arrow(832, 340, 1032, 316, sw=1.3, head=12)
    star(930, 302)
    f.arrow(832, 364, 1032, 380, sw=1.3, head=12)
    star(958, 382)
    # 3.2 → 3.3 / 3.5
    f.arrow(1030, 352, 732, 512, sw=1.3, head=12)
    f.text(835, 440, "未满", size=33)
    xor(1130, 442)
    f.arrow(1240, 330, 1386, 400, sw=1.3, head=12)
    f.text(1300, 295, "已满", size=33)
    # 3.4 / 3.5 → 读者
    f.arrow(1474, 145, 1828, 145, sw=1.3, head=12)
    f.text(1652, 122, "超期信息", size=33)
    f.arrow(1615, 400, 1828, 400, sw=1.3, head=12)
    f.text(1720, 372, "无法借阅", size=33)
    f.text(1720, 420, "原因", size=33)
    # 3.3 输出
    f.arrow(730, 540, 936, 528, sw=1.3, head=12)
    star(792, 588)
    f.arrow(735, 618, 1828, 618, sw=1.3, head=12)
    f.text(1620, 588, "借阅信息", size=33)
    f.arrow(736, 632, 936, 700, sw=1.3, head=12)
    star(776, 646)
    return f


FIGS = [
    ("设计流程", f_design_flow),
    ("分层架构模式", f_layers),
    ("体系结构设计", f_arch_design),
    ("事件驱动", f_event),
    ("微服务模式", f_micro),
    ("类图", f_class),
    ("顺序图", f_seq),
    ("活动图", f_activity),
    ("功能模块图", f_modchart),
    ("功能模块设计", f_moddesign),
    ("数据流图", f_dfd),
]
