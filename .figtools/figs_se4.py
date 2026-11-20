# -*- coding: utf-8 -*-
"""软件工程导论插图 SVG 重绘 —— 第 4 批（模块结构 / N-S / PAD / 复杂度 / 测试）"""
import math

import se_kit as K
from se_kit import Fig, INK, BOXF, BOXW, BLUE, GREEN, YELLOW, PINK, RED, GRAY

FONT = "'Microsoft YaHei', 'SimHei', sans-serif"
DASH = "6,5"


# ---------------------------------------------------------------- 通用图元

def T(f, x, y, s, size=40, anchor="middle", bold=False, color=INK, italic=False):
    f.text(x, y, s, size=size, anchor=anchor, bold=bold, color=color, italic=italic)


def frame(f, x, y, w, h, sw=3.0, fill="none", rx=0, dash=None):
    f.rect(x, y, w, h, fill=fill, sw=sw, rx=rx, dash=dash)


def tbox(f, x, y, w, h, lines, size=40, sw=3.0, lh=1.3, fill="none",
         bold=False, color=INK, anchor="middle"):
    """矩形 + 居中的一行或多行文字。"""
    f.rect(x, y, w, h, fill=fill, sw=sw)
    if isinstance(lines, str):
        lines = [lines]
    n = len(lines)
    step = size * lh
    y0 = y + h / 2 - step * (n - 1) / 2
    for i, s in enumerate(lines):
        if anchor == "start":
            T(f, x + 12, y0 + i * step, s, size, "start", bold, color)
        else:
            T(f, x + w / 2, y0 + i * step, s, size, "middle", bold, color)


def vstack(f, cx, y0, chars, size, gap=1.0, color=INK, bold=False):
    """竖排（逐字正立）文字。返回结束 y。"""
    y = y0
    for c in chars:
        T(f, cx, y, c, size, "middle", bold, color)
        y += size * gap
    return y


def dia4(f, cx, cy, hw, hh, sw=3.0, fill="none"):
    f.poly([(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy),
            (cx, cy - hh)], sw=sw, fill=fill)


def para(f, x0, y0, x1, y1, lean, sw=3.0, fill="none"):
    """平行四边形：上下边水平，右端左斜 lean。"""
    f.poly([(x0, y0), (x0 + lean, y0), (x1, y1), (x1 - lean, y1), (x0, y0)],
           sw=sw, fill=fill)


def brace_v(f, x, y1, y2, w=34, sw=2.6, side=-1, color=INK):
    """竖向花括号：side=-1 尖朝左，side=1 尖朝右。"""
    ym = (y1 + y2) / 2
    d = side * w
    pts = [(x + d, y1), (x + d * 0.45, y1 + (ym - y1) * 0.12),
           (x + d * 0.45, ym - (ym - y1) * 0.10), (x, ym),
           (x + d * 0.45, ym + (y2 - ym) * 0.10),
           (x + d * 0.45, y2 - (y2 - ym) * 0.12), (x + d, y2)]
    f.poly(pts, sw=sw, fill="none")


def block_arrow(f, x1, y, x2, thick=26, head=34, fill="#a8c0e8", sw=1.2):
    """水平块箭头（指向 x2）。"""
    s = 1 if x2 > x1 else -1
    xs = x2 - s * head
    pts = [(x1, y - thick / 2), (xs, y - thick / 2), (xs, y - head / 2),
           (x2, y), (xs, y + head / 2), (xs, y + thick / 2), (x1, y + thick / 2)]
    f.poly(pts + [pts[0]], sw=sw, fill=fill)


def circled(f, cx, cy, r, s, size=34):
    f.circle(cx, cy, r, fill="#ffffff", sw=2.2)
    T(f, cx, cy, s, size)


def arr(f, x1, y1, x2, y2, sw=3.0, head=28, w=0.40, dash=None, color=INK):
    """带实心三角箭头的连线（SVG 与预览一致）。"""
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy) or 1
    ux, uy = dx / d, dy / d
    f.line(x1, y1, x2 - ux * head * 0.9, y2 - uy * head * 0.9, sw=sw, dash=dash)
    px, py = -uy, ux
    hw = head * w
    f.poly([(x2, y2),
            (x2 - ux * head + px * hw, y2 - uy * head + py * hw),
            (x2 - ux * head - px * hw, y2 - uy * head - py * hw),
            (x2, y2)], fill=color, sw=1.0)


def chain(f, parent_cx, parent_bottom, bus_y, kids, kid_top,
          sw=3.0, head=16, arrow=False, fill_bus=True):
    """模块结构图：父框底部 -> 横线 -> 各子框顶部竖线。kids 为子框中心 x 列表。"""
    f.line(parent_cx, parent_bottom, parent_cx, bus_y, sw=sw)
    if fill_bus:
        f.line(min(kids + [parent_cx]), bus_y, max(kids + [parent_cx]), bus_y, sw=sw)
    for kx in kids:
        if arrow:
            f.arrow(kx, bus_y, kx, kid_top, sw=sw, head=head)
        else:
            f.line(kx, bus_y, kx, kid_top, sw=sw)


# ---------------------------------------------------------------- 1 上层模块

def f_top(Fig):
    f = Fig(1374, 456)
    tbox(f, 421, 38, 485, 114, "图书借阅系统", size=60)
    for x in (4, 482, 941):
        tbox(f, x, 298, 364, 114, "输出数据" if x == 941 else
             ("输入数据" if x == 4 else "调度"), size=60)
    chain(f, 664, 152, 220, [186, 664, 1123], 298)
    return f


# ---------------------------------------------------------------- 2 下层模块

def f_lower(Fig):
    f = Fig(1919, 1247)
    tbox(f, 845, 32, 338, 88, "输入数据", size=52)
    row1 = [(72, 317), (342, 585), (624, 760), (785, 975), (1000, 1136),
            (1161, 1338), (1356, 1640), (1658, 1888)]
    txt1 = [["图书信息", "维护事务"], ["读者信息", "维护事务"], ["读者", "号"],
            ["图书条", "码号"], ["续借", "事务"], ["支付", "事务"],
            ["管理员", "查询事务"], ["读者", "查询事务"]]
    for (x0, x1), lines in zip(row1, txt1):
        tbox(f, x0, 234, x1 - x0, 144, lines, size=48, lh=1.15)
    chain(f, 1014, 120, 172, [(a + b) // 2 for a, b in row1], 234)

    tbox(f, 814, 448, 337, 88, "输出数据", size=52)
    row2 = [(114, 358), (410, 654), (706, 949), (998, 1248), (1290, 1540),
            (1579, 1823)]
    txt2 = ["借阅信息", "超期信息", "续借信息", "还书信息",
            ["读者的查", "询结果"], ["管理员的", "查询结果"]]
    for (x0, x1), s in zip(row2, txt2):
        tbox(f, x0, 650, x1 - x0, 144, s, size=46, lh=1.2)
    chain(f, 982, 536, 588, [(a + b) // 2 for a, b in row2], 650)

    tbox(f, 800, 880, 348, 84, "调度", size=52)
    row3 = [(118, 362), (412, 650), (696, 850), (897, 1051), (1105, 1259),
            (1299, 1543), (1589, 1826)]
    txt3 = [["图书信息", "维护"], ["读者信息", "维护"], "借书", "续借", "还书",
            ["读者的", "信息查询"], ["管理员的", "信息查询"]]
    for (x0, x1), s in zip(row3, txt3):
        tbox(f, x0, 1088, x1 - x0, 140, s, size=46, lh=1.2)
    chain(f, 974, 964, 1016, [(a + b) // 2 for a, b in row3], 1088)
    return f


# ---------------------------------------------------------------- 3 N-S 图

def f_ns(Fig):
    f = Fig(1596, 938)
    sw = 3.0
    # 外框与横带
    f.rect(54, 26, 1501, 881, fill="none", sw=sw)
    for y, x0, x1 in ((126, 54, 1555), (231, 54, 1448), (336, 54, 1449),
                      (466, 54, 1126), (606, 54, 843), (800, 54, 1448)):
        f.line(x0, y, x1, y, sw=sw)
    # 竖线
    f.line(450, 606, 450, 800, sw=sw)
    f.line(844, 466, 844, 800, sw=sw)
    f.line(1126, 336, 1126, 800, sw=sw)
    f.line(1448, 231, 1448, 906, sw=sw)

    T(f, 804, 78, "输入year", 46)
    T(f, 810, 180, "DO WHILE year不等于0", 49)
    T(f, 804, 855, "输入year", 46)

    # 条件 1：year能被4整除
    f.line(54, 231, 1126, 334, sw=sw)
    f.line(1126, 334, 1448, 231, sw=sw)
    T(f, 1080, 272, "year能被4整除", 48)
    T(f, 95, 292, "是", 46)
    T(f, 1385, 292, "否", 46)

    # 条件 2：year能被100整除
    f.line(54, 336, 843, 464, sw=sw)
    f.line(843, 464, 1126, 336, sw=sw)
    T(f, 880, 380, "year能被100整除", 48)
    T(f, 95, 424, "是", 46)
    T(f, 1040, 424, "否", 46)

    # 条件 3：year能被400整除
    f.line(54, 466, 450, 606, sw=sw)
    f.line(450, 606, 843, 466, sw=sw)
    T(f, 500, 500, "year能被400", 46)
    T(f, 500, 552, "整除", 46)
    T(f, 95, 560, "是", 46)
    T(f, 765, 560, "否", 46)

    # 输出分支
    T(f, 252, 672, "输出year", 50)
    T(f, 252, 728, "是闰年", 50)
    T(f, 646, 672, "输出year", 50)
    T(f, 646, 728, "不是闰年", 50)
    T(f, 985, 620, "输出year", 50)
    T(f, 985, 676, "是闰年", 50)
    T(f, 1287, 560, "输出year", 50)
    T(f, 1287, 616, "不是闰年", 50)
    return f


# ---------------------------------------------------------------- 4 PAD 图

def f_pad(Fig):
    f = Fig(1606, 973)
    sw = 2.6
    # 主竖线
    f.line(84, 38, 84, 930, sw=sw)
    f.line(486, 38, 486, 930, sw=sw)
    f.line(720, 38, 720, 617, sw=sw)
    f.line(720, 707, 720, 817, sw=sw)
    f.line(956, 38, 956, 394, sw=sw)
    f.line(1184, 38, 1184, 166, sw=sw)
    f.line(1192, 250, 1192, 368, sw=sw)
    f.line(960, 485, 960, 601, sw=sw)

    # 顺序框
    f.rect(84, 94, 190, 62, fill="none", sw=sw)
    T(f, 112, 126, "输入year", 32, "start")
    # WHILE 框（右端小环）
    f.rect(84, 206, 336, 62, fill="none", sw=sw)
    f.line(398, 206, 398, 268, sw=sw)
    f.line(420, 206, 420, 268, sw=sw)
    T(f, 92, 237, "WHILE year不等于0", 33, "start")
    f.line(420, 237, 486, 237, sw=sw)

    # 结束顺序框
    f.rect(486, 842, 191, 64, fill="none", sw=sw)
    T(f, 512, 875, "输入year", 32, "start")

    # 选择 1：year能被4整除（框 486..720, 595..728）
    f.line(486, 595, 720, 595, sw=sw)
    f.line(486, 728, 720, 728, sw=sw)
    f.poly([(697, 595), (628, 662), (687, 728)], sw=sw)
    T(f, 505, 632, "year能被", 33, "start")
    T(f, 528, 690, "4整除", 33, "start")
    f.rect(720, 732, 302, 64, fill="none", sw=sw)
    T(f, 733, 763, "输出year不是闰年", 33, "start")

    # 选择 2：year能被100整除（框 720..956, 372..506）
    f.line(720, 372, 956, 372, sw=sw)
    f.line(720, 506, 956, 506, sw=sw)
    f.poly([(941, 372), (880, 439), (934, 506)], sw=sw)
    T(f, 740, 410, "year能被", 33, "start")
    T(f, 756, 466, "100整除", 33, "start")
    f.rect(960, 510, 258, 62, fill="none", sw=sw)
    T(f, 982, 541, "输出year是闰年", 33, "start")

    # 选择 3：year能被400整除（框 955..1192, 138..272）
    f.line(955, 138, 1185, 138, sw=sw)
    f.line(955, 272, 1192, 272, sw=sw)
    f.poly([(1185, 138), (1120, 205), (1185, 272)], sw=sw)
    T(f, 975, 176, "year能被", 33, "start")
    T(f, 988, 232, "400整除", 33, "start")
    f.rect(1184, 64, 262, 63, fill="none", sw=sw)
    T(f, 1204, 96, "输出year是闰年", 33, "start")
    f.rect(1192, 284, 310, 62, fill="none", sw=sw)
    T(f, 1214, 315, "输出year不是闰年", 33, "start")
    return f


# ---------------------------------------------------------------- 5 环路复杂度

def f_cyc(Fig):
    f = Fig(1857, 986)
    sw = 3.0
    # 开始
    f.rect(400, 55, 155, 82, fill="none", sw=sw, rx=40)
    T(f, 478, 96, "开始", 58)
    arr(f, 478, 137, 478, 192, sw=sw, head=26)

    # 输入 x
    f.poly([(397, 195), (602, 195), (559, 258), (358, 258), (397, 195)], sw=sw)
    T(f, 452, 226, "输入", 56)
    T(f, 522, 228, "x", 58, italic=True)
    arr(f, 478, 258, 478, 315, sw=sw, head=26)

    # 判断 x<=2
    dia4(f, 478, 368, 99, 50, sw=sw)
    T(f, 440, 372, "x", 46, italic=True)
    T(f, 468, 370, "≤", 46)
    T(f, 505, 372, "2?", 46)
    T(f, 312, 330, "是", 46)
    T(f, 632, 330, "否", 46)
    f.line(378, 368, 182, 368, sw=sw)
    arr(f, 182, 368, 182, 478, sw=sw, head=26)

    # 判断 x<=5
    f.line(577, 368, 683, 368, sw=sw)
    arr(f, 683, 368, 683, 434, sw=sw, head=26)
    dia4(f, 683, 486, 99, 50, sw=sw)
    T(f, 645, 490, "x", 46, italic=True)
    T(f, 673, 488, "≤", 46)
    T(f, 710, 490, "5?", 46)
    T(f, 566, 450, "是", 46)
    T(f, 790, 450, "否", 46)
    f.line(583, 486, 478, 486, sw=sw)
    arr(f, 478, 486, 478, 556, sw=sw, head=26)
    f.line(782, 486, 878, 486, sw=sw)
    arr(f, 878, 486, 878, 538, sw=sw, head=26)

    # 处理框
    f.rect(82, 480, 202, 78, fill="none", sw=sw)
    T(f, 165, 520, "y=x", 46)
    T(f, 206, 506, "2", 28, italic=True)
    f.rect(377, 558, 201, 78, fill="none", sw=sw)
    T(f, 477, 598, "y=2x-3", 50)
    f.rect(795, 540, 166, 106, fill="none", sw=sw)
    T(f, 836, 594, "y=", 50)
    T(f, 905, 570, "1", 42)
    f.line(881, 592, 929, 592, sw=2.6)
    T(f, 905, 618, "x", 46, italic=True)

    # 汇合
    f.line(182, 558, 182, 670, sw=sw)
    f.line(182, 670, 878, 670, sw=sw)
    f.line(878, 646, 878, 670, sw=sw)
    arr(f, 478, 636, 478, 733, sw=sw, head=26)

    # 输出 y / 结束
    f.poly([(397, 735), (597, 735), (559, 799), (358, 799), (397, 735)], sw=sw)
    T(f, 452, 767, "输出", 56)
    T(f, 518, 769, "y", 58, italic=True)
    arr(f, 478, 799, 478, 862, sw=sw, head=26)
    f.rect(400, 864, 155, 72, fill="none", sw=sw, rx=36)
    T(f, 478, 900, "结束", 58)

    # 编号圈与引线
    marks = [("1", 715, 168, (688, 180), (600, 196)),
             ("2", 717, 255, (692, 267), (562, 306)),
             ("3", 88, 428, (100, 448), (122, 472)),
             ("4", 806, 360, (795, 378), (748, 450)),
             ("5", 120, 620, (146, 621), (374, 590)),
             ("6", 1030, 537, (1008, 545), (966, 528)),
             ("7", 690, 750, (668, 758), (600, 764))]
    for s, cx, cy, p0, p1 in marks:
        circled(f, cx, cy, 21, s, 24)
        f.line(p0[0], p0[1], p1[0], p1[1], sw=2.0)

    # 程序图
    nodes = {"1": (1328, 156), "2": (1324, 318), "3": (1224, 492),
             "4": (1424, 492), "5": (1332, 643), "6": (1516, 652),
             "7": (1224, 802)}
    for s, (cx, cy) in nodes.items():
        f.circle(cx, cy, 52, fill="#ffffff", sw=3.0)
        T(f, cx, cy, s, 44)
    edges = [((1328, 208), (1324, 264)),
             ((1290, 362), (1246, 442)),
             ((1360, 362), (1400, 442)),
             ((1224, 544), (1224, 748)),
             ((1400, 536), (1352, 596)),
             ((1452, 530), (1488, 604)),
             ((1298, 690), (1264, 760)),
             ((1478, 696), (1272, 782))]
    for p0, p1 in edges:
        arr(f, p0[0], p0[1], p1[0], p1[1], sw=3.0, head=24)
    T(f, 1305, 552, "R1", 46, "start")
    T(f, 1437, 698, "R2", 46, "start")
    T(f, 1162, 660, "R3", 46, "start")
    T(f, 1595, 910, "环路复杂度为3", 58, bold=True, color="#0000ff")
    return f


# ---------------------------------------------------------------- 6 软件测试流程图

def f_test(Fig):
    f = Fig(1941, 936)
    sw = 3.0
    size = 50
    boxes = [(84, 64, 386, 98, "用户需求"), (1470, 64, 385, 98, "验收测试"),
             (184, 257, 384, 97, "需求分析"), (1286, 257, 384, 97, "系统测试"),
             (338, 442, 385, 96, "概要设计"), (1131, 442, 384, 96, "集成测试"),
             (514, 616, 385, 96, "详细设计"), (1035, 616, 384, 96, "单元测试"),
             (787, 798, 385, 98, "编码")]
    for x, y, w, h, s in boxes:
        tbox(f, x, y, w, h, s, size=size)
    # 虚线对应关系
    for y, x0, x1 in ((114, 470, 1470), (306, 568, 1286),
                      (490, 723, 1131), (664, 899, 1035)):
        f.line(x0, y, x1, y, sw=2.4, dash="30,9,4,9")
    # 左列自上而下
    left = [((350, 162), (250, 257)), ((450, 354), (390, 442)),
            ((620, 538), (580, 616)), ((700, 712), (880, 798))]
    # 右列自下而上
    right = [((1080, 798), (1230, 712)), ((1250, 616), (1340, 538)),
             ((1400, 442), (1470, 354)), ((1560, 257), (1620, 162))]
    for p0, p1 in left + right:
        arr(f, p0[0], p0[1], p1[0], p1[1], sw=sw, head=30)
    return f


# ---------------------------------------------------------------- 7 测试层次

def f_level(Fig):
    f = Fig(1509, 1056)
    GRAYF = "#d9d9d9"
    BLU = "#2b8fb0"
    RED = "#c00000"

    # 页眉
    for dx in (0, 40):
        f.poly([(55 + dx, 32), (110 + dx, 63), (55 + dx, 94), (78 + dx, 63),
                (55 + dx, 32)], fill=BLU, sw=1)
    T(f, 215, 63, "测试的层次", 64, "start", bold=True, color="#17809b")
    f.circle(1140, 45, 34, fill=BLU, sw=1.5)
    f.circle(1140, 45, 27, fill="#ffffff", sw=1)
    T(f, 1140, 40, "B", 28, color=BLU, bold=True)
    T(f, 1140, 60, "BJUT 1960", 6, color=BLU, bold=True)
    T(f, 1200, 42, "北京工业大学", 32, "start", bold=True, color="#3aa8c8")
    T(f, 1200, 72, "BEIJINGUNIVERSITYOFTECHNOLOGY", 9, "start",
      bold=True, color="#3aa8c8")

    boxes = [(588, 152, 172, 83, "产品"), (383, 268, 173, 84, "子系统1"),
             (926, 268, 173, 84, "子系统2"),
             (157, 434, 206, 84, "软件子系统1"), (507, 434, 207, 84, "硬件子系统1"),
             (790, 434, 207, 84, "软件子系统2"), (1108, 434, 206, 84, "硬件子系统2"),
             (77, 598, 193, 87, "软件模块1"), (338, 598, 195, 87, "软件模块2"),
             (55, 740, 206, 82, "软件程序1"), (338, 740, 195, 82, "软件程序2"),
             (570, 740, 212, 82, "软件程序3"),
             (66, 899, 119, 82, "单元1"), (218, 899, 92, 82, "单元2")]
    for x, y, w, h, s in boxes:
        f.rect(x, y, w, h, fill=GRAYF, sw=0, rx=6)
        T(f, x + w / 2, y + h / 2, s, 36, bold=True)

    def tree(pcx, pbottom, kids, ktop, busy):
        f.line(pcx, pbottom, pcx, busy, sw=2.0)
        f.line(min(kids + [pcx]), busy, max(kids + [pcx]), busy, sw=2.0)
        for kx in kids:
            arr(f, kx, busy, kx, ktop, sw=2.2, head=20)

    tree(674, 235, [469, 1013], 268, 259)
    tree(469, 352, [260, 611], 434, 402)
    tree(1013, 352, [894, 1211], 434, 393)
    tree(260, 518, [181, 430], 598, 557)
    tree(181, 685, [158, 435, 676], 740, 710)
    tree(158, 822, [138, 319], 899, 861)

    # 标注：系统测试 / 验收测试
    f.poly([(882, 145), (882, 168), (762, 190)], fill="#bfbfbf", sw=1.5)
    f.rect(882, 62, 193, 103, fill="#bfbfbf", sw=1.8)
    T(f, 978, 90, "系统测试", 32, bold=True, color=RED)
    T(f, 978, 134, "验收测试", 32, bold=True, color=RED)

    # 标注：单元测试
    f.poly([(611, 958), (611, 990), (312, 950)], fill="#bfbfbf", sw=1.5)
    f.rect(611, 923, 192, 102, fill="#bfbfbf", sw=1.8)
    T(f, 706, 951, "单元测试", 36, bold=True, color=RED)

    # 集成测试 与花括号
    T(f, 859, 656, "集成测试", 36, "end", bold=True, color=RED)
    brace_v(f, 1010, 545, 800, w=52, sw=2.4, side=-1)
    T(f, 1065, 566, "模块内的集成", 36, "start", bold=True, color=RED)
    T(f, 1065, 668, "子系统内的集成测试", 36, "start", bold=True, color=RED)
    T(f, 1065, 782, "子系统间的集成测试", 36, "start", bold=True, color=RED)
    return f


# ---------------------------------------------------------------- 8 测试方法

def f_method(Fig):
    f = Fig(1714, 799)
    LB = "#a8c0e8"

    # 块箭头（先画，文字覆盖其上）
    block_arrow(f, 355, 413, 190, thick=26, head=34, fill=LB)
    block_arrow(f, 1390, 485, 1520, thick=26, head=34, fill=LB)

    vstack(f, 100, 234, "结构化测试方法", 54, 1.14, color="#1f4e79")
    vstack(f, 292, 322, "白盒方法", 55, 1.18, color="#2e5c8a")
    vstack(f, 1350, 354, "黑盒方法", 54, 1.18, color=INK)
    for i, col in enumerate(("基于需", "求的测", "试方法")):
        vstack(f, 1560 + i * 60, 387, col, 53, 1.15, color="#2e5c8a")

    # 黑底列表
    f.rect(854, 88, 376, 628, fill="#1a1a1a", sw=1.5)
    items = ["等价类划分法", "边界值分析法", "判定表方法", "因果图法",
             "Pairwise方法", "正交试验法", "功能图法"]
    for i, s in enumerate(items):
        T(f, 875, 150 + i * 85, s, 52, "start", bold=True, color="#ffffff")

    # 白盒方法列表
    white = ["语句覆盖", "判定覆盖", "条件覆盖", "判定条件覆盖",
             "条件组合覆盖", "基本路径覆盖"]
    for i, s in enumerate(white):
        T(f, 435, 188 + i * 76, s, 53, "start")

    # 花括号
    brace_v(f, 420, 143, 663, w=28, sw=2.2, side=-1, color="#f0b080")
    brace_v(f, 1240, 88, 716, w=78, sw=2.6, side=1, color="#2e5c8a")
    return f


# ---------------------------------------------------------------- 9 因果图法

def f_causal(Fig):
    f = Fig(1823, 1174)
    sw = 2.0
    cols = [43, 131, 410, 474, 537, 601, 665, 728, 792, 856, 919, 983, 1046, 1110]
    rows = [18, 123, 172, 221, 270, 319, 368, 417, 465, 514, 563, 612, 661]
    f.rect(cols[0], rows[0], cols[-1] - cols[0], rows[-1] - rows[0], sw=sw)
    for x in cols[1:-1]:
        f.line(x, rows[0], x, rows[-1], sw=sw)
    # 横线：左侧标签列按行组合并
    for y in (rows[1], rows[6], rows[8]):
        f.line(cols[0], y, cols[-1], y, sw=sw)
    for i, y in enumerate(rows[1:-1]):
        if y not in (rows[1], rows[6], rows[8]):
            f.line(cols[1], y, cols[-1], y, sw=sw)

    # 列号 1..11
    for i in range(11):
        cx = (cols[2 + i] + cols[3 + i]) / 2
        T(f, cx, 76, str(i + 1), 30, bold=True)

    # 左侧行组标签
    T(f, 87, 230, "输", 32)
    T(f, 87, 262, "入", 32)
    T(f, 87, 395, "中间", 24)
    T(f, 87, 427, "结点", 24)
    T(f, 87, 520, "输", 32)
    T(f, 87, 552, "出", 32)

    data = [
        ("投入2元5角硬币", "11110000000"),
        ("投入3元硬币", "00001111000"),
        ("按“可乐”按钮", "10001000100"),
        ("按“雪碧”按钮", "01000100010"),
        ("按“红茶”按钮", "00100010001"),
        ("已投币", "11111111000"),
        ("已按钮", "11101110111"),
        ("退还5角硬币", "00001110000"),
        ("送出“可乐”饮料", "10001000000"),
        ("送出“雪碧”饮料", "01000100000"),
        ("送出“红茶”饮料", "00100010000"),
    ]
    for i, (label, vals) in enumerate(data):
        y = (rows[i + 1] + rows[i + 2]) / 2
        T(f, 405, y, label, 33, "end")
        for j, ch in enumerate(vals):
            T(f, (cols[2 + j] + cols[3 + j]) / 2, y, ch, 28)

    # 红框
    f.rect(392, 3, 752, 129, sw=5.0, stroke="#c00000")

    T(f, 1450, 325, "生成判定表", 70, bold=True)

    # 下方测试用例表
    cols2 = [485, 718, 1149, 1772]
    rows2 = [676, 745, 823, 901, 979, 1049, 1118, 1173]
    f.rect(cols2[0], rows2[0], cols2[-1] - cols2[0], rows2[-1] - rows2[0], sw=sw)
    for x in cols2[1:-1]:
        f.line(x, rows2[0], x, rows2[-1], sw=sw)
    for y in rows2[1:-1]:
        f.line(cols2[0], y, cols2[-1], y, sw=sw)
    f.rect(cols2[0], rows2[0], cols2[1] - cols2[0], rows2[1] - rows2[0],
           fill="#ccffcc", sw=0)
    f.rect(cols2[1], rows2[0], cols2[2] - cols2[1], rows2[1] - rows2[0],
           fill="#ccffcc", sw=0)
    f.rect(cols2[2], rows2[0], cols2[3] - cols2[2], rows2[1] - rows2[0],
           fill="#ccffcc", sw=0)
    f.line(cols2[0], rows2[0], cols2[-1], rows2[0], sw=sw)
    f.line(cols2[0], rows2[1], cols2[-1], rows2[1], sw=sw)
    heads = ["用例编号", "测试用例", "预期输出"]
    for i, s in enumerate(heads):
        T(f, (cols2[i] + cols2[i + 1]) / 2, 711, s, 30, bold=True)
    body = [("1", "投入2元5角，按“可乐”", "送出“可乐”饮料"),
            ("2", "投入2元5角，按“雪碧”", "送出“雪碧”饮料"),
            ("3", "投入2元5角，按“红茶”", "送出“红茶”饮料"),
            ("4", "投入3元，按“可乐”", "找5角，送出“可乐”"),
            ("5", "投入3元，按“雪碧”", "找5角，送出“雪碧”"),
            ("6", "投入3元，按“红茶”", "找5角，送出“红茶”")]
    for i, (a, b, c) in enumerate(body):
        y = (rows2[i + 1] + rows2[i + 2]) / 2
        T(f, (cols2[0] + cols2[1]) / 2, y, a, 30)
        T(f, (cols2[1] + cols2[2]) / 2, y, b, 30)
        T(f, (cols2[2] + cols2[3]) / 2, y, c, 30)

    T(f, 285, 833, "生成测试用例", 60, bold=True)
    T(f, 285, 915, "（有效输入）", 58, bold=True)
    return f


# ---------------------------------------------------------------- 10 测试用例表

def f_case(Fig):
    f = Fig(1028, 808)
    sw = 1.6
    S = 16
    f.rect(21, 26, 969, 206, sw=sw)
    for y in (74, 177, 232):
        f.line(21, y, 990, y, sw=sw)
    f.line(156, 26, 156, 232, sw=sw)
    f.line(280, 26, 280, 74, sw=sw)
    f.line(592, 26, 592, 74, sw=sw)

    T(f, 51, 39, "用例ID", S, "start")
    T(f, 166, 39, "XXXX-", S, "start")
    T(f, 166, 61, "XX-XX", S, "start")
    T(f, 310, 38, "用例名称", S, "start")
    T(f, 622, 38, "系统登录", S, "start")
    T(f, 51, 86, "用例描述", S, "start")
    for y, s in ((86, "系统登录"),
                 (112, "用户名存在、密码正确的情况下，进入系统"),
                 (138, "页面信息包含：页面背景显示"),
                 (164, "用户名和密码录入接口，输入数据后的登入系统接口")):
        T(f, 186, y, s, S, "start")
    T(f, 51, 189, "用例入口", S, "start")
    T(f, 186, 189, "打开IE，在地址栏输入相应地址", S, "start")
    T(f, 186, 215, "进入该系统登录页面", S, "start")

    # 第二表
    c2 = [21, 156, 344, 597, 903, 990]
    r2 = [258, 283, 309, 358, 454, 503, 529, 578, 626, 675, 724, 772, 799]
    f.rect(21, 258, 969, 541, sw=sw)
    for y in r2[1:-1]:
        f.line(21, y, 990, y, sw=sw)
    for x in c2[1:-1]:
        f.line(x, 258, x, 799, sw=sw)
    heads = ["测试用例ID", "场景", "测试步骤", "预期结果", "备注"]
    for i, s in enumerate(heads):
        T(f, c2[i] + 30, 271, s, S, "start")

    def row(i, texts):
        """第 i 个数据行：texts 为 {列号: 单行或行列表}。"""
        y0 = r2[1 + i]
        for j, v in texts.items():
            s0 = 14 if j == 4 else S
            if isinstance(v, str):
                T(f, c2[j] + 30, y0 + 12.5, v, s0, "start")
            else:
                for k, s in enumerate(v):
                    T(f, c2[j] + 30, y0 + 12.5 + 19 * k, s, s0, "start")

    row(0, {0: "TC1", 1: "初始页面显示", 2: "从用例入口处进入",
            3: "页面元素完整，显示与详细设计一致"})
    row(1, {0: "TC2", 1: ["用户名录入－验", "证"],
            2: "输入已存在的用户：test", 3: "输入成功"})
    row(2, {0: "TC3", 1: ["用户名－容错性", "验证"],
            2: ["输入：", "aaaaaabbbbbbcccccddddddeeeee"],
            3: ["输入到蓝色显示的字符时，系统拒绝", "输入"],
            4: ["输入数", "据超过规", "定长度范", "围"]})
    row(3, {0: "TC4", 1: "密码－密码录入",
            2: ["输入与用户名相关联的数", "据：test"], 3: "输入成功"})
    row(4, {0: "TC5", 1: "系统登录－成功",
            2: "TC2，TC4，单击登录按钮", 3: "登录系统成功"})
    row(5, {0: "TC6", 1: ["系统登录－用户", "名、密码校验"],
            2: ["没有输入用户名、密码，单", "击登录按钮"],
            3: ["系统登录失败，并提示：请检查用户", "名和密码的输入是否正确"]})
    row(6, {0: "TC7", 1: ["系统登录－密码", "校验"],
            2: ["输入用户名，没有输入密", "码，单击登录按钮"],
            3: ["系统登录失败，并提示：需要输入密", "码"]})
    row(7, {0: "TC8", 1: ["系统登录－密码", "有效性校验"],
            2: ["输入用户名，输入密码与用", "户名不一致，单击登录按钮"],
            3: "系统登录失败，并提示：错误的密码"})
    row(8, {0: "TC9", 1: ["系统登录－输入", "有效性校验"],
            2: ["输入不存在的用户名、密", "码，单击登录按钮"],
            3: ["系统登录失败，并提示：用户名不存", "在"]})
    row(9, {0: "TC10", 1: ["系统登录－安全", "校验"],
            2: "连续3次未成功",
            3: ["系统提示：您没有使用该系统的权", "限，请与管理员联系！"]})
    for j in range(5):
        T(f, c2[j] + 30, 785, "…", S, "start")
    return f


# ---------------------------------------------------------------- 11 缺陷报告表

def f_bug(Fig):
    f = Fig(928, 950)
    sw = 1.6
    rows = [16, 66, 117, 168, 219, 269, 369, 719, 770, 820, 931]
    f.rect(26, 16, 881, 915, sw=sw)
    for y in rows[1:-1]:
        f.line(26, y, 907, y, sw=sw)
    f.line(166, 16, 166, 931, sw=sw)
    for y0, y1 in ((66, 269),):
        f.line(483, y0, 483, y1, sw=sw)
        f.line(632, y0, 632, y1, sw=sw)
    # 标签列浅灰
    for y0, y1 in zip(rows[:-1], rows[1:]):
        f.rect(26, y0, 140, y1 - y0, fill="#e8e8e8", sw=0)
    f.line(26, 16, 26, 931, sw=sw)
    f.line(166, 16, 166, 931, sw=sw)

    lab = [(16, 66, "模块名称"), (66, 117, "版本号"), (117, 168, "缺陷类型"),
           (168, 219, "可重复性"), (219, 269, "测试平台"), (269, 369, "简述"),
           (369, 719, "操作步骤"), (719, 770, "实际结果"), (770, 820, "预期结果"),
           (820, 931, "注释")]
    for y0, y1, s in lab:
        T(f, 96, (y0 + y1) / 2, s, 21, bold=True)

    T(f, 180, 41, "贴吧注册登录页面", 21, "start")
    T(f, 507, 91, "测试人", 21, bold=True)
    T(f, 656, 91, "庄睿哲", 21, "start")
    T(f, 180, 142, "功能错误", 21, "start")
    T(f, 507, 142, "严重级别", 21, bold=True)
    T(f, 656, 142, "B", 21, "start")
    T(f, 180, 193, "是", 21, "start")
    T(f, 507, 193, "缺陷状态", 21, bold=True)
    T(f, 656, 193, "New", 21, "start")
    T(f, 180, 244, "Win7", 21, "start")
    T(f, 507, 244, "浏览器", 21, bold=True)
    T(f, 656, 244, "百度浏览器", 21, "start")

    T(f, 180, 305, "系统规定注册用户名的长度为 6-20 字符。用少于 6 个字符的用户名可以成功", 21, "start")
    T(f, 180, 340, "注册", 21, "start")

    steps = ["1.  进入贴吧网站首页",
             "2.  点击注册，进入用户注册页面",
             "3.  单击“同意”按钮，进入用户注册页面",
             "4.  在用户名文本框中输入“123”",
             "5.  设置密码为“johnson”",
             "6.  注册完毕后返回登录页面",
             "7.  输入用户名“123”，密码“johnson”"]
    for i, s in enumerate(steps):
        T(f, 180, 395 + i * 50, s, 21, "start")

    T(f, 180, 744, "注册成功，登陆成功", 21, "start")
    T(f, 180, 795, "提示用户名错误，不能注册成功", 21, "start")
    T(f, 180, 848, "建议修改", 21, "start")
    return f


FIGS = [("上层模块", f_top), ("下层模块", f_lower), ("N-S图", f_ns),
        ("PAD图", f_pad), ("环路复杂度", f_cyc), ("软件测试流程图", f_test),
        ("测试层次", f_level), ("测试方法", f_method), ("因果图法", f_causal),
        ("测试用例表", f_case), ("缺陷报告表", f_bug)]
