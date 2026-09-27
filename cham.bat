@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

set "BAINOP=%~dp0bainop"
set "KETQUA=%~dp0ket_qua.txt"

echo.
echo ============================================================
echo    CHAM BAI TU DONG - 2 DE VIOS + SOLAR
echo ============================================================
echo.

rem ---- 1. kiem tra python ----
python --version >nul 2>&1
if errorlevel 1 (
    echo [LOI] Khong tim thay Python trong PATH.
    echo       Cai Python 3.8+ roi bat lai may, hoac them vao PATH.
    echo.
    pause
    exit /b 2
)

rem ---- 2. kiem tra gcc ----
gcc --version >nul 2>&1
if errorlevel 1 (
    echo [LOI] Khong tim thay gcc trong PATH.
    echo       Cai MinGW-w64 / TDM-GCC, hoac MSYS2, roi them vao PATH.
    echo.
    pause
    exit /b 2
)

rem ---- 3. chon che do cham ----
echo Ban muon cham theo che do nao?
echo   1. Chi can bai CHAY DUOC  ^- mac dinh, Enter hoac 1
echo   2. Cham CHIEM logic 5 ham ^- them --strict
echo.
set "MODE="
set /p MODE=Chon [1]/[2] ^(Enter = 1^): 
if "%MODE%"=="2" (
    set "STRICT=--strict"
) else (
    set "STRICT="
)
if "%MODE%"=="" echo Da chon: chi kiem tra bai chay duoc.
if "%MODE%"=="1" echo Da chon: chi kiem tra bai chay duoc.
if "%MODE%"=="2" echo Da chon: cham chiem logic.

rem ---- 4. thu muc bai nop ----
if not exist "%BAINOP%\" (
    mkdir "%BAINOP%"
    echo.
    echo [YEU CAU] Da tao thu muc moi. Hay copy file .c cua hoc vien vao:
    echo.
    echo     %BAINOP%
    echo.
    echo     Ten file nen chua "vios" hoac "solar" de tu doan de bai:
    echo     vi du  vios_hoa.c   solar_phuong.c
    echo.
    pause
    exit /b 0
)

if not exist "%BAINOP%\*.c" (
    echo.
    echo [YEU CAU] Thu muc bainop chua co file .c nao:
    echo           %BAINOP%
    echo.
    pause
    exit /b 0
)

set "COUNT=0"
for /f %%f in ('dir /b /a-d "%BAINOP%\*.c" 2^>nul') do set /a COUNT+=1

echo.
echo Tim thay %COUNT% file .c. Dang cham...
echo.

rem ---- 5. chay test, ghi ra file roi hien thi ----
rem Khong dung "tee" vi Windows khong co san lenh nay.
python run_tests.py --batch "%BAINOP%" %STRICT% > "%KETQUA%" 2>&1
type "%KETQUA%"

echo.
echo ============================================================
echo   Ket qua da luu vao: ket_qua.txt
echo ============================================================
echo.

pause
