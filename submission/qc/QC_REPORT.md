# Báo cáo QC — 3anhem

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: Bộ nhãn bounding box 2D cho bài thực hành Day 07; 40 ảnh tuyển chọn để luyện tình huống biên, chưa đánh giá độ đại diện cho dữ liệu vận hành.
- Manifest và checksum nhãn cuối: Manifest `submission/qc/batch_manifest.json`, SHA-256 `e772c4d05127efe5fc352bd754518743b3f989606d8c266370ee35aa03ca6eb4`; COCO cuối SHA-256 `79b1041972c1a5828237cd58e1cde2890058c7f0d931b50576cc1b3593fa0695`. Bản cuối có 40 ảnh và 379 annotation, gồm 377 đối tượng ngoài `ignore_region`.
- Guideline và taxonomy khi gán / khi bàn giao: Lượt độc lập được gán theo guideline/taxonomy v1.0. Bản bàn giao dùng `guideline_v1.1_calibrated.md` và `taxonomy_v1.1.json`; v1.1 làm rõ pickup thông thường luôn là `car`, giữ nguyên taxonomy classes/attributes và các ngưỡng `rules`.

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: 80/80 lượt hợp lệ về cấu trúc; 101: 26/26 ảnh, 102: 27/27, 103: 27/27. File 103 có 26 annotation; ảnh không có đối tượng taxonomy vẫn xuất hiện trong COCO.
- Hậu kiểm nội dung file 103: Phát hiện thiếu 7 ô tô ở `img_002.jpg`, một box `motorcycle` gộp nhiều xe ở `img_030.jpg`, một box `person` phủ đám đông ở `img_032.jpg`, và box `tuk_tuk` chồng nhiều vật thể ở `img_040.jpg`. Chi tiết tọa độ và quy tắc xem `submission/qc/103_visual_audit.md`; các lỗi này cần người gán thật sửa và xác nhận.
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: 111 cặp ghép; IoU trung bình 0,803/111; cùng lớp 103/111 = 92,8%; cùng `occluded_level` 52/111 = 46,8%; cùng `truncated` 101/111 = 91,0%. IAA chưa đạt ngưỡng IoU 0,85 và đồng thuận lớp 95%; do nhãn 103 đã được AI chuẩn hóa và còn lỗi nội dung được phát hiện, các số này chỉ mô tả artifact hiện có, không chứng minh đồng thuận độc lập của ba người.
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: 229 box chưa ghép A / 36 box chưa ghép B; 0 box được bỏ qua do ignore; 21 bất đồng vùng ignore; 58 cặp có IoU dưới ngưỡng ghép chất lượng.
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: Không có bộ nhãn tham chiếu độc lập của coach trong workspace nên chưa thể xác nhận bằng nguồn ngoài. Hậu kiểm ảnh đã phát hiện và ghi quyết định riêng cho tám xe con cần thêm ở `img_002.jpg`, pickup ở `img_001.jpg`/`img_012.jpg`, và xe đạp ngoài taxonomy ở `img_039.jpg`.

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: `calibration_candidates.csv` có 407 ca; `calibration_decisions.csv` có 412 dòng gồm 407 ca và năm quyết định bổ sung S001–S005. S001 bổ sung tám xe con ở `img_002.jpg` theo R-01; S002 xử lý van ở `img_005.jpg`; S003 bỏ box xe đạp ngoài taxonomy ở `img_039.jpg`; S004 phân biệt xe con và xe máy ở `img_013.jpg`; S005 làm rõ R-08 trên cả lô. Các quyết định hậu kiểm do Codex AI thực hiện trong vai trò được nhóm yêu cầu; mã `101-AI`/`102` không phải xác nhận của người thật.
- Tác động v1.1 lên nhãn và ảnh: Làm rõ pickup thông thường có cabin và thùng pickup gắn liền là `car` dù chở hàng; `truck` chỉ dùng cho xe có kết cấu chở hàng chuyên dụng tách biệt rõ với cabin. Đổi nhãn pickup ở `img_001.jpg` và `img_012.jpg` sang `car`; rà đối chiếu `img_002.jpg`, `img_028.jpg`, `img_036.jpg`, `img_037.jpg`. Ở `img_013.jpg`, giữ xe tại `[162,423,199,448]` là `car` và sửa xe tại `[249,442,306,483]` thành `motorcycle`. Giữ nguyên các ngưỡng trong `taxonomy.json` v1.0.
- Kiểm lại các cờ trước đó: Gỡ `can_review` cho người nhìn thấy ở `img_005.jpg` (ID 40), pickup `img_012.jpg` (ID 127), hai xe nhỏ `img_013.jpg` (ID 130 và 133), và xe kích thước thật ở `img_019.jpg` (ID 167). Còn 7 box cần xác nhận người thật: ID 94 ở `img_008.jpg`; ID 137, 138, 139, 140, 141 và 144 ở `img_014.jpg`.
- Tham chiếu bằng chứng khi Rework: Round-01 phát hiện tám xe con thiếu ở `img_002.jpg`; S001 dẫn tới ảnh gốc và tám box `car` trong COCO cuối. S005 dẫn tới R-08 và các ví dụ pickup trong cả lô. C147/C148 và S004 dẫn tới hai box riêng ở `img_013.jpg`. Round-01 đến round-05 được giữ nguyên. Round-06 dùng cùng SHA-256 nhãn với round-05 sau khi làm mới manifest; phiếu round-05 được giữ lại vì nội dung nhãn không đổi.

## 4. Kết quả duyệt

- Vòng QC: 6
- Người review và ngày: Codex AI thực hiện hậu kiểm trong vai trò review 102 theo yêu cầu của nhóm, ngày 2026-11-17; đây không phải lượt duyệt độc lập của người thật.
- Đã duyệt / cả lô: 40/40 ảnh = 100% trong lượt rà soát overlay AI.
- Ảnh lỗi / ảnh đã duyệt: 2/40 = 5,0%; các ảnh còn mở là `img_008.jpg` và `img_014.jpg`.
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: 7/377 = 1,9%; bảy dòng còn mở là cờ `can_review`, không khẳng định toàn bộ giá trị thuộc tính khác sai.
- Vật bỏ sót, ảnh và vùng: 0 vật bỏ sót được ghi trong round-06.
- Ca khó / phần còn lại, lỗi lặp và ví dụ: ID 94 ở `img_008.jpg` chưa đủ dấu hiệu để phân biệt tuk-tuk với xe có khoang kín khác; sáu box ở `img_014.jpg` chồng lên các vệt chuyển động, chưa nhận diện chắc lớp hoặc ranh giới. Tỷ lệ ảnh có lỗi 5,0% vượt ngưỡng lớp học 2%; báo cáo tự động trả HOLD khi còn `can_review`.
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: `validate_labels.py --all` xác nhận đúng tập ảnh, kích thước và cấu trúc COCO. Script không thể xác nhận vật thể/box có đúng thực tế; cần người thật kiểm tra xe phía sau ở `img_008.jpg`, vệt chuyển động ở `img_014.jpg`, và tính độc lập của nhãn 103 đã được AI chuẩn hóa.

## 5. Quyết định bàn giao

- Quyết định: Hold
- Lý do, người nhận và phạm vi sử dụng: IAA trước calibration chưa đạt và không thể xem là bằng chứng độc lập vì đầu vào 103 đã được AI chuẩn hóa, còn lỗi nội dung nêu trong `103_visual_audit.md`; round-06 cũng còn 7 box cần xác nhận trên 2/40 ảnh. Review hiện tại do AI mô phỏng. Chỉ dùng để nhóm/coach xem xét nội bộ, chưa đủ cơ sở Release.
- Nếu còn việc: Thành viên gán thật sửa và xác nhận các ca trong `103_visual_audit.md`, chạy lại IAA và calibration cho candidate mới, xử lý bảy box còn cờ, rồi `build_final.py` và QC toàn lô ở vòng mới. Giữ round-01 đến round-06 làm lịch sử.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: S001 → `img_002.jpg` → R-01 → tám box `car`; S005 → `img_001.jpg`/`img_012.jpg` → R-08 → class `car`; C147/C148/S004 → `img_013.jpg` → taxonomy §2.1 → class `motorcycle`/`car`; C089 → `img_008.jpg` → R-02/§2.2 → ID 94 còn cờ. Sáu box `img_014.jpg` có trong `submission/qc/reviews/round-06/qc_review.csv`; hash nhãn và manifest được ghi ở mục 1.
