# -*- coding: utf-8 -*-
"""计组插图 第 5 批：RISC Ⅱ 指令格式、CPU 结构、三个数据流、六级流水、中断标记、
控制单元外特性、组合逻辑控制单元、微程序相关四图，以及自绘的 I/O 控制方式对比图。"""

import js_kit as K
from js_kit import Fig

INK = K.INK
BOXW = K.BOXW
BOXF = K.BOXF
BLUE = K.BLUE
GREEN = K.GREEN
YELLOW = K.YELLOW


# ---------------------------------------------------------------- 通用小工具
def vtext(f, cx, ytop, s, size=14, gap=1.12):
    """竖排文字（每字一行，水平居中于 cx）。"""
    for i, ch in enumerate(s):
        f.text(cx, ytop + size * gap * (i + 0.5), ch, size=size)


def circ(f, cx, cy, s, r=8.5, size=11):
    f.circle(cx, cy, r, fill="#ffffff", sw=1.3)
    f.text(cx, cy, str(s), size=size)


def dots3(f, cx, cy, gap=7, r=1.6):
    for k in (-1, 0, 1):
        f.circle(cx, cy + k * gap, r, fill=INK, sw=0.5)


def harr(f, x1, x2, y, hw=4.0, hh=9.0, hl=11.0):
    """水平空心粗箭头（头在 x2 一侧）。"""
    if x2 > x1:
        p = [(x1, y - hw), (x2 - hl, y - hw), (x2 - hl, y - hh), (x2, y),
             (x2 - hl, y + hh), (x2 - hl, y + hw), (x1, y + hw), (x1, y - hw)]
    else:
        p = [(x1, y - hw), (x2 + hl, y - hw), (x2 + hl, y - hh), (x2, y),
             (x2 + hl, y + hh), (x2 + hl, y + hw), (x1, y + hw), (x1, y - hw)]
    f.poly(p, sw=1.4)


def dharr(f, x1, x2, y, hw=4.0, hh=9.0, hl=11.0):
    """水平双向空心粗箭头。"""
    p = [(x1, y), (x1 + hl, y - hh), (x1 + hl, y - hw), (x2 - hl, y - hw),
         (x2 - hl, y - hh), (x2, y), (x2 - hl, y + hh), (x2 - hl, y + hw),
         (x1 + hl, y + hw), (x1 + hl, y + hh), (x1, y)]
    f.poly(p, sw=1.4)


def varr(f, x, y1, y2, hw=4.0, hh=9.0, hl=11.0):
    """竖直空心粗箭头（头在 y2 一侧）。"""
    if y2 > y1:
        p = [(x - hw, y1), (x - hw, y2 - hl), (x - hh, y2 - hl), (x, y2),
             (x + hh, y2 - hl), (x + hw, y2 - hl), (x + hw, y1), (x - hw, y1)]
    else:
        p = [(x - hw, y1), (x - hw, y2 + hl), (x - hh, y2 + hl), (x, y2),
             (x + hh, y2 + hl), (x + hw, y2 + hl), (x + hw, y1), (x - hw, y1)]
    f.poly(p, sw=1.4)


def dvarr(f, x, y1, y2, hw=4.0, hh=9.0, hl=11.0):
    p = [(x, y1), (x - hh, y1 + hl), (x - hw, y1 + hl), (x - hw, y2 - hl),
         (x - hh, y2 - hl), (x, y2), (x + hh, y2 - hl), (x + hw, y2 - hl),
         (x + hw, y1 + hl), (x + hh, y1 + hl), (x, y1)]
    f.poly(p, sw=1.4)


def htube(f, x1, x2, y, hw=4.0):
    """水平空心粗线（无箭头）。"""
    p = [(x1, y - hw), (x2, y - hw), (x2, y + hw), (x1, y + hw), (x1, y - hw)]
    f.poly(p, sw=1.4)


def vtube(f, x, y1, y2, hw=4.0):
    p = [(x - hw, y1), (x - hw, y2), (x + hw, y2), (x + hw, y1), (x - hw, y1)]
    f.poly(p, sw=1.4)


def curly(f, x, y1, y2, w=11):
    """右侧花括号（开口向左）。"""
    ym = (y1 + y2) / 2
    p = [(x, y1), (x + w * 0.5, y1 + 2), (x + w * 0.5, ym - 7), (x + w, ym),
         (x + w * 0.5, ym + 7), (x + w * 0.5, y2 - 2), (x, y2)]
    f.poly(p, sw=1.4)


# ================================================================ 1 RISC Ⅱ
def f_risc2(Fig):
    f = Fig(548, 383)
    sz = 15

    def cellrow(y, edges, labels):
        for i, s in enumerate(labels):
            x1, x2 = edges[i], edges[i + 1]
            f.rect(x1, y, x2 - x1, 27, fill=BOXW, sw=1.5)
            if not s:
                continue
            cx = (x1 + x2) / 2
            if s in ("rs1", "rs2"):
                f.sub_text(cx, y + 14, "rs", s[-1], size=sz, italic=False)
            elif s.startswith("imm"):
                f.sub_text(cx, y + 14, "imm", s[3:], size=sz, italic=False)
            else:
                f.text(cx, y + 14, s, size=sz)

    def bits(y, items):
        for x, s in items:
            f.text(x, y, s, size=12)

    # (a)
    cellrow(45, [50, 125, 147, 239, 308, 332, 428, 496],
            ["OP", "S", "DEST", "rs1", "0", "", "rs2"])
    bits(33, [(50, "31"), (107, "25"), (133, "24"), (160, "23"), (213, "19"),
              (232, "18"), (272, "14"), (292, "13"), (310, "12"),
              (396, "5"), (411, "4"), (487, "0")])
    f.text(276, 97, "（a）  第二源操作数在寄存器中的短立即数格式", size=15)

    # (b)
    cellrow(151, [50, 125, 148, 240, 309, 332, 496],
            ["OP", "S", "DEST", "rs1", "1", "imm13"])
    bits(139, [(50, "31"), (107, "25"), (133, "24"), (160, "23"), (213, "19"),
               (232, "18"), (276, "14"), (296, "13"), (312, "12"), (487, "0")])
    f.text(112, 203, "（b）  第二源操作数为", size=15, anchor="start")
    f.sub_text(302, 203, "imm", "13", size=15, italic=False)
    f.text(326, 203, "的短立即数格式", size=15, anchor="start")

    # (c)
    cellrow(259, [50, 125, 148, 239, 496], ["OP", "S", "DEST", "imm19"])
    bits(247, [(50, "31"), (107, "25"), (133, "24"), (160, "23"), (213, "19"),
               (232, "18"), (487, "0")])
    f.text(276, 311, "（c）  长立即数格式", size=15)

    f.text(276, 355, "图 7.23   RISC Ⅱ 的指令格式", size=15)
    return f


# ================================================================ 2 CPU 结构图
def f_cpu(Fig):
    f = Fig(884, 376)

    # ---------------- 图 8.1
    f.rect(56, 98, 179, 179, fill="none", sw=1.6)
    f.text(70, 112, "CPU", size=15, anchor="start")
    K.box(f, 81, 130, 58, 56, "ALU", size=15)
    K.box(f, 151, 130, 60, 56, "寄存器", size=14)
    K.box(f, 82, 204, 57, 56, ["中断", "系统"], size=14, lh=1.25)
    K.box(f, 151, 204, 60, 56, "CU", size=15)

    # 三组总线
    for x in (288, 302, 339, 353, 391, 405):
        f.line(x, 96, x, 278, sw=1.6)
    vtext(f, 276, 198, "控制总线", size=13, gap=1.1)
    vtext(f, 325, 198, "数据总线", size=13, gap=1.1)
    vtext(f, 375, 198, "地址总线", size=13, gap=1.1)

    # 箭头
    dharr(f, 236, 288, 127)
    dharr(f, 236, 339, 160)
    htube(f, 236, 288, 195, hw=3)
    htube(f, 302, 339, 195, hw=3)
    harr(f, 353, 389, 192)
    # 系统总线括号
    f.poly([(287, 281), (290, 289), (298, 290), (338, 290), (344, 297),
            (350, 290), (390, 290), (397, 289), (398, 281)], sw=1.3)
    f.text(342, 303, "系统总线", size=14)
    f.text(240, 330, "图 8.1   使用系统总线的 CPU", size=15)

    # ---------------- 图 8.2
    f.rect(475, 31, 182, 229, fill="none", sw=1.3, dash="14,4,3,4")
    f.text(562, 52, "ALU", size=15)

    alu_rows = [(76, "状态标志"), (118, "移位"), (159, "取反")]
    for y, s in alu_rows:
        K.box(f, 526, y, 98, 27, s, size=14)
    K.box(f, 526, 201, 98, 42, ["算术和", "布尔逻辑"], size=14, lh=1.2)

    f.line(480, 89, 480, 222, sw=1.4)
    for y in (89, 131, 172, 222):
        f.line(480, y, 500, y, sw=1.4)
        f.arrow(500, y, 524, y, sw=1.4, head=8)

    # 内部 CPU 数据总线
    f.rect(688, 35, 40, 223, fill=BOXW, sw=1.5, rx=3)
    vtext(f, 708, 92, "内部CPU数据总线", size=13, gap=1.05)
    # 寄存器
    K.box(f, 792, 35, 62, 152, "寄存器", size=14)
    K.box(f, 793, 217, 62, 40, "CU", size=15)
    K.box(f, 793, 276, 62, 45, ["中断", "系统"], size=14, lh=1.2)

    # 数据总线 <-> 寄存器
    dharr(f, 728, 792, 54, hw=3, hh=7, hl=9)
    dharr(f, 728, 792, 74, hw=3, hh=7, hl=9)
    dharr(f, 728, 792, 172, hw=3, hh=7, hl=9)
    dots3(f, 760, 122, gap=8, r=1.7)
    # 数据总线 <-> ALU 各部件
    for y in (89, 131, 172, 222):
        f.arrow(624, y, 686, y, sw=1.4, head=8)
    # 寄存器 <-> CU
    dvarr(f, 822, 189, 215, hw=3, hh=7, hl=8)
    # CU <-> 中断系统
    varr(f, 822, 259, 274, hw=3, hh=7, hl=8)
    # 数据总线 与 CU 的交叉箭头
    dharr(f, 730, 791, 236, hw=3.2, hh=7, hl=8)
    varr(f, 760, 310, 183, hw=3.2, hh=7, hl=8)
    # 中断系统 <-> 控制信号线
    dharr(f, 765, 792, 290, hw=3, hh=6, hl=7)
    # 控制信号回路
    vtube(f, 765, 290, 312, hw=4)
    htube(f, 575, 765, 312, hw=4)
    vtube(f, 575, 272, 316, hw=4)
    f.poly([(566, 275), (575, 259), (584, 275)], sw=1.4)
    f.text(660, 297, "控制信号", size=14)
    f.text(700, 326, "图 8.2   CPU 的内部结构", size=15)
    return f


# ================================================================ 3 取指周期数据流
def _cpu_frame(f, x1, y1, x2, y2):
    f.rect(x1, y1, x2 - x1, y2 - y1, fill="none", sw=1.6)
    f.text((x1 + x2) / 2, y1 + 12, "CPU", size=15)


def f_fetch(Fig):
    f = Fig(623, 363)
    _cpu_frame(f, 61, 49, 323, 301)
    K.box(f, 87, 95, 87, 36, "PC", size=15)
    K.box(f, 212, 95, 86, 36, "MAR", size=15)
    K.box(f, 213, 165, 85, 36, "CU", size=15)
    K.box(f, 87, 235, 87, 36, "IR", size=15)
    K.box(f, 212, 235, 86, 36, "MDR", size=15)
    K.box(f, 492, 125, 85, 56, "存储器", size=14)

    for x in (365, 381, 409, 423, 450, 466):
        f.line(x, 86, x, 286, sw=1.6)
    vtext(f, 373, 6, "地址总线", size=13, gap=1.08)
    vtext(f, 416, 6, "数据总线", size=13, gap=1.08)
    vtext(f, 458, 6, "控制总线", size=13, gap=1.08)

    harr(f, 174, 212, 113)
    circ(f, 192, 99, 1)
    harr(f, 298, 365, 113)
    circ(f, 330, 99, 2)
    harr(f, 298, 366, 184)
    circ(f, 337, 170, 3)
    harr(f, 409, 300, 253)
    circ(f, 340, 239, 4)
    harr(f, 212, 174, 253)
    circ(f, 196, 239, 5)

    # (PC)+1 回路
    htube(f, 134, 213, 183.5, hw=3.5)
    vtube(f, 130, 143, 187, hw=3.5)
    f.poly([(125, 149), (130, 132), (135, 149)], sw=1.4)
    f.text(112, 160, "+1", size=14)
    circ(f, 196, 172, 6)

    # 总线与存储器
    harr(f, 466, 492, 131, hw=3, hh=6, hl=7)
    harr(f, 492, 423, 148, hw=3, hh=6, hl=7)
    harr(f, 466, 492, 165, hw=3, hh=6, hl=7)
    htube(f, 381, 409, 170, hw=3.5)
    htube(f, 381, 409, 253, hw=3.5)

    f.text(310, 345, "图 8.10  取指周期数据流", size=15)
    return f


# ================================================================ 4 间址周期数据流
def f_indirect(Fig):
    f = Fig(621, 355)
    _cpu_frame(f, 41, 47, 303, 298)
    K.box(f, 193, 94, 85, 35, "MAR", size=15)
    K.box(f, 193, 164, 85, 35, "CU", size=15)
    K.box(f, 193, 233, 85, 35, "MDR", size=15)
    K.box(f, 471, 123, 87, 56, "存储器", size=14)

    for x in (345, 360, 389, 403, 431, 446):
        f.line(x, 84, x, 284, sw=1.6)
    vtext(f, 353, 4, "地址总线", size=13, gap=1.08)
    vtext(f, 396, 4, "数据总线", size=13, gap=1.08)
    vtext(f, 438, 4, "控制总线", size=13, gap=1.08)

    # ① (MDR)->MAR
    htube(f, 148, 193, 251, hw=3.5)
    vtube(f, 148, 112, 255, hw=3.5)
    harr(f, 148, 193, 108)
    circ(f, 167, 232, 1)

    harr(f, 278, 345, 111)
    circ(f, 310, 96, 2)
    harr(f, 278, 346, 181)
    circ(f, 310, 166, 3)
    harr(f, 346, 280, 251)
    circ(f, 310, 236, 4)

    # 总线与存储器
    harr(f, 446, 471, 130, hw=3, hh=6, hl=7)
    harr(f, 471, 403, 147, hw=3, hh=6, hl=7)
    harr(f, 446, 471, 164, hw=3, hh=6, hl=7)
    htube(f, 360, 389, 168, hw=3.5)
    htube(f, 360, 389, 251, hw=3.5)

    f.text(300, 335, "图 8.11  间址周期数据流", size=15)
    return f


# ================================================================ 5 中断周期数据流
def f_intr(Fig):
    f = Fig(608, 372)
    _cpu_frame(f, 68, 62, 326, 314)
    K.box(f, 94, 109, 84, 36, "PC", size=15)
    K.box(f, 216, 109, 85, 36, "MAR", size=15)
    K.box(f, 216, 179, 85, 36, "CU", size=15)
    K.box(f, 216, 249, 85, 36, "MDR", size=15)
    K.box(f, 494, 139, 85, 56, "存储器", size=14)

    for x in (368, 384, 412, 427, 455, 470):
        f.line(x, 100, x, 297, sw=1.6)
    vtext(f, 376, 18, "地址总线", size=13, gap=1.08)
    vtext(f, 419, 18, "数据总线", size=13, gap=1.08)
    vtext(f, 462, 18, "控制总线", size=13, gap=1.08)

    # ① CU -> MAR
    varr(f, 258, 179, 146, hw=3.5, hh=7, hl=9)
    circ(f, 276, 163, 1)
    harr(f, 301, 368, 127)
    circ(f, 335, 111, 2)
    harr(f, 301, 369, 197)
    circ(f, 335, 181, 3)

    # ④ (PC) -> MDR
    vtube(f, 111, 145, 267, hw=3.5)
    harr(f, 111, 216, 267)
    circ(f, 196, 241, 4)

    # ⑤ MDR -> 总线
    harr(f, 301, 369, 267)
    circ(f, 335, 251, 5)

    # ⑥ CU -> PC
    htube(f, 151, 216, 197, hw=3.5)
    varr(f, 151, 197, 146, hw=3.5, hh=7, hl=9)
    circ(f, 170, 181, 6)

    # 存储器与控制总线
    for y in (150, 158, 166, 174):
        f.arrow(470, y, 494, y, sw=1.4, head=7)
    htube(f, 384, 412, 188, hw=3.5)
    htube(f, 384, 412, 201, hw=3.5)

    f.text(300, 350, "图 8.12  中断周期数据流", size=15)
    return f


# ================================================================ 6 六级流水时序
def f_pipeline(Fig):
    f = Fig(690, 421)
    x0, cw, N = 98.0, 39.15, 14
    ytop, ybot = 52, 78

    f.line(99, 29, 630, 29, sw=1.3)
    f.poly([(624, 25), (634, 29), (624, 33)], sw=1.3)
    f.text(645, 29, "t", size=15, italic=True)
    f.text(95, 29, "时间", size=14, anchor="end")
    f.text(58, 58, "时间", size=14)
    f.text(58, 76, "单元", size=14)

    f.rect(x0, ytop, cw * N, ybot - ytop, fill="none", sw=1.5)
    for k in range(1, N):
        f.line(x0 + k * cw, ytop, x0 + k * cw, ybot, sw=1.3)
    for k in range(N):
        f.text(x0 + (k + 0.5) * cw, (ytop + ybot) / 2, str(k + 1), size=14)

    stages = ["FI", "DI", "CO", "FO", "EI", "WO"]
    for i in range(1, 10):
        ay = 117 + (i - 1) * 30.1
        ly = ay - 11
        f.text(88, ly, "指令 %d" % i, size=14, anchor="end")
        for k, s in enumerate(stages):
            cx = x0 + (i - 1 + k + 0.5) * cw
            f.text(cx, ly, s, size=13)
        xa = x0 + (i - 1) * cw + 1
        xb = x0 + (i + 5) * cw - 1
        f.line(xa, ay, xb, ay, sw=1.4)
        f.poly([(xa + 7, ay - 5), (xa, ay), (xa + 7, ay + 5)], sw=1.4)
        f.poly([(xb - 7, ay - 5), (xb, ay), (xb - 7, ay + 5)], sw=1.4)

    for k in range(N + 1):
        K.dashed(f, x0 + k * cw, ybot, x0 + k * cw, 372, sw=1.1, dash="7,6")

    f.text(310, 400, "图 8.15  指令六级流水时序", size=15)
    return f


# ================================================================ 7 中断请求标记寄存器
def f_intflag(Fig):
    f = Fig(451, 224)
    edges = [22, 52, 81, 111, 141, 170, 373, 402, 433]
    f.rect(22, 18, 411, 27, fill=BOXW, sw=1.5)
    for x in edges[1:-1]:
        f.line(x, 18, x, 45, sw=1.4)
    for i, s in enumerate(["1", "2", "3", "4", "5"]):
        f.text((edges[i] + edges[i + 1]) / 2, 32, s, size=14)
    f.text((edges[7] + edges[8]) / 2, 32, "n", size=14, italic=True)

    # 中间的省略断口
    for yy in (18, 45):
        f.line(259, yy - 3.5, 264, yy + 3.5, sw=1.2)
        f.line(267, yy - 3.5, 272, yy + 3.5, sw=1.2)

    labels = [(37, "掉电"), (66, "过热"), (96, "主存读写校验错"), (126, "阶上溢"),
              (155, "非法除法"), (387, "键盘输入"), (417, "打印机输出")]
    for cx, s in labels:
        vtext(f, cx, 55, s, size=14, gap=1.12)

    f.text(228, 196, "图 8.24   中断请求标记寄存器", size=15)
    return f


# ================================================================ 8 控制单元的外特性
def f_cuouter(Fig):
    f = Fig(599, 325)
    K.box(f, 135, 24, 153, 39, "指令寄存器", size=15)
    f.rect(135, 102, 153, 126, fill=BOXW, sw=1.6, rx=3)
    f.text(211, 165, "控制单元", size=17)

    # 指令寄存器 -> 控制单元（空心向下箭头）
    varr(f, 211, 64, 100, hw=4.5, hh=9, hl=10)

    # 左侧输入
    for y in (119, 169, 209):
        f.arrow(80, y, 134, y, sw=1.4, head=8)
    f.text(58, 113, "标志", size=15)
    dots3(f, 95, 145, gap=7, r=1.6)
    f.text(58, 213, "时钟", size=15)

    # 右侧输出
    harr(f, 289, 322, 120, hw=4.5, hh=9, hl=10)
    f.text(420, 120, "CPU 内的控制信号", size=14)
    harr(f, 289, 528, 157, hw=4.5, hh=9, hl=11)
    f.text(410, 183, "到系统总线的控制信号", size=14)
    harr(f, 528, 300, 205, hw=4.5, hh=9, hl=11)
    f.text(410, 223, "来自系统总线的控制信号", size=14)

    f.line(528, 51, 528, 253, sw=1.6)
    f.line(545, 51, 545, 253, sw=1.6)
    vtext(f, 537, 96, "系统总线", size=13, gap=1.05)

    f.text(270, 290, "图 9.2   控制单元外特性", size=15)
    return f


# ================================================================ 9 组合逻辑控制单元框图
def f_comblogic(Fig):
    f = Fig(602, 488)
    K.box(f, 295, 52, 126, 33, "IR", size=15)
    K.box(f, 295, 119, 126, 33, "操作码译码", size=14)
    f.rect(278, 186, 160, 120, fill=BOXW, sw=1.5, rx=3)
    f.text(358, 246, "CU", size=17)
    f.rect(165, 186, 50, 120, fill=BOXW, sw=1.5, rx=3)
    vtext(f, 190, 190, "节拍发生器", size=13, gap=1.12)

    # IR -> 译码
    varr(f, 358, 85, 119, hw=5, hh=8, hl=9)
    f.text(378, 100, "n", size=13, italic=True)
    f.text(389, 100, "位操作码", size=13, anchor="start")

    # 译码 -> CU
    for x in (310, 330, 404):
        varr(f, x, 152, 184, hw=2.6, hh=6, hl=7)
    f.text(301, 165, "0", size=13)
    f.text(322, 165, "1", size=13)
    f.text(365, 168, "…", size=13)
    f.text(414, 165, "2", size=13)
    f.text(422, 160, "n-1", size=9)

    # 节拍发生器 -> CU
    for y, lab in ((202, "T"), (230, "T"), (290, "T")):
        f.arrow(215, y, 277, y, sw=1.4, head=8)
    f.sub_text(243, 196, "T", "0", size=13)
    f.sub_text(243, 225, "T", "1", size=13)
    dots3(f, 243, 258, gap=7, r=1.6)
    f.sub_text(243, 285, "T", "n", size=13)

    # CLK
    f.arrow(38, 246, 164, 246, sw=1.4, head=8)
    f.text(95, 222, "CLK", size=14)
    f.text(95, 240, "（机器主频）", size=13)

    # CU 输出
    for x in (304, 324, 412):
        f.arrow(x, 306, x, 341, sw=1.4, head=8)
    f.sub_text(304, 355, "C", "0", size=13)
    f.sub_text(324, 355, "C", "1", size=13)
    f.text(366, 355, "…", size=13)
    f.sub_text(412, 355, "C", "n", size=13)
    f.text(300, 392, "发至 CPU 内部及系统总线的控制信号", size=14)

    # 标志
    f.arrow(498, 202, 439, 202, sw=1.4, head=8)
    f.arrow(498, 290, 439, 290, sw=1.4, head=8)
    dots3(f, 465, 246, gap=8, r=1.7)
    f.text(524, 246, "标志", size=14)

    f.text(300, 462, "图 10.1  带译码和节拍输入的控制单元框图", size=15)
    return f


# ================================================================ 10 机器指令对应的微程序
def f_microprog(Fig):
    f = Fig(536, 690)
    x1, xm, x2 = 69, 183, 244
    ys = [34, 62, 90, 118, 182, 245, 273, 301, 329, 357, 385, 414, 443, 472,
          499, 528, 555, 584, 620]
    f.rect(x1, ys[0], x2 - x1, ys[-1] - ys[0], fill=BOXW, sw=1.6)
    for y in ys[1:-1]:
        f.line(x1, y, x2, y, sw=1.4)
    f.line(xm, ys[0], xm, 118, sw=1.4)
    f.line(xm, 245, xm, 414, sw=1.4)
    f.line(xm, 443, xm, 584, sw=1.4)

    f.text(156, 16, "控制存储器", size=15)

    left = ["M", "M+1", "M+2", "", "", "P", "P+1", "P+2", "Q", "Q+1",
            "Q+2", "⋮", "K", "K+1", "K+2", "J", "J+1", "⋮"]
    right = ["M+1", "M+2", "xxx", "", "", "P+1", "P+2", "M", "Q+1", "Q+2",
             "M", "", "K+1", "K+2", "M", "J+1", "M", ""]
    for i in range(18):
        yc = (ys[i] + ys[i + 1]) / 2
        s = left[i]
        if s == "⋮":
            dots3(f, 157, yc, gap=6, r=1.4)
        elif s:
            f.text(60, yc, s, size=15, anchor="end")
        r = right[i]
        if r == "⋮":
            dots3(f, (xm + x2) / 2, yc, gap=6, r=1.4)
        elif r:
            f.text((xm + x2) / 2, yc, r, size=15)

    # 两行长单元格
    f.text(156, 138, "⋮", size=16)
    f.text(156, 172, "转执行周期微程序", size=14)
    f.text(156, 198, "⋮", size=16)
    f.text(156, 233, "转取指周期微程序", size=14)

    # 右侧括号与说明
    braces = [(34, 118, "取指周期微程序"), (118, 182, "间址周期微程序"),
              (182, 245, "中断周期微程序"), (245, 329, "对应 LDA 操作的微程序"),
              (329, 414, "对应 ADD 操作的微程序"), (443, 528, "对应 STA 操作的微程序"),
              (528, 584, "对应 JMP 操作的微程序")]
    for y1, y2, s in braces:
        curly(f, 250, y1, y2, w=12)
        f.text(272, (y1 + y2) / 2, s, size=13, anchor="start")

    f.text(268, 662, "图 10.4  不同机器指令所对应的微程序", size=15)
    return f


# ================================================================ 11 微程序控制单元
def f_ucu(Fig):
    f = Fig(623, 519)
    f.rect(42, 63, 471, 385, fill="none", sw=1.3, dash="14,4,3,4")

    # IR
    f.rect(377, 22, 104, 36, fill=BOXW, sw=1.5, rx=3)
    f.line(419, 22, 419, 58, sw=1.4)
    f.text(398, 40, "OP", size=14)
    f.text(492, 40, "IR", size=15, anchor="start")

    K.box(f, 377, 96, 103, 57, ["微地址", "形成部件"], size=13, lh=1.25)
    K.box(f, 377, 192, 103, 59, "顺序逻辑", size=15)
    K.box(f, 377, 289, 103, 34, "CMAR", size=14)
    K.box(f, 377, 362, 103, 36, "地址译码", size=14)

    f.rect(131, 265, 139, 39, fill=BOXW, sw=1.5, rx=3)
    f.line(194, 265, 194, 304, sw=1.4)
    f.text(160, 284, "CMDR", size=13)
    f.text(232, 284, "下地址", size=13)
    K.box(f, 131, 341, 139, 57, "控制存储器", size=14)

    # 主链
    varr(f, 399, 58, 94, hw=4.5, hh=8, hl=9)
    varr(f, 428, 153, 190, hw=3.2, hh=7, hl=8)
    varr(f, 428, 251, 287, hw=3.2, hh=7, hl=8)
    varr(f, 428, 323, 360, hw=3.2, hh=7, hl=8)
    # 地址译码 -> 控制存储器
    f.poly([(428, 398), (428, 437), (196, 437), (196, 400)], sw=1.4)
    f.poly([(432, 398), (432, 433), (200, 433)], sw=1.4)
    # 控制存储器 -> CMDR
    dvarr(f, 200, 341, 306, hw=3.2, hh=7, hl=8)
    # CMDR 下地址 -> 顺序逻辑
    f.poly([(229, 265), (229, 217), (375, 217)], sw=1.4)
    f.poly([(238, 265), (238, 226), (375, 226)], sw=1.4)
    f.poly([(367, 213), (377, 221.5), (367, 230)], sw=1.4)
    # CMDR -> CPU 控制信号
    f.poly([(162, 265), (162, 60)], sw=1.4)
    f.poly([(171, 265), (171, 60)], sw=1.4)
    f.poly([(158, 70), (166.5, 58), (175, 70)], sw=1.4)
    f.text(372, 40, "至 CPU 内部和系统总线的控制信号", size=14, anchor="end")

    # 标志 / CLK
    f.arrow(544, 208, 481, 208, sw=1.4, head=8)
    f.arrow(544, 238, 481, 238, sw=1.4, head=8)
    f.text(554, 208, "标志", size=14, anchor="start")
    f.text(554, 238, "CLK", size=14, anchor="start")

    f.text(300, 490, "图 10.5  微程序控制单元的基本组成", size=15)
    return f


# ================================================================ 12 串行/并行微程序
def f_serpar(Fig):
    f = Fig(960, 448)
    # (a)
    f.line(61, 47, 455, 47, sw=1.4)
    f.line(463, 47, 855, 47, sw=1.4)
    for xa, xb in ((61, 455), (463, 855)):
        f.poly([(xa + 8, 42), (xa, 47), (xa + 8, 52)], sw=1.4)
        f.poly([(xb - 8, 42), (xb, 47), (xb - 8, 52)], sw=1.4)
    f.line(459, 35, 459, 57, sw=1.3)
    f.text(258, 30, "第 i 条微指令周期", size=15)
    f.text(657, 30, "第 i+1 条微指令周期", size=15)

    segs = [(61, 258, "取第 i 条微指令"), (258, 459, "执行第 i 条微指令"),
            (459, 657, "取第 i+1 条微指令"), (657, 855, "执行第 i+1 条微指令")]
    f.rect(61, 82, 794, 39, fill=BOXW, sw=1.5)
    for xa, xb, s in segs:
        if xa != 61:
            f.line(xa, 82, xa, 121, sw=1.4)
        f.text((xa + xb) / 2, 101, s, size=15)
    f.text(420, 152, "（a） 串行操作", size=15)

    # (b)
    rows = [(220, 60, 459, [("取第 i 条微指令", 60, 258), ("执行第 i 条微指令", 258, 459)]),
            (258, 258, 657, [("取第 i+1 条微指令", 258, 459), ("执行第 i+1 条微指令", 459, 657)]),
            (296, 459, 855, [("取第 i+2 条微指令", 459, 657), ("执行第 i+2 条微指令", 657, 855)])]
    for y, xa, xb, cells in rows:
        f.rect(xa, y, xb - xa, 38, fill=BOXW, sw=1.5)
        f.line(cells[0][2], y, cells[0][2], y + 38, sw=1.4)
        for s, cx1, cx2 in cells:
            f.text((cx1 + cx2) / 2, y + 19, s, size=15)
    f.text(430, 366, "（b） 并行操作", size=15)

    f.text(470, 420, "图 10.15  串行微程序和并行微程序控制方式", size=15)
    return f


# ================================================================ 13 主机控制 I/O 设备的方式（自绘）
def f_ioctl(Fig):
    f = Fig(900, 420)
    f.text(450, 28, "主机与 I/O 设备数据传送的四种控制方式", size=18, bold=True)

    panels = [
        ("程序查询方式", "字（字节）",
         ["CPU 全程参与：先查询设备", "状态，就绪后传送一个字", "（或字节），再继续查询。"],
         "干预最多"),
        ("程序中断方式", "字（字节）",
         ["CPU 每传送一个字，就被", "中断一次，转入中断服务", "程序完成一次传送。"],
         "干预较多"),
        ("DMA 方式", "数据块",
         ["传送前由 CPU 初始化", "DMA 控制器，传送过程", "由 DMA 接口接管。"],
         "干预较少"),
        ("通道方式", "一组数据块",
         ["CPU 只启动通道并执行", "通道程序，一批数据块", "传完后才向 CPU 报告。"],
         "干预最少"),
    ]
    w, h, y0 = 196, 296, 66
    for k, (name, unit, desc, deg) in enumerate(panels):
        x = 30 + k * (w + 18)
        # 外框
        f.rect(x, y0, w, h, fill=BOXW, sw=1.6)
        # 标题条
        f.rect(x, y0, w, 40, fill=BLUE, sw=1.6)
        f.text(x + w / 2, y0 + 20, name, size=16, bold=True)
        # 传送单位
        f.text(x + 14, y0 + 60, "传送单位", size=12, anchor="start", color="#555555")
        f.text(x + w / 2, y0 + 84, unit, size=15, bold=True)
        f.line(x + 12, y0 + 100, x + w - 12, y0 + 100, sw=1.0, dash="4,4")
        # CPU 干预
        f.text(x + 14, y0 + 118, "CPU 干预程度", size=12, anchor="start", color="#555555")
        for i, s in enumerate(desc):
            f.text(x + 12, y0 + 140 + i * 21, s, size=12, anchor="start")
        # 干预程度
        f.rect(x + 12, y0 + 210, w - 24, 26, fill=YELLOW, sw=1.2, rx=3)
        f.text(x + w / 2, y0 + 223, deg, size=13)
        # 小示意
        bx, by = x + 24, y0 + 252
        f.rect(bx, by, 44, 26, fill=BOXF, sw=1.3)
        f.text(bx + 22, by + 13, "CPU", size=11)
        f.rect(bx + 108, by, 40, 26, fill=BOXF, sw=1.3)
        f.text(bx + 128, by + 13, "I/O", size=11)
        f.arrow(bx + 46, by + 13, bx + 106, by + 13, sw=(2.6, 2.1, 1.6, 1.2)[k], head=9)

    f.text(450, 390, "注：箭头粗细示意 CPU 对传送过程的干预程度，越粗表示干预越多。",
           size=12, color="#555555")
    f.text(450, 410, "图 10.20  主机控制 I/O 设备的四种方式", size=14)
    return f


FIGS = [
    ("RISC Ⅱ指令格式", f_risc2),
    ("CPU结构图", f_cpu),
    ("取指周期数据流", f_fetch),
    ("间指周期数据流", f_indirect),
    ("中断周期数据流", f_intr),
    ("指令的六级流水时序", f_pipeline),
    ("中断请求标记寄存器", f_intflag),
    ("控制单元的外特性", f_cuouter),
    ("组合逻辑控制单元框图", f_comblogic),
    ("机器指令对应的微程序", f_microprog),
    ("微程序控制单元", f_ucu),
    ("串行微程序和并行微程序控制方式", f_serpar),
    ("主机控制IO设备的方式", f_ioctl),
]
