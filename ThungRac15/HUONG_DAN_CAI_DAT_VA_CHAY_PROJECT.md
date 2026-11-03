# 📖 HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH ĐỒ ÁN
## ĐỀ TÀI: HỆ THỐNG THÙNG RÁC THÔNG MINH IOT (SMART TRASH BIN) - NHÓM 15

> **Dành cho:** Bạn học, Giảng viên hoặc Người nhận file nén `.rar` / `.zip` muốn chạy lại toàn bộ hệ thống trên máy tính của mình từ A đến Z.

---

## ⚠️ LƯU Ý SỐNG CÒN TRƯỚC KHI GIẢI NÉN
- **ĐẶT TÊN THƯ MỤC KHÔNG DẤU:** Khi giải nén file `.rar`, hãy giải nén vào đường dẫn **hoàn toàn KHÔNG CÓ DẤU TIẾNG VIỆT** (Ví dụ khuyên dùng: `D:\ThungRac15` hoặc `C:\Projects\ThungRac15`).
- *Lý do:* Trình biên dịch C++ của PlatformIO (`xtensa-esp32-elf-g++`) sẽ bị lỗi fatal error nếu đường dẫn chứa ký tự tiếng Việt có dấu (như `Tài liệu`, `Đồ án`...).

---

## 🛠️ PHẦN 1: CÁC PHẦN MỀM CẦN CÓ TRÊN MÁY TÍNH
Để chạy dự án, máy tính của bạn cần cài đặt sẵn 2 công cụ cơ bản sau:
1. **Visual Studio Code (VSCode):** [Tải tại đây](https://code.visualstudio.com/)
2. **Python (Bản 3.8 trở lên):** [Tải tại đây](https://www.python.org/) *(Khi cài nhớ tích chọn vào ô "Add Python to PATH")*.

### Cài 2 Extension bắt buộc trong VSCode:
Mở VSCode, vào biểu tượng **Extensions (Ctrl + Shift + X)** ở thanh bên trái, tìm và cài đặt:
1. **PlatformIO IDE** (Biểu tượng đầu con kiến ngoài hành tinh - Dùng để quản lý nạp thư viện và biên dịch ESP32).
2. **Wokwi Simulator** (Dùng để chạy mạch mô phỏng phần cứng trực tiếp trong VSCode).

---

## 🚀 PHẦN 2: CÁC BƯỚC KHỞI CHẠY HỆ THỐNG

### Bước 1: Mở thư mục dự án trong VSCode
1. Mở phần mềm **Visual Studio Code**.
2. Chọn menu **File** $\rightarrow$ **Open Folder...**
3. Tìm chọn đúng thư mục dự án đã giải nén (Ví dụ: `D:\ThungRac15`).
4. Đợi khoảng 1-2 phút ở lần đầu tiên mở để PlatformIO tự động tải các gói vi điều khiển ESP32 và thư viện.

### Bước 2: Biên dịch mã nguồn (Build Firmware)
1. Bạn nhìn xuống thanh trạng thái màu xanh dương ở góc dưới cùng màn hình VSCode.
2. Bấm vào biểu tượng **Dấu tích (✓) - PlatformIO: Build**.
3. Đợi vài giây cho đến khi Terminal báo chữ **`[SUCCESS]`** màu xanh lá cây là code đã được dịch sang file nhị phân `firmware.bin` thành công.

### Bước 3: Chạy mạch mô phỏng Wokwi
1. Nhấp chuột vào file **`diagram.json`** ở cột thư mục bên trái để mở sơ đồ mạch điện.
2. Bấm phím **`F1`** (hoặc `Ctrl + Shift + P`) trên bàn phím.
3. Gõ chữ: **`Wokwi: Start Simulator`** rồi ấn **Enter**.
4. Mạch sẽ khởi động: Đèn xanh sáng lên, còi kêu bíp báo hiệu ESP32 đã kết nối Wi-Fi ảo và thông mạng MQTT thành công.

### Bước 4: Bật Máy chủ Cơ sở dữ liệu MySQL Laragon & Middleware Server
1. Mở phần mềm **Laragon** trên máy tính và bấm **`Start All`** (để khởi chạy máy chủ MySQL cổng 3306).
2. Nhấp đúp chuột trái vào file **`Chay_Server_Database.bat`** trong thư mục dự án.
3. Cửa sổ dòng lệnh sẽ kết nối tới HiveMQ và MySQL Laragon (`thung_rac_db`):
   ```text
   [*] Ket noi MySQL Laragon (127.0.0.1:3306) thanh cong!
   [*] Database 'thung_rac_db' san sang nhan du lieu.
   [*] DA KET NOI MQTT BROKER THANH CONG (HiveMQ: broker.hivemq.com:1883)
   [*] Dang lang nghe tat ca thung rac tai topic: doan/nhom15/#
   ```
4. 👉 Bạn có thể mở **HeidiSQL / phpMyAdmin** trong Laragon để xem trực tiếp các bảng `tbl_thung_rac`, `tbl_nhat_ky_telemetry`, `tbl_su_kien_canh_bao`.
5. 👉 Cứ để cửa sổ `Chay_Server_Database.bat` chạy ngầm.

### Bước 5: Mở Giao diện Quản lý (Web Dashboard)
1. Trong thư mục dự án, tìm file **`Giao_Dien_Van_Hanh.html`**.
2. Nhấp đúp chuột vào file này để mở bằng bất kỳ trình duyệt Web nào (Google Chrome, Microsoft Edge, Cốc Cốc...).
3. Quan sát góc trên cùng: Chấm tròn xanh lá hiện **"Trực tuyến (broker.hivemq.com)"** nghĩa là Giao diện đã kết nối thời gian thực với hệ thống!

---

## 🎯 PHẦN 3: KỊCH BẢN THỬ NGHIỆM ĐỂ CHẤM ĐIỂM (DEMO)

Chia đôi màn hình máy tính: **Một bên là VSCode (mạch Wokwi)** và **Một bên là Trình duyệt Web (Dashboard)**:

| Tính năng | Thao tác trên Wokwi | Hiện tượng quan sát được |
| :--- | :--- | :--- |
| **1. Cảm biến Mở nắp tự động** | Click chuột vào cảm biến PIR, chọn *Simulate motion*. | • Động cơ Servo quay 90° mở nắp 3s rồi tự đóng.<br>• Web Dashboard hiện thông báo nắp mở/đóng.<br>• Server Python ghi lại lịch sử vào file Excel. |
| **2. Cảnh báo Rác đầy** | Click vào Cảm biến siêu âm, kéo thanh *Distance* xuống dưới 5cm. | • Còi hú, đèn LED đỏ sáng chớp tắt.<br>• Cột rác trên Web dâng lên 100% màu đỏ rực, hiện chữ "KHẨN CẤP".<br>• Server ghi ngay sự kiện rác đầy vào Database. |
| **3. Định vị vị trí GPS** | Nhấn và giữ 1 giây vào cái Nút bấm tròn màu xanh dương (góc trên phải). | • Web nhận tọa độ và xuất hiện nút **"Định Vị Trên Google Maps"**.<br>• Click vào nút để mở bản đồ thực tế. |
| **4. Điều khiển cấu hình 2 chiều** | Trên Web: nhập số **15** vào ô *Cài Đặt Ngưỡng* $\rightarrow$ bấm **Áp Dụng**. | • Lệnh bay xuyên qua Internet xuống ESP32.<br>• Trên Wokwi kéo rác về 14cm $\rightarrow$ Mạch hú còi ngay lập tức (chứng minh mạch đã đổi mốc theo lệnh từ Web!). |
| **5. Quản lý Đa thiết bị (Multi-bin)** | Trên Web: bấm nút **"Mô phỏng Thêm Thùng 2 (Demo)"** ở góc trên. | • Web tự động đẻ ra thêm Card quản lý Thùng rác #2 (Khu B) với đầy đủ thông số Pin, rác, GPS riêng biệt. |

---

## 📊 XEM KẾT QUẢ DATABASE (FILE EXCEL)
- Sau khi chạy thử nghiệm, bạn vào lại thư mục dự án sẽ thấy file **`Lich_Su_Thu_Gom.csv`**.
- Mở file này bằng **Microsoft Excel** để xem toàn bộ nhật ký ngày giờ (Timestamp), mã thùng rác, và nội dung sự kiện được lưu trữ vĩnh viễn với Tiếng Việt có dấu chuẩn 100%.

---

## ❓ XỬ LÝ LỖI THƯỜNG GẶP (FAQ)
1. **Hỏi:** *Tại sao bấm F5 trên VSCode lại bị lỗi bảng màu cam "Failed to launch GDB"?*
   - **Đáp:** Phím F5 trong VSCode là lệnh gỡ lỗi phần cứng. Để chạy mô phỏng Wokwi, bạn phải bấm **`F1`** $\rightarrow$ chọn **`Wokwi: Start Simulator`**.
2. **Hỏi:** *Tại sao Web báo "Mất kết nối mạng"?*
   - **Đáp:** Đảm bảo máy tính của bạn đang có kết nối Internet bình thường để Web và ESP32 có thể bắt tay nhau qua Cloud Broker `broker.hivemq.com`.
3. **Hỏi:** *File Excel mở lên cột thời gian bị hiện dấu `########`?*
   - **Đáp:** Do cột A trong Excel đang bị hẹp, bạn chỉ cần rê chuột kéo giãn độ rộng của cột A ra là hiển thị ngày giờ đầy đủ.

---
*(Dự án được xây dựng và kiểm thử hoàn chỉnh theo chuẩn Kiến Trúc IoT 4 Tầng - Chúc bạn nghiệm thu đạt kết quả cao nhất!)*
