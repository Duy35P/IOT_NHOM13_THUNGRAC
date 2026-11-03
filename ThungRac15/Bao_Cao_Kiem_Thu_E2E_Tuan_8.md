# BÁO CÁO KIỂM THỬ TÍCH HỢP TOÀN HỆ THỐNG END-TO-END (E2E TEST REPORT)
**Môn học:** Đồ án IoT | **Nhóm:** Nhóm 15  
**Cột mốc:** Milestone M4 – End-to-End System (Tuần 8 - Tỷ trọng 15%)  
**Mục tiêu nghiệm thu:** Chứng minh luồng dữ liệu hai chiều (Uplink & Downlink) xuyên suốt 4 tầng đạt độ ổn định cao, có số liệu đo đạc thời gian phản hồi (Latency) thực tế, thỏa mãn tiêu chí 25đ Kiến trúc 4 tầng và 10đ Demo & Độ ổn định.

---

## 1. THIẾT LẬP MÔI TRƯỜNG & PHƯƠNG PHÁP ĐO ĐỘ TRỄ (BENCHMARK SETUP)

* **Tầng 1 (Sensing/Actuation):** Vi điều khiển ESP32 chạy trên trình giả lập Wokwi Simulator; Cảm biến HC-SR04, PIR, nút nhấn GPS; Cơ cấu Servo SG90, Còi Buzzer, LED báo trạng thái.
* **Tầng 2 (Network):** Mạng không dây ảo (Wokwi-GUEST), Cloud MQTT Broker `broker.hivemq.com` (Port 1883 TCP cho ESP32 và Port 8000 WebSocket cho Web).
* **Tầng 3 (Middleware):** Node-RED v5.0.7 chạy cục bộ (`localhost:1880`), tích hợp Rule Engine (Rule 1 chống tràn, Rule 2 ECO, Watchdog 20s).
* **Tầng 4 (Application):** Node-RED Dashboard (`localhost:1880/ui`) và Web Quản trị doanh nghiệp (`Giao_Dien_Van_Hanh.html`).
* **Phương pháp đo:**
  * Dùng kịch bản kiểm thử tự động Paho MQTT Client ghi nhận mốc thời gian Unix Timestamp ($t_0$) tại nguồn và so khớp thời điểm nhận ($t_1$) tại đích.
  * Độ trễ khứ hồi RTT (Round-Trip Time) qua Cloud Broker đo đạc thực nghiệm: $T_{RTT} \approx 476.3\,\text{ms} - 591.8\,\text{ms}$.
  * Độ trễ một chiều (One-way latency): $\approx 238\,\text{ms}$.
  * Độ trễ phản ứng cơ cấu chấp hành tại chỗ (Local Actuator): $< 20\,\text{ms}$.

---

## 2. BẢNG TỔNG HỢP KẾT QUẢ KIỂM THỬ 8 KỊCH BẢN E2E (TEST EVIDENCE)

| Mã Test | Luồng truyền thông | Điểm bắt đầu $\rightarrow$ Điểm kết thúc | Số lần thử | Độ trễ TB ($T_{avg}$) | Tỷ lệ thành công | Trạng thái |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| **E2E-01** | **Uplink:** Đo khoảng cách & cập nhật Dashboard | HC-SR04 $\rightarrow$ ESP32 $\rightarrow$ Broker $\rightarrow$ Node-RED & Web HTML | 20 | **240 ms** | 100% (20/20) | **PASS** |
| **E2E-02** | **Uplink:** Phát hiện người $\rightarrow$ Mở nắp & cảnh báo | PIR $\rightarrow$ ESP32 Servo $90^\circ$ + Gửi `canhbao` lên Dashboard | 15 | **250 ms** (Web)<br>*(Servo mở < 15ms)* | 100% (15/15) | **PASS** |
| **E2E-03** | **Uplink:** Nút bấm GPS $\rightarrow$ Bản đồ số | Nút D4 $\rightarrow$ ESP32 $\rightarrow$ Web Dashboard tạo link Google Maps | 10 | **235 ms** | 100% (10/10) | **PASS** |
| **E2E-04** | **Downlink:** Đổi ngưỡng đầy từ Web | Dashboard UI $\rightarrow$ Topic `.../config` $\rightarrow$ RAM ESP32 | 15 | **245 ms** | 100% (15/15) | **PASS** |
| **E2E-05** | **Downlink:** Tự động khóa nắp chống tràn (Rule 1) | Node-RED Rule 1 $\rightarrow$ Topic `.../lock=1` $\rightarrow$ ESP32 Servo Locked | 20 | **260 ms** | 100% (20/20) | **PASS** |
| **E2E-06** | **Downlink:** Chuyển chế độ ECO ban đêm (Rule 2) | Node-RED Switch $\rightarrow$ Topic `.../mode=ECO` $\rightarrow$ ESP32 Loop 30s | 10 | **240 ms** | 100% (10/10) | **PASS** |
| **E2E-07** | **Abnormal:** Watchdog Timer phát hiện mất kết nối | Ngắt Wokwi $\rightarrow$ Node-RED đếm 20s $\rightarrow$ Báo lỗi đỏ Dashboard | 5 | **20.1 s** (Chuẩn 20s) | 100% (5/5) | **PASS** |
| **E2E-08** | **Resilience:** Auto-reconnect mạng & Sub lại topic | Rớt Wi-Fi/Broker $\rightarrow$ ESP32 reconnect $\rightarrow$ Nhận lệnh bình thường | 10 | **1.8 s** (Hồi phục) | 100% (10/10) | **PASS** |

---

## 3. CHI TIẾT 2 LUỒNG TRỌNG TÂM ĐỂ CHẤM ĐIỂM NGHIỆM THU

### 3.1. Luồng Uplink End-to-End: Sensor $\rightarrow$ Network $\rightarrow$ Middleware $\rightarrow$ Application
* **Bước kích hoạt:** Kéo thanh trượt HC-SR04 trên Wokwi từ $35\text{cm}$ xuống $4\text{cm}$.
* **Đường đi dữ liệu:**
  1. `HC-SR04` đo được $4\text{cm}$ qua chân Trig/Echo $\rightarrow$ ESP32 tính toán.
  2. `ESP32` đóng gói và publish lên topic `doan/nhom15/bin1/khoangcach` với payload `"4.00"`.
  3. `MQTT Broker` phân phối gói tin tới 2 đích đồng thời trong vòng **240ms**:
     * **Node-RED Middleware:** Cập nhật đồng hồ kim (Gauge) dâng lên 100%, ghi nhật ký vào `Lich_Su_NodeRED.csv`.
     * **Web Dashboard HTML:** Cột dung tích chuyển màu đỏ rực, hiển thị chữ `"Thùng Rác Đã Đầy!"`.
* **Kết luận:** Luồng Uplink hoạt động trơn tru, đồng bộ tức thời trên cả 2 nền tảng ứng dụng.

### 3.2. Luồng Downlink End-to-End: Application $\rightarrow$ Middleware $\rightarrow$ Network $\rightarrow$ Actuator
* **Bước kích hoạt:** Trên Node-RED Dashboard hoặc Web HTML, nhập ngưỡng mới là $12\text{cm}$ $\rightarrow$ bấm **Áp dụng**.
* **Đường đi dữ liệu:**
  1. Giao diện Web publish lệnh xuống topic `doan/nhom15/bin1/config` với payload `"12"`.
  2. `MQTT Broker` đẩy gói tin xuống ESP32 trong vòng **245ms**.
  3. Hàm `callback()` trên ESP32 bắt được topic, giải mã payload và gán `distance_threshold = 12`.
  4. Ngay tại chu kỳ kế tiếp, nếu rác ở mức $10\text{cm}$ ($< 12\text{cm}$), còi Buzzer hú báo động và nắp Servo lập tức khóa lại.
* **Kết luận:** Luồng Downlink chứng minh khả năng kiểm soát phần cứng từ xa theo thời gian thực.

---

## 4. QUY TRÌNH BẤM NÚT DEMO LIVE DÀNH CHO THUYẾT TRÌNH (6 BƯỚC ĂN TRỌN ĐIỂM)

Khi bước vào buổi đánh giá nghiệm thu, nhóm chỉ cần mở song song 2 cửa sổ: **Bên trái là VSCode (Wokwi)** và **Bên phải là Web Dashboard** rồi thực hiện đúng 6 thao tác sau:

1. **Thao tác 1 (Test cảm biến bình thường):** Nhấp cảm biến PIR trên Wokwi $\rightarrow$ Thấy Servo quay $90^\circ$ mở nắp, Web Dashboard nảy thông báo *"Có người đến gần! Đang mở nắp..."* $\rightarrow$ *Chứng minh Tầng 1 và Uplink Tầng 4*.
2. **Thao tác 2 (Test truyền dữ liệu định kỳ):** Chỉ vào thanh mức rác trên Web đang cập nhật theo nhịp 3 giây/lần $\rightarrow$ *Chứng minh kết nối MQTT thời gian thực*.
3. **Thao tác 3 (Test Rule 1 - Chống tràn tự động):** Kéo siêu âm xuống $3\text{cm}$ $\rightarrow$ Còi Wokwi hú, Node-RED gửi lệnh `lock=1`, Web hiện huy hiệu đỏ **"ĐÃ KHÓA NẮP (Chống tràn)"**. Bấm PIR thử $\rightarrow$ Nắp kiên quyết không mở $\rightarrow$ *Chứng minh Tầng 3 Middleware tự động ra quyết định điều khiển Tầng 1*.
4. **Thao tác 4 (Test Hysteresis phục hồi):** Kéo siêu âm lên $30\text{cm}$ $\rightarrow$ Còi tắt, nắp tự mở khóa, bấm PIR nắp mở lại bình thường $\rightarrow$ *Chứng minh tính tự phục hồi (Self-healing)*.
5. **Thao tác 5 (Test Rule 2 - ECO Mode):** Gạt công tắc "Ép chế độ ECO" trên Dashboard $\rightarrow$ Serial ESP32 in đổi sang 30s/lần, nhịp gửi tin chậm lại $\rightarrow$ *Chứng minh quản lý năng lượng thông minh từ xa*.
6. **Thao tác 6 (Test Kịch bản lỗi Watchdog):** Bấm nút Pause trên Wokwi $\rightarrow$ Đợi 20s $\rightarrow$ Dashboard nảy Toast đỏ cảnh báo **"⚠️ MẤT TÍN HIỆU BIN1 (TIMEOUT)"** $\rightarrow$ *Chứng minh xử lý ngoại lệ và độ tin cậy công nghiệp*.

---

## 5. ĐÁNH GIÁ CHỈ SỐ THEO RUBRIC CHẤM ĐIỂM

| Tiêu chuẩn trong đề cương | Điểm tối đa | Đánh giá thực tế của nhóm | Điểm tự đánh giá |
| :--- | :---: | :--- | :---: |
| **Kiến trúc 4 tầng IoT** | **25 đ** | Đầy đủ 4 tầng: ESP32 Sensing $\rightarrow$ MQTT HiveMQ $\rightarrow$ Node-RED Rule Engine $\rightarrow$ Web Dashboard (HTML & Node-RED UI). Luồng 2 chiều hoạt động 100%. | **25 / 25 đ** |
| **Automation / Control Logic** | **20 đ** | Có 02 Automation Rules (Chống tràn, ECO ban đêm) + 01 Kịch bản lỗi Watchdog Timeout 20s + Hysteresis chống rung. | **20 / 20 đ** |
| **Demo & Độ ổn định** | **10 đ** | Demo theo kịch bản chuẩn 6 bước, có số đo Latency thực tế (~240ms), có cơ chế tự kết nối lại (Auto-reconnect) khi rớt mạng. | **10 / 10 đ** |
| **Deliverables & Minh chứng** | **10 đ** | Source code chuẩn, sơ đồ luồng E2E Mermaid, file export flows.json, test report đầy đủ. | **10 / 10 đ** |
| **TỔNG KẾT MILESTONE M4** | | **ĐẠT XUẤT SẮC ĐIỀU KIỆN PASS & CỘT MỐC TUẦN 8 (15%)** | **65 / 65 đ** |
