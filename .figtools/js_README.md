# 计组插图 SVG 重绘规范（js_kit）

目标：把 `D:\Note\计算机基础知识\计算机组成原理\插图\*.png` 里的课本插图，用矢量 SVG 1:1 重绘，保持内容、结构、文字与原图一致，风格是教材线稿（黑线、浅灰填充、微软雅黑/黑体）。

## 一、工作流

1. 用 read 工具读原图：`D:\Note\计算机基础知识\计算机组成原理\插图\<图名>.png`。看不清细节就用 python + PIL 裁剪放大后再读（PIL 可以写 `D:\Note\.svg_work\js\crops\`）。
2. 在 `D:\Note\.figtools\figs_js<N>.py` 里写图函数（用 write/edit 工具创建；**不能用 python 直接写 .py 文件**，会被沙箱拒绝）。
3. 运行构建：`& 'C:\Users\cr051\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe' 'D:\Note\.figtools\js_kit.py' <图名> [<图名> ...]`
   - 输出到 `D:\Note\.svg_work\js\svg\<图名>.svg`、`preview\<图名>.png`；
   - 同时生成对比图 `D:\Note\.svg_work\js\cmp\<图名>_cmp.png`（**上=原图，下=你的图**）。
4. 用 read_image 看对比图，找出差异（位置、字号、箭头、框大小），改代码再构建，**至少迭代 2 轮**，直到结构、比例、文字位置与原图基本一致。
5. 全部图完成后回报清单。

## 二、版式规则

- 画布尺寸 = 原图像素尺寸（用 PIL 读原图得到 `w, h`），保证 1:1 观感。
- 字号：原图正文一般 13–18px，标题 18–22px；先量原图文字高度再定，宁可略大不要过小。
- 线条：框线 `sw=1.4~1.6`，箭头 `sw=1.4~1.6, head=9`，虚线 `dash="5,4"`。
- 颜色：正文黑 `#2b2b2b`；普通元件浅灰填充 `#ededed`；总线/寄存器可白底；重要框可用 `#dce6f3`(蓝)、`#d9e3cc`(绿)、`#fdf3cf`(黄)；强调文字可用 `#c00000`。
- 中文用全角标点，术语与原图完全一致（不要改字、不要漏标号如 ①②③）。
- 图内不要留大面积空白；元素间距均匀。

## 三、可用工具（`from js_kit import *`）

```python
import js_kit as K
from js_kit import Fig, INK, BOXF, BOXW, BLUE, GREEN, YELLOW, RED, GRAY

def f_xxx(Fig):
    f = Fig(W, H)                       # 画布 = 原图尺寸
    K.box(f, x, y, w, h, "文字", size=15)          # 浅灰填充框，可传多行 list
    K.plain(f, x, y, w, h, ["第一行", "第二行"], size=14)   # 白底框
    K.shell(f, x, y, w, h)                          # 空框
    K.dia(f, cx, cy, w, h, "判断?", size=14)         # 菱形
    K.cells(f, x, y, [w1, w2, w3], h, ["A", "B", "C"])  # 一行单元格（表格行）
    K.gridbox(f, x, y, w, h, rows, cols, head=["列1", "列2"])  # 网格
    K.adown(f, x, y1, y2)  / K.aright(f, x1, y, x2)  # 竖直/水平箭头
    K.textof(f, x, y, "文字", size=14, anchor="middle")
    K.brace(f, x, y1, y2, w=12, side=1)             # 竖直方括号
    K.dashed(f, x1, y1, x2, y2)                     # 虚线
    K.wave(f, x0, y0, width, hi, lo, [1,0,1,1])     # 数字波形（也可自己用 f.poly 画）
    # 底层还可直接用 svgkit 的图元：
    f.rect(x, y, w, h, fill="none", sw=1.4, rx=0, dash=None)
    f.line(x1, y1, x2, y2, sw=1.4, dash=None)
    f.arrow(x1, y1, x2, y2, sw=1.4, dash=None, head=9)
    f.poly([(x1,y1), (x2,y2), ...], sw=1.4, fill="none")   # 折线/多边形（不闭合需自己回到起点）
    f.text(x, y, "文字", size=14, anchor="middle", bold=False, color=None)
    f.circle(cx, cy, r, fill="none", sw=1.4)
    f.ellipse(cx, cy, rx, ry, fill="none", sw=1.4)
    return f
```

注意：`f.arrow` 的箭头尖在终点；`f.text` 的 y 是垂直中心；`fill="none"` 表示不填充（不要传 None）。

## 四、模块格式（严格）

```python
# -*- coding: utf-8 -*-
import js_kit as K
from js_kit import Fig

def f_rom(Fig):
    f = Fig(760, 320)
    ...
    return f

def f_bus(Fig):
    ...

FIGS = [("冯·诺依曼计算机结构框图", f_rom), ("单总线结构", f_bus)]
```

- 文件名固定：`figs_js1.py` … `figs_js9.py`（各批次一个，互不覆盖）。
- `FIGS` 里的名字必须与 `插图\<图名>.png` 的文件名（去掉 .png）逐字一致。

## 五、验收标准

- `js_kit.py` 构建无异常，`ET.parse` 通过（脚本已内置）。
- 对比图上：所有框、箭头、文字与原图位置对应；无文字重叠、无文字出界（超出画布）。
- 文字内容与原图一致（含上下标、编号、希腊字母、$...$ 形式可用普通字符）。
- 电路/时序图允许线条简化，但连接的部件、引脚名、时序波形必须对得上。
