# Guideline gán nhãn — v0.1_draft — Thành viên 101

- Phiên bản: v0.1 (Bản cá nhân độc lập Pha 1)
- Ngày: 2026-11-16
- Người viết / duyệt: 101

---

## 1. Mục tiêu

- **Mục đích sử dụng**: Bộ dữ liệu gán nhãn bounding box (2D) trên ảnh đường phố phục vụ huấn luyện mô hình phát hiện đối tượng (Object Detection) cho hệ thống lái xe tự động / hỗ trợ lái xe nâng cao (ADAS) và camera giám sát giao thông đô thị.
- **Rủi ro an toàn**:
  - Nhầm lẫn hoặc bỏ sót người đi bộ / người đi xe máy (vulnerable road users - VRU) có thể dẫn đến tai nạn đâm va nghiêm trọng.
  - Nhầm lẫn giữa các loại phương tiện có kích thước, quán tính và quỹ đạo di chuyển khác nhau (ô tô con vs xe tải/xe buýt) gây sai lệch trong ước lượng khoảng cách và lập quỹ đạo phanh/tránh.
  - Báo động giả (False Positive) từ tượng đá, ma-nơ-canh, biển quảng cáo hoặc hình ảnh phản chiếu trên gương làm hệ thống phanh gấp đột ngột (phantom braking), gây nguy hiểm cho phương tiện phía sau.

---

## 2. Lớp và thuộc tính

### 2.1. Lớp đối tượng (Classes)

Mỗi vật thể thuộc đúng một lớp duy nhất. Nếu vật thể không thuộc bất kỳ lớp hợp lệ nào dưới đây (ví dụ: xe đạp, xích lô, xe động vật kéo, xe nôi em bé): **Không gán box** (trừ trường hợp đám đông không thể tách rời thì dùng `ignore_region`).

| Lớp | Định nghĩa (chuẩn xác) | Ví dụ cụ thể | Phản ví dụ / Dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô con từ 4 đến 9 chỗ ngồi dùng chở người, bao gồm sedan, hatchback, SUV, CUV, xe bán tải (pickup) chở khách thông thường. | Sedan, SUV, crossover, xe bán tải gia đình. | Xe van chở hàng kín, xe tuk-tuk, xe chở ô tô (`truck`). |
| `truck` | Xe tải chở hàng hóa các loại (hạng nhẹ, trung, nặng), xe đầu kéo, xe chuyên dụng công trình, xe bồn, xe lồng chở ô tô con. | Xe tải thùng, xe ben, xe chở xe hai tầng (`img_002.jpg`). | Xe bán tải nhỏ cá nhân (`car`), xe thùng kín chở hàng loại nhỏ (`van`). |
| `van` | Xe ô tô chở người hoặc hàng hóa có thân xe dạng hộp kín đồng nhất một khoang (panel van, minivan thương mại cỡ nhỏ đến vừa). | Xe cứu thương cỡ nhỏ, xe van bưu chính bọc kín, minivan. | Xe SUV lớn (`car`), xe buýt cỡ lớn (`bus`), xe tải thùng rời (`truck`). |
| `motorcycle` | Phương tiện hai bánh (hoặc ba bánh có động cơ cỡ nhỏ gắn kèm thùng hông), bao gồm xe máy, mô tô phân khối lớn, xe tay ga, xe gắn máy điện. | Xe máy số, xe scooter, mô tô thể thao. | Xe đạp điện không có bàn đạp công suất nhỏ (nếu quy chuẩn tách riêng), xe ba bánh chở hàng lớn. |
| `person` | Con người sống thật trong tư thế đi bộ, đứng, ngồi, nằm, chạy, hoặc đang điều khiển / ngồi trên các phương tiện giao thông. | Người đi bộ qua đường, tài xế lái xe máy, hành khách ngồi sau xe máy. | Tượng đồng/tượng đá nhân vật lịch sử (`img_011.jpg`, `img_017.jpg`), ma-nơ-canh trong tiệm (`img_033.jpg`), hình chân dung trên áp phích/biển quảng cáo (`img_018.jpg`). |
| `ignore_region` | Vùng không gian đặc biệt cần bỏ qua: nơi chứa đám đông dính chùm không thể tách rời, hoặc cụm phương tiện/người quá xa mờ (chiều cao < 20 px). Bỏ sót hoặc không gán chi tiết trong vùng này không bị phạt lỗi. | Vùng người/xe phía chân trời mờ đặc, khu chợ đông nghẹt che khuất nhau hoàn toàn. | Từng cá nhân riêng lẻ có thể nhận dạng rõ ràng (phải vẽ box độc lập). |

### 2.2. Thuộc tính (Attributes)

| Tên thuộc tính | Kiểu dữ liệu | Các giá trị cho phép | Ý nghĩa và ngưỡng định lượng cụ thể |
|---|---|---|---|
| `occluded_level` | Select | `0`, `1`, `2`, `3` | **Mức độ che khuất (Occlusion Level)** tính theo diện tích thân vật thể bị che bởi vật cản khác:<br>- `0`: Thấy rõ hoàn toàn (che khuất 0%).<br>- `1`: Che khuất nhẹ (từ 1% đến 30% diện tích).<br>- `2`: Che khuất đáng kể (từ 31% đến 70% diện tích).<br>- `3`: Che khuất nặng (trên 70% diện tích), nhưng vẫn đủ đặc trưng nhận dạng chắc chắn. |
| `truncated` | Select | `no`, `yes` | **Bị cắt mép ảnh (Truncation)**:<br>- `no`: Toàn bộ vật thể nằm trọn vẹn trong khung hình ảnh.<br>- `yes`: Một phần thân vật thể bị cắt ngang bởi 1 trong 4 đường viền biên của bức ảnh. |
| `can_review` | Checkbox | `true`, `false` | **Đánh dấu cần xem xét lại**:<br>- Tick `true` nếu người gán không hoàn toàn tự tin về lớp hoặc ranh giới box, yêu cầu nhóm/reviewer thẩm định lại trong phiên calibration. Mặc định là `false`. |

---

## 3. Quy tắc vẽ bounding box

1. **Phần nhìn thấy (Visible Extent)**:
   - Box chỉ bao quanh phần điểm ảnh thực sự nhìn thấy được của vật thể (visible bounding box). **Tuyệt đối không suy đoán** phần thân xe hay chân người bị che khuất ngầm dưới lòng đất hoặc sau vật cản khác để vẽ box phình to ra.
2. **Độ khít (Tightness)**:
   - Cạnh box phải tiếp xúc sát mép ngoài cùng của vật thể (bánh xe, gương chiếu hậu, mũ bảo hiểm, tay lái...). Không để khoảng trống thừa > 3 px và không cắt xén điểm ảnh của vật thể.
3. **Người điều khiển / ngồi trên xe máy (Motorcycle Rider & Passenger)**:
   - **Tách 2 box riêng biệt**:
     - 1 box `motorcycle` ôm trọn chiếc xe máy (từ lốp trước, đuôi xe, gương lái đến gầm xe).
     - 1 box `person` ôm trọn người ngồi trên xe (từ mũ bảo hiểm/đầu đến bàn chân/gác chân).
     - Phần giao nhau giữa người và xe (ví dụ người ngồi đè lên yên) được bao trong cả hai box. Người lái xe máy gán `occluded_level = 1` hoặc `2` tùy mức bị đầu xe/ghi-đông che.
4. **Xe chở xe (Ví dụ: xe lồng tải chở ô tô con `img_002.jpg`)**:
   - Gán 1 box `truck` lớn bao trọn toàn bộ xe chở hàng (bao gồm cabin và rơ-moóc chuyên dụng).
   - Với các ô tô con nằm trên sàn chở hàng: **Gán từng box `car` riêng biệt** cho mỗi chiếc ô tô nhìn thấy được trên sàn tải (bởi mô hình phát hiện vật cần học được hình thái ô tô trong mọi ngữ cảnh và tránh va chạm).
5. **Tượng, hình vẽ, biển quảng cáo, ma-nơ-canh**:
   - **Không gán box** cho tượng đồng, tượng đá người/ngựa (`img_011.jpg`, `img_017.jpg`), tượng bán tải (`img_027.jpg`).
   - **Không gán box** cho hình người in trên pano/biển quảng cáo (`img_018.jpg`) hoặc ma-nơ-canh trong tiệm (`img_033.jpg`).
6. **Hình ảnh phản chiếu (Reflection)**:
   - **Không gán box** cho hình ảnh phản chiếu người hoặc xe qua gương chiếu hậu (`img_020.jpg`) hay mặt kính cửa sổ.
7. **Ngưỡng kích thước tối thiểu (Min Box Size)**:
   - Chỉ gán box cho các đối tượng có **chiều cao ≥ 20 px** và mắt thường có thể phân biệt được lớp.
   - Đối tượng có chiều cao < 20 px: Bỏ qua (không gán). Nếu đối tượng nhỏ tập trung thành cụm ở hậu cảnh thì gán 1 vùng `ignore_region`.
8. **Xe tự hành / xe ghi hình (Ego Vehicle)**:
   - Nắp capo hoặc một phần thân xe chở camera ở mép đáy màn hình: Không gán box (hoặc gán `ignore_region` nếu che diện tích lớn).

---

## 4. Ca khó và tình huống biên trong 40 ảnh

| Ảnh | Tình huống phát hiện | Rule ID đề xuất | Quyết định của tôi | Lý do kỹ thuật |
|---|---|---|---|---|
| `img_002.jpg` | Xe tải lồng chở 8 chiếc ô tô con trên hai tầng giá đỡ | `R-01` | Gán 1 box `truck` cho xe tải; gán các box `car` riêng cho từng ô tô con trên giá đỡ | Mô hình tự lái cần nhận diện xe tải đang lưu thông, đồng thời cần phát hiện vật thể ô tô con để tránh va chạm hàng hóa nhô ra. |
| `img_004.jpg` | Xe ba bánh chở khách tuk-tuk đặc trưng đường phố | `R-02` | Tạm gán `can_review = true`, đưa ra họp Pha 2 để bổ sung lớp `tuk_tuk` vào taxonomy | v0 không có lớp xe 3 bánh. Gán vào `car` thì sai kích thước động học, gán `motorcycle` thì sai hình thái và độ an toàn. |
| `img_005.jpg` | Người đi bộ và xe máy bị che khuất một phần bởi xe khác | `R-03` | Ôm sát phần nhìn thấy, đặt `occluded_level = 2` | Tuân thủ nguyên tắc không suy đoán phần bị che khuất; ghi nhận đúng mức độ che 31-70%. |
| `img_011.jpg` | Tượng đồng danh nhân đặt tại quảng trường / ven đường | `R-04` | Không gán box `person` | Tượng không phải người thật tham gia giao thông; tránh gây lỗi nhận diện sai và phanh khẩn cấp vô căn cứ. |
| `img_017.jpg` | Tượng người cưỡi ngựa bằng đồng cỡ lớn | `R-04` | Không gán box `person` | Là tác phẩm điêu khắc nghệ thuật tĩnh, không phải con người hay phương tiện lưu thông. |
| `img_018.jpg` | Khuôn mặt người lớn in trên biển quảng cáo ven đường | `R-05` | Không gán box `person` | Hình ảnh 2D trên biển bảng tĩnh, không có hành vi di chuyển của người đi bộ. |
| `img_020.jpg` | Xe ô tô phản chiếu rõ nét qua gương chiếu hậu | `R-06` | Không gán box `car` | Là ảnh ảo qua gương phản xạ, vị trí vật lý không nằm ở hướng quan sát trực tiếp. |
| `img_027.jpg` | Mô hình xe bán tải làm tượng trang trí trên bệ cao | `R-04` | Không gán box `car` | Tượng tĩnh trưng bày trên trụ cao, không di chuyển trên làn đường. |
| `img_033.jpg` | Ma-nơ-canh mặc quần áo đứng trong tủ kính cửa hàng | `R-05` | Không gán box `person` | Là hình nộm tĩnh trong nhà, không phải người tham gia giao thông. |
| `img_035.jpg` | Xe tuk-tuk 3 bánh di chuyển giữa dòng phương tiện | `R-02` | Tạm tick `can_review = true`, đề xuất thêm lớp `tuk_tuk` | Cần biểu diễn nhất quán với `img_004.jpg`. |
| `img_037.jpg` | Xe bán tải gắn nắp thùng hàng cao ngang nóc cabin (`Master 75`) và xe buýt lớn | `R-07` | Bán tải gán `car` (hoặc thảo luận chuyển `van`), xe buýt đề xuất thêm lớp `bus` | Xe buýt quá lớn so với `car`/`van`, cần một lớp `bus` riêng trong Pha 2. |
| `img_038.jpg` | Xe ô tô mô hình đồ chơi trưng bày | `R-08` | Không gán box | Kích thước phi thực tế, không phải phương tiện giao thông. |

---

## 5. QC và phiên bản

- **Ngưỡng chất lượng kỳ vọng**:
  - IoU box lớn (≥ 50 px): ≥ 0.85
  - IoU box nhỏ (< 50 px): ≥ 0.70
  - Độ khớp lớp (Class Agreement): ≥ 0.95
  - Tỉ lệ lỗi tối đa theo ảnh: ≤ 2% (tối đa 0 ảnh sai trên 40 ảnh).
- **Thẩm quyền quyết định ca tranh chấp**:
  - Các ca tick `can_review` hoặc bất đồng ý kiến sẽ do cả nhóm thảo luận tại cuộc họp Pha 2 và Pha 5, người điều phối nhóm (101) tổng hợp và chốt sau khi lấy ý kiến đa số.

### Lịch sử thay đổi

| Phiên bản | Ngày | Người sửa | Nội dung thay đổi | Lý do / Căn cứ |
|---|---|---|---|---|
| v0 | 2026-11-16 | Giảng viên | Bản khởi đầu sơ sài | Cung cấp khung ban đầu |
| v0.1 | 2026-11-16 | 101 | Bổ sung định lượng ngưỡng occlusion, định nghĩa phản ví dụ, quy tắc người đi xe máy, xe chở xe, và bảng 12 ca khó cụ thể | Khảo sát độc lập 40 ảnh tại Pha 1 |
