========================================================================
   HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH DỰ ÁN THÙNG RÁC THÔNG MINH IOT
   (SMART TRASH BIN PROJECT - NHÓM 15)
========================================================================

ĐỌC KỸ TRƯỚC KHI BẮT ĐẦU:
- Khi giải nén file .rar, vui lòng giải nén vào đường dẫn KHÔNG CÓ DẤU TIẾNG VIỆT
  (Ví dụ: D:\ThungRac15 hoặc C:\ThungRac15).
  Nếu để tên thư mục tiếng Việt có dấu, trình biên dịch C++ sẽ báo lỗi!

------------------------------------------------------------------------
BƯỚC 1: CÁC PHẦN MỀM CẦN CÀI TRƯỚC TRÊN MÁY TÍNH
------------------------------------------------------------------------
1. Phần mềm Visual Studio Code (VSCode).
2. Ngôn ngữ Python (bản 3.8 trở lên, nhớ tích "Add Python to PATH" khi cài).
3. Mở VSCode, vào mục Extensions (Ctrl+Shift+X), cài đặt 2 extension sau:
   - "PlatformIO IDE"
   - "Wokwi Simulator"

------------------------------------------------------------------------
BƯỚC 2: CÁC BƯỚC KHỞI CHẠY HỆ THỐNG
------------------------------------------------------------------------
1. Mở VSCode: Menu File -> Open Folder... -> Chọn thư mục vừa giải nén.
2. Biên dịch code: Nhìn thanh màu xanh ở đáy màn hình VSCode, bấm vào dấu
   tích (✓) để Build firmware. Đợi nó báo [SUCCESS] màu xanh là xong.
3. Chạy mạch mô phỏng:
   - Nhấp vào file "diagram.json" bên cột trái để mở sơ đồ mạch.
   - Bấm phím F1 trên bàn phím, gõ "Wokwi: Start Simulator" rồi ấn Enter.
   - Mạch Wokwi sẽ chạy, đèn sáng, còi bíp một tiếng là kết nối mạng thành công.
4. Bật Server Database:
   - Vào thư mục dự án trên máy tính, nhấp đúp vào file:
     "Chay_Server_Database.bat"
   - Một cửa sổ đen hiện lên báo "Đã kết nối tới trạm Middleware", cứ để
     nó chạy ngầm không tắt đi.
5. Mở Web Quản lý:
   - Nhấp đúp vào file "Giao_Dien_Van_Hanh.html" để mở bằng trình duyệt Web
     (Chrome, Edge, Cốc Cốc...).
   - Đèn xanh lá hiện "Trực tuyến" là hệ thống đã đồng bộ thời gian thực!

------------------------------------------------------------------------
BƯỚC 3: THỬ NGHIỆM TÍNH NĂNG (DEMO CHẤM ĐIỂM)
------------------------------------------------------------------------
- Mở nắp tự động: Trên Wokwi bấm vào cảm biến PIR (Simulate motion) -> Nắp
  mở 3s, Web báo nắp mở, Server ghi nhận.
- Cảnh báo đầy: Kéo thanh cảm biến siêu âm < 5cm -> Còi hú, đèn đỏ sáng,
  Web báo 100% rác đầy khẩn cấp.
- Gửi GPS: Ấn giữ 1 giây nút tròn màu xanh trên Wokwi -> Web hiện nút bấm
  chỉ đường qua Google Maps.
- Điều khiển 2 chiều: Trên Web, chỉnh mốc báo đầy thành 15cm rồi ấn "Áp Dụng"
  -> Kéo rác về 14cm trên Wokwi còi sẽ hú ngay lập tức (chứng minh lệnh từ Web
  đã bay xuống mạch điều khiển).
- Quản lý nhiều thùng: Trên Web, bấm nút "Mô phỏng Thêm Thùng 2 (Demo)" để
  chứng minh tính năng quản lý đa thiết bị.

------------------------------------------------------------------------
BƯỚC 4: XEM DỮ LIỆU ĐÃ LƯU TRỮ (DATABASE)
------------------------------------------------------------------------
Vào lại thư mục dự án, mở file "Lich_Su_Thu_Gom.csv" bằng Microsoft Excel để
xem toàn bộ lịch sử ngày giờ và hành động được lưu lại vĩnh viễn không bị mất.

Xem hướng dẫn chi tiết và hình ảnh tại file: HUONG_DAN_CAI_DAT_VA_CHAY_PROJECT.md
========================================================================
