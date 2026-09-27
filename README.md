# Bộ Test Tự Động - Bài Tập C Nhúng

Chấm tự động 2 bài: giám sát ECU Toyota Vios và trạm điện mặt trời áp mái.

> **Mặc định bộ test chỉ kiểm tra bài "chạy được"**: biên dịch được, chạy không
> lỗi, không treo, có in ra kết quả. **Không** kiểm tra logic 5 hàm có đúng
> không. Muốn chấm logic thì thêm `--strict` — xem [Hai chế độ chấm](#hai-chế-độ-chấm).

| File | Dùng để |
|---|---|
| `TEST_CASES.md` | **Đặc tả đầy đủ**: quy tắc đề, thuật toán chấm, bảng 34 test case, ma trận coverage |
| `vios_template.c` / `solar_template.c` | File giao cho học viên — 5 hàm có `TODO`, phần còn lại giữ nguyên |
| `vios_solution.c` / `solar_solution.c` | Đáp án mẫu, dùng để tự kiểm bộ test |
| `tests/cases.py` | Toàn bộ test case và thuật toán so kết quả |
| `run_tests.py` | Chấm bài bằng 1 lệnh |
| `cham.bat` | **Double-click để chấm cả thư mục bài nộp** — không cần nhớ lệnh |
| `bainop/` | Thư mục bỏ file `.c` của học viên vào (tự tạo lần đầu) |

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

## Hai chế độ chấm

| | Mặc định — "chạy được" | `--strict` — "chấm chiem" |
|---|---|---|
| Biên dịch được với gcc | ✅ | ✅ |
| Chạy không lỗi, không treo (`rc == 0`) | ✅ | ✅ |
| Có in ra kết quả | ✅ | ✅ |
| Kiểm từ khóa `expects` / `not_expects` | ❌ | ✅ |
| Kiểm giá trị trung bình (sai số 0.06) | ❌ | ✅ |

```bat
python run_tests.py bai_hoa.c --vios              :: mặc định: chỉ cần chạy được
python run_tests.py bai_hoa.c --vios --strict     :: thêm kiểm logic
```

pytest không dùng được tên `--strict` (pytest đã chiếm cờ này), nên gõ:

```bat
pytest tests/test_vios.py -v --student=bai_hoa.c --strict-grading
```

> ⚠️ Ở chế độ mặc định, một bài mà 5 hàm còn nguyên dạng `return "TODO"` từ
> template vẫn đạt `17/17`. Bộ chấm mặc định không phân biệt được bài làm đúng
> với bài làm chưa làm gì — nếu cần chấm điểm logic thì phải bật `--strict`.

## Cách 1: double-click `cham.bat` (không cần nhớ lệnh)

```
1. Copy file .c của học viên vào thư mục  bainop\
2. Double-click  cham.bat
3. Chọn 1 (chỉ cần chạy được) hoặc 2 (chấm chặt logic)
4. Đọc kết quả trên màn hình, đồng thời lưu vào  ket_qua.txt
```

Lần chạy đầu tiên, `cham.bat` tự tạo thư mục `bainop` và hỏi bạn copy bài vào.

Tên file nên chứa `vios` hoặc `solar` để tự đoán đề, ví dụ
`vios_hoa.c`, `solar_phuong.c`. File tên không rõ đề sẽ được **bỏ qua** và
liệt kê ra màn hình để bạn đổi tên — không bị tính là FAIL.

Nếu muốn **một file .c = một điểm số** để chấm lớp, xem [Mục 7.3](#73-chấm-điểm-cả-lớp).

## Cách 2: gõ lệnh

```bat
:: Chấm bài Vios
python run_tests.py bai_hoa.c --vios
python run_tests.py "C:\duong\dan\bai.c" --vios

:: Chấm bài Solar
python run_tests.py bai_phuong.c --solar

:: Tự đoán đề từ tên file (tên chứa "vios" hoặc "solar")
python run_tests.py bai_vios_hoa.c

:: Chấm cả thư mục bài nộp (tự đoán đề từng file)
python run_tests.py --batch "bainop"

:: Chấm cả thư mục, giao đề cố định
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

## Chấm điểm cả lớp

Khi cần chấm **chặt** để lấy điểm cho cả lớp, dùng `cham_lop.bat` — nó luôn
chạy `--strict`, không cần chọn chế độ:

```bat
cham_lop.bat
cham_lop.bat "C:\duong\dan\thu_muc_bai_nop"
```

Kết quả hiện trên màn hình và lưu vào `ket_qua_lop.txt`. Bạn có thể mở file đó,
cột cuối là điểm phần `/17` của từng bài.

## Test linh hoạt thế nào

*(Các mục dưới đây chỉ áp dụng khi bật `--strict`.)*

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
    "no_output_ok": False,
    "expects": ["an toan"],
    "not_expects": ["nguy hiem"],
    "avg": 100.0,
    "desc": "Mô tả case này bắt lỗi gì.",
}
```

`expects` / `not_expects` / `avg` chỉ được dùng ở chế độ `--strict`. Đặt
`"no_output_ok": True` nếu case đó chạy xong mà không in gì vẫn được tính PASS
(dùng cho case thiếu dữ liệu).

Chạy lại là xong. Thêm test mà không sửa `cases.py` sẽ không được nhận.
