#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper dung chung cho bo test Vios & Solar.

- bien dich file .c bang gcc
- chay exe voi mot chuoi stdin cho truoc
- cac hook pytest: --student, --check-style

Toan bo thuat toan so sanh nam o cases.py de run_tests.py
dung duoc ke ca khi khong cai pytest.
"""
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from cases import normalize, check_avg, check_case, check_style  # noqa: E402,F401

ROOT = pathlib.Path(__file__).parent.parent
TESTS_DIR = ROOT / "tests"

GCC = shutil.which("gcc") or shutil.which("cc") or "gcc"

# -finput-charset / -fexec-charset bat buoc khi hoc vien go chu co dau
# trong chuoi ky tu. Windows mac dinh la ANSI (cp1252) nen "NGUY HIE"M"
# se bien thanh "NGUY H?M" va khong bao gio khop duoc.
GCC_FLAGS = ["-std=c99", "-O2",
             "-finput-charset=UTF-8", "-fexec-charset=UTF-8"]

# Thu tu thu kiem cac encoding khi doc output.
DECODERS = ["utf-8", "cp1258", "cp1252", "latin-1"]


def compile_c(source_path: str, exe_path: str) -> tuple:
    """Bien dich file C. Tra ve (ok, log)."""
    cmd = [GCC] + GCC_FLAGS + ["-o", exe_path, source_path]
    result = subprocess.run(cmd, capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
    return result.returncode == 0, (result.stdout + result.stderr)


def decode_output(raw: bytes) -> str:
    """
    Doc stdout cua chuong trinh C.

    Khong doan ma encoding mot lan: thoa tu dau, dung encoding dau tien
    giai ma duoc ma khong sinh ky tu thay the (U+FFFD).
    """
    for enc in DECODERS:
        try:
            return raw.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return raw.decode("utf-8", errors="replace")


def run_exe(exe_path: str, stdin_text: str, timeout: int = 5) -> tuple:
    """Chay exe. Tra ve (stdout, stderr, returncode)."""
    try:
        result = subprocess.run([exe_path], input=stdin_text.encode("utf-8"),
                                capture_output=True, timeout=timeout)
        return (decode_output(result.stdout),
                decode_output(result.stderr),
                result.returncode)
    except subprocess.TimeoutExpired:
        return "", "TIMEOUT", -1
    except Exception as e:  # noqa: BLE001
        return "", str(e), -1


def build_exe(source_path: str, out_dir: str = None) -> tuple:
    """
    Bien dich file .c thanh exe trong thu muc tam.
    Tra ve (duong_dan_exe_or_None, log).
    """
    out_dir = out_dir or tempfile.mkdtemp(prefix="ctest_")
    exe_path = os.path.join(out_dir, "bai.exe")
    ok, log = compile_c(source_path, exe_path)
    return (exe_path if ok else None), log


def resolve_student(option_value: str, default_name: str) -> pathlib.Path:
    """Chon file .c can cham: --student neu co, nguoc lai solution mau."""
    if option_value:
        p = pathlib.Path(option_value)
        if not p.is_absolute():
            for base in (ROOT, pathlib.Path.cwd()):
                cand = base / p
                if cand.exists():
                    return cand
        return p
    return ROOT / default_name


# ---------------------------------------------------------------------
#  Hook pytest
# ---------------------------------------------------------------------

def pytest_addoption(parser):
    parser.addoption("--student", action="store", default=None,
                     help="Duong dan file .c cua hoc vien")
    parser.addoption("--check-style", "--style", action="store_true",
                     default=False, dest="check_style",
                     help="Kiem tra them hoc vien co dung for/switch/if "
                          "theo yeu cau cua de bai (mac dinh: KHONG kiem tra)")


def report_compile_error(log: str, source: pathlib.Path) -> str:
    """Chuyen log gcc thanh thong bao de doc cho học viên."""
    return (f"Bien dich that bai: {source}\n"
            f"{'-' * 60}\n{log.strip()}\n{'-' * 60}\n"
            f"Nguyen nhan thuong gap:\n"
            f"  - Thieu #include <stdio.h> hoac <string.h>\n"
            f"  - Ten ham/khai bao khong khop voi trong template\n"
            f"  - Dung ham khong ton tai (clrscr, gotoxy... can conio.h)\n"
            f"  - Thieu return trong ham tra ve gia tri\n"
            f"Kiem tra: {GCC} --version")
