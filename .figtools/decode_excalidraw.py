# -*- coding: utf-8 -*-
"""解码 Excalidraw 插件 .md 里的 compressed-json，输出场景 JSON 并统计元素类型。"""

import collections
import glob
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lzjson  # noqa: E402

SRC = r"D:\Note\.figwork\src"
OUT = r"D:\Note\.figwork\json"


def load_scene(md_text):
    m = re.search(r"```compressed-json\s*\n(.*?)\n```", md_text, re.S)
    if not m:
        return None, "no compressed-json"
    body = m.group(1)
    payload = "".join(re.findall(r"[A-Za-z0-9+/=]", body))
    text = lzjson.decompress_from_base64(payload)
    if not text:
        return None, "lz-string failed"
    return json.loads(text), "ok"


def main():
    os.makedirs(OUT, exist_ok=True)
    for p in sorted(glob.glob(os.path.join(SRC, "f*.md"))):
        with io.open(p, encoding="utf-8") as fh:
            text = fh.read()
        scene, status = load_scene(text)
        name = os.path.basename(p)[:-3]
        if scene is None:
            print(name, status)
            continue
        with io.open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8") as fh:
            fh.write(json.dumps(scene, ensure_ascii=False, indent=1))
        els = scene.get("elements", [])
        kinds = collections.Counter(e.get("type") for e in els)
        files = scene.get("files") or {}
        print("%s  elements=%d  files=%d  %s" % (name, len(els), len(files),
                                                 dict(kinds)))


if __name__ == "__main__":
    main()
