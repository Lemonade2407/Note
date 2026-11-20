# 软件工程导论插图 SVG 重绘规范（se_kit）

目标：把 `D:\Note\计算机基础知识\软件工程导论\图片\*.png|*.jpg` 里的配图，用矢量 SVG 1:1 重绘，内容、结构、文字与原图一致；风格是课程笔记线稿（黑线、浅灰填充、微软雅黑/黑体）。

## 一、工作流

1. 用 read_image 读原图：`D:\Note\计算机基础知识\软件工程导论\图片\<图名>.png`（少数是 .jpg，构建脚本会自动找）。
2. 在 `D:\Note\.figtools\figs_se<N>.py` 写图函数（用 write/edit 工具；**python 直接写 .py 会被沙箱拒绝**）。
3. 构建：`& 'C:\Users\cr051\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe' 'D:\Note\.figtools\se_kit.py' <图名> ...`
4. read_image 看 `D:\Note\.svg_work\se\cmp\<图名>_cmp.png`（**上=原图，下=重绘**），改代码重建，**至少迭代 2 轮**。

## 二、版式规则

- 画布尺寸取原图像素尺寸（`python -c "from PIL import Image; print(Image.open(r'...').size)"`），保证比例一致；原图特别大（>1400px）时可等比缩到 1200 宽。
- 字号：原图正文 13–17px；标题 18–22px；表格内文字 12–14px。
- 线：框线 sw=1.4，箭头 sw=1.4/head=9，虚线 dash="5,4"。
- 颜色：正文 `#2b2b2b`；普通填充 `#ededed`；强调/高亮可用 `#dce6f3`(蓝)、`#d9e3cc`(绿)、`#fdf3cf`(黄)、`#f2d7d3`(粉)、`#c00000`(红字)。
- 文字必须与原图逐字一致（含标题、编号、英文术语、括号），不要自创、不要漏项；中文用全角标点。

## 三、可用工具

```python
import se_kit as K
from se_kit import Fig, INK, BOXF, BOXW, BLUE, GREEN, YELLOW, PINK, RED, GRAY

def f_xxx(Fig):
    f = Fig(W, H)
    K.box(f, x, y, w, h, "文字", size=15)                  # 浅灰框
    K.plain(f, x, y, w, h, ["行1", "行2"], size=14)         # 白框
    K.shell(f, x, y, w, h)                                  # 空框
    K.dia(f, cx, cy, w, h, "条件?", size=14)                # 菱形
    K.cells(f, x, y, [w1, w2, w3], h, ["列1", "列2", "列3"]) # 一行单元格
    K.gridbox(f, x, y, w, h, rows, cols, head=["表头…"])     # 网格
    K.adown(f, x, y1, y2) / K.aright(f, x1, y, x2)          # 箭头
    K.textof(f, x, y, "文字", size=14, anchor="start")
    K.brace(f, x, y1, y2), K.dashed(f, x1, y1, x2, y2), K.wave(...)
    # 底层 svgkit 图元
    f.rect(x, y, w, h, fill="none", sw=1.4, rx=0, dash=None)
    f.line(x1, y1, x2, y2, sw=1.4, dash=None)
    f.arrow(x1, y1, x2, y2, sw=1.4, dash=None, head=9)
    f.poly([(x1, y1), (x2, y2), ...], sw=1.4, fill="none")   # 折线/多边形
    f.text(x, y, "文字", size=14, anchor="middle", bold=False, color=None)
    f.circle(cx, cy, r, fill="none", sw=1.4)
    f.ellipse(cx, cy, rx, ry, fill="none", sw=1.4)
    return f
```

注意：`f.arrow` 箭头尖在终点；`f.text` 的 y 是文字垂直中心；`fill="none"` 表示不填充（不要传 None）。

## 四、模块格式（严格）

```python
# -*- coding: utf-8 -*-
import se_kit as K
from se_kit import Fig

def f_a(Fig):
    f = Fig(800, 500)
    ...
    return f

FIGS = [("瀑布模型", f_a)]
```

- 文件名固定 `figs_se1.py` … `figs_se9.py`；`FIGS` 里的图名必须与 `图片\<图名>.png|jpg` 的文件名（去掉扩展名）逐字一致。

## 五、验收标准

- 构建无异常、`ET.parse` 通过（脚本已内置）。
- 对比图上所有框、箭头、文字、泳道、表头位置与原图对应；无文字重叠、无出界。
- 图形语义正确：UML 图（用例/类/顺序/活动/状态）的符号规范，判定表/判定树的行列完整，模型图（瀑布/螺旋/增量/V/原型）的阶段与箭头方向正确。
