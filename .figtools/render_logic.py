# -*- coding: utf-8 -*-
"""渲染数字逻辑插图：输出 SVG + PNG 预览。"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import figs_logic_tbl as T  # noqa: E402
import figs_logic_chip as Cc  # noqa: E402

OUT = r"D:\Note\.figwork\logic\svg"
PRE = r"D:\Note\.figwork\logic\preview"

JOBS = [
    ("逻辑代数基本运算", T.f_logic_basic),
    ("逻辑代数复合运算", T.f_logic_compound),
    ("SR锁存器", Cc.f_sr_latch),
    ("下降沿D触发器", Cc.f_dff_fall),
    ("上升沿JK触发器", Cc.f_jkff),
    ("上升沿T触发器", Cc.f_tff),
    ("译码器74LS138", Cc.f_138),
    ("数据选择器74LS151", Cc.f_151),
    ("加法器74LS283", Cc.f_283),
    ("数值比较器74LS85", Cc.f_85),
    ("移位寄存器74LS194", Cc.f_194),
    ("计数器74LS163", Cc.f_163),
    ("mealy状态图", Cc.f_mealy),
    ("Moore状态图", Cc.f_moore),
]


def main(only=None):
    for d in (OUT, PRE):
        os.makedirs(d, exist_ok=True)
    for name, fn in JOBS:
        if only and name not in only:
            continue
        f = fn()
        f.save(os.path.join(OUT, name + ".svg"))
        f.preview(os.path.join(PRE, name + ".png"))
        print("%s: %dx%d" % (name, f.w, f.h))


if __name__ == "__main__":
    main(sys.argv[1:] or None)
