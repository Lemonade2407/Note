# -*- coding: utf-8 -*-
"""把笔记里的 ![[x.png]] 引用换成 ![[x.svg]]，并修正指定坏引用。

用法：python swap_refs.py <笔记.md> <旧后缀> <新后缀> [坏名映射...]
坏名映射格式：OLD=NEW（不含扩展名）
"""

import re
import sys

IMG = re.compile(r"!\[\[([^\]|]+?)(\.[A-Za-z]+)(\|[^\]]*)?\]\]")


def main():
    path, old_ext, new_ext = sys.argv[1], sys.argv[2], sys.argv[3]
    fix = {}
    for kv in sys.argv[4:]:
        k, v = kv.split("=", 1)
        fix[k] = v

    raw = open(path, "rb").read()
    text = raw.decode("utf-8")
    changed = []

    def repl(m):
        name, ext, alias = m.group(1), m.group(2), m.group(3) or ""
        if ext.lower() != old_ext.lower():
            return m.group(0)
        base = name.split("/")[-1]
        if base in fix:
            base = fix[base]
        changed.append(base + new_ext)
        return "![[%s%s%s]]" % (base, new_ext, alias)

    out = IMG.sub(repl, text)
    open(path, "wb").write(out.encode("utf-8"))
    print("替换 %d 处 → %s" % (len(changed), new_ext))
    if changed:
        print("示例：" + "，".join(changed[:5]))


if __name__ == "__main__":
    main()
