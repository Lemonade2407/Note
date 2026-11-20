# -*- coding: utf-8 -*-
"""软件工程导论插图 SVG 重绘 —— 第 1 批（11 张）。

图名与 图片/图名.png 逐字一致。
"""
import math

import se_kit as K
from se_kit import Fig, INK, BOXF, BOXW, BLUE, GREEN, YELLOW, RED, GRAY

TEAL = "#18A3C6"      # 幻灯片标题与校徽色
ORANGE = "#C55A11"    # 表格橙色标题字
LGREEN = "#DDE6D3"    # 范式表浅绿
PANEL = "#CEDEC3"     # 瀑布模型浅绿底板
TBLUE = "#0364BF"     # 过程模型表表头蓝
LAV = "#CAD3E8"       # 过程模型表浅蓝紫
GRAYBG = "#E7E7E7"    # 设计模式表底色
DASH = "5,4"


# ---------------------------------------------------------------- 通用图元

def slide(f, title, tw=42):
    """幻灯片页眉：双箭头 + 标题 + 校徽。"""
    for dx in (0, 40):
        f.poly([(42 + dx, 26), (60 + dx, 26), (84 + dx, 52), (60 + dx, 78),
                (42 + dx, 78), (66 + dx, 52)], sw=1.0, fill=TEAL)
    f.text(158, 55, title, size=tw, bold=True, color=TEAL, anchor="start")
    # 校徽
    f.circle(790, 46, 26, sw=2.6, fill="#FFFFFF")
    f.circle(790, 46, 20, sw=1.0, fill="#FFFFFF")
    f.text(790, 42, "BJUT", size=11, bold=True, color=TEAL)
    f.text(790, 58, "1960", size=7, color=TEAL)
    f.text(826, 38, "北京工业大学", size=27, bold=True, color=TEAL, anchor="start")
    f.text(828, 65, "BEIJING UNIVERSITY OF TECHNOLOGY", size=8,
           color="#1F5FA8", anchor="start")


def vt(f, cx, yc, s, size=16, bold=False, color=INK, gap=None):
    """竖排文字：一字一行，整体以 yc 为中心。"""
    gap = gap or size * 1.12
    n = len(s)
    y0 = yc - gap * (n - 1) / 2
    for i, ch in enumerate(s):
        f.text(cx, y0 + i * gap, ch, size=size, bold=bold, color=color)


def vt2(f, cx, yc, s, size=16, bold=False, color=INK, gap=None):
    """竖排文字：两字一行。"""
    gap = gap or size * 1.5
    lines = [s[i:i + 2] for i in range(0, len(s), 2)]
    y0 = yc - gap * (len(lines) - 1) / 2
    for i, ln in enumerate(lines):
        f.text(cx, y0 + i * gap, ln, size=size, bold=bold, color=color)


def curve(f, x1, y1, x2, y2, sw=1.3, head=8, dash=None, n=16):
    """象限弧：起点切向水平，终点切向竖直。"""
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * x2 + t * t * x2
        y = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * y1 + t * t * y2
        pts.append((x, y))
    f.poly(pts, sw=sw, dash=dash)
    if head:
        f.arrow(pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1], sw=sw, head=head)


def star(f, cx, cy, r, color="#E00000"):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    f.poly(pts, sw=1.0, fill=color)


def para(f, x, y, w, h, off=14, lines=None, size=16, lh=1.35):
    """平行四边形（流程图输入/输出）。"""
    f.poly([(x + off, y), (x + w, y), (x + w - off, y + h), (x, y + h)], sw=1.5)
    if lines:
        if isinstance(lines, str):
            lines = [lines]
        step = size * lh
        y0 = y + h / 2 - step * (len(lines) - 1) / 2
        for i, s in enumerate(lines):
            f.text(x + w / 2, y0 + i * step, s, size=size, bold=True)


def mc(f, x, y, w, h, lines, size=16, bold=False, color=INK, lh=1.35, pad=None):
    """单元格内多行文字（默认居中，给 pad 则左对齐）。"""
    if isinstance(lines, str):
        lines = [lines]
    step = size * lh
    y0 = y + h / 2 - step * (len(lines) - 1) / 2
    for i, s in enumerate(lines):
        if pad is None:
            f.text(x + w / 2, y0 + i * step, s, size=size, bold=bold, color=color)
        else:
            f.text(x + pad, y0 + i * step, s, size=size, bold=bold, color=color,
                   anchor="start")


# ---------------------------------------------------------------- 1 产品质量

def f_chanpin(Fig):
    f = Fig(1378, 694)
    S = 17
    # 根
    K.plain(f, 562, 41, 324, 113, "系统/软件产品质量", size=20)
    f.line(724, 154, 724, 161, sw=1.4)
    f.line(173, 161, 1300, 161, sw=1.4)
    cols = [(98, 248), (259, 409), (419, 569), (580, 730),
            (744, 894), (901, 1052), (1063, 1213), (1224, 1375)]
    names = ["功能性", "性能效率", "兼容性", "易用性", "可靠性", "信息安全性",
             "维护性", "可移植性"]
    subs = [
        ["功能完备性", "功能正确性", "功能适合性", "功能性的\n依从性"],
        ["时间特性", "资源利用性", "容量", "性能效率的\n依从性"],
        ["共存性", "互操作性", "兼容性的\n依从性"],
        ["可辨识性", "易学性", "易操作性", "用户差错防御性", "用户界面舒适性",
         "易访问性", "易用性的\n依从性"],
        ["成熟性", "可用性", "容错性", "易恢复性", "可靠性的\n依从性"],
        ["保密性", "完整性", "抗抵赖性", "可核查性", "真实性", "信息安全的\n依从性"],
        ["模块化", "可重用性", "易分析性", "易修改性", "易测试性", "维护性的\n依从性"],
        ["适应性", "易安装性", "易替换性", "可移植性的\n依从性"],
    ]
    steps = [47, 47, 50, 34, 39, 36, 36, 47]
    for i, (x, x2) in enumerate(cols):
        cx = (x + x2) / 2
        f.line(cx, 161, cx, 203, sw=1.4)
        K.plain(f, x, 203, x2 - x, 95, names[i], size=19)
        K.shell(f, x, 305, x2 - x, 375)
        y = 340
        for it in subs[i]:
            for j, ln in enumerate(it.split("\n")):
                f.text(cx, y + j * 26, ln, size=S)
            y += steps[i]
    return f


# ---------------------------------------------------------------- 2 软件工程范式对比表

def f_fanshi(Fig):
    f = Fig(1125, 596)
    X = [10, 72, 184, 490, 780, 1118]
    Y = [6, 51, 101, 219, 280, 374, 472, 520, 588]
    # 底色
    for r in range(8):
        for c in range(5):
            if r == 0:
                fill = LGREEN if c >= 2 else BOXW
            elif r == 1:
                fill = LGREEN if c >= 2 else BOXW
            elif r == 2 or r == 4 or r == 6:
                fill = LGREEN
            else:
                fill = LGREEN if c == 0 else BOXW
            f.rect(X[c], Y[r], X[c + 1] - X[c], Y[r + 1] - Y[r], fill=fill, sw=0)
    # 网格
    for r in range(9):
        f.line(X[0], Y[r], X[-1], Y[r], sw=1.2)
    f.line(X[0], Y[0], X[0], Y[-1], sw=1.2)
    f.line(X[-1], Y[0], X[-1], Y[-1], sw=1.2)
    f.line(X[2], Y[0], X[2], Y[-1], sw=1.2)
    for x in (X[3], X[4]):
        f.line(x, Y[0], x, Y[-1], sw=1.2)
    f.line(X[1], Y[2], X[1], Y[-1], sw=1.2)
    for r in (2, 3, 4, 5, 6, 7):
        f.line(X[1], Y[r], X[-1], Y[r], sw=1.2)
    # 表头
    f.text((X[0] + X[2]) / 2, (Y[0] + Y[1]) / 2 + 24, "元素", size=21, bold=True)
    hdr = ["工程范式", "开源范式", "群智范式"]
    for i, s in enumerate(hdr):
        f.text((X[i + 2] + X[i + 3]) / 2, (Y[0] + Y[1]) / 2, s, size=22,
               bold=True, color=ORANGE)
    sub = ["自上而下，逐步求精", "自下而上，关联演化", "宏观演化，局部求精"]
    for i, s in enumerate(sub):
        f.text((X[i + 2] + X[i + 3]) / 2, (Y[1] + Y[2]) / 2, s, size=20, bold=True)
    # 行首列
    rows = [("需求", 2), ("质量", 3), ("效率", 4), ("过程模型", 5), ("支持工具", 6),
            ("计算环境", 7)]
    for s, r in rows:
        f.text((X[1] + X[2]) / 2, (Y[r] + Y[r + 1]) / 2, s, size=18, bold=True)
    vt(f, (X[0] + X[1]) / 2, (Y[2] + Y[5]) / 2, "理念", size=21, bold=True, gap=26)
    vt(f, (X[0] + X[1]) / 2, (Y[5] + Y[8]) / 2, "方法", size=21, bold=True, gap=26)
    # 正文
    body = [
        (2, [["有明确用户和明确一致的用户需", "求描述，这是软件开发的前提"],
             ["没有明确的用户，开发者基于", "自己的构思创作软件源代码"],
             ["有潜在用户群体，基于原型", "体验发现用户，引导用户", "体验，并不断产生需求"]]),
        (3, [["源代码满足需求规格的程度"],
             ["开发社区的规模和口碑"],
             ["软件社区关注度和口碑"]]),
        (4, [["开发满足需求软件的时间和成本"],
             ["响应开发社区问题的时间"],
             ["“激发更多参与者作出贡献，以", "及汇聚广大贡献者才智” 的效率"]]),
        (5, [["瀑布模型、敏捷模型、", "能力成熟度模型"],
             ["开发者社区的自组织模式"],
             ["激发与汇聚模型"]]),
        (6, [["软件产品线工具集"],
             ["版本控制工具、缺陷追踪工具"],
             ["激发与汇聚工具集"]]),
        (7, [["面向计算机环境"],
             ["面向互联网环境"],
             ["面向人机物融合环境"]]),
    ]
    for r, cells in body:
        for i, lines in enumerate(cells):
            mc(f, X[i + 2], Y[r], X[i + 3] - X[i + 2], Y[r + 1] - Y[r], lines,
               size=18, pad=12)
    return f


# ---------------------------------------------------------------- 3 过程模型对比

def f_guocheng(Fig):
    f = Fig(1024, 724)
    slide(f, "过程模型")
    X = [65, 250, 490, 625, 775, 980]
    Y = [118, 247, 355, 462, 575, 690]
    head = ["模型", "需求分析的方式", ["迭代", "层级"], ["软件版本", "提交方式"],
            "降低风险的方式"]
    for c in range(5):
        f.rect(X[c], Y[0], X[c + 1] - X[c], Y[1] - Y[0], fill=TBLUE, sw=1.4)
        mc(f, X[c], Y[0], X[c + 1] - X[c], Y[1] - Y[0], head[c], size=22,
           bold=True, color="#ffffff")
    body = [
        (["瀑布模型", "一次性明确", "无", "完整版本", "准确地需求分析"], True),
        (["快速原型模型", ["迭代明确+瀑布开发"], ["需求分析活", "动"], "完整版本",
          "迭代地需求分析"], True),
        (["增量开发模型", ["局部明确+增量开发", "+需求变更"], ["开发活动+需", "求更新"],
          "增量部分", ["及时地用户反馈"]], True),
        (["螺旋模型", ["快速原型+瀑布+增", "量"], "整个过程", ["更新的完", "整版本"],
          ["完整的", "风险分析机制"]], True),
    ]
    for i, (cells, _) in enumerate(body):
        y, h = Y[i + 1], Y[i + 2] - Y[i + 1]
        for c in range(5):
            f.rect(X[c], y, X[c + 1] - X[c], h, fill=LAV, sw=1.4)
            mc(f, X[c], y, X[c + 1] - X[c], h, cells[c], size=21, bold=True)
    return f


# ---------------------------------------------------------------- 4 瀑布模型

def f_pubu(Fig):
    f = Fig(1024, 724)
    slide(f, "瀑布模型")
    f.rect(30, 100, 965, 500, fill=PANEL, sw=0)
    stages = ["可行性研究", "项目实施计划", "需求分析", "概要设计", "详细设计",
              "编码", "测试", "维护"]
    docs = ["可行性研究报告", "软件项目计划", "需求规格说明", "概要设计说明",
            "程序规格说明", "原程序代码", "测试报告", "维护报告"]
    ys = [137, 194, 251, 308, 365, 422, 479, 536]
    xs, w = [], 172
    for i in range(8):
        xs.append(258 + 22 * i)
    # 时间括号
    def brace_v(x, y1, y2):
        f.line(x - 31, y1, x + 31, y1, sw=1.6)
        f.line(x - 31, y2, x + 31, y2, sw=1.6)
        f.arrow(x - 5, y1 + 2, x - 5, y2 - 2, head=7)
        f.arrow(x - 5, y2 - 2, x - 5, y1 + 2, head=7)

    brace_v(180, 112, 207)
    brace_v(180, 207, 489)
    brace_v(180, 489, 558)
    vt(f, 232, 160, "计划时期", size=17, gap=19)
    vt(f, 232, 348, "开发时期", size=17, gap=19)
    vt(f, 240, 521, "运行时期", size=15, gap=17)

    for i in range(8):
        y = ys[i]
        K.box(f, xs[i], y - 20, w, 40, stages[i], size=17, fill=PANEL, sw=1.2, rx=0)
        # 文档虚线框
        f.rect(709, y - 22, 182, 44, fill=PANEL, sw=1.2, dash="4,3", rx=9)
        f.text(800, y, docs[i], size=17)
        # 虚线箭头
        f.arrow(xs[i] + w, y, 709, y, sw=1.2, dash=DASH, head=8)
        if i < 7:
            curve(f, xs[i] + w, y, xs[i + 1] + w, ys[i + 1] - 20, sw=1.2, head=8)
    f.text(200, 580, "（时期）", size=16)
    f.text(420, 580, "（阶段）", size=16)
    f.text(800, 580, "（文档）", size=16)
    # 下方条目
    for i, s in enumerate(["GB/T 8567-2006  《计算机软件文档编制规范》",
                           "GJB 438B-2009 《军用软件开发文档通用要求》"]):
        f.circle(178, 620 + i * 43, 4.5, fill=INK, sw=0)
        f.text(200, 620 + i * 43, s, size=25, anchor="start")
    return f


# ---------------------------------------------------------------- 5 双V模型

def f_shuangV(Fig):
    f = Fig(1294, 777)
    # 中轴
    f.line(515, 26, 515, 735, sw=1.2, dash="2,4")
    # 左 V
    L = [(50, 120, 240, 77), (102, 275, 230, 70), (172, 438, 231, 70),
         (228, 585, 227, 70)]
    lab = ["需求分析", "概要设计", "详细设计", "编码"]
    for (x, y, w, h), s in zip(L, lab):
        K.plain(f, x, y, w, h, s, size=38, sw=1.6)
    for i in range(3):
        x1, y1 = L[i][0] + 100, L[i][1] + L[i][3]
        x2, y2 = L[i + 1][0] + 100, L[i + 1][1]
        f.arrow(x1, y1, x2, y2, sw=2.6, head=14)
    f.arrow(57, 30, 120, 118, sw=2.6, head=14)
    # 左 V 底部回折
    f.poly([(310, 655), (310, 700), (596, 700)], sw=2.2)
    f.arrow(596, 700, 596, 662, sw=2.2, head=12)
    # 右侧回折线（编码 -> 代码审查）
    f.line(455, 620, 507, 620, sw=2.2, dash=None)
    f.arrow(507, 620, 563, 620, sw=2.2, head=12)

    # 右 V 三个包围框 + 内部两框
    boxes = [
        ((720, 105, 535, 113), ["系统测试计划、", "设计、实现"], (730, 118, 250, 82),
         "执行系统测试", (1000, 118, 250, 82)),
        ((668, 262, 537, 116), ["集成测试计划、", "设计、实现"], (678, 275, 250, 80),
         "执行集成测试", (950, 275, 250, 80)),
        ((620, 428, 545, 107), ["单元测试计划、", "设计、实现"], (630, 438, 248, 80),
         "执行单元测试", (902, 438, 248, 80)),
    ]
    for (ox, oy, ow, oh), txt, (ix, iy, iw, ih), txt2, (jx, jy, jw, jh) in boxes:
        f.rect(ox, oy, ow, oh, fill=BOXW, sw=1.8)
        f.rect(ox + 7, oy + 7, ow - 14, oh - 14, fill=BOXW, sw=1.8)
        K.plain(f, ix, iy, iw, ih, txt, size=29, sw=1.6)
        K.plain(f, jx, jy, jw, jh, txt2, size=29, sw=1.6)
    K.plain(f, 565, 588, 260, 72, "代码审查", size=38, sw=1.6)

    # 水平 V&V 双箭头
    vv = [(290, 160, 730, 160, 150), (332, 310, 678, 310, 300),
          (403, 472, 630, 472, 462), (455, 620, 565, 620, 600)]
    for x1, y1, x2, y2, ty in vv:
        f.arrow(x1, y1, x2, y2, sw=1.6, head=10)
        f.arrow(x2, y2, x1, y1, sw=1.6, head=10)
        f.text((x1 + x2) / 2, ty, "V&V", size=36, bold=True)

    # 右侧斜向箭头（V 形右臂逐级上升）
    f.arrow(925, 40, 878, 112, sw=3.0, head=15)
    f.arrow(860, 212, 1098, 104, sw=3.0, head=15)
    f.arrow(1120, 96, 1180, 26, sw=3.0, head=15)
    f.arrow(770, 372, 1068, 244, sw=3.0, head=15)
    f.arrow(706, 540, 1038, 396, sw=3.0, head=15)
    f.poly([(825, 620), (940, 620), (1032, 532)], sw=2.6)
    f.arrow(1032, 532, 1037, 523, sw=2.6, head=13)
    return f


# ---------------------------------------------------------------- 6 快速原型模型

def f_yuanxing(Fig):
    f = Fig(1024, 724)
    slide(f, "快速原型模型")
    f.rect(170, 96, 720, 604, fill="#F5F5F5", sw=0)
    # 左侧外框
    f.rect(197, 108, 370, 582, fill=BOXW, sw=1.5)
    cx = 355
    K.plain(f, 283, 190, 144, 26, "快速分析", size=18, sw=1.4)
    para(f, 275, 243, 162, 30, off=18, lines="需求说明", size=18)
    K.plain(f, 283, 297, 144, 26, "构造原型", size=18, sw=1.4)
    para(f, 268, 350, 175, 32, off=20, lines="原  型", size=18)
    K.plain(f, 283, 405, 144, 26, "运行原型", size=18, sw=1.4)
    K.plain(f, 283, 460, 144, 26, "评价原型", size=18, sw=1.4)
    para(f, 275, 515, 162, 30, off=18, lines="修改意见", size=18)
    K.dia(f, cx, 582, 110, 52, "修改类型", size=17, sw=1.4)
    f.text(cx, 655, "停止修改", size=18, bold=True)
    # 竖框
    f.rect(210, 405, 32, 112, fill=BOXW, sw=1.4)
    vt(f, 226, 461, "修改原型", size=16, gap=19)
    f.rect(489, 405, 32, 112, fill=BOXW, sw=1.4)
    vt(f, 505, 461, "修改说明", size=16, gap=19)
    # 竖向箭头
    for y1, y2 in ((108, 190), (216, 243), (273, 297), (323, 350), (382, 405),
                   (431, 460), (486, 515), (545, 556), (608, 640)):
        f.arrow(cx, y1, cx, y2, sw=1.4, head=8)
    # 左右回路
    f.poly([(300, 582), (226, 582), (226, 517)], sw=1.4)
    f.arrow(226, 517, 226, 513, sw=1.4, head=8)
    f.poly([(226, 405), (226, 366), (268, 366)], sw=1.4)
    f.arrow(253, 366, 268, 366, sw=1.4, head=8)
    f.poly([(410, 582), (505, 582), (505, 517)], sw=1.4)
    f.arrow(505, 517, 505, 513, sw=1.4, head=8)
    f.poly([(505, 405), (505, 258), (437, 258)], sw=1.4)
    f.arrow(455, 258, 437, 258, sw=1.4, head=8)

    # 右侧瀑布
    rx = 790
    items = [(197, "rect", "需求分析"), (250, "para", "需求说明"),
             (302, "rect", "设计"), (355, "para", "设计说明"),
             (408, "rect", "编码"), (462, "para", "源程序清单"),
             (512, "rect", "测  试"), (565, "para", "软件产品"),
             (615, "rect", "维护")]
    yy = []
    for y, kind, s in items:
        yy.append(y)
        if kind == "rect":
            K.plain(f, 725, y, 135, 30, s, size=18, sw=1.4)
        else:
            para(f, 715, y, 153, 30, off=18, lines=s, size=18)
    for i in range(8):
        y1 = yy[i] + 30
        f.arrow(rx, y1, rx, yy[i + 1], sw=1.4, head=8)
    # 右侧交互箭头
    f.arrow(716, 207, 574, 207, sw=1.5, head=10, dash=DASH)
    f.arrow(567, 258, 715, 258, sw=1.5, head=9)
    f.poly([(706, 311), (642, 311), (642, 302), (568, 320), (642, 338),
            (642, 329), (706, 329)], sw=1.4, fill=BOXW)
    f.poly([(568, 355), (632, 355), (632, 346), (706, 364), (632, 382),
            (632, 373), (568, 373)], sw=1.4, fill=BOXW)
    f.arrow(567, 577, 712, 577, sw=1.5, head=9, dash=DASH)
    f.text(800, 682, "（2）改进过程", size=13)
    return f


# ---------------------------------------------------------------- 7 增量开发模型

def f_zengliang(Fig):
    f = Fig(1024, 724)
    slide(f, "增量开发模型")
    # 左侧三框 + 右侧两框
    left = [(33, 67, "定义需求框架"), (87, 147, "确定增量内容及其优先级"),
            (178, 237, "设计系统体系结构")]
    for x, x2, s in left:
        K.plain(f, x, 210, x2 - x, 230, "", size=17, sw=1.4)
        vt2(f, (x + x2) / 2, 325, s, size=17, gap=26)
    right = [(870, 928, "系统确认测试和用户验收测试"), (950, 1008, "软件移交")]
    for x, x2, s in right:
        K.plain(f, x, 210, x2 - x, 230, "", size=17, sw=1.4)
        vt2(f, (x + x2) / 2, 325, s, size=17, gap=26)
    for x, y in ((67, 325), (147, 325), (237, 325), (928, 325)):
        f.arrow(x, y, x + 20, y, sw=1.4, head=9)
    f.arrow(825, 325, 868, 325, sw=1.4, head=9)

    # 增量开发分组
    f.rect(275, 208, 265, 244, fill="#F5F5F5", sw=1.3, dash="6,4")
    f.text(400, 233, "增量开发", size=19, bold=True)
    inc = [(292, 277, 120, "增量分析"), (310, 312, 120, "增量设计"),
           (348, 347, 120, "增量实现"), (380, 382, 110, "测试"),
           (405, 417, 115, "增量集成")]
    for x, y, w, s in inc:
        K.plain(f, x, y, w, 28, s, size=17, sw=1.2)
    # 下一增量内容的确定
    f.rect(560, 208, 270, 244, fill="#F5F5F5", sw=1.3, dash="6,4")
    f.text(695, 233, "下一增量内容的确定", size=19, bold=True)
    f.rect(610, 258, 173, 182, fill=BOXW, sw=1.3)
    f.line(610, 385, 783, 385, sw=1.3)
    mc(f, 610, 258, 173, 127, ["用户使用增量产品", "提出反馈意见：修",
                               "改、补充需求"], size=17, lh=1.35)
    mc(f, 610, 385, 173, 55, ["和用户沟通探索下", "一增量内容的初步", "需求"],
       size=17, lh=1.35)

    # 连接线
    f.poly([(237, 325), (258, 325), (258, 291), (292, 291)], sw=1.4)
    f.arrow(258, 291, 292, 291, sw=1.4, head=8)
    f.poly([(520, 431), (552, 431), (552, 300), (610, 300)], sw=1.4)
    f.arrow(552, 300, 610, 300, sw=1.4, head=8)

    # 循环弧箭头
    def qarc(x1, y1, qx, qy, x2, y2):
        pts = []
        for i in range(21):
            t = i / 20.0
            pts.append(((1 - t) ** 2 * x1 + 2 * (1 - t) * t * qx + t * t * x2,
                        (1 - t) ** 2 * y1 + 2 * (1 - t) * t * qy + t * t * y2))
        f.poly(pts, sw=1.8)
        f.arrow(pts[-3][0], pts[-3][1], pts[-1][0], pts[-1][1], sw=1.8, head=10)

    qarc(492, 170, 462, 182, 424, 208)
    qarc(652, 170, 676, 186, 700, 208)
    f.rect(487, 152, 168, 24, fill="#D9D9D9", sw=0)
    f.text(571, 164, "下一增量开发", size=17)

    # 虚线反馈
    f.poly([(207, 440), (207, 475), (470, 475)], sw=1.3, dash="6,4")
    f.arrow(470, 475, 470, 447, sw=1.3, dash="6,4", head=8)
    f.rect(262, 462, 196, 26, fill="#D9D9D9", sw=0)
    f.text(360, 475, "指导和控制增量集成", size=16)
    f.poly([(50, 440), (50, 525), (730, 525)], sw=1.3, dash="6,4")
    f.arrow(730, 525, 730, 452, sw=1.3, dash="6,4", head=8)
    f.rect(315, 512, 198, 26, fill="#D9D9D9", sw=0)
    f.text(414, 525, "指导下一个增量的选择", size=16)
    return f


# ---------------------------------------------------------------- 8 螺旋模型

def f_luoxuan(Fig):
    f = Fig(1024, 724)
    slide(f, "螺旋模型")
    cx, cy = 440, 382
    # 坐标轴
    f.line(210, cy, 880, cy, sw=1.2)
    f.line(cx, 150, cx, 724, sw=1.2, dash="3,5")
    # 螺旋线（3.75 圈，椭圆螺线；半径按原图实测轴交点拟合）
    pts = []
    N = 900
    for i in range(N + 1):
        th = 7.5 * math.pi * i / N
        rx = 40 + 9.2 * th
        pts.append((cx + rx * math.cos(th), cy + 0.66 * rx * math.sin(th)))
    f.poly(pts, sw=1.3)
    # 斜虚线
    f.line(446, 372, 778, 256, sw=1.1, dash="5,4")
    f.line(446, 392, 764, 412, sw=1.1, dash="5,4")
    # 轴
    f.arrow(cx, 175, cx, 92, sw=1.6, head=9)
    f.text(400, 105, "累计费用", size=16)
    f.poly([(392, 165), (420, 150), (450, 143), (478, 142)], sw=1.2)
    f.arrow(470, 142, 482, 142, sw=1.2, head=8)
    f.text(520, 143, "各步骤的进度", size=16)

    T = 15
    # 上方：风险分析 ×4
    for x, y in ((550, 247), (505, 285), (462, 318)):
        f.text(x, y, "风险分析", size=T)
    f.text(400, 336, "风险", size=T)
    f.text(400, 352, "分析", size=T)
    # 左侧计划
    f.text(378, 392, "需求计划", size=T)
    f.text(378, 408, "与生命", size=T)
    f.text(378, 424, "周期计划", size=T)
    f.text(375, 455, "开发计划", size=T)
    f.text(390, 490, "集成与", size=T)
    f.text(390, 506, "测试计划", size=T)
    f.text(250, 505, "计划下一阶段", size=T)
    f.text(240, 205, "确定目标，", size=T)
    f.text(240, 221, "选择方案，", size=T)
    f.text(240, 237, "设定约束条件", size=T)
    # 中间
    f.text(447, 405, "操作概念", size=T)
    f.text(500, 400, "软件", size=T)
    f.text(500, 416, "需求", size=T)
    f.text(558, 398, "软件", size=T)
    f.text(558, 414, "产品", size=T)
    f.text(558, 430, "设计", size=T)
    f.text(628, 420, "详细", size=T)
    f.text(628, 436, "设计", size=T)
    f.text(505, 371, "原型 1", size=14)
    f.text(551, 371, "原型 2", size=14)
    f.text(594, 371, "原型 3", size=14)
    f.text(762, 348, "可运行", size=T)
    f.text(762, 364, "的原型", size=T)
    f.text(810, 400, "模拟、", size=T)
    f.text(810, 416, "模型、", size=T)
    f.text(810, 432, "基准", size=T)
    f.text(810, 265, "评估方案，", size=T)
    f.text(810, 281, "识别并排除", size=T)
    f.text(810, 297, "风险", size=T)
    f.text(800, 528, "开发、验证", size=T)
    f.text(800, 544, "下一级产品", size=T)
    # 下方
    f.text(450, 455, "需求", size=T)
    f.text(450, 471, "确认", size=T)
    f.text(480, 490, "设计验证", size=T)
    f.text(480, 506, "与确认", size=T)
    f.text(455, 560, "实现", size=T)
    f.text(555, 525, "集成", size=T)
    f.text(555, 541, "测试", size=T)
    vt(f, 528, 555, "验收测试", size=T, gap=17)
    vt(f, 612, 490, "单元测试", size=T, gap=17)
    vt(f, 664, 490, "编码", size=T, gap=17)

    # 红色说明文字
    red = [
        (30, 100, ["为项目的这个阶段定义专门目", "标。制定对过程和产品的约束，", "而且制定详细的管理计划。"]),
        (605, 100, ["分析项目风险，根据这些风险规", "避的策略方案。每一个项目风险",
                    "确定以后要进行详细的分析，并", "采取措施规避这些风险。"]),
        (55, 578, ["对项目进行评审以确定是否需要", "进入螺旋线的下一个回路。如果",
                   "决定继续，就要做出项目的下个", "阶段计划。"]),
        (555, 592, ["在风险预估以后，为系统选择开", "发模型进行开发，并进行各个阶",
                    "段的验证。"]),
    ]
    for x, y, lines in red:
        for i, s in enumerate(lines):
            f.text(x, y + i * 27, s, size=21, bold=True, color=RED, anchor="start")
    return f


# ---------------------------------------------------------------- 9 CMMI

def f_cmmi(Fig):
    f = Fig(1180, 727)
    bars = [
        (45, 145, 95, "#00A3AE", "优化级 Optimizing", 500, TEAL),
        (175, 285, 230, "#A8CDE9", "定量管理级 Quantitatively Managed", 600, "#A8CDE9"),
        (305, 410, 358, "#EA7459", "定义级 Defined", 480, "#EA7459"),
        (420, 540, 480, "#FCCF00", "管理级 Managed", 570, "#FCCF00"),
        (555, 665, 610, "#A4CB4A", "初始级 Performed", 620, "#A4CB4A"),
    ]
    nums = ["5 -", "4 -", "3 -", "2 -", "1 -"]
    for i, (y1, y2, tip, col, txt, tx, ncol) in enumerate(bars):
        f.rect(148, y1, 1032 - 148, y2 - y1, fill=col, sw=0)
        f.poly([(85, tip), (148, y1), (148, y2)], sw=0, fill=col)
        f.text(tx, (y1 + y2) / 2, txt, size=40, color="#ffffff")
        f.text(52 if i < 2 else 60, tip, nums[i], size=58, color=ncol)
    vt(f, 1095, 130, "CMMI", size=34, gap=40, color="#00A3AE")
    vt(f, 1095, 480, "成熟度等级", size=32, gap=44, color="#00A3AE")
    return f


# ---------------------------------------------------------------- 10 敏捷开发

def f_minjie(Fig):
    f = Fig(1024, 724)
    slide(f, "过程改进")
    f.rect(103, 150, 9, 40, fill="#1F5FA8", sw=0)
    f.text(125, 170, "敏捷开发", size=31, bold=True, anchor="start")
    left = ["开发周期末尾集中交付", "坚持最初的计划和需求", "开发团队与业务团队各自工作",
            "团队成员自主决定工作方式", "依赖邮件、文档、通讯工具",
            "通过文档、报告等衡量进度", "定期代码审查和代码重构"]
    right = ["定期交付可用产品增量", "定期回顾需求变化的响应策略", "跨职能团队合作",
             "严苛的监督和管理措施", "强调直接沟通", "以可工作的软件衡量进度",
             "追求绝对进度"]
    ys = [265, 313, 361, 409, 457, 505, 553]
    for i, s in enumerate(left):
        f.text(120, ys[i], s, size=26, anchor="start")
    for i, s in enumerate(right):
        f.text(550, ys[i], s, size=26, anchor="start")
    for x, y, r in ((443, 400, 23), (420, 565, 22), (820, 245, 24), (900, 305, 24),
                    (755, 360, 22), (740, 490, 22), (855, 540, 22)):
        star(f, x, y, r)
    return f


# ---------------------------------------------------------------- 11 软件设计模式分类

def f_moshi(Fig):
    f = Fig(1383, 706)
    X = [47, 139, 484, 803, 1266]
    Y = [20, 92, 209, 688]
    for r in range(3):
        for c in range(4):
            f.rect(X[c], Y[r], X[c + 1] - X[c], Y[r + 1] - Y[r], fill=GRAYBG, sw=0)
    for x in X:
        f.line(x, Y[0], x, Y[-1], sw=2)
    for y in Y:
        f.line(X[0], y, X[-1], y, sw=2)
    heads = ["创建型", "结构型", "行为型"]
    for i, s in enumerate(heads):
        f.text((X[i + 1] + X[i + 2]) / 2, (Y[0] + Y[1]) / 2, s, size=37, color=ORANGE)
    vt(f, (X[0] + X[1]) / 2, (Y[1] + Y[2]) / 2, "类", size=36, color=ORANGE, gap=50)
    vt(f, (X[0] + X[1]) / 2, (Y[2] + Y[3]) / 2, "对象", size=36, color=ORANGE, gap=50)
    S = 31
    f.text(179, (Y[1] + Y[2]) / 2, "Factory Method", size=S, color=ORANGE, anchor="start")
    f.text(524, (Y[1] + Y[2]) / 2, "Adapter (类)", size=S, color=ORANGE, anchor="start")
    f.text(843, 132, "Interpreter", size=S, color=ORANGE, anchor="start")
    f.text(843, 176, "Template Method", size=S, color=ORANGE, anchor="start")
    cols = [
        (179, ["Abstract Factory", "Builder", "Prototype", "Singleton"],
         [360, 417, 473, 530]),
        (524, ["Adapter (对象)", "Bridge", "Composite", "Decorator", "Facade",
               "Flyweight", "Proxy"], [307, 364, 417, 471, 528, 582, 640]),
        (843, ["Chain of Responsibility", "Command", "Iterator", "Mediator", "Memento",
               "Observer", "State", "Strategy", "Visitor"],
         [245, 291, 335, 381, 427, 473, 519, 565, 612]),
    ]
    for x, names, ys in cols:
        for s, y in zip(names, ys):
            f.text(x, y, s, size=S, color=ORANGE, anchor="start")
    return f


FIGS = [
    ("产品质量", f_chanpin),
    ("软件工程范式对比表", f_fanshi),
    ("过程模型对比", f_guocheng),
    ("瀑布模型", f_pubu),
    ("双V模型", f_shuangV),
    ("快速原型模型", f_yuanxing),
    ("增量开发模型", f_zengliang),
    ("螺旋模型", f_luoxuan),
    ("CMMI", f_cmmi),
    ("敏捷开发", f_minjie),
    ("软件设计模式分类", f_moshi),
]
