# Tóm tắt IAA (taxonomy v1.0)

- Ảnh được so sánh (có >=2 người gán): **40**; số người gán: 3
- Lượt gán đủ **80/80**.
- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= 0.5, ghép 1-1 không phân biệt lớp). Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.
- Mẫu số: 111 cặp box ghép (tổng mọi cặp người gán, ảnh chung).

| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | Cùng occluded_level | Cùng truncated | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |
|---|---|---|---|---|---|---|---|---|---|
| **TỔNG** | 40 | 111 | 0.803 | 92.8% | 46.8% | 91.0% | 229/36 | 0 | CHƯA ĐẠT |
| 101|102 | 13 | 91 | 0.816 | 93.4% | 40.7% | 91.2% | 32/30 | 0 | CHƯA ĐẠT |
| 101|103 | 13 | 10 | 0.721 | 80.0% | 60.0% | 90.0% | 122/4 | 0 | CHƯA ĐẠT |
| 102|103 | 14 | 10 | 0.771 | 100.0% | 90.0% | 90.0% | 75/2 | 0 | CHƯA ĐẠT |

Ngưỡng IAA: IoU TB >= 0.85, đồng thuận lớp >= 95%.

Số ca bất thường: 407 ({'bo_sot_thua': 248, 'iou_thap': 58, 'sai_thuoc_tinh': 62, 'co_can_review': 10, 'sai_lop': 8, 'bat_dong_ignore': 21}), trên 35 ảnh cần calibration.
