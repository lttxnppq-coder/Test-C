#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Danh sach test case + toan bo thuat toan cham.

File nay KHONG import pytest, de run_tests.py dung duoc
ke ca khi may chua cai pytest. tests/conftest.py import
tu file nay (khong import nguoc lai).

Cau truc mot case:
    id          : ten case, hien len report
    stdin       : chuong trinh duoc chay voi input nay
    expects     : list tu khoa BAT BUOC phai xuat hien trong stdout
    not_expects : list tu khoa KHONG DUOC xuat hien trong stdout
    avg         : gia tri trung binh 4 banh / 4 chuoi, hoac None
    desc        : case nay danh loi gi (tieng Viet, doc trong TEST_CASES.md)

Tinh trung binh chi duoc doc tu DONG co chu "trung binh".
Ly do khong quet ca output: input duoc in ra boi chinh chuong trinh,
nen case "50 50 50 50" (avg = 50) se khop vo lan voi gia tri input da in
va assert tro thanh vo nghia.
"""

import re
import unicodedata

EPS = 0.06

# =====================================================================
#  DE VIOS - Giam sat ECU Toyota Vios 2007
#  Thu tu stdin: tocDoXe  nhietDoDongCo  cheDoLai  banh0 banh1 banh2 banh3
#  (7 so, tach bang space hoac xuong dong deu duoc)
# =====================================================================

VIOS_CASES = [
    {
        "id": "01_normal_an_toan",
        "stdin": "60\n85\n1\n40 41 40 42\n",
        "expects": ["normal", "eco", "an toan", "binh thuong"],
        "not_expects": ["nguy hiem", "overheat", "high", "qua toc"],
        "avg": 40.75,
        "desc": "Nhiet do 85 <= 90 -> NORMAL, che do 1 -> ECO, khong qua toc. "
                "Dung mode 1 (ECO) de chu 'normal' chi co the den tu ham 1.",
    },
    {
        "id": "02_bien_90_normal",
        "stdin": "50\n90\n1\n50 52 48 50\n",
        "expects": ["normal", "eco", "an toan"],
        "not_expects": ["overheat", "high", "nguy hiem", "qua toc"],
        "avg": 50.0,
        "desc": "Bien 90.0 DUNG phai la NORMAL (bat buoc <=, khong phai <).",
    },
    {
        "id": "03_bien_90_1_high",
        "stdin": "50\n90.1\n1\n50 52 48 50\n",
        "expects": ["high", "eco"],
        "not_expects": ["normal", "overheat", "nguy hiem"],
        "avg": 50.0,
        "desc": "Vua vuot 90 -> HIGH. Bat loi viet < thay <=.",
    },
    {
        "id": "04_bien_105_high",
        "stdin": "50\n105\n3\n50 52 48 50\n",
        "expects": ["high", "sport"],
        "not_expects": ["overheat", "normal", "eco", "nguy hiem"],
        "avg": 50.0,
        "desc": "Bien 105.0 van HIGH, mode 3 -> SPORT.",
    },
    {
        "id": "05_bien_105_1_overheat",
        "stdin": "50\n105.1\n2\n50 52 48 50\n",
        "expects": ["overheat", "normal", "nguy hiem"],
        "not_expects": ["an toan", "high"],
        "avg": 50.0,
        "desc": "Vuot 105 -> OVERHEAT, ham 5 phai tra NGUY HIEM vi nhiet do.",
    },
    {
        "id": "06_qua_toc_index1",
        "stdin": "80\n80\n2\n40 121 40 40\n",
        "expects": ["normal", "qua toc", "nguy hiem"],
        "not_expects": ["an toan", "overheat", "eco", "sport"],
        "avg": 60.25,
        "desc": "Chi banh index 1 vuot 120. Bat loi for chi duyet index 0.",
    },
    {
        "id": "07_bien_120_an_toan",
        "stdin": "80\n80\n2\n118 119 120 120\n",
        "expects": ["normal", "an toan", "binh thuong"],
        "not_expects": ["nguy hiem", "qua toc", "overheat"],
        "avg": 119.25,
        "desc": "Dung 120.0 KHONG lai qua toc (bat buoc >, khong phai >=).",
    },
    {
        "id": "08_bien_120_1_nguyhiem",
        "stdin": "80\n80\n2\n120.1 100 100 100\n",
        "expects": ["qua toc", "nguy hiem"],
        "not_expects": ["an toan", "binh thuong"],
        "avg": 105.025,
        "desc": "120.1 vuot nguong o index 0 -> qua toc + NGUY HIEM.",
    },
    {
        "id": "09_qua_toc_index3",
        "stdin": "80\n80\n2\n40 40 40 121\n",
        "expects": ["qua toc", "nguy hiem"],
        "not_expects": ["an toan", "binh thuong"],
        "avg": 60.25,
        "desc": "QUAN TRONG: banh index 3 vuot 120. Bat loi for(i=0;i<3;i++) "
                "- de bai yeu cau duyet DU 4 phan tu.",
    },
    # Luu y: 4 case nay dung nhiet do 100 (=> HIGH) de con tu khoa "normal"
    # trong not_expects chi tro ve TEN CHE DO, khong bi trung voi trang
    # thai nhiet do "NORMAL" (ma 80C cung ra NORMAL).
    {
        "id": "10_drive_eco",
        "stdin": "60\n100\n1\n40 42 38 40\n",
        "expects": ["eco", "high", "an toan"],
        "not_expects": ["normal", "sport", "nguy hiem", "overheat"],
        "avg": 40.0,
        "desc": "Che do lai 1 -> ECO (switch case 1).",
    },
    {
        "id": "11_drive_sport",
        "stdin": "60\n100\n3\n40 42 38 40\n",
        "expects": ["sport", "high", "an toan"],
        "not_expects": ["eco", "normal", "nguy hiem", "overheat"],
        "avg": 40.0,
        "desc": "Che do lai 3 -> SPORT (switch case 3).",
    },
    {
        "id": "12_drive_default_99",
        "stdin": "60\n100\n99\n40 42 38 40\n",
        "expects": ["normal", "high", "an toan"],
        "not_expects": ["eco", "sport", "nguy hiem", "overheat"],
        "avg": 40.0,
        "desc": "Mode 99 -> default -> NORMAL.",
    },
    {
        "id": "13_drive_default_0",
        "stdin": "60\n100\n0\n40 42 38 40\n",
        "expects": ["normal", "high", "an toan"],
        "not_expects": ["eco", "sport", "nguy hiem", "overheat"],
        "avg": 40.0,
        "desc": "Mode 0 -> default -> NORMAL (nguon de: drivers_vios/test_ham2).",
    },
    {
        "id": "14_combo_full",
        "stdin": "180\n110\n3\n130 125 121 119\n",
        "expects": ["overheat", "sport", "qua toc", "nguy hiem"],
        "not_expects": ["an toan", "binh thuong", "eco"],
        "avg": 123.75,
        "desc": "Combo: nhiet > 105 + SPORT + vuot 120 o ca index 0, 1, 2.",
    },
    {
        "id": "15_input_mot_dong",
        "stdin": "60 85 1 40 41 40 42\n",
        "expects": ["normal", "eco", "an toan"],
        "not_expects": ["nguy hiem", "overheat"],
        "avg": 40.75,
        "desc": "7 so tren MOT DONG. Phai dung scanf de khong phu thuoc "
                "so dong (nhet ca du lieu vao mot bien khong duoc).",
    },
    {
        "id": "16_input_thieu",
        "stdin": "50\n85\n2\n40\n",
        "expects": [],
        "not_expects": ["an toan", "nguy hiem", "overheat", "qua toc"],
        "avg": None,
        "desc": "Thieu du lieu. Chuong trinh phai dung lai, KHONG duoc in "
                "ket luan tren bien gia tri chua khoi tao.",
    },
]

# =====================================================================
#  DE SOLAR - Tram Dien Mat Troi Ap Mai
#  Thu tu stdin: congSuat  nhietDoPin  cheDo  dienAp0 dienAp1 dienAp2 dienAp3
# =====================================================================

SOLAR_CASES = [
    {
        "id": "01_optimal_an_toan",
        "stdin": "50.5\n40\n2\n380.2 381.5 379.8 382.0\n",
        "expects": ["optimal", "grid tied", "an toan", "binh thuong"],
        "not_expects": ["nguy hiem", "critical heat", "qua ap", "high temp"],
        "avg": 380.875,
        "desc": "Pin 40 < 45 -> OPTIMAL, mode 2 -> GRID-TIED, khong qua ap.",
    },
    {
        "id": "02_bien_45_high_temp",
        "stdin": "50\n45\n1\n402 400 398 400\n",
        "expects": ["high temp", "off grid", "an toan"],
        "not_expects": ["optimal", "critical heat", "nguy hiem", "qua ap"],
        "avg": 400.0,
        "desc": "Bien 45.0 phai la HIGH_TEMP. De noi <45, KHONG phai <=45. "
                "Day la loi sai hay gap nhat cua bai nay.",
    },
    {
        "id": "03_bien_65_high_temp",
        "stdin": "50\n65\n3\n402 400 398 400\n",
        "expects": ["high temp", "hybrid", "an toan"],
        "not_expects": ["critical heat", "optimal", "nguy hiem"],
        "avg": 400.0,
        "desc": "Bien 65.0 van HIGH_TEMP, mode 3 -> HYBRID.",
    },
    {
        "id": "04_bien_65_1_critical",
        "stdin": "50\n65.1\n2\n402 400 398 400\n",
        "expects": ["critical heat", "grid tied", "nguy hiem"],
        "not_expects": ["an toan", "high temp", "optimal", "qua ap"],
        "avg": 400.0,
        "desc": "Vuot 65 -> CRITICAL_HEAT, ham 5 phai tra NGUY HIEM vi nhiet do.",
    },
    {
        "id": "05_qua_ap_mau_slide",
        "stdin": "50\n40\n2\n420.5 418.0 425.2 455.0\n",
        "expects": ["optimal", "qua ap", "nguy hiem"],
        "not_expects": ["an toan", "binh thuong"],
        "avg": 429.675,
        "desc": "Vi du trong slide: V_avg = 429.675. Chuoi 455 nam o index 3 "
                "nen case nay cung bat loi for(i=0;i<3;i++) o ham 4.",
    },
    {
        "id": "06_bien_450_an_toan",
        "stdin": "50\n40\n2\n450 450 450 450\n",
        "expects": ["optimal", "grid tied", "an toan", "binh thuong"],
        "not_expects": ["nguy hiem", "qua ap", "critical heat"],
        "avg": 450.0,
        "desc": "Dung 450.0 KHONG lai qua ap (bat buoc >, khong phai >=).",
    },
    {
        "id": "07_bien_450_1_nguyhiem",
        "stdin": "50\n40\n2\n450.1 400 400 400\n",
        "expects": ["qua ap", "nguy hiem"],
        "not_expects": ["an toan", "binh thuong"],
        "avg": 412.525,
        "desc": "450.1 vuot nguong o index 0 -> qua ap + NGUY HIEM.",
    },
    {
        "id": "08_inverter_fault",
        "stdin": "50\n40\n4\n402 400 398 400\n",
        "expects": ["fault", "an toan"],
        "not_expects": ["off grid", "grid tied", "hybrid", "nguy hiem"],
        "avg": 400.0,
        "desc": "Mode 4 -> FAULT. Nhiet do va dien ap binh thuong nen van "
                "AN TOAN: de chi bat NGUY HIEM khi CRITICAL_HEAT hoac qua ap.",
    },
    {
        "id": "09_inverter_offgrid",
        "stdin": "50\n40\n1\n402 400 398 400\n",
        "expects": ["off grid", "an toan"],
        "not_expects": ["grid tied", "hybrid", "fault", "nguy hiem"],
        "avg": 400.0,
        "desc": "Che do inverter 1 -> OFF-GRID.",
    },
    {
        "id": "10_inverter_hybrid",
        "stdin": "50\n40\n3\n402 400 398 400\n",
        "expects": ["hybrid", "an toan"],
        "not_expects": ["off grid", "grid tied", "fault", "nguy hiem"],
        "avg": 400.0,
        "desc": "Che do inverter 3 -> HYBRID.",
    },
    {
        "id": "11_inverter_default_99",
        "stdin": "50\n40\n99\n402 400 398 400\n",
        "expects": ["fault", "an toan"],
        "not_expects": ["off grid", "grid tied", "hybrid", "nguy hiem"],
        "avg": 400.0,
        "desc": "QUAN TRONG: mode 99 -> default -> FAULT. Loi hay gap nhat la "
                "copy cau 'default: return \"NORMAL\"' tu bai Vios sang bai nay.",
    },
    {
        "id": "12_inverter_default_0",
        "stdin": "50\n40\n0\n402 400 398 400\n",
        "expects": ["fault", "an toan"],
        "not_expects": ["off grid", "grid tied", "hybrid", "nguy hiem"],
        "avg": 400.0,
        "desc": "Mode 0 -> default -> FAULT (nguon de: drivers_solar/test_ham2).",
    },
    {
        "id": "13_combo_full",
        "stdin": "60\n70\n4\n460 470 400 400\n",
        "expects": ["critical heat", "fault", "qua ap", "nguy hiem"],
        "not_expects": ["an toan", "binh thuong", "optimal", "high temp"],
        "avg": 432.5,
        "desc": "Combo: pin > 65 + FAULT + 2 chuoi vuot 450V.",
    },
    {
        "id": "14_input_mot_dong",
        "stdin": "50.5 40 2 420.5 418.0 425.2 455.0\n",
        "expects": ["optimal", "grid tied", "qua ap", "nguy hiem"],
        "not_expects": ["an toan", "binh thuong"],
        "avg": 429.675,
        "desc": "7 so tren MOT DONG. Phai dung scanf de khong phu thuc so dong.",
    },
    {
        "id": "15_temp_44_9",
        "stdin": "50\n44.9\n2\n402 400 398 400\n",
        "expects": ["optimal", "grid tied", "an toan"],
        "not_expects": ["high temp", "critical heat", "nguy hiem"],
        "avg": 400.0,
        "desc": "44.9 van OPTIMAL (nguon de: drivers_solar/test_ham1).",
    },
    {
        "id": "16_input_thieu",
        "stdin": "50\n40\n2\n400\n",
        "expects": [],
        "not_expects": ["an toan", "nguy hiem", "qua ap", "critical heat"],
        "avg": None,
        "desc": "Thieu du lieu. Chuong trinh phai dung lai, KHONG duoc in "
                "ket luan tren bien gia tri chua khoi tao.",
    },
]

# Cac test doc lap: do chinh xac cua phep chia trung binh.
# Tach rieng vi khac muc y so voi danh sach case chinh.
EXTRA_CASES = {
    "vios": [
        {
            "id": "avg_chinh_xac",
            "stdin": "60\n80\n2\n40.5 41.0 40.0 40.8\n",
            "avg": 40.575,
            "desc": "Do chinh xac cua phep chia trung binh (3 chu so thap phan).",
        }
    ],
    "solar": [
        {
            "id": "avg_chinh_xac",
            "stdin": "50\n40\n2\n431.5 428.25 435.0 447.25\n",
            "avg": 435.5,
            "desc": "Do chinh xac cua phep chia trung binh (3 chu so thap phan).",
        }
    ],
}

# De bai yeu cau dung cac cu phap nay. Kiem tra nay TAT MAT DINH,
# bat bang co so --check-style / --style
STYLE_RULES = [
    ("co_for", r"\bfor\s*\(", "De bai yeu cau vong lap for (duyet 4 banh / 4 chuoi)."),
    ("co_switch", r"\bswitch\s*\(", "De bai yeu cau switch/case de lay ten che do."),
    ("co_if_else", r"\bif\s*\(", "De bai yeu cau if/else if/else de danh gia nhiet do."),
]

SUITES = {
    "vios": {
        "title": "DE VIOS (Toyota Vios 2007)",
        "solution": "vios_solution.c",
        "cases": VIOS_CASES,
    },
    "solar": {
        "title": "DE SOLAR (Tram Dien Mat Troi)",
        "solution": "solar_solution.c",
        "cases": SOLAR_CASES,
    },
}

# =====================================================================
#  Thuat toan chuan hoa output
# =====================================================================

def normalize(s: str) -> str:
    """
    Chuan hoa chuoi output de so sanh tu khoa linh hoat.

    Vi du: "Trang thai nhiet do: OVERHEAT" -> "trang thai nhiet do overheat"
          "NGUY HIỂM!!!"                 -> "nguy hiem"
          "GRID-TIED"                    -> "grid tied"

    Buoc 1: lower()
    Buoc 2: tach thanh phan (NFD) va bo combining marks -> bo dau tieng Viet
    Buoc 3: 'đ' -> 'd'  (U+0111 khong tach thanh phan duoc)
    Buoc 4: moi ky tu khong phai [a-z0-9] thanh mot dau cach
    Buoc 5: gom nhieu dau cach lien tiep thanh mot
    """
    if not s:
        return ""
    s = s.lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("\u0111", "d")  # đ
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def word_present(haystack_norm: str, needle_norm: str) -> bool:
    """
    Kiem tra tu khoa co xuat hien trong output da chuan hoa hay khong.

    Khoa hon substring thuong: co bien tu. Vi du 'qua ap' se KHONG khop
    voi 'qua ap lao' - tranh bao loi o nhung case ma output dai hon
    mong doi.
    """
    if not needle_norm:
        return True
    pattern = r"(?<![a-z0-9])" + re.escape(needle_norm) + r"(?![a-z0-9])"
    return re.search(pattern, haystack_norm) is not None


def check_avg(expected, stdout: str, eps: float = EPS) -> str:
    """
    Kiem tra gia tri trung binh. CHI doc dong co chu 'trung binh'.

    Tra ve None neu dung, nguoc lai tra ve chuoi mo ta loi.
    Neu khong tim thay dong do -> bao loi ro rang thay vi quet ca output,
    vi quet ca output se khop nham voi cac so input da duoc in ra.
    """
    target = [ln for ln in stdout.splitlines() if "trung binh" in normalize(ln)]
    if not target:
        return ("Khong tim thay dong nao co chu 'trung binh' trong output. "
                "Hay in gia tri trung binh dung theo template, vi du: "
                "'Van toc trung binh 4 banh: 40.75 km/h'.")
    nums = []
    for line in target:
        # Gia tri trung binh nam sau dau ':' trong template
        # ("Van toc trung binh 4 banh: 40.75"). Neu khong co ':' thi lay
        # ca dong, tranh con so "4" trong chu "4 banh" bi tinh nham.
        segment = line.rsplit(":", 1)[1] if ":" in line else line
        nums += [float(x) for x in re.findall(r"-?\d+\.\d+|-?\d+", segment)]
    if not nums:
        return f"Dong 'trung binh' khong co so nao de so sanh. Output:\n{stdout}"
    for n in nums:
        if abs(n - expected) < eps:
            return None
    return (f"Sai gia tri trung binh. Mong doi {expected} "
            f"(sai so cho phep {eps}), thuc te {nums}.")


def check_case(case: dict, stdout: str, stdout_norm: str = None) -> list:
    """
    Kiem tra mot case. Tra ve danh sach loi; danh sach rong = PASS.
    """
    if stdout_norm is None:
        stdout_norm = normalize(stdout)
    errors = []
    for kw in case.get("expects", []):
        if not word_present(stdout_norm, normalize(kw)):
            errors.append(f"Thieu tu khoa '{kw}'")
    for kw in case.get("not_expects", []):
        if word_present(stdout_norm, normalize(kw)):
            errors.append(f"Khong duoc xuat hien tu khoa '{kw}'")
    if case.get("avg") is not None:
        err = check_avg(case["avg"], stdout)
        if err:
            errors.append(err)
    return errors


def check_style(source_text: str) -> list:
    """
    Kiem tra hoc vien co dung cu phap de bai yeu cau hay khong.
    Tra ve danh sach loi (rong = dat).
    """
    errors = []
    for name, pattern, desc in STYLE_RULES:
        if not re.search(pattern, source_text):
            errors.append(f"Thieu '{name}' - {desc}")
    return errors
