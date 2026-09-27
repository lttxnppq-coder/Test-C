#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cham bai hoc vien bang 1 lenh, khong bat buoc pytest.

Mac dinh chi kiem tra bai co BIEN DICH DUOC va CHAY DUOC khong (return code 0,
khong treo, co in ra ket qua). Khong kiem tra logic 5 ham co dung hay khong.
Them --strict neu muon cham chiem: kiem tra tu khoa va gia tri trung binh.

Cach dung
---------
  python run_tests.py                              # kiem tra bo test bang 2 solution mau
  python run_tests.py bai_hv.c --vios              # cham bai Vios
  python run_tests.py bai_hv.c --solar             # cham bai Solar
  python run_tests.py "C:\\duong\\dan\\bai.c" --vios
  python run_tests.py bai_hv.c                     # tu doan theo ten file (vios_/solar_)
  python run_tests.py bai1.c bai2.c bai3.c        # cham nhieu file mot luc
  python run_tests.py bai1.c bai2.c --ask         # ten file khong ro de -> hoi
  python run_tests.py --batch "bainop" --vios      # cham ca mot thu muc
  python run_tests.py --batch "bainop" --strict    # cham chiem
  python run_tests.py --help

Ket qua: 0 = tat ca PASS, 1 = co FAIL, 2 = loi tham so.
"""
import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT / "tests"))

from cases import EXTRA_CASES, SUITES, check_case, check_style, normalize  # noqa: E402
from conftest import build_exe, report_compile_error, run_exe  # noqa: E402

# Khi in ra file (khong phai cua so terminal) thi bo qua ma mau ANSI, neu khong
# ket_qua.txt se chua day ky tu dieu khien, mo bang Notepad thay to ky tu la.
# Cach nay khong can co "bat tat mau" nao ca.
try:
    USE_COLOR = sys.stdout.isatty()
except Exception:  # noqa: BLE001
    USE_COLOR = False

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BOLD = "\033[1m"
if not USE_COLOR:
    RESET = RED = GREEN = YELLOW = CYAN = BOLD = ""


def grade(source: pathlib.Path, suite: str, check_src: bool, strict: bool) -> tuple:
    """
    Cham mot file .c theo mot de.
    Tra ve (so_pass, tong_so, danh sach_dong_loi).
    """
    info = SUITES[suite]
    passed, total, failures = 0, 0, []

    exe, log = build_exe(str(source))
    if not exe:
        return 0, 1, [("BIEN DICH THAT BAI", report_compile_error(log, source))]

    for case in list(info["cases"]) + list(EXTRA_CASES[suite]):
        total += 1
        stdout, stderr, rc = run_exe(exe, case["stdin"])
        if rc != 0:
            detail = (f"Chuong trinh khong chay xong (rc={rc}). stderr={stderr}"
                      if rc != -1 else stderr)
            failures.append((case["id"], detail))
            continue
        errors = check_case(case, stdout, strict=strict)
        if errors:
            failures.append((case["id"], "; ".join(errors) + f"\n    Output:\n    "
                                                             + stdout.replace("\n", "\n    ")))
        else:
            passed += 1

    if check_src:
        total += 1
        errors = check_style(source.read_text(encoding="utf-8", errors="replace"))
        if errors:
            failures.append(("check_style", "; ".join(errors)))
        else:
            passed += 1

    return passed, total, failures


def print_header(title: str, source: pathlib.Path):
    print("\n" + "=" * 68)
    print(f"{BOLD}{CYAN}  {title}{RESET}")
    print(f"  File: {source}")
    print("=" * 68)


def print_report(passed: int, total: int, failures: list):
    for case_id, msg in failures:
        print(f"{RED}  FAIL{RESET}  {case_id}")
        for line in msg.splitlines():
            print(f"          {line}")
    if not failures:
        print(f"{GREEN}  PASS{RESET}  {passed}/{total} case")
    elif passed:
        print(f"\n  {YELLOW}{passed}/{total} PASS, {total - passed} FAIL{RESET}")


def detect_suite(name: str):
    """Doan de tu ten file. Tra ve 'vios'/'solar'/None."""
    low = name.lower()
    if "solar" in low:
        return "solar"
    if "vios" in low:
        return "vios"
    return None


def ask_suite(name: str):
    """
    Hoi nguoi dung de bai cua mot file, khi ten file khong ro.
    Tra ve 'vios'/'solar'/None (None = nguoi dung bo qua).
    """
    print(f"\n  {YELLOW}Ten file '{name}' khong cho biet thuoc de bai nao.{RESET}")
    print(f"  Nhap 1 = Vios   2 = Solar   Enter = bo qua file nay")
    try:
        ans = input("  Lua chon: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return None
    if ans in ("1", "v", "vios"):
        return "vios"
    if ans in ("2", "s", "solar"):
        return "solar"
    return None


def collect_files(paths, suite: str, ask: bool):
    """
    Chuyen danh sach duong dan thanh list (file, suite).
    Tu tach cac file .c trong thu muc neu gap thu muc.
    """
    items = []
    for raw in paths:
        p = resolve_file(raw)
        if p.is_dir():
            found = sorted(p.glob("*.c"))
            if not found:
                print(f"{YELLOW}Thu muc {p} khong co file .c nao.{RESET}")
            for f in found:
                items.append((f, suite))
        elif p.exists():
            # Chi nhan file .c. Keo nham PDF/txt vao se ra loi gcc rat
            # kho hieu, thong bao ro rang de hon.
            if p.suffix.lower() != ".c":
                print(f"{YELLOW}Bo qua '{p.name}': chi cham file .c.{RESET}")
                continue
            items.append((p, suite))
        else:
            print(f"{RED}Khong tim thay file: {p}{RESET}")
            return None

    out = []
    for f, forced in items:
        if forced:
            out.append((f, forced))
            continue
        guess = detect_suite(f.name)
        if guess is None:
            if not ask:
                print(f"{RED}Khong doan duoc de bai tu ten file '{f.name}'.{RESET}\n"
                      f"Hay chi ro:  --vios  hoac  --solar\n"
                      f"Vi du: python run_tests.py \"{f.name}\" --vios\n"
                      f"Ho them  --ask  de duoc hoi truc tiep.")
                return None
            guess = ask_suite(f.name)
            if guess is None:
                continue
        out.append((f, guess))
    return out


class Row:
    """Ket qua cham 1 file, dung de in bang diem."""

    def __init__(self, name, suite, passed, total, failures):
        self.name = name
        self.suite = suite
        self.passed = passed
        self.total = total
        self.failures = failures

    @property
    def ok(self) -> bool:
        return not self.failures

    @property
    def ratio(self) -> float:
        return (self.passed / self.total) if self.total else 0.0


def print_summary_table(rows, skipped=None):
    """
    In bang diem tong hop: xep theo diem giam dan, de nhin 1 lan la ra
    ai dat, ai khong dat, ai xep hang may.
    """
    if not rows:
        return
    width = max(12, min(40, max(len(r.name) for r in rows)))
    line = "=" * (width + 32)
    rule = "-" * (width + 32)

    print("\n" + line)
    print(f"  {BOLD}{'BAI':<{width}}  {'DE':<6}  {'DIEM':<8}  KET QUA{RESET}")
    print("  " + rule)
    for r in sorted(rows, key=lambda r: (-r.ratio, r.name)):
        mark = f"{GREEN}DAT{RESET}" if r.ok else f"{RED}FAIL{RESET}"
        score = f"{r.passed}/{r.total}"
        print(f"  {r.name:<{width}}  {r.suite:<6}  {score:<8}  {mark}")
    print("  " + rule)

    n_ok = sum(1 for r in rows if r.ok)
    avg = sum(r.ratio for r in rows) / len(rows)
    if n_ok == len(rows):
        print(f"  {BOLD}Trung binh: {avg * 100:.0f}%   Dat {n_ok}/{len(rows)}{RESET}")
    else:
        print(f"  {BOLD}Trung binh: {avg * 100:.0f}%   "
              f"Dat {GREEN}{n_ok}{RESET}, khong dat {RED}{len(rows) - n_ok}{RESET}"
              f"   (tong {len(rows)} bai){RESET}")
    if skipped:
        print(f"\n  {YELLOW}Bo qua {len(skipped)} file vi ten khong ro de bai:{RESET}")
        for name in skipped:
            print(f"    {name}  ->  doi ten thanh vios_{name} hoac solar_{name}")
    print(line)


def grade_many(items, check_src: bool, strict: bool, show_cases: bool):
    """
    Cham nhieu file va in bang diem.
    show_cases=True thi in them chi tiet tung case FAIL (dung khi chi cham
    1 file va can biet sai choi).
    Tra ve (rows, tong_so_case, so_case_dat).
    """
    rows = []
    total_all = total_pass = 0
    for f, suite in items:
        p, t, fails = grade(f, suite, check_src, strict)
        total_pass += p
        total_all += t
        rows.append(Row(f.name, suite, p, t, fails))
        if show_cases and fails:
            for cid, msg in fails:
                print(f"      {RED}{cid}{RESET}: {msg.splitlines()[0]}")
    return rows, total_pass, total_all


def resolve_file(raw: str) -> pathlib.Path:
    p = pathlib.Path(raw)
    if p.is_absolute() or p.exists():
        return p
    return (ROOT / p).resolve()


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Cham bai Vios & Solar - cham linh hoat dau tieng Viet",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("students", nargs="*", metavar="BAI",
                    help="File .c can cham. Nhieu duoc. Keo file vao cham.bat "
                         "thi moi tham so nay")
    ap.add_argument("--vios", action="store_true", help="Cham de Vios")
    ap.add_argument("--solar", action="store_true", help="Cham de Solar")
    ap.add_argument("--batch", metavar="THU_MUC", help="Cham tat ca file .c trong thu muc")
    ap.add_argument("--strict", "--strict-grading", "--cham-chiem",
                    action="store_true", dest="strict",
                    help="Cham chiem: kiem tra them tu khoa va gia tri trung binh. "
                         "Mac dinh chi kiem tra bai co chay duoc hay khong")
    ap.add_argument("--ask", action="store_true",
                    help="File ten khong ro de bai se duoc hoi truc tiep thay vi "
                         "bao loi. cham.bat luon bat co")
    ap.add_argument("--style", "--check-style", action="store_true",
                    dest="style", help="Kiem tra them for/switch/if theo de bai")
    args = ap.parse_args()

    if args.vios and args.solar:
        print(f"{RED}Khong the chay --vios va --cung luc --solar.{RESET}\n"
              f"Moi de chi mot bai. Hay chay rieng hai lenh.")
        return 2
    if args.students and args.batch:
        print(f"{RED}Khong the truyen ca ten file va --batch.{RESET}")
        return 2

    forced = "vios" if args.vios else ("solar" if args.solar else None)

    # ---- cham nhieu file trong thu muc ----
    if args.batch:
        folder = pathlib.Path(args.batch)
        if not folder.is_dir():
            print(f"{RED}Khong phai thu muc: {folder}{RESET}")
            return 2
        files = sorted(folder.glob("*.c"))
        if not files:
            print(f"{YELLOW}Thu muc {folder} khong co file .c nao.{RESET}")
            return 2

        # --vios/--solar ep ca thu muc vao mot de; khong chi ro de:
        # doan de cho tung file theo ten, file khong doan duoc se bi BO QUA
        # (khong coi la FAIL) de khong lam nguoi cham nghia bai do sai.
        items, skipped = [], []
        if forced:
            items = [(f, forced) for f in files]
        else:
            for f in files:
                guess = detect_suite(f.name)
                if guess is None:
                    skipped.append(f.name)
                else:
                    items.append((f, guess))

        if not items:
            # print_summary_table() bo qua qua khi khong co row nao, nen
            # phai in huong dan doi ten o day, khong o trong ham do.
            print(f"{YELLOW}Trong thu muc khong co file .c nao doan duoc de bai nao.{RESET}")
            print(f"{YELLOW}Bo qua {len(skipped)} file:{RESET}")
            for name in skipped:
                print(f"  {name}  ->  doi ten thanh vios_{name} hoac solar_{name}")
            return 2

        print_header(f"CHAM {len(items)} BAI - {folder}", folder)
        rows, total_pass, total_all = grade_many(items, args.style, args.strict,
                                                 show_cases=False)
        print_summary_table(rows, skipped)
        if total_pass == total_all and total_all:
            return 0
        return 1

    # ---- cham file dua vao tu dong lenh (keo tha file vao cham.bat) ----
    if args.students:
        items = collect_files(args.students, forced, args.ask)
        if items is None:
            return 2
        if not items:
            print(f"{YELLOW}Khong co file .c nao de cham.{RESET}")
            return 2
        if len(items) == 1:
            f, suite = items[0]
            print_header(f"CHAM {SUITES[suite]['title']}", f)
            p, t, fails = grade(f, suite, args.style, args.strict)
            print_report(p, t, fails)
            print("\n" + "=" * 68)
            if t and not fails:
                print(f"{GREEN}  TAT CA TEST PASSED: {p}/{t}{RESET}")
            elif t:
                print(f"{RED}  CO TEST FAILED: {p}/{t} case PASS{RESET}")
            else:
                print(f"{YELLOW}  KHONG CO CASE NAO CHAY{RESET}")
            print("=" * 68)
            return 0 if t and not fails else 1

        print_header(f"CHAM {len(items)} BAI", ROOT)
        rows, total_pass, total_all = grade_many(items, args.style, args.strict,
                                                 show_cases=False)
        print_summary_table(rows)
        return 0 if total_pass == total_all and total_all else 1

    # ---- khong truyen gi: tu kiem bo test bang 2 file dap an mau ----
    if args.vios:
        suites = ["vios"]
    elif args.solar:
        suites = ["solar"]
    else:
        suites = ["vios", "solar"]

    print(f"{BOLD}{CYAN}  Tu kiem bo test bang 2 file dap an mau{RESET}")
    print(f"  {YELLOW}Neu khong co file mau, hay cham bai that cua hoc vien:{RESET}")
    print(f"  {YELLOW}keo file .c vao cham.bat, hoac go:"
          f" python run_tests.py bai.c --vios{RESET}")
    found_any = False

    total_pass = total_all = 0
    for suite in suites:
        target = ROOT / SUITES[suite]["solution"]
        print_header(f"CHAM {SUITES[suite]['title']}", target)
        if not target.exists():
            print(f"{YELLOW}Khong co file mau {target.name} trong thu muc nay "
                  f"(intentional - de khong lo dap an).{RESET}")
            continue
        found_any = True
        p, t, fails = grade(target, suite, args.style, args.strict)
        total_pass += p
        total_all += t
        print_report(p, t, fails)

    if not found_any:
        return 2

    print("\n" + "=" * 68)
    if total_pass == total_all:
        verdict = f"{GREEN}  TAT CA TEST PASSED: {total_pass}/{total_all}{RESET}"
    else:
        verdict = f"{RED}  CO TEST FAILED: {total_pass}/{total_all} case PASS{RESET}"
    print(verdict)
    print("=" * 68)
    return 0 if total_pass == total_all and total_all else 1


if __name__ == "__main__":
    sys.exit(main())
