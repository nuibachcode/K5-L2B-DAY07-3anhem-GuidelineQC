# Guideline gán nhãn — v1.1 (Bản hiệu chỉnh nhóm 3anhem)

- **Phiên bản:** v1.1
- **Ngày:** 2026-11-16
- **Nhóm thực hiện:** 3anhem (Mã thành viên: 101, 102, 103)
- **Người điều phối & duyệt:** 101
- **Công cụ áp dụng:** CVAT, xuất chuẩn COCO 1.0

---

## 1. Mục tiêu

- **Mục đích sử dụng**: Bộ dữ liệu gán nhãn bounding box (2D) dùng để huấn luyện và đánh giá mô hình phát hiện vật thể (Object Detection) phục vụ hệ thống lái xe tự động / hỗ trợ lái xe an toàn (ADAS) và hệ thống camera giám sát giao thông đô thị.
- **Rủi ro an toàn và trọng số lỗi**:
  - *Bỏ sót người đi bộ / người điều khiển phương tiện (VRU)*: Rủi ro tai nạn giao thông nghiêm trọng cấp độ cao nhất.
  - *Nhầm lẫn loại phương tiện*: Ô tô con vs Xe tải/Xe buýt có kích thước và khoảng cách phanh hoàn toàn khác nhau, gây nguy cơ va chạm do ước tính khoảng cách sai.
  - *Báo động giả (False Positive)*: Nhận nhầm tượng đá, phù điêu, ma-nơ-canh, biển quảng cáo hoặc hình ảnh phản chiếu trên gương làm hệ thống kích hoạt phanh khẩn cấp vô căn cứ (*phantom braking*), gây nguy hiểm cho xe phía sau.

---

## 2. Lớp và thuộc tính (Taxonomy v1.1; nhãn độc lập được gán theo v1.0)

Sau cuộc họp Pha 2, nhóm thống nhất mở rộng taxonomy từ 6 lớp ban đầu lên **8 lớp** để giải quyết triệt để các tình huống thực tế trong 40 ảnh.

### 2.1. Danh sách lớp (Classes)

| Lớp | Định nghĩa (chuẩn xác) | Ví dụ trong bộ ảnh | Phản ví dụ / Dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô chở người từ 4 đến 9 chỗ, bao gồm sedan, hatchback, SUV, CUV và xe bán tải dạng pickup thông thường. Pickup thông thường được gán `car` dù đang chở hàng. | Xe sedan, SUV, ô tô con trên xe lồng (`img_002.jpg`), pickup (`img_001.jpg`, `img_012.jpg`, `img_028.jpg`, `img_037.jpg`). | Xe van chở hàng kín, xe tải có thân/thùng chở hàng chuyên dụng (`truck`), xe tuk-tuk, xe buýt (`bus`), xe mô hình đồ chơi (`img_038.jpg`). |
| `truck` | Xe chở hàng có cabin và thân/thùng/sàn tải chuyên dụng, tách biệt rõ với khoang cabin; gồm xe container, xe ben, xe đầu kéo và xe lồng chở ô tô. Pickup thông thường không chuyển thành `truck` chỉ vì đang chở hàng. | Xe chở ô tô 2 tầng (`img_002.jpg`), xe tải nhỏ có thân chở hàng chuyên dụng (`img_036.jpg`). | Pickup thông thường (`car`), xe thùng kín liền khối (`van`). Không gán riêng các kiện hàng hóa trên thùng xe. |
| `van` | Xe ô tô chở người hoặc hàng hóa có thân xe dạng thùng kín liền khối với cabin (panel van, minivan). | Xe minivan, xe cứu thương cỡ nhỏ, xe chuyển phát bọc kín. | Xe tải thùng rời (`truck`), xe bán tải gắn nắp thùng cao (`car`), xe buýt cỡ lớn (`bus`). |
| `bus` | Xe ô tô khách cỡ lớn chở nhiều người (thường từ 16 chỗ trở lên), xe buýt công cộng, xe du lịch lớn. | Xe buýt lớn trong cảnh phố (`img_009.jpg`, `img_031.jpg`, `img_037.jpg`, `img_040.jpg`). | Xe tải lớn (`truck`), xe van 16 chỗ cỡ nhỏ (`van`). |
| `tuk_tuk` | Phương tiện cơ giới 3 bánh chuyên chở khách hoặc hàng hóa nhẹ đặc trưng đô thị (auto-rickshaw, xe lam). | Xe tuk-tuk 3 bánh (`img_004.jpg`, `img_016.jpg`, `img_035.jpg`). | Xe máy 2 bánh (`motorcycle`), xe xích lô đạp chân (ngoài taxonomy). |
| `motorcycle` | Phương tiện cơ giới 2 bánh (kể cả xe máy gắn thêm thùng phụ bên hông - sidecar), gồm xe máy số, xe tay ga, mô tô phân khối lớn. | Xe máy lưu thông trên đường (`img_005.jpg`, `img_026.jpg`), xe máy có sidecar (`img_022.jpg`). | Xe đạp, xích lô, xe tuk-tuk 3 bánh, người điều khiển xe máy (phải tách riêng `person`). |
| `person` | Con người thật còn sống trong mọi tư thế (đi bộ, đứng, ngồi, nằm, chạy) hoặc đang điều khiển / ngồi trên phương tiện. | Người đi bộ qua đường, người lái/ngồi sau xe máy (`img_005.jpg`), người mặc trang phục biểu diễn (`img_011.jpg`). | Tượng đồng/đá (`img_017.jpg`), ma-nơ-canh (`img_033.jpg`), hình chân dung quảng cáo (`img_018.jpg`), hình phản chiếu trên kính. |
| `ignore_region` | Vùng không gian cục bộ chứa đám đông hoặc cụm đối tượng mục tiêu quá mờ/nhỏ (< 60 px) không thể tách rời ổn định. Bỏ sót trong vùng này không tính là lỗi. | Cụm người/xe dính chùm phía xa cuối phố, vùng chợ đông nghẹt không phân tách nổi từng người. | Không dùng để che vật rõ nét, không dùng để che toàn bộ ảnh hoặc che đối tượng ngoài taxonomy. |

**Đối tượng ngoài taxonomy:**
- Xe đạp, xích lô, xe động vật kéo, xe nôi: **Không gán box cho phương tiện**. Chỉ gán box `person` cho người điều khiển nếu nhìn thấy rõ.
- Hàng hóa chở trên xe (thùng gỗ, bao tải, phụ tùng): Không gán nhãn hàng hóa riêng.

### 2.2. Thuộc tính (Attributes)

| Thuộc tính | Kiểu dữ liệu | Giá trị | Ý nghĩa & Ngưỡng định lượng cụ thể |
|---|---|---|---|
| `occluded_level` | Select | `0`, `1`, `2`, `3` | **Tỷ lệ diện tích thân vật thể bị che khuất bởi vật khác**:<br>- `0`: Thấy rõ hoàn toàn (che 0%).<br>- `1`: Che nhẹ (1% – 30% diện tích toàn thân vật thể bị che khuất).<br>- `2`: Che đáng kể (31% – 70% diện tích toàn thân vật thể bị che khuất).<br>- `3`: Che nặng (> 70% diện tích toàn thân vật thể bị che khuất nhưng vẫn nhận diện được chắc chắn). |
| `truncated` | Select | `no`, `yes` | **Bị cắt bởi mép ảnh**:<br>- `no`: Nằm trọn vẹn trong 4 cạnh của ảnh.<br>- `yes`: Bị cắt ngang bởi ít nhất một mép biên của khung hình ảnh. |
| `can_review` | Checkbox | `true`, `false` | Đánh dấu khi người gán chưa hoàn toàn chắc chắn về lớp hoặc ranh giới, cần đưa ra hiệu chỉnh trong phiên họp calibration. |

---

## 3. Quy tắc vẽ Bounding Box (Rules `R-01` đến `R-08`)

- **`R-01` (Xe chở xe)**: Trên xe chuyên dụng chở ô tô (`img_002.jpg`), gán 1 box `truck` bao toàn bộ xe tải chở hàng; đồng thời **gán từng box `car` riêng biệt** cho mỗi ô tô con nguyên chiếc nhìn thấy trên hai tầng giá đỡ. *(Giải quyết bất đồng giữa 102 và 101/103: mô hình cần phát hiện chướng ngại vật ô tô con để tránh va chạm hàng hóa).*
- **`R-02` (Xe ba bánh tuk-tuk)**: Xe tuk-tuk gán vào lớp riêng `tuk_tuk`. Người lái và hành khách ngồi trên xe nếu nhìn thấy rõ thì gán thêm box `person` tương ứng.
- **`R-03` (Người điều khiển và xe máy)**: Bắt buộc tách thành **2 box độc lập**:
  - 1 box `motorcycle` ôm trọn thân xe máy (từ bánh trước, bánh sau, gương lái đến gầm xe).
  - 1 box `person` ôm trọn người ngồi trên xe (từ mũ bảo hiểm đến gót chân).
  - Phần thân người và xe giao nhau được bao trong cả hai box. Box `person` đặt `occluded_level = 1` hoặc `2` tùy mức che khuất của đầu xe.
- **`R-04` (Vật không phải thực thể sống / phương tiện thật)**: **Tuyệt đối KHÔNG gán box** cho:
  - Tượng đồng, tượng đá danh nhân (`img_017.jpg`).
  - Tượng mô hình phương tiện trang trí trên bệ (`img_027.jpg`).
  - Ma-nơ-canh trong tủ kính (`img_033.jpg`).
  - Ô tô mô hình, xe đồ chơi trẻ em (`img_038.jpg`).
  - Hình in người hoặc xe trên biển hiệu, poster, pano quảng cáo (`img_018.jpg`).
  - Hình ảnh phản chiếu qua gương chiếu hậu (`img_020.jpg`) hoặc mặt kính tòa nhà.
- **`R-05` (Phương tiện ngoài taxonomy)**: Xe đạp, xích lô, xe ngựa kéo (`img_006.jpg`, `img_029.jpg`, `img_039.jpg`) không thuộc taxonomy nên **không gán box phương tiện**. Chỉ gán box `person` cho người điều khiển hoặc hành khách nếu nhận diện rõ.
- **`R-06` (Ngưỡng kích thước tối thiểu)**: Box phải có **chiều cao $\ge$ 20 px** mới gán nhãn độc lập. Đối tượng có chiều cao < 20 px thì bỏ qua, nếu tập trung dày đặc thì gom vào 1 box `ignore_region`.
- **`R-07` (Độ khít và ôm sát phần nhìn thấy)**: Box phải ôm khít phần điểm ảnh thực sự nhìn thấy được (*visible extent*). Tuyệt đối không phỏng đoán phần bị che khuất ngầm dưới đất hoặc sau vật cản khác để phóng to box.
- **`R-08` (Phân loại xe bán tải)**: Pickup thông thường có cabin và thùng hàng gắn liền theo thiết kế pickup, kể cả thùng mở, đang chở hàng hoặc gắn nắp thùng cao (`img_001.jpg`, `img_012.jpg`, `img_028.jpg`, `img_037.jpg`), xếp vào `car`. Chỉ xếp `truck` khi xe có kết cấu xe tải chuyên dụng với thân/thùng chở hàng tách biệt rõ với cabin; mục đích hàng hóa hoặc món hàng đang chở không tự quyết định lớp.

---

## 4. Ca khó và tình huống biên trong 40 ảnh

| Ảnh | Tình huống phát hiện | Mã quy tắc | Quyết định thống nhất của nhóm | Lý do kỹ thuật |
|---|---|---|---|---|
| `img_002.jpg` | Xe tải chở 8 ô tô con trên hai tầng giá đỡ | `R-01` | 1 box `truck` cho xe tải, 8 box `car` cho từng ô tô con trên giá | Nhận diện cả xe vận chuyển và các chướng ngại vật ô tô trên sàn tải |
| `img_004.jpg`, `img_016.jpg`, `img_035.jpg` | Xe ba bánh chở khách tuk-tuk | `R-02` | Gán lớp `tuk_tuk`, người lái gán `person` | Đã bổ sung lớp `tuk_tuk` vào taxonomy v1.0 để phân biệt rõ hình thái |
| `img_005.jpg`, `img_026.jpg` | Người điều khiển xe máy bị che một phần | `R-03` | 1 box `person`, 1 box `motorcycle`, đặt `occluded_level=1` hoặc `2` | Tách biệt người và phương tiện theo chuẩn 2D ADAS |
| `img_006.jpg`, `img_029.jpg`, `img_039.jpg` | Người đi xe đạp, xích lô trên đường | `R-05` | Không gán xe đạp/xích lô; gán box `person` cho người đạp xe | Xe đạp ngoài taxonomy; người đi xe là đối tượng cần bảo vệ (VRU) |
| `img_009.jpg`, `img_031.jpg`, `img_040.jpg` | Xe buýt lớn chở khách lưu thông | `Taxonomy §2.1 (bus)` | Gán lớp `bus` | Đã bổ sung lớp `bus` vào taxonomy v1.0 |
| `img_011.jpg` | Người mặc trang phục hóa trang bên cạnh xe máy | `R-04` | Gán `person` (vì là người thật), xe máy gán `motorcycle` | Trang phục cosplay không biến người thật thành tượng |
| `img_017.jpg` | Tượng đồng người cưỡi ngựa nghệ thuật | `R-04` | Không gán box | Tượng điêu khắc tĩnh, không tham gia giao thông |
| `img_018.jpg` | Chân dung người lớn trên biển quảng cáo | `R-04` | Không gán box | Ảnh 2D trên biển hiệu quảng cáo tĩnh |
| `img_020.jpg` | Xe ô tô phản chiếu qua gương chiếu hậu | `R-04` | Không gán box | Ảnh ảo phản chiếu, không có thực thể vật lý ở hướng nhìn |
| `img_027.jpg` | Mô hình xe bán tải làm tượng trên bệ cao | `R-04` | Không gán box | Tác phẩm trang trí tĩnh ngoài làn đường |
| `img_033.jpg` | Ma-nơ-canh mặc đồ trong tủ kính | `R-04` | Không gán box | Hình nộm tĩnh trong nhà |
| `img_037.jpg` | Xe bán tải gắn nắp thùng cao (`Master 75`) và xe buýt | `R-08`, `Taxonomy §2.1 (bus)` | Xe bán tải gán `car`, xe buýt gán `bus` | Phân loại chuẩn theo hình thái và mục đích sử dụng |
| `img_012.jpg` | Pickup thông thường có thùng mở đang chở hàng | `R-08` | Gán `car`; hàng hóa không làm đổi lớp phương tiện | Phân loại theo kết cấu pickup, nhất quán với định nghĩa `car` |
| `img_038.jpg` | Xe ô tô mô hình đồ chơi trưng bày | `R-04` | Không gán box | Đồ chơi mô hình thu nhỏ, không phải phương tiện thật |

---

## 5. QC và Lịch sử phiên bản

- **Ngưỡng kiểm soát chất lượng (Khóa cứng theo `rules`)**:
  - `min_box_height_px`: 20
  - `iou_thr_large`: 0.85 (cho box $\ge$ 50 px)
  - `iou_thr_small`: 0.70 (cho box < 50 px)
  - `iaa_iou`: 0.85
  - `iaa_class`: 0.95
  - `error_rate_img_max`: 0.02 (tối đa 2% lỗi theo ảnh)
- **Quy trình giải quyết bất đồng**: Mọi bất đồng ở Pha 3 sẽ được đánh dấu `can_review` hoặc ghi vào `image_issues.csv` để đưa vào phiên calibration ở Pha 5.

### Lịch sử thay đổi

| Phiên bản | Ngày | Người sửa | Nội dung thay đổi chính | Căn cứ / Lý do |
|---|---|---|---|---|
| `v0` | 2026-11-16 | Giảng viên | Bản khởi đầu sơ sài (5 lớp + ignore_region) | Cung cấp bài toán gốc |
| `v1.0` | 2026-11-16 | Nhóm 3anhem (101, 102, 103) | - Mở rộng taxonomy thêm 2 lớp: `bus` và `tuk_tuk` (tổng cộng 8 lớp).<br>- Lượng hóa cụ thể các ngưỡng `occluded_level` (0, 1, 2, 3).<br>- Thống nhất quy tắc `R-01` đến `R-08`: gán ô tô con trên xe chở xe, tách người và xe máy thành 2 box, loại bỏ toàn bộ tượng/ma-nơ-canh/quảng cáo/phản chiếu. | Khảo sát 40 ảnh và giải quyết các điểm bất đồng giữa các bản cá nhân 101, 102, 103. |
| `v1.1` | 2026-11-17 | Rà soát AI theo yêu cầu nhóm | Làm rõ tỷ lệ che khuất, sửa ví dụ người thật ở `img_011.jpg`, sửa tham chiếu xe buýt, và giải quyết mâu thuẫn pickup: pickup thông thường luôn là `car`; xe tải chuyên dụng là `truck`. Rà lại các ảnh pickup trên cả lô theo `R-08`. | Đối chiếu ảnh với định nghĩa lớp v1.0; giữ nguyên tập lớp, thuộc tính, schema và mục `rules`. Quyết định hậu kiểm AI; cần người thật xác nhận trước bàn giao Release. |
