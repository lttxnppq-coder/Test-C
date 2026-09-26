#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test cho bai Solar (Tram Dien Mat Troi Ap Mai) - 16 case + 1 test do chinh xac.

Chay:
    pytest tests/test_solar.py -v
    pytest tests/test_solar.py -v --student=duong/dan/bai_hoc_vien.c
    pytest tests/test_solar.py -v --student=bai.c --check-style

Khong chi --student -> mac dinh cham solar_solution.c (de kiem tra bo test chay dung).
Toan bo danh sach case nam o tests/cases.py.
"""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from conftest import (  # noqa: E402
    build_exe, check_style, report_compile_error, resolve_student, run_exe,
)
from cases import SOLAR_CASES, EXTRA_CASES, check_case, normalize  # noqa: E402

SUITE = "solar"
DEFAULT_STUDENT = "solar_solution.c"


@pytest.fixture(scope="module")
def student_source(request):
    return resolve_student(request.config.getoption("--student"), DEFAULT_STUDENT)


@pytest.fixture(scope="module")
def student_exe(student_source, tmp_path_factory):
    assert student_source.exists(), (
        f"Khong tim thay file {student_source}. "
        f"Dung --student=duong/dan/file.c"
    )
    exe, log = build_exe(str(student_source), str(tmp_path_factory.mktemp("solar_build")))
    assert exe, report_compile_error(log, student_source)
    return exe


def _run_case(exe, case):
    stdout, stderr, rc = run_exe(exe, case["stdin"])
    assert rc == 0, f"Chuong trinh khong chay xong (rc={rc}). stderr={stderr}"
    errors = check_case(case, stdout)
    assert not errors, (
        f"{case['id']}: " + "; ".join(errors)
        + f"\n{'-' * 60}\nOutput:\n{stdout}\nChuan hoa: {normalize(stdout)}"
    )


@pytest.mark.parametrize("case", SOLAR_CASES, ids=[c["id"] for c in SOLAR_CASES])
def test_solar_case(student_exe, case):
    _run_case(student_exe, case)


@pytest.mark.parametrize(
    "case", EXTRA_CASES[SUITE], ids=[c["id"] for c in EXTRA_CASES[SUITE]]
)
def test_solar_extra(student_exe, case):
    _run_case(student_exe, case)


def test_solar_style(student_source, request):
    """Kiem tra hoc vien co dung for/switch/if theo yeu cau de bai."""
    if not request.config.getoption("check_style"):
        pytest.skip("Bo kiem tra cu phap. Bat bang --check-style")
    errors = check_style(student_source.read_text(encoding="utf-8", errors="replace"))
    assert not errors, f"{student_source.name}: " + "; ".join(errors)
