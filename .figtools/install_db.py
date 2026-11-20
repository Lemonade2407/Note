# -*- coding: utf-8 -*-
"""安装数据库笔记的 3 张正式 SVG，并删除被替换掉的 10 张 png。"""

import os
import shutil

ROOT = r"D:\Note\计算机基础知识\数据库系统概论"
SRC = r"D:\Note\.figwork\db\svg"
IMG = os.path.join(ROOT, "图片")

SVGS = ["实体间的联系", "查询处理步骤", "ODBC的工作流程"]
PNGS = ["SQL数据类型", "参照完整性检查和违约处理", "多值依赖", "数据库设计各个阶段",
        "实体间的联系", "ESQL编程实例1", "ESQL语句实例2", "ODBC的工作流程",
        "查询处理步骤", "活锁和死锁"]


def main():
    for n in SVGS:
        shutil.copyfile(os.path.join(SRC, n + ".svg"), os.path.join(IMG, n + ".svg"))
        print("svg ok:", n)
    for n in PNGS:
        p = os.path.join(IMG, n + ".png")
        if os.path.exists(p):
            os.remove(p)
            print("png del:", n)
        else:
            print("png miss:", n)


main()
