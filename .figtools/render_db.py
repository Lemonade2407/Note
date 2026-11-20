# -*- coding: utf-8 -*-
"""渲染数据库笔记插图到 .figwork\db\{svg,preview}。"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from svgkit import Fig  # noqa: E402

OUT = r"D:\Note\.figwork\db"

JOBS = [
    ("实体间的联系", "f_er_relation"),
    ("查询处理步骤", "f_query_steps"),
    ("ODBC的工作流程", "f_odbc"),
]


def main(only=None):
    import figs_db
    for name, fn in JOBS:
        if only and name != only:
            continue
        f = getattr(figs_db, fn)(Fig)
        svg = os.path.join(OUT, "svg", name + ".svg")
        os.makedirs(os.path.dirname(svg), exist_ok=True)
        f.save(svg)
        png = os.path.join(OUT, "preview", name + ".png")
        os.makedirs(os.path.dirname(png), exist_ok=True)
        f.preview(png)
        print("%s: %dx%d" % (name, f.w, f.h))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
