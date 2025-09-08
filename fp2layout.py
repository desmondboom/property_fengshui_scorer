#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import re
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np
import pytesseract

# --------- 可调词典：房间名正则 -> 归一化类型 ----------
ROOM_PATTERNS = [
    (r"\bmaster\s*bed(room)?\b", "master_bedroom"),
    (r"\bbed(room)?\s*([1-9])\b", "bedroom"),
    (r"\bbed(room)?\b", "bedroom"),
    (r"\blounge\b", "lounge"),
    (r"\bliving\s*/?\s*dining\b", "living_dining"),
    (r"\bkitchen\b", "kitchen"),
    (r"\bpantry\b", "pantry"),
    (r"\bdouble\s*garage\b|\bgarage\b", "garage"),
    (r"\balfresco\b", "alfresco"),
    (r"\bentry\b|\bfoyer\b|\bporch\b", "entry"),
    (r"\bbath(room)?\b", "bath"),
    (r"\bens(uite)?\b", "ensuite"),
    (r"\bwc\b|\btoilet\b|\bpowder\b", "wc"),
    (r"\bldry\b|\blaundry\b", "laundry"),
    (r"\bwir\b|\bwalk[-\s]*in\s*robe\b", "wir"),
    (r"\brobe\b|\bcloset\b", "robe"),
    (r"\bstudy\b|\boffice\b", "study"),
]

DIRECTION_8 = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

# 允许的朝向 & 反向映射
ALLOWED_FACING = {"N", "NE", "E", "SE", "S", "SW", "W", "NW"}
OPPOSITE = {
    "N": "S",
    "NE": "SW",
    "E": "W",
    "SE": "NW",
    "S": "N",
    "SW": "NE",
    "W": "E",
    "NW": "SE",
}


@dataclass
class DetectedLabel:
    raw_text: str
    norm_label: str
    bbox: Tuple[int, int, int, int]  # left, top, width, height
    conf: float
    center_xy: Tuple[float, float]  # normalized [0,1] relative to image (x,y)
    direction8: str
    palace9: str  # 九宫：NW,N,NE / W,C,E / SW,S,SE


def infer_house_facing(rooms: List[DetectedLabel]) -> Optional[str]:
    """
    简易推断：
    1) 优先用 entry/porch/foyer 所在九宫当作朝向；
    2) 没有入口标签，则若有 alfresco/backyard/balcony，则用其对面方向；
    3) 否则返回 None。
    """
    # 先找入口
    for r in rooms:
        nl = r.norm_label.lower()
        if nl in {"entry", "porch", "foyer"}:
            return r.palace9  # 直接用所在宫位 N/NE/...（与八方名一致）
    # 用后院类的反向兜底
    for r in rooms:
        nl = r.norm_label.lower()
        if nl in {"alfresco", "backyard", "balcony"}:
            return OPPOSITE.get(r.palace9)
    return None


def preprocess_for_ocr(img: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 提高对比 + 去噪
    gray = cv2.bilateralFilter(gray, 7, 50, 50)
    # 自适应阈值（反白）
    th = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 35, 15
    )
    # 膨胀，让细文字连成块
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    th = cv2.dilate(th, kernel, iterations=1)
    return th


def ocr_lines(img: np.ndarray) -> List[Dict]:
    # 用 image_to_data 拿到每个“行”的框
    config = "--oem 3 --psm 6"  # assume uniform block of text
    data = pytesseract.image_to_data(
        img, lang="eng", config=config, output_type=pytesseract.Output.DICT
    )
    n = len(data["text"])
    lines = {}
    for i in range(n):
        text = data["text"][i].strip()
        conf = float(data["conf"][i]) if data["conf"][i] != "-1" else -1
        if conf < 0:
            continue
        key = (data["block_num"][i], data["par_num"][i], data["line_num"][i])
        bbox = (data["left"][i], data["top"][i], data["width"][i], data["height"][i])
        if key not in lines:
            lines[key] = {
                "text": [],
                "bbox": [bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]],
                "confs": [],
            }
        lines[key]["text"].append(text)
        lines[key]["confs"].append(conf)
        # 扩 bbox
        l, t, r, b = lines[key]["bbox"]
        l = min(l, bbox[0])
        t = min(t, bbox[1])
        r = max(r, bbox[0] + bbox[2])
        b = max(b, bbox[1] + bbox[3])
        lines[key]["bbox"] = [l, t, r, b]
    # 合并文本
    out = []
    for _, v in lines.items():
        joined = " ".join([x for x in v["text"] if x])
        if joined.strip():
            out.append(
                {
                    "text": joined,
                    "bbox": v["bbox"],
                    "conf": float(np.mean(v["confs"])) if v["confs"] else 0.0,
                }
            )
    return out


def normalize_label(text: str) -> Optional[Tuple[str, Dict]]:
    txt = text.lower()
    # 常见噪声清洗
    txt = (
        txt.replace("’", "'")
        .replace("‘", "'")
        .replace("`", "'")
        .replace("l'dry", "ldry")
    )
    for pat, norm in ROOM_PATTERNS:
        if re.search(pat, txt):
            # 补充 bedroom 序号
            m = re.search(r"\bbed(room)?\s*([1-9])\b", txt)
            meta = {}
            if norm == "bedroom" and m:
                meta["number"] = int(m.group(2))
            return norm, meta
    return None


def rotate_point(xy: Tuple[float, float], north_deg: float) -> Tuple[float, float]:
    # 将点以图像中心(0.5,0.5)为原点，顺时针旋转 -north_deg，让“真北”对齐到上方
    theta = -np.deg2rad(north_deg)
    x, y = xy
    cx, cy = 0.5, 0.5
    X = x - cx
    Y = y - cy
    xr = X * np.cos(theta) - Y * np.sin(theta)
    yr = X * np.sin(theta) + Y * np.cos(theta)
    return (xr + cx, yr + cy)


def to_direction8(xy: Tuple[float, float]) -> str:
    # 以图像中心为原点, 计算角度 => 8 方位
    cx, cy = 0.5, 0.5
    vx, vy = xy[0] - cx, cy - xy[1]  # y 轴向上为正
    ang = (np.rad2deg(np.arctan2(vy, vx)) + 360.0) % 360.0
    idx = int(((ang + 22.5) % 360) // 45)  # 每45°一扇区
    return DIRECTION_8[idx]


def to_palace9(xy: Tuple[float, float]) -> str:
    # 九宫：把画面三等分
    x, y = xy
    col = 0 if x < 1 / 3 else (2 if x > 2 / 3 else 1)
    row = 0 if y < 1 / 3 else (2 if y > 2 / 3 else 1)
    grid = {
        (0, 0): "NW",
        (1, 0): "N",
        (2, 0): "NE",
        (0, 1): "W",
        (1, 1): "C",
        (2, 1): "E",
        (0, 2): "SW",
        (1, 2): "S",
        (2, 2): "SE",
    }
    return grid[(col, row)]


def detect_layout(
    image_path: str, north_deg: float, house_facing: Optional[str] = None
) -> Dict:
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(image_path)
    H, W = img.shape[:2]
    prep = preprocess_for_ocr(img)
    lines = ocr_lines(prep)

    rooms: List[DetectedLabel] = []
    for ln in lines:
        norm = normalize_label(ln["text"])
        if not norm:
            continue
        norm_label, meta = norm
        l, t, r, b = ln["bbox"]
        cx = (l + r) / 2.0 / W
        cy = (t + b) / 2.0 / H
        cxr, cyr = rotate_point((cx, cy), north_deg)
        direction = to_direction8((cxr, cyr))
        palace = to_palace9((cxr, cyr))
        item = DetectedLabel(
            raw_text=ln["text"],
            norm_label=(
                norm_label
                if not (norm_label == "bedroom" and "number" in meta)
                else f"bedroom_{meta['number']}"
            ),
            bbox=(l, t, r - l, b - t),
            conf=float(ln["conf"]),
            center_xy=(round(cxr, 4), round(cyr, 4)),
            direction8=direction,
            palace9=palace,
        )
        rooms.append(item)

    if not house_facing:
        guessed = infer_house_facing(rooms)
        house_facing = guessed if guessed in ALLOWED_FACING else None

    result = {
        "image_size": {"width": W, "height": H},
        "north_deg": north_deg,
        "house_facing": house_facing,
        "rooms": [asdict(r) for r in rooms],
        "schema_version": "v1",
    }
    return result


def main():
    ap = argparse.ArgumentParser(
        description="Floorplan -> Structured JSON (rooms + directions)"
    )
    ap.add_argument("--image", required=True, help="input floorplan image (png/jpg)")
    ap.add_argument(
        "--north-deg",
        type=float,
        default=0.0,
        help="true north relative to image up, clockwise degrees",
    )
    ap.add_argument(
        "--house-facing",
        type=str,
        choices=sorted(list(ALLOWED_FACING)),
        help="house facing direction: N/NE/E/SE/S/SW/W/NW; if omitted, try to infer from entry/alfresco",
    )
    ap.add_argument("--out", default="layout.json", help="output JSON path")
    args = ap.parse_args()

    data = detect_layout(args.image, args.north_deg, args.house_facing)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[ok] saved: {args.out}  rooms={len(data['rooms'])}")


if __name__ == "__main__":
    main()
