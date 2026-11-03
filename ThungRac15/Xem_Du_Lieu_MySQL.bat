@echo off
chcp 65001 >nul
title XEM DU LIEU MYSQL LARAGON - THUNG RAC IOT NHOM 15
echo ====================================================================
echo   TRUY VAN CO SO DU LIEU MYSQL (LARAGON) - DATABASE: thung_rac_db
echo ====================================================================
echo.

if exist "E:\Laragon\laragon\bin\mysql\mysql-8.4.3-winx64\bin\mysql.exe" (
    set "MYSQL_CMD=E:\Laragon\laragon\bin\mysql\mysql-8.4.3-winx64\bin\mysql.exe"
) else (
    set "MYSQL_CMD=mysql"
)

echo [1] BANG TRANG THAI CAC THUNG RAC (tbl_thung_rac):
"%MYSQL_CMD%" -u root -e "USE thung_rac_db; SELECT ma_thung, ten_thung, khoang_cach, phan_tram_rac, dung_luong_pin, che_do, trang_thai_khoa, vi_tri_gps, cap_nhat_lan_cuoi FROM tbl_thung_rac;"

echo.
echo [2] TOP 5 LICH SU DO DAC TELEMETRY (tbl_nhat_ky_telemetry):
"%MYSQL_CMD%" -u root -e "USE thung_rac_db; SELECT id, ma_thung, khoang_cach, phan_tram_rac, pin, che_do, thoi_gian FROM tbl_nhat_ky_telemetry ORDER BY id DESC LIMIT 5;"

echo.
echo [3] TOP 5 LICH SU SU KIEN VA CANH BAO (tbl_su_kien_canh_bao):
"%MYSQL_CMD%" -u root -e "USE thung_rac_db; SELECT id, ma_thung, loai_su_kien, noi_dung, thoi_gian FROM tbl_su_kien_canh_bao ORDER BY id DESC LIMIT 5;"

echo.
pause
