# -*- coding: utf-8 -*-
"""笔记体检：标题层级、表格列数、图片引用、编码与换行。

用法：python check_md.py <笔记.md> [<笔记.md> ...]
"""

import os
import re
import sys

IMG = re.compile(r"!\[\[([^\]|]+?)(?:\|[^\]]*)?\]\]")


def check(path):
    raw = open(path, "rb").read()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    crlf = raw.count(b"\r\n")
    lines = text.split("\n")
    tail_nl = text.endswith("\n")
    problems = []

    # 标题层级
    heads = []
    for i, s in enumerate(lines, 1):
        m = re.match(r"^(#{1,6}) (.*)$", s)
        if m:
            heads.append((i, len(m.group(1)), m.group(2)))
    prev = 0
    for ln, lv, title in heads:
        if prev and lv > prev + 1:
            problems.append("L%d 标题层级跳跃：%s → %s" % (ln, "#" * prev, "#" * lv))
        prev = lv
    counts = {}
    for _, lv, _ in heads:
        counts[lv] = counts.get(lv, 0) + 1

    # 表格列数（连续以 | 开头的行视为一张表）
    blocks, cur = [], []
    for i, s in enumerate(lines, 1):
        if s.lstrip().startswith("|"):
            cur.append((i, s))
        elif cur:
            blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)
    table_rows = 0
    for b in blocks:
        cols = [len(r.strip().strip("|").replace("\\|", "").split("|")) for _, r in b]
        table_rows += len(b)
        if len(set(cols)) > 1:
            problems.append("表格列数不一致（L%d 起）：%s" % (b[0][0], cols))

    # 图片引用
    refs = []
    for i, s in enumerate(lines, 1):
        for m in IMG.finditer(s):
            refs.append((i, m.group(1).strip()))
    missing = []
    d = os.path.dirname(path)
    for ln, r in refs:
        cands = [os.path.join(d, r), os.path.join(d, "图片", r), os.path.join(d, "插图", r),
                 os.path.join(d, os.path.basename(r))]
        if not any(os.path.exists(c) for c in cands):
            missing.append("L%d %s" % (ln, r))

    # 连续空行（忽略文件末尾的换行）
    blank_run = 0
    max_blank = 0
    for s in text.rstrip("\n").split("\n"):
        if s.strip() == "":
            blank_run += 1
            max_blank = max(max_blank, blank_run)
        else:
            blank_run = 0

    print("=" * 70)
    print(path)
    print("  行数 %d | 字节 %d | BOM %s | CRLF %d | 末尾换行 %s"
          % (len(lines), len(raw), "有" if bom else "无", crlf, tail_nl))
    print("  标题 " + " ".join("H%d=%d" % (k, v) for k, v in sorted(counts.items())))
    print("  表格 %d 张 / %d 行 | 图片引用 %d 处" % (len(blocks), table_rows, len(refs)))
    if max_blank > 1:
        print("  ! 存在连续空行（最多 %d 行）" % max_blank)
    for p in problems:
        print("  ! " + p)
    for m in missing:
        print("  ! 图片缺失 " + m)
    if not problems and not missing:
        print("  检查通过")
    return not problems and not missing


if __name__ == "__main__":
    ok = True
    for p in sys.argv[1:]:
        ok = check(p) and ok
    sys.exit(0 if ok else 1)
