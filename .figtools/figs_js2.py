# -*- coding: utf-8 -*-
"""计组插图重绘 —— 第 2 批（存储器 13 张）。"""
import js_kit as K
from js_kit import Fig, INK


# ---------------------------------------------------------------- 小工具

def tw(s, size):
    """粗略文字宽度。"""
    w = 0.0
    for ch in s:
        w += (1.0 if ord(ch) > 0x2000 else 0.56) * size
    return w


def vtext(f, cx, cy0, s, size=14, lh=1.18):
    """竖排文字（一个字一行），cy0 为首字中心。"""
    for i, ch in enumerate(s):
        f.text(cx, cy0 + i * size * lh, ch, size=size)


def ol(f, cx, cy, s, size=14, anchor="middle", gap=0.62, sw=1.0):
    """文字 + 上划线（CS/WE/RAS/CAS）。"""
    f.text(cx, cy, s, size=size, anchor=anchor)
    w = tw(s, size)
    x0 = cx - w / 2 if anchor == "middle" else (cx - w if anchor == "end" else cx)
    f.line(x0, cy - size * gap, x0 + w, cy - size * gap, sw=sw)


def sb(f, cx, cy, main, sub, size=14, anchor="middle", ovl=None, ital=False):
    """主字 + 下标，anchor 以整体宽度为准。"""
    wm = tw(main, size)
    ws = tw(sub, size * 0.70)
    tot = wm + ws
    x = cx - tot / 2 if anchor == "middle" else (cx - tot if anchor == "end" else cx)
    f.text(x, cy, main, size=size, anchor="start", italic=ital)
    f.text(x + wm, cy + size * 0.28, sub, size=size * 0.70, anchor="start", italic=ital)
    if ovl:
        f.line(x + wm, cy + size * 0.28 - size * 0.50, x + tot,
               cy + size * 0.28 - size * 0.50, sw=0.9)
    return tot


def arr2(f, x1, x2, y, sw=1.1, head=6):
    """水平双向箭头。"""
    f.arrow((x1 + x2) / 2, y, x2, y, sw=sw, head=head)
    f.arrow((x1 + x2) / 2, y, x1, y, sw=sw, head=head)


def arr2v(f, y1, y2, x, sw=1.1, head=6):
    f.arrow(x, (y1 + y2) / 2, x, y2, sw=sw, head=head)
    f.arrow(x, (y1 + y2) / 2, x, y1, sw=sw, head=head)


def dots3(f, cx, cy, r=2.0, gap=7, vert=True):
    for i in (-1, 0, 1):
        if vert:
            f.circle(cx, cy + i * gap, r, fill=INK, sw=0.5)
        else:
            f.circle(cx + i * gap, cy, r, fill=INK, sw=0.5)


def jdot(f, cx, cy, r=2.6):
    f.circle(cx, cy, r, fill=INK, sw=0.6)


def hatch(f, x0, x1, y, h=15, step=8.5, sw=0.8):
    """沿水平线 y 向上画斜线（无效区）。"""
    x = x0
    while x <= x1:
        xa = x
        xb = min(x + h * 0.62, x1)
        f.line(xa, y, xb, y - h, sw=sw)
        x += step


def hatch_band(f, x0, x1, yt, yb, step=5.0, sw=0.8):
    """矩形区域斜线填充（45°）。"""
    x = x0 - (yb - yt)
    while x < x1:
        for (ax, ay, bx, by) in ((max(x0, x), min(x0 + 1e9, x)), ):
            pass
        # 计算斜线在矩形内的部分
        yy1, yy2 = yb, yt
        xx1 = x + (0 if True else 0)
        # 线段: (x + t, yb - t), t in [0, yb-yt]
        t0 = max(0.0, x0 - x)
        t1 = min(yb - yt, x1 - x)
        if t1 > t0:
            f.line(x + t0, yb - t0, x + t1, yb - t1, sw=sw)
        x += step


def hexband(f, x0, x1, yt, yb, slant=11, sw=1.4):
    """总线/数据有效六边形带。"""
    ym = (yt + yb) / 2
    f.poly([(x0, ym), (x0 + slant, yt), (x1 - slant, yt), (x1, ym),
            (x1 - slant, yb), (x0 + slant, yb), (x0, ym)], sw=sw)


def xbus(f, x0, x1, yt, yb, xcs, half=14, sw=1.4):
    """总线（双线 + 交叉点）。xcs 为交叉点列表，每次交叉两条线互换上下。"""
    ya, ybb = yt, yb
    pa = [(x0, ya)]
    pb = [(x0, ybb)]
    ym = (yt + yb) / 2.0
    for xc in xcs:
        pa.append((xc - half, ya))
        pb.append((xc - half, ybb))
        pa.append((xc, ym))
        pb.append((xc, ym))
        ya, ybb = ybb, ya
        pa.append((xc + half, ya))
        pb.append((xc + half, ybb))
    pa.append((x1, ya))
    pb.append((x1, ybb))
    f.poly(pa, sw=sw)
    f.poly(pb, sw=sw)


def mos(f, cx, cy, gate="left", hs=11, gs=14, lead=10, sw=1.2):
    """MOS 管符号：沟道竖条 + 栅极竖条 + 栅极引线。"""
    gx = cx - 5 if gate == "left" else cx + 5
    f.line(cx, cy - hs, cx, cy + hs, sw=sw)
    f.line(gx, cy - gs, gx, cy + gs, sw=sw)
    if gate == "left":
        f.line(gx, cy, gx - lead, cy, sw=sw)
    else:
        f.line(gx, cy, gx + lead, cy, sw=sw)


def amp(f, cx, cy, w=40, h=26, inv=False, up=False, sw=1.2):
    """三角形放大器；inv=输出端小圈。"""
    if up:
        f.poly([(cx - w / 2, cy + h / 2), (cx + w / 2, cy + h / 2), (cx, cy - h / 2),
                (cx - w / 2, cy + h / 2)], sw=sw, fill=K.BOXW)
        if inv:
            f.circle(cx, cy - h / 2 - 3, 3, fill=K.BOXW, sw=sw)
    else:
        f.poly([(cx - w / 2, cy - h / 2), (cx - w / 2, cy + h / 2), (cx + w / 2, cy),
                (cx - w / 2, cy - h / 2)], sw=sw, fill=K.BOXW)
        if inv:
            f.circle(cx + w / 2 + 3, cy, 3, fill=K.BOXW, sw=sw)


def brace_l(f, x, y1, y2, w=15, sw=1.2):
    """向左的花括号（尖在左中）。"""
    ym = (y1 + y2) / 2
    b = x - w * 0.5
    f.poly([(x, y1), (x - 1.5, y1 + 2.5), (x - 4, y1 + 4.5), (b + 1, y1 + 6),
            (b, y1 + 10), (b, ym - 12), (b - 1, ym - 8), (b - 3, ym - 4),
            (x - w, ym), (b - 3, ym + 4), (b - 1, ym + 8), (b, ym + 12),
            (b, y2 - 10), (b + 1, y2 - 6), (x - 4, y2 - 4.5),
            (x - 1.5, y2 - 2.5), (x, y2)], sw=sw)


def brace_r(f, x, y1, y2, w=15, sw=1.2):
    ym = (y1 + y2) / 2
    b = x + w * 0.5
    f.poly([(x, y1), (x + 1.5, y1 + 2.5), (x + 4, y1 + 4.5), (b - 1, y1 + 6),
            (b, y1 + 10), (b, ym - 12), (b + 1, ym - 8), (b + 3, ym - 4),
            (x + w, ym), (b + 3, ym + 4), (b + 1, ym + 8), (b, ym + 12),
            (b, y2 - 10), (b - 1, y2 - 6), (x + 4, y2 - 4.5),
            (x + 1.5, y2 - 2.5), (x, y2)], sw=sw)


def brace_u(f, x1, x2, y, w=14, sw=1.2):
    """向上的水平花括号（尖朝上）。"""
    xm = (x1 + x2) / 2
    b = y - w * 0.5
    f.poly([(x1, y), (x1 + 1.5, y - 2.5), (x1 + 4, y - 4.5), (x1 + 9, b + 1),
            (x1 + 13, b), (xm - 15, b), (xm - 10, b - 1), (xm - 5, b - 3),
            (xm, y - w), (xm + 5, b - 3), (xm + 10, b - 1), (xm + 15, b),
            (x2 - 13, b), (x2 - 9, b + 1), (x2 - 4, y - 4.5),
            (x2 - 1.5, y - 2.5), (x2, y)], sw=sw)


# ================================================================ 1 存储器层次结构
def f_memhier(Fig):
    f = Fig(532, 198)
    K.box(f, 44, 62, 88, 36, "CPU", size=17, fill=K.BOXW)
    K.box(f, 164, 62, 88, 36, "缓存", size=17, fill=K.BOXW)
    K.box(f, 280, 62, 88, 36, "主存", size=17, fill=K.BOXW)
    K.box(f, 400, 62, 88, 36, "辅存", size=17, fill=K.BOXW)
    for (xa, xb) in ((132, 164), (252, 280), (368, 400)):
        f.arrow(xa, 74, xb, 74, sw=1.3, head=7)
        f.arrow(xb, 88, xa, 88, sw=1.3, head=7)
    f.poly([(324, 62), (324, 18), (90, 18), (90, 58)], sw=1.5, head=8)
    f.poly([(90, 98), (90, 142), (324, 142), (324, 102)], sw=1.5, head=8)
    f.text(263, 128, "缓存-主存层次", size=14)
    f.text(400, 128, "主存-辅存层次", size=14)
    f.text(212, 176, "图 4.3  缓存-主存层次和主存-辅存层次", size=14)
    return f


# ================================================================ 2 主存基本组成
def f_mainmem(Fig):
    f = Fig(474, 436)
    K.box(f, 43, 44, 104, 99, "存储体", size=16, fill=K.BOXW)
    K.box(f, 198, 45, 51, 98, ["读/写", "电路"], size=14, fill=K.BOXW)
    K.box(f, 299, 44, 52, 99, "MDR", size=15, fill=K.BOXW)
    K.box(f, 44, 171, 104, 29, "驱动器", size=14, fill=K.BOXW)
    K.box(f, 44, 228, 104, 28, "译码器", size=14, fill=K.BOXW)
    K.box(f, 44, 285, 104, 29, "MAR", size=15, fill=K.BOXW)
    K.box(f, 172, 200, 104, 28, "控制电路", size=14, fill=K.BOXW)
    # 存储体 <-> 读/写电路
    f.arrow(196, 64, 150, 64, sw=1.3, head=7)
    f.arrow(150, 124, 196, 124, sw=1.3, head=7)
    dots3(f, 172, 94, r=1.8, gap=7)
    # 读/写电路 <-> MDR
    f.arrow(251, 64, 297, 64, sw=1.3, head=7)
    f.arrow(297, 124, 251, 124, sw=1.3, head=7)
    dots3(f, 274, 94, r=1.8, gap=7)
    # MDR <-> 数据总线
    f.poly([(349, 92), (369, 82), (415, 82), (433, 92), (415, 102),
            (369, 102), (349, 92)], sw=1.4, fill=K.BOXW)
    f.text(391, 70, "数据总线", size=14)
    # 存储体 -> 驱动器 / 译码器 -> 驱动器 / MAR -> 译码器
    for (y1, y2) in ((171, 145), (228, 201), (285, 258)):
        f.arrow(63, y1, 63, y2, sw=1.3, head=7)
        f.line(127, y1, 127, y2, sw=1.3)
        dots3(f, 95, (y1 + y2) / 2, r=1.8, gap=7)
    # 控制电路 -> 读/写电路（空心箭头）
    f.line(219, 200, 219, 152, sw=1.3)
    f.line(229, 200, 229, 152, sw=1.3)
    f.poly([(214, 152), (234, 152), (224, 143), (214, 152)], sw=1.3, fill=INK)
    # 读 / 写
    f.arrow(192, 266, 192, 231, sw=1.3, head=7)
    f.arrow(257, 266, 257, 231, sw=1.3, head=7)
    f.text(192, 278, "读", size=15)
    f.text(257, 278, "写", size=15)
    # 地址总线
    f.line(76, 350, 76, 320, sw=1.3)
    f.line(88, 350, 88, 320, sw=1.3)
    f.poly([(71, 320), (93, 320), (82, 310), (71, 320)], sw=1.3, fill=INK)
    f.text(105, 340, "地址总线", size=14, anchor="start")
    f.text(240, 380, "图 4.4  主存的基本组成", size=14)
    return f


# ================================================================ 3 主存地址分配
def f_addrmap(Fig):
    f = Fig(943, 364)
    # (a) IBM 370
    xs = [271, 333, 397, 460, 524]
    ys = [77, 104, 131, 158]
    vals = [["0", "1", "2", "3"], ["4", "5", "6", "7"], ["8", "9", "10", "11"]]
    for j in range(4):
        for i in range(3):
            f.rect(xs[j], ys[i], xs[j + 1] - xs[j], ys[i + 1] - ys[i], sw=1.4)
            f.text((xs[j] + xs[j + 1]) / 2, (ys[i] + ys[i + 1]) / 2, vals[i][j], size=15)
    # (b) PDP-11
    xs2 = [602, 666, 730]
    vals2 = [["1", "0"], ["3", "2"], ["5", "4"]]
    for j in range(2):
        for i in range(3):
            f.rect(xs2[j], ys[i], xs2[j + 1] - xs2[j], ys[i + 1] - ys[i], sw=1.4)
            f.text((xs2[j] + xs2[j + 1]) / 2, (ys[i] + ys[i + 1]) / 2, vals2[i][j], size=15)
    titles = [(347, xs[0], xs[4]), (655, xs2[0], xs2[2])]
    for (cx, a, b) in titles:
        f.text(cx, 36, "字节地址", size=14)
        brace_u(f, a, b, 70, w=15)
    f.text(238, 62, "字地址", size=14)
    f.text(583, 62, "字地址", size=14)
    for i, v in enumerate(("0", "4", "8")):
        f.text(253, 90 + i * 27, v, size=15)
    for i, v in enumerate(("0", "2", "4")):
        f.text(585, 90 + i * 27, v, size=15)
    f.text(397, 180, "(a) IBM 370", size=14)
    f.text(666, 180, "(b) PDP-11", size=14)
    f.text(450, 208, "图 4.6  字节寻址的主存地址分配", size=14)
    lines = [
        "由图 4.6(a)所示，对 24 位地址线的主存而言，按字节寻址的范围是 16 M，按字寻址的范围",
        "为 4 M。由图 4.6(b)所示，对 24 位地址线而言，按字节寻址的范围仍为 16 M，但按字寻址的范",
        "围为 8 M。",
    ]
    for i, s in enumerate(lines):
        f.text(45, 248 + i * 33, s, size=18, anchor="start")
    return f


# ================================================================ 4 存储芯片的基本结构
def f_chipstruct(Fig):
    f = Fig(718, 293)
    f.rect(146, 34, 362, 201, sw=1.6)
    f.rect(166, 60, 59, 148, sw=1.4)
    vtext(f, 196, 86, "译码驱动", size=15)
    f.rect(242, 60, 168, 148, sw=1.4)
    vtext(f, 326, 86, "存储矩阵", size=15)
    f.rect(429, 60, 59, 148, sw=1.4)
    vtext(f, 459, 86, "读/写电路", size=15)
    # 左：地址线
    for y in (53, 70, 153, 170):
        f.arrow(90, y, 146, y, sw=1.2, head=7)
    dots3(f, 107, 112, r=1.8, gap=8)
    brace_l(f, 82, 48, 176, w=15)
    vtext(f, 52, 88, "地址线", size=15)
    f.arrow(95, 198, 146, 198, sw=1.2, head=7)
    f.text(38, 198, "片选线", size=15, anchor="start")
    # 右：数据线
    for y in (53, 70, 153, 170):
        f.arrow(508, y, 564, y, sw=1.2, head=7)
    dots3(f, 536, 112, r=1.8, gap=8)
    brace_r(f, 568, 48, 176, w=15)
    vtext(f, 604, 88, "数据线", size=15)
    f.arrow(600, 205, 508, 205, sw=1.2, head=7)
    f.text(608, 205, "读/写控制线", size=15, anchor="start")
    f.text(360, 262, "图 4.7  存储芯片的基本结构", size=14)
    return f


# ================================================================ 5 译码驱动方式
def f_decode(Fig):
    f = Fig(1091, 488)
    # ---------- (a) 16×1 字节线选法
    f.rect(100, 79, 40, 197, sw=1.4)
    vtext(f, 120, 100, "地址译码器", size=15)
    for i, s in enumerate(("A3", "A2", "A1", "A0")):
        y = 118 + i * 42
        sb(f, 52, y, "A", s[1], size=15)
        f.arrow(68, y, 98, y, sw=1.2, head=6)
    f.rect(178, 76, 269, 200, sw=1.2, dash="9,4,2,4")
    f.text(152, 96, "字线", size=12)
    f.text(166, 132, "0", size=14)
    f.text(160, 258, "15", size=14)
    cells = [(187, 92, "0,0"), (363, 92, "0,7"), (187, 220, "15,0"), (363, 220, "15,7")]
    for (x, y, s) in cells:
        f.rect(x, y, 53, 25, sw=1.4, fill=K.BOXW)
        f.text(x + 26.5, y + 12.5, s, size=14)
    f.text(300, 180, "16×8 矩阵", size=14)
    # 字线 0 / 15
    f.line(140, 130, 389, 130, sw=1.3)
    f.line(213, 117, 213, 130, sw=1.3)
    jdot(f, 213, 130)
    f.line(140, 258, 389, 258, sw=1.3)
    f.line(213, 245, 213, 258, sw=1.3)
    jdot(f, 213, 258)
    dots3(f, 213, 185, r=1.8, gap=8)
    dots3(f, 389, 185, r=1.8, gap=8)
    dots3(f, 293, 104, r=1.8, gap=8, vert=False)
    dots3(f, 293, 232, r=1.8, gap=8, vert=False)
    # 位线
    for x in (187, 213, 240, 267, 389):
        arr2v(f, 280, 318, x, sw=1.1, head=6)
    f.text(155, 300, "0", size=14)
    f.text(400, 300, "7 位线", size=14, anchor="start")
    dots3(f, 310, 300, r=1.8, gap=8, vert=False)
    # 读/写控制电路
    f.rect(178, 320, 269, 44, sw=1.5)
    f.text(312, 342, "读/写控制电路", size=15)
    f.text(30, 342, "读/写选通", size=14, anchor="start")
    f.arrow(130, 342, 176, 342, sw=1.2, head=6)
    # D0..D7
    for x in (187, 213, 240, 267, 389):
        f.arrow(x, 404, x, 366, sw=1.1, head=6)
        f.arrow(x, 366, x, 404, sw=1.1, head=6)
    for i, x in enumerate((187, 213, 240)):
        sb(f, x, 420, "D", str(i), size=14)
    sb(f, 389, 420, "D", "7", size=14)
    dots3(f, 310, 420, r=1.8, gap=8, vert=False)
    f.text(250, 466, "图 4.9  16×1 字节线选法结构示意图", size=14)

    # ---------- (b) 1K×1 重合法
    f.rect(599, 79, 57, 197, sw=1.4)
    vtext(f, 627, 92, "X", size=15)
    vtext(f, 627, 120, "地址译码器", size=15)
    for i, s in enumerate(("A4", "A3", "A2", "A1", "A0")):
        y = 82 + i * 42
        sb(f, 550, y, "A", s[1], size=15)
        f.arrow(566, y, 597, y, sw=1.2, head=6)
    f.rect(681, 38, 284, 232, sw=1.2, dash="9,4,2,4")
    sb(f, 672, 120, "X", "0", size=14, anchor="end")
    sb(f, 672, 220, "X", "31", size=14, anchor="end")
    cells = [(699, 54, "0,0"), (865, 54, "0,31"), (699, 192, "31,0"), (865, 192, "31,31")]
    for (x, y, s) in cells:
        f.rect(x, y, 63, 22, sw=1.4, fill=K.BOXW)
        f.text(x + 31.5, y + 11, s, size=13)
    f.text(790, 148, "32×32 矩阵", size=14)
    # X0 / X31 行线
    for (y, xa, xb) in ((139, 656, 930), (220, 656, 930)):
        f.line(xa, y, xb, y, sw=1.3)
    for x in (730, 896):
        f.line(x, 76, x, 139, sw=1.3)
        jdot(f, x, 139)
    for x in (730, 896):
        f.line(x, 214, x, 220, sw=1.3)
        jdot(f, x, 220)
    dots3(f, 730, 165, r=1.8, gap=8)
    dots3(f, 896, 165, r=1.8, gap=8)
    dots3(f, 790, 62, r=1.8, gap=8, vert=False)
    # 列方向 MOS 对（重合法）
    for xc in (730, 896):
        # Y 选择线由译码器上来到 y=240，左右分接两只管的栅极
        f.line(xc, 357, xc, 240, sw=1.2)
        f.line(xc - 23, 240, xc + 23, 240, sw=1.2)
        jdot(f, xc, 240)
        for s in (-1, 1):
            f.line(xc + s * 23, 240, xc + s * 23, 248, sw=1.2)   # 栅极引线
            f.line(xc + s * 23, 248, xc + s * 23, 278, sw=1.3)   # 栅条
            f.line(xc + s * 31, 250, xc + s * 31, 274, sw=1.3)   # 沟道条
            f.line(xc + s * 31, 250, xc + s * 31, 214, sw=1.2)   # 列线
            f.line(xc + s * 31, 274, xc + s * 31, 290, sw=1.2)
        f.line(xc - 31, 290, xc + 31, 290, sw=1.2)
        jdot(f, xc, 290)
        f.line(xc, 290, xc, 301, sw=1.2)
    # 数据线到 I/O
    f.line(660, 301, 981, 301, sw=1.2)
    for xc in (730, 896):
        jdot(f, xc, 301)
    # I/O
    f.rect(981, 270, 35, 45, sw=1.4)
    f.text(998, 292, "I/O", size=13)
    f.text(1032, 279, "D", size=14)
    f.arrow(1018, 292, 1052, 292, sw=1.2, head=6)
    f.arrow(1052, 292, 1018, 292, sw=1.2, head=6)
    # Y 地址译码器
    sb(f, 700, 342, "Y", "0", size=14)
    sb(f, 890, 342, "Y", "31", size=14)
    dots3(f, 800, 342, r=1.8, gap=8, vert=False)
    f.rect(665, 357, 290, 40, sw=1.5)
    f.text(810, 377, "Y 地址译码器", size=15)
    for i, s in enumerate(("A9", "A8", "A7", "A6", "A5")):
        x = 710 + i * 52
        f.arrow(x, 425, x, 399, sw=1.2, head=6)
        sb(f, x, 440, "A", s[1], size=14)
    f.text(746, 466, "图 4.10  1 K×1 位重合法结构示意图", size=14)
    return f


def hatch_d(f, x0, x1, y, h=14, step=8.5, sw=0.8):
    """沿水平线 y 向下画斜线（无效区）。"""
    x = x0 - h * 0.62
    while x <= x1:
        f.line(max(x, x0), y + h - max(0, x0 - x), min(x + h * 0.62, x1), y, sw=sw)
        x += step


# ================================================================ 6 静态RAM的基本单元电路
def f_sramcell(Fig):
    f = Fig(707, 450)
    f.rect(140, 55, 330, 197, sw=1.0, dash="9,3,2,3")
    # Vcc 与地
    sb(f, 321, 46, "V", "CC", size=14, ital=True)
    f.line(321, 56, 321, 88, sw=1.3)
    f.line(240, 88, 402, 88, sw=1.5)
    jdot(f, 321, 88)
    f.line(240, 196, 402, 196, sw=1.5)
    f.line(321, 196, 321, 205, sw=1.3)
    for (dy, w) in ((0, 26), (6, 16), (12, 7)):
        f.line(321 - w / 2, 205 + dy, 321 + w / 2, 205 + dy, sw=1.3)
    # 左反相器 T3 / T1
    f.line(240, 88, 240, 104, sw=1.3)
    f.line(240, 126, 240, 160, sw=1.3)
    f.line(240, 182, 240, 196, sw=1.3)
    for (yc, y0, y1) in ((115, 104, 126), (171, 160, 182)):
        f.line(240, y0, 252, y0, sw=1.3)
        f.line(252, y0, 252, y1, sw=1.6)
        f.line(252, y1, 240, y1, sw=1.3)
        f.line(259, y0 - 2, 259, y1 + 2, sw=1.5)
        f.line(259, yc, 266, yc, sw=1.3)
    f.line(266, 115, 266, 171, sw=1.3)
    # 右反相器 T4 / T2
    f.line(396, 88, 396, 104, sw=1.3)
    f.line(396, 126, 396, 160, sw=1.3)
    f.line(396, 182, 396, 196, sw=1.3)
    for (yc, y0, y1) in ((115, 104, 126), (171, 160, 182)):
        f.line(396, y0, 384, y0, sw=1.3)
        f.line(384, y0, 384, y1, sw=1.6)
        f.line(384, y1, 396, y1, sw=1.3)
        f.line(377, y0 - 2, 377, y1 + 2, sw=1.5)
        f.line(377, yc, 370, yc, sw=1.3)
    f.line(370, 115, 370, 171, sw=1.3)
    # 节点线 A′ / A
    f.line(169, 153, 278, 153, sw=1.4)
    f.line(364, 153, 467, 153, sw=1.4)
    jdot(f, 240, 153)
    jdot(f, 396, 153)
    # 交叉耦合
    f.line(266, 143, 364, 153, sw=1.3)
    f.line(370, 143, 278, 153, sw=1.3)
    # 访问管 T5 / T6（串在位线中，栅极接行地址选择）
    for (xc, s) in ((169, -1), (467, 1)):
        f.line(xc, 156, xc, 180, sw=2.6)
        f.line(xc + s * 8, 154, xc + s * 8, 182, sw=1.4)
        f.line(xc + s * 8, 168, xc + s * 16, 168, sw=1.3)
        f.line(xc + s * 16, 168, xc + s * 16, 224, sw=1.3)
        jdot(f, xc + s * 16, 224)
    # 位线
    f.line(169, 180, 169, 258, sw=1.4)
    f.line(467, 180, 467, 258, sw=1.4)
    # 行地址选择
    f.line(112, 224, 543, 224, sw=1.4)
    f.text(64, 208, "行地址选择", size=14)
    # 列地址选择
    f.line(115, 283, 490, 283, sw=1.4)
    f.text(64, 283, "列地址选择", size=14)
    # T7 / T8（列选择管）
    for (x, s) in ((169, -1), (467, 1)):
        f.line(x, 256, x, 280, sw=2.6)
        f.line(x + s * 8, 254, x + s * 8, 282, sw=1.4)
        f.line(x + s * 8, 268, x + s * 8, 283, sw=1.3)
        jdot(f, x + s * 8, 283)
    f.text(190, 252, "T7", size=13)
    f.text(486, 252, "T8", size=13)
    # 底部：写放大器 ×2、读出放大器
    f.line(169, 278, 169, 322, sw=1.3)
    f.line(169, 322, 247, 322, sw=1.3)
    f.circle(247, 322, 3.2, fill=K.BOXW, sw=1.2)
    f.poly([(251, 309), (251, 335), (305, 322), (251, 309)], sw=1.3, fill=K.BOXW)
    f.text(278, 300, "写放大器", size=13)
    f.line(305, 322, 341, 322, sw=1.3)
    jdot(f, 323, 322)
    f.poly([(341, 309), (341, 335), (395, 322), (341, 309)], sw=1.3, fill=K.BOXW)
    f.text(368, 300, "写放大器", size=13)
    f.line(395, 322, 467, 322, sw=1.3)
    jdot(f, 467, 322)
    f.line(467, 278, 467, 322, sw=1.3)
    f.line(467, 322, 519, 322, sw=1.3)
    f.poly([(523, 309), (523, 335), (568, 322), (523, 309)], sw=1.3, fill=K.BOXW)
    f.text(545, 300, "读出放大器", size=13)
    f.line(568, 322, 640, 322, sw=1.3)
    f.arrow(620, 322, 645, 322, sw=1.2, head=7)
    f.text(586, 306, "输出", size=13, anchor="start")
    sb(f, 618, 306, "D", "OUT", size=13, anchor="start")
    # 写入 DIN / 写选择 / 读选择
    f.line(323, 322, 323, 352, sw=1.3)
    f.text(266, 366, "写入", size=13, anchor="start")
    sb(f, 300, 366, "D", "IN", size=13, anchor="start")
    f.arrow(366, 352, 366, 338, sw=1.2, head=6)
    f.text(376, 352, "写选择", size=13, anchor="start")
    f.arrow(550, 352, 550, 338, sw=1.2, head=6)
    f.text(470, 360, "读选择", size=13, anchor="start")
    # 标注
    f.text(228, 100, "T3", size=13)
    f.text(228, 180, "T1", size=13)
    f.text(412, 100, "T4", size=13)
    f.text(412, 180, "T2", size=13)
    f.text(186, 132, "T5", size=13)
    f.text(444, 132, "T6", size=13)
    f.text(262, 140, "A′", size=14)
    f.text(414, 140, "A", size=14)
    f.text(86, 138, "位线 A′", size=14, anchor="start")
    f.arrow(120, 148, 146, 186, sw=1.1, head=6)
    f.text(560, 138, "位线 A", size=14, anchor="end")
    f.arrow(552, 148, 474, 186, sw=1.1, head=6)
    f.text(330, 428, "图 4.11  静态 RAM 的基本单元电路", size=14)
    return f


# ================================================================ 7 SRAM 芯片
def f_sramchip(Fig):
    f = Fig(553, 482)
    # 行选择
    f.rect(187, 25, 29, 109, sw=1.4)
    vtext(f, 201, 55, "行选择", size=13, lh=1.25)
    for i, s in enumerate(("8", "7", "6", "5", "4", "3")):
        y = 37 + i * 17
        sb(f, 118, y, "A", s, size=13)
        f.line(132, y, 185, y, sw=1.2)
        f.arrow(170, y, 185, y, sw=1.2, head=6)
    # 存储矩阵
    f.rect(268, 25, 107, 109, sw=1.5)
    f.text(321, 50, "64×64", size=14)
    f.text(321, 88, "存储矩阵", size=14)
    for (y, t) in ((38, "0"), (54, "1"), (122, "63")):
        f.text(228, y - 6, t, size=13)
        f.line(216, y, 268, y, sw=1.2)
    dots3(f, 240, 85, r=1.8, gap=8)
    # 列 I/O 电路 / 列选择
    f.rect(268, 151, 107, 82, sw=1.5)
    f.line(268, 192, 375, 192, sw=1.3)
    f.text(321, 172, "列 I/O 电路", size=13)
    f.text(321, 213, "列选择", size=13)
    # 存储矩阵下方列线
    f.rect(268, 134, 107, 17, sw=1.1)
    f.line(296, 134, 296, 151, sw=1.1)
    f.line(350, 134, 350, 151, sw=1.1)
    f.text(282, 142, "0", size=12)
    f.text(323, 142, "…", size=13)
    f.text(362, 142, "15", size=12)
    # 输入 / 输出三态
    f.rect(187, 151, 29, 82, sw=1.4)
    vtext(f, 201, 168, "输入三态", size=12, lh=1.18)
    f.rect(428, 151, 27, 82, sw=1.4)
    vtext(f, 441, 168, "输出三态", size=12, lh=1.18)
    # I/O 引脚
    for i, (y, t) in enumerate(((166, "4"), (184, "3"), (201, "2"), (219, "1"))):
        f.text(112, y, "I/O", size=13, anchor="end")
        f.text(114, y + 4, t, size=9, anchor="start")
        f.line(134, y, 187, y, sw=1.2)
        f.line(216, y, 268, y, sw=1.2)
        f.line(375, y, 428, y, sw=1.2)
        jdot(f, 150 + i * 11, y, 2.2)
    # 输出三态到 I/O 的环路
    loops = [(161, 471, 296, 174), (169, 482, 307, 163),
             (177, 493, 318, 152), (185, 503, 329, 141)]
    for (y, rx, ly, lx) in loops:
        f.line(455, y, rx, y, sw=1.2)
        f.line(rx, y, rx, ly, sw=1.2)
        f.line(rx, ly, lx, ly, sw=1.2)
    f.line(141, 166, 141, 329, sw=1.2)
    f.line(152, 184, 152, 318, sw=1.2)
    f.line(163, 201, 163, 307, sw=1.2)
    f.line(174, 219, 174, 296, sw=1.2)
    for (x, y) in ((150, 166), (161, 184), (172, 201), (183, 219)):
        jdot(f, x, y, 2.2)
    # 列选择引脚
    for i, s in enumerate(("9", "2", "1", "0")):
        x = 282 + i * 26
        f.line(x, 233, x, 262, sw=1.2)
        sb(f, x, 272, "A", s, size=13)
    # 与门
    for (gy, gout) in ((342, 355), (378, 391)):
        f.rect(130, gy, 18, 28, sw=1.3, rx=3)
        f.text(139, gy + 14, "&", size=13)
        f.circle(127, gy + 8, 2.6, fill=K.BOXW, sw=1.0)
        f.circle(127, gy + 20, 2.6, fill=K.BOXW, sw=1.0)
    ol(f, 95, 348, "CS", size=14, anchor="middle")
    f.line(108, 348, 124, 348, sw=1.2)
    jdot(f, 112, 348, 2.2)
    f.line(112, 348, 112, 362, sw=1.2)
    f.line(112, 362, 124, 362, sw=1.2)
    ol(f, 95, 392, "WE", size=14, anchor="middle")
    f.line(108, 392, 112, 392, sw=1.2)
    jdot(f, 112, 392, 2.2)
    f.line(112, 392, 112, 398, sw=1.2)
    f.line(112, 398, 124, 398, sw=1.2)
    f.line(148, 355, 202, 355, sw=1.2)
    f.line(202, 355, 202, 236, sw=1.2)
    f.line(202, 236, 201, 236, sw=1.2)
    f.line(148, 391, 442, 391, sw=1.2)
    f.line(442, 391, 442, 236, sw=1.2)
    f.text(310, 460, "图 4.13  2114 RAM 芯片结构示意图", size=14)
    return f


# ================================================================ 8 SRAM 读周期
def f_sram_read(Fig):
    f = Fig(667, 387)
    # 时间标记竖线
    for (x, y1, y2) in ((128, 59, 289), (216, 167, 301), (311, 80, 245),
                        (321, 80, 245), (484, 58, 245), (284, 231, 324),
                        (529, 195, 245), (551, 236, 314)):
        f.line(x, y1, x, y2, sw=1.0)
    f.text(137, 38, "地址有效", size=14)
    f.text(492, 38, "地址失效", size=14)
    # tRC / tA
    arr2(f, 128, 484, 70, sw=1.1, head=6)
    sb(f, 300, 55, "t", "RC", size=14, ital=True)
    arr2(f, 128, 311, 94, sw=1.1, head=6)
    sb(f, 214, 81, "t", "A", size=14, ital=True)
    # 地址总线
    xbus(f, 90, 600, 104, 126, [128, 484], half=14, sw=1.4)
    f.text(72, 115, "A", size=15)
    # CS
    f.poly([(89, 169), (208, 169), (224, 191), (306, 191), (322, 169), (600, 169)], sw=1.4)
    hatch_d(f, 89, 208, 169, h=13)
    hatch_d(f, 322, 600, 169, h=13)
    ol(f, 72, 180, "CS", size=15)
    arr2(f, 224, 306, 218, sw=1.1, head=6)
    sb(f, 265, 204, "t", "CO", size=13, ital=True)
    f.text(432, 157, "片选失效", size=13, anchor="start")
    f.arrow(425, 163, 335, 163, sw=1.0, head=6)
    # DOUT
    f.line(89, 256, 300, 256, sw=1.4)
    hatch(f, 89, 300, 256, h=14)
    hexband(f, 300, 531, 244, 268, slant=11, sw=1.4)
    f.line(531, 256, 600, 256, sw=1.4)
    hatch(f, 531, 600, 256, h=14)
    sb(f, 78, 256, "D", "OUT", size=15, anchor="end")
    arr2(f, 216, 284, 280, sw=1.1, head=6)
    sb(f, 250, 268, "t", "CX", size=13, ital=True)
    arr2(f, 321, 551, 291, sw=1.1, head=6)
    sb(f, 470, 278, "t", "OTD", size=13, ital=True)
    arr2(f, 484, 529, 219, sw=1.1, head=6)
    sb(f, 506, 206, "t", "OHA", size=13, ital=True)
    f.text(232, 320, "数据有效", size=13)
    f.arrow(268, 307, 282, 307, sw=1.0, head=6)
    f.text(398, 312, "数据稳定", size=13, anchor="start")
    f.arrow(392, 307, 330, 307, sw=1.0, head=6)
    f.text(560, 305, "高阻", size=13, anchor="start")
    f.text(300, 355, "图 4.15  2114 RAM 的读周期时序", size=14)
    return f


# ================================================================ 9 SRAM 写周期
def f_sram_write(Fig):
    f = Fig(613, 395)
    for (x, y1, y2) in ((115, 47, 174), (250, 168, 281), (323, 242, 306),
                        (413, 108, 298), (491, 227, 298), (503, 50, 143)):
        f.line(x, y1, x, y2, sw=1.0)
    f.text(118, 28, "地址有效", size=14)
    f.text(497, 28, "地址失效", size=14)
    arr2(f, 115, 503, 65, sw=1.1, head=6)
    sb(f, 300, 50, "t", "WC", size=14, ital=True)
    xbus(f, 88, 570, 74, 97, [115, 503], half=14, sw=1.4)
    f.text(72, 86, "A", size=15)
    arr2(f, 115, 185, 123, sw=1.1, head=6)
    sb(f, 148, 110, "t", "AW", size=13, ital=True)
    arr2(f, 185, 413, 123, sw=1.1, head=6)
    sb(f, 300, 110, "t", "W", size=13, ital=True)
    arr2(f, 413, 503, 123, sw=1.1, head=6)
    sb(f, 456, 108, "t", "WR", size=13, ital=True)
    # CS
    f.poly([(88, 134), (178, 134), (196, 156), (408, 156), (422, 134), (551, 134)], sw=1.4)
    hatch_d(f, 88, 178, 134, h=13)
    hatch_d(f, 422, 551, 134, h=13)
    ol(f, 72, 145, "CS", size=15)
    # WE
    f.poly([(88, 190), (181, 190), (203, 212), (408, 212), (422, 190), (551, 190)], sw=1.4)
    hatch_d(f, 88, 181, 190, h=13)
    hatch_d(f, 422, 551, 190, h=13)
    ol(f, 72, 200, "WE", size=15)
    arr2(f, 185, 250, 180, sw=1.1, head=6)
    sb(f, 214, 167, "t", "DTW", size=13, ital=True)
    # DOUT
    hexband(f, 88, 250, 248, 273, slant=10, sw=1.3)
    f.line(250, 261, 549, 261, sw=1.3)
    hatch(f, 250, 549, 261, h=13)
    sb(f, 78, 261, "D", "OUT", size=15, anchor="end")
    arr2(f, 323, 413, 291, sw=1.1, head=6)
    sb(f, 366, 278, "t", "DW", size=13, ital=True)
    arr2(f, 413, 491, 291, sw=1.1, head=6)
    sb(f, 452, 278, "t", "DH", size=13, ital=True)
    # DIN
    f.line(88, 318, 320, 318, sw=1.3)
    hatch(f, 88, 320, 318, h=13)
    hexband(f, 320, 550, 306, 330, slant=10, sw=1.3)
    sb(f, 78, 318, "D", "IN", size=15, anchor="end")
    f.text(305, 368, "图 4.16  2114 RAM 的写周期时序", size=14)
    return f


# ================================================================ 10 三管 MOS DRAM 芯片
def f_dram3(Fig):
    f = Fig(797, 534)
    f.rect(96, 37, 65, 210, sw=1.5)
    vtext(f, 128, 55, "行地址译码器", size=13, lh=1.25)
    for i, s in enumerate(("9", "8", "7", "6", "5")):
        y = (50, 105, 145, 185, 225)[i]
        sb(f, 58, y, "A", s, size=14, anchor="end")
        f.arrow(72, y, 94, y, sw=1.2, head=6)
    rows = [(49, 88, "0"), (103, 139, "1"), (197, 233, "31")]
    for (y1, y2, t) in rows:
        f.line(161, y1, 608, y1, sw=1.3)
        f.line(161, y2, 608, y2, sw=1.3)
        f.text(156, y1 - 8, t, size=13, anchor="end")
        f.text(156, y2 - 8, t, size=13, anchor="end")
    cols = [224, 296, 368, 488, 560]
    # 单元 + 引线 + 位线
    for (y1, y2, _t) in rows:
        cy = (y1 + y2) / 2.0
        for cx in cols:
            f.rect(cx - 18, cy - 11, 36, 22, sw=1.4, fill=K.BOXW)
            f.line(cx, cy - 11, cx, y1, sw=1.2)
            jdot(f, cx, y1, 2.0)
            f.line(cx, cy + 11, cx, y2, sw=1.2)
            jdot(f, cx, y2, 2.0)
            f.line(cx - 18, cy, cx - 31, cy, sw=1.2)
            f.line(cx + 18, cy, cx + 31, cy, sw=1.2)
    for cx in cols:
        f.line(cx - 31, rows[0][0] + (rows[0][1] - rows[0][0]) / 2.0 - 2,
               cx - 31, 289, sw=1.2)
        f.line(cx + 31, rows[0][0] + (rows[0][1] - rows[0][0]) / 2.0 - 2,
               cx + 31, 289, sw=1.2)
        for (y1, y2, _t) in rows[1:]:
            cy = (y1 + y2) / 2.0
            jdot(f, cx - 31, cy, 2.0)
            jdot(f, cx + 31, cy, 2.0)
    for cx in cols:
        dots3(f, cx, 170, r=1.6, gap=11)
    dots3(f, 428, 168, r=1.6, gap=11, vert=False)
    # 刷新放大器
    for cx in cols:
        f.poly([(cx - 31, 267), (cx + 2, 254), (cx + 2, 280), (cx - 31, 267)],
               sw=1.2, fill=K.BOXW)
        f.line(cx + 2, 267, cx + 31, 267, sw=1.2)
        jdot(f, cx - 31, 267, 2.0)
        jdot(f, cx + 31, 267, 2.0)
    # 读/写控制电路
    f.rect(181, 289, 420, 29, sw=1.5)
    f.text(391, 303, "读/写控制电路", size=14)
    # 列选条
    f.rect(181, 318, 420, 26, sw=1.4)
    for x in (196, 243, 290, 337, 557):
        f.line(x, 318, x, 344, sw=1.1)
    for (x, t) in ((186, "0"), (233, "1"), (280, "2"), (327, "3"), (567, "31")):
        f.text(x, 331, t, size=13, anchor="start")
    dots3(f, 430, 331, r=1.6, gap=11, vert=False)
    # 列地址译码器
    f.rect(181, 344, 420, 29, sw=1.5)
    f.text(391, 358, "列地址译码器", size=14)
    # D
    f.arrow(604, 303, 648, 303, sw=1.2, head=6)
    f.arrow(648, 303, 604, 303, sw=1.2, head=6)
    f.text(634, 290, "D", size=14)
    # A4..A0
    for i, s in enumerate(("4", "3", "2", "1", "0")):
        x = 215 + i * 88
        f.arrow(x, 405, x, 375, sw=1.2, head=6)
        sb(f, x, 420, "A", s, size=14)
    vtext(f, 125, 292, "预充电信号", size=13, lh=1.2)
    # 右侧标注
    f.text(690, 46, "读选择线", size=13, anchor="start")
    f.line(686, 49, 612, 49, sw=1.0)
    f.text(690, 76, "写选择线", size=13, anchor="start")
    f.line(686, 79, 612, 79, sw=1.0)
    f.text(452, 172, "单元", size=13, anchor="start")
    f.text(452, 190, "电路", size=13, anchor="start")
    f.line(448, 178, 404, 210, sw=1.0)
    f.text(690, 285, "刷新", size=13, anchor="start")
    f.text(690, 303, "放大器", size=13, anchor="start")
    f.line(686, 288, 596, 272, sw=1.0)
    vtext(f, 752, 150, "读数", size=13, lh=1.2)
    vtext(f, 752, 186, "据线", size=13, lh=1.2)
    vtext(f, 780, 175, "写数", size=13, lh=1.2)
    vtext(f, 780, 211, "据线", size=13, lh=1.2)
    f.line(746, 140, 597, 100, sw=1.0)
    f.line(774, 165, 592, 132, sw=1.0)
    f.text(400, 505, "图 4.19  1K×1 位三管 MOS 动态 RAM 结构示意图", size=14)
    return f


# ================================================================ 11 单管式 DRAM 芯片
def f_dram1(Fig):
    f = Fig(671, 485)
    # 时序与控制
    f.rect(161, 46, 359, 58, sw=1.5)
    f.text(340, 75, "时序与控制", size=15)
    for (y, s) in ((55, "RAS"), (70, "CAS"), (85, "WE")):
        ol(f, 62, y, s, size=13, anchor="end")
        f.arrow(72, y, 159, y, sw=1.2, head=6)
    for (y, s) in ((55, "行时钟"), (70, "列时钟"), (85, "写时钟")):
        f.arrow(520, y, 566, y, sw=1.2, head=6)
        f.text(570, y, s, size=13, anchor="start")
    # 行/列地址存储器
    f.rect(115, 129, 61, 88, sw=1.4)
    vtext(f, 145, 148, "行地址存储器", size=12, lh=1.2)
    f.rect(117, 281, 60, 88, sw=1.4)
    vtext(f, 147, 300, "列地址存储器", size=12, lh=1.2)
    for (y, t) in ((142, "6"), (178, "0")):
        f.text(70, y, "A′", size=13, anchor="end")
        f.text(71, y + 5, t, size=9, anchor="start")
        f.arrow(90, y, 114, y, sw=1.2, head=6)
    f.arrow(96, 321, 115, 321, sw=1.2, head=6)
    f.line(147, 369, 147, 391, sw=1.2)
    f.line(147, 391, 187, 391, sw=1.2)
    f.line(187, 391, 187, 316, sw=1.2)
    f.arrow(187, 316, 229, 316, sw=1.2, head=6)
    f.arrow(176, 155, 228, 155, sw=1.2, head=6)
    f.arrow(176, 190, 228, 190, sw=1.2, head=6)
    # 中央阵列
    f.rect(230, 132, 183, 237, sw=1.5)
    f.line(281, 132, 281, 369, sw=1.4)
    for y in (180, 204, 228, 271, 295, 320):
        f.line(281, y, 413, y, sw=1.2)
    f.rect(230, 132, 51, 96, sw=1.2)
    vtext(f, 255, 150, "行译码器", size=12, lh=1.2)
    f.rect(230, 228, 51, 43, sw=1.2)
    for (i, s) in enumerate(("读出", "放大", "器控", "制")):
        f.text(255, 236 + i * 10, s, size=9)
    f.rect(230, 271, 51, 98, sw=1.2)
    vtext(f, 255, 290, "行译码器", size=12, lh=1.2)
    f.text(347, 148, "64×128", size=12)
    f.text(347, 166, "存储单元阵列", size=12)
    f.text(347, 192, "基准单元", size=12)
    f.text(347, 216, "列译码器", size=12)
    f.text(347, 240, "128 个读出—", size=12)
    f.text(347, 256, "再生放大器", size=12)
    f.text(347, 283, "列译码器", size=12)
    f.text(347, 308, "基准单元", size=12)
    f.text(347, 338, "64×128", size=12)
    f.text(347, 356, "存储单元阵列", size=12)
    # 右侧三块
    f.rect(500, 137, 88, 53, sw=1.4)
    f.text(544, 156, "数据输入", size=13)
    f.text(544, 174, "寄存器", size=13)
    f.rect(500, 224, 88, 66, sw=1.4)
    f.text(544, 248, "I/O", size=13)
    f.text(544, 266, "缓存器", size=13)
    f.rect(500, 324, 88, 52, sw=1.4)
    f.text(544, 342, "数据输出", size=13)
    f.text(544, 360, "驱动", size=13)
    f.arrow(544, 190, 544, 222, sw=1.2, head=6)
    f.arrow(544, 290, 544, 322, sw=1.2, head=6)
    f.arrow(626, 158, 590, 158, sw=1.2, head=6)
    sb(f, 630, 158, "D", "IN", size=13, anchor="start")
    f.arrow(590, 345, 626, 345, sw=1.2, head=6)
    sb(f, 630, 345, "D", "OUT", size=13, anchor="start")
    # 阵列与 I/O 之间的双向箭头
    for y in (203, 228, 294):
        f.arrow(413, y, 470, y, sw=1.2, head=6)
        f.arrow(470, y, 413, y, sw=1.2, head=6)
    f.line(458, 203, 458, 228, sw=1.2)
    f.line(458, 228, 458, 294, sw=1.2)
    f.line(470, 228, 500, 228, sw=1.2)
    f.line(470, 203, 500, 203, sw=1.2)
    f.line(470, 294, 500, 294, sw=1.2)
    f.text(335, 450, "图 4.20  4116 动态 RAM（16 K×1 位）芯片的结构", size=14)
    return f


# ================================================================ 12 DRAM 读时序
def f_dram_read(Fig):
    f = Fig(592, 376)
    for (x, y1, y2) in ((160, 28, 300), (245, 88, 340), (300, 250, 340),
                        (412, 88, 300), (478, 88, 300)):
        f.line(x, y1, x, y2, sw=1.0)
    arr2(f, 160, 445, 30, sw=1.1, head=6)
    sb(f, 300, 17, "t", "CRD", size=14, ital=True)    # RAS
    f.poly([(70, 55), (148, 55), (160, 73), (358, 73), (376, 55), (443, 55),
            (458, 73), (520, 73)], sw=1.4)
    ol(f, 55, 55, "RAS", size=14, anchor="end")
    # CAS
    f.poly([(70, 98), (230, 98), (245, 118), (394, 118), (412, 98), (520, 98)], sw=1.4)
    ol(f, 55, 98, "CAS", size=14, anchor="end")
    # WE
    f.line(85, 164, 520, 164, sw=1.3)
    hatch_d(f, 85, 520, 164, h=13)
    ol(f, 60, 164, "WE", size=14, anchor="end")
    arr2(f, 163, 233, 195, sw=1.0, head=6)
    sb(f, 198, 183, "t", "suRD-CAS", size=12, ital=True, ovl="CAS")
    arr2(f, 412, 477, 226, sw=1.0, head=6)
    sb(f, 452, 213, "t", "hRD-CAS", size=12, ital=True, ovl="CAS")
    # DOUT
    f.line(70, 258, 285, 258, sw=1.3)
    hexband(f, 285, 460, 242, 274, slant=10, sw=1.3)
    f.line(460, 258, 520, 258, sw=1.3)
    sb(f, 78, 258, "D", "OUT", size=14, anchor="end")
    arr2(f, 160, 300, 310, sw=1.0, head=6)
    sb(f, 225, 298, "t", "aRAS", size=12, ital=True, ovl="RAS")
    arr2(f, 245, 300, 330, sw=1.0, head=6)
    sb(f, 272, 318, "t", "aCAS", size=12, ital=True, ovl="CAS")
    arr2(f, 412, 478, 285, sw=1.0, head=6)
    sb(f, 490, 272, "t", "hCAS-OUT", size=12, ital=True, ovl="CAS")
    f.text(298, 355, "图 4.22  动态 RAM 读工作方式时序图", size=14)
    return f


# ================================================================ 13 DRAM 写时序
def f_dram_write(Fig):
    f = Fig(532, 339)
    for (x, y1, y2) in ((137, 25, 300), (182, 80, 300), (265, 190, 300),
                        (330, 80, 300), (451, 25, 300), (462, 25, 300)):
        f.line(x, y1, x, y2, sw=1.0)
    arr2(f, 137, 451, 33, sw=1.1, head=6)
    sb(f, 294, 20, "t", "CWR", size=14, ital=True)
    # RAS
    f.poly([(70, 40), (125, 40), (137, 59), (352, 59), (369, 41), (451, 41),
            (462, 59), (505, 59)], sw=1.4)
    ol(f, 55, 40, "RAS", size=14, anchor="end")
    # CAS
    f.poly([(70, 97), (170, 97), (182, 118), (317, 118), (330, 97), (505, 97)], sw=1.4)
    ol(f, 55, 97, "CAS", size=14, anchor="end")
    # WE
    f.poly([(66, 158), (120, 158), (136, 176), (290, 176), (306, 158), (494, 158)], sw=1.4)
    hatch_d(f, 66, 120, 158, h=12)
    hatch_d(f, 306, 494, 158, h=12)
    ol(f, 55, 158, "WE", size=14, anchor="end")
    sb(f, 100, 130, "t", "suWR-CAS", size=12, ital=True, ovl="CAS")
    arr2(f, 120, 182, 145, sw=1.0, head=6)
    sb(f, 232, 128, "t", "WWR", size=12, ital=True)
    arr2(f, 182, 330, 140, sw=1.0, head=6)
    sb(f, 372, 145, "t", "hWR-CAS", size=12, ital=True, ovl="CAS")
    arr2(f, 330, 420, 160, sw=1.0, head=6)
    # DIN
    f.line(66, 224, 240, 224, sw=1.2)
    hatch(f, 66, 240, 224, h=13)
    hexband(f, 240, 470, 212, 236, slant=10, sw=1.3)
    f.line(470, 224, 494, 224, sw=1.2)
    hatch(f, 470, 494, 224, h=13)
    sb(f, 72, 224, "D", "IN", size=14, anchor="end")
    sb(f, 92, 186, "t", "suDIN-CAS", size=12, ital=True, ovl="CAS")
    arr2(f, 182, 240, 200, sw=1.0, head=6)
    sb(f, 258, 190, "t", "hDIN-CAS", size=12, ital=True, ovl="CAS")
    arr2(f, 470, 505, 200, sw=1.0, head=6)
    # DOUT
    f.line(66, 272, 492, 272, sw=1.3)
    sb(f, 72, 272, "D", "OUT", size=14, anchor="end")
    f.text(266, 320, "图 4.23  动态 RAM 写工作方式时序图", size=14)
    return f


FIGS = [
    ("存储器层次结构", f_memhier),
    ("主存基本组成", f_mainmem),
    ("主存地址分配", f_addrmap),
    ("存储芯片的基本结构", f_chipstruct),
    ("译码驱动方式", f_decode),
    ("静态RAM的基本单元电路", f_sramcell),
    ("SRAM芯片", f_sramchip),
    ("SRAM读周期", f_sram_read),
    ("SRAM写周期", f_sram_write),
    ("三管MOS DRAM芯片", f_dram3),
    ("单管式DRAM 芯片", f_dram1),
    ("DRAM读时序", f_dram_read),
    ("DRAM写时序", f_dram_write),
]
