# Guideline gán nhãn bounding box — v0 cá nhân (bản nháp)

- **Phiên bản:** v0
- **Ngày:** 2026-11-16
- **Người viết / duyệt:** Chưa điền mã thành viên; bản nháp được tạo theo yêu cầu, cần người gán xác nhận trước khi khóa.
- **Phạm vi khảo sát:** Đã rà soát `img_001.jpg`–`img_040.jpg` trong `data/images/`.
- **Taxonomy:** Giữ nguyên các lớp và thuộc tính trong `submission/taxonomy.json`; chưa đề xuất thêm lớp.

## 1. Mục tiêu

Tạo nhãn bounding box 2D nhất quán cho **người và một số phương tiện đường bộ** để huấn luyện, kiểm tra mô hình phát hiện đối tượng. Nhãn chỉ mô tả vật thể thật nhìn thấy trong ảnh; không suy diễn phần bị che khuất và không gán vật thể ngoài các lớp đã có trong taxonomy. Bộ ảnh có cả cảnh đường phố, bãi đỗ, nhà kho, nơi trưng bày và tình huống đối chứng, nên áp dụng cùng một quy tắc bất kể bối cảnh.

## 2. Lớp và thuộc tính

### Lớp

| Lớp | Định nghĩa | Ví dụ trong bộ ảnh | Phản ví dụ / dễ nhầm |
|---|---|---|---|
| `car` | Ô tô chở người cỡ con: sedan, hatchback, wagon, SUV hoặc xe con có kiểu dáng đặc biệt nhưng là xe thật, nguyên chiếc. | Các xe con trên xe chở xe ở `img_002`; wagon ở `img_024`; xe diễu hành cỡ thật ở `img_019`. | Xe buýt; xe máy; xe mô hình; thân vỏ trưng bày chưa thành xe hoàn chỉnh; xe chỉ xuất hiện trong gương hoặc hình ảnh. |
| `truck` | Xe chở hàng có cabin và thùng/sàn chở hàng, gồm xe tải lớn, xe chở ô tô và pickup. Pickup vẫn là `truck` khi thùng có nắp/camper cap. | Xe chở ô tô ở `img_002`; pickup chở hàng ở `img_012`; pickup ở `img_028` và `img_037`. | Xe buýt; tuk-tuk; xe con; hàng hóa đặt trên xe. Không gán riêng từng kiện hàng. |
| `van` | Xe thương mại nhỏ có khoang chở hàng kín, gắn liền với thân xe; không có thùng hàng riêng biệt phía sau cabin. | Xe giao hàng nhỏ dạng panel van, thân kín liền khối. | Pickup có thùng hở hoặc thùng riêng, kể cả khi phủ nắp (`truck`); xe tải nhỏ có sàn/thùng hàng riêng như `img_036`; xe buýt; xe con. Nếu ảnh không cho thấy rõ cấu tạo khoang, đánh dấu `can_review`. |
| `motorcycle` | Xe cơ giới hai bánh, gồm xe máy và scooter. Một xe máy có sidecar vẫn là **một** đối tượng `motorcycle`; box bao cả xe máy và sidecar gắn liền. | Xe máy trong các cảnh giao thông; xe máy có sidecar ở `img_022`. | Tuk-tuk/auto rickshaw ba bánh; xe đạp; cyclo; người lái xe. |
| `person` | Người thật còn sống, nhìn thấy trong ảnh; người đi bộ, người lái/ngồi trên xe và diễn viên mặc trang phục đều thuộc lớp này. | Người đi xe máy ở `img_005`/`img_026`; người mặc trang phục ở `img_011`; tài xế nhìn thấy ở `img_019`. | Tượng ở `img_017`; hình người trên biển quảng cáo ở `img_018`; ma-nơ-canh ở `img_033`/`img_038`; hình phản chiếu. |
| `ignore_region` | Một vùng cục bộ chứa đối tượng thuộc phạm vi nhưng không thể tách/gán ổn định từng box, hoặc đối tượng quá nhỏ theo ngưỡng bên dưới. Đây là vùng bỏ qua, không phải một vật thể. | Một cụm người/xe chồng lấn đến mức không thể nhận diện từng instance; đối tượng thuộc lớp mục tiêu cao dưới 20 px. | Không dùng để che cả ảnh, che vật ngoài taxonomy, hoặc che đối tượng rõ ràng chỉ vì cảnh đông. |

**Ngoài phạm vi taxonomy:** Không gán box cho xe buýt, tuk-tuk/auto rickshaw ba bánh, xe đạp, cyclo, ngựa, hàng hóa, tượng, đồ chơi, ma-nơ-canh, ảnh in hay phản chiếu. Không ép các vật này vào lớp gần giống nhất. Chỉ dùng `ignore_region` nếu có một cụm đối tượng *thuộc lớp mục tiêu* nhưng không thể tách rõ; không vẽ `ignore_region` quanh vật ngoài phạm vi.

### Thuộc tính

| Thuộc tính | Giá trị và ngưỡng | Cách chọn |
|---|---|---|
| `occluded_level` | `0`: không bị vật khác che; `1`: 1–30% diện tích ước tính bị che; `2`: 31–70%; `3`: trên 70% nhưng vẫn nhận diện chắc chắn. | Ước lượng phần vật thể bị **vật khác che**, không tính phần bị cắt bởi mép ảnh. Nếu không thể nhận diện chắc lớp sau khi bị che, không tự đoán; đánh dấu cần xem lại hoặc ghi vấn đề cấp ảnh nếu không thể tạo box. |
| `truncated` | `no` / `yes` | `yes` chỉ khi vật thể bị biên ảnh cắt mất một phần. Vật bị che bởi người/xe khác nhưng không chạm mép ảnh không phải truncated. |
| `can_review` | tick / không tick | Tick khi còn nghi ngờ hợp lý về lớp, ranh giới box hoặc thuộc tính; ghi rõ lý do/ảnh để reviewer tìm lại. Không tick vật đã được quy tắc loại khỏi taxonomy. |

Đối với `ignore_region`, dùng giá trị mặc định của CVAT cho thuộc tính không áp dụng; nếu vùng được tạo do tình huống chưa thể quyết định, bật `can_review` và ghi nguyên nhân.

## 3. Quy tắc vẽ box

1. Vẽ rectangle trục ngang/dọc ôm sát **phần nhìn thấy** của đúng một đối tượng. Không bao phần bị che, bóng đổ, mặt đường, khoảng trống hoặc vật đang chở. Không đoán hình dáng phần khuất.
2. Vẽ mỗi người và mỗi phương tiện thành box riêng. Người lái/ngồi trên xe có box `person`; xe có box lớp xe tương ứng. Chỉ vẽ người khi có bằng chứng nhìn thấy người thật, không vẽ theo suy đoán từ chiếc xe.
3. Trên xe chở xe, vẽ box cho xe tải/chở xe và cho từng ô tô thật, nguyên chiếc, nhìn thấy đủ để nhận dạng riêng (`img_002`). Không gộp xe chở với xe hàng; không gán box cho khung chằng buộc hay hàng hóa. Thân vỏ trưng bày rời trên nóc xe ở `img_024` không phải một xe hoàn chỉnh để gán thêm.
4. Đối tượng chạm biên ảnh vẫn được gán nếu phần nhìn thấy đủ để xác định lớp; box ôm phần thấy được và đặt `truncated=yes`. Nếu chỉ còn một mảnh không đủ xác định lớp, không suy diễn; ghi vấn đề để reviewer xem.
5. Che khuất và nhòe ảnh không tự động làm mất nhãn. Vẫn gán khi có thể nhận diện lớp và phần nhìn thấy; đặt mức `occluded_level` theo tỷ lệ che. Với nhòe chuyển động như `img_014`, nếu không chắc đó là người/vật lớp nào thì không đoán và bật cờ review/ghi vấn đề.
6. **Ngưỡng kích thước:** box đối tượng mục tiêu cao từ 20 px trở lên thì gán box bình thường. Đối tượng mục tiêu cao dưới 20 px không gán box riêng; gộp vùng cục bộ bằng `ignore_region`. Không dùng vùng này để phủ các đối tượng lớn, rõ nét ở gần đó.
7. Trong đám đông/bãi xe, gán từng người hoặc xe nếu còn tách được đường bao. Chỉ dùng một `ignore_region` nhỏ quanh cụm thực sự không thể phân tách; không dùng một box cho cả đám đông như thể đó là một người hay một xe.
8. Vật thật nhìn qua cửa kính vẫn được gán nếu phân biệt được với phản chiếu. Vật chỉ nhìn thấy trong gương, mặt kính phản chiếu, ảnh in, biển quảng cáo, tượng, ma-nơ-canh và đồ chơi không được gán (`img_017`, `img_018`, `img_020`, `img_027`, `img_033`, `img_038`).
9. Xe không thuộc lớp nào trong taxonomy thì bỏ qua, không tạo lớp mới trong bản v0. Nếu tình huống đó lặp lại hoặc ảnh hưởng đáng kể đến mục tiêu mô hình, ghi thành điểm cần thảo luận khi hợp nhất guideline.

## 4. Ca khó đã thấy trong 40 ảnh

| Ảnh | Tình huống | Rule ID | Quyết định ban đầu | Lý do / điểm cần kiểm tra |
|---|---|---|---|---|
| `img_002.jpg` | Xe tải chở nhiều ô tô trên hai tầng | R-01 | Một box `truck` cho xe chở; một box `car` cho từng xe con nhìn thấy rõ. | Các xe là các instance riêng, không gộp vào box xe tải. |
| `img_004.jpg`, `img_016.jpg`, `img_035.jpg` | Tuk-tuk/auto rickshaw ba bánh, một số chở hàng quá khổ | R-02 | Không ép vào `motorcycle` hay `truck`; chỉ gán người thật nhìn thấy nếu đủ kích thước. | Taxonomy hiện không có lớp xe ba bánh này; hàng hóa không thuộc lớp. Đưa đề xuất mở lớp ra họp nhóm. |
| `img_005.jpg`, `img_026.jpg`, `img_040.jpg` | Một hoặc nhiều người ngồi trên xe máy, có che khuất | R-03 | Box riêng cho từng người nhìn thấy và một box `motorcycle` cho mỗi xe. | Không gộp người với xe; đặt occlusion theo từng box. |
| `img_006.jpg`, `img_023.jpg`, `img_029.jpg`, `img_039.jpg` | Xe đạp/cyclo cùng người tham gia giao thông | R-04 | Không gán box cho xe đạp/cyclo; gán riêng người thật nhìn thấy. | Các loại xe này ngoài taxonomy, không phải `motorcycle`. |
| `img_009.jpg`, `img_032.jpg` | Xe buýt trong cảnh giao thông | R-05 | Không gán xe buýt; gán người nếu có thể tách và đạt ngưỡng. | Không có lớp bus; không ép thành `truck`. |
| `img_011.jpg` | Người mặc trang phục hóa trang bên cạnh xe máy | R-06 | Gán `person` nếu là người thật; gán riêng các xe máy đủ rõ. | Trang phục không làm người thật thành tượng/đạo cụ. |
| `img_014.jpg` | Người đi bộ và xe trong cảnh nhòe chuyển động | R-07 | Gán những người/xe còn nhận dạng chắc chắn; đánh dấu review nếu không chắc. | Không vẽ box dựa trên vệt nhòe không thể phân lớp. |
| `img_017.jpg`, `img_027.jpg` | Tượng người và tượng pickup | R-08 | Không gán tượng thành `person`/`truck`. | Hình dáng giống vật thể mục tiêu nhưng không phải vật thật đang hoạt động. |
| `img_018.jpg`, `img_033.jpg`, `img_038.jpg` | Người trên biển quảng cáo, ma-nơ-canh, xe đồ chơi | R-09 | Không gán hình in, ma-nơ-canh hay đồ chơi. | Loại các hình/đồ vật mô phỏng để tránh false positive. |
| `img_019.jpg` | Xe cỡ thật trong đoàn diễu hành và người ngồi trên xe | R-10 | Gán xe là `car`, gán riêng người thật nhìn thấy. | Kiểu dáng hoạt hình không làm mất tư cách xe thật cỡ đầy đủ; phân biệt với xe mô hình nhỏ. |
| `img_020.jpg` | Xe chỉ nhìn thấy trong gương chiếu hậu | R-11 | Không gán các xe trong ảnh phản chiếu. | Tránh coi ảnh phản chiếu là instance vật thể trong cảnh. |
| `img_022.jpg` | Xe máy có sidecar | R-12 | Một box `motorcycle` ôm xe máy và sidecar gắn liền. | Sidecar là bộ phận của tổ hợp xe máy, không phải xe thứ hai. |
| `img_024.jpg` | Nhiều xe thật trong nơi trưng bày; thân vỏ xe đặt trên nóc | R-13 | Gán từng xe thật, nguyên chiếc nhìn thấy; bỏ thân vỏ rời trên nóc. | Bối cảnh trưng bày không tự loại xe thật; thân vỏ rời không phải xe hoàn chỉnh. |
| `img_028.jpg` | Pickup có ngựa ở thùng | R-14 | Gán pickup là `truck`; ngựa ngoài phạm vi. | Không gán động vật hoặc hàng trên xe. |
| `img_030.jpg` | Bãi xe máy dày, nhiều xe chồng lấn | R-15 | Box từng xe còn tách được; `ignore_region` chỉ quanh cụm không thể tách. | Không bỏ cả vùng nếu các xe riêng vẫn nhìn rõ. |
| `img_036.jpg`, `img_037.jpg` | Xe tải nhỏ có thùng riêng và pickup có nắp thùng | R-16 | Cả hai là `truck`: `img_036` có thùng hàng riêng; `img_037` vẫn là pickup dù có camper cap. | `van` dành cho xe có khoang hàng kín liền thân; nếu cấu tạo không phân biệt được ở ảnh khác thì tick `can_review`. |

## 5. QC và phiên bản

- Trước khi gán, rà toàn bộ 40 ảnh và áp dụng cùng quy tắc trên; không thêm lớp hoặc tự đổi định nghĩa giữa chừng.
- Giữ nguyên ngưỡng cố định trong `submission/taxonomy.json`: chiều cao box tối thiểu 20 px; ghép box IAA tại IoU `0.5`; ngưỡng IoU `0.85` cho vật cao từ 50 px và `0.7` cho vật nhỏ hơn; IAA đạt khi IoU trung bình `>= 0.85` và đồng thuận lớp `>= 95%`; tỷ lệ ảnh lỗi tối đa `2%`. Đây là ngưỡng QC của bài lab, không thay thế quy tắc phân lớp/vẽ box.
- Box không chắc phải bật `can_review`; tình huống không thể tạo box thì ghi tên ảnh, vùng và lý do vào bảng vấn đề cấp ảnh theo quy trình của nhóm.
- Nếu đổi quyết định làm thay đổi đối tượng được chọn, lớp, kích thước box hoặc thuộc tính thì tăng phiên bản và ghi lại lý do/ảnh liên quan. Bản này là đề xuất v0 cá nhân, chưa phải guideline nhóm và chưa qua calibration.

| Phiên bản | Thay đổi | Lý do / ca tham chiếu |
|---|---|---|
| v0 | Viết quy tắc ban đầu cho các lớp, box, thuộc tính và ca biên sau khi rà soát 40 ảnh. | `img_002`, `img_004`, `img_014`, `img_017`, `img_019`, `img_020`, `img_022`, `img_024`, `img_027`, `img_030`, `img_035`, `img_037`, cùng các nhóm ca liệt kê ở Mục 4. |
