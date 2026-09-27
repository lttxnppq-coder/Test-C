@echo off
chcp 65001 >nul <nul
setlocal
cd /d "%~dp0"

set "BAINOP=%~dp0bainop"
set "KETQUA=%~dp0ket_qua.txt"

echo.
echo ============================================================
echo    CHAM BAI TU DONG - 2 DE VIOS + SOLAR
echo ============================================================
echo.

rem ---- 1. kiem tra Python ----
rem Them "<nul" o moi lenh kiem tra: neu khong, chung se TU DOC HET
rem stdin, va lenh "set /p" o duoi se khong con gi de doc - nghia la
rem che do cham se tu doi sang mac dinh ma khong hien bao loi gi.
python --version >nul 2>&1 <nul
if errorlevel 1 goto :thieu_python

rem ---- 2. kiem tra gcc ----
gcc --version >nul 2>&1 <nul
if errorlevel 1 goto :thieu_gcc

rem ---- 3. chon che do cham ----
echo Cham theo che do nao?
echo   1. Chi can bai CHAY DUOC  ^- mac dinh, Enter hoac 1
echo   2. Cham CHIEM logic 5 ham ^- kiem ca dung/sai
echo.
set "MODE="
set /p MODE=Chon [1]/[2] ^(Enter = 1^): 
rem So sanh bang findstr de an toan khi doc tu stdin/file
echo %MODE% | findstr /i /b "^2" >nul 2>&1
if %errorlevel% equ 0 (
    set "STRICT=--strict"
    echo   Da chon: cham chiem logic.
) else (
    set "STRICT="
    echo   Da chon: chi kiem tra bai chay duoc.
)

rem ---- 4. co file duoc keo vao khong? ----
rem KHONG dung if (...) o day: ben trong nhon, chuoi "2>^&1" se lam
rem cmd dong nhon sai va bao loi "was unexpected at this time".
if "%~1"=="" goto :khong_keo_file

echo.
echo Cham cac file duoc keo vao...
python run_tests.py %* %STRICT% --ask > "%KETQUA%" 2>&1
goto :xong

:khong_keo_file
if not exist "%BAINOP%\" goto :tao_thu_muc
if not exist "%BAINOP%\*.c" goto :thu_muc_rong

set "COUNT=0"
for /f %%f in ('dir /b /a-d "%BAINOP%\*.c" 2^>nul') do set /a COUNT+=1
echo.
echo Tim thay %COUNT% file .c trong bainop. Dang cham...
echo.
python run_tests.py --batch "%BAINOP%" %STRICT% > "%KETQUA%" 2>&1
goto :xong

:tao_thu_muc
mkdir "%BAINOP%"
echo.
echo [YEU CAU] Da tao thu muc moi:
echo.
echo     %BAINOP%
echo.
echo   Hai cach dua bai vao:
echo     a) Keo file .c cua hoc vien THANG VAO cua so nay
echo     b) Copy file .c vao thu muc bainop\ o tren
echo.
echo   Ten file nen chua "vios" hoac "solar", vi du vios_hoa.c
echo   Neu ten khong ro de, may se hoi ban.
echo.
pause
exit /b 0

:thu_muc_rong
echo.
echo [YEU CAU] Thu muc bainop chua co file .c nao:
echo           %BAINOP%
echo.
echo   Hay keo file .c cua hoc vien vao cham.bat,
echo   hoac copy vao thu muc bainop\ roi chay lai.
echo.
pause
exit /b 0

:xong
rem Khong dung "tee" vi Windows khong co san lenh nay.
rem Khi in ra file, Python tu bo ma mau nen ket_qua.txt mo bang
rem Notepad se doi ra mau chu binh thuong, khong co ky tu dieu khien.
type "%KETQUA%"

echo.
echo ============================================================
echo   Ket qua da luu vao: ket_qua.txt
echo ============================================================
echo.

pause
exit /b 0

:thieu_python
echo.
echo [LOI] Thieu Python.
echo       Double-click "cai_dat.bat" de cai tu dong.
echo.
pause
exit /b 2

:thieu_gcc
echo.
echo [LOI] Thieu trinh bien dich C (gcc).
echo       Double-click "cai_dat.bat" de cai tu dong.
echo.
pause
exit /b 2
