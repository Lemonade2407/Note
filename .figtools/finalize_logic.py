# -*- coding: utf-8 -*-
"""落地：SVG 写入 数字逻辑\\图片\\、笔记 14 处链接改为 .svg、清理临时目录。"""

import glob
import io
import os
import shutil

NOTE = r"D:\Note\计算机基础知识\数字逻辑.md"
PIC = os.path.join(os.path.dirname(NOTE), "数字逻辑", "图片")
SRC = r"D:\Note\.figwork\svg"


def main():
    os.makedirs(PIC, exist_ok=True)
    files = sorted(glob.glob(os.path.join(SRC, "*.svg")))
    for p in files:
        shutil.copy2(p, os.path.join(PIC, os.path.basename(p)))
    print("copied:", len(files))

    with io.open(NOTE, "rb") as fh:
        text = fh.read().decode("utf-8")
    miss = []
    for p in files:
        n = os.path.splitext(os.path.basename(p))[0]
        old, new = "![[%s]]" % n, "![[%s.svg]]" % n
        if old not in text:
            miss.append(n)
        text = text.replace(old, new)
    with io.open(NOTE, "wb") as fh:
        fh.write(text.encode("utf-8"))
    print("miss:", miss)
    print("svg links:", text.count(".svg]]"), "bare:", len(glob.glob(os.path.join(PIC, "*.svg"))))

    shutil.rmtree(r"D:\Note\.figwork", ignore_errors=True)
    print("cleaned .figwork")


if __name__ == "__main__":
    main()
