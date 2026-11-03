# ĐỒ ÁN IOT: HỆ THỐNG THÙNG RÁC THÔNG MINH (SMART TRASH BIN)

> **Môn học:** Internet of Things (IoT)  
> **Repository:** [IOT_NHOM13_THUNGRAC](https://github.com/Duy35P/IOT_NHOM13_THUNGRAC)  
> **Kiến trúc:** 4 tầng (Sensing/Actuation $\rightarrow$ Network/MQTT $\rightarrow$ Middleware & Database $\rightarrow$ Application/Web Dashboard & Node-RED)

---

## 📁 Cấu trúc Thư mục Dự án

```text
IOT_NHOM13_THUNGRAC/
├── ThungRac15/                   # Thư mục chính: Thùng rác #1 + Hệ thống Backend/Frontend/Database
│   ├── src/main.cpp              # Firmware ESP32 Thùng rác #1 (HC-SR04, PIR, Servo, Buzzer, LED)
│   ├── diagram.json              # Sơ đồ mạch mô phỏng Wokwi Thùng rác #1
│   ├── platformio.ini            # Cấu hình PlatformIO cho Thùng rác #1
│   ├── wokwi.toml                # Cấu hình liên kết Wokwi Simulator
│   ├── middleware.py             # Middleware Python (kết nối HiveMQ MQTT, đồng bộ MySQL Laragon)
│   ├── Giao_Dien_Van_Hanh.html   # Dashboard Web giám sát & điều khiển thời gian thực
│   ├── init_mysql_laragon.sql    # Kịch bản khởi tạo Cơ sở dữ liệu MySQL (thung_rac_db)
│   ├── nodered/                  # Cấu hình luồng Node-RED (flows.json, settings.js)
│   ├── Chay_Server_Database.bat  # Script 1-click chạy Middleware + kiểm tra MySQL
│   ├── Chay_NodeRED.bat          # Script 1-click khởi chạy Node-RED
│   ├── Xem_Du_Lieu_MySQL.bat     # Script truy vấn nhanh cơ sở dữ liệu
│   ├── HUONG_DAN_CAI_DAT_VA_CHAY_PROJECT.md # Hướng dẫn chi tiết từng bước
│   ├── Bao_Cao_Chi_Tiet_Kien_Truc_He_Thong_3_Phan.md
│   ├── Bao_Cao_Kiem_Thu_E2E_Tuan_8.md
│   └── ...                       # Báo cáo kịch bản, phân tích OWASP, sơ đồ kiến trúc
│
└── ThungRac15_Bin2/              # Firmware ESP32 Thùng rác #2 (Node phụ độc lập)
    ├── src/main.cpp              # Mã nguồn ESP32 Thùng rác #2 (chủ đề doan/nhom15/bin2/...)
    ├── diagram.json              # Mạch mô phỏng Wokwi Thùng rác #2
    ├── platformio.ini            # Cấu hình nạp/biên dịch Thùng rác #2
    └── wokwi.toml
```

---

## 🚀 Hướng Dẫn Vận Hành Nhanh

### 1. Chuẩn bị Môi trường
* **VS Code** có cài 2 Extension: **PlatformIO IDE** và **Wokwi Simulator**.
* **Python** (3.8 trở lên, đã chọn `Add Python to PATH`). Cài thư viện:
  ```bash
  pip install paho-mqtt mysql-connector-python
  ```
* **Laragon / XAMPP**: Khởi động dịch vụ MySQL (cổng mặc định `3306`, user: `root`, password: trống).
* Nhập cơ sở dữ liệu từ file `ThungRac15/init_mysql_laragon.sql` vào MySQL.

### 2. Khởi chạy Middleware Server
* Mở thư mục `ThungRac15` và nhấp đúp file **`Chay_Server_Database.bat`** (hoặc chạy lệnh `python middleware.py`).
* Server sẽ tự động kết nối Broker HiveMQ (`broker.hivemq.com:1883`) và MySQL Database.

### 3. Khởi chạy Giao diện Giám sát (Dashboard)
* Nhấp đúp mở trực tiếp file **`ThungRac15/Giao_Dien_Van_Hanh.html`** trên trình duyệt (Chrome/Edge).
* Giao diện hỗ trợ theo dõi mức rác %, trạng thái nắp, dung lượng pin, vị trí GPS, lịch sử đổ rác, và điều khiển khóa nắp/chế độ ECO từ xa.

### 4. Khởi chạy Mô phỏng Wokwi
* **Thùng rác #1:** Mở thư mục `ThungRac15` trong VS Code $\rightarrow$ Mở `diagram.json` $\rightarrow$ Nhấn `F1` $\rightarrow$ Gõ `Wokwi: Start Simulator`.
* **Thùng rác #2:** Mở thư mục `ThungRac15_Bin2` trong cửa sổ VS Code mới $\rightarrow$ Mở `diagram.json` $\rightarrow$ Nhấn `F1` $\rightarrow$ Gõ `Wokwi: Start Simulator`.
