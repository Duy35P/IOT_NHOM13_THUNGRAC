# 📖 HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY PROJECT TUẦN 7
## ĐỀ TÀI: HỆ THỐNG THÙNG RÁC THÔNG MINH IOT (SMART TRASH BIN) - NHÓM 15
### CHỦ ĐỀ: QUY TẮC NGHIỆP VỤ TỰ ĐỘNG & KỊCH BẢN BẤT THƯỜNG (BUSINESS RULES & ABNORMAL SCENARIOS)

> **Dành cho:** Thành viên trong nhóm, Giảng viên chấm thi hoặc người nhận project muốn chạy toàn bộ hệ thống từ đầu trên máy tính cá nhân.

---

## 🌟 ĐIỂM MỚI VÀ KHÁC BIỆT Ở TUẦN 7
Ở các tuần trước, hệ thống chủ yếu thực hiện truyền nhận telemetry và bật/tắt thủ công. **Ở Tuần 7**, hệ thống đã được tích hợp bộ não điều khiển trung gian:
1. **Nền tảng Node-RED (Tầng 3 Middleware):** Thay thế server Python thủ công, hoạt động như một **Rule Engine** công nghiệp xử lý logic ngầm.
2. **02 Automation Rules tự động hóa:**
   * **Rule 1 - Chống tràn rác tự động:** Tự động phát hiện rác đầy $\rightarrow$ gửi lệnh khóa nắp xuống ESP32 (từ chối mở nắp khi có người đến gần). Tự mở khóa khi rác được đổ sạch.
   * **Rule 2 - Tiết kiệm điện ban đêm (ECO Mode):** Bộ lập lịch (Scheduler) tự động chuyển ESP32 sang chế độ gửi tin chậm (30s/lần) trong khung giờ đêm (22h–05h) để tiết kiệm pin. Có công tắc Override trên Dashboard.
3. **01 Kịch bản lỗi / bất thường (Abnormal Scenario):**
   * **Watchdog Timer (20s):** Tự động phát hiện sự cố mất tín hiệu / mất nguồn / ngắt kết nối ESP32 và bắn thông báo cảnh báo đỏ trên Dashboard + ghi log sự cố.
4. **Hai giao diện trực quan trên Web:**
   * **Flow Editor:** `http://localhost:1880` (Sơ đồ nối dây logic trực quan dạng khối).
   * **Dashboard Vận hành:** `http://localhost:1880/ui` (Màn hình điều khiển, đồng hồ đo, biểu đồ thời gian thực).

---

## 🛠️ PHẦN 1: YÊU CẦU MÔI TRƯỜNG & PHẦN MỀM

1. **Visual Studio Code (VSCode):** Cài sẵn 2 extension:
   * **PlatformIO IDE** (quản lý build firmware ESP32).
   * **Wokwi Simulator** (mô phỏng phần cứng ESP32, Servo, Cảm biến siêu âm, PIR, Buzzer).
2. **Node.js (Bản 18 trở lên):** Kiểm tra bằng cách mở CMD gõ `node -v` và `npm -v`.
3. **Đường dẫn thư mục:** Đặt project trong thư mục **KHÔNG DẤU TIẾNG VIỆT** (Ví dụ khuyên dùng: `D:\ThungRac15`).

---

## 🚀 PHẦN 2: CÁC BƯỚC KHỞI CHẠY HỆ THỐNG TUẦN 7

Thực hiện đúng theo 4 bước tuần tự sau:

### Bước 1: Mở thư mục dự án và Biên dịch Firmware mới
1. Mở VSCode $\rightarrow$ chọn **File** $\rightarrow$ **Open Folder...** $\rightarrow$ chọn thư mục `D:\ThungRac15`.
2. Bấm vào biểu tượng **Dấu tích (✓) - PlatformIO: Build** ở thanh trạng thái màu xanh dưới cùng của VSCode.
3. Chờ Terminal thông báo **`[SUCCESS]`** màu xanh lá cây để đảm bảo firmware mới (đã bổ sung logic nhận lệnh khóa nắp và chế độ ECO) được biên dịch thành công.

### Bước 2: Bật mạch mô phỏng Wokwi
1. Nhấp mở file **`diagram.json`** trong danh mục cây thư mục bên trái của VSCode.
2. Bấm phím **`F1`** (hoặc `Ctrl + Shift + P`) trên bàn phím.
3. Gõ: **`Wokwi: Start Simulator`** và ấn **Enter**.
4. Mạch sẽ chạy: Còi kêu bíp ngắn báo hiệu ESP32 đã kết nối WiFi ảo và kết nối thành công tới MQTT Broker (`broker.hivemq.com`).

### Bước 3: Khởi động Middleware Node-RED (Rule Engine)
1. Mở thư mục dự án `D:\ThungRac15` trong File Explorer của Windows.
2. Nhấp đúp chuột vào file: **`Chay_NodeRED.bat`**.
3. Cửa sổ Command Prompt màu đen sẽ hiện lên. Khi thấy dòng chữ:
   ```text
   Started flows
   Server now running at http://127.0.0.1:1880/
   ```
   $\rightarrow$ **Giữ nguyên cửa sổ đen này chạy ngầm** (không được đóng cửa sổ này trong suốt quá trình demo).

> ⚠️ **LƯU Ý:** Không chạy cùng lúc file `Chay_Server_Database.bat` (Python) cũ để tránh bị ghi trùng lặp dữ liệu vào cơ sở dữ liệu. Node-RED đã đảm nhận hoàn toàn việc xử lý và ghi log.

### Bước 4: Mở giao diện trên trình duyệt Web
Mở trình duyệt Google Chrome hoặc Microsoft Edge và mở 2 tab sau:
1. **Tab 1 - Sơ đồ luồng (Flow Editor):** Truy cập **`http://localhost:1880`**  
   *(Đây là nơi giáo viên xem toàn bộ sơ đồ khối logic, MQTT in/out, Rule 1, Rule 2, Watchdog)*.
2. **Tab 2 - Bảng điều khiển quản lý (Dashboard):** Truy cập **`http://localhost:1880/ui`**  
   *(Nơi xem đồng hồ dung tích rác, đồ thị, trạng thái khóa nắp và nút bấm điều khiển)*.
3. *(Tùy chọn)* Bạn vẫn có thể mở thêm file **`Giao_Dien_Van_Hanh.html`** để xem song song Dashboard HTML của Tuần 6.

---

## 🎯 PHẦN 3: KỊCH BẢN THỰC NGHIỆM ĐỂ DEMO & BẢO VỆ ĐỒ ÁN (TEST CASES)

Chia đôi màn hình máy tính: **Một bên là VSCode (mạch Wokwi)** và **Một bên là Trình duyệt Web (`http://localhost:1880/ui`)**:

| Mã Test | Thao tác thực hiện | Hiện tượng quan sát được | Ý nghĩa kỹ thuật giải thích cho Thầy/Cô |
| :---: | :--- | :--- | :--- |
| **T1: Kích hoạt Khóa nắp tự động (Rule 1)** | Trên Wokwi: Nhấp vào cảm biến siêu âm HC-SR04, kéo thanh trượt khoảng cách xuống dưới ngưỡng (ví dụ: kéo về $3\text{cm}$). | • Còi Buzzer trên Wokwi hú vang báo động.<br>• Terminal Serial in: `=> Node-RED: KHOA NAP (chong tran)`.<br>• Node-RED Dashboard chuyển trạng thái: **"ĐÃ KHÓA NẮP CHỐNG TRÀN"** màu đỏ. | Hệ thống có Middleware tự động phát hiện rác đầy và ra quyết định khóa từ xa, không cần sự can thiệp thủ công của con người. |
| **T2: Từ chối mở nắp khi thùng đầy** | Trong khi thùng đang bị khóa (ở test T1), nhấp vào cảm biến chuyển động PIR trên Wokwi $\rightarrow$ chọn *Simulate motion*. | • Động cơ Servo đứng yên, nắp thùng **KHÔNG MỞ**.<br>• Dashboard hiện thông báo Toast: *"Thùng đang khóa (đầy) - từ chối người dùng"*.<br>• Còi kêu bíp cảnh cáo. | Cơ chế chống tràn: bảo vệ không cho người dân tiếp tục nhét thêm rác khi thùng đã đầy. |
| **T3: Tự động phục hồi trạng thái (Hysteresis)** | Kéo thanh trượt khoảng cách siêu âm ra xa (ví dụ: kéo lên $30\text{cm}$ mô phỏng công nhân vừa dọn rác). | • Node-RED nhận biết mức rác đã an toàn $\rightarrow$ tự gửi lệnh `lock = 0`.<br>• Terminal Serial in: `=> Node-RED: MO KHOA NAP`.<br>• Giờ bấm lại PIR thì Servo mở nắp bình thường. | Tính năng tự phục hồi (Self-healing / Auto-recovery) sau khi dọn rác, có khoảng trễ hysteresis 3cm tránh chập chờn. |
| **T4: Chuyển chế độ ECO tiết kiệm pin (Rule 2)** | Trên Node-RED Dashboard: Gạt bật công tắc **"Ép chế độ ECO"**. | • Node-RED gửi lệnh `mode = ECO`.<br>- Terminal Serial in: `=> Node-RED: Che do ECO (30s/lan)`.<br>• Chu kỳ gửi tin của ESP32 dãn từ 3 giây lên 30 giây một lần. | Quản lý năng lượng thông minh: tự động kích hoạt ban đêm từ 22h-05h để tiết kiệm pin ngoài trời. |
| **T5: Kịch bản lỗi Mất tín hiệu (Watchdog Timer)** | Trên thanh công cụ Wokwi: Bấm nút **Pause / Stop** dừng mô phỏng và đợi đúng $20\text{s}$. | • Đúng sau 20 giây, Node-RED kích hoạt Watchdog.<br>• Dashboard nảy ra thông báo màu đỏ: **"⚠️ MẤT TÍN HIỆU BIN1 (TIMEOUT)"**.<br>• Thẻ trạng thái đổi sang **MẤT KẾT NỐI**. | Kịch bản bất thường (Abnormal Scenario): Tự động phát hiện khi thiết bị gặp sự cố hỏng hóc, hết pin hoặc mất mạng. |
| **T6: Cấu hình ngưỡng từ xa 2 chiều** | Trên Node-RED Dashboard: Nhập ngưỡng rác mới $= 15\text{cm}$ rồi bấm Enter. Sau đó kéo siêu âm Wokwi về $12\text{cm}$. | • ESP32 nhận cấu hình mới.<br>• Mức $12\text{cm}$ trước đây chưa đầy thì nay lập tức bị khóa nắp ngay. | Khả năng điều khiển cấu hình 2 chiều (Bidirectional Downlink Configuration) từ trung tâm xuống thiết bị. |

---

## 📊 PHẦN 4: KIỂM TRA FILE CƠ SỞ DỮ LIỆU (DATABASE)

Mỗi lần Node-RED khởi động và chạy các Rule, hệ thống sẽ tự động ghi nhật ký vào thư mục:
👉 **`D:\ThungRac15\nodered\logs\`**

* Tên file có dạng: **`Lich_Su_NodeRED_<ngày_giờ>.csv`**.
* File này sử dụng chuẩn mã hóa **UTF-8 with BOM**, bạn chỉ cần nhấp đúp chuột là mở thẳng bằng **Microsoft Excel**.
* Toàn bộ tiếng Việt có dấu hiển thị chuẩn 100%, ghi lại đầy đủ các cột:
  * `Thời gian` (Timestamp chính xác từng giây).
  * `Mã thùng` (`bin1`).
  * `Khoảng cách (cm)`.
  * `Mức rác (%)`.
  * `Trạng thái Khóa` (`LOCKED` / `UNLOCKED`).
  * `Chế độ` (`NORMAL` / `ECO`).
  * `Sự kiện` (`RULE1_KHOA_NAP`, `RULE1_MO_KHOA`, `RULE2_ECO`, `LOI_MAT_TIN_HIEU`, ...).

---

## ❓ PHẦN 5: XỬ LÝ LỖI THƯỜNG GẶP (FAQ & TROUBLESHOOTING)

1. **Hỏi:** *Nhấp vào `Chay_NodeRED.bat` nhưng cửa sổ báo lỗi `Port 1880 in use`?*
   * **Khắc phục:** Cổng 1880 đang bị một tiến trình Node-RED cũ chiếm giữ. Mở Task Manager (Ctrl + Shift + Esc), tìm mục **Node.js: Server-side JavaScript** $\rightarrow$ chọn **End Task**, sau đó nhấp lại file `Chay_NodeRED.bat`.

2. **Hỏi:** *Người khác tải file nén `.rar` về máy của họ thì chạy như thế nào?*
   * **Khắc phục:** Người nhận chỉ cần giải nén vào ổ đĩa không dấu (ví dụ `D:\ThungRac15`). Nếu máy họ chưa có thư mục `node_modules` bên trong `nodered`, họ chỉ cần mở CMD tại thư mục `D:\ThungRac15\nodered` và gõ:
     ```cmd
     npm install
     ```
     Sau đó nhấp đúp `Chay_NodeRED.bat` là chạy được ngay lập tức!

3. **Hỏi:** *Trên Dashboard Node-RED báo `Disconnected`?*
   * **Khắc phục:** Kiểm tra máy tính có kết nối Internet không, vì Node-RED cần truy cập Broker công cộng `broker.hivemq.com` để nhận dữ liệu từ Wokwi.
