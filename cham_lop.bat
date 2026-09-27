@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

rem "else" phai nam trong block (), neu khong cmd se nuot phan do vao
rem gia tri cua bien.
if "%~1"=="" (
    set "BAINOP=%~dp0bainop"
) else (
    set "BAINOP=%~1"
)
set "KETQUA=%~dp0ket_qua_lop.txt"

echo.
echo ============================================================
echo    CHAM CA LO - luon dung che do CHAM CHIEM (--strict)
echo ============================================================
echo.

if not exist "%BAINOP%\*.c" (
    echo [LOI] Khong tim thay file .c nao trong:
    echo        %BAINOP%
    echo.
    pause
    exit /b 2
)

echo Thu muc: %BAINOP%
echo Dang cham...
echo.

python run_tests.py --batch "%BAINOP%" --strict > "%KETQUA%" 2>&1
type "%KETQUA%"

echo.
echo ============================================================
echo   Ket qua da luu vao: ket_qua_lop.txt
echo   (mo file do de cham diem)
echo ============================================================
echo.

pause
