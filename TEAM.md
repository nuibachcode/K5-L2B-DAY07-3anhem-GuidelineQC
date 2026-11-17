# Thông tin nhóm

- Tên nhóm: 3anhem
- Mã thành viên: 101, 102, 103
- Người điều phối theo hồ sơ nhóm: 101
- Vai trò review vòng cuối: Codex AI mô phỏng vai trò 102 theo yêu cầu; chưa có xác nhận review độc lập của người thật.
- Không tạo commit hoặc push GitHub theo yêu cầu.

## Kết quả tóm tắt

- Lượt gán hợp lệ về cấu trúc: 80/80 (101: 26/26 ảnh, 102: 27/27, 103: 27/27). File 103 có 26 annotation và đã được AI ánh xạ từ khung 1024×1024; hậu kiểm thấy lỗi nội dung ở `img_002`, `img_030`, `img_032`, `img_040`. Xem `submission/qc/103_visual_audit.md`.
- IAA trước calibration: 111 cặp; IoU trung bình 0,803; đồng thuận lớp 92,8%; thấp hơn ngưỡng 0,85/95%. Vì nhãn 103 đã qua chuẩn hóa AI và có lỗi nội dung, các số chỉ mô tả artifact hiện tại, không xác nhận ba lượt gán độc lập.
- Calibration: 407 candidate và 5 quyết định bổ sung, tổng 412 dòng. Bản bàn giao áp dụng guideline/taxonomy v1.1 để giải quyết mâu thuẫn phân loại pickup; mục `rules` giữ nguyên.
- Nhãn cuối: 40 ảnh, 379 annotation (377 đối tượng ngoài `ignore_region`).
- Vòng QC cuối: round-06 duyệt 40/40 ảnh; giữ phiếu rà round-05 vì SHA-256 nhãn không đổi. Còn 7 box `can_review` ở `img_008.jpg` và `img_014.jpg`. Tỷ lệ là 7/377 annotation và 2/40 ảnh.
- Quyết định: **Hold**. Các box còn mờ và tính độc lập của nhãn 103 cần review người thật trước Release. Codex AI đã hỗ trợ hoàn thiện hồ sơ theo yêu cầu, không thay cho chữ ký hay xác nhận của thành viên.
