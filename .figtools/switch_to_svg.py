# -*- coding: utf-8 -*-
"""把 26 张 SVG 落进笔记图片目录、改链接、删掉 .excalidraw 与临时目录。"""

import glob
import io
import os
import shutil

BASE = r"D:\Note\计算机基础知识\数据结构与算法"
PIC = os.path.join(BASE, "图片")
NOTE = os.path.join(BASE, "数据结构与算法.md")
SRC = r"D:\Note\.svg_work\svg"


def main():
    files = sorted(glob.glob(os.path.join(SRC, "*.svg")))
    for p in files:
        shutil.copy2(p, os.path.join(PIC, os.path.basename(p)))
    print("copied svg:", len(files))

    with io.open(NOTE, "rb") as fh:
        text = fh.read().decode("utf-8")
    names = [os.path.splitext(os.path.basename(p))[0] for p in files]
    miss = []
    for n in names:
        old = "![[%s.excalidraw]]" % n
        if old not in text:
            miss.append(n)
        text = text.replace(old, "![[%s.svg]]" % n)
    with io.open(NOTE, "wb") as fh:
        fh.write(text.encode("utf-8"))
    print("miss:", miss)
    print("svg links:", text.count(".svg]]"), "excalidraw links:", text.count(".excalidraw]]"))

    gone = 0
    for p in glob.glob(os.path.join(PIC, "*.excalidraw")):
        os.remove(p)
        gone += 1
    print("removed excalidraw:", gone)

    if os.path.isdir(r"D:\Note\.svg_work"):
        shutil.rmtree(r"D:\Note\.svg_work")
        print("removed .svg_work")

    print("svg in pic:", len(glob.glob(os.path.join(PIC, "*.svg"))))


if __name__ == "__main__":
    main()
