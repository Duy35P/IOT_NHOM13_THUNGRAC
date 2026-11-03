"""
====================================================================
HE THONG THUNG RAC THONG MINH IOT - NHOM 15
MIDDLEWARE SERVER (MQTT -> MYSQL LARAGON + CSV BACKUP)
====================================================================
"""

import sys
import os
import csv
import time
from datetime import datetime

# Dam bao in tieng Viet UTF-8 an toan tren Windows Console
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import pymysql
import paho.mqtt.client as mqtt

# ----------------- CAU HINH MQTT & MYSQL -----------------
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "doan/nhom15/#"

MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "thung_rac_db"

CSV_FILE = "Lich_Su_Thu_Gom.csv"

# Cache trang thai bo nho tam
bins_cache = {
    "bin1": {"nguong": 5, "pin": 100, "mode": "NORMAL", "khoangcach": 40.0, "pct": 0},
    "bin2": {"nguong": 5, "pin": 100, "mode": "NORMAL", "khoangcach": 40.0, "pct": 0}
}

# ----------------- KET NOI MYSQL -----------------
db_conn = None

def get_db_connection():
    global db_conn
    try:
        if db_conn is not None:
            db_conn.ping()
            return db_conn
    except Exception:
        db_conn = None

    try:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            charset="utf8mb4",
            autocommit=True,
            connect_timeout=5
        )
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DB}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            cur.execute(f"USE `{MYSQL_DB}`;")
            # Tao cac bang neu chua co
            cur.execute("""
                CREATE TABLE IF NOT EXISTS `tbl_thung_rac` (
                    `ma_thung` VARCHAR(20) PRIMARY KEY,
                    `ten_thung` VARCHAR(100) NOT NULL,
                    `vi_tri_gps` VARCHAR(100) DEFAULT 'Chua cap nhat',
                    `nguong_day` INT DEFAULT 5,
                    `dung_luong_pin` INT DEFAULT 100,
                    `khoang_cach` FLOAT DEFAULT 40.0,
                    `phan_tram_rac` INT DEFAULT 0,
                    `che_do` VARCHAR(20) DEFAULT 'NORMAL',
                    `trang_thai_khoa` TINYINT(1) DEFAULT 0,
                    `trang_thai_ket_noi` VARCHAR(20) DEFAULT 'ONLINE',
                    `cap_nhat_lan_cuoi` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS `tbl_nhat_ky_telemetry` (
                    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
                    `ma_thung` VARCHAR(20) NOT NULL,
                    `khoang_cach` FLOAT DEFAULT NULL,
                    `phan_tram_rac` INT DEFAULT NULL,
                    `pin` INT DEFAULT NULL,
                    `che_do` VARCHAR(20) DEFAULT 'NORMAL',
                    `thoi_gian` DATETIME DEFAULT CURRENT_TIMESTAMP,
                    INDEX `idx_ma_thung` (`ma_thung`),
                    INDEX `idx_thoi_gian` (`thoi_gian`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS `tbl_su_kien_canh_bao` (
                    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
                    `ma_thung` VARCHAR(20) NOT NULL,
                    `loai_su_kien` VARCHAR(50) NOT NULL,
                    `noi_dung` TEXT NOT NULL,
                    `thoi_gian` DATETIME DEFAULT CURRENT_TIMESTAMP,
                    INDEX `idx_ma_thung_sukien` (`ma_thung`),
                    INDEX `idx_loai_su_kien` (`loai_su_kien`),
                    INDEX `idx_thoi_gian_sukien` (`thoi_gian`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)
            # Khoi tao 2 thung mac dinh
            cur.execute("""
                INSERT INTO `tbl_thung_rac` (`ma_thung`, `ten_thung`, `vi_tri_gps`, `nguong_day`, `dung_luong_pin`)
                VALUES 
                    ('bin1', 'Thùng rác #1 (Khu A - Thư viện)', 'Lat: 10.8505, Lng: 106.7720', 5, 100),
                    ('bin2', 'Thùng rác #2 (Khu B - Ký túc xá)', 'Lat: 10.8512, Lng: 106.7735', 5, 100)
                ON DUPLICATE KEY UPDATE `ma_thung` = `ma_thung`;
            """)
        conn.select_db(MYSQL_DB)
        db_conn = conn
        return db_conn
    except Exception as e:
        print(f"[!] Canh bao loi ket noi MySQL Laragon: {e}")
        return None

# ----------------- KHOI TAO CSV BACKUP -----------------
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(["Thoi_Gian", "Thung_Rac", "Loai_Du_Lieu", "Gia_Tri", "Luu_MySQL"])

def log_csv(time_str, bin_id, data_type, payload, mysql_saved=True):
    try:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow([time_str, bin_id, data_type, payload, "OK" if mysql_saved else "Chua"])
    except Exception as e:
        print(f"[!] Loi ghi CSV backup: {e}")

# ----------------- XU LY DU LIEU VAO MYSQL -----------------
def save_to_mysql(bin_id, data_type, payload, time_str):
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        if bin_id not in bins_cache:
            bins_cache[bin_id] = {"nguong": 5, "pin": 100, "mode": "NORMAL", "khoangcach": 40.0, "pct": 0}

        cache = bins_cache[bin_id]

        with conn.cursor() as cur:
            # 1. KHOANG CACH TELEMETRY
            if data_type == "khoangcach":
                try:
                    d = float(payload)
                    cache["khoangcach"] = d
                    nguong = cache.get("nguong", 5)
                    pct = max(0, min(100, int(round((40 - d) / (40 - nguong) * 100))))
                    cache["pct"] = pct
                    
                    cur.execute("""
                        UPDATE `tbl_thung_rac` 
                        SET `khoang_cach` = %s, `phan_tram_rac` = %s, `trang_thai_ket_noi` = 'ONLINE', `cap_nhat_lan_cuoi` = %s
                        WHERE `ma_thung` = %s;
                    """, (d, pct, time_str, bin_id))

                    cur.execute("""
                        INSERT INTO `tbl_nhat_ky_telemetry` (`ma_thung`, `khoang_cach`, `phan_tram_rac`, `pin`, `che_do`, `thoi_gian`)
                        VALUES (%s, %s, %s, %s, %s, %s);
                    """, (bin_id, d, pct, cache["pin"], cache["mode"], time_str))
                    return True
                except ValueError:
                    pass

            # 2. BATTERY
            elif data_type == "battery":
                try:
                    bat = int(float(payload))
                    cache["pin"] = bat
                    cur.execute("""
                        UPDATE `tbl_thung_rac` 
                        SET `dung_luong_pin` = %s, `trang_thai_ket_noi` = 'ONLINE', `cap_nhat_lan_cuoi` = %s
                        WHERE `ma_thung` = %s;
                    """, (bat, time_str, bin_id))

                    cur.execute("""
                        INSERT INTO `tbl_nhat_ky_telemetry` (`ma_thung`, `pin`, `che_do`, `thoi_gian`)
                        VALUES (%s, %s, %s, %s);
                    """, (bin_id, bat, cache["mode"], time_str))
                    return True
                except ValueError:
                    pass

            # 3. GPS
            elif data_type == "gps":
                cur.execute("""
                    UPDATE `tbl_thung_rac` 
                    SET `vi_tri_gps` = %s, `trang_thai_ket_noi` = 'ONLINE', `cap_nhat_lan_cuoi` = %s
                    WHERE `ma_thung` = %s;
                """, (payload, time_str, bin_id))

                cur.execute("""
                    INSERT INTO `tbl_su_kien_canh_bao` (`ma_thung`, `loai_su_kien`, `noi_dung`, `thoi_gian`)
                    VALUES (%s, 'GPS', %s, %s);
                """, (bin_id, payload, time_str))
                return True

            # 4. CANH BAO
            elif data_type == "canhbao":
                loai = "CANH_BAO"
                if "KHẨN CẤP" in payload or "ĐẦY" in payload or "day" in payload.lower():
                    loai = "CANH_BAO_DAY"
                elif "mở nắp" in payload or "mo nap" in payload.lower():
                    loai = "MO_NAP"
                elif "khóa" in payload or "khoa" in payload.lower():
                    loai = "KHOA_NAP"
                
                cur.execute("""
                    INSERT INTO `tbl_su_kien_canh_bao` (`ma_thung`, `loai_su_kien`, `noi_dung`, `thoi_gian`)
                    VALUES (%s, %s, %s, %s);
                """, (bin_id, loai, payload, time_str))
                return True

            # 5. CONFIG NGUONG
            elif data_type == "config":
                try:
                    n = int(payload)
                    cache["nguong"] = n
                    cur.execute("""
                        UPDATE `tbl_thung_rac` 
                        SET `nguong_day` = %s, `cap_nhat_lan_cuoi` = %s
                        WHERE `ma_thung` = %s;
                    """, (n, time_str, bin_id))

                    cur.execute("""
                        INSERT INTO `tbl_su_kien_canh_bao` (`ma_thung`, `loai_su_kien`, `noi_dung`, `thoi_gian`)
                        VALUES (%s, 'CAU_HINH', %s, %s);
                    """, (bin_id, f"Đặt ngưỡng báo đầy = {n}cm", time_str))
                    return True
                except ValueError:
                    pass

            # 6. CHE DO (MODE)
            elif data_type == "mode":
                cache["mode"] = payload
                cur.execute("""
                    UPDATE `tbl_thung_rac` 
                    SET `che_do` = %s, `cap_nhat_lan_cuoi` = %s
                    WHERE `ma_thung` = %s;
                """, (payload, time_str, bin_id))

                cur.execute("""
                    INSERT INTO `tbl_su_kien_canh_bao` (`ma_thung`, `loai_su_kien`, `noi_dung`, `thoi_gian`)
                    VALUES (%s, 'CHE_DO', %s, %s);
                """, (bin_id, f"Chuyển chế độ hoạt động: {payload}", time_str))
                return True

            # 7. KHOA NAP (LOCK)
            elif data_type == "lock":
                is_lock = 1 if str(payload).strip() == "1" else 0
                cur.execute("""
                    UPDATE `tbl_thung_rac` 
                    SET `trang_thai_khoa` = %s, `cap_nhat_lan_cuoi` = %s
                    WHERE `ma_thung` = %s;
                """, (is_lock, time_str, bin_id))

                cur.execute("""
                    INSERT INTO `tbl_su_kien_canh_bao` (`ma_thung`, `loai_su_kien`, `noi_dung`, `thoi_gian`)
                    VALUES (%s, 'KHOA_NAP', %s, %s);
                """, (bin_id, "Đã khóa nắp chống tràn" if is_lock else "Đã mở khóa nắp", time_str))
                return True

        return True
    except Exception as e:
        print(f"[!] Loi luu vao MySQL: {e}")
        return False

# ----------------- CALLBACK MQTT -----------------
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[*] DA KET NOI MQTT BROKER THANH CONG (HiveMQ: {MQTT_BROKER}:{MQTT_PORT})")
        client.subscribe(MQTT_TOPIC)
        print(f"[*] Dang lang nghe tat ca thung rac tai topic: {MQTT_TOPIC}\n")
    else:
        print(f"[!] Ket noi MQTT that bai! Ma loi: {rc}")

def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload = msg.payload.decode('utf-8', errors='ignore')
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        parts = topic.split('/')
        if len(parts) >= 4:
            bin_id = parts[2].lower()
            data_type = parts[3].lower()

            # Luu vao MySQL
            saved = save_to_mysql(bin_id, data_type, payload, time_now)

            # In console ro rang
            db_tag = "[MySQL OK]" if saved else "[MySQL FAIL]"
            clean_payload = payload.replace('\n', ' ')
            print(f"[{time_now}] {db_tag} {bin_id.upper():<6} | {data_type:<11} : {clean_payload}")

            # Ghi CSV du phong
            log_csv(time_now, bin_id, data_type, clean_payload, saved)
    except Exception as err:
        print(f"[!] Loi xu ly goi tin MQTT: {err}")

# ----------------- MAIN PROGRAM -----------------
if __name__ == "__main__":
    print("=" * 65)
    print("   HE THONG TRUYEN THONG & LUU TRU DATABASE IOT - NHOM 15")
    print(f"   Database : MySQL Laragon ({MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB})")
    print(f"   Broker   : {MQTT_BROKER}:{MQTT_PORT}")
    print("=" * 65)

    # Kiem tra ket noi MySQL ban dau
    test_conn = get_db_connection()
    if test_conn:
        print(f"[*] Ket noi MySQL Laragon ({MYSQL_HOST}:{MYSQL_PORT}) thanh cong!")
        print(f"[*] Database '{MYSQL_DB}' san sang nhan du lieu.")
    else:
        print("[!] CHU Y: Chua ket noi duoc MySQL Laragon (Hay bat Laragon -> Start All).")
        print("[*] Du lieu se duoc luu tam vao CSV va tu dong ket noi lai khi MySQL online.")

    # Khoi tao MQTT Client
    try:
        client = mqtt.Client(client_id="Python_Middleware_MySQL_Nhom15")
    except Exception:
        client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    print("\n[*] Dang ket noi MQTT Broker...")
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[*] Da dung Server Middleware.")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Loi ket noi MQTT: {e}")
