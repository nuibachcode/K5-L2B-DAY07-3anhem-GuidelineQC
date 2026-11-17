# Hậu kiểm trực quan `submission/labels/103.json`

- Phạm vi: 27 ảnh theo phân công 103; 26 annotation. Đây là lượt rà của Codex AI trên ảnh gốc và overlay sau khi tọa độ trong file đã được chuẩn hóa từ khung tham chiếu 1024×1024.
- `img_002.jpg`: file 103 chỉ có 1 box `car` trên xe chở 8 ô tô, trong khi R-01 yêu cầu box riêng cho từng ô tô nhìn thấy. Thiếu 7 box `car`.
- `img_030.jpg`: box `motorcycle` `[0.94, 246.09, 922.5, 457.03]` bao phủ một cụm nhiều xe máy; đây không phải box cho một xe. Cần tách từng xe nhìn thấy rõ hoặc áp dụng `ignore_region` cho phần không thể phân tách ổn định.
- `img_032.jpg`: box `person` `[11.25, 237.3, 663.75, 109.57]` bao phủ cả hàng người ở trạm xe buýt; cần box riêng theo từng người nhìn rõ hoặc `ignore_region` cho cụm không thể tách ổn định.
- `img_040.jpg`: box `tuk_tuk` `[315.94, 95, 821.25, 406.25]` trùm tuk-tuk nền, người đi xe máy và một phần xe con màu xanh. Cần xác định lại từng vật thể và vẽ box theo R-07.

Các lỗi nội dung này chưa được sửa trong file nhãn độc lập ở lượt hiện tại để không âm thầm thay đổi đầu vào đã dùng tính IAA/calibration. File 103 vốn đã được AI chuẩn hóa tọa độ nên số IAA hiện có chỉ mô tả các artifact hiện tại, không chứng minh ba người đã gán độc lập. Người gán thật cần sửa và xác nhận file 103; sau đó phải chạy lại `qc_compare.py`, tạo lại các quyết định cho candidate mới, `build_final.py` và QC toàn lô.
