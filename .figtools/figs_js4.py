# -*- coding: utf-8 -*-
"""计算机组成原理 第 4 批插图（js_kit 版）。

图名与 插图\\<图名>.png 逐字一致。
"""
import js_kit as K
from js_kit import Fig, INK, BOXF, BOXW, RED, GRAY

TXT = "#111111"


# ------------------------------------------------------------------ 富文本

def _w(s, size):
    w = 0.0
    for ch in s:
        w += size if ord(ch) > 127 else size * 0.56
    return w


def rt(f, x, y, parts, size=20, anchor="start", bold=False, color=TXT,
       it=False, subs=0.72):
    """富文本：parts = [(文字, 模式)]，模式 n 正常 / b 下标 / p 上标。"""
    tot = 0.0
    for s, k in parts:
        sz = size * subs if k in "bp" else size
        tot += _w(s, sz)
    if anchor == "middle":
        x -= tot / 2
    elif anchor == "end":
        x -= tot
    cx = x
    for s, k in parts:
        sz = size * subs if k in "bp" else size
        if k == "b":
            f.text(cx, y + size * 0.28, s, sz, anchor="start", bold=bold,
                   color=color, italic=it)
        elif k == "p":
            f.text(cx, y - size * 0.30, s, sz, anchor="start", bold=bold,
                   color=color, italic=it)
        else:
            f.text(cx, y, s, sz, anchor="start", bold=bold, color=color,
                   italic=it)
        cx += _w(s, sz)
    return tot


def n(s):
    return (s, "n")


def b(s):
    return (s, "b")


def p(s):
    return (s, "p")


def title(f, cx, y, s, size=21):
    f.text(cx, y, s, size=size)


def vline_up_arrow(f, x, y1, y2, sw=1.5, head=8):
    """从 y1 向上到 y2 的箭头。"""
    f.arrow(x, y1, x, y2, sw=sw, head=head)


# ------------------------------------------------------------------ 图 6.19

def f_par_adder(Fig):
    f = Fig(626, 193)
    xs = [56, 144, 235, 374, 463]
    ws = [68, 69, 68, 68, 68]
    top, h = 59, 33
    names = ["FA_n", "FA_n-1", "FA_n-2", "FA_1", "FA_0"]
    clab = ["C_n", "C_n-1", "C_n-2", "C_1", "C_0"]
    slab = ["S_n", "S_n-1", "S_n-2", "S_1", "S_0"]

    for i, x0 in enumerate(xs):
        w = ws[i]
        f.rect(x0, top, w, h, fill="#ffffff", sw=1.6)
        rt(f, x0 + w / 2, top + h / 2, [n("FA"), b(names[i][3:])],
           size=17, anchor="middle", it=True)
        # S 竖线
        f.line(x0 + 45, top, x0 + 45, 30, sw=1.5)
        rt(f, x0 + 45, 20, [n("S"), b(slab[i][2:])], size=16, anchor="middle",
           it=True)
        # 底部两个输入
        for dx in (12, 34):
            f.line(x0 + dx, top + h, x0 + dx, 139, sw=1.5)
        # 进位输出
        f.line(x0 + 56, top + h, x0 + 56, 127, sw=1.5)

    for i, x0 in enumerate(xs):
        if i == 0:
            f.line(50, 48, x0 + 23, 48, sw=1.5)
        else:
            px = xs[i - 1]
            f.line(px + 56, 127, x0 - 11, 127, sw=1.5)
            f.line(x0 - 11, 127, x0 - 11, 48, sw=1.5)
            f.line(x0 - 11, 48, x0 + 23, 48, sw=1.5)
        f.line(x0 + 23, 48, x0 + 23, top, sw=1.5)
        rt(f, x0 + 2, 38, [n("C"), b(clab[i][2:])], size=17, anchor="middle",
           it=True)

    # FA_0 的进位输入 C_-1
    f.line(463 + 56, 127, 541, 127, sw=1.5)
    rt(f, 549, 127, [n("C"), b("-1")], size=16, anchor="start", it=True)

    # 省略号
    f.text(340, 76, "…", size=22)
    title(f, 360, 162, "图 6.19　并行加法器示意图", size=21)
    return f


# ------------------------------------------------------------------ 图 6.20

def f_carry_chain(Fig):
    f = Fig(718, 164)
    xs = [84, 230.5, 377, 523.5]
    lab = ["3", "2", "1", "0"]

    for i, x0 in enumerate(xs):
        ax, ay, aw, ah = x0, 36, 24, 50
        bx, by, bw, bh = x0 + 62, 24, 26, 49
        f.rect(ax, ay, aw, ah, fill="#ffffff", sw=1.8)
        f.rect(bx, by, bw, bh, fill="#ffffff", sw=1.8)
        f.text(ax + aw / 2, ay + ah / 2, chr(38), size=20)
        f.text(bx + bw / 2, by + bh / 2, chr(38), size=20)

        # 进位输入（左）与输入小圈
        bub = x0 - 5
        f.circle(bub, 60, 4.5, fill="#ffffff", sw=1.5)
        if i == 0:
            rt(f, 46, 60, [n("C"), b("3")], size=17, anchor="middle", it=True)
            f.line(58, 60, bub - 4.5, 60, sw=1.5)
        else:
            px = xs[i - 1]
            f.line(px + 88, 37, px + 118, 37, sw=1.5)
            f.line(px + 118, 37, px + 118, 60, sw=1.5)
            f.line(px + 118, 60, bub - 4.5, 60, sw=1.5)
            rt(f, px + 113, 25, [n("C"), b(lab[i])], size=17, anchor="middle",
               it=True)
        f.line(bub + 4.5, 60, x0, 60, sw=1.5)

        # A 输出 -> B 输入
        f.line(x0 + 24, 49, x0 + 54, 49, sw=1.5)
        f.circle(x0 + 58, 49, 4, fill="#ffffff", sw=1.5)
        f.line(x0 + 62, 49, x0 + 62, 49, sw=1.5)

        # d 输入（右侧下方）
        f.line(x0 + 24, 72, x0 + 41, 72, sw=1.5)
        f.line(x0 + 41, 72, x0 + 41, 83, sw=1.5)
        f.line(x0 + 33, 84, x0 + 49, 84, sw=2.2)
        rt(f, x0 + 41, 97, [n("d"), b(lab[i])], size=17, anchor="middle",
           it=True)

        # B 的 t 输入
        f.line(x0 + 88, 60, x0 + 106, 60, sw=1.5)
        f.line(x0 + 106, 60, x0 + 106, 78, sw=1.5)
        rt(f, x0 + 106, 90, [n("t"), b(lab[i])], size=17, anchor="middle",
           it=True)

    # 最后一级的 C_-1 输出
    px = xs[-1]
    f.line(px + 88, 37, px + 118, 37, sw=1.5)
    f.line(px + 118, 37, px + 118, 60, sw=1.5)
    rt(f, px + 122, 25, [n("C"), b("-1")], size=17, anchor="start", it=True)

    title(f, 359, 140, "图 6.20　四位串行进位链", size=21)
    return f


# ------------------------------------------------------------------ 图 6.22

def f_group_carry(Fig):
    f = Fig(816, 335)
    xs = [72, 244, 417, 587]
    w, top, h = 140, 104, 82
    lines = [["第 1 组", "第 15～12 并行"],
             ["第 2 组", "第 11～8 并行"],
             ["第 3 组", "第 7～4 并行"],
             ["第 4 组", "第 3～0 并行"]]
    top_labels = [["15", "14", "13", "12"], ["11", "10", "9", "8"],
                  ["7", "6", "5", "4"], ["3", "2", "1", "0"]]

    for gi, x0 in enumerate(xs):
        f.rect(x0, top, w, h, fill="#ffffff", sw=1.6)
        f.text(x0 + w / 2, top + 32, lines[gi][0], size=21)
        f.text(x0 + w / 2, top + 63, lines[gi][1], size=21)
        for k in range(4):
            cx = x0 + 25 + 30.5 * k
            vline_up_arrow(f, cx, top, 57)
            rt(f, cx, 45, [n("C"), b(top_labels[gi][k])], size=18,
               anchor="middle", it=True)
        # 下方 d / t
        for k in range(4):
            dx = x0 + 8 + 36 * k
            tx = x0 + 25 + 36 * k
            f.line(dx, top + h, dx, 245, sw=1.5)
            f.line(tx, top + h, tx, 211, sw=1.5)
            rt(f, dx, 257, [n("d"), b(top_labels[gi][k])], size=18,
               anchor="middle", it=True)
            rt(f, tx, 225, [n("t"), b(top_labels[gi][k])], size=18,
               anchor="middle", it=True)

    # 跳跃进位：第 g+1 组的 C(最高) -> 第 g 组
    for gi in range(3):
        sxc = xs[gi + 1] + 25
        f.circle(sxc, 86, 3.2, fill=TXT, sw=1.0)
        f.line(sxc, 86, xs[gi] + 163, 86, sw=1.5)
        f.line(xs[gi] + 163, 86, xs[gi] + 163, 146, sw=1.5)
        f.arrow(xs[gi] + 163, 146, xs[gi] + w, 146, sw=1.5, head=9)

    # C_-1
    f.line(752, 88, 752, 146, sw=1.5)
    f.arrow(752, 146, xs[3] + w, 146, sw=1.5, head=9)
    rt(f, 750, 78, [n("C"), b("-1")], size=18, anchor="middle", it=True)

    title(f, 408, 302, "图 6.22　单重分组跳跃进位链框图", size=20)
    return f


# ------------------------------------------------------------------ 图 6.23

def f_group_carry2(Fig):
    f = Fig(850, 384)
    big = [(43, 344), (422, 343)]
    sx = [48, 144, 237, 331, 432, 527, 617, 710]
    sw_, sb, sh = 61, 230, 36

    for (bx, bw) in big:
        f.rect(bx, 83, bw, 49, fill="#ffffff", sw=1.6)
    f.text(43 + 172, 107, "第  一  大  组", size=22)
    f.text(422 + 171, 107, "第  二  大  组", size=22)

    tops = [[66, "31"], [150, "27"], [246, "23"], [338, "19"],
            [449, "15"], [533, "11"], [625, "7"], [717, "3"]]
    for x, s in tops:
        vline_up_arrow(f, x, 83, 40)
        rt(f, x, 28, [n("C"), b(s)], size=18, anchor="middle", it=True)

    # 组内进位分支
    taps = [(150, 132, 0), (246, 226, 1), (338, 318, 2),
            (449, 412, 3), (533, 513, 4), (625, 604, 5), (717, 696, 6)]
    for src, dst, bi in taps:
        f.circle(src, 62, 3.2, fill=TXT, sw=1.0)
        f.line(src, 62, dst, 62, sw=1.5)
        f.line(dst, 62, dst, 245, sw=1.5)
        f.arrow(dst, 245, sx[bi] + sw_, 245, sw=1.5, head=9)

    # C15 跨大组
    f.line(449, 62, 412, 62, sw=1.5)
    f.line(412, 62, 412, 245, sw=1.5)
    f.circle(412, 108, 3.2, fill=TXT, sw=1.0)
    f.arrow(412, 108, 387, 108, sw=1.5, head=9)

    # C_-1
    f.line(790, 275, 790, 107, sw=1.5)
    f.arrow(790, 107, 765, 107, sw=1.5, head=9)
    f.circle(790, 245, 3.2, fill=TXT, sw=1.0)
    f.arrow(790, 245, sx[7] + sw_, 245, sw=1.5, head=9)
    rt(f, 790, 288, [n("C"), b("-1")], size=17, anchor="middle", it=True)

    ctxt = [("30", "28"), ("26", "24"), ("22", "20"), ("18", "16"),
            ("14", "12"), ("10", "8"), ("6", "4"), ("2", "0")]
    for i, x0 in enumerate(sx):
        f.rect(x0, sb, sw_, sh, fill="#ffffff", sw=1.6)
        f.text(x0 + sw_ / 2, sb + sh / 2, str(i + 1), size=20)
        # D / T 上升箭头
        for dx in (7, 19):
            f.arrow(x0 + dx, sb, x0 + dx, 133, sw=1.5, head=8)
        rt(f, x0 - 6, 152, [n("D"), b(str(i + 1))], size=17, anchor="middle",
           it=True)
        rt(f, x0 + 30, 152, [n("T"), b(str(i + 1))], size=17, anchor="middle",
           it=True)
        # 3 根进位上升箭头
        for dx in (31, 43, 55):
            f.arrow(x0 + dx, sb, x0 + dx, 207, sw=1.5, head=8)
        rt(f, x0 + 31, 186, [n("C"), b(ctxt[i][0])], size=15, anchor="middle", it=True)
        rt(f, x0 + 55, 186, [n("C"), b(ctxt[i][1])], size=15, anchor="middle", it=True)
        # 底部 d / t
        for dx in (8, 52):
            f.arrow(x0 + dx, 300, x0 + dx, sb + sh, sw=1.5, head=8)
        f.text(x0 + 30, 285, "…", size=20)
        rt(f, x0 + 8, 313, [n("d"), b("i")], size=17, anchor="middle", it=True)
        rt(f, x0 + 52, 313, [n("t"), b("i")], size=17, anchor="middle", it=True)

    title(f, 425, 357, "图 6.23　32 位并行加法器双重分组跳跃进位链框图", size=20)
    return f


# ------------------------------------------------------------------ 公式排版


def _w2(s, size):
    w = 0.0
    for ch in s:
        w += size if ord(ch) > 127 else size * 0.56
    return w


def FX(s):
    """把 ~{AB} / ~B / x_{i+1} / 2^{-2} 这样的串解析成图元表。"""
    items, i = [], 0
    while i < len(s):
        c = s[i]
        if c == "~":
            i += 1
            if i < len(s) and s[i] == "{":
                j = s.index("}", i)
                items.append(("ov", s[i + 1:j]))
                i = j + 1
            else:
                items.append(("ov", s[i]))
                i += 1
        elif c in "_^":
            k = "b" if c == "_" else "p"
            i += 1
            if i < len(s) and s[i] == "{":
                j = s.index("}", i)
                items.append((k, s[i + 1:j]))
                i = j + 1
            else:
                items.append((k, s[i]))
                i += 1
        elif c == "{":
            j = s.index("}", i)
            items.extend(FX(s[i + 1:j]))
            i = j + 1
        else:
            j = i
            while j < len(s) and s[j] not in "~_^{":
                j += 1
            items.append(("n", s[i:j]))
            i = j
    return items


def _fw(items, size, subs=0.68):
    w = 0.0
    for k, v in items:
        w += _w2(v, size * subs if k in "bp" else size)
    return w


def fx(f, x, y, s, size=24, anchor="start", it=True, color=TXT):
    """画一段带上下标/上划线的公式，返回宽度。"""
    items = FX(s) if isinstance(s, str) else s
    w = _fw(items, size)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    cx = x
    for idx, (k, v) in enumerate(items):
        nxt = items[idx + 1][0] if idx + 1 < len(items) else None
        if k == "b":
            f.text(cx, y + size * 0.26, v, size * 0.68, anchor="start",
                   italic=it, color=color)
            cx += _w2(v, size * 0.68)
        elif k == "p":
            f.text(cx, y - size * 0.30, v, size * 0.68, anchor="start",
                   italic=it, color=color)
            cx += _w2(v, size * 0.68)
        elif k == "ov":
            iw = _w2(v, size)
            f.line(cx, y - size * 0.60, cx + iw, y - size * 0.60, sw=1.5)
            f.text(cx, y, v, size=size, anchor="start", italic=it, color=color)
            cx += iw
        else:
            f.text(cx, y, v, size=size, anchor="start", italic=it, color=color)
            cx += _w2(v, size)
        if nxt in ("b", "p") and k == "n":
            cx -= size * 0.13
    return w


def dstr(f, y, s, xc, adv=23, size=25, ul=None):
    """稀疏排布的数字串（每个字符按固定步距），ul 为需加下划线的下标列表。"""
    toks = s.split()
    n = len(toks)
    x = xc - adv * (n - 1) / 2.0
    pos = []
    for t in toks:
        f.text(x, y, t, size=size)
        pos.append(x)
        x += adv
    if ul:
        for idx in ul:
            f.line(pos[idx] - adv * 0.34, y + size * 0.40,
                   pos[idx] + adv * 0.34, y + size * 0.40, sw=1.6)
    return pos


# ------------------------------------------------------------------ 表 6.11


def f_rule2(Fig):
    f = Fig(1379, 656)
    xs = [8, 336, 589, 1356]
    ys = [72, 135, 198, 261, 324, 387, 450, 513, 576, 639]
    f.rect(8, 72, 1348, 567, fill="#ffffff", sw=1.6)
    f.rect(8, 72, 1348, 63, fill="#e8e8e8", sw=1.6)
    for y in ys[1:-1]:
        f.line(8, y, 1356, y, sw=1.4)
    for x in xs[1:-1]:
        f.line(x, 72, x, 639, sw=1.4)

    fx(f, 172, 104, "乘数判断位  y_{n-1}y_n", size=26, anchor="middle")
    fx(f, 462, 104, "标志位 C_j", size=26, anchor="middle")
    f.text(972, 104, "操　作　内　容", size=26)

    judge = ["0 0", "0 1", "1 0", "1 1", "0 0", "0 1", "1 0", "1 1"]
    cj = ["0", "0", "0", "0", "1", "1", "1", "1"]
    ops = ["z→2位,y^{*}→2位,C_j 保持“0”",
           "z+x^{*}→2位,y^{*}→2位,C_j 保持“0”",
           "z+2x^{*}→2位,y^{*}→2位,C_j 保持“0”",
           "z-x^{*}→2位,y^{*}→2位,C_j 置“1”",
           "z+x^{*}→2位,y^{*}→2位,C_j 置“0”",
           "z+2x^{*}→2位,y^{*}→2位,C_j 置“0”",
           "z-x^{*}→2位,y^{*}→2位,C_j 保持“1”",
           "z→2位,y^{*}→2位,C_j 保持“1”"]
    for i in range(8):
        yc = (ys[i + 1] + ys[i + 2]) / 2.0
        dstr(f, yc, judge[i], 172, adv=34, size=26)
        f.text(462, yc, cj[i], size=26)
        fx(f, 620, yc, ops[i], size=25)

    title(f, 690, 40, "表 6.11　原码两位乘的运算规则", size=26)
    return f


# ------------------------------------------------------------------ 表 6.18


def f_cmp2(Fig):
    f = Fig(1214, 513)
    ys = [64, 164, 206, 247, 289, 330, 371, 413, 454, 495]
    f.rect(10, 64, 1180, 431, fill="#ffffff", sw=1.6)
    f.rect(10, 64, 1180, 100, fill="#e8e8e8", sw=1.6)
    for y in ys[1:-1]:
        f.line(10, y, 1190, y, sw=1.4)
    f.line(368, 64, 368, 495, sw=1.4)

    f.text(189, 90, "判断位", size=26)
    fx(f, 189, 140, "y_{n-1}y_ny_{n+1}", size=26, anchor="middle")
    f.text(779, 100, "操　作　内　容", size=26)

    judge = ["0 0 0", "0 0 1", "0 1 0", "0 1 1", "1 0 0", "1 0 1", "1 1 0",
             "1 1 1"]
    ops = ["[z_{i+1}]_补 = 2^{-2}[z_i]_补",
           "[z_{i+1}]_补 = 2^{-2}{[z_i]_补 + [x]_补}",
           "[z_{i+1}]_补 = 2^{-2}{[z_i]_补 + [x]_补}",
           "[z_{i+1}]_补 = 2^{-2}{[z_i]_补 + 2[x]_补}",
           "[z_{i+1}]_补 = 2^{-2}{[z_i]_补 + 2[-~x]_补}",
           "[z_{i+1}]_补 = 2^{-2}{[z_i]_补 + [-~x]_补}",
           "[z_{i+1}]_补 = 2^{-2}{[z_i]_补 + [-~x]_补}",
           "[z_{i+1}]_补 = 2^{-2}[z_i]_补"]
    for i in range(8):
        yc = (ys[i + 1] + ys[i + 2]) / 2.0
        dstr(f, yc, judge[i], 189, adv=30, size=26)
        fx(f, 420, yc, ops[i], size=25)

    title(f, 607, 36, "表 6.18　补码两位乘的运算规则", size=26)
    return f


# ------------------------------------------------------------------ 图 7.19


def f_pdp8(Fig):
    f = Fig(425, 252)
    # 三条指令格式框
    rows = [(12, 40, [115, 176, 205, 234, 376], ["操作码", "间", "页", "地址码"],
             [(0, 115), (2, 176), (3, 206), (4, 222), (5, 240), (11, 376)]),
            (81, 109, [115, 174, 317, 376], ["1 1 0", "设备", "操作码"],
             [(0, 115), (2, 168), (3, 180), (8, 310), (9, 320), (11, 376)]),
            (150, 178, [115, 174, 376], ["1 1 1", "辅助操作码"],
             [(0, 115), (2, 168), (3, 180), (11, 376)])]
    for (y0, y1, dxs, labs, nums) in rows:
        f.rect(dxs[0], y0, dxs[-1] - dxs[0], y1 - y0, fill="#ffffff", sw=1.6)
        for x in dxs[1:-1]:
            f.line(x, y0, x, y1, sw=1.4)
        for k, lab in enumerate(labs):
            f.text((dxs[k] + dxs[k + 1]) / 2.0, (y0 + y1) / 2.0, lab, size=19)
        for (v, x) in nums:
            f.text(x, y1 + 17, str(v), size=17)

    f.text(10, 26, "访存类指令", size=17, anchor="start")
    f.text(10, 95, "I/O 类指令", size=17, anchor="start")
    f.text(10, 164, "寄存器类指令", size=17, anchor="start")
    title(f, 212, 228, "图 7.19　PDP-8 指令格式", size=20)
    return f


# ------------------------------------------------------------------ 图 7.3/7.4


def f_store(Fig):
    f = Fig(622, 871)

    def hdr(y):
        f.text(289, y, "存储器", size=21)
        f.text(553, y, "地址(十进制)", size=21)

    def frame(x, y, w, h):
        f.rect(x, y, w, h, fill="#ffffff", sw=1.6)

    # ---- (a) 对准边界 ----
    hdr(57)
    ys = [70, 102, 133, 165, 196, 228, 259, 291, 322, 354, 385]
    frame(71, 70, 436, 315)
    for y in ys[1:-1]:
        f.line(71, y, 507, y, sw=1.4)
    f.line(179, 133, 179, 196, sw=1.4)
    f.line(289, 133, 289, 228, sw=1.4)
    f.line(398, 133, 398, 196, sw=1.4)

    def cell(x0, x1, y0, y1, s, size=15):
        f.text((x0 + x1) / 2.0, (y0 + y1) / 2.0, s, size=size)

    cell(71, 507, 70, 102, "字(地址 0)")
    cell(71, 507, 102, 133, "字(地址 4)")
    for k, s in enumerate(["字节(地址 11)", "字节(地址 10)", "字节(地址 9)",
                           "字节(地址 8)"]):
        xs = [71, 179, 289, 398, 507]
        cell(xs[k], xs[k + 1], 133, 165, s)
    for k, s in enumerate(["字节(地址 15)", "字节(地址 14)", "字节(地址 13)",
                           "字节(地址 12)"]):
        xs = [71, 179, 289, 398, 507]
        cell(xs[k], xs[k + 1], 165, 196, s)
    cell(71, 289, 196, 228, "半字(地址 18)")
    cell(289, 507, 196, 228, "半字(地址 16)")
    cell(71, 289, 228, 259, "半字(地址 22)")
    cell(289, 507, 228, 259, "半字(地址 20)")
    cell(71, 507, 259, 291, "双字(地址 24)")
    cell(71, 507, 291, 322, "双字")
    cell(71, 507, 322, 354, "双字(地址 32)")
    cell(71, 507, 354, 385, "双字")
    for k in range(10):
        f.text(530, (ys[k] + ys[k + 1]) / 2.0, str(4 * k), size=18,
               anchor="start")
    f.text(289, 407, "(a) 对准边界", size=20)

    # ---- (b) 不对准边界 ----
    hdr(440)
    ys2 = [456, 488, 519, 551]
    frame(72, 456, 436, 95)
    for y in ys2[1:-1]:
        f.line(72, y, 508, y, sw=1.4)
    f.line(180, 488, 180, 519, sw=1.4)
    f.line(290, 456, 290, 551, sw=1.4)
    f.rect(72, 456, 218, 32, fill="#e8e8e8", sw=1.6)
    f.text(181, 472, "字(地址 2)", size=17)
    f.text(399, 472, "半字(地址 0)", size=17)
    for (a, bb, s) in [(72, 180, "字节(地址 7)"), (180, 290, "字节(地址 6)"),
                       (290, 508, "字(地址 4)")]:
        f.rect(a, 488, bb - a, 31, fill="#e8e8e8", sw=1.6)
        f.text((a + bb) / 2.0, 503, s, size=17)
    f.text(181, 535, "半字(地址 10)", size=17)
    f.text(399, 535, "半字(地址 8)", size=17)
    for k in range(3):
        f.text(530, (ys2[k] + ys2[k + 1]) / 2.0, str(4 * k), size=18,
               anchor="start")
    f.text(289, 573, "(b) 不对准边界", size=20)
    f.text(290, 617, "图 7.3　存储器中数据的存放", size=21)

    # ---- 图 7.4 ----
    f.text(160, 655, "字地址", size=20)
    f.text(385, 655, "字地址", size=20)
    for (x0, vals) in [(140, ["3", "2", "1", "0", "7", "6", "5", "4"]),
                       (363, ["0", "1", "2", "3", "4", "5", "6", "7"])]:
        f.rect(x0, 707, 167, 54, fill="#ffffff", sw=1.6)
        for x in (x0 + 42, x0 + 83, x0 + 125):
            f.line(x, 707, x, 761, sw=1.4)
        f.line(x0, 734, x0 + 167, 734, sw=1.4)
        for k, v in enumerate(vals):
            cx = x0 + 21 + 41 * (k % 4)
            cy = 720 if k < 4 else 748
            f.text(cx, cy, v, size=20)
        f.text(x0 - 12, 720, "0", size=18, anchor="end")
        f.text(x0 - 12, 748, "4", size=18, anchor="end")
    f.text(220, 790, "(a) 低字节为低地址", size=19)
    f.text(445, 790, "(b) 高字节为低地址", size=19)
    f.text(290, 820, "图 7.4　两种字节次序", size=21)
    return f


# ------------------------------------------------------------------ ALU 页


def _alu_chip(f, x, y, w, h, primed, bubble_gp):
    """画一个 74181 芯片符号。"""
    f.rect(x, y, w, h, fill="#ffffff", sw=2.0)
    f.text(x + w / 2, y + 30, "74181", size=21)
    f.text(x + w / 2, y + 74, "4 位 ALU", size=21)
    # 顶部 F0..F3
    for k in range(4):
        px = x + 48 + k * 42
        f.arrow(px, y, px, y - 32, sw=1.5, head=8)
        fx(f, px, y - 46, "F_%d" % (3 - k), size=21, anchor="middle")
    # 左侧输出
    lefts = [("C_{n+4}", 15), ("A=B", 47), ("G", 75), ("P", 102)]
    for (s, dy) in lefts:
        yy = y + dy
        f.arrow(x, yy, x - 26, yy, sw=1.5, head=8)
        if bubble_gp and s in ("G", "P"):
            f.circle(x - 6, yy, 5, fill="#ffffff", sw=1.5)
        if s == "C_{n+4}" and not bubble_gp:
            f.circle(x - 6, yy, 5, fill="#ffffff", sw=1.5)
        fx(f, x - 34, yy, s, size=21, anchor="end")
    # 右侧输入
    for k, s in enumerate(["S_3", "S_2", "S_1", "S_0", "M"]):
        yy = y + 4 + k * 25
        f.arrow(x + w + 26, yy, x + w, yy, sw=1.5, head=8)
        lab = s[:-1] + "'" if (primed and s != "M") else s
        fx(f, x + w + 32, yy, lab, size=21, anchor="start")
    # 底部输入
    bots = ["B_3", "B_2", "B_1", "B_0", "A_3", "A_2", "A_1", "A_0", "C_{-1}"]
    for k, s in enumerate(bots):
        px = x + 13 + k * 22 + (14 if k >= 4 else 0)
        f.arrow(px, y + h + 48, px, y + h, sw=1.5, head=8)
        if s == "C_{-1}" and not bubble_gp:
            f.circle(px, y + h + 7, 5, fill="#ffffff", sw=1.5)
        fx(f, px, y + h + 40, s, size=21, anchor="middle")


def f_alu_page(Fig):
    f = Fig(1198, 1258)
    fx(f, 75, 34, "图 6.16 所示是 ALU 框图。图中 A_i 和 B_i 为输入变量；k_i 为控制信号，"
                  "k_i 的不同取值可决定", size=25, it=False)
    fx(f, 75, 80, "该电路做哪一种算术运算或哪一种逻辑运算；F_i 是输出函数。", size=25,
       it=False)
    fx(f, 75, 121, "现在 ALU 电路已制成集成电路芯片，例如，74181 是能完成 4 位二进制代码"
                   "的算术逻辑运", size=25, it=False)
    fx(f, 75, 163, "件，外特性如图 6.17 所示。", size=25, it=False)

    # 图 6.16 ALU 梯形
    f.poly([(44, 360), (112, 360), (137, 394), (162, 360), (240, 360),
            (200, 445), (95, 445), (44, 360)], sw=2.0)
    f.text(148, 412, "ALU", size=24)
    f.arrow(80, 322, 80, 358, sw=1.5, head=8)
    fx(f, 80, 306, "A_i", size=22, anchor="middle")
    f.arrow(190, 322, 190, 358, sw=1.5, head=8)
    fx(f, 190, 306, "B_i", size=22, anchor="middle")
    f.arrow(148, 445, 148, 452, sw=1.5, head=8)
    fx(f, 148, 464, "F_i", size=22, anchor="middle")
    f.arrow(232, 377, 205, 377, sw=1.5, head=8)
    f.arrow(232, 422, 205, 422, sw=1.5, head=8)
    for k in range(3):
        f.circle(252, 392 + k * 8, 1.6, fill=TXT, sw=1.0)
    fx(f, 272, 400, "k_i", size=22, anchor="middle")
    f.text(152, 488, "图 6.16　ALU 框图", size=21)

    _alu_chip(f, 428, 268, 223, 114, primed=True, bubble_gp=False)
    _alu_chip(f, 842, 268, 223, 114, primed=False, bubble_gp=True)
    f.text(555, 478, "(a) 正逻辑", size=21)
    f.text(985, 478, "(b) 负逻辑", size=21)
    f.text(640, 527, "图 6.17　74181 外特性示意图", size=21)

    fx(f, 75, 596, "74181 有两种工作方式，即正逻辑和负逻辑，分别如图 6.17(a) 和图 6.17(b)"
                   " 所示。表 6.32", size=25, it=False)
    fx(f, 75, 637, "列出了其算术/逻辑运算功能，逻辑电路参见附录 6C 的图 6.30。", size=25,
       it=False)
    f.text(600, 690, "表 6.32　74181 ALU 的算术/逻辑运算功能表", size=24)

    # ---- 表 6.32 ----
    cols = [27, 262, 448, 681, 869, 1180]
    f.rect(27, 715, 1153, 486, fill="#ffffff", sw=1.6)
    f.rect(27, 715, 1153, 189, fill="#e8e8e8", sw=1.6)
    f.line(27, 762, 1180, 762, sw=1.4)
    f.line(27, 810, 1180, 810, sw=1.4)
    for x in cols[1:-1]:
        f.line(x, 762, x, 904, sw=1.4)
    f.line(448, 810, 448, 904, sw=1.4)
    f.line(869, 810, 869, 904, sw=1.4)
    for y in (946, 988, 1031, 1074, 1116, 1158):
        f.line(27, y, 1180, y, sw=1.4)

    f.text(600, 740, "功　能", size=24)
    f.text(471, 786, "负逻辑输入或输出", size=23)
    f.text(930, 786, "正逻辑输入或输出", size=23)
    f.text(144, 813, "工作方式选择", size=22)
    fx(f, 144, 872, "输入 S_3S_2S_1S_0", size=22, anchor="middle")
    f.text(355, 840, "逻辑运算", size=22)
    fx(f, 355, 878, "(M=1)", size=22, anchor="middle")
    f.text(565, 840, "算术运算", size=22)
    fx(f, 565, 878, "(M=0)(C_{-1}=0)", size=22, anchor="middle")
    f.text(777, 840, "逻辑运算", size=22)
    fx(f, 777, 878, "(M=1)", size=22, anchor="middle")
    f.text(1025, 840, "算术运算", size=22)
    fx(f, 1025, 878, "(M=0)(C_{-1}=1)", size=22, anchor="middle")

    rows = [
        ("0000", ["~A", "A 减 1", "~A", "A"]),
        ("0001", ["~{AB}", "~{AB} 减 1", "~{A+B}", "A+B"]),
        ("0010", ["~A+B", "A~B 减 1", "~AB", "A+~B"]),
        ("0011", ["逻辑 1", "减 1", "逻辑 0", "减 1"]),
        ("0100", ["~{A+B}", "A 加 (A+~B)", "~{AB}", "A 加 AB"]),
        ("0101", ["~B", "AB 加 (A+~B)", "~B", "(A+~B) 加 AB"]),
        ("0110", ["A⊕B", "A 减 B 减 1", "A⊕B", "A 减 B 减 1"]),
    ]
    ys = [904, 946, 988, 1031, 1074, 1116, 1158, 1201]
    for i, (bits, cells) in enumerate(rows):
        yc = (ys[i] + ys[i + 1]) / 2.0
        dstr(f, yc, " ".join(bits), 144, adv=26, size=25)
        for k, s in enumerate(cells):
            fx(f, [355, 565, 777, 1025][k], yc, s, size=23, anchor="middle")
    f.rect(0, 1254, 1198, 4, fill="#1a1a1a", sw=0)
    return f


def f_alu_cont(Fig):
    f = Fig(1193, 606)
    f.text(1150, 48, "续表", size=22, anchor="end")
    cols = [28, 276, 460, 693, 922, 1165]
    f.rect(28, 25, 1137, 548, fill="#ffffff", sw=1.6)
    f.rect(28, 25, 1137, 185, fill="#e8e8e8", sw=1.6)
    f.line(28, 72, 1165, 72, sw=1.4)
    f.line(28, 118, 1165, 118, sw=1.4)
    for x in cols[1:-1]:
        f.line(x, 72, x, 210, sw=1.4)
    for y in (250, 290, 331, 371, 411, 451, 492, 532):
        f.line(28, y, 1165, y, sw=1.4)

    f.text(597, 48, "功　能", size=24)
    f.text(368, 96, "负逻辑输入或输出", size=23)
    f.text(929, 96, "正逻辑输入或输出", size=23)
    f.text(152, 120, "工作方式选择", size=22)
    fx(f, 152, 162, "输入 S_3S_2S_1S_0", size=22, anchor="middle")
    f.text(368, 132, "逻辑运算", size=22)
    fx(f, 368, 180, "(M=1)", size=22, anchor="middle")
    f.text(577, 132, "算术运算", size=22)
    fx(f, 577, 180, "(M=0)(C_{-1}=0)", size=22, anchor="middle")
    f.text(807, 132, "逻辑运算", size=22)
    fx(f, 807, 180, "(M=1)", size=22, anchor="middle")
    f.text(1043, 132, "算术运算", size=22)
    fx(f, 1043, 180, "(M=0)(C_{-1}=1)", size=22, anchor="middle")

    rows = [
        ("0111", ["A+~B", "A+~B", "~{AB}", "AB 减 1"]),
        ("1000", ["~{AB}", "A 加 (A+B)", "~{A+B}", "A 加 AB"]),
        ("1001", ["A⊕B", "A 加 B", "~{A⊕B}", "A 加 B"]),
        ("1010", ["B", "~{AB} 加 (A+B)", "B", "(A+~B) 加 AB"]),
        ("1011", ["A+B", "A+B", "AB", "AB 减 1"]),
        ("1100", ["逻辑 0", "A 加 A^{*}", "逻辑 1", "A 加 A^{*}"]),
        ("1101", ["~{AB}", "AB 加 A", "A+~B", "(A+B) 加 A"]),
        ("1110", ["AB", "~{AB} 加 A", "A+B", "(A+~B) 加 A"]),
        ("1111", ["A", "A", "A", "A 减 1"]),
    ]
    ys = [210, 250, 290, 331, 371, 411, 451, 492, 532, 573]
    for i, (bits, cells) in enumerate(rows):
        yc = (ys[i] + ys[i + 1]) / 2.0
        dstr(f, yc, " ".join(bits), 152, adv=26, size=25)
        for k, s in enumerate(cells):
            fx(f, [368, 577, 807, 1043][k], yc, s, size=23, anchor="middle")

    f.text(40, 592, "① 1=高电平 0=低电平; ② * 表示每一位均移到下一个更高位, 即 A* = 2A",
           size=21, anchor="start")
    return f


# ------------------------------------------------------------------ 例 6.17


def f_ex1(Fig):
    f = Fig(1367, 1420)
    fx(f, 520, 4, "z_n=2^{-1}(y_1·x^{*}+z_{n-1})", size=25)
    fx(f, 75, 45, "例 6.17　已知 x=-0.1110，y=-0.1101，求[x·y]_原。", size=26,
       it=False)
    fx(f, 75, 92, "解：因为　　x=-0.1110", size=26, it=False)
    fx(f, 75, 133, "所以 [x]_原=1.1110，x^{*}=0.1110(为绝对值)，x_0=1", size=26,
       it=False)
    fx(f, 75, 178, "又因为　　　　y=-0.1101", size=26, it=False)
    fx(f, 75, 218, "所以 [y]_原=1.1101，y^{*}=0.1101(为绝对值)，y_0=1", size=26,
       it=False)
    fx(f, 75, 262, "按原码一位乘运算规则，[x·y]_原 的数值部分计算如表 6.9 所示。",
       size=26, it=False)

    f.rect(0, 530, 1367, 20, fill="#1a1a1a", sw=0)
    f.text(85, 638, "246", size=22, anchor="start")
    f.text(760, 638, "第 3 篇　中央处理器", size=22, anchor="middle")
    f.line(55, 666, 1310, 666, sw=1.6)
    f.text(683, 716, "表 6.9　例 6.17 数值部分的计算", size=24)

    # 表格
    xs = [40, 310, 530, 1330]
    top, hb, bot = 741, 795, 1382
    f.rect(40, top, 1290, bot - top, fill="#ffffff", sw=1.6)
    f.rect(40, top, 1290, hb - top, fill="#e8e8e8", sw=1.6)
    for x in xs[1:-1]:
        f.line(x, top, x, bot, sw=1.4)
    for y in (889, 1022, 1156, 1289):
        f.line(40, y, 1330, y, sw=1.8)

    f.text(175, 768, "部　分　积", size=24)
    f.text(420, 768, "乘　　数", size=24)
    f.text(930, 768, "说　　明", size=24)

    rows = [
        ("0.0000", "1101", [3], "开始部分积 z_0=0"),
        ("+ 0.1110", "", None, "乘数为 1,加上 x^{*}"),
        ("0.1110", "", None, ""),
        ("0.0111", "0110", [3], "→1 位得 z_1,乘数同时→1 位"),
        ("+ 0.0000", "", None, "乘数为 0,加上 0"),
        ("0.0111", "0", [0], ""),
        ("0.0011", "1011", [3], "→1 位得 z_2,乘数同时→1 位"),
        ("+ 0.1110", "", None, "乘数为 1,加上 x^{*}"),
        ("1.0001", "10", None, ""),
        ("0.1000", "1101", [3], "→1 位得 z_3,乘数同时→1 位"),
        ("+ 0.1110", "", None, "乘数为 1,加上 x^{*}"),
        ("1.0110", "110", None, ""),
        ("0.1011", "0110", None, "→1 位得 z_4,乘数已全部移出"),
    ]
    ys = [818, 863, 908, 953, 998, 1043, 1088, 1133, 1178, 1223, 1268, 1313,
          1358]
    for i, (pp, mul, ul, note) in enumerate(rows):
        y = ys[i]
        s = pp
        if s.startswith("+"):
            f.text(105, y, "+", size=25)
            s = s[2:]
        dstr(f, y, " ".join(s), 202, adv=23, size=25)
        if mul:
            dstr(f, y, " ".join(mul), 420, adv=23, size=25, ul=ul)
        if note:
            fx(f, 560, y, note, size=23)
    return f


# ------------------------------------------------------------------ 例 6.18


def f_ex2(Fig):
    f = Fig(1387, 1028)
    fx(f, 75, 40, "例 6.18　设 x=0.111111，y=-0.111001，用原码两位乘求[x·y]_原。",
       size=26, it=False)
    fx(f, 75, 88, "解：① 数值部分的计算如表 6.12 所示，其中", size=26, it=False)
    fx(f, 290, 135, "x^{*}=0.111111，[-x^{*}]_补=1.000001，2x^{*}=1.111110，"
                    "y^{*}=0.111001", size=26)
    f.text(690, 190, "表 6.12　例 6.18 原码两位乘数值部分的运算过程", size=24)

    xs = [52, 369, 582, 687, 1315]
    top, hb, bot = 213, 267, 861
    f.rect(52, top, 1263, bot - top, fill="#ffffff", sw=1.6)
    f.rect(52, top, 1263, hb - top, fill="#e8e8e8", sw=1.6)
    for x in xs[1:-1]:
        f.line(x, top, x, bot, sw=1.4)
    for y in (387, 527, 668, 808):
        f.line(52, y, 1315, y, sw=1.8)
    f.text(210, 242, "部　分　积", size=24)
    fx(f, 475, 242, "乘数 y^{*}", size=24, anchor="middle")
    fx(f, 634, 242, "C_j", size=24, anchor="middle")
    f.text(1000, 242, "说　　明", size=24)

    rows = [
        (300, "000.000000", "00111001", [7], "0", "开始,部分积为 0,C_j=0"),
        (348, "+000.111111", "", None, "", "根据 y_{n-1}y_nC_j=010,加 x^{*},保持 C_j=0"),
        (412, "000.111111", "11001110", [6], "0", "→2 位,得新的部分积,乘数同时→2 位"),
        (452, "000.001111", "", None, "", "根据“100”加 2 x^{*},保持 C_j=0"),
        (497, "+001.111110", "", None, "", ""),
        (553, "010.001101", "11", None, "", "→2 位,得新的部分积,乘数同时→2 位"),
        (592, "000.100011", "01110011", [6], "0", "根据“110”减 x^{*}(即加[-x^{*}]_补),C_j 置“1”"),
        (637, "+111.000001", "", None, "", ""),
        (693, "111.100100", "0111", None, "", "→2 位,得新的部分积,乘数同时→2 位"),
        (732, "111.111001", "00011100", [6], "1", "根据“001”加 x^{*},C_j 置“0”"),
        (777, "+000.111111", "", None, "", ""),
        (833, "000.111000", "000111", None, "", "形成最终结果"),
    ]
    for (y, pp, mul, ul, cj, note) in rows:
        s = pp
        if s.startswith("+"):
            f.text(85, y, "+", size=25)
            s = s[1:]
        dstr(f, y, " ".join(s), 236, adv=24, size=25)
        if mul:
            dstr(f, y, " ".join(mul), 475, adv=24, size=25, ul=ul)
        if cj:
            f.text(634, y, cj, size=25)
            f.line(622, y + 13, 646, y + 13, sw=1.6)
        if note:
            fx(f, 700, y, note, size=22)

    fx(f, 75, 905, "② 乘积符号的确定：", size=24, it=False)
    fx(f, 690, 955, "x_0⊕y_0=0⊕1=1", size=25, anchor="middle")
    fx(f, 75, 1005, "故", size=25, it=False)
    fx(f, 190, 1005, "[x·y]_原=1.111000000111", size=25)
    return f


FIGS = [
    ("并行加法器", f_par_adder),
    ("串行进位链", f_carry_chain),
    ("单重分组跳跃进位", f_group_carry),
    ("双重分组跳跃进位", f_group_carry2),
    ("原码两位乘规则", f_rule2),
    ("补码两位乘运算规则", f_cmp2),
    ("PDP-8", f_pdp8),
    ("数据的存放方式", f_store),
    ("ALU电路", f_alu_page),
    ("ALU电路续表", f_alu_cont),
    ("原码一位乘例题", f_ex1),
    ("原码两位乘例题", f_ex2),
]
