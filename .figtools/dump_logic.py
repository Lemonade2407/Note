# -*- coding: utf-8 -*-
"""导出 5764bff^ 中 数字逻辑/ 目录下的全部文件（ASCII 名 + 索引）。"""

import io
import os
import subprocess

REPO = r"D:\Note"
REV = "5764bff^"
PREFIX = "数字逻辑/"
OUT = r"D:\Note\.figwork\src"


def git(*args):
    p = subprocess.run(["git"] + list(args), cwd=REPO,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.stdout


def main():
    os.makedirs(OUT, exist_ok=True)
    names = git("-c", "core.quotepath=false", "ls-tree", "-r", "--name-only", REV)
    paths = [p for p in names.decode("utf-8").splitlines() if p.startswith(PREFIX)]
    print("files:", len(paths))
    rows = []
    for i, path in enumerate(sorted(paths)):
        blob = git("show", "%s:%s" % (REV, path))
        slug = "f%02d%s" % (i, os.path.splitext(path)[1])
        with io.open(os.path.join(OUT, slug), "wb") as fh:
            fh.write(blob)
        rows.append("%s\t%d\t%s" % (slug, len(blob), path))
    with io.open(os.path.join(OUT, "_index.txt"), "w", encoding="utf-8") as fh:
        fh.write("rev %s\n" % REV + "\n".join(rows))
    print("\n".join(rows))


if __name__ == "__main__":
    main()
