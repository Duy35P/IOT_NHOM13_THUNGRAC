# KỊCH BẢN DEMO TRỰC TIẾP HỆ THỐNG TRONG 3 PHÚT (CHÍNH XÁC TỪNG BƯỚC)
## ĐỀ TÀI: HỆ THỐNG THÙNG RÁC THÔNG MINH IOT (SMART TRASH BIN - NHÓM 15)

---

## 🖥️ CHUẨN BỊ MÀN HÌNH TRƯỚC KHI BẮT ĐẦU (00:00)

Chia đôi màn hình máy tính (tỉ lệ 50 - 50):
* **Nửa màn hình bên Trái:** Cửa sổ **VSCode** mở file `diagram.json` (mạch mô phỏng Wokwi) + mở sẵn bảng **Serial Monitor**.
* **Nửa màn hình bên Phải:** Trình duyệt Web mở sẵn Dashboard vận hành: **`http://localhost:1880/ui`** (hoặc `Giao_Dien_Van_Hanh.html`).
* **Cửa sổ chạy ngầm:** File `Chay_NodeRED.bat` đã bật và đang báo `Started flows`.

---

## ⏱️ DÒNG THỜI GIAN DEMO CHI TIẾT (TỪNG GIÂY)

```
00:00 ──(30s)──> 00:30 ──(50s)──> 01:20 ──(40s)──> 02:00 ──(35s)──> 02:35 ──(25s)──> 03:00
  [GIỚI THIỆU &]    [RULE 1: KHÓA]    [RULE 2: ECO &]    [WATCHDOG 20S:]    [ĐỊNH VỊ GPS &]
  [MỞ NẮP TỰ ĐỘNG]  [CHỐNG TRÀN RÁC]  [CÀI NGƯỠNG ĐỔI]   [BÁO MẤT TÍN HIỆU] [XUẤT FILE CSV]
```

---

### PHÚT THỨ 1: GIỚI THIỆU & TỰ ĐỘNG HÓA CHỐNG TRÀN (00:00 - 01:20)

#### 📍 Bước 1: Giới thiệu hệ sinh thái 3 phần & Mở nắp không chạm (00:00 - 00:30 | 30 giây)
* **Thao tác:** 
  1. Dùng chuột chỉ nhanh vào mạch Wokwi bên trái và Dashboard bên phải.
  2. Trên Wokwi: Nhấp vào cảm biến **PIR** $\rightarrow$ bấm chọn **Simulate motion**.
* **Hiện tượng quan sát được:**
  * Động cơ Servo SG90 quay $90^\circ$ mở nắp thùng, giữ nguyên trong 3 giây rồi tự động đóng về $0^\circ$.
  * Đèn LED Xanh sáng. Dashboard bên phải ghi nhận sự kiện: *"Có người đến gần! Đang mở nắp..."* và tăng bộ đếm lượt người dùng.
* **Lời thoại thuyết trình (Voiceover):**
  > *"Kính thưa Thầy/Cô, hệ thống Thùng rác thông minh Nhóm 15 gồm 3 phần: Part 1 là Node thiết bị ESP32 bên trái; kết nối qua MQTT Broker trung gian; và Part 2 - Part 3 là Middleware Node-RED cùng Web Dashboard bên phải. Đầu tiên, khi người dân tiếp cận, cảm biến PIR phát hiện thân nhiệt, Servo tự động mở nắp $90^\circ$ trong 3 giây rồi đóng kín để ngăn mùi hôi và vi khuẩn."*

---

#### 📍 Bước 2: Kích hoạt Rule 1 - Tự động khóa nắp chống tràn & Từ chối người dùng (00:30 - 01:20 | 50 giây)
* **Thao tác:**
  1. Trên Wokwi: Nhấp vào cảm biến siêu âm **HC-SR04**, kéo thanh trượt khoảng cách xuống **$3\text{cm}$** (mô phỏng rác đầy sát nắp).
  2. Quan sát 3 giây, sau đó nhấp tiếp vào **PIR** $\rightarrow$ chọn **Simulate motion** để thử mở nắp.
  3. Kéo thanh trượt siêu âm lùi về **$30\text{cm}$** (mô phỏng công nhân vừa dọn rác).
* **Hiện tượng quan sát được:**
  * **Khi rác đầy ($3\text{cm}$):** Còi Buzzer hú báo động, đèn LED Đỏ bật sáng. Node-RED Rule 1 lập tức phát hiện $\rightarrow$ bắn lệnh `lock = "1"`. Dashboard đổi sang nhãn đỏ: **"ĐÃ KHÓA NẮP CHỐNG TRÀN"**.
  * **Khi bấm PIR:** Servo hoàn toàn đứng yên, **nắp thùng từ chối mở**. Dashboard hiện cảnh báo Toast: *"Thùng đang khóa (đầy) - từ chối người dùng"*.
  * **Khi dọn rác ($30\text{cm}$):** Hệ thống kích hoạt cơ chế tự phục hồi (*Auto-recovery* có khoảng trễ trễ Hysteresis 3cm), còi tắt, đèn chuyển sang Xanh, nắp mở khóa bình thường.
* **Lời thoại thuyết trình (Voiceover):**
  > *"Điểm đặc biệt ở Part 2 là Rule Engine tự động: Khi rác dâng đầy chạm ngưỡng $5\text{cm}$, server tự động phát lệnh khóa nắp và hú còi. Lúc này, dù người dân có cố tình vẫy tay trước cảm biến PIR thì nắp vẫn khóa chặt để chống tràn rác ra đường phố. Ngay khi nhân viên vệ sinh dọn sạch rác, hệ thống tự động mở khóa và sẵn sàng hoạt động trở lại."*

---

### PHÚT THỨ 2: QUẢN LÝ NĂNG LƯỢNG & ĐIỀU KHIỂN 2 CHIỀU (01:20 - 02:00)

#### 📍 Bước 3: Chế độ ECO ban đêm & Đổi ngưỡng từ xa (01:20 - 02:00 | 40 giây)
* **Thao tác:**
  1. Trên Web Dashboard bên phải: Gạt bật công tắc **"Ép chế độ ECO"**.
  2. Quan sát khung Serial Monitor bên VSCode.
  3. Tại ô nhập **"Cài đặt ngưỡng rác đầy"**, nhập số **`15`** và ấn Enter.
* **Hiện tượng quan sát được:**
  * Terminal Serial của ESP32 in ngay dòng: `=> Node-RED: che do ECO (30s)`.
  * Nhịp gửi tin của ESP32 lập tức dãn ra từ 3 giây lên **30 giây/lần**.
  * ESP32 nhận giá trị ngưỡng mới: `=> Da cap nhat nguong moi: 15`. Kéo khoảng cách về $12\text{cm}$ là hệ thống đã kích hoạt báo động.
* **Lời thoại thuyết trình (Voiceover):**
  > *"Để tối ưu năng lượng ngoài trời, Rule 2 tự động chuyển thùng rác sang chế độ ECO vào khung giờ đêm từ 22h đến 5h sáng, dãn chu kỳ gửi tin từ 3s lên 30s để tiết kiệm pin. Người quản trị cũng có thể điều khiển 2 chiều từ xa, đổi ngưỡng rác đầy từ 5cm lên 15cm trực tiếp trên Web mà không cần nạp lại firmware cho ESP32."*

---

### PHÚT THỨ 3: XỬ LÝ LỖI MẤT MẠNG, ĐỊNH VỊ GPS VÀ CƠ SỞ DỮ LIỆU (02:00 - 03:00)

#### 📍 Bước 4: Kịch bản bất thường - Watchdog Timer 20s phát hiện rớt mạng (02:00 - 02:35 | 35 giây)
* **Thao tác:**
  1. Trên thanh công cụ Wokwi: Nhấp nút **Pause** (Tạm dừng mô phỏng) để giả lập sự cố đứt cáp, mất Wi-Fi hoặc hết pin đột ngột.
  2. Đợi đúng 20 giây và nhìn vào thẻ trạng thái trên Dashboard.
* **Hiện tượng quan sát được:**
  * Đúng sau 20 giây không có tín hiệu nhịp tim, Watchdog Timer của Part 2 hết hạn.
  * Dashboard nảy ra cảnh báo khẩn cấp màu đỏ: **"⚠️ LOI_MAT_TIN_HIEU - THÙNG 1 MẤT KẾT NỐI"**.
* **Lời thoại thuyết trình (Voiceover):**
  > *"Đối với thiết bị IoT thực tế, lỗi mất kết nối là rủi ro lớn nhất. Hệ thống của nhóm tích hợp Watchdog Timer 20 giây: Nếu quá 20 giây không nhận được gói tin keep-alive từ ESP32, server sẽ tự động kích hoạt còi cảnh báo trên Dashboard và đánh dấu thiết bị đã OFFLINE để bảo trì kịp thời."*

---

#### 📍 Bước 5: Định vị GPS bản đồ số & Kiểm tra Database CSV (02:35 - 03:00 | 25 giây)
* **Thao tác:**
  1. Bật lại nút **Resume** trên Wokwi, bấm vào nút **GPS** (hoặc gõ lệnh gửi GPS).
  2. Nhấp vào đường link **Google Maps** trên Dashboard để mở bản đồ dẫn đường.
  3. Mở nhanh file log: `D:\ThungRac15\nodered\logs\Lich_Su_NodeRED_<ngày>.csv` bằng Excel.
* **Hiện tượng quan sát được:**
  * Tọa độ vệ tinh GNSS hiển thị chính xác vị trí thùng rác trên bản đồ Google Maps phục vụ xe thu gom.
  * File Excel mở lên hiển thị 100% tiếng Việt có dấu (UTF-8 BOM), lưu đầy đủ từng giây lịch sử đóng/mở nắp, khóa chống tràn và các cảnh báo lỗi.
* **Lời thoại thuyết trình (Voiceover):**
  > *"Cuối cùng, vị trí thùng rác được định vị qua Module GPS u-blox NEO-6M hiển thị trực tiếp trên Google Maps giúp tài xế tối ưu hóa lộ trình xe gom rác. Mọi sự kiện đều được lưu trữ vĩnh viễn vào cơ sở dữ liệu CSV chuẩn UTF-8 BOM, hỗ trợ mở trực tiếp trên Excel không lỗi font. Nhóm đã hoàn thành trọn vẹn kịch bản demo E2E trong đúng 3 phút. Xin cảm ơn Thầy/Cô!"*

---

## 📋 BẢNG CHECKLIST TỔNG HỢP CHO NGƯỜI THỰC HIỆN DEMO

| Mốc thời gian | Tên phân đoạn | Thao tác chính cần làm | Hiện tượng cần chỉ vào |
|:---:|:---|:---|:---|
| **00:00 - 00:30** | Mở nắp tự động (PIR) | Nhấp PIR $\rightarrow$ *Simulate motion* | Servo quay $90^\circ$ mở 3s, Dashboard hiện người đến |
| **00:30 - 01:20** | Rule 1: Khóa chống tràn | Kéo siêu âm về $3\text{cm}$ $\rightarrow$ bấm lại PIR | Buzzer kêu, đèn đỏ sáng, Dashboard báo KHÓA, nắp từ chối mở |
| **01:20 - 02:00** | Rule 2: ECO & Đổi ngưỡng | Gạt công tắc ECO $\rightarrow$ Nhập ngưỡng mới 15cm | Serial in `che do ECO (30s)`, ESP32 nhận ngưỡng mới |
| **02:00 - 02:35** | Watchdog Timer 20s | Nhấp Pause trên Wokwi $\rightarrow$ đợi 20s | Dashboard hiện cảnh báo đỏ: *MẤT TÍN HIỆU TIMEOUT* |
| **02:35 - 03:00** | GPS & Xuất Excel | Bấm GPS $\rightarrow$ Mở Google Maps & Mở file CSV | Bản đồ dẫn đường hiện lên, File CSV mở bằng Excel chuẩn UTF-8 |
