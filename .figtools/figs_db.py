# -*- coding: utf-8 -*-
"""数据库系统概论插图：重绘 3 张 + 新绘 2 张。

用法：
    python figs_db.py                # 全部重绘 + 预览 + 与原图对比
    python figs_db.py 实体间的联系    # 只跑指定图
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import js_kit as K  # noqa: E402
import svgkit  # noqa: E402
from js_kit import BOXF, BOXW, INK, SOFT  # noqa: E402

svgkit.FONT_SVG = "'Microsoft YaHei', 'SimHei', sans-serif"

PIC = r"D:\Note\计算机基础知识\数据库系统概论\图片"
WORK = r"D:\Note\.svg_work\db"
BLUE = "#dce6f3"
GREEN = "#d9e3cc"
YELLOW = "#fdf3cf"


def lbl(f, x, y, s, size=16, anchor="middle", bold=False, color=None, italic=False):
    f.text(x, y, s, size=size, anchor=anchor, bold=bold, color=color, italic=italic)


# ---------------------------------------------------------------- 实体间的联系
def f_relation(Fig):
    f = Fig(780, 400)
    plans = [(1, 1, "1:1 联系"), (1, "n", "1:n 联系"), ("m", "n", "m:n 联系")]
    for i, (up, low, cap) in enumerate(plans):
        x = 130 + i * 260
        K.box(f, x - 78, 40, 156, 46, "实体型A", size=17)
        K.box(f, x - 78, 210, 156, 46, "实体型B", size=17)
        f.line(x, 86, x, 122, sw=1.4)
        f.line(x, 172, x, 210, sw=1.4)
        K.dia(f, x, 147, 150, 50, "联系名", size=17)
        lbl(f, x + 12, 104, str(up), 16, "start", italic=True)
        lbl(f, x + 12, 196, str(low), 16, "start", italic=True)
        lbl(f, x, 320, "(%s) %s" % ("abc"[i], cap), 17)
    lbl(f, 390, 362, "图 7.6  两个实体型之间的三类联系", 16)
    return f


# ---------------------------------------------------------------- ODBC 工作流程
def f_odbc(Fig):
    f = Fig(480, 700)
    cx = 210
    K.box(f, cx - 80, 30, 160, 44, "配置数据源", size=16)
    f.rect(cx - 80, 84, 160, 40, dash="4,3", sw=1.2)
    lbl(f, cx, 104, "动态配置数据源", 14)
    K.box(f, cx - 80, 138, 160, 44, "初始化环境", size=16)
    K.box(f, cx - 80, 196, 160, 44, "建立连接", size=16)
    K.box(f, cx - 80, 254, 160, 44, "分配语句句柄", size=16)
    K.box(f, cx - 80, 312, 160, 44, "执行SQL语句", size=16)
    K.dia(f, cx, 408, 190, 76, "有无结果集", size=16)
    K.box(f, cx - 80, 470, 160, 44, "结果集处理", size=16)
    K.box(f, cx - 80, 540, 160, 44, "中止", size=16)

    K.adown(f, cx, 74, 138, sw=1.4)
    K.adown(f, cx, 182, 196, sw=1.4)
    K.adown(f, cx, 240, 254, sw=1.4)
    K.adown(f, cx, 298, 312, sw=1.4)
    K.adown(f, cx, 356, 370, sw=1.4)
    # 有 → 结果集处理
    K.adown(f, cx, 446, 470, sw=1.4)
    lbl(f, cx + 10, 462, "有", 15, "start")
    K.adown(f, cx, 514, 540, sw=1.4)
    # 无 → 中止（右侧绕行）
    f.poly([(cx + 95, 408), (cx + 150, 408), (cx + 150, 562), (cx + 82, 562)], sw=1.4, head=9)
    lbl(f, cx + 104, 392, "无", 15, "start")
    # 结果集处理 → 分配语句句柄（循环）
    f.poly([(cx - 80, 492), (40, 492), (40, 276), (cx - 80, 276)], sw=1.4, head=9)
    lbl(f, 240, 660, "图 8.5  ODBC 的工作流程", 15)
    return f


# ---------------------------------------------------------------- 查询处理步骤
def f_query_steps(Fig):
    f = Fig(640, 620)
    cx = 280
    K.box(f, cx - 70, 26, 140, 30, "查询语句", size=15)
    K.box(f, cx - 90, 76, 180, 56, ["词法分析", "语法分析"], size=16)
    K.box(f, cx - 90, 156, 180, 96, ["语义分析", "符号名转换", "安全性检查", "完整性初步检查"], size=15, lh=1.3)
    K.box(f, cx - 90, 276, 180, 34, "查询树(query tree)", size=15)
    K.box(f, cx - 90, 330, 180, 56, ["代数优化", "物理优化等"], size=16)
    K.box(f, cx - 90, 410, 180, 34, "查询执行计划", size=15)
    K.box(f, cx - 70, 486, 140, 30, "代码生成", size=15)
    K.box(f, cx - 90, 538, 180, 34, "查询计划的执行代码", size=14)

    K.adown(f, cx, 56, 76)
    K.adown(f, cx, 132, 156)
    K.adown(f, cx, 252, 276)
    K.adown(f, cx, 310, 330)
    K.adown(f, cx, 386, 410)
    K.adown(f, cx, 444, 486)
    K.adown(f, cx, 516, 538)

    # 数据库（数据字典）圆柱
    dx, dy, dw, dh = 470, 190, 130, 150
    f.rect(dx, dy + 14, dw, dh - 28, fill=SOFT, sw=1.4)
    f.ellipse(dx + dw / 2, dy + 14, dw / 2, 14, fill=SOFT, sw=1.4)
    f.ellipse(dx + dw / 2, dy + dh - 14, dw / 2, 14, fill="none", sw=1.4)
    f.line(dx, dy + 14, dx, dy + dh - 14, sw=1.4)
    f.line(dx + dw, dy + 14, dx + dw, dy + dh - 14, sw=1.4)
    lbl(f, dx + dw / 2, dy + 60, "数据库", 16)
    lbl(f, dx + dw / 2, dy + 84, "数据字典", 16)

    f.arrow(dx, 300, cx + 90, 200, sw=1.4, head=9)
    f.arrow(dx, 250, cx + 90, 358, sw=1.4, head=9)

    for y, s in ((90, "查询分析"), (204, "查询检查"), (358, "查询优化"), (503, "查询执行")):
        lbl(f, 40, y, s, 15, "start")
    lbl(f, 300, 590, "图 9.1  查询处理步骤", 15)
    return f


# ---------------------------------------------------------------- 三级模式两级映像
def f_three_schema(Fig):
    f = Fig(780, 470)
    for i, name in enumerate(["用户1", "用户2", "用户3"]):
        x = 110 + i * 120
        K.box(f, x - 44, 24, 88, 32, name, size=14, fill=SOFT)
        K.adown(f, x, 56, 82, sw=1.2)
        K.box(f, x - 48, 82, 96, 38, "外模式%d" % (i + 1), size=14, fill=BLUE)
        f.line(x, 120, x, 146, sw=1.2)
        f.line(x, 146, 350, 146, sw=1.2)
    f.line(350, 146, 350, 172, sw=1.2)
    K.box(f, 160, 172, 420, 48, "模式（逻辑模式）：全体数据的逻辑结构", size=15, fill=GREEN)
    K.adown(f, 370, 220, 300, sw=1.4)
    K.box(f, 160, 300, 420, 48, "内模式（存储模式）：物理结构与存储方式", size=15, fill=YELLOW)
    lbl(f, 600, 146, "外模式/模式映像", 14, "start")
    lbl(f, 600, 224, "逻辑独立性", 14, "start", color="#1f5fa0")
    lbl(f, 600, 292, "模式/内模式映像", 14, "start")
    lbl(f, 600, 344, "物理独立性", 14, "start", color="#1f5fa0")
    lbl(f, 390, 412, "两级映像保证了数据独立性：外模式不变则应用程序不必修改", 15)
    return f


# ---------------------------------------------------------------- 事务状态转换
def f_tx_states(Fig):
    f = Fig(720, 400)

    def ell(cx, cy, rx, ry, label):
        f.ellipse(cx, cy, rx, ry, fill=SOFT, sw=1.4)
        lbl(f, cx, cy, label, 15)

    ell(110, 110, 66, 34, "活动状态")
    ell(330, 60, 66, 32, "部分提交")
    ell(330, 190, 66, 32, "失败状态")
    ell(560, 50, 66, 32, "提交")
    ell(560, 200, 66, 32, "中止")
    f.arrow(176, 106, 262, 70, sw=1.4, head=9)
    lbl(f, 214, 74, "读/写操作", 13)
    f.arrow(120, 144, 268, 180, sw=1.4, head=9)
    lbl(f, 168, 178, "出错", 13)
    f.arrow(396, 56, 492, 52, sw=1.4, head=9)
    lbl(f, 444, 34, "最后一条语句", 13)
    f.arrow(396, 194, 492, 196, sw=1.4, head=9)
    f.arrow(330, 92, 330, 158, sw=1.4, head=9)
    f.arrow(330, 222, 330, 300, sw=1.4, head=9)
    lbl(f, 420, 284, "撤销（UNDO）", 13, "start")
    f.poly([(330, 300), (560, 300), (560, 232)], sw=1.4, head=9)
    lbl(f, 300, 350, "提交后数据永久保存；中止后回滚到事务开始前的状态", 14)
    return f


FIGS = [
    ("实体间的联系", f_relation),
    ("ODBC的工作流程", f_odbc),
    ("查询处理步骤", f_query_steps),
    ("三级模式与两级映像", f_three_schema),
    ("事务状态转换", f_tx_states),
]


def montage(name, prev_png):
    from PIL import Image
    src = os.path.join(PIC, name + ".png")
    mine = Image.open(prev_png).convert("RGB")
    if os.path.exists(src):
        orig = Image.open(src).convert("RGB")
        w = max(orig.width, mine.width)
        h = orig.height + mine.height + 30
        canvas = Image.new("RGB", (w, h), "#ffffff")
        canvas.paste(orig, ((w - orig.width) // 2, 0))
        canvas.paste(mine, ((w - mine.width) // 2, orig.height + 30))
    else:
        canvas = mine
        w, h = mine.size
    out = os.path.join(WORK, "cmp", name + "_cmp.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    canvas.save(out)
    return out


def main():
    want = sys.argv[1:]
    os.makedirs(os.path.join(WORK, "svg"), exist_ok=True)
    os.makedirs(os.path.join(WORK, "preview"), exist_ok=True)
    for name, fn in FIGS:
        if want and name not in want:
            continue
        fig = fn(K.Fig)
        p = fig.save(os.path.join(WORK, "svg", name + ".svg"))
        png = fig.preview(os.path.join(WORK, "preview", name + ".png"), bg="#ffffff")
        out = montage(name, png)
        print("%-16s %4dx%-4d %6dB  %s" % (name, fig.w, fig.h, os.path.getsize(p), out))


if __name__ == "__main__":
    main()
