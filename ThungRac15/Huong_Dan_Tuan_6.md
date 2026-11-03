# HƯỚNG DẪN CHI TIẾT TUẦN 6: XÂY DỰNG TẦNG MIDDLEWARE VÀ DATABASE

Để hoàn thiện kiến trúc 4 tầng chuẩn công nghiệp IoT, chúng ta sẽ chọn phương án **Python Middleware**. 
Lý do: Rất dễ cài đặt, chạy thẳng trên VSCode, và **KHÔNG CẦN sửa lại code ESP32**.

Cơ chế hoạt động: Code Python sẽ chạy ngầm đóng vai trò là "Máy chủ trung gian" (Middleware). Nó sẽ liên tục nghe lén mạng MQTT, nhặt các thông báo quan trọng (như khi rác đầy, mở nắp) và tự động ghi vào một file cơ sở dữ liệu Lich_Su_Thu_Gom.csv (Excel).

## BƯỚC 1: Cài đặt công cụ
1. Bạn đã có sẵn VSCode. Bạn cần chắc chắn máy mình đã cài ngôn ngữ Python. (Nếu chưa cài, hãy lên trang chủ python.org để tải và cài đặt).
2. Mở Terminal trong VSCode (bấm Ctrl + \` hoặc vào menu Terminal -> New Terminal).
3. Gõ lệnh sau để cài thư viện MQTT cho Python:
   pip install paho-mqtt==1.6.1
   *(Nhấn Enter và đợi nó báo Successfully installed)*

## BƯỚC 2: Chạy Server Middleware
1. Trong thư mục ThungRac15, mình đã tạo sẵn cho bạn một file tên là **middleware.py**.
2. Trên màn hình Terminal của VSCode, gõ lệnh sau để khởi động Server:
   python middleware.py
3. Nếu thành công, Terminal sẽ hiện dòng chữ: 
   [*] Đã kết nối tới trạm Middleware...
   [*] Đang lắng nghe dữ liệu từ các thùng rác...

## BƯỚC 3: Demo và Nghiệm thu
Để minh họa cho giáo viên xem hệ thống hoạt động:
1. Chia màn hình: Một bên mở mô phỏng Wokwi, một bên mở Terminal đang chạy con Python.
2. Trên Wokwi: Kéo cảm biến mức rác cho nó đầy, hoặc kích hoạt cảm biến chuyển động để mở nắp.
3. Quan sát Terminal: Lập tức Server Python sẽ báo là đã bắt được dữ liệu và lưu lại.
4. **Kết quả Database:** Bạn nhìn sang cột bên trái của VSCode, sẽ thấy một file mới tự động xuất hiện tên là **Lich_Su_Thu_Gom.csv**. 
5. Mở file CSV đó ra (hoặc mở bằng Excel), giáo viên sẽ thấy toàn bộ lịch sử giờ giấc đổ rác được lưu lại vĩnh viễn dù có tắt máy tính!

## 💡 CÂU HỎI VẤN ĐÁP BẢO VỆ TUẦN 6
**Hỏi:** Hệ thống của em đủ 4 tầng chưa? Các tầng là gì?
**Đáp:** Dạ đủ 4 tầng chuẩn IoT ạ:
1. Tầng Thiết bị (Device Layer): Mạch ESP32 trên Wokwi.
2. Tầng Mạng (Network Layer): Mạng WiFi và giao thức truyền tải MQTT.
3. Tầng Nền tảng (Platform/Middleware): Dùng trạm HiveMQ làm Broker và con Bot Python (middleware.py) làm Server lưu trữ Database (Lich_Su_Thu_Gom.csv).
4. Tầng Ứng dụng (App Layer): Chính là file Web HTML Giao_Dien_Van_Hanh giám sát trực quan ạ.
