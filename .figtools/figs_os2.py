# -*- coding: utf-8 -*-
"""为《操作系统》笔记新增的示意图（风格与 figs_os.py 一致：白底、黑色描边、黑体）。"""

import svgkit
from svgkit import Fig

svgkit.FONT_SVG = "'Microsoft YaHei', 'SimHei', sans-serif"

INK = svgkit.INK
BOXF = "#ededed"
SOFT = "#f7f7f7"
BLUE = "#dce6f3"
GREEN = "#d9e3cc"
PINK = "#f2d7d3"


# ---------------------------------------------------------------- 基础图元
def boxr(f, x, y, w, h, lines, size=17, fill=BOXF, sw=1.5, rx=7, lh=1.4, bold=False):
    if isinstance(lines, str):
        lines = [lines]
    f.rect(x, y, w, h, fill=fill, sw=sw, rx=rx)
    n = len(lines)
    gap = size * lh
    y0 = y + h / 2 - (n - 1) * gap / 2
    for i, s in enumerate(lines):
        f.text(x + w / 2, y0 + i * gap, s, size=size, bold=bold)


def plain(f, x, y, w, h, lines, size=17, sw=1.4, lh=1.4, anchor="middle"):
    """无填充的白框。"""
    if isinstance(lines, str):
        lines = [lines]
    f.rect(x, y, w, h, fill="#ffffff", sw=sw, rx=5)
    n = len(lines)
    gap = size * lh
    y0 = y + h / 2 - (n - 1) * gap / 2
    for i, s in enumerate(lines):
        cx = x + w / 2 if anchor == "middle" else x + 10
        f.text(cx, y0 + i * gap, s, size=size, anchor=anchor)


def dia(f, cx, cy, w, h, s, size=16, fill="#ffffff", sw=1.4):
    pts = [(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy), (cx, cy - h / 2)]
    f.poly(pts, sw=sw, fill=fill)
    f.text(cx, cy, s, size=size)


def adown(f, x, y1, y2, sw=1.5, head=9):
    f.arrow(x, y1, x, y2, sw=sw, head=head)


# ---------------------------------------------------------------- 1 中断处理流程
def f_interrupt(F):
    f = F(880, 430)
    boxr(f, 260, 24, 320, 46, "中断请求（外设、时钟、故障）", size=17)
    adown(f, 420, 70, 100)
    boxr(f, 180, 100, 440, 104,
         ["中断隐指令（由硬件自动完成，不是程序指令）",
          "① 关中断　　② 保存断点（PC、PSW）", "③ 引出中断服务程序"], size=16, lh=1.5)
    adown(f, 420, 204, 232)
    boxr(f, 180, 232, 440, 104,
         ["中断服务程序（软件完成）", "① 保存现场　　② 处理中断", "③ 恢复现场、开中断"], size=16, lh=1.5)
    adown(f, 420, 336, 364)
    boxr(f, 260, 364, 320, 44, "返回断点，继续执行原程序", size=17)
    f.text(64, 152, "硬件", size=16, bold=True)
    f.text(64, 284, "软件", size=16, bold=True)
    f.line(96, 152, 176, 152, sw=1.2, dash="5,4")
    f.line(96, 284, 176, 284, sw=1.2, dash="5,4")
    return f


# ---------------------------------------------------------------- 2 系统调用过程
def f_syscall(F):
    f = F(860, 340)
    f.line(30, 158, 830, 158, sw=1.3, dash="7,6")
    f.text(30, 60, "用户态", size=16, anchor="start", bold=True)
    f.text(30, 268, "内核态", size=16, anchor="start", bold=True)
    boxr(f, 110, 46, 210, 56, "用户程序执行", size=17)
    f.arrow(320, 74, 372, 74, sw=1.6, head=9)
    boxr(f, 372, 40, 250, 68, ["执行系统调用", "（陷入指令 trap）"], size=17, lh=1.45)
    f.arrow(497, 108, 497, 210, sw=1.6, head=9)
    f.text(512, 138, "陷入内核态：保存现场、查系统调用表", size=15, anchor="start")
    boxr(f, 372, 210, 250, 68, ["内核执行服务例程", "（读写文件、申请内存…）"], size=17, lh=1.45)
    f.poly([(372, 244), (110, 244), (110, 102)], sw=1.6, head=9)
    f.text(300, 306, "处理完毕返回用户态，带回返回值、恢复现场", size=15, anchor="middle")
    f.text(124, 120, "继续执行", size=15, anchor="start")
    return f


# ---------------------------------------------------------------- 3 进程状态队列
def f_queues(F):
    f = F(880, 360)
    boxr(f, 390, 30, 110, 52, "CPU", size=18)
    plain(f, 120, 150, 260, 118, "", sw=1.4)
    f.text(250, 140, "就绪队列", size=17, bold=True)
    for i, cx in enumerate((178, 250, 322)):
        f.circle(cx, 205, 26, fill="#ffffff", sw=1.3)
        f.text(cx, 205, "进程", size=15)
    plain(f, 520, 150, 260, 118, "", sw=1.4)
    f.text(650, 140, "阻塞队列", size=17, bold=True)
    for cx in (578, 650, 722):
        f.circle(cx, 205, 26, fill="#ffffff", sw=1.3)
        f.text(cx, 205, "进程", size=15)
    boxr(f, 640, 24, 120, 44, "终止", size=17)
    f.text(60, 209, "新建", size=16, bold=True)
    f.arrow(96, 209, 118, 209, sw=1.5, head=9)
    f.arrow(300, 148, 400, 84, sw=1.5, head=9)
    f.text(292, 88, "被调度", size=15, anchor="middle")
    f.arrow(410, 84, 320, 148, sw=1.5, head=9)
    f.text(408, 136, "时间片到", size=15, anchor="start")
    f.arrow(500, 84, 600, 148, sw=1.5, head=9)
    f.text(556, 92, "等待事件", size=15, anchor="middle")
    f.arrow(518, 246, 384, 246, sw=1.5, head=9)
    f.text(452, 268, "事件发生", size=15, anchor="middle")
    f.arrow(502, 48, 638, 48, sw=1.5, head=9)
    f.text(566, 30, "运行结束", size=15, anchor="middle")
    f.text(440, 330, "就绪队列按优先级或到达顺序排队，阻塞队列按等待的事件排队", size=15)
    return f


# ---------------------------------------------------------------- 4 生产者-消费者
def f_pc(F):
    f = F(900, 520)
    left = [("生产一个数据", 40), ("P(empty)", 106), ("P(mutex)", 172),
            ("放入缓冲区", 238), ("V(mutex)", 304), ("V(full)", 370)]
    for s, y in left:
        boxr(f, 120, y, 200, 46, s, size=17)
    for i in range(len(left) - 1):
        adown(f, 220, left[i][1] + 46, left[i + 1][1])
    right = [("P(full)", 40), ("P(mutex)", 106), ("取出数据", 172),
             ("V(mutex)", 238), ("V(empty)", 304), ("消费数据", 370)]
    for s, y in right:
        boxr(f, 580, y, 200, 46, s, size=17)
    for i in range(len(right) - 1):
        adown(f, 680, right[i][1] + 46, right[i + 1][1])
    boxr(f, 386, 150, 128, 120, ["缓冲区", "n 个单元"], size=17, fill=SOFT, lh=1.6)
    f.poly([(320, 261), (386, 230)], sw=1.5, head=9)
    f.poly([(514, 200), (580, 195)], sw=1.5, head=9)
    f.text(450, 300, "互斥访问缓冲区", size=15)
    f.text(450, 452, "顺序：先 P(empty)/P(full)，再 P(mutex)——反过来可能死锁", size=15)
    f.text(220, 24, "生产者", size=17, bold=True)
    f.text(680, 24, "消费者", size=17, bold=True)
    return f


# ---------------------------------------------------------------- 5 资源分配图
def f_rag(F):
    f = F(780, 420)
    f.circle(170, 120, 40, fill="#ffffff", sw=1.5)
    f.text(170, 120, "P1", size=18, bold=True)
    f.circle(170, 270, 40, fill="#ffffff", sw=1.5)
    f.text(170, 270, "P2", size=18, bold=True)
    plain(f, 470, 76, 150, 84, "", sw=1.5)
    f.text(545, 66, "R1（2 个实例）", size=15)
    for cx in (516, 570):
        f.circle(cx, 118, 13, fill="#ffffff", sw=1.2)
    plain(f, 470, 226, 150, 84, "", sw=1.5)
    f.text(545, 216, "R2（1 个实例）", size=15)
    f.circle(545, 268, 13, fill="#ffffff", sw=1.2)
    f.arrow(210, 106, 466, 96, sw=1.4, dash="6,5", head=9)
    f.arrow(466, 132, 212, 132, sw=1.5, head=9)
    f.arrow(210, 284, 466, 292, sw=1.4, dash="6,5", head=9)
    f.arrow(466, 256, 212, 264, sw=1.5, head=9)
    f.text(390, 340, "虚线：请求边（P 等 R）　　实线：分配边（R 已给 P）", size=15)
    f.text(390, 372, "R1 的两个实例都给了 P1，R2 给了 P2，P1 与 P2 互相等待 → 死锁", size=15)
    return f


# ---------------------------------------------------------------- 6 分页地址变换
def f_paging(F):
    f = F(900, 440)
    f.text(20, 63, "逻辑地址", size=15, anchor="start")
    f.row_cells(110, 40, [230, 130], h=46, labels=["页号 P", "页内偏移 W"], size=17)
    f.text(150, 100, "高位部分", size=13)
    f.text(380, 100, "低位部分", size=13)
    f.arrow(405, 86, 405, 128, sw=1.5, head=9)
    f.text(420, 108, "偏移量不变", size=14, anchor="start")
    f.text(20, 153, "物理地址", size=15, anchor="start")
    f.row_cells(110, 130, [230, 130], h=46, labels=["物理块号 b", "页内偏移 W"], size=17)
    f.text(665, 112, "页表（内存中）", size=15)
    f.table(560, 130, [90, 120], [36, 34, 34, 34],
            {(0, 0): "页号", (0, 1): "物理块号", (1, 0): "0", (1, 1): "5",
             (2, 0): "1", (2, 1): "8", (3, 0): "2", (3, 1): "2"}, size=15, header_bold=True)
    f.poly([(558, 202), (330, 202), (330, 180)], sw=1.5, head=9)
    f.text(444, 190, "取出块号 b", size=13)
    boxr(f, 560, 300, 210, 54, ["页表寄存器 PTR", "页表起始地址 + 页表长度"], size=15, lh=1.5)
    f.arrow(665, 300, 665, 268, sw=1.5, head=9)
    f.text(450, 396, "① 越界检查：P 与页表长度比较　② 查页表得物理块号 b　③ b 与 W 拼接成物理地址", size=14)
    return f


# ---------------------------------------------------------------- 7 缺页中断处理
def f_page_fault(F):
    f = F(900, 540)
    boxr(f, 350, 24, 200, 44, "访问某逻辑地址", size=17)
    adown(f, 450, 68, 96)
    dia(f, 450, 136, 240, 80, "所需页在内存？", size=16)
    boxr(f, 690, 114, 150, 44, "继续执行", size=17)
    f.arrow(570, 136, 688, 136, sw=1.5, head=9)
    f.text(620, 118, "是", size=15)
    adown(f, 450, 176, 204)
    f.text(466, 192, "否", size=15, anchor="start")
    boxr(f, 330, 204, 240, 44, "产生缺页中断（内中断）", size=16)
    adown(f, 450, 248, 276)
    dia(f, 450, 316, 260, 80, "内存有空闲页框？", size=16)
    boxr(f, 60, 294, 190, 44, "分配一个空闲页框", size=16)
    f.arrow(318, 316, 252, 316, sw=1.5, head=9)
    f.text(300, 300, "有", size=15)
    boxr(f, 680, 294, 190, 44, "按置换算法选淘汰页", size=16)
    f.arrow(582, 316, 678, 316, sw=1.5, head=9)
    f.text(626, 300, "无", size=15)
    boxr(f, 330, 386, 240, 44, "从外存调入所需的页", size=16)
    adown(f, 450, 356, 386)
    f.poly([(155, 338), (155, 408), (326, 408)], sw=1.5, head=9)
    f.poly([(775, 338), (775, 408), (574, 408)], sw=1.5, head=9)
    f.text(872, 434, "被淘汰页若被修改过，需先写回外存", size=13, anchor="end")
    adown(f, 450, 430, 458)
    boxr(f, 330, 458, 240, 40, "修改页表，重新执行该指令", size=16)
    return f


# ---------------------------------------------------------------- 8 文件物理结构
def f_file_alloc(F):
    f = F(900, 500)
    # 连续分配
    f.text(30, 52, "连续分配", size=17, anchor="start", bold=True)
    for i in range(8):
        x = 170 + i * 76
        fill = BOXF if 3 <= i <= 5 else "#ffffff"
        f.rect(x, 30, 66, 40, fill=fill, sw=1.3)
        f.text(x + 33, 50, str(i), size=15)
    f.text(620, 92, "FCB 记起始块号 3、长度 3", size=14, anchor="middle")
    # 链接分配
    f.text(30, 210, "链接分配", size=17, anchor="start", bold=True)
    ch = [(170, 3), (330, 7), (490, 1)]
    for x, n in ch:
        f.rect(x, 188, 66, 40, fill=BOXF, sw=1.3)
        f.text(x + 33, 208, "块 " + str(n), size=14)
    f.arrow(236, 208, 328, 208, sw=1.4, head=9)
    f.arrow(396, 208, 488, 208, sw=1.4, head=9)
    f.text(240, 178, "下一块指针", size=13)
    f.text(400, 178, "下一块指针", size=13)
    f.text(660, 208, "每块末尾存下一块的块号", size=14, anchor="middle")
    # 索引分配
    f.text(30, 370, "索引分配", size=17, anchor="start", bold=True)
    boxr(f, 160, 326, 104, 84, ["索引块", "（索引表）"], size=15, lh=1.5)
    for i in range(3):
        y = 324 + i * 46
        f.rect(430, y, 66, 40, fill=BOXF, sw=1.3)
        f.text(463, y + 20, "块 " + str([3, 7, 1][i]), size=14)
        f.arrow(266, 348 + i * 10, 426, y + 20, sw=1.3, head=8)
    f.text(520, 344, "索引块里按顺序存", size=14, anchor="start")
    f.text(520, 368, "放各数据块块号", size=14, anchor="start")
    return f


# ---------------------------------------------------------------- 9 UNIX 混合索引
def f_inode(F):
    f = F(900, 500)
    boxr(f, 40, 60, 150, 60, ["inode", "文件控制信息"], size=16, lh=1.4)
    rows = ["直接地址 0", "直接地址 1", "…", "直接地址 9", "一次间接", "二次间接", "三次间接"]
    ys = [130, 164, 198, 232, 272, 312, 352]
    for s, y in zip(rows, ys):
        f.rect(40, y, 150, 32, fill=BOXF if "间接" not in s else SOFT, sw=1.2)
        f.text(115, y + 16, s, size=14)
    f.text(115, 40, "索引结点（内存/磁盘）", size=15)
    for i in range(4):
        f.rect(250, 130 + i * 34, 46, 32, fill=BOXF, sw=1.2)
        f.text(273, 146 + i * 34, "数据块", size=12)
        f.line(192, 146 + i * 34, 248, 146 + i * 34, sw=1.1)
    f.text(273, 118, "直接块（10 个）", size=14, anchor="middle")
    # 一次间接
    boxr(f, 250, 262, 90, 40, "索引块", size=14)
    f.arrow(190, 288, 248, 282, sw=1.4, head=8)
    f.rect(390, 262, 60, 40, fill=BOXF, sw=1.2)
    f.text(420, 282, "数据", size=13)
    f.arrow(340, 282, 388, 282, sw=1.4, head=8)
    f.text(470, 282, "256 个块号", size=14, anchor="start")
    # 二次间接
    boxr(f, 250, 322, 90, 40, "索引块", size=14)
    f.arrow(190, 328, 248, 334, sw=1.4, head=8)
    boxr(f, 380, 314, 90, 40, "索引块", size=14)
    f.arrow(340, 342, 378, 338, sw=1.4, head=8)
    f.rect(510, 314, 60, 40, fill=BOXF, sw=1.2)
    f.text(540, 334, "数据", size=13)
    f.arrow(470, 334, 508, 334, sw=1.4, head=8)
    f.text(590, 334, "256×256 个块号", size=14, anchor="start")
    # 三次间接
    boxr(f, 250, 382, 90, 40, "索引块", size=14)
    f.arrow(190, 368, 248, 394, sw=1.4, head=8)
    f.text(360, 404, "再经两级索引块（256³ 个块号）", size=14, anchor="start")
    f.text(40, 444, "最大文件 = (10 + 256 + 256² + 256³) × 块大小", size=15, anchor="start")
    f.text(40, 470, "块大小 4KB、指针 4B 时约 40KB + 1MB + 256MB + 64GB", size=15, anchor="start")
    return f


# ---------------------------------------------------------------- 10 磁盘调度轨迹
def f_disk(F):
    f = F(900, 480)
    y0, y1 = 420, 60          # 磁道 0 → y1, 磁道 200 → y0
    def yv(t):
        return y0 - (y0 - y1) * t / 200.0
    f.line(90, y1, 90, y0, sw=1.4)
    for t in (0, 50, 100, 150, 200):
        f.line(84, yv(t), 90, yv(t), sw=1.2)
        f.text(70, yv(t), str(t), size=13, anchor="end")
    f.text(70, 40, "磁道号", size=14, anchor="end")
    f.text(500, 462, "请求到达的先后顺序 →", size=15)
    reqs = [55, 58, 39, 18, 90, 160, 150, 38, 184]
    start = 100
    xs = [170 + 72 * i for i in range(len(reqs) + 1)]
    sstf = [100, 90, 58, 55, 39, 38, 18, 150, 160, 184]
    pts_f = [(xs[i], yv(v)) for i, v in enumerate([start] + reqs)]
    f.poly(pts_f, sw=1.6)
    pts_s = [(xs[i], yv(v)) for i, v in enumerate(sstf)]
    f.poly(pts_s, sw=1.6, dash="6,5")
    for i, (x, v) in enumerate(zip(xs, [start] + reqs)):
        f.circle(x, yv(v), 4, fill=INK, sw=1)
        f.text(x, yv(v) - 16, str(v), size=13)
    f.text(170, 448, "起点 100", size=13, anchor="middle")
    f.line(600, 430, 650, 430, sw=1.6)
    f.text(660, 430, "FCFS", size=14, anchor="start")
    f.line(600, 452, 650, 452, sw=1.6, dash="6,5")
    f.text(660, 452, "SSTF", size=14, anchor="start")
    return f


# ---------------------------------------------------------------- 11 缓冲时序
def f_buffer(F):
    f = F(900, 460)
    axis_y = 400
    f.line(90, axis_y, 850, axis_y, sw=1.4)
    for i in range(9):
        x = 90 + i * 90
        f.line(x, axis_y, x, axis_y - 6, sw=1.2)
        f.text(x, axis_y + 18, str(i), size=13)
    f.text(858, axis_y + 18, "时间", size=13, anchor="start")

    def seg(row_y, x0, x1, label, fill, h=30, size=13):
        f.rect(x0, row_y, x1 - x0, h, fill=fill, sw=1.3)
        f.text((x0 + x1) / 2, row_y + h / 2, label, size=size)

    # 单缓冲：T 与 M 串行，C 与 T 重叠
    f.text(20, 44, "单缓冲", size=16, anchor="start", bold=True)
    seq1 = [(90, 220, "T 磁盘→缓冲", BOXF), (220, 340, "M 缓冲→用户", SOFT),
            (340, 470, "T", BOXF), (470, 590, "M", SOFT),
            (590, 720, "T", BOXF), (720, 840, "M", SOFT)]
    for x0, x1, lb, fl in seq1:
        seg(32, x0, x1, lb, fl)
    f.text(20, 96, "CPU", size=14, anchor="start")
    for x0, x1 in ((90, 340), (340, 590), (590, 840)):
        seg(84, x0, x1, "C 处理", BLUE, h=26)
    f.text(480, 150, "每块平均耗时 = max(C, T) + M", size=16)

    # 双缓冲：T 与 M 并行
    f.text(20, 200, "双缓冲", size=16, anchor="start", bold=True)
    for x0, x1, lb in ((90, 300, "T 磁盘→缓冲1"), (300, 510, "T 磁盘→缓冲2"), (510, 720, "T 磁盘→缓冲1")):
        seg(186, x0, x1, lb, BOXF)
    for x0, x1, lb in ((140, 300, "M 缓冲1→用户"), (350, 510, "M 缓冲2→用户"), (560, 720, "M 缓冲1→用户")):
        seg(226, x0, x1, lb, SOFT)
    f.text(20, 292, "CPU", size=14, anchor="start")
    for x0, x1 in ((90, 300), (300, 510), (510, 720)):
        seg(280, x0, x1, "C 处理", BLUE, h=26)
    f.text(480, 344, "两块缓冲交替使用：T 与 M 可并行，每块耗时 = max(C + M, T)", size=16)
    return f


# ---------------------------------------------------------------- 12 SPOOLing
def f_spool(F):
    f = F(880, 360)
    f.rect(330, 24, 200, 290, dash="7,6", sw=1.3)
    f.text(430, 308, "磁盘上的输入井 / 输出井", size=14)
    boxr(f, 40, 60, 120, 60, ["输入设备", "（键盘）"], size=15, lh=1.4)
    boxr(f, 190, 60, 120, 60, ["输入进程"], size=16)
    boxr(f, 350, 50, 160, 80, ["输入井", "（暂存作业数据）"], size=15, lh=1.5, fill=SOFT)
    boxr(f, 560, 60, 130, 60, ["用户进程"], size=16)
    f.arrow(160, 90, 188, 90, sw=1.5, head=9)
    f.arrow(310, 90, 348, 90, sw=1.5, head=9)
    f.arrow(510, 90, 558, 90, sw=1.5, head=9)
    boxr(f, 560, 230, 130, 60, ["输出设备", "（打印机）"], size=15, lh=1.4)
    boxr(f, 350, 220, 160, 80, ["输出井", "（暂存输出数据）"], size=15, lh=1.5, fill=SOFT)
    boxr(f, 190, 230, 120, 60, ["输出进程"], size=16)
    f.arrow(558, 260, 512, 260, sw=1.5, head=9)
    f.arrow(348, 260, 312, 260, sw=1.5, head=9)
    f.arrow(190, 260, 162, 260, sw=1.5, head=9)
    f.poly([(610, 122), (610, 228)], sw=1.5, head=9)
    f.text(626, 180, "写文件", size=14, anchor="start")
    f.text(440, 336, "申请打印时只写入输出井，真正打印由输出进程按队列完成", size=14)
    return f


FLOW = [
    ("中断处理流程", "f_interrupt"),
    ("系统调用过程", "f_syscall"),
    ("进程状态队列", "f_queues"),
    ("生产者消费者PV", "f_pc"),
    ("资源分配图", "f_rag"),
    ("分页地址变换", "f_paging"),
    ("缺页中断处理", "f_page_fault"),
    ("文件物理结构", "f_file_alloc"),
    ("UNIX混合索引", "f_inode"),
    ("磁盘调度轨迹", "f_disk"),
    ("缓冲时序", "f_buffer"),
    ("SPOOLing", "f_spool"),
]
