# -*- coding: utf-8 -*-
"""操作系统笔记的 8 张插图：用 svgkit 生成与原始截图一致的 SVG。

画布尺寸沿用原截图（坐标即原图像素），字号按原图文字包围盒标定。
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import svgkit  # noqa: E402
from svgkit import Fig  # noqa: E402

svgkit.FONT_SVG = "'Microsoft YaHei', 'SimHei', sans-serif"

INK = svgkit.INK
BOXF = "#ededed"
PINK = "#f2d7d3"
BLUE = "#dce6f3"
GREEN = "#d9e3cc"
RED = "#c00000"
GREY = "#cccccc"


# ---------------------------------------------------------------- 基础图元
def ell(f, cx, cy, rx, ry, label=None, size=21, fill="none", sw=2.1):
    f.ellipse(cx, cy, rx, ry, fill=fill, sw=sw)
    if label:
        f.text(cx, cy, label, size=size, bold=True)


def block_arrow(f, x, y1, y2, shaft=20, head=52, hl=30, fill="#f0f0f0", sw=1.5):
    """竖直向下的空心块箭头（浅灰填充）。"""
    pts = [
        (x - shaft / 2, y1), (x + shaft / 2, y1),
        (x + shaft / 2, y2 - hl), (x + head / 2, y2 - hl),
        (x, y2), (x - head / 2, y2 - hl),
        (x - shaft / 2, y2 - hl),
    ]
    f.poly(pts + [pts[0]], sw=sw, fill=fill)


def dashed_chan(f, x1, x2, y1, y2, dash="7,6", sw=1.5, caps=True):
    """两条竖直虚线构成的窄通道（进程的时间线）。"""
    f.line(x1, y1, x1, y2, dash=dash, sw=sw)
    f.line(x2, y1, x2, y2, dash=dash, sw=sw)
    if caps:
        f.line(x1, y1, x2, y1, sw=sw)
        f.line(x1, y2, x2, y2, sw=sw)


def box(f, x, y, w, h, lines, size=20, fill=BOXF, sw=1.6, lh=1.5):
    if isinstance(lines, str):
        lines = [lines]
    f.rect(x, y, w, h, fill=fill, sw=sw)
    n = len(lines)
    step = size * lh
    y0 = y + h / 2 - (n - 1) * step / 2
    for i, s in enumerate(lines):
        f.text(x + w / 2, y0 + i * step, s, size=size, bold=True)


def bez(f, p0, p1, p2, n=26, head=9, sw=1.7):
    """二次贝塞尔折线（带箭头）。"""
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        x = u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0]
        y = u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]
        pts.append((x, y))
    f.poly(pts, sw=sw, head=head)


def doc(f, x, y, w=48, h=64, fill="#fbeaa8"):
    """黄色文档图标：矩形 + 三行横线 + 右上折角。"""
    f.rect(x, y, w, h, fill=fill, sw=1.2)
    for i in range(3):
        f.line(x + 8, y + 22 + i * 12, x + w - 8, y + 22 + i * 12, sw=1.1)
    f.line(x + w - 15, y, x + w, y + 15, sw=1.1)


def cylinder(f, x, y, w, h, ry=18, sw=1.4):
    f.rect(x, y + ry, w, h - 2 * ry, sw=sw)
    f.ellipse(x + w / 2, y + ry, w / 2, ry, sw=sw)
    f.ellipse(x + w / 2, y + h - ry, w / 2, ry, sw=sw)


def brace(f, x, y1, y2, w=10, sw=1.5):
    """右侧方括号：上下横 + 竖 + 中间开口。"""
    f.line(x, y1, x + w, y1, sw=sw)
    f.line(x + w, y1, x + w, y2, sw=sw)
    f.line(x, y2, x + w, y2, sw=sw)
    mid = (y1 + y2) / 2
    f.line(x, mid, x + w, mid, sw=sw)


def vtext(f, x, y0, s, size=18, step=None, bold=True):
    """竖排文字（“就绪队列”“阻塞队列”）。"""
    step = step or size * 1.18
    for i, ch in enumerate(s):
        f.text(x, y0 + i * step, ch, size=size, bold=bold)


# ---------------------------------------------------------------- 1 五状态
def f_states(F):
    f = F(1062, 280)
    f.rect(314, 15, 486, 248, dash="6,4", rx=7, sw=1.3, stroke=GREY)
    for lb, cx, cy in (
        ("创建态", 196, 164), ("就绪态", 410, 164), ("执行态", 557, 65),
        ("阻塞态", 709, 163), ("终止态", 903, 65),
    ):
        ell(f, cx, cy, 76, 37.5, lb, size=21)
    f.arrow(52, 164, 120, 164, sw=2.1, head=10)
    f.arrow(272, 164, 334, 164, sw=2.1, head=10)
    f.arrow(633, 65, 827, 65, sw=2.1, head=10)
    f.arrow(979, 65, 1012, 65, sw=2.1, head=10)
    f.arrow(470, 95, 411, 122, sw=2.0, head=10)   # 时间片用尽
    f.text(427, 84, "时间片用尽", size=18)
    f.arrow(482, 142, 556, 102, sw=2.0, head=10)  # 进程调度
    f.text(524, 141, "进程调度", size=18)
    f.arrow(630, 80, 684, 125, sw=2.0, head=10)   # 执行 -> 阻塞
    f.text(714, 80, "I/O请求或事件等待", size=18)
    bez(f, (666, 189), (548, 252), (452, 198))  # 阻塞 -> 就绪
    f.text(570, 243, "I/O完成或事件发生", size=18)
    return f


# ---------------------------------------------------------------- 2 进程切换模型
def f_switch(F):
    f = F(1092, 616)
    f.text(322, 37, "进程P0", size=26, bold=True)
    f.text(562, 37, "操作系统", size=26, bold=True)
    f.text(905, 45, "进程P1", size=26, bold=True)
    block_arrow(f, 320, 68, 160, shaft=20, head=54, hl=30)
    block_arrow(f, 320, 180, 262, shaft=20, head=54, hl=30)
    f.text(250, 116, "运行", size=26, bold=True)
    f.text(182, 208, "特殊的运行状态", size=25, bold=True)
    dashed_chan(f, 311, 329, 266, 605)
    f.text(246, 398, "就绪", size=26, bold=True)
    f.text(246, 432, "或", size=26, bold=True)
    f.text(246, 466, "阻塞", size=26, bold=True)
    f.line(292, 171, 604, 171, sw=2.6)
    f.text(415, 139, "中断或系统调用", size=26, bold=True, anchor="start")
    f.arrow(604, 173, 604, 194, sw=1.9)
    box(f, 447, 195, 315, 47, "中断处理或系统服务", size=25)
    f.arrow(604, 242, 604, 261, sw=1.9)
    box(f, 422, 262, 365, 84, ["修改P0状态，状态信息保存到", "PCB0"], size=24, lh=1.45)
    f.arrow(604, 346, 604, 361, sw=1.9)
    box(f, 447, 362, 315, 49, "调度程序选中P1", size=25)
    f.arrow(604, 411, 604, 442, sw=1.9)
    box(f, 447, 443, 315, 53, "从PCB1读入状态信息", size=24)
    f.poly([(604, 496), (604, 519), (886, 519)], head=9, sw=1.8)
    dashed_chan(f, 893, 919, 78, 493)
    f.text(972, 297, "就绪", size=26, bold=True)
    block_arrow(f, 906, 528, 600, shaft=26, head=54, hl=30)
    f.text(996, 557, "运行", size=26, bold=True)
    return f


# ---------------------------------------------------------------- 3 进程切换模型 2
def f_switch2(F):
    f = F(754, 376)
    f.text(205, 22, "进程P0", size=20, bold=True)
    f.text(430, 22, "操作系统", size=20, bold=True)
    f.text(620, 22, "进程P1", size=20, bold=True)
    f.text(152, 64, "运行", size=20, bold=True)
    block_arrow(f, 218, 44, 106, shaft=16, head=40, hl=22)
    f.text(112, 184, "特殊的运行状态", size=19, bold=True)
    block_arrow(f, 218, 120, 190, shaft=16, head=40, hl=22)
    block_arrow(f, 218, 194, 265, shaft=16, head=40, hl=22)
    f.line(244, 122, 437, 122, sw=1.9)
    f.text(365, 96, "中断或系统调用", size=20, bold=True)
    f.arrow(437, 122, 437, 180, sw=1.8)
    box(f, 315, 182, 248, 38, "中断处理或系统服务", size=19)
    f.poly([(439, 220), (439, 268), (250, 268)], head=9, sw=1.8)
    dashed_chan(f, 608, 626, 60, 320)
    f.text(690, 140, "就绪", size=20, bold=True)
    return f


# ---------------------------------------------------------------- 4 上下文切换
def f_context(F):
    f = F(1020, 752)
    f.text(300, 42, "用户态", size=27, bold=True)
    f.text(640, 42, "内核态", size=27, bold=True)
    f.text(215, 102, "进程1", size=24, bold=True)
    f.text(400, 102, "进程2", size=24, bold=True)
    f.text(640, 102, "操作系统", size=24, bold=True)
    f.arrow(215, 122, 215, 183, sw=1.8)
    f.circle(215, 192, 7, fill="#ffffff", sw=1.5)
    f.line(215, 199, 215, 714, dash="6,5", sw=1.4)
    f.text(104, 226, "中断或系统调用", size=26, bold=True, anchor="start")
    f.line(400, 205, 400, 714, dash="6,5", sw=1.4)
    box(f, 528, 192, 277, 46, "上下文保存到PCB1", size=26)
    f.arrow(666, 238, 666, 280, sw=1.9)
    box(f, 524, 281, 281, 53, "恢复PCB2中上下文", size=26, fill=PINK)
    f.poly([(528, 334), (404, 370)], head=9, sw=1.8)
    f.circle(400, 377, 7, fill="#ffffff", sw=1.5)
    f.text(232, 448, "中断或系统调用", size=26, bold=True, anchor="start")
    f.poly([(407, 384), (640, 462)], head=9, sw=1.8)
    box(f, 524, 465, 281, 53, "上下文保存到PCB2", size=26, fill=PINK)
    f.arrow(666, 518, 666, 559, sw=1.9)
    box(f, 528, 560, 277, 46, "恢复PCB1中上下文", size=26)
    f.poly([(666, 606), (666, 656), (215, 656), (215, 710)], head=9, sw=1.8)
    return f


# ---------------------------------------------------------------- 5 三级调度
def f_sched3(F):
    f = F(1358, 706)
    f.text(46, 44, "【例】一个作业从提交给计算机系统到执行结束，一般都要经历提交、收容、执行和完成 4 个状态。",
           size=26, anchor="start", bold=True)
    box(f, 152, 159, 86, 86, "输入设备", size=17, fill="none")
    f.arrow(238, 201, 278, 188, sw=1.8)
    f.text(294, 94, "提交状态", size=19, bold=True, color=RED)
    doc(f, 281, 119)
    cylinder(f, 376, 106, 346, 412, ry=18)
    f.text(548, 502, "外存", size=19, bold=True)
    f.text(433, 152, "收容状态", size=19, bold=True, color=RED)
    for dx in (410, 524, 635):
        doc(f, dx, 178)
    f.arrow(522, 209, 460, 209, sw=1.9)
    f.arrow(633, 209, 574, 209, sw=1.9)
    f.text(548, 262, "等待队列", size=19, bold=True)
    for cy, lb, ty in ((312, "就绪挂起队列", 374), (412, "阻塞挂起队列", 488)):
        for cx in (430, 505, 580):
            f.ellipse(cx, cy, 21, 21, sw=1.4)
            f.text(cx, cy, "进程", size=14, bold=True)
        f.arrow(483, cy, 453, cy, sw=1.4)
        f.arrow(558, cy, 528, cy, sw=1.4)
        f.text(553, ty, lb, size=19, bold=True)
    f.text(798, 120, "后备作业", size=19, bold=True)
    doc(f, 775, 141)
    f.arrow(772, 205, 745, 236, sw=1.8)
    f.text(796, 232, "作业调度", size=19, bold=True)
    f.arrow(724, 252, 862, 252, sw=1.9)
    f.ellipse(797, 345, 30, 30, sw=1.4)
    f.text(797, 345, "进程", size=16, bold=True)
    f.arrow(866, 345, 830, 345, sw=1.9)
    f.arrow(764, 345, 722, 345, sw=1.9)
    f.text(796, 404, "交换调度", size=19, bold=True)
    f.rect(868, 163, 322, 342, fill="#e9eef8", sw=1.4)
    f.text(1035, 502, "内存", size=19, bold=True)
    vtext(f, 900, 250, "就绪队列", size=18)
    vtext(f, 1088, 250, "阻塞队列", size=18)
    for cx in (967, 1124):
        for cy in (232, 335, 438):
            f.ellipse(cx, cy, 35, 35, sw=1.4)
            f.text(cx, cy, "进程", size=17, bold=True)
        f.arrow(cx, 298, cx, 269, sw=1.5)
        f.arrow(cx, 401, cx, 372, sw=1.5)
    f.arrow(975, 508, 975, 611, sw=1.9)
    f.text(1046, 560, "进程调度", size=19, bold=True)
    f.ellipse(890, 552, 26, 26, sw=1.4)
    f.text(890, 552, "进程", size=15, bold=True)
    box(f, 943, 614, 60, 58, "CPU", size=17, fill="#ece7f4")
    return f


# ---------------------------------------------------------------- 6~8 线程模型
def f_one2one(F):
    f = F(424, 364)
    f.rect(34, 46, 245, 106, fill=BLUE, sw=1.2)
    f.rect(34, 152, 245, 110, fill=GREEN, sw=1.2)
    xs = (100, 135, 166, 196)
    for x in xs:
        f.rect(x, 61, 22, 63, fill="#ffffff", sw=1.3)
        f.rect(x, 166, 22, 63, fill="#ffffff", sw=1.3)
        f.line(x + 11, 124, x + 11, 166, sw=1.3)
    f.text(305, 19, "用户线程", size=21, bold=True)
    for x in xs:
        f.arrow(238, 33, x + 11, 57, sw=1.4)
    f.text(307, 292, "核心线程", size=21, bold=True)
    for x in xs:
        f.arrow(240, 286, x + 11, 234, sw=1.4)
    brace(f, 290, 46, 260)
    f.text(362, 111, "用户空间", size=20, bold=True)
    f.text(362, 216, "内核空间", size=20, bold=True)
    f.text(200, 338, "一对一模型", size=21, bold=True)
    return f


def f_many2one(F):
    f = F(526, 338)
    f.rect(94, 59, 229, 102, fill=BLUE, sw=1.2)
    f.rect(94, 161, 229, 106, fill=GREEN, sw=1.2)
    xs = (170, 198, 226)
    for x in xs:
        f.rect(x, 62, 22, 73, fill="#ffffff", sw=1.3)
        f.line(x + 11, 135, x + 11, 155, sw=1.3)
    f.line(181, 155, 237, 155, sw=1.3)
    f.line(214, 155, 214, 166, sw=1.3)
    f.rect(203, 166, 22, 70, fill="#ffffff", sw=1.3)
    f.text(330, 28, "用户线程", size=20, bold=True)
    for x in xs:
        f.arrow(292, 42, x + 11, 58, sw=1.4)
    f.text(362, 296, "核心线程", size=20, bold=True)
    f.arrow(300, 288, 227, 240, sw=1.4)
    brace(f, 331, 59, 272)
    f.text(400, 122, "用户空间", size=19, bold=True)
    f.text(400, 225, "内核空间", size=19, bold=True)
    f.text(233, 328, "多对一模型", size=20, bold=True)
    return f


def f_many2many(F):
    f = F(610, 468)
    f.rect(109, 81, 256, 143, fill=BLUE, sw=1.2)
    f.rect(109, 224, 256, 146, fill=GREEN, sw=1.2)
    ux = (176, 205, 238, 270, 302)
    for x in ux:
        f.rect(x, 91, 22, 94, fill="#ffffff", sw=1.3)
        f.line(x + 11, 185, x + 11, 205, sw=1.3)
    f.line(187, 205, 313, 205, sw=1.3)
    kx = (205, 240, 270)
    f.line(240, 205, 240, 248, sw=1.3)
    for x in kx:
        f.rect(x, 248, 22, 92, fill="#ffffff", sw=1.3)
    f.text(350, 33, "用户线程", size=21, bold=True)
    for x in ux:
        f.arrow(392, 46, x + 11, 87, sw=1.4)
    f.text(350, 406, "核心线程", size=21, bold=True)
    for x in kx:
        f.arrow(410, 384, x + 11, 344, sw=1.4)
    brace(f, 375, 81, 368)
    f.text(432, 152, "用户空间", size=20, bold=True)
    f.text(440, 304, "内核空间", size=20, bold=True)
    f.text(320, 445, "多对多模型", size=21, bold=True)
    return f
