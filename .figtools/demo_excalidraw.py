# -*- coding: utf-8 -*-
"""生成 Excalidraw 版样张（单链表、跳表），并渲染 PNG 自检。"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exrender  # noqa: E402
from demo_fix import fig_skip_list, fig_single_list  # noqa: E402
from exkit import Exc  # noqa: E402

DEMO = r"D:\Note\_excalidraw_demo"
PREV = os.path.join(DEMO, "preview")


def main():
    os.makedirs(PREV, exist_ok=True)
    jobs = [("示例-单链表", fig_single_list), ("示例-跳表", fig_skip_list)]
    for name, fn in jobs:
        e = fn(Exc)
        p1 = e.save(os.path.join(DEMO, name + ".excalidraw"))
        p2 = e.save_md(os.path.join(DEMO, name + ".excalidraw.md"), name)
        with open(p1, encoding="utf-8") as fh:
            scene = json.load(fh)
        kinds = {}
        for el in scene["elements"]:
            kinds[el["type"]] = kinds.get(el["type"], 0) + 1
        png, w, h = exrender.render(p1, os.path.join(PREV, name + ".png"), scale=1.6)
        print(
            f"{name}: 元素 {len(scene['elements'])} {kinds}  "
            f"excalidraw={os.path.getsize(p1)}B  md={os.path.getsize(p2)}B  png={w}x{h}"
        )


if __name__ == "__main__":
    main()
