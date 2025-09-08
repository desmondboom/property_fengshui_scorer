#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import math
import sys
from collections import Counter, defaultdict

EAST_GOOD = {"N", "E", "SE", "S"}
WEST_GOOD = {"NW", "NE", "W", "SW"}
ALL_DIR8 = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

# 朝向 -> 宅卦（用于标注；本版评分仅用“东/西四宅”的吉凶集合）
FACING_TO_GUA = {
    "S": "坎",  # 坐北朝南
    "N": "离",  # 坐南朝北
    "W": "震",  # 坐东朝西
    "NW": "巽",  # 坐东南朝西北
    "SE": "乾",  # 坐西北朝东南
    "E": "兑",  # 坐西朝东
    "NE": "艮",  # 坐东北朝西南
    "SW": "坤",  # 坐西南朝东北
}

EAST_HOUSES = {"坎", "离", "震", "巽"}

# 房间类别映射（可按需增改）
LABEL_BUCKET = {
    "main_door": {"entry", "porch"},
    "kitchen": {"kitchen", "pantry"},
    "wet": {"bath", "wc", "ensuite", "laundry"},
    "master": {"master_bedroom"},
    "bed": {"bedroom", "bedroom_1", "bedroom_2", "bedroom_3", "bedroom_4", "bedroom_5"},
    "garage": {"garage", "store", "wir", "robe"},
}


def load_layout(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "house_facing" not in data:
        raise ValueError("layout.json 需包含 house_facing (N/NE/E/SE/S/SW/W/NW)")
    if data["house_facing"] not in ALL_DIR8:
        raise ValueError("house_facing 取值应为: " + ",".join(ALL_DIR8))
    return data


def house_group_and_gua(facing: str):
    gua = FACING_TO_GUA.get(facing, None)
    group = "east" if (gua in EAST_HOUSES) else "west"
    good = EAST_GOOD if group == "east" else WEST_GOOD
    bad = set(ALL_DIR8) - good
    return group, gua, good, bad


def pick_rooms(data: dict, bucket: set):
    out = []
    for r in data["rooms"]:
        lbl = r.get("norm_label", "").lower()
        if lbl in bucket:
            out.append(r)
    return out


def pick_first(data: dict, labels: set):
    arr = pick_rooms(data, labels)
    return arr[0] if arr else None


def in_set(palace: str, s: set):
    return palace in s


def score_layout(data: dict) -> dict:
    facing = data["house_facing"]
    group, gua, good, bad = house_group_and_gua(facing)
    house_gua_label = (
        f"{gua}宅({'东四宅' if group=='east' else '西四宅'})" if gua else ("未知宅卦")
    )

    breakdown = {}

    # 1) 大门
    door = pick_first(data, LABEL_BUCKET["main_door"])
    s = 0
    why = "未检测到大门"
    if door:
        p = door["palace9"]
        if in_set(p, good):
            s, why = 20, f"大门在{p}(吉位)"
        elif p == "C":
            s, why = -10, "大门在中宫不宜"
        else:
            s, why = -15, f"大门在{p}(凶位)"
    breakdown["main_door"] = {"score": s, "why": why}

    # 2) 主卧
    master = pick_first(data, LABEL_BUCKET["master"])
    s = 0
    why = "未检测到主卧"
    if master:
        p = master["palace9"]
        if in_set(p, good):
            s, why = 12, f"主卧在{p}(吉位)"
        elif p == "C":
            s, why = -10, "主卧在中宫不宜"
        else:
            s, why = -12, f"主卧在{p}(凶位)"
    breakdown["master_bed"] = {"score": s, "why": why}

    # 3) 厨房
    kitchens = pick_rooms(data, LABEL_BUCKET["kitchen"])
    s = 0
    why = "未检测到厨房"
    if kitchens:
        # 若有多个，以第一个为准；其余微调
        main_k = kitchens[0]
        p = main_k["palace9"]
        if in_set(p, bad) and p != "C":
            s, why = 10, f"厨房在{p}(凶位)属泄凶"
        elif p == "C":
            s, why = -10, "厨房占中宫不宜"
        else:
            s, why = -8, f"厨房在{p}(吉位)易泄吉"
        # 额外：若同时有卫生间同宫，加微扣
    breakdown["kitchen"] = {"score": s, "why": why}

    # 4) 卫浴/洗衣（湿区）
    wets = pick_rooms(data, LABEL_BUCKET["wet"])
    s = 0
    hits = []
    for w in wets:
        p = w["palace9"]
        if p == "C":
            s -= 4
            hits.append(f"{p}中宫-4")
        elif in_set(p, bad):
            s += 2
            hits.append(f"{p}+2")
        else:
            s -= 2
            hits.append(f"{p}-2")
    why = "；".join(hits) if hits else "未检测到湿区"
    breakdown["bath_laundry"] = {"score": s, "why": why}

    # 5) 次卧（整体倾向）
    beds = [r for r in data["rooms"] if r["norm_label"].startswith("bedroom")]
    s = 0
    good_n = bad_n = 0
    for b in beds:
        p = b["palace9"]
        if in_set(p, good):
            s += 3
            good_n += 1
        elif p == "C":
            s -= 4
            bad_n += 1
        else:
            s -= 3
            bad_n += 1
    why = f"卧室吉{good_n}间、凶{bad_n}间"
    breakdown["other_bed"] = {"score": s, "why": why}

    # 6) 车库/储物
    gs = pick_rooms(data, LABEL_BUCKET["garage"])
    s = 0
    for g in gs:
        p = g["palace9"]
        if in_set(p, bad) and p != "C":
            s += 1
    why = f"{len(gs)}处，凶位给+1/处"
    breakdown["garage_store"] = {"score": s, "why": why}

    # 7) 中宫占用
    s = 0
    offenders = []
    for r in data["rooms"]:
        if r["palace9"] == "C" and r["norm_label"] in (
            LABEL_BUCKET["kitchen"] | LABEL_BUCKET["wet"]
        ):
            s -= 5
            offenders.append(r["norm_label"])
    why = "中宫包含：" + ",".join(offenders) if offenders else "中宫安全"
    breakdown["center_c"] = {"score": s, "why": why}

    # 8) 穿堂直冲（Entry 与后门/Alfresco 近似对线）
    entry = door
    alfresco = pick_first(data, {"alfresco", "backyard", "balcony"})
    s = 0
    why = "未检测/不成立"
    if entry and alfresco:
        ex, ey = entry["center_xy"]
        ax, ay = alfresco["center_xy"]
        # 同列（x 差<0.1）且纵向距离>0.5 视为对穿
        if abs(ex - ax) < 0.10 and abs(ey - ay) > 0.50:
            s = -8
            why = "Entry 与后部主要开口近似同列，疑似穿堂"
    breakdown["throughline"] = {"score": s, "why": why}

    # 汇总
    total = sum(v["score"] for v in breakdown.values())
    # 归一到 0-100 区间（硬顶/硬底）
    total = max(0, min(100, 50 + total))  # 以 50 为基准，中性加减
    grade = (
        "S"
        if total >= 90
        else (
            "A"
            if total >= 80
            else ("B" if total >= 70 else ("C" if total >= 60 else "D"))
        )
    )
    out = {
        "total": int(round(total)),
        "grade": grade,
        "house_gua": house_gua_label,
        "breakdown": breakdown,
        "advice": build_advice(group, breakdown),
    }
    return out


def build_advice(group: str, bd: dict):
    tips = []
    if bd["master_bed"]["score"] < 0:
        tips.append(
            "主卧若落凶位：优先调整床头朝东四(东/南/东南/北)或西四(西/西北/西南/东北)的吉向。"
        )
    if bd["kitchen"]["score"] < 0:
        tips.append("厨房落吉位易泄吉：宜以金属与中性色弱化火气，炉口朝宅吉方。")
    if bd["bath_laundry"]["score"] < 0:
        tips.append("湿区落吉位：常闭门、强排风、以金元素为主，减少湿浊外溢。")
    if bd["throughline"]["score"] < 0:
        tips.append("入口与后门对穿：设玄关/矮柜/厚帘，走廊用地毯与分段照明“缓气”。")
    if not tips:
        tips.append("整体格局稳健：保持整洁、通风、动静分区即可。")
    return tips


def main():
    ap = argparse.ArgumentParser(description="ZhongXuan Scoring (八宅+形峦)")
    ap.add_argument("layout_json", help="A 步输出的 layout.json，需包含 house_facing")
    args = ap.parse_args()
    data = load_layout(args.layout_json)
    result = score_layout(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
