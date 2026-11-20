# -*- coding: utf-8 -*-
"""把正式风格 SVG 覆盖到 数字逻辑\\图片\\，清理临时目录。"""

import glob
import os
import shutil

PIC = r"D:\Note\计算机基础知识\数字逻辑\图片"
SRC = r"D:\Note\.figwork\logic\svg"


def main():
    files = sorted(glob.glob(os.path.join(SRC, "*.svg")))
    for p in files:
        shutil.copy2(p, os.path.join(PIC, os.path.basename(p)))
    print("copied:", len(files))
    for p in files:
        print("  ", os.path.basename(p), os.path.getsize(p))
    shutil.rmtree(r"D:\Note\.figwork", ignore_errors=True)
    print("cleaned")


if __name__ == "__main__":
    main()
