# Guideline cá nhân

Mỗi thành viên **một file**: `guideline_<mã>.md` (ví dụ `guideline_101.md`).
Đây là bản **đầu tiên** của bạn, viết độc lập ở Pha 1. Không sửa lại sau khi họp nhóm.


BỔ SUNG GUIDELINE – CÁC TRƯỜNG HỢP KHÓ
1. Mục tiêu
Nhãn được sử dụng để huấn luyện mô hình phát hiện người và phương tiện giao thông trên ảnh đường phố, phục vụ các bài toán như camera giám sát giao thông, phân tích mật độ giao thông và xe tự lái. Đối tượng cần gán nhãn bao gồm người và các phương tiện giao thông thực tế xuất hiện trong ảnh, kể cả trường hợp bị che khuất, bị cắt bởi biên ảnh hoặc nằm phía sau vật cản. Chỉ gán nhãn những đối tượng có đủ đặc điểm để nhận diện chính xác, không suy đoán những phần không nhìn thấy.
2. Lớp và thuộc tính
2.1. Danh sách lớp (Class List)
Lớp	Định nghĩa
car	Ô tô con, taxi, SUV, ô tô cá nhân.
truck	Xe tải, xe ben, xe container.
van	Xe thùng kín cỡ nhỏ.
motorcycle	Xe máy, xe mô tô, xe tay ga.
person	Người đi bộ, người lái xe, người ngồi trên xe, người dắt xe.
ignore_region	Vùng không thể gán nhãn chính xác hoặc vùng không cần gán từng đối tượng theo quy định dự án.

2.2. Thuộc tính (Attributes)
Thuộc tính	Giá trị	Ý nghĩa
occluded_level	0, 1, 2, 3	Mức độ bị che khuất: 0 không bị che, 1 bị che ít, 2 bị che nhiều, 3 không đủ khả năng nhận diện rõ.
truncated	no, yes	Đối tượng có bị cắt bởi biên ảnh hay không.
can_review	Tick / Không	Tick khi annotator không chắc chắn, cần người khác kiểm tra lại.

2.3. Quy ước thuộc tính
- occluded_level=0: Đối tượng nhìn thấy rõ toàn bộ.
- occluded_level=1: Đối tượng bị che một phần nhỏ, vẫn nhìn thấy phần lớn.
- occluded_level=2: Đối tượng bị che khuất nhiều nhưng vẫn xác định được class.
- occluded_level=3: Đối tượng không đủ đặc điểm để xác định chắc chắn, cần xem xét lại; không dùng để ép gán nhãn một đối tượng không nhận diện được.
- truncated=no: Đối tượng nằm hoàn toàn trong khung hình.
- truncated=yes: Một phần đối tượng nằm ngoài biên ảnh.
- can_review: Đánh dấu những trường hợp chưa chắc chắn để chuyển sang bước kiểm duyệt.

3. Quy tắc vẽ box
- Gán box cho tất cả người và phương tiện thực tế thuộc danh sách class.
- Bounding box phải ôm sát đối tượng, chỉ bao gồm phần thuộc đối tượng.

Không suy đoán hoặc vẽ phần bị che khuất.



Chọn đúng class và thuộc tính tương ứng.



Người và phương tiện phải có bounding box riêng, kể cả khi người đang lái hoặc ngồi trên xe.



Đối tượng bị che khuất vẫn được gán nhãn nếu đủ đặc điểm nhận diện.



Đối tượng bị cắt bởi biên ảnh vẫn được gán nhãn nếu nhận diện được, chỉ vẽ phần nằm trong ảnh.



Đối tượng vừa bị che vừa bị cắt phải thiết lập cả occluded_level và truncated=yes.



Không gán nhãn bóng đổ, hình phản chiếu, hình ảnh trang trí hoặc vật thể không thuộc danh sách class.



Đối tượng quá nhỏ hoặc quá xa, không đủ khả năng nhận diện thì không gán nhãn.
 - Đối tượng bị che khuất bởi hàng rào, rào chắn hoặc vật cản vẫn được gán nhãn nếu có đủ đặc điểm nhận diện. Chỉ vẽ box phần đối tượng nhìn thấy, không suy đoán phần bị che.

- Đối với phương tiện có vật thể hoặc hàng hóa đặt trên xe, chỉ gán nhãn phương tiện thuộc danh sách class. Không gán nhãn riêng hàng hóa nếu hàng hóa không thuộc danh sách lớp.

- Không gán nhãn đồ chơi, mô hình ô tô hoặc phương tiện mô phỏng nếu mục tiêu dataset là nhận diện phương tiện giao thông thực tế.

- Không gán nhãn hình vẽ, hình in, hình quảng cáo hoặc hình ảnh phương tiện xuất hiện trên biển hiệu, poster, màn hình và các vật dụng trang trí.
4. Ca khó (bổ sung)
4.1. Xe phía sau hàng rào, rào chắn: Xe máy, ô tô hoặc người nằm phía sau hàng rào vẫn được gán nhãn nếu nhận diện được đối tượng. Vẽ box theo phần nhìn thấy, không vẽ bao gồm hàng rào. Nếu hàng rào che khuất nhiều nhưng vẫn xác định được loại phương tiện thì vẫn gán nhãn và chọn occluded_level phù hợp. Nếu không thể xác định đối tượng thì bỏ qua hoặc đánh dấu can_review.

4.2. Xe nhìn qua kính: Phương tiện thật nhìn thấy qua cửa kính, kính cửa sổ hoặc kính chắn gió vẫn được gán nhãn nếu nhận diện được. Trường hợp chỉ nhìn thấy hình phản chiếu của xe trên kính thì không gán nhãn. Nếu kính bị mờ, tối hoặc phản sáng khiến không xác định được phương tiện thì đánh dấu can_review.

4.3. Xe mô hình, ô tô đồ chơi: Không gán nhãn ô tô đồ chơi, xe mô hình, xe điều khiển từ xa hoặc mô hình trưng bày. Chỉ gán nhãn phương tiện giao thông thực tế có khả năng tham gia giao thông.

4.4. Vật thể, hàng hóa trên xe: Không gán nhãn riêng hàng hóa, bao tải, thùng hàng, đồ nội thất hoặc vật dụng được chở trên phương tiện. Chỉ gán nhãn phương tiện vận chuyển. Nếu có người ngồi hoặc đứng trên xe thì vẫn gán nhãn person nếu nhận diện được. Phương tiện khác được chở như hàng hóa trên xe tải không gán nhãn như phương tiện tham gia giao thông.

4.5. Hình tượng, tượng người và tượng phương tiện: Không gán nhãn tượng người, tượng động vật, tượng xe hoặc mô hình trang trí. Không gán nhãn hình vẽ người, hình ảnh ô tô trên poster, biển quảng cáo, tranh ảnh hoặc màn hình điện tử. Chỉ gán nhãn người và phương tiện thực tế.

4.6. Đối tượng bị che khuất một phần: Vẫn gán nhãn nếu nhận diện được đối tượng. Chọn occluded_level tương ứng: 0 không bị che, 1 bị che ít, 2 bị che nhiều, 3 không đủ khả năng xác định rõ đối tượng.

4.7. Đối tượng bị cắt bởi biên ảnh: Nếu người hoặc phương tiện nằm một phần ngoài khung hình, vẫn gán nhãn phần nhìn thấy và chọn truncated=yes. Không tự suy đoán kích thước phần nằm ngoài ảnh.

4.8. Đối tượng vừa bị che vừa bị cắt: Vẫn gán nhãn nếu nhận diện được. Đồng thời thiết lập occluded_level và truncated=yes.

4.9. Nhiều phương tiện chồng lấn: Mỗi phương tiện được vẽ một box riêng nếu xác định được từng đối tượng. Không gộp nhiều xe thành một box. Nếu không thể phân biệt ranh giới giữa các xe thì đánh dấu can_review.

4.10. Đối tượng quá nhỏ hoặc ở xa: Nếu đối tượng quá nhỏ, không đủ đặc điểm để xác định class thì không gán nhãn. Đề xuất thử nghiệm ngưỡng 8–10 px chiều cao box trên ảnh gốc trước khi chốt ngưỡng chính thức.

5. QC và phiên bản (bổ sung)
- Kiểm tra không bỏ sót người và phương tiện thực tế.
- Không gán nhãn mô hình, đồ chơi, tượng hoặc hình ảnh trên biển quảng cáo.
- Không gán nhãn hàng hóa, vật dụng trên xe.
- Không nhầm hình phản chiếu trên kính với phương tiện thật.
- Đối tượng sau hàng rào vẫn phải được xem xét gán nhãn nếu nhận diện được.
- Đối tượng không chắc chắn phải tick can_review.
- Mọi thay đổi quy tắc ảnh hưởng đến nhãn phải cập nhật phiên bản guideline.