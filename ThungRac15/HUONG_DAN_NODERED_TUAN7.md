# NODE-RED – TẦNG 3 MIDDLEWARE (TUẦN 5–7)

## Chạy
1. Bật mô phỏng Wokwi như cũ (`F1` → `Wokwi: Start Simulator`). Firmware mới đã build sẵn.
2. Nhấp đúp **`Chay_NodeRED.bat`** (lần đầu mất ~30s để nạp). Cửa sổ đen báo `Started flows` là xong.
3. Mở:
   - Editor (sơ đồ flow): http://localhost:1880
   - Dashboard: http://localhost:1880/ui

> Không dùng chung `Chay_Server_Database.bat` (Python) cùng lúc nếu muốn log không bị trùng — Node-RED đã thay vai trò đó. Giao diện Web HTML cũ vẫn chạy song song được.

> Máy khác tải về: thư mục `nodered/node_modules` rất nặng, có thể xóa trước khi nén. Người nhận chạy `npm install` trong thư mục `nodered` để cài lại (đã có `package.json`).

## Flow làm gì (file `nodered/flows.json` – dùng *Import* để nộp giáo viên)
| Thành phần | Loại | Mô tả |
|---|---|---|
| **RULE 1** Chống tràn | Automation | `khoangcach ≤ ngưỡng` → publish `…/bin1/lock = 1` (ESP32 từ chối mở nắp). Rác đổ đi (`> ngưỡng + 3cm`) → `lock = 0`. Có histeresis 3cm để không khóa/mở liên tục. |
| **RULE 2** ECO ban đêm | Scheduler | Mỗi 30s kiểm tra giờ: 22h–05h → publish `…/bin1/mode = ECO` (ESP32 gửi dữ liệu 30s/lần thay vì 3s). Chỉ gửi khi đổi trạng thái. Công tắc "Ép chế độ ECO" trên Dashboard để demo không cần chờ đêm. |
| **ABNORMAL** Mất tín hiệu | Watchdog | Nếu 20s không có gói tin nào từ một thùng → cảnh báo `MAT TIN HIEU BINx` (toast + log). |
| Ngưỡng từ xa | Command | Ô số trên Dashboard → publish `…/config` (ESP32 đổi ngưỡng như Web HTML). |
| Thống kê | Xử lý | Đếm lượt mở nắp trong ngày. |
| Log | History | Ghi `nodered/logs/Lich_Su_NodeRED_<thời gian khởi động>.csv` (có BOM, mở Excel không lỗi font). |

Topic mới ESP32 lắng nghe: `doan/nhom15/bin1/lock`, `doan/nhom15/bin1/mode`.

## Kịch bản test & bằng chứng (chụp màn hình cho báo cáo Tuần 7)
| # | Thao tác | Kết quả mong đợi | Chụp ở đâu |
|---|---|---|---|
| T1 | Wokwi: kéo siêu âm xuống 3cm | Còi hú; Node-RED log `RULE1_KHOA_NAP`; Terminal Wokwi/Serial: `KHOA NAP` | Dashboard + file CSV |
| T2 | Khi đang khóa, bấm PIR | Nắp **không** mở; Dashboard hiện "Thùng đang khóa (đầy) - từ chối người dùng" | Wokwi (servo đứng yên) + toast |
| T3 | Kéo siêu âm lên 30cm | Log `RULE1_MO_KHOA`; PIR mở nắp được lại | CSV |
| T4 | Bật công tắc "Ép chế độ ECO" | Log `RULE2_ECO`; Dashboard "Che do: ECO"; Web cập nhật dữ liệu chậm còn 30s/lần | Dashboard |
| T5 | Dừng Wokwi, đợi 20s | Toast + log `LOI_MAT_TIN_HIEU` | Dashboard + CSV |
| T6 | Dashboard đặt ngưỡng 15 → kéo siêu âm 12cm | Còi hú ngay (lệnh xuống ESP32) | Wokwi |

Đã kiểm tra tự động T1, T3, T5 và log CSV bằng script giả lập ESP32 (Rule 1 khóa/mở đúng, watchdog bắn sau 20s).
