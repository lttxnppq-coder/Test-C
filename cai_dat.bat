@echo off
chcp 65001 >nul <nul
setlocal
cd /d "%~dp0"

echo.
echo ============================================================
echo    CAI DAT BO TEST - CHAY 1 LAN DUY NHAT
echo    (Python 3.8+ va trinh bien dich C gcc)
echo ============================================================
echo.

set "THIEU="

python --version >nul 2>&1 <nul
if errorlevel 1 goto :thieu_python
for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo   [co]    %%v
goto :da_kiem_python

:thieu_python
echo   [thieu] Python
set "THIEU=1"

:da_kiem_python
gcc --version >nul 2>&1 <nul
if errorlevel 1 goto :thieu_gcc
echo   [co]    gcc - trinh bien dich C
goto :da_kiem_gcc

:thieu_gcc
echo   [thieu] gcc  (trinh bien dich C)
set "THIEU=1"

:da_kiem_gcc
if "%THIEU%"=="" goto :da_du

echo.
echo   Can cai them mot hoac hai thu ben tren.
echo.

rem ---- co winget khong? "where" ra ngay, khong treo ----
where winget >nul 2>&1
if errorlevel 1 goto :khong_co_winget

echo   Tim thay winget. Bat dau cai, may co the hoi ban dong y.
echo.

python --version >nul 2>&1 <nul
if not errorlevel 1 goto :cai_gcc
echo.
echo   --- Cai Python ---
winget install -e --id Python.Python.3.13

:cai_gcc
gcc --version >nul 2>&1 <nul
if not errorlevel 1 goto :xong_cai
echo.
echo   --- Cai gcc (MinGW-w64) ---
winget install -e --id BrechtSanders.WinLibs.POSIX.UCRT

:xong_cai
echo.
echo ============================================================
echo   Da chay xong lenh cai dat.
echo.
echo   HAY DONG CUA SO NAY VA MO LAI - bat buoc.
echo   Windows chi doc lai PATH o cua so moi moi thay duoc.
echo   Sau do chay lai cai_dat.bat de kiem tra.
echo ============================================================
echo.
pause
exit /b 0

:da_du
echo.
echo ============================================================
echo   DA DU DUNG. Kiem tra xong.
echo   Bay gi chi can keo file .c cua hoc vien vao cham.bat.
echo ============================================================
echo.
pause
exit /b 0

:khong_co_winget
echo.
echo ============================================================
echo   KHONG TIM THAY WINGET
echo.
echo   Cai thu cong theo thu tu:
echo.
echo   1. Python
echo      https://www.python.org/downloads/
echo      Tai ban cai cho Windows. Khi cai, TICK "Add Python to PATH".
echo
echo   2. gcc - trinh bien dich C
echo      https://winlibs.com/
echo      Tai ban Win64 dang UCRT (file .zip), giai nen ra dia C:\mingw64
echo      Sau do them thu muc sau vao PATH:
echo         C:\mingw64\bin
echo
echo   3. Mo lai may roi chay lai cai_dat.bat de kiem tra.
echo ============================================================
echo.
pause
exit /b 2
