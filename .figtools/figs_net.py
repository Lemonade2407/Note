# -*- coding: utf-8 -*-
"""计算机网络笔记的示意图（SVG + PIL 预览）。"""

import svgkit

svgkit.FONT_SVG = "'Microsoft YaHei', 'SimHei', sans-serif"

INK = "#2b2b2b"
BOXF = "#ededed"
BLUE = "#dce6f3"
GREEN = "#d9e3cc"
PINK = "#f2d7d3"
YELL = "#fdf6cf"
ORANGE = "#fbe3cf"
RED = "#c00000"


def boxr(f, x, y, w, h, lines, size=16, fill=BOXF, sw=1.4, rx=6, lh=1.4, bold=False, color=None):
    f.rect(x, y, w, h, fill=fill, sw=sw, rx=rx)
    lines = lines if isinstance(lines, (list, tuple)) else [lines]
    n = len(lines)
    y0 = y + h / 2 - (n - 1) * size * lh / 2
    for i, s in enumerate(lines):
        f.text(x + w / 2, y0 + i * size * lh, s, size=size, bold=bold, color=color)


def plain(f, x, y, w, h, lines, size=16, sw=1.4, rx=6, lh=1.4, bold=False):
    boxr(f, x, y, w, h, lines, size=size, fill="#ffffff", sw=sw, rx=rx, lh=lh, bold=bold)


def lab(f, x, y, s, size=15, anchor="middle", color=INK, bold=False):
    f.text(x, y, s, size=size, anchor=anchor, color=color, bold=bold)


def adown(f, x, y1, y2, sw=1.5, head=9):
    f.arrow(x, y1, x, y2, sw=sw, head=head)


def cells(f, x, y, widths, h, labels, fills=None, size=15, sw=1.4):
    cx = x
    for i, w in enumerate(widths):
        f.rect(cx, y, w, h, fill=(fills or {}).get(i, "#ffffff"), sw=sw)
        if i < len(labels) and labels[i]:
            f.text(cx + w / 2, y + h / 2, labels[i], size=size)
        cx += w
    return cx


def title(f, s, size=17):
    f.text(30, 28, s, size=size, anchor="start", bold=True)


# ---------------------------------------------------------------- 1 封装
def f_encap(Fig):
    f = Fig(900, 470)
    title(f, "逐层封装：每层加上本层首部；接收端按相反顺序逐层解封装")
    R = 790
    y1, y2, y3, y4, y5 = 62, 130, 198, 266, 334
    hh = 44

    f.rect(440, y1, R - 440, hh, fill=GREEN, sw=1.4)
    lab(f, (440 + R) / 2, y1 + hh / 2, "应用数据（报文）", 15)
    lab(f, 220, y1 + hh / 2, "应用层", 16, anchor="end")

    f.rect(376, y2, 64, hh, fill=BLUE, sw=1.4)
    lab(f, 408, y2 + hh / 2, "TCP 首部", 13)
    f.rect(440, y2, R - 440, hh, fill=GREEN, sw=1.4)
    lab(f, (440 + R) / 2, y2 + hh / 2, "应用数据", 15)
    lab(f, 220, y2 + hh / 2, "传输层（报文段）", 16, anchor="end")

    f.rect(312, y3, 64, hh, fill=ORANGE, sw=1.4)
    lab(f, 344, y3 + hh / 2, "IP 首部", 13)
    f.rect(376, y3, 64, hh, fill=BLUE, sw=1.4)
    lab(f, 408, y3 + hh / 2, "TCP 首部", 13)
    f.rect(440, y3, R - 440, hh, fill=GREEN, sw=1.4)
    lab(f, (440 + R) / 2, y3 + hh / 2, "应用数据", 15)
    lab(f, 220, y3 + hh / 2, "网络层（分组）", 16, anchor="end")

    f.rect(256, y4, 56, hh, fill=YELL, sw=1.4)
    lab(f, 284, y4 + hh / 2, "帧首部", 12)
    f.rect(312, y4, 64, hh, fill=ORANGE, sw=1.4)
    lab(f, 344, y4 + hh / 2, "IP 首部", 13)
    f.rect(376, y4, 64, hh, fill=BLUE, sw=1.4)
    lab(f, 408, y4 + hh / 2, "TCP 首部", 13)
    f.rect(440, y4, R - 440, hh, fill=GREEN, sw=1.4)
    lab(f, (440 + R) / 2, y4 + hh / 2, "应用数据", 15)
    f.rect(R, y4, 40, hh, fill=YELL, sw=1.4)
    lab(f, R + 20, y4 + hh / 2, "帧尾", 12)
    lab(f, 220, y4 + hh / 2, "链路层（帧）", 16, anchor="end")

    f.rect(256, y5, 574, hh, fill="#ffffff", sw=1.4, dash="6,4")
    lab(f, 543, y5 + hh / 2, "比特流（0101…）", 15)
    lab(f, 220, y5 + hh / 2, "物理层", 16, anchor="end")

    for yy in (y1, y2, y3, y4):
        adown(f, 700, yy + hh + 2, yy + 64, sw=1.3, head=8)
    f.text(430, 430, "箭头方向：发送端逐层加首部，接收端逐层去首部", size=14, anchor="start")
    return f


# ---------------------------------------------------------------- 2 编码
def f_encode(Fig):
    bits = [1, 0, 1, 1, 0, 0, 1, 0]
    f = Fig(900, 420)
    title(f, "常用数字编码波形：不归零、曼彻斯特、差分曼彻斯特")
    x0, cw = 150, 78
    n = len(bits)
    x_end = x0 + n * cw

    for i, b in enumerate(bits):
        lab(f, x0 + i * cw + cw / 2, 56, str(b), 16)
    for i in range(n + 1):
        x = x0 + i * cw
        f.line(x, 66, x, 350, sw=0.9, dash="4,4")
    lab(f, x0 - 16, 40, "数据比特", 14, anchor="end")

    # 不归零
    yhi, ylo = 100, 136
    lab(f, x0 - 16, (yhi + ylo) / 2, "不归零 NRZ", 15, anchor="end")
    pts = [(x0, yhi if bits[0] else ylo)]
    for i, b in enumerate(bits):
        xa = x0 + i * cw
        y = yhi if b else ylo
        pts.append((xa, y))
        pts.append((xa + cw, y))
    f.poly(pts, sw=1.9)

    # 曼彻斯特
    yhi, ylo = 200, 236
    lab(f, x0 - 16, (yhi + ylo) / 2, "曼彻斯特", 15, anchor="end")
    for i, b in enumerate(bits):
        xa = x0 + i * cw
        if b:
            f.line(xa, yhi, xa + cw / 2, yhi, sw=1.9)
            f.line(xa + cw / 2, yhi, xa + cw / 2, ylo, sw=1.9)
            f.line(xa + cw / 2, ylo, xa + cw, ylo, sw=1.9)
        else:
            f.line(xa, ylo, xa + cw / 2, ylo, sw=1.9)
            f.line(xa + cw / 2, ylo, xa + cw / 2, yhi, sw=1.9)
            f.line(xa + cw / 2, yhi, xa + cw, yhi, sw=1.9)

    # 差分曼彻斯特
    yhi, ylo = 300, 336
    lab(f, x0 - 16, (yhi + ylo) / 2, "差分曼彻斯特", 15, anchor="end")
    level = 1
    prev_y = yhi
    for i, b in enumerate(bits):
        xa = x0 + i * cw
        if b == 0:
            level = 1 - level
        ya = yhi if level else ylo
        yb = ylo if level else yhi
        f.line(xa, prev_y, xa, ya, sw=1.9)
        f.line(xa, ya, xa + cw / 2, ya, sw=1.9)
        f.line(xa + cw / 2, ya, xa + cw / 2, yb, sw=1.9)
        f.line(xa + cw / 2, yb, xa + cw, yb, sw=1.9)
        prev_y = yb
    f.text(30, 392, "曼彻斯特：每位中间必有跳变，1 高→低、0 低→高；差分曼彻斯特：位开始处跳变表示 0、不跳变表示 1", size=14, anchor="start")
    return f


# ---------------------------------------------------------------- 3 滑动窗口
def f_windows(Fig):
    f = Fig(940, 580)
    title(f, "停止等待、后退 N 帧（GBN）、选择重传（SR）的时空图（时间向下）")
    panels = [("停止等待", 70), ("后退 N 帧 GBN", 370), ("选择重传 SR", 660)]
    tw = 200
    top, bot = 120, 520

    def send(px, y, label, dash=None, color=INK, size=12):
        f.arrow(px + 26, y, px + 26 + tw, y + 26, sw=1.4, dash=dash, head=8)
        f.text(px + 34, y - 12, label, size=size, anchor="start", color=color)

    def ack(px, y, label, dash="5,3", color=INK, size=12):
        f.arrow(px + 26 + tw, y, px + 26, y + 26, sw=1.4, dash=dash, head=8)
        f.text(px + 18 + tw, y - 12, label, size=size, anchor="end", color=color)

    for name, px in panels:
        lab(f, px + 26 + tw / 2, 82, name, 16, bold=True)
        f.line(px + 26, top - 14, px + 26, bot, sw=1.1, dash="4,4")
        f.line(px + 26 + tw, top - 14, px + 26 + tw, bot, sw=1.1, dash="4,4")
        f.text(px + 18, 104, "发送", 12, anchor="end")
        f.text(px + 34 + tw, 104, "接收", 12, anchor="start")

    # 停止等待
    px = 70
    send(px, 130, "帧 0")
    ack(px, 170, "ACK0")
    send(px, 214, "帧 1")
    ack(px, 254, "ACK1")
    send(px, 298, "帧 2")
    ack(px, 338, "ACK2")
    f.text(px, 430, "每发一帧就停下等确认", size=12, anchor="start")
    f.text(px, 450, "信道利用率低", size=12, anchor="start")

    # GBN
    px = 370
    send(px, 130, "帧 0")
    send(px, 164, "帧 1", color=RED)
    send(px, 198, "帧 2")
    send(px, 232, "帧 3")
    ack(px, 276, "ACK0")
    send(px, 320, "帧 1", color="#1f5fa0")
    send(px, 354, "帧 2", color="#1f5fa0")
    send(px, 388, "帧 3", color="#1f5fa0")
    f.text(px, 462, "帧 1 丢失 → 超时后重传 1、2、3", size=12, anchor="start", color=RED)

    # SR
    px = 660
    send(px, 130, "帧 0")
    send(px, 164, "帧 1", color=RED)
    send(px, 198, "帧 2")
    send(px, 232, "帧 3")
    ack(px, 276, "ACK0")
    ack(px, 310, "ACK2")
    ack(px, 344, "ACK3")
    send(px, 386, "帧 1", color="#1f5fa0")
    f.text(px, 462, "帧 1 丢失 → 只重传丢失的那一帧", size=12, anchor="start", color=RED)

    f.text(30, 556, "窗口大小：停止等待 W=1；GBN 接收窗口为 1、出错后重传该帧及其后所有帧；SR 收发窗口都大于 1，可乱序接收并逐帧确认",
           size=13, anchor="start")
    return f


# ---------------------------------------------------------------- 4 CSMA/CD
def f_csma(Fig):
    f = Fig(900, 430)
    title(f, "CSMA/CD：争用期 2τ 内可能发生冲突，故帧长不能太短")
    ax, by = 100, 250
    f.line(80, 60, 80, 330, sw=0, dash=None)
    lab(f, 60, ax, "A", 16, anchor="end")
    lab(f, 60, by, "B", 16, anchor="end")
    f.line(80, ax, 860, ax, sw=1.0, dash="5,4")
    f.line(80, by, 860, by, sw=1.0, dash="5,4")

    # A 的发送与传播
    f.arrow(140, ax, 470, 168, sw=1.8, head=9)
    f.text(200, 82, "t=0 时 A 开始发送", size=13, anchor="start")
    # B 的发送（在 A 的信号到达前）
    f.arrow(360, by, 470, 168, sw=1.8, head=9)
    f.text(300, 292, "A 的信号尚未到达 B 时\nB 也发送（冲突）", size=13, anchor="start")

    # 冲突后信号回传
    f.arrow(470, 168, 470, by, sw=1.4, head=8)
    f.arrow(470, 168, 470, ax, sw=1.4, head=8)
    lab(f, 492, 214, "冲突发生", 14, anchor="start", color=RED)

    # 2τ 标注
    f.line(140, 350, 140 + 330, 350, sw=1.2)
    f.arrow(140, 350, 140, 340, sw=1.2, head=7)
    f.arrow(470, 350, 470, 340, sw=1.2, head=7)
    lab(f, 305, 368, "争用期 2τ（以太网取 51.2 μs，即 512 bit 时间）", 14)

    boxr(f, 560, 300, 300, 96,
         ["最小帧长 = 2τ × 数据率", "= 51.2 μs × 10 Mb/s = 512 bit = 64 B",
          "帧太短则可能在冲突信号返回前就发完"],
         size=13, fill=YELL, sw=1.3, lh=1.5)
    lab(f, 660, 60, "时间 →", 14, anchor="middle")
    return f


# ---------------------------------------------------------------- 5 交换机
def f_switch(Fig):
    f = Fig(880, 430)
    title(f, "以太网交换机自学习：记录源 MAC 与端口，未知目的地址则洪泛")
    hosts = [("主机 A\n11-11-11", 110), ("主机 B\n22-22-22", 220), ("主机 C\n33-33-33", 330)]
    for name, y in hosts:
        boxr(f, 40, y - 22, 110, 46, name.split("\n"), size=13, fill=BLUE, sw=1.3, lh=1.35)
    boxr(f, 250, 76, 120, 290, ["交", "换", "机"], size=15, fill=BOXF, sw=1.4, lh=1.6)
    for i, (name, y) in enumerate(hosts):
        f.line(150, y, 250, y, sw=1.4)
        lab(f, 200, y - 14, "端口 %d" % (i + 1), 12)
    f.line(370, 200, 470, 200, sw=1.4)
    lab(f, 420, 186, "端口 4", 12)

    # 转发表
    f.rect(470, 120, 110, 44, fill=BOXF, sw=1.3)
    lab(f, 525, 142, "MAC 地址", 13)
    f.rect(580, 120, 70, 44, fill=BOXF, sw=1.3)
    lab(f, 615, 142, "端口", 13)
    rows = [("11-11-11", "1"), ("33-33-33", "3")]
    for i, (m, p) in enumerate(rows):
        yy = 164 + i * 40
        f.rect(470, yy, 110, 40, sw=1.3, fill="#ffffff")
        lab(f, 525, yy + 20, m, 13)
        f.rect(580, yy, 70, 40, sw=1.3, fill="#ffffff")
        lab(f, 615, yy + 20, p, 13)
    lab(f, 560, 108, "交换表（MAC—端口）", 13)

    # 流程文字
    f.text(40, 396, "① A 发帧给 C：交换机记下 A→端口 1；转发表无 C，向其他端口洪泛", size=13, anchor="start")
    f.text(40, 418, "② C 回帧给 A：记下 C→端口 3；此后 A↔C 的帧只在对应端口间定向转发", size=13, anchor="start")
    return f


# ---------------------------------------------------------------- 6 IPv4 首部
def f_ipv4(Fig):
    f = Fig(900, 470)
    title(f, "IPv4 数据报首部（固定 20 B，每行 32 bit）")
    x = 110
    u = 21.0
    b4, b8, b16, b32 = 4 * u, 8 * u, 16 * u, 32 * u
    hh = 42
    ys = [80, 128, 176, 224, 272, 320, 372]

    # 位标尺
    for i, s in enumerate(["0", "8", "16", "24", "31"]):
        lab(f, x + (0, 8, 16, 24, 31)[i] * u, 66, s, 12)
    f.line(x, 74, x + b32, 74, sw=1.0)

    cells(f, x, ys[0], [b4, b4, b8, b16], hh, ["版本", "首部长度", "区分服务", "总长度"])
    cells(f, x, ys[1], [b16, 3 * u, 13 * u], hh, ["标识", "标志", "片偏移"])
    cells(f, x, ys[2], [b8, b8, b16], hh, ["生存时间 TTL", "协议", "首部检验和"])
    plain(f, x, ys[3], b32, hh, "源 IP 地址（32 位）")
    plain(f, x, ys[4], b32, hh, "目的 IP 地址（32 位）")
    boxr(f, x, ys[5], b32, hh, "可选字段（0~40 B）", 15, fill=YELL)
    boxr(f, x, ys[6], b32, hh, "数据部分（上层报文）", 15, fill=GREEN)

    # 底部说明
    f.text(30, 440, "首部长度以 4 B 为单位（最小 5，即 20 B）；标志位 DF 禁止分片、MF 表示后面还有分片", size=13, anchor="start")
    f.text(30, 462, "分片：片偏移以 8 B 为单位，除最后一片外每片数据长度必须是 8 的整数倍", size=13, anchor="start")
    return f


# ---------------------------------------------------------------- 7 子网与 CIDR
def f_subnet(Fig):
    f = Fig(900, 470)
    title(f, "子网划分（借主机位）与 CIDR 路由聚合（超网）")
    x, u = 120, 19.0
    bw = 32 * u
    hh = 46
    f.rect(x, 70, 24 * u, hh, fill=BLUE, sw=1.4)
    lab(f, x + 12 * u, 70 + hh / 2, "网络号（24 位）", 14)
    f.rect(x + 24 * u, 70, 3 * u, hh, fill=ORANGE, sw=1.4)
    lab(f, x + 25.5 * u, 92 - 10, "子网号", 11)
    lab(f, x + 25.5 * u, 92 + 12, "3 位", 11)
    f.rect(x + 27 * u, 70, 5 * u, hh, fill=GREEN, sw=1.4)
    lab(f, x + 29.5 * u, 92 - 10, "主机号", 11)
    lab(f, x + 29.5 * u, 92 + 12, "5 位", 11)
    lab(f, x, 132, "192.168.1.0/24 借 3 位作子网号 → 掩码 255.255.255.224，8 个子网 × 每子网 30 台主机",
        13, anchor="start")

    # CIDR 聚合
    blocks = ["200.1.8.0/24", "200.1.9.0/24", "200.1.10.0/24", "200.1.11.0/24"]
    for i, s in enumerate(blocks):
        boxr(f, 60 + i * 150, 210, 130, 40, s, 13, fill=YELL, sw=1.3)
        f.arrow(125 + i * 150, 252, 125 + i * 150, 300, sw=1.1, head=7)
    boxr(f, 60, 300, 580, 44, "聚合后：200.1.8.0/22（前缀 22 位，覆盖 4 个 C 类网段）", 14, fill=GREEN)
    lab(f, 350, 372, "把这 4 条路由合并成 1 条，缩小路由表", 13)

    boxr(f, 660, 200, 220, 100,
         ["最长前缀匹配", "目的 200.1.9.5 同时匹配", "/16 与 /22 → 选 /22"], size=12, fill="#f7f7f7", sw=1.3, lh=1.5)
    return f


# ---------------------------------------------------------------- 8 TCP 连接
def f_tcp_conn(Fig):
    f = Fig(900, 600)
    title(f, "TCP 三次握手与四次挥手（含 TIME-WAIT 等待 2MSL）")
    cx, sx = 250, 680
    top, bot = 70, 560
    f.line(cx, top, cx, bot, sw=1.3, dash="6,4")
    f.line(sx, top, sx, bot, sw=1.3, dash="6,4")
    lab(f, cx, top - 16, "客户", 16, bold=True)
    lab(f, sx, top - 16, "服务器", 16, bold=True)

    def msg(y, to_right, label, color=INK, dash=None):
        if to_right:
            f.arrow(cx, y, sx, y + 26, sw=1.5, dash=dash, head=9)
            f.text(cx + 12, y - 12, label, size=13, anchor="start", color=color)
        else:
            f.arrow(sx, y, cx, y + 26, sw=1.5, dash=dash, head=9)
            f.text(sx - 12, y - 12, label, size=13, anchor="end", color=color)

    lab(f, 40, 100, "三次握手", 14, anchor="start", bold=True)
    msg(100, True, "SYN=1, seq=x")
    msg(150, False, "SYN=1, ACK=1, seq=y, ack=x+1")
    msg(200, True, "ACK=1, seq=x+1, ack=y+1")
    lab(f, cx - 12, 118, "SYN-SENT", 11, anchor="end")
    lab(f, cx - 12, 230, "ESTABLISHED", 11, anchor="end")
    lab(f, sx + 12, 170, "SYN-RCVD", 11, anchor="start")
    lab(f, sx + 12, 232, "ESTABLISHED", 11, anchor="start")

    f.line(60, 262, 840, 262, sw=0.9, dash="4,4")
    lab(f, 40, 286, "数据传送", 14, anchor="start", bold=True)
    f.arrow(cx, 290, sx, 306, sw=1.5, head=8)
    f.arrow(sx, 306, cx, 322, sw=1.5, head=8)
    lab(f, (cx + sx) / 2, 340, "全双工数据传输（滑动窗口 + 累计确认）", 12)

    f.line(60, 352, 840, 352, sw=0.9, dash="4,4")
    lab(f, 40, 376, "四次挥手", 14, anchor="start", bold=True)
    msg(380, True, "FIN=1, seq=u")
    msg(420, False, "ACK=1, ack=u+1")
    msg(460, False, "FIN=1, ACK=1, seq=w, ack=u+1")
    msg(500, True, "ACK=1, ack=w+1")
    lab(f, cx - 12, 398, "FIN-WAIT-1", 11, anchor="end")
    lab(f, cx - 12, 440, "FIN-WAIT-2", 11, anchor="end")
    lab(f, cx - 12, 506, "TIME-WAIT", 11, anchor="end")
    lab(f, sx + 12, 440, "CLOSE-WAIT", 11, anchor="start")
    lab(f, sx + 12, 480, "LAST-ACK", 11, anchor="start")
    f.rect(cx - 92, 514, 84, 32, fill=YELL, sw=1.3, rx=4)
    lab(f, cx - 50, 530, "2MSL", 12)
    f.text(60, 576, "TIME-WAIT 等待 2MSL：保证最后的 ACK 能到达，并让旧连接的报文在网络中消失",
           size=13, anchor="start")
    return f


# ---------------------------------------------------------------- 9 拥塞控制
def f_congestion(Fig):
    f = Fig(900, 460)
    title(f, "TCP 拥塞窗口变化：慢开始（指数）→ 拥塞避免（线性）→ 超时后 ssthresh 减半、cwnd 归 1")
    ox, oy = 110, 390
    xw, yh = 38.0, 13.0
    f.line(ox, oy, 830, oy, sw=1.4)
    f.line(ox, oy, ox, 70, sw=1.4)
    f.arrow(830, oy, 850, oy, sw=1.4, head=8)
    f.arrow(ox, 70, ox, 50, sw=1.4, head=8)
    lab(f, 850, oy + 22, "轮次", 13, anchor="end")
    lab(f, ox - 12, 60, "cwnd", 13, anchor="end")

    ticks_x = [1, 4, 8, 12, 16, 19]
    for t in ticks_x:
        lab(f, ox + (t - 1) * xw, oy + 20, str(t), 12)
    for v in (4, 8, 12, 16, 20, 24):
        lab(f, ox - 10, oy - v * yh, str(v), 12, anchor="end")
        f.line(ox, oy - v * yh, 830, oy - v * yh, sw=0.7, dash="3,5")

    # (轮次, cwnd)
    seq = [(1, 1), (2, 2), (3, 4), (4, 8), (5, 9), (6, 10), (7, 11), (8, 12),
           (9, 1), (10, 2), (11, 4), (12, 6), (13, 7), (14, 8), (15, 9), (16, 10),
           (17, 11), (18, 12), (19, 13)]
    pts = [(ox + (t - 1) * xw, oy - c * yh) for t, c in seq]
    f.poly(pts, sw=2.0)

    # ssthresh 参考线
    for v, s in ((8, "ssthresh=8"), (6, "ssthresh=6")):
        f.line(ox, oy - v * yh, 840, oy - v * yh, sw=1.2, dash="8,5")
        f.text(818, oy - v * yh - 12, s, size=11, anchor="end")

    f.text(100, 426, "① 慢开始（指数增长）→ ② 到 ssthresh 转拥塞避免（线性增长）→ ③ 超时：ssthresh 减半、cwnd=1",
           size=13, anchor="start")
    f.text(ox + 9.6 * xw, oy - 1.2 * yh, "超时", size=12, anchor="start", color=RED)
    f.text(110, 448, "若收到三个重复 ACK（快重传），则执行快恢复：ssthresh = cwnd/2，cwnd = ssthresh 后直接进入拥塞避免",
           size=13, anchor="start")
    return f


# ---------------------------------------------------------------- 10 DNS
def f_dns(Fig):
    f = Fig(900, 470)
    title(f, "域名解析：主机→本地域名服务器用递归查询，本地→其他服务器用迭代查询")
    boxr(f, 50, 208, 118, 48, ["主机", "（客户端）"], 14, fill=BLUE)
    boxr(f, 232, 208, 160, 48, ["本地域名服务器", "（默认 DNS）"], 13, fill=GREEN)
    boxr(f, 620, 78, 160, 44, "根域名服务器", 13, fill=YELL)
    boxr(f, 620, 180, 160, 44, "com 顶级域名服务器", 12, fill=YELL)
    boxr(f, 620, 282, 160, 44, "example.com 权限服务器", 11, fill=YELL)

    def tag(x, y, s):
        f.circle(x, y, 11, fill="#ffffff", sw=1.2)
        lab(f, x, y, s, 12)

    # ① 递归查询
    f.arrow(168, 222, 230, 222, sw=2.0, head=9)
    tag(199, 204, "1")
    # ⑧ 返回结果
    f.arrow(230, 244, 170, 244, sw=2.0, head=9)
    tag(199, 262, "8")
    f.text(50, 196, "递归查询", size=12, anchor="start")

    # ②③ 本地 ↔ 根
    f.arrow(392, 216, 618, 104, sw=1.3, head=8)
    tag(492, 146, "2")
    f.arrow(618, 116, 394, 232, sw=1.3, dash="5,4", head=8)
    tag(534, 186, "3")
    # ④⑤ 本地 ↔ com
    f.arrow(392, 226, 618, 196, sw=1.3, head=8)
    tag(498, 196, "4")
    f.arrow(618, 208, 394, 236, sw=1.3, dash="5,4", head=8)
    tag(520, 226, "5")
    # ⑥⑦ 本地 ↔ 权限服务器
    f.arrow(392, 242, 618, 296, sw=1.3, head=8)
    tag(498, 282, "6")
    f.arrow(618, 308, 394, 250, sw=1.3, dash="5,4", head=8)
    tag(534, 316, "7")

    f.text(460, 130, "迭代查询", size=12, anchor="start")
    f.text(40, 356, "① 主机问本地 DNS；② 本地问根；③ 根只返回 com 服务器地址；④ 本地问 com；", size=13, anchor="start")
    f.text(40, 382, "⑤ com 返回 example.com 权限服务器地址；⑥ 本地问权限服务器；⑦ 得到 IP；⑧ 缓存后返回给主机。", size=13, anchor="start")
    f.text(40, 414, "DNS 通常使用 UDP 53 端口（区域传送用 TCP）；各级服务器与主机的缓存按 TTL 过期。", size=13, anchor="start")
    return f


# ---------------------------------------------------------------- 11 HTTP 过程
def f_http(Fig):
    f = Fig(880, 420)
    title(f, "浏览器访问一个网页的完整过程")
    boxr(f, 60, 150, 120, 50, ["浏览器"], 15, fill=BLUE)
    boxr(f, 620, 150, 150, 50, ["Web 服务器"], 15, fill=GREEN)
    boxr(f, 330, 60, 140, 44, ["DNS 服务器"], 14, fill=YELL)

    f.arrow(120, 150, 330, 96, sw=1.3, head=8)
    f.text(150, 100, "① DNS 解析域名 → IP", size=12, anchor="start")
    f.arrow(400, 104, 120, 168, sw=1.3, dash="5,4", head=8)

    f.arrow(180, 150, 620, 150, sw=1.5, head=9)
    f.text(300, 134, "② TCP 三次握手建立连接（80 端口）", size=12, anchor="start")

    f.arrow(180, 176, 620, 176, sw=1.5, head=9)
    f.text(300, 196, "③ 发送 HTTP 请求报文（GET /index.html）", size=12, anchor="start")

    f.arrow(620, 222, 180, 222, sw=1.5, head=9)
    f.text(300, 242, "④ 返回 HTTP 响应（200 OK + HTML）", size=12, anchor="start")

    f.arrow(180, 262, 620, 262, sw=1.2, dash="5,4", head=8)
    f.text(300, 282, "⑤ 浏览器解析 HTML，再请求图片/CSS/JS（复用连接）", size=12, anchor="start")

    f.arrow(620, 302, 180, 302, sw=1.2, dash="5,4", head=8)
    f.text(300, 322, "⑥ 渲染页面，按需四次挥手释放连接", size=12, anchor="start")
    f.text(60, 380, "HTTP 本身无状态，用 Cookie/Session 保持会话；持久连接可复用同一条 TCP 连接传输多个对象。",
           size=13, anchor="start")
    return f


FLOW = [
    ("封装解封装", f_encap),
    ("编码波形", f_encode),
    ("滑动窗口时空图", f_windows),
    ("CSMA-CD争用期", f_csma),
    ("交换机自学习", f_switch),
    ("IPv4首部", f_ipv4),
    ("子网划分与CIDR", f_subnet),
    ("TCP三次握手四次挥手", f_tcp_conn),
    ("TCP拥塞控制", f_congestion),
    ("DNS解析过程", f_dns),
    ("HTTP访问过程", f_http),
]
