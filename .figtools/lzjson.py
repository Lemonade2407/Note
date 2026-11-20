# -*- coding: utf-8 -*-
"""lz-string 的 Python 实现（只做 decompressFromBase64），用于解 Excalidraw 插件的 compressed-json。"""

_KEY_B64 = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=")


def _get_base_value(ch):
    if ch in _KEY_B64:
        return _KEY_B64.index(ch)
    return 0


def decompress_from_base64(data):
    if not data:
        return ""
    n = len(data)

    def get_next(idx):
        return _get_base_value(data[idx])

    return _decompress(n, 32, get_next)


def _decompress(length, reset_value, get_next_value):
    dictionary = {}
    enlarge_in = 4
    dict_size = 4
    num_bits = 3
    entry = ""
    result = []

    state = {"val": get_next_value(0), "pos": reset_value, "index": 1}

    def read_bits(n):
        bits = 0
        maxpower = 1 << n
        power = 1
        while power != maxpower:
            resb = state["val"] & state["pos"]
            state["pos"] >>= 1
            if state["pos"] == 0:
                state["pos"] = reset_value
                state["val"] = get_next_value(state["index"])
                state["index"] += 1
            if resb > 0:
                bits |= power
            power <<= 1
        return bits

    for i in range(3):
        dictionary[i] = chr(i)

    c = read_bits(2)
    if c == 0:
        char = chr(read_bits(8))
    elif c == 1:
        char = chr(read_bits(16))
    else:
        return ""

    dictionary[3] = char
    w = char
    result.append(char)

    while True:
        if state["index"] > length:
            return ""
        c = read_bits(num_bits)
        if c == 0:
            dictionary[dict_size] = chr(read_bits(8))
            dict_size += 1
            c = dict_size - 1
            enlarge_in -= 1
        elif c == 1:
            dictionary[dict_size] = chr(read_bits(16))
            dict_size += 1
            c = dict_size - 1
            enlarge_in -= 1
        elif c == 2:
            return "".join(result)

        if enlarge_in == 0:
            enlarge_in = 1 << num_bits
            num_bits += 1

        if c in dictionary:
            entry = dictionary[c]
        elif c == dict_size:
            entry = w + w[0]
        else:
            return None
        result.append(entry)
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        enlarge_in -= 1
        w = entry
        if enlarge_in == 0:
            enlarge_in = 1 << num_bits
            num_bits += 1
