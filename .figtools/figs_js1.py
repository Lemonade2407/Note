# -*- coding: utf-8 -*-
"""计组插图 SVG 重绘 —— 第 1 批（图 1.7~1.20）"""
import js_kit as K
from js_kit import Fig, INK, BOXF, BOXW, BLUE, GREEN, YELLOW, RED, GRAY

DASH = "5,4"


def hharrow(f, x1, yc, x2, sh=4.0, hl=12, hh=9, sw=1.5):
    """水平空心箭头（轮廓箭头），指向右，yc 为轴心，sh 为半轴高。"""
    xh = x2 - hl
    pts = [(x1, yc - sh), (xh, yc - sh), (xh, yc - hh), (x2, yc),
           (xh, yc + hh), (xh, yc + sh), (x1, yc + sh), (x1, yc - sh)]
    f.poly(pts, sw=sw, fill="#ffffff")


def vharrow(f, xc, y1, y2, sh=4.0, hl=11, hh=9, sw=1.5):
    """竖直空心箭头，y2<y1 向上，y2>y1 向下。"""
    s = 1 if y2 > y1 else -1
    yh = y2 - s * hl
    pts = [(xc - sh, y1), (xc - sh, yh), (xc - hh, yh), (xc, y2),
           (xc + hh, yh), (xc + sh, yh), (xc + sh, y1), (xc - sh, y1)]
    f.poly(pts, sw=sw, fill="#ffffff")


def bdarrow(f, x1, y1, x2, y2, sw=1.4, head=8):
    """虚线箭头。"""
    f.arrow(x1, y1, x2, y2, sw=sw, dash=DASH, head=head)


def dl(f, x1, y1, x2, y2, sw=1.4):
    """虚线。"""
    f.line(x1, y1, x2, y2, sw=sw, dash=DASH)


# ---------------------------------------------------------------- 图 1.7
def f_vn(Fig):
    f = Fig(719, 311)
    S = 17
    K.box(f, 86, 126, 78, 38, "输入设备", size=S)
    K.box(f, 226, 126, 80, 38, "运算器", size=S)
    K.box(f, 226, 51, 80, 38, "存储器", size=S)
    K.box(f, 369, 126, 80, 38, "输出设备", size=S)
    K.box(f, 226, 210, 80, 38, "控制器", size=S)

    # 数据线（实线）
    f.arrow(46, 144, 86, 144, head=9)
    f.arrow(163, 144, 226, 144, head=9)
    f.arrow(305, 144, 369, 144, head=9)
    f.arrow(448, 144, 486, 144, head=9)
    f.arrow(247, 126, 247, 89, head=9)          # 运算器 -> 存储器
    f.line(280, 126, 280, 88, sw=1.5)           # 存储器 - 运算器（带节点）
    f.circle(280, 102, 3.4, fill="#ffffff", sw=1.5)
    f.line(280, 111, 275.5, 119, sw=1.4)
    f.line(280, 111, 284.5, 119, sw=1.4)
    f.line(282, 102, 336, 102, sw=1.5)
    f.line(336, 102, 336, 225, sw=1.5)
    f.arrow(336, 225, 305, 225, head=9)

    # 控制线（虚线）
    dl(f, 191, 69, 191, 174)
    bdarrow(f, 200, 69, 226, 69)
    dl(f, 191, 69, 200, 69)
    dl(f, 191, 174, 242, 174)
    bdarrow(f, 242, 182, 242, 210)
    dl(f, 242, 174, 242, 182)

    dl(f, 125, 163, 125, 225)
    dl(f, 125, 225, 208, 225, )
    bdarrow(f, 208, 225, 226, 225)

    dl(f, 407, 163, 407, 236)
    dl(f, 407, 236, 322, 236)
    bdarrow(f, 322, 236, 305, 236)

    dl(f, 266, 163, 266, 211)
    f.arrow(266, 176, 266, 165, dash=DASH, head=8)
    f.arrow(266, 198, 266, 209, dash=DASH, head=8)

    # 图例
    f.arrow(520, 46, 570, 46, head=9)
    f.text(580, 46, "数据线", size=17, anchor="start")
    f.arrow(520, 72, 570, 72, head=9, dash=DASH)
    f.text(580, 72, "控制线和反馈线", size=17, anchor="start")

    f.text(367, 286, "图 1.7  典型的冯·诺依曼计算机结构框图", size=19)
    return f


# ---------------------------------------------------------------- 图 1.8
def f_memcenter(Fig):
    f = Fig(709, 334)
    S = 16
    K.box(f, 261, 94, 80, 37, "控制器", size=S)
    K.box(f, 118, 169, 79, 37, "输入设备", size=S)
    K.box(f, 261, 169, 80, 37, "存储器", size=S)
    K.box(f, 405, 169, 81, 36, "输出设备", size=S)
    K.box(f, 261, 244, 80, 37, "运算器", size=S)

    # 空心数据线
    hharrow(f, 53, 187, 118, sh=4, hl=12, hh=10)
    hharrow(f, 197, 187, 261, sh=4, hl=12, hh=10)
    hharrow(f, 341, 187, 405, sh=4, hl=12, hh=10)
    hharrow(f, 486, 187, 538, sh=4, hl=12, hh=10)
    vharrow(f, 302, 167, 131, sh=3.5, hl=11, hh=8)   # 存储器 -> 控制器
    vharrow(f, 287, 206, 244, sh=5, hl=11, hh=9)     # 存储器 -> 运算器
    vharrow(f, 316, 244, 206, sh=4, hl=11, hh=9)     # 运算器 -> 存储器

    # 控制线（实线）
    f.line(137, 100, 261, 100, sw=1.5)
    f.arrow(137, 100, 137, 168, head=9)
    f.line(341, 100, 465, 100, sw=1.5)
    f.arrow(465, 100, 465, 168, head=9)
    f.line(324, 131, 324, 169, sw=1.5)
    f.arrow(324, 145, 324, 167, head=8)

    # 反馈线（虚线）
    dl(f, 221, 123, 250, 123)
    bdarrow(f, 250, 123, 261, 123)
    dl(f, 221, 123, 221, 262)
    dl(f, 221, 262, 245, 262)
    bdarrow(f, 245, 262, 261, 262)

    dl(f, 380, 254, 380, 122)
    dl(f, 380, 254, 352, 254)
    dl(f, 380, 122, 350, 122)
    bdarrow(f, 350, 122, 341, 122)

    dl(f, 436, 169, 436, 112)
    dl(f, 436, 112, 350, 112)
    bdarrow(f, 350, 112, 341, 112)

    # 图例
    f.arrow(569, 54, 606, 54, head=9)
    f.text(615, 54, "控制线", size=16, anchor="start")
    f.arrow(569, 76, 606, 76, head=9, dash=DASH)
    f.text(615, 76, "反馈线", size=16, anchor="start")
    hharrow(f, 569, 98, 606, sh=3.5, hl=10, hh=8)
    f.text(615, 98, "数据线", size=16, anchor="start")

    f.text(38, 206, "计算步骤", size=17, anchor="start")
    f.text(34, 224, "和原始数据", size=17, anchor="start")
    f.text(493, 207, "计算结果", size=17, anchor="start")

    f.text(355, 313, "图 1.8  以存储器为中心的计算机结构框图", size=19)
    return f


# ------------------------------------------------- 双线总线与空心箭头
def hbus(f, x1, x2, y1, y2, hl=9, flare=4, sw=1.5, ha="both"):
    """水平双线总线；ha: 'both'/'left'/'right'/'none'。"""
    ym = (y1 + y2) / 2.0
    xs = x1 + hl if ha in ("left", "both") else x1
    xe = x2 - hl if ha in ("right", "both") else x2
    f.line(xs, y1, xe, y1, sw=sw)
    f.line(xs, y2, xe, y2, sw=sw)
    if ha in ("left", "both"):
        f.poly([(x1 + hl, y1 - flare), (x1, ym), (x1 + hl, y2 + flare)], sw=sw, fill="#ffffff")
    if ha in ("right", "both"):
        f.poly([(x2 - hl, y1 - flare), (x2, ym), (x2 - hl, y2 + flare)], sw=sw, fill="#ffffff")


def vbus(f, x1, x2, y1, y2, hl=9, flare=4, sw=1.5, ha="both"):
    """竖直双线总线。"""
    xm = (x1 + x2) / 2.0
    f.line(x1, y1 + (hl if ha in ("top", "both") else 0), x1,
           y2 - (hl if ha in ("bottom", "both") else 0), sw=sw)
    f.line(x2, y1 + (hl if ha in ("top", "both") else 0), x2,
           y2 - (hl if ha in ("bottom", "both") else 0), sw=sw)
    if ha in ("top", "both"):
        f.poly([(x1 - flare, y1 + hl), (xm, y1), (x2 + flare, y1 + hl)], sw=sw, fill="#ffffff")
    if ha in ("bottom", "both"):
        f.poly([(x1 - flare, y2 - hl), (xm, y2), (x2 + flare, y2 - hl)], sw=sw, fill="#ffffff")


def vtxt(f, x, y, s, size=15, gap=None):
    """竖排文字（逐字堆叠），y 为首字中心。"""
    gap = gap or size * 1.2
    for i, ch in enumerate(s):
        f.text(x, y + i * gap, ch, size=size)


# ---------------------------------------------------------------- 图 3.1
def f_cpu2bus(Fig):
    f = Fig(607, 326)
    S = 16
    K.box(f, 47, 23, 118, 59, ["中央处理器", "CPU"], size=S, lh=1.6)
    K.box(f, 48, 224, 117, 59, "主存", size=S)
    for x, w in ((188, 95), (319, 92), (481, 93)):
        K.box(f, x, 121, w, 39, "I/O 接口", size=S)
    K.box(f, 188, 224, 95, 59, ["I/O", "设备 1"], size=S, lh=1.6)
    K.box(f, 319, 224, 92, 59, ["I/O", "设备 2"], size=S, lh=1.6)
    K.box(f, 481, 224, 93, 59, ["I/O", "设备 n"], size=S, lh=1.6)

    # I/O 总线
    f.line(164, 49, 565, 49, sw=1.5)
    f.line(164, 57, 565, 57, sw=1.5)
    f.poly([(565, 45), (588, 53), (565, 61)], sw=1.5, fill="#ffffff")
    f.text(378, 37, "I/O 总线", size=16)

    # M 总线
    vbus(f, 100, 111, 85, 219, hl=17, flare=5, ha="both")
    vtxt(f, 86, 134, "M总线", size=15, gap=20)

    for cx in (235, 366, 504):
        vbus(f, cx - 4, cx + 4, 60, 118, hl=7, flare=3)
        vbus(f, cx - 4, cx + 4, 163, 221, hl=7, flare=3)

    f.text(300, 306, "图 3.1  面向 CPU 的双总线结构框图", size=18)
    return f


# ---------------------------------------------------------------- 图 3.2
def f_single(Fig):
    f = Fig(574, 311)
    S = 16
    K.box(f, 32, 110, 62, 134, "CPU", size=S)
    K.box(f, 118, 110, 62, 134, "主存", size=S)
    for x, w in ((215, 93), (332, 94), (457, 94)):
        K.box(f, x, 110, w, 39, "I/O 接口", size=S)
    K.box(f, 217, 205, 92, 61, ["I/O", "设备 1"], size=S, lh=1.6)
    K.box(f, 333, 205, 93, 61, ["I/O", "设备 2"], size=S, lh=1.6)
    K.box(f, 458, 205, 93, 61, ["I/O", "设备 n"], size=S, lh=1.6)

    hbus(f, 22, 548, 45, 53, hl=16, flare=5)
    f.text(285, 32, "单总线(系统总线)", size=16)

    for cx in (63, 149, 262, 379, 504):
        vbus(f, cx - 4, cx + 4, 60, 106, hl=7, flare=3)
    for cx in (262, 379, 504):
        vbus(f, cx - 4, cx + 4, 153, 202, hl=7, flare=3)

    f.text(441, 129, "…", size=17)
    f.text(441, 235, "…", size=17)
    f.text(285, 292, "图 3.2  单总线结构框图", size=18)
    return f


# ---------------------------------------------------------------- 图 3.3
def f_mem2bus(Fig):
    f = Fig(690, 310)
    S = 16
    K.box(f, 70, 103, 63, 135, "CPU", size=S)
    K.box(f, 206, 103, 64, 135, "主存", size=S)
    for x, w in ((304, 93), (421, 93), (545, 95)):
        K.box(f, x, 104, w, 38, "I/O 接口", size=S)
    K.box(f, 304, 201, 93, 58, ["I/O", "设备 1"], size=S, lh=1.6)
    K.box(f, 421, 201, 93, 58, ["I/O", "设备 2"], size=S, lh=1.6)
    K.box(f, 545, 201, 95, 58, ["I/O", "设备 n"], size=S, lh=1.6)

    hbus(f, 52, 646, 38, 46, hl=16, flare=5)
    f.text(345, 26, "系统总线", size=16)

    # 存储总线
    f.line(143, 166, 195, 166, sw=1.5)
    f.line(143, 174, 195, 174, sw=1.5)
    f.poly([(143, 162), (136, 170), (143, 178)], sw=1.5, fill="#ffffff")
    f.poly([(195, 162), (202, 170), (195, 178)], sw=1.5, fill="#ffffff")
    f.text(168, 155, "存储总线", size=14)

    for cx in (101, 236, 350, 467, 592):
        vbus(f, cx - 4, cx + 4, 57, 98, hl=7, flare=3)
    for cx in (350, 467, 592):
        vbus(f, cx - 4, cx + 4, 153, 195, hl=7, flare=3)

    f.text(530, 123, "…", size=17)
    f.text(530, 230, "…", size=17)
    f.text(345, 290, "图 3.3  以存储器为中心的双总线结构框图", size=18)
    return f


# ---------------------------------------------------------------- 图 3.7
def f_dual(Fig):
    f = Fig(573, 372)
    S = 16
    K.box(f, 55, 86, 66, 35, "CPU", size=S)
    K.box(f, 162, 86, 69, 35, "主存", size=S)
    K.box(f, 273, 86, 68, 35, "通道", size=S)
    K.box(f, 273, 208, 67, 35, "I/O 接口", size=S)
    K.box(f, 417, 208, 69, 35, "I/O 接口", size=S)
    K.box(f, 267, 278, 79, 35, "I/O 设备 0", size=13)
    K.box(f, 410, 278, 82, 35, "I/O 设备 n", size=13)

    f.line(48, 37, 510, 37, sw=1.5)
    f.line(48, 51, 510, 51, sw=1.5)
    f.text(470, 25, "主存总线", size=15)

    f.line(203, 159, 510, 159, sw=1.5)
    f.line(203, 174, 510, 174, sw=1.5)
    f.text(465, 147, "I/O 总线", size=15)

    for cx in (88, 196, 307):
        vbus(f, cx - 4, cx + 4, 57, 82, hl=7, flare=3)
    vbus(f, 303, 311, 125, 155, hl=7, flare=3)
    for cx in (307, 451):
        vbus(f, cx - 4, cx + 4, 178, 204, hl=7, flare=3)
    for cx in (307, 451):
        vbus(f, cx - 4, cx + 4, 247, 274, hl=7, flare=3)

    f.text(380, 225, "…", size=17)
    f.text(380, 295, "…", size=17)
    f.text(300, 345, "图 3.7  双总线结构", size=18)
    return f


# ---------------------------------------------------------------- 图 3.8
def f_tri(Fig):
    f = Fig(639, 275)
    S = 16
    K.box(f, 71, 44, 68, 35, "CPU", size=S)
    K.box(f, 71, 112, 68, 34, "主存", size=S)
    K.box(f, 198, 112, 90, 34, "I/O 接口", size=S)
    K.box(f, 332, 111, 88, 35, "I/O 接口", size=S)
    K.box(f, 486, 111, 89, 35, "I/O 接口", size=S)
    K.box(f, 189, 191, 108, 35, "高速 I/O 设备", size=14)
    K.box(f, 332, 191, 88, 35, "I/O 设备 1", size=13)
    K.box(f, 486, 191, 89, 35, "I/O 设备 n", size=13)

    # I/O 总线（左端空心大箭头）
    f.line(158, 57, 578, 57, sw=1.5)
    f.line(158, 66, 578, 66, sw=1.5)
    f.poly([(158, 50), (140, 61.5), (158, 73)], sw=1.5, fill="#ffffff")
    f.text(370, 47, "I/O 总线", size=16)

    # 主存总线
    vbus(f, 100, 109, 82, 109, hl=9, flare=4)
    f.text(24, 95, "主存总线", size=15, anchor="start")

    # DMA 总线
    f.line(149, 125, 189, 125, sw=1.5)
    f.line(149, 132, 189, 132, sw=1.5)
    f.poly([(149, 121), (142, 128.5), (149, 136)], sw=1.5, fill="#ffffff")
    f.poly([(189, 121), (196, 128.5), (189, 136)], sw=1.5, fill="#ffffff")
    f.text(132, 157, "DMA 总线", size=16, anchor="start")

    for cx in (242, 375, 530):
        vbus(f, cx - 4, cx + 4, 70, 106, hl=7, flare=3)
        vbus(f, cx - 4, cx + 4, 150, 186, hl=7, flare=3)

    f.text(450, 128, "…", size=17)
    f.text(450, 208, "…", size=17)
    f.text(300, 258, "图 3.8  三总线结构", size=18)
    return f


# ---------------------------------------------------------------- 图 3.9
def f_tri2(Fig):
    f = Fig(623, 334)
    S = 15
    K.box(f, 127, 39, 90, 36, "CPU", size=16)
    K.box(f, 368, 39, 89, 36, "Cache", size=16)
    K.box(f, 127, 88, 90, 35, "主存", size=16)
    K.box(f, 231, 88, 125, 35, "局部 I/O 控制器", size=13)

    hbus(f, 228, 356, 52, 61, hl=14, flare=5)
    f.text(292, 40, "局部总线", size=15)

    hbus(f, 74, 543, 147, 158, hl=14, flare=5)
    f.text(320, 135, "系统总线", size=15)

    hbus(f, 61, 548, 270, 281, hl=14, flare=5)
    f.text(345, 260, "扩展总线", size=15)

    names = [("局域网", 52, 80), ("SCSI", 144, 82), ("扩展总线接口", 238, 111),
             ("Modem", 362, 82), ("串行接口", 455, 81)]
    for s, x, w in names:
        K.box(f, x, 197, w, 35, s, size=14 if len(s) > 4 else 15)

    for x in (92, 184, 294, 404, 496):
        f.line(x, 232, x, 270, sw=1.4)
    for x, y1, y2 in ((294, 158, 197), (171, 123, 147), (294, 61, 88), (412, 75, 147)):
        f.line(x, y1, x, y2, sw=1.4)

    f.text(300, 315, "图 3.9  三总线结构的又一形式", size=18)
    return f


# ---------------------------------------------------------------- 图 3.10
def f_quad(Fig):
    f = Fig(635, 430)
    K.box(f, 466, 32, 91, 35, "主存", size=16)
    K.box(f, 95, 91, 90, 35, "CPU", size=16)
    K.box(f, 273, 91, 92, 35, "Cache/桥", size=16)

    hbus(f, 195, 265, 104, 112, hl=10, flare=4)
    f.text(228, 131, "局部总线", size=15)
    hbus(f, 373, 589, 104, 112, hl=10, flare=4)
    f.text(481, 131, "系统总线", size=15)
    hbus(f, 64, 592, 228, 238, hl=15, flare=5)
    f.text(310, 258, "高速总线", size=15)
    hbus(f, 64, 592, 343, 353, hl=15, flare=5)
    f.text(300, 372, "扩展总线", size=15)

    for s, x, w in (("SCSI", 95, 90), ("图形", 224, 77), ("多媒体", 338, 92), ("局域网", 468, 91)):
        K.box(f, x, 164, w, 35, s, size=16)
    for s, x, w in (("FAX", 96, 90), ("扩展总线接口", 206, 112), ("Modem", 338, 110), ("串行接口", 468, 91)):
        K.box(f, x, 279, w, 36, s, size=14 if len(s) > 4 else 16)

    f.line(512, 67, 512, 104, sw=1.4)
    f.line(320, 126, 320, 228, sw=1.4)
    for x in (141, 263, 384, 513):
        f.line(x, 199, x, 228, sw=1.4)
    for x in (141, 263, 393, 513):
        f.line(x, 315, x, 343, sw=1.4)

    f.text(300, 405, "图 3.10  四总线结构", size=18)
    return f


# ---------------------------------------------------------------- 图 3.11
def sarc(f, x1, x2, y, h=16, sw=1.2):
    """虚线半圆弧（接口内的联动示意）。"""
    import math
    cx = (x1 + x2) / 2.0
    rx = (x2 - x1) / 2.0
    pts = [(cx - rx * math.cos(math.pi * i / 20.0), y - h * math.sin(math.pi * i / 20.0))
           for i in range(21)]
    f.poly(pts, sw=sw, dash=DASH)


def f_chain(Fig):
    f = Fig(660, 262)
    K.box(f, 52, 24, 48, 195, "", size=15, fill=BOXF)
    vtxt(f, 76, 44, "总线控制部件", size=15, gap=26)

    f.line(100, 37, 564, 37, sw=1.4)
    f.line(100, 59, 564, 59, sw=1.4)
    f.text(570, 37, "数据线", size=16, anchor="start")
    f.text(570, 59, "地址线", size=16, anchor="start")

    f.line(112, 86, 564, 86, sw=1.4)
    f.arrow(112, 86, 102, 86, head=8)
    f.line(100, 106, 564, 106, sw=1.4)
    f.arrow(100, 106, 100, 106, head=8)
    f.poly([(108, 101), (100, 106), (108, 111)], sw=1.4, fill="#ffffff")
    f.text(140, 73, "BS", size=17, anchor="start")
    f.text(140, 118, "BR", size=17, anchor="start")

    for x, w, n in ((196, 105, "0"), (329, 103, "1"), (460, 103, "n")):
        K.box(f, x, 132, w, 40, "", size=15)
        f.text(x + w / 2.0, 149, "I/O 接口 " + n, size=14)
        sarc(f, x + 17, x + w - 17, 171, h=11)

    taps = [(215, 106), (237, 86), (260, 59), (281, 37),
            (348, 106), (369, 86), (391, 59), (412, 37),
            (479, 106), (500, 86), (522, 59), (543, 37)]
    for x, ytop in taps:
        if ytop in (37, 59):          # 数据/地址：向下箭头 + 节点
            f.circle(x, ytop, 2.4, fill=INK)
            f.line(x, ytop, x, 130, sw=1.4)
            f.poly([(x - 3.5, 122), (x, 130), (x + 3.5, 122)], sw=1.4, fill="#ffffff")
        else:                          # BS/BR：向上箭头
            f.line(x, 132, x, ytop + 2, sw=1.4)
            f.poly([(x - 3.5, ytop + 10), (x, ytop + 2), (x + 3.5, ytop + 10)],
                   sw=1.4, fill="#ffffff")

    # BG 链
    f.line(100, 203, 215, 203, sw=1.4)
    f.arrow(215, 203, 215, 176, head=8)
    for a, b in ((281, 348), (412, 479)):
        f.line(a, 174, a, 203, sw=1.4)
        f.poly([(a - 4, 181), (a, 174), (a + 4, 181)], sw=1.4, fill="#ffffff")
        f.line(a, 203, b, 203, sw=1.4)
        f.arrow(b, 203, b, 176, head=8)
    f.line(543, 174, 543, 203, sw=1.4)
    f.poly([(539, 181), (543, 174), (547, 181)], sw=1.4, fill="#ffffff")
    f.line(543, 203, 584, 203, sw=1.4)
    f.text(146, 192, "BG", size=17, anchor="middle")
    f.text(600, 203, "…", size=17)

    f.text(330, 240, "（a） 链式查询方式", size=18)
    return f


# ---------------------------------------------------------------- 图 3.12
def f_counter(Fig):
    f = Fig(684, 265)
    K.box(f, 33, 19, 48, 160, "", size=15)
    vtxt(f, 57, 38, "总线控制部件", size=15, gap=24)

    for y, s in ((48, "数据线"), (71, "地址线"), (95, "设备地址线")):
        f.line(81, y, 545, y, sw=1.4)
        f.text(552, y, s, size=15, anchor="start")

    f.line(81, 118, 545, 118, sw=1.4)
    f.poly([(89, 113), (81, 118), (89, 123)], sw=1.4, fill="#ffffff")
    f.line(92, 142, 545, 142, sw=1.4)
    f.poly([(100, 137), (92, 142), (100, 147)], sw=1.4, fill="#ffffff")
    f.text(95, 105, "BS", size=16, anchor="start")
    f.text(95, 130, "BR", size=16, anchor="start")

    for x, w, n in ((153, 106, "0"), (283, 104, "1"), (417, 104, "n")):
        K.box(f, x, 172, w, 39, "I/O 接口 " + n, size=16)

    taps = [(166, 142, 0), (185, 118, 0), (204, 95, 1), (225, 71, 1), (245, 48, 1),
            (296, 142, 0), (316, 118, 0), (335, 95, 1), (354, 71, 1), (374, 48, 1),
            (431, 142, 0), (450, 118, 0), (470, 95, 1), (489, 71, 1), (508, 48, 1)]
    for x, ytop, dot in taps:
        f.line(x, ytop, x, 172, sw=1.4)
        f.poly([(x - 3.5, ytop + 9), (x, ytop + 2), (x + 3.5, ytop + 9)],
               sw=1.4, fill="#ffffff")
        f.poly([(x - 3.5, 165), (x, 172), (x + 3.5, 165)], sw=1.4, fill="#ffffff")
        if dot:
            f.circle(x, ytop, 2.4, fill=INK)

    f.text(330, 240, "（b） 计数器定时查询方式", size=18)
    return f


# ---------------------------------------------------------------- 图 3.13
def f_indep(Fig):
    f = Fig(679, 330)
    K.box(f, 37, 31, 48, 183, "", size=15)
    vtxt(f, 61, 52, "总线控制部件", size=15, gap=26)

    f.line(84, 42, 553, 42, sw=1.4)
    f.line(84, 65, 553, 65, sw=1.4)
    f.text(560, 42, "地址线", size=16, anchor="start")
    f.text(560, 65, "数据线", size=16, anchor="start")

    # 各级 BG/BR 线
    lv = [(88, 445, "BGn"), (111, 424, "BRn"), (134, 303, "BG1"),
          (158, 281, "BR1"), (181, 167, "BG0"), (204, 145, "BR0")]
    for y, xend, name in lv:
        f.line(84, y, xend, y, sw=1.4)
        f.poly([(92, y - 5), (84, y), (92, y + 5)], sw=1.4, fill="#ffffff")

    for x, w, n in ((125, 105, "0"), (261, 104, "1"), (402, 104, "n")):
        K.box(f, x, 231, w, 39, "I/O 接口 " + n, size=16)

    # 每个接口的 4 根引线：BR, BG, 数据, 地址
    for xb, (xbr, xbg, xd, xa), (ybr, ybg) in (
            ((125, 105), (145, 167, 189, 210), (204, 181)),
            ((261, 104), (281, 303, 324, 345), (158, 134)),
            ((402, 104), (424, 445, 466, 488), (111, 88))):
        f.line(xbr, ybr, xbr, 231, sw=1.4)
        f.line(xbg, ybg, xbg, 231, sw=1.4)
        f.line(xd, 65, xd, 231, sw=1.4)
        f.circle(xd, 65, 2.4, fill=INK)
        f.line(xa, 42, xa, 231, sw=1.4)
        f.circle(xa, 42, 2.4, fill=INK)
        for x in (xbr, xbg, xd, xa):
            f.poly([(x - 3.5, 222), (x, 230), (x + 3.5, 222)], sw=1.4, fill="#ffffff")

    f.text(376, 79, "BG", size=15, anchor="start")
    f.text(395, 82, "n", size=11, anchor="start")
    f.text(381, 102, "BR", size=15, anchor="start")
    f.text(400, 105, "n", size=11, anchor="start")
    f.text(251, 125, "BG", size=15, anchor="start")
    f.text(270, 128, "1", size=11, anchor="start")
    f.text(254, 149, "BR", size=15, anchor="start")
    f.text(273, 152, "1", size=11, anchor="start")
    f.text(110, 172, "BG", size=15, anchor="start")
    f.text(129, 175, "0", size=11, anchor="start")
    f.text(113, 195, "BR", size=15, anchor="start")
    f.text(132, 198, "0", size=11, anchor="start")

    f.text(378, 248, "…", size=17)
    f.text(330, 305, "（c） 独立请求方式", size=18)
    return f


# ---------------------------------------------------------------- 图 3.18
def bez(p0, p1, p2, p3, n=18):
    pts = []
    for i in range(n + 1):
        t = i / float(n)
        u = 1 - t
        x = u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0]
        y = u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]
        pts.append((x, y))
    return pts


def _async(f, dx, kind, cap):
    """异步通信互锁波形：dx 为子图左端偏移，kind=a/b/c。"""
    low1, hi1, low2, hi2 = 56, 27, 97, 68
    x0 = 82 + dx
    r1, f1 = x0 + 18, x0 + 67      # 请求上升/下降
    r2, f2 = x0 + 51, x0 + 101     # 回答上升/下降
    f.poly([(x0, low1), (r1, low1), (r1, hi1), (f1, hi1), (f1, low1), (x0 + 117, low1)], sw=1.8)
    f.poly([(x0, low2), (r2, low2), (r2, hi2), (f2, hi2), (f2, low2), (x0 + 117, low2)], sw=1.8)
    f.text(x0 - 31, 44, "请求", size=17)
    f.text(x0 - 31, 87, "回答", size=17)

    # 请求 -> 回答（向下弧）
    f.poly(bez((r1 + 1, 43), (r1 + 12, 43), (r2 - 4, 50), (r2 - 1, 62)), sw=1.6)
    f.arrow(r2 - 2, 56, r2, 67, sw=1.6, head=8)
    if kind in ("b", "c"):
        # 回答 -> 请求下降沿（向上弧）
        f.poly(bez((r2 + 3, 65), (r2 + 12, 54), (r2 + 13, 40), (r2 + 10, 29)), sw=1.6)
        f.arrow(r2 + 10, 40, r2 + 10, 29, sw=1.6, head=8)
    if kind == "c":
        # 请求下降沿 -> 回答下降沿（向下弧）
        f.poly(bez((f1 + 3, 30), (f1 + 15, 31), (f2 - 6, 40), (f2 - 2, 54)), sw=1.6)
        f.arrow(f2 - 4, 46, f2 - 1, 57, sw=1.6, head=8)
    f.text(x0 + 47, 132, "（%s） %s" % (kind, cap), size=18)


def f_async(Fig):
    f = Fig(625, 197)
    _async(f, 0, "a", "不互锁")
    _async(f, 180, "b", "半互锁")
    _async(f, 360, "c", "全互锁")
    f.text(310, 172, "图 3.18  异步通信中请求与回答的互锁", size=19)
    return f


FIGS = [
    ("冯·诺依曼计算机结构框图", f_vn),
    ("以存储器为中心的计算机结构框图", f_memcenter),
    ("CPU为中心的双总线结构", f_cpu2bus),
    ("单总线结构", f_single),
    ("以存储器为中心的双总线结构", f_mem2bus),
    ("双总线结构", f_dual),
    ("三总线结构", f_tri),
    ("三总线结构的又一形式", f_tri2),
    ("四总线结构", f_quad),
    ("链式查询方式", f_chain),
    ("计数器定时查询方式", f_counter),
    ("独立请求方式", f_indep),
    ("异步通信三种方式", f_async),
]
