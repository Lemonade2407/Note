# -*- coding: utf-8 -*-
"""软件工程导论 配图重绘（第 2 批，11 张）。"""
import math

import se_kit as K
from se_kit import Fig, INK

TITLE = "#17869c"      # 标题青
CY = "#1a9db8"         # 装饰箭头青
BL = "#1a5fa8"         # 校徽蓝
RED = "#c00000"


# ------------------------------------------------------------------ 小工具

def vt(f, x, cy, s, size, gap, bold=False):
    """竖排文字（逐字堆叠），(x,cy) 为整串中心。"""
    n = len(s)
    y0 = cy - gap * (n - 1) / 2.0
    for i, ch in enumerate(s):
        f.text(x, y0 + i * gap, ch, size=size, bold=bold)


def actor(f, cx, hy, label=None, r=7, size=11, sw=1.4):
    """小人：头心 (cx,hy)。"""
    f.circle(cx, hy, r, sw=sw)
    f.line(cx, hy + r, cx, hy + r + 20, sw=sw)
    f.line(cx - 14, hy + r + 9, cx + 14, hy + r + 9, sw=sw)
    f.line(cx, hy + r + 20, cx - 12, hy + r + 33, sw=sw)
    f.line(cx, hy + r + 20, cx + 12, hy + r + 33, sw=sw)
    if label:
        f.text(cx, hy + r + 45, label, size=size)


def tx(f, x, y, s, size=14, color=None, bold=False):
    f.text(x, y, s, size=size, anchor="start", color=color, bold=bold)


def mid(f, x, y, s, size=14, color=None, bold=False):
    f.text(x, y, s, size=size, color=color, bold=bold)


def chev(f, x, y, s, color=CY):
    """双尖角箭头装饰。"""
    for i in range(2):
        x0 = x + i * s * 0.72
        f.poly([(x0, y - s / 2), (x0 + s * 0.55, y), (x0, y + s / 2)],
               sw=s * 0.30, fill=color)


def logo(f, cx, cy, k=1.0):
    """北京工业大学校徽（简化）。"""
    f.circle(cx, cy, 23 * k, fill=BL, sw=1.0)
    f.circle(cx, cy, 18 * k, fill="none", sw=0.8)
    f.text(cx, cy + 1 * k, "B", size=20 * k, color="#ffffff", bold=True)
    f.text(cx, cy + 13 * k, "BJUT", size=5.4 * k, color="#ffffff")
    tx(f, cx + 32 * k, cy - 9 * k, "北京工业大学", 21 * k, color=TITLE, bold=True)
    tx(f, cx + 32 * k, cy + 11 * k, "BEIJINGUNIVERSITYOFTECHNOLOGY", 8.0 * k,
       color=TITLE)


# ------------------------------------------------------------------ 1 建模规范1

def f_mjgf1(Fig):
    f = Fig(1320, 439)
    S, L = 30, 336
    # 第 1 行：椭圆 / 圆角矩形 = 数据加工
    f.ellipse(74, 69, 46, 42, sw=1.6)
    mid(f, 165, 62, "或", 28)
    f.rect(207, 33, 87, 68, rx=13, sw=1.6)
    tx(f, L, 54, "椭圆形或圆角矩形表示数据加工，其中要注明加工的名字，需要使用", S)
    tx(f, L, 104, "动词性短语。", S)
    # 第 2 行：长方形 / 长方体 = 外部实体
    f.rect(37, 145, 78, 59, sw=1.6)
    mid(f, 165, 172, "或", 28)
    f.rect(212, 160, 48, 44, sw=1.6)
    f.poly([(212, 160), (236, 140), (284, 140), (260, 160), (212, 160)], sw=1.6)
    f.poly([(260, 160), (284, 140), (284, 184), (260, 204)], sw=1.6)
    tx(f, L, 170, "长方形或长方体表示外部实体，其中要注明数据源或数据汇点的名字。", S)
    # 第 3 行：双横线 / 右开口矩形 = 数据存储
    f.line(34, 301, 119, 301, sw=1.9)
    f.line(34, 310, 119, 310, sw=1.9)
    mid(f, 165, 274, "或", 28)
    f.poly([(285, 254), (207, 254), (207, 300), (285, 300)], sw=1.6)
    tx(f, L, 251, "双横线或右开口长方形表示数据存储，要用名词或名词性短语为其", S)
    tx(f, L, 301, "命名。", S)
    # 第 4 行：箭头 = 数据流
    f.arrow(141, 377, 286, 377, sw=1.9)
    tx(f, L, 350, "箭头表示数据流，即被加工数据的传递方向，要用名词或名词性短语", S)
    tx(f, L, 400, "为其命名。", S)
    return f


# ------------------------------------------------------------------ 2 建模规范2

def _panel(f, cx, cy, r, kind, num=None):
    f.circle(cx, cy, r, sw=1.6)
    if num:
        f.text(cx, cy + 1, num, size=24)


def f_mjgf2(Fig):
    f = Fig(1347, 598)
    S = 26
    R = 38

    def arrow_in(pts, head=9):
        f.poly(pts, sw=1.6, head=head)

    # ---------------- 左上：A、B 同时输入（* 号）
    cx, cy = 211, 119
    _panel(f, cx, cy, R, "and")
    tx(f, 62, 52, "A", 26)
    tx(f, 56, 178, "B", 26)
    f.poly([(75, 74), (188, 106)], sw=1.6, head=9)
    f.poly([(72, 166), (188, 133)], sw=1.6, head=9)
    f.text(147, 114, "*", size=34)
    f.arrow(cx + R + 2, cy, 302, cy, sw=1.6)
    tx(f, 306, 100, "C", 26)
    tx(f, 357, 94, "数据A和数据B同时输", S)
    tx(f, 357, 128, "入才能变换成数据C", S)

    # ---------------- 右上：A 变换成 B 或 C
    cx, cy = 808, 119
    _panel(f, cx, cy, R, "xorout")
    tx(f, 660, 92, "A", 26)
    f.arrow(672, cy, cx - R - 2, cy, sw=1.6)
    f.poly([(838, 103), (912, 62)], sw=1.6, head=9)
    f.poly([(838, 135), (912, 178)], sw=1.6, head=9)
    f.text(853, 119, "+", size=30)
    tx(f, 884, 56, "B", 26)
    tx(f, 884, 182, "C", 26)
    tx(f, 961, 90, "数据A变换成数据B或数据C", S)
    tx(f, 961, 124, "或数据B和数据C，其中“+”", S)
    tx(f, 961, 158, "号可以省略", S)

    # ---------------- 左中：A 变换成 B 和 C
    cx, cy = 211, 310
    _panel(f, cx, cy, R, "andout")
    tx(f, 68, 270, "A", 26)
    f.poly([(75, 291), (188, 305)], sw=1.6, head=9)
    f.poly([(235, 296), (322, 262)], sw=1.6, head=9)
    f.poly([(235, 325), (322, 356)], sw=1.6, head=9)
    f.text(258, 302, "*", size=34)
    tx(f, 316, 240, "B", 26)
    tx(f, 316, 372, "C", 26)
    tx(f, 357, 285, "数据A变换成数据B", S)
    tx(f, 357, 319, "和数据C", S)

    # ---------------- 右中：A 或 B（互斥）输入
    cx, cy = 808, 310
    _panel(f, cx, cy, R, "orin")
    tx(f, 662, 246, "A", 26)
    tx(f, 658, 388, "B", 26)
    f.poly([(672, 262), (786, 297)], sw=1.6, head=9)
    f.poly([(670, 366), (786, 325)], sw=1.6, head=9)
    f.text(746, 310, "⊕", size=32)
    f.arrow(cx + R + 2, cy, 908, cy, sw=1.6)
    tx(f, 912, 298, "C", 26)
    tx(f, 961, 268, "数据A或数据B（但不能", S)
    tx(f, 961, 302, "A、B同时）输入时变换", S)
    tx(f, 961, 336, "成数据C", S)

    # ---------------- 左下：A 或 B 或 A、B 同时
    cx, cy = 211, 457
    _panel(f, cx, cy, R, "orin2")
    tx(f, 66, 412, "A", 26)
    tx(f, 66, 548, "B", 26)
    f.poly([(75, 420), (188, 449)], sw=1.6, head=9)
    f.poly([(72, 542), (188, 470)], sw=1.6, head=9)
    f.text(147, 456, "+", size=30)
    f.arrow(cx + R + 2, cy, 302, cy, sw=1.6)
    tx(f, 306, 438, "C", 26)
    tx(f, 357, 425, "数据A或数据B或数据", S)
    tx(f, 357, 459, "A、数据B同时输入变", S)
    tx(f, 357, 493, "换成数据C，其中，", S)
    tx(f, 357, 526, "“+”号可以省略", S)

    # ---------------- 右下：A 变换成 B 或 C（不可同时）
    cx, cy = 808, 457
    _panel(f, cx, cy, R, "xorout2")
    tx(f, 660, 440, "A", 26)
    f.arrow(672, cy, cx - R - 2, cy, sw=1.6)
    f.poly([(837, 441), (912, 402)], sw=1.6, head=9)
    f.poly([(837, 473), (912, 514)], sw=1.6, head=9)
    f.text(852, 457, "⊕", size=32)
    tx(f, 884, 396, "B", 26)
    tx(f, 884, 520, "C", 26)
    tx(f, 961, 446, "数据A变换成数据B或数", S)
    tx(f, 961, 480, "据C，但不能变换成数据", S)
    tx(f, 961, 514, "B和数据C", S)
    return f


# ------------------------------------------------------------------ 3 顶层图

def f_dingceng(Fig):
    f = Fig(1262, 642)
    CX, CYy, RX, RY = 618, 320, 112, 300

    def edge(y):
        t = 1 - ((y - CYy) / float(RY)) ** 2
        return RX * math.sqrt(max(t, 0.0))

    # 外部实体
    f.rect(4, 69, 93, 445, sw=2.0)
    vt(f, 50, 291, "图书馆管理员", 34, 42)
    f.rect(1160, 13, 95, 626, sw=2.0)
    vt(f, 1207, 324, "读者", 34, 41)
    # 系统
    f.ellipse(CX, CYy, RX, RY, sw=2.0)
    vt(f, CX, 318, "图书借阅系统", 32, 41)

    # 左侧 4 条数据流
    left = [("读者信息维护事务", 178, 1), ("图书信息维护事务", 261, 1),
            ("管理员查询事务", 342, 1), ("管理员查询结果", 414, -1)]
    for s, y, d in left:
        x1, x2 = 97, CX - edge(y)
        if d > 0:
            f.arrow(x1, y, x2, y, sw=2.0)
        else:
            f.arrow(x2, y, x1, y, sw=2.0)
        mid(f, (x1 + x2) / 2, y - 22, s, 35)

    # 右侧 11 条数据流
    right = [("读者号", 42, -1), ("预借书条码号", 100, -1), ("超期信息", 147, 1),
             ("借阅信息", 203, 1), ("续借事务", 258, -1), ("续借信息", 314, 1),
             ("欲还书条码号", 369, -1), ("支付罚款事务", 425, -1),
             ("还书信息", 480, 1), ("读者查询事务", 536, -1),
             ("读者查询结果", 592, 1)]
    for s, y, d in right:
        x1, x2 = CX + edge(y), 1160
        if d > 0:
            f.arrow(x1, y, x2, y, sw=2.0)
        else:
            f.arrow(x2, y, x1, y, sw=2.0)
        mid(f, 930, y - 20, s, 35)
    return f


# ------------------------------------------------------------------ 4 一层数据流图

def _proc(f, cx, cy, r, num, lines, size=19):
    f.circle(cx, cy, r, sw=1.6)
    dy = -r * 0.26
    half = math.sqrt(max(r * r - dy * dy, 1))
    f.line(cx - half, cy + dy, cx + half, cy + dy, sw=1.6)
    f.text(cx, cy - r * 0.62, num, size=size)
    if len(lines) == 1:
        f.text(cx, cy + r * 0.42, lines[0], size=size)
    else:
        y0 = cy + r * 0.26 - (len(lines) - 1) * 12.5
        for i, s in enumerate(lines):
            f.text(cx, y0 + i * 25, s, size=size)


def _store(f, x1, x2, y, label, size=19):
    f.line(x1, y, x2, y, sw=1.8)
    f.line(x1, y + 7, x2, y + 7, sw=1.8)
    f.text((x1 + x2) / 2.0, y - 20, label, size=size)


def f_yiceng(Fig):
    f = Fig(989, 602)
    S = 19
    # 外部实体
    f.rect(5, 44, 53, 510, sw=1.8)
    vt(f, 31, 309, "管理员", 22, 31)
    f.rect(928, 8, 45, 568, sw=1.8)
    vt(f, 950, 292, "读者", 21, 30)

    # 数据存储
    _store(f, 252, 365, 222, "图书信息", S)
    _store(f, 420, 530, 200, "借阅信息", S)
    _store(f, 420, 536, 433, "读者信息", S)

    # 加工
    _proc(f, 315, 88, 65, "2", ["图书信息", "维护"], 19)
    _proc(f, 541, 64, 50, "3", ["借书"], 19)
    _proc(f, 338, 358, 76, "6", ["管理员的", "信息查询"], 19)
    _proc(f, 350, 536, 60, "1", ["读者信息", "维护"], 19)
    _proc(f, 687, 208, 50, "4", ["续借"], 19)
    _proc(f, 689, 360, 52, "5", ["还书"], 19)
    _proc(f, 635, 512, 60, "7", ["读者的", "信息查询"], 19)

    # 左侧数据流
    f.arrow(58, 78, 248, 78, sw=1.6)
    mid(f, 165, 57, "图书信息维护事务", S)
    f.arrow(58, 305, 260, 305, sw=1.6)
    mid(f, 160, 285, "管理员查询事务", S)
    f.arrow(262, 355, 60, 355, sw=1.6)
    mid(f, 160, 335, "管理员查询结果", S)
    f.arrow(58, 515, 295, 515, sw=1.6)
    mid(f, 180, 494, "读者信息维护事务", S)

    # 右侧数据流
    f.arrow(927, 34, 590, 34, sw=1.6)
    mid(f, 760, 15, "读者号", S)
    f.arrow(927, 65, 591, 65, sw=1.6)
    mid(f, 762, 47, "欲借书条码号", S)
    f.arrow(592, 96, 925, 96, sw=1.6)
    mid(f, 760, 78, "超期信息", S)
    f.arrow(592, 122, 925, 122, sw=1.6)
    mid(f, 760, 104, "借阅信息", S)
    f.arrow(735, 187, 925, 187, sw=1.6)
    mid(f, 830, 168, "续借信息", S)
    f.arrow(925, 227, 738, 227, sw=1.6)
    mid(f, 830, 209, "续借事务", S)
    f.arrow(740, 356, 925, 356, sw=1.6)
    mid(f, 830, 337, "还书信息", S)
    f.arrow(925, 390, 742, 390, sw=1.6)
    mid(f, 830, 371, "欲还书条码号", S)
    f.arrow(925, 428, 740, 424, sw=1.6)
    mid(f, 830, 410, "支付罚款事务", S)
    f.arrow(925, 497, 697, 497, sw=1.6)
    mid(f, 810, 478, "读者查询事务", S)
    f.arrow(695, 535, 925, 535, sw=1.6)
    mid(f, 810, 517, "读者查询结果", S)

    # 内部数据流
    f.arrow(315, 153, 315, 214, sw=1.6)
    f.arrow(302, 233, 328, 283, sw=1.6)
    f.poly([(540, 108), (517, 162)], sw=1.6, head=9)
    f.arrow(420, 205, 392, 292, sw=1.6)
    f.arrow(443, 209, 606, 453, sw=1.6)
    f.arrow(640, 330, 538, 210, sw=1.6)
    f.arrow(655, 330, 628, 452, sw=1.6)
    f.arrow(525, 431, 420, 358, sw=1.6)
    f.arrow(392, 492, 452, 443, sw=1.6)
    f.arrow(540, 444, 585, 468, sw=1.6)
    f.arrow(637, 192, 535, 192, sw=1.6)

    # 逻辑符号
    f.text(612, 102, "⊕", size=30)
    f.text(540, 132, "*", size=30)
    f.text(292, 291, "*", size=30)
    f.text(683, 150, "*", size=30)
    f.text(700, 296, "*", size=30)
    f.text(752, 460, "*", size=30)
    return f


# ------------------------------------------------------------------ ATM 用例图（复用）

def atm_uc(f, ox, oy, k, fs):
    """(ox,oy) 为系统边界左上角，k 为缩放，fs 为用例名字号。"""
    def P(x, y):
        return (ox + x * k, oy + y * k)

    f.rect(ox, oy, 353 * k, 305 * k, sw=1.6)
    x, y = P(178, 22)
    f.text(x, y, "ATM Server", size=fs * 1.55, bold=True)

    ucs = [("服务启动", 109, 45, 41, 15), ("服务停止", 109, 91, 41, 16),
           ("创建会话", 111, 148, 41, 15), ("菜单事务", 116, 214, 41, 16),
           ("错误处理", 275, 142, 41, 15), ("查询", 283, 188, 40, 15),
           ("转账", 284, 226, 40, 15), ("取款", 158, 279, 40, 15),
           ("存款", 285, 279, 40, 15)]
    for name, cx, cy, rx, ry in ucs:
        f.ellipse(ox + cx * k, oy + cy * k, rx * k, ry * k, sw=1.4)
        f.text(ox + cx * k, oy + cy * k, name, size=fs)

    # 参与者
    for label, hy in (("管理员", 22), ("客户", 134), ("银行", 238)):
        hx = ox - 63 * k
        f.circle(hx, oy + hy * k, 7 * k, sw=1.4)
        f.line(hx, oy + (hy + 7) * k, hx, oy + (hy + 28) * k, sw=1.4)
        f.line(hx - 14 * k, oy + (hy + 14) * k, hx + 14 * k, oy + (hy + 14) * k, sw=1.4)
        f.line(hx, oy + (hy + 28) * k, hx - 12 * k, oy + (hy + 42) * k, sw=1.4)
        f.line(hx, oy + (hy + 28) * k, hx + 12 * k, oy + (hy + 42) * k, sw=1.4)
        f.text(hx, oy + (hy + 54) * k, label, size=fs * 0.92)

    # 参与者与用例的联系
    f.line(ox - 49 * k, oy + 36 * k, ox + 68 * k, oy + 45 * k, sw=1.4)
    f.line(ox - 49 * k, oy + 36 * k, ox + 68 * k, oy + 91 * k, sw=1.4)
    f.line(ox - 49 * k, oy + 148 * k, ox + 70 * k, oy + 148 * k, sw=1.4)
    f.line(ox - 49 * k, oy + 252 * k, ox + 75 * k, oy + 214 * k, sw=1.4)

    # include / extend
    f.arrow(ox + 111 * k, oy + 163 * k, ox + 113 * k, oy + 197 * k,
            sw=1.3, dash="5,4", head=8)
    f.text(ox + 104 * k, oy + 180 * k, "<<include>>", size=fs * 0.90)
    f.arrow(ox + 250 * k, oy + 152 * k, ox + 158 * k, oy + 204 * k,
            sw=1.3, dash="5,4", head=8)
    f.text(ox + 208 * k, oy + 180 * k, "<<extend>>", size=fs * 0.90)

    # 查询/转账/取款/存款 -> 菜单事务
    for sx, sy in ((242, 188), (244, 226), (158, 264), (245, 279)):
        f.arrow(ox + sx * k, oy + sy * k, ox + 157 * k, oy + 212 * k,
                sw=1.4, head=8)


# ------------------------------------------------------------------ 5 图形描述需求

def f_txxxq(Fig):
    f = Fig(1024, 724)
    chev(f, 42, 52, 42)
    tx(f, 148, 52, "需求的描述方法", 44, color=TITLE, bold=True)
    logo(f, 720, 45, 1.0)
    tx(f, 104, 164, "图形模型", 38, bold=True)

    # 左：用例图
    atm_uc(f, 128, 287, 1.0, 12)

    # 右：顺序图
    L1, L2, L3 = 516, 672, 822
    actor(f, L1, 118, None, r=7)
    f.rect(645, 118, 63, 29, sw=1.2)
    f.text(676, 132, "ATM", size=16)
    f.rect(799, 118, 65, 29, sw=1.2)
    f.text(831, 132, "Database", size=14)
    for x in (L1, L2, L3):
        f.line(x, 160, x, 700, sw=1.0)

    bars = [(509, 184, 15, 176), (667, 184, 13, 176), (816, 199, 15, 50),
            (509, 384, 15, 85), (667, 375, 15, 159), (816, 378, 15, 50),
            (509, 496, 15, 59), (667, 558, 17, 138), (816, 490, 15, 29),
            (509, 563, 15, 133)]
    for bx, by, bw, bh in bars:
        f.rect(bx, by, bw, bh, fill="#ffffff", sw=1.2)

    def msg(y, x1, x2, label, size=16):
        f.arrow(x1, y, x2, y, sw=1.2, head=8)
        f.text((x1 + x2) / 2.0, y - 14, label, size=size)

    msg(204, 505, 666, "Card")
    msg(212, 682, 814, "Card number", 15)
    msg(246, 814, 682, "Card OK", 15)
    msg(262, 666, 529, "PIN request", 15)
    msg(288, 529, 666, "PIN")
    msg(310, 666, 529, "Option menu", 15)
    f.text(597, 326, "<<exception>>", size=13)
    f.text(597, 343, "invalid card", size=14)
    f.arrow(666, 358, 529, 358, sw=1.2, head=8)
    f.arrow(814, 292, 872, 292, sw=1.2, dash="5,4", head=8)
    f.rect(871, 275, 100, 36, fill="#e8e8e8", sw=1.2)
    f.text(921, 293, "Validate card", size=12)

    msg(386, 505, 666, "Withdraw request", 15)
    msg(392, 682, 814, "Balance request", 15)
    msg(420, 814, 682, "Balance")
    msg(452, 666, 529, "Amount request", 15)
    f.arrow(814, 440, 872, 440, sw=1.2, dash="5,4", head=8)
    f.rect(871, 426, 100, 34, fill="#e8e8e8", sw=1.2)
    f.text(921, 443, "Handle request", size=12)
    msg(466, 529, 666, "Amount")
    msg(492, 682, 814, "Debit (amount)", 15)
    msg(520, 814, 682, "Debit response", 15)
    f.text(597, 530, "<<exception>>", size=13)
    f.text(597, 547, "insufficient cash", size=14)
    f.arrow(666, 562, 529, 562, sw=1.2, head=8)

    msg(590, 666, 529, "Card")
    msg(616, 529, 666, "Card removed", 15)
    f.arrow(814, 612, 872, 612, sw=1.2, dash="5,4", head=8)
    f.rect(871, 594, 100, 38, fill="#e8e8e8", sw=1.2)
    f.text(921, 606, "Complete", size=12)
    f.text(921, 620, "transaction", size=12)
    msg(640, 666, 529, "Cash")
    msg(660, 529, 666, "Cash removed", 15)
    msg(690, 666, 529, "Receipt")
    return f


# ------------------------------------------------------------------ 6 ER图

def f_er(Fig):
    f = Fig(1344, 647)
    A = 24  # 属性字号

    def ent(cx, cy, w, h, s):
        f.rect(cx - w / 2, cy - h / 2, w, h, fill="#ffffff", sw=1.6)
        f.text(cx, cy, s, size=A + 2)

    def rel(cx, cy, w, h, s):
        f.poly([(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2),
                (cx - w / 2, cy), (cx, cy - h / 2)], sw=1.6, fill="#ffffff")
        f.text(cx, cy, s, size=A + 2)

    def att(cx, cy, s, rx=None):
        if rx is None:
            rx = max(34, A * 0.56 * len(s) + 12)
        f.ellipse(cx, cy, rx, 20, sw=1.5)
        f.text(cx, cy, s, size=A)

    # ---- 实体与联系
    ent(241, 182, 101, 48, "读者")
    rel(483, 182, 84, 62, "借阅")
    ent(773, 184, 137, 46, "单本图书")
    rel(953, 184, 86, 52, "馆藏")
    ent(1134, 184, 107, 52, "图书")
    rel(230, 345, 84, 48, "属于")
    ent(241, 494, 137, 46, "读者类别")
    ent(773, 494, 107, 46, "管理员")
    rel(955, 492, 84, 48, "管理")
    ent(1130, 494, 129, 46, "存放区域")
    rel(1133, 345, 84, 48, "存放")

    # ---- 读者的属性
    for cx, cy, s in ((116, 63, "读者号"), (229, 63, "姓名"), (341, 89, "密码"),
                      (94, 201, "电话"), (94, 133, "性别"), (129, 280, "身份证号")):
        att(cx, cy, s)
    # ---- 借阅的属性
    for cx, cy, s in ((455, 63, "借书日期"), (601, 64, "还书日期"),
                      (760, 68, "是否归还"), (908, 74, "条码号"),
                      (354, 278, "续借日期"), (469, 330, "罚款金额"),
                      (607, 295, "是否交罚款")):
        att(cx, cy, s)
    # ---- 单本图书
    att(771, 282, "图书状态")
    # ---- 图书的属性
    for cx, cy, s in ((1024, 97, "书号"), (1136, 75, "书名"), (1258, 72, "作者"),
                      (1273, 142, "单价"), (1267, 223, "类别"),
                      (1233, 297, "出版社"), (1008, 273, "出版日期")):
        att(cx, cy, s)
    # ---- 读者类别
    for cx, cy, s in ((94, 406, "类别号"), (391, 411, "最大借书天数"),
                      (101, 570, "类别名"), (241, 584, "最大续借天数"),
                      (474, 584, "最大借书数量")):
        att(cx, cy, s)
    # ---- 管理员
    for cx, cy, s in ((695, 393, "编号"), (856, 396, "电话"),
                      (691, 566, "姓名"), (854, 566, "密码")):
        att(cx, cy, s)
    # ---- 存放区域
    for cx, cy, s in ((1011, 570, "最大存放数量"), (1221, 570, "区域名")):
        att(cx, cy, s)

    # ---- 连线
    links = [
        (116, 63, 241, 158), (229, 63, 241, 158), (341, 89, 255, 170),
        (94, 133, 196, 170), (94, 201, 196, 176), (129, 280, 212, 205),
        (455, 63, 474, 152), (601, 64, 497, 156), (760, 68, 520, 168),
        (908, 74, 540, 175), (354, 278, 460, 205), (469, 330, 476, 212),
        (607, 295, 507, 208), (771, 282, 773, 206),
        (1024, 97, 1096, 165), (1136, 75, 1134, 160), (1258, 72, 1160, 170),
        (1273, 142, 1178, 180), (1267, 223, 1170, 205), (1233, 297, 1146, 208),
        (1008, 273, 1096, 200), (94, 406, 200, 480), (391, 411, 292, 476),
        (101, 570, 196, 512), (241, 584, 255, 514), (474, 584, 300, 512),
        (695, 393, 756, 474), (856, 396, 792, 474), (691, 566, 762, 512),
        (854, 566, 788, 512), (1011, 570, 1096, 512), (1221, 570, 1160, 512),
        (241, 206, 230, 320), (241, 369, 241, 471), (773, 207, 773, 471),
        (1134, 210, 1133, 321), (1133, 369, 1133, 471), (902, 492, 913, 492),
    ]
    for x1, y1, x2, y2 in links:
        f.line(x1, y1, x2, y2, sw=1.4)

    # ---- 基数
    mid(f, 350, 168, "m", 24)
    mid(f, 623, 166, "n", 24)
    mid(f, 874, 168, "m", 24)
    mid(f, 1040, 166, "1", 24)
    mid(f, 210, 258, "n", 24)
    mid(f, 254, 417, "1", 24)
    mid(f, 874, 480, "n", 24)
    mid(f, 1033, 480, "1", 24)
    mid(f, 1122, 273, "n", 24)
    mid(f, 1122, 420, "1", 24)
    return f


# ------------------------------------------------------------------ 7 状态图画法

def f_ztgf(Fig):
    f = Fig(1270, 323)
    S = 38
    f.circle(10, 168, 10, fill=INK, sw=1.2)
    f.arrow(21, 168, 227, 168, sw=1.8)

    def box(x, n):
        f.rect(x, 13, 250, 297, rx=30, sw=1.8)
        f.line(x, 98, x + 250, 98, sw=1.8)
        f.line(x, 205, x + 250, 205, sw=1.8)
        f.text(x + 125, 49, "状态%s" % n, size=S)
        f.text(x + 125, 154, "状态变量%s" % n, size=S)
        f.text(x + 125, 260, "活动表%s" % n, size=S)

    box(230, "1")
    box(755, "2")
    tx(f, 30, 136, "初始事件", 37)
    f.text(592, 135, "事件表达式", 37)
    f.text(1111, 137, "结束事件", 37)
    f.arrow(480, 158, 750, 158, sw=1.8)
    f.arrow(1005, 158, 1214, 158, sw=1.8)
    f.circle(1235, 165, 17, sw=1.8)
    f.circle(1235, 165, 9, fill=INK, sw=1.0)
    return f


# ------------------------------------------------------------------ 8 状态图

def f_zhuangtai(Fig):
    f = Fig(1340, 731)
    S = 29

    def st(x, y, w, h, lines, split=None):
        f.rect(x, y, w, h, rx=22, sw=1.8)
        if split is None:
            n = len(lines)
            step = S * 1.45
            y0 = y + h / 2 - step * (n - 1) / 2
            for i, s in enumerate(lines):
                f.text(x + w / 2, y0 + i * step, s, size=S)
        else:
            f.line(x, y + split, x + w, y + split, sw=1.8)
            f.text(x + w / 2, y + split / 2, lines[0], size=S)
            f.text(x + w / 2, y + split + (h - split) / 2, lines[1], size=S)

    f.circle(65, 84, 29, fill=INK, sw=1.2)
    f.arrow(95, 84, 203, 78, sw=1.8)

    st(205, 23, 270, 125, ["读者主界面", "do: 等待功能选择"], 58)
    st(661, 27, 220, 114, ["借书界面", "do: 等待刷卡"], 55)
    st(1079, 34, 232, 110, ["检查是否有", "超期未还图书"])
    st(650, 198, 224, 72, ["显示超期信息"])
    st(1113, 270, 194, 110, ["检查借书量", "是否已满"])
    st(654, 338, 228, 76, ["提示不能借阅", "的原因"])
    st(217, 410, 220, 106, ["借书界面", "do: 是否继续"], 52)
    st(1060, 600, 251, 103, ["借书界面", "do: 等待图书扫码"], 50)
    st(631, 616, 232, 87, ["写入借阅信息", "修改图书状态"])
    st(228, 616, 209, 84, ["显示借阅信息"])

    # 迁移
    f.arrow(475, 78, 659, 78, sw=1.8)
    mid(f, 558, 62, "选择借书", S)
    f.arrow(881, 78, 1077, 78, sw=1.8)
    mid(f, 975, 62, "刷卡", S)

    f.poly([(1080, 144), (1080, 230), (876, 230)], sw=1.8, head=9)
    mid(f, 1100, 190, "是", S)
    f.arrow(1216, 144, 1216, 268, sw=1.8)
    mid(f, 1236, 200, "否", S)
    f.arrow(1113, 343, 886, 343, sw=1.8)
    mid(f, 1074, 328, "是", S)

    # 提示不能借阅 -> 读者主界面
    f.poly([(654, 376), (441, 376), (441, 150)], sw=1.8, head=9)
    mid(f, 555, 358, "确认", S)
    # 显示超期信息 -> 读者主界面
    f.poly([(650, 236), (384, 236), (384, 150)], sw=1.8, head=9)
    mid(f, 552, 220, "确认", S)
    # 借书界面(是否继续) -> 读者主界面
    f.arrow(315, 410, 315, 150, sw=1.8)
    mid(f, 285, 300, "退出", S)

    # 继续借书
    f.poly([(437, 452), (1123, 452), (1123, 382)], sw=1.8, head=9)
    mid(f, 566, 436, "继续借书", S)
    f.arrow(1216, 380, 1216, 598, sw=1.8)
    mid(f, 1236, 437, "否", S)
    f.arrow(1060, 650, 865, 650, sw=1.8)
    mid(f, 980, 634, "图书扫码", S)
    f.arrow(631, 660, 439, 660, sw=1.8)
    f.arrow(342, 616, 342, 518, sw=1.8)
    mid(f, 370, 566, "确认", S)
    return f


# ------------------------------------------------------------------ 9 判定表

def f_pdb(Fig):
    f = Fig(1664, 905)
    XS = [71, 185, 701, 920, 1139, 1359, 1578]
    YS = [60, 152, 291, 383, 475, 637, 800]
    W, H = XS[-1] - XS[0], YS[-1] - YS[0]
    f.rect(XS[0], YS[0], W, H, fill="#ffffff", sw=2.6)
    for x in XS[1:-1]:
        f.line(x, YS[0], x, YS[-1], sw=2.0)
    for y in YS[1:-1]:
        f.line(XS[0], y, XS[-1], y, sw=2.0)

    # 规则号
    for i, n in enumerate("1234"):
        f.text((XS[2 + i] + XS[3 + i]) / 2, (YS[0] + YS[1]) / 2, n, size=54, bold=True)

    # 竖排“条件”“动作”
    vt(f, 128, 246, "条件", 62, 92)
    vt(f, 128, 566, "动作", 62, 92)

    # 条件桩
    conds = [("订货额", ["≥1000", "≥1000", "≥1000", "<1000"], 1, 54),
             ("顾客信誉", ["好", "不好", "不好", "-"], 2, 50),
             ("老顾客", ["-", "是", "不是", "-"], 3, 50)]
    for name, vals, r, vs in conds:
        f.text((XS[1] + XS[2]) / 2, (YS[r] + YS[r + 1]) / 2, name, size=54)
        for i, v in enumerate(vals):
            f.text((XS[2 + i] + XS[3 + i]) / 2, (YS[r] + YS[r + 1]) / 2, v, size=vs)

    # 动作桩
    acts = [("订单设“优先”标", "志", ["√", "√", "", ""], 4),
            ("订单设“正常”标", "志", ["", "", "√", "√"], 5)]
    for l1, l2, vals, r in acts:
        cx = (XS[1] + XS[2]) / 2
        f.text(cx, (YS[r] + YS[r + 1]) / 2 - 38, l1, size=50)
        f.text(cx, (YS[r] + YS[r + 1]) / 2 + 38, l2, size=50)
        for i, v in enumerate(vals):
            if v:
                f.text((XS[2 + i] + XS[3 + i]) / 2, (YS[r] + YS[r + 1]) / 2, v, size=54)
    return f


# ------------------------------------------------------------------ 10 判定树

def f_pds(Fig):
    f = Fig(1230, 521)
    S = 34
    mid(f, 300, 48, "产品种类", 36)
    mid(f, 600, 48, "超产数量", 36)
    mid(f, 1040, 48, "奖金数额", 36)

    mid(f, 120, 268, "奖金政策", 34)
    mid(f, 336, 168, "产品A", 34)
    mid(f, 336, 346, "产品B", 34)

    # 根到两类产品
    f.line(196, 258, 288, 180, sw=1.6)
    f.line(196, 278, 288, 334, sw=1.6)

    A = [("1<N≤50", "N"), ("50<N≤100", "50+1.25(N-50)"),
         ("N>100", "112.5+1.5(N-100)")]
    B = [("1<N≤25", "2N"), ("25<N≤50", "50+2.5(N-25)"),
         ("N>50", "112.5+3(N-50)")]
    for (cy0, items) in ((168, A), (346, B)):
        ys = [cy0 - 50, cy0, cy0 + 50]
        for (c, fm), y in zip(items, ys):
            f.line(390, cy0, 480, y, sw=1.6)
            tx(f, 494, y, c, S)
            f.line(716, y, 848, y, sw=1.6)
            tx(f, 862, y, fm, S)
    return f


# ------------------------------------------------------------------ 11 用例图

def f_yongli(Fig):
    f = Fig(1024, 724)
    chev(f, 42, 52, 42)
    tx(f, 148, 52, "建立用例模型", 44, color=TITLE, bold=True)
    logo(f, 720, 45, 1.0)

    S = 26
    for y, s in ((160, "用例图从用户的观点描述系统"), (212, "的功能，由一组用例、参与者"),
                 (264, "以及它们之间关系所组成。")):
        tx(f, 108, y, s, S, bold=True)

    # 第一条要点
    f.circle(90, 322, 3.5, fill=RED, sw=1.0)
    tx(f, 108, 320, "用例", S, color=RED, bold=True)
    tx(f, 160, 320, "是从用户角度描述系", S, bold=True)
    tx(f, 108, 372, "统的行为，一个功能描述", S, bold=True)
    tx(f, 108, 424, "成一系列事件", S, bold=True)

    # 第二条要点
    f.circle(90, 492, 3.5, fill=RED, sw=1.0)
    tx(f, 108, 490, "参与者", S, color=RED, bold=True)
    tx(f, 186, 490, "是与系统交互的外", S, bold=True)
    tx(f, 108, 542, "部实体（使用系统的用户、", S, bold=True)
    tx(f, 108, 594, "系统交互的其他外部系统、", S, bold=True)
    tx(f, 108, 646, "硬件设备或组织机构）", S, bold=True)

    atm_uc(f, 572, 212, 1.126, 13)
    return f


FIGS = [
    ("建模规范1", f_mjgf1),
    ("建模规范2", f_mjgf2),
    ("顶层图", f_dingceng),
    ("一层数据流图", f_yiceng),
    ("图形描述需求", f_txxxq),
    ("ER图", f_er),
    ("状态图画法", f_ztgf),
    ("状态图", f_zhuangtai),
    ("判定表", f_pdb),
    ("判定树", f_pds),
    ("用例图", f_yongli),
]
