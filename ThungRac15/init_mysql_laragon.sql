-- ====================================================================
-- HE THONG THUNG RAC THONG MINH IOT - NHOM 15
-- KHOI TAO DATABASE MYSQL (LARAGON)
-- Host: 127.0.0.1 (localhost) | Port: 3306 | User: root | Password: ""
-- ====================================================================

CREATE DATABASE IF NOT EXISTS `thung_rac_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `thung_rac_db`;

-- 1. Bảng quản lý danh mục và trạng thái hiện tại của các thùng rác
CREATE TABLE IF NOT EXISTS `tbl_thung_rac` (
    `ma_thung` VARCHAR(20) PRIMARY KEY,
    `ten_thung` VARCHAR(100) NOT NULL,
    `vi_tri_gps` VARCHAR(100) DEFAULT 'Lat: 10.8505, Lng: 106.7720',
    `nguong_day` INT DEFAULT 5,
    `dung_luong_pin` INT DEFAULT 100,
    `khoang_cach` FLOAT DEFAULT 40.0,
    `phan_tram_rac` INT DEFAULT 0,
    `che_do` VARCHAR(20) DEFAULT 'NORMAL',
    `trang_thai_khoa` TINYINT(1) DEFAULT 0,
    `trang_thai_ket_noi` VARCHAR(20) DEFAULT 'ONLINE',
    `cap_nhat_lan_cuoi` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Bảng lưu nhật ký đo đạc định kỳ (Telemetry - khoảng cách, % rác, pin)
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

-- 3. Bảng lưu sự kiện, cảnh báo và lịch sử thu gom / kích hoạt rule
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

-- 4. Khởi tạo dữ liệu ban đầu cho 2 thùng rác
INSERT INTO `tbl_thung_rac` (`ma_thung`, `ten_thung`, `vi_tri_gps`, `nguong_day`, `dung_luong_pin`, `khoang_cach`, `phan_tram_rac`, `che_do`, `trang_thai_khoa`, `trang_thai_ket_noi`)
VALUES 
    ('bin1', 'Thùng rác #1 (Khu A - Thư viện)', 'Lat: 10.8505, Lng: 106.7720', 5, 100, 40.0, 0, 'NORMAL', 0, 'ONLINE'),
    ('bin2', 'Thùng rác #2 (Khu B - Ký túc xá)', 'Lat: 10.8512, Lng: 106.7735', 5, 100, 40.0, 0, 'NORMAL', 0, 'ONLINE')
ON DUPLICATE KEY UPDATE `ten_thung` = VALUES(`ten_thung`);
