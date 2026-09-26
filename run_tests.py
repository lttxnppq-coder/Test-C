#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cham bai hoc vien bang 1 lenh, khong bat buoc pytest.

Cach dung
---------
  python run_tests.py                              # kiem tra bo test bang 2 solution mau
  python run_tests.py bai_hv.c --vios              # cham bai Vios
  python run_tests.py bai_hv.c --solar             # cham bai Solar
  python run_tests.py "C:\\duong\\dan\\bai.c" --vios
  python run_tests.py bai_hv.c                     # tu doan theo ten file (vios_/solar_)
  python run_tests.py --batch "bainop" --vios      # cham ca mot thu muc
  python run_tests.py --batch "bainop" --style     # them kiem tra cu phap for/switch/if
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

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BOLD = "\033[1m"


def grade(source: pathlib.Path, suite: str, check_src: bool) -> tuple:
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
            failures.append((case["id"],
                             f"Chuong trinh khong chay xong (rc={rc}). stderr={stderr}"))
            continue
        errors = check_case(case, stdout)
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


def detect_suite(name: str) -> str:
    """Doan de tu ten file. Tra ve 'vios'/'solar'/None."""
    low = name.lower()
    if "solar" in low:
        return "solar"
    if "vios" in low:
        return "vios"
    return None


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
    ap.add_argument("student", nargs="?", help="File .c can cham")
    ap.add_argument("--vios", action="store_true", help="Cham de Vios")
    ap.add_argument("--solar", action="store_true", help="Cham de Solar")
    ap.add_argument("--batch", metavar="THU_MUC", help="Cham tat ca file .c trong thu muc")
    ap.add_argument("--style", "--check-style", action="store_true",
                    dest="style", help="Kiem tra them for/switch/if theo de bai")
    args = ap.parse_args()

    if args.vios and args.solar:
        print(f"{RED}Khong the chay --vios va --cung luc --solar.{RESET}\n"
              f"Moi de chi mot bai. Hay chay rieng hai lenh.")
        return 2
    if args.student and args.batch:
        print(f"{RED}Khong the truyen ca ten file va --batch.{RESET}")
        return 2

    # ---- chay ca mot thu muc ----
    if args.batch:
        folder = pathlib.Path(args.batch)
        if not folder.is_dir():
            print(f"{RED}Khong phai thu muc: {folder}{RESET}")
            return 2
        files = sorted(folder.glob("*.c"))
        if not files:
            print(f"{YELLOW}Thu muc {folder} khong co file .c nao.{RESET}")
            return 2
        suites = [s for s, want in (("vios", args.vios), ("solar", args.solar)) if want]
        if not suites:
            print(f"{RED}Phai chi ro --vios hoac --solar khi dung --batch.{RESET}")
            return 2
        total_pass = total_all = 0
        for suite in suites:
            print_header(f"CHAM {SUITES[suite]['title']} - {folder}", folder)
            for f in files:
                p, t, fails = grade(f, suite, args.style)
                total_pass += p
                total_all += t
                mark = f"{GREEN}PASS{RESET}" if not fails else f"{RED}FAIL{RESET}"
                print(f"  {mark}  {f.name}  ({p}/{t})")
                for cid, msg in fails:
                    print(f"          {RED}{cid}{RESET}: {msg.splitlines()[0]}")
        print("\n" + "=" * 68)
        verdict = (f"{GREEN}  TAT CA PASS: {total_pass}/{total_all}{RESET}"
                   if total_pass == total_all
                   else f"{RED}  CO FAIL: {total_pass}/{total_all} case PASS{RESET}")
        print(verdict)
        print("=" * 68)
        return 0 if total_pass == total_all else 1

    # ---- cham 1 file ----
    if args.student:
        source = resolve_file(args.student)
        if not source.exists():
            print(f"{RED}Khong tim thay file: {source}{RESET}")
            return 2
        if args.vios:
            suites = ["vios"]
        elif args.solar:
            suites = ["solar"]
        else:
            guess = detect_suite(source.name)
            if guess is None:
                print(f"{RED}Khong doan duoc de bai tu ten file '{source.name}'.{RESET}\n"
                      f"Hay chi ro:  --vios  hoac  --solar\n"
                      f"Vi du: python run_tests.py \"{source.name}\" --vios")
                return 2
            suites = [guess]
    else:
        if args.vios:
            suites = ["vios"]
        elif args.solar:
            suites = ["solar"]
        else:
            suites = ["vios", "solar"]
        source = None

    total_pass = total_all = 0
    for suite in suites:
        target = source or (ROOT / SUITES[suite]["solution"])
        print_header(f"CHAM {SUITES[suite]['title']}", target)
        if not target.exists():
            print(f"{YELLOW}Khong co file mau {target.name} de kiem tra bo test."
                  f"Hay chi --student=<file .c>{RESET}")
            continue
        p, t, fails = grade(target, suite, args.style)
        total_pass += p
        total_all += t
        print_report(p, t, fails)

    print("\n" + "=" * 68)
    if total_all == 0:
        verdict = f"{YELLOW}  KHONG CO CASE NAO CHAY{RESET}"
    elif total_pass == total_all:
        verdict = f"{GREEN}  TAT CA TEST PASSED: {total_pass}/{total_all}{RESET}"
    else:
        verdict = f"{RED}  CO TEST FAILED: {total_pass}/{total_all} case PASS{RESET}"
    print(verdict)
    print("=" * 68)
    return 0 if total_pass == total_all and total_all else 1


if __name__ == "__main__":
    sys.exit(main())
