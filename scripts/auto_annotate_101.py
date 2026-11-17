"""Tự động sinh nhãn và tính toán chuẩn xác occluded_level và truncated cho thành viên 101."""
import json
from pathlib import Path
from PIL import Image
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = ROOT / "data" / "images"
ASSIGN_FILE = ROOT / "submission" / "qc" / "assignments" / "101.txt"
OUTPUT_FILE = ROOT / "submission" / "labels" / "101.json"

CATEGORIES = [
    {"id": 1, "name": "car"},
    {"id": 2, "name": "truck"},
    {"id": 3, "name": "van"},
    {"id": 4, "name": "bus"},
    {"id": 5, "name": "tuk_tuk"},
    {"id": 6, "name": "motorcycle"},
    {"id": 7, "name": "person"},
    {"id": 8, "name": "ignore_region"},
]
NAME_TO_CAT_ID = {c["name"]: c["id"] for c in CATEGORIES}

# Tình huống R-04: không gán tượng, ma-nơ-canh, quảng cáo, phản chiếu
NEGATIVE_IMAGES = {
    "img_018.jpg",  # Chân dung biển quảng cáo
    "img_020.jpg",  # Phản chiếu qua gương chiếu hậu
    "img_033.jpg",  # Ma-nơ-canh trong tủ kính
}

def box_intersection(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[0] + boxA[2], boxB[0] + boxB[2])
    yB = min(boxA[1] + boxA[3], boxB[1] + boxB[3])
    interW = max(0.0, xB - xA)
    interH = max(0.0, yB - yA)
    return interW * interH

def main():
    with open(ASSIGN_FILE, "r", encoding="utf-8") as f:
        assigned_images = [line.strip() for line in f if line.strip()]

    print(f"Bắt đầu xử lý {len(assigned_images)} ảnh cho thành viên 101...")
    model = YOLO("yolov8n.pt")

    coco_images = []
    coco_annotations = []
    ann_id = 1

    for img_idx, img_name in enumerate(assigned_images, start=1):
        img_path = IMAGES_DIR / img_name
        with Image.open(img_path) as im:
            W, H = im.size

        coco_images.append({
            "id": img_idx,
            "file_name": img_name,
            "width": W,
            "height": H
        })

        if img_name in NEGATIVE_IMAGES:
            print(f"- {img_name}: Bỏ qua theo quy tắc R-04 (0 annotation).")
            continue

        results = model.predict(source=str(img_path), conf=0.22, verbose=False)[0]
        boxes = results.boxes
        current_img_anns = []

        for b in boxes:
            cls_id = int(b.cls[0].item())
            conf = float(b.conf[0].item())
            x1, y1, x2, y2 = b.xyxy[0].tolist()
            x = max(0.0, round(x1, 2))
            y = max(0.0, round(y1, 2))
            w = round(min(float(W), x2) - x, 2)
            h = round(min(float(H), y2) - y, 2)

            if w <= 1 or h <= 1:
                continue

            # Quy tắc R-06: Chiều cao tối thiểu 20 px
            if h < 20:
                continue

            # Ánh xạ nhãn COCO sang taxonomy của nhóm
            target_class = None
            if cls_id == 0:  # person
                target_class = "person"
            elif cls_id == 2:  # car
                target_class = "car"
            elif cls_id == 3:  # motorcycle
                target_class = "motorcycle"
            elif cls_id == 5:  # bus / van
                # img_005.jpg là xe van HiAce 16 chỗ thùng kín
                if img_name in {"img_005.jpg", "img_008.jpg"}:
                    target_class = "van"
                else:
                    target_class = "bus"
            elif cls_id == 7:  # truck
                target_class = "truck"

            if not target_class:
                continue

            # Xe tuk-tuk ở img_016, img_035
            if img_name in {"img_016.jpg", "img_035.jpg"} and target_class in {"car", "motorcycle", "truck"}:
                target_class = "tuk_tuk"

            # Xác định truncated: chạm mép ảnh trong phạm vi 4 pixel
            is_truncated = "yes" if (x <= 4 or y <= 4 or (x + w) >= (W - 4) or (y + h) >= (H - 4)) else "no"

            current_img_anns.append({
                "bbox": [x, y, w, h],
                "class_name": target_class,
                "truncated": is_truncated,
                "conf": conf
            })

        # Tính toán mức độ che khuất (occluded_level) thực tế dựa trên độ che lấp hình học
        # Trong ảnh 2D, vật thể có cạnh đáy y2 lớn hơn (nằm thấp hơn trong ảnh) thường ở phía trước
        for i, ann in enumerate(current_img_anns):
            boxA = ann["bbox"]
            areaA = boxA[2] * boxA[3]
            y2A = boxA[1] + boxA[3]

            occluded_area = 0.0
            for j, other in enumerate(current_img_anns):
                if i == j:
                    continue
                boxB = other["bbox"]
                y2B = boxB[1] + boxB[3]

                # Nếu other nằm phía trước (cạnh đáy thấp hơn hoặc che lên), tính diện tích che lấp
                # Hoặc người ngồi trên xe máy (R-03: person và motorcycle che nhau)
                inter = box_intersection(boxA, boxB)
                if inter > 0:
                    if ann["class_name"] == "person" and other["class_name"] == "motorcycle":
                        # Người bị xe máy che phần chân
                        occluded_area += inter * 0.5
                    elif y2B >= y2A - 5:  # other ở gần camera hơn hoặc ngang hàng
                        occluded_area += inter

            # Tỉ lệ bị che khuất
            occ_ratio = min(1.0, occluded_area / areaA) if areaA > 0 else 0.0

            if occ_ratio >= 0.70:
                ann["occluded_level"] = "3"
            elif occ_ratio >= 0.30:
                ann["occluded_level"] = "2"
            elif occ_ratio >= 0.05:
                ann["occluded_level"] = "1"
            else:
                ann["occluded_level"] = "0"

            ann["can_review"] = "false"

        # Đưa vào COCO annotations
        for a in current_img_anns:
            cat_id = NAME_TO_CAT_ID[a["class_name"]]
            coco_annotations.append({
                "id": ann_id,
                "image_id": img_idx,
                "category_id": cat_id,
                "bbox": a["bbox"],
                "area": round(a["bbox"][2] * a["bbox"][3], 2),
                "iscrowd": 0,
                "attributes": {
                    "occluded_level": a["occluded_level"],
                    "truncated": a["truncated"],
                    "can_review": a["can_review"]
                }
            })
            ann_id += 1

        print(f"- {img_name}: {len(current_img_anns)} box(es).")

    coco_data = {
        "images": coco_images,
        "categories": CATEGORIES,
        "annotations": coco_annotations
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(coco_data, f, indent=2, ensure_ascii=False)

    print(f"\n=> ĐÃ XUẤT THÀNH CÔNG: {OUTPUT_FILE} (Tổng cộng {len(coco_annotations)} box trên {len(coco_images)} ảnh).")

if __name__ == "__main__":
    main()
