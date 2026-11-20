# -*- coding: utf-8 -*-
"""第 0 批：跳表结构（复用 demo_fix 里已校验的函数）。"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from demo_fix import fig_skip_list  # noqa: F401,E402


def f_skip(C=__import__("svgkit").Fig):
    return fig_skip_list(C)
