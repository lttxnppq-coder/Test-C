# Bộ Test Tự Động - Bài Tập C Nhúng

Chấm tự động 2 bài: giám sát ECU Toyota Vios và trạm điện mặt trời áp mái.

| File | Dùng để |
|---|---|
| `TEST_CASES.md` | **Đặc tả đầy đủ**: quy tắc đề, thuật toán chấm, bảng 34 test case, ma trận coverage |
| `vios_template.c` / `solar_template.c` | File giao cho học viên — 5 hàm có `TODO`, phần còn lại giữ nguyên |
| `vios_solution.c` / `solar_solution.c` | Đáp án mẫu, dùng để tự kiểm bộ test |
| `tests/cases.py` | Toàn bộ test case và thuật toán so kết quả |
| `run_tests.py` | Chấm bài bằng 1 lệnh |

## Yêu cầu môi trường

- `gcc` trong PATH (MinGW-w64 / TDM-GCC / MSYS2 / Linux / macOS)
- Python 3.8+
- `pytest` là tuỳ chọn — chỉ dùng để xem báo cáo đẹp hơn

```bat
gcc --version
python --version
pip install -r requirements.txt    :tùy chọn
```

## Chạy thử bộ test

```bat
python run_tests.py
```

Lệnh này chấm 2 file đáp án mẫu `vios_solution.c` / `solar_solution.c`.
**Hai file đó không có trong repo này** (đó là đáp án, để khoá khỏi lộ). Nếu
muốn tự kiểm bộ test thì tự viết lời giải theo `TEST_CASES.md` rồi chấm:

```bat
python run_tests.py bai_cua_toi.c --vios
```

Kết quả mong đợi khi lời giải đúng: `17/17` PASS mỗi đề.

## Chấm bài học viên

```bat
:: Chấm bài Vios
python run_tests.py bai_hoa.c --vios
python run_tests.py "C:\duong\dan\bai.c" --vios

:: Chấm bài Solar
python run_tests.py bai_phuong.c --solar

:: Tự đoán đề từ tên file (tên chứa "vios" hoặc "solar")
python run_tests.py bai_vios_hoa.c

:: Chấm cả thư mục bài nộp
python run_tests.py --batch "bainop" --vios
```

Dùng pytest nếu muốn xem chi tiết từng case:

```bat
pytest tests/ -v
pytest tests/test_vios.py -v --student=bai_hoa.c
```

Thêm kiểm tra học viên có dùng đúng `for` / `switch` / `if` theo yêu cầu đề
(mặc định **không** bật):

```bat
python run_tests.py --batch "bainop" --vios --style
pytest tests/test_vios.py -v --student=bai_hoa.c --check-style
```

Mã thoát: `0` tất cả PASS · `1` có FAIL · `2` lỗi tham số.

## Test linh hoạt thế nào

Output của chương trình được chuẩn hóa trước khi so: bỏ dấu tiếng Việt, chuyển
chữ thường, mọi ký tự đặc biệt thành dấu cách. Nên những cách sau đều được
chấp nhận:

```
Ket luan: NGUY HIEM
Ket luan: Nguy Hiem
nguy hiem!!
```

Sai số giá trị trung bình cho phép 0.06, nên in `%.1f` hay `%.2f` đều không bị
trừ điểm.

## Học viên nộp gì

Một file `.c` duy nhất, dựa trên template. Không cần đổi tên, nhưng đặt tên
`vios_<mssv>.c` / `solar_<mssv>.c` cho dễ chấm.

Bắt buộc giữ nguyên:

- Thứ tự đọc bằng `scanf` (7 số, thứ tự cố định)
- Tên và kiểu 5 hàm
- Các dòng `printf` trong `main()`, đặc biệt dòng có chữ `trung binh`

## Lưu ý khi phát bài

- **Xoá `vios_solution.c` và `solar_solution.c`** trước khi gửi cho học viên —
  đó là đáp án.
- Template giao đi đã bỏ sẵn phần lời giải trong 5 hàm `TODO`.

## Thêm test case mới

Mở `tests/cases.py`, thêm một dict vào `VIOS_CASES` hoặc `SOLAR_CASES`:

```python
{
    "id": "17_case_moi",
    "stdin": "60\n80\n2\n100 110 90 100\n",
    "expects": ["an toan"],
    "not_expects": ["nguy hiem"],
    "avg": 100.0,
    "desc": "Mô tả case này bắt lỗi gì.",
}
```

Chạy lại là xong. Thêm test mà không sửa `cases.py` sẽ không được nhận.
