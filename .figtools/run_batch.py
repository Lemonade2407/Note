# -*- coding: utf-8 -*-
"""用法：python run_batch.py b3 [b4 ...]  —— 按批次渲染并出预览 PNG。"""

import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_all  # noqa: E402

JOBS = {
    "b0": [("跳表结构", "f_skip")],
    "b1": [("顺序表的示意图", "f_seqlist"), ("单链表结构", "f_single_list"),
           ("循环单链表示意图", "f_circ_single"), ("双向循环链表", "f_circ_double")],
    "b2": [("静态链表", "f_static_list"), ("栈", "f_stack"),
           ("函数递归调用时的活动记录", "f_activation"), ("队列的插入和删除", "f_queue")],
    "b3": [("循环队列的插入和删除", "f_circ_queue"), ("双端队列的基本操作", "f_deque"),
           ("十字链表的节点", "f_olnode")],
    "b4": [("广义表示意图", "f_glists"), ("广义表的存储表示", "f_glist_store"),
           ("满二叉树与完全二叉树", "f_bintree_kind"),
           ("二叉树的链接存储表示", "f_bintree_link")],
    "b5": [("二叉树静态链表表示", "f_bt_static"), ("线索二叉树表示", "f_threaded"),
           ("Huffman树构建过程", "f_huffman")],
    "b6": [("左单旋转", "f_rot_l"), ("右单旋转", "f_rot_r"),
           ("先左后右双旋转", "f_rot_lr"), ("先右后左双旋转", "f_rot_rl"),
           ("同构情况下的一字形旋转", "f_splay_zig"),
           ("异构形状下的之字形旋转", "f_splay_zigzag")],
    "b7": [("十字链表示例", "f_olist")],
}


def main():
    for tag in sys.argv[1:]:
        mod = importlib.import_module("figs_" + tag)
        jobs = [(name, getattr(mod, fn)) for name, fn in JOBS[tag]]
        build_all.build(jobs)


if __name__ == "__main__":
    main()
