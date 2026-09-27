# Bộ Test Tự Động — Bài Tập C Nhúng

Chấm tự động 2 bài: **giám sát ECU Toyota Vios** và **trạm điện mặt trời áp mái**.
Mỗi đề có 17 test case, tổng 34 case.

Cách dùng nhanh nhất: **kéo file `.c` của học viên vào `cham.bat`**.

---

## Bắt đầu trong 3 bước

### Bước 1 — Cài đặt (chỉ làm 1 lần)

Double-click **`cai_dat.bat`**. Nó sẽ tự kiểm tra và cài:

- Python 3
- `gcc` — trình biên dịch C

Nếu máy đã có sẵn thì không cài gì thêm.

> Sau khi cài xong **phải đóng cửa sổ đó rồi mở lại**, vì Windows chỉ đọc lại
> `PATH` khi mở cửa sổ mới. Nếu chạy lại `cai_dat.bat` mà vẫn báo thiếu thì
> chính là lý do này.

Cài tay nếu script báo không có `winget` — hướng dẫn có in ra ngay trong cửa sổ đó.

### Bước 2 — Đưa bài vào

**Cách A — kéo thả (nhanh nhất):** kéo file `.c` của học viên, **thả thẳng vào cửa sổ `cham.bat`**.

Có thể kéo nhiều file cùng lúc, hoặc kéo cả thư mục bài nộp vào.

**Cách B — bỏ vào thư mục:** copy file `.c` vào thư mục `bainop\` rồi double-click `cham.bat`.

> **Nên đặt tên file chứa `vios` hoặc `solar`** — ví dụ `vios_hoa.c`,
> `solar_phuong.c`. Đó là cách máy tự biết đó là đề nào.
> File tên không rõ, `cham.bat` sẽ **hỏi bạn** thay vì đoán bừa.

### Bước 3 — Đọc kết quả

Chọn chế độ chấm rồi xem bảng điểm hiện trên màn hình. Kết quả cũng được lưu vào
`ket_qua.txt` để mở lại sau bằng Notepad (file này không có mã màu, đọc sạch).

---

## Hai chế độ chấm

`cham.bat` sẽ hỏi bạn chọn:

| | **1 — "chạy được"** (mặc định) | **2 — "chấm chặt"** |
|---|---|---|
| Biên dịch được với `gcc` | ✅ | ✅ |
| Chạy không lỗi, không treo (`rc == 0`) | ✅ | ✅ |
| Có in ra kết quả | ✅ | ✅ |
| Kiểm từ khóa `expects` / `not_expects` | ❌ | ✅ |
| Kiểm giá trị trung bình (sai số 0.06) | ❌ | ✅ |

Chọn `2` khi cần lấy điểm số chấm nghiêm túc. Chọn `1` (hoặc Enter) khi chỉ
muốn xem bài có chạy không.

> ⚠️ **Điểm cần biết:** ở chế độ 1, một bài mà 5 hàm còn nguyên dạng
> `return "TODO"` từ template vẫn đạt `17/17`. Bộ chấm mặc định **không phân biệt
> được** bài làm đúng với bài chưa làm gì. Muốn chấm điểm logic thì bắt buộc
> dùng chế độ 2.

---

## Bảng điểm

Khi chấm nhiều file, in ra một bảng xếp hạng, từ điểm cao xuống thấp:

```
=================================================
  BAI                DE      DIEM      KET QUA
  -------------------------------------------------
  solar_phuong.c     solar   17/17     DAT
  vios_hoa.c         vios    17/17     DAT
  vios_chua_lamgi.c  vios    1/17      FAIL
  vios_treo.c        vios    1/17      FAIL
  -------------------------------------------------
  Trung binh: 53%   Dat 2, khong dat 2   (tong 4 bai)
=================================================
```

- Cột `DIEM` là số case PASS trên tổng 17.
- `DAT` = không case nào FAIL, `FAIL` = có ít nhất một case FAIL.
- File bị bỏ qua vì tên không rõ đề được liệt kê riêng, **không tính là FAIL**.

Chấm đúng 1 file thì không có bảng, mà in chi tiết từng case FAIL — dễ biết học
viên sai chỗ nào.

---

## Chấm cả lớp

Khi cần chấm **chặt** để lấy điểm cho cả lớp, double-click **`cham_lop.bat`**.
Nó luôn chạy chế độ chặt, không cần chọn gì:

```bat
cham_lop.bat                                        :: chấm thư mục bainop\
cham_lop.bat "C:\duong\dan\thu_muc_bai_nop"          :: chấm thư mục khác
```

Kết quả lưu vào `ket_qua_lop.txt`.

---

## Gõ lệnh trực tiếp

```bat
:: Chấm 1 bài, chỉ ra đề
python run_tests.py bai_hoa.c --vios
python run_tests.py bai_phuong.c --solar

:: Tự đoán đề từ tên file (chứa "vios" hoặc "solar")
python run_tests.py bai_vios_hoa.c

:: Chấm nhiều file một lúc
python run_tests.py bai1.c bai2.c bai3.c
python run_tests.py "C:\Hoc\sin\hoc" --vios

:: Tên file không rõ đề thì hỏi từng file
python run_tests.py bai1.c bai2.c --ask

:: Chấm cả thư mục (tự đoán đề từng file)
python run_tests.py --batch "bainop"
python run_tests.py --batch "bainop" --vios        :: giao đề cố định cho cả thư mục

:: Chấm chặt logic
python run_tests.py bai_hoa.c --vios --strict
python run_tests.py --batch "bainop" --strict
```

Muốn bảng điểm và thông báo "đổi tên file" thì thêm `--ask` hoặc dùng `--batch`.

Mã thoát: `0` tất cả PASS · `1` có FAIL · `2` lỗi tham số / không có file nào chấm được.

---

## Xem chi tiết từng test case

`run_tests.py` in ra đúng những gì bạn cần để chấm. Nếu vẫn muốn báo cáo kiểu
pytest thì cài thêm:

```bat
pip install -r requirements.txt
pytest tests/ -v
```

Chấm bài cụ thể bằng pytest:

```bat
pytest tests/test_vios.py -v --student=bai_hoa.c
```

Thêm kiểm tra học viên có dùng đúng `for` / `switch` / `if` theo yêu cầu đề
(mặc định **không** bật):

```bat
python run_tests.py --batch "bainop" --vios --style
pytest tests/test_vios.py -v --student=bai_hoa.c --check-style
```

> pytest đã dùng cờ `--strict` cho ý nghĩa khác, nên bộ test này tên cờ là
> `--strict-grading` (hoặc `--cham-chiem`):
>
> ```bat
> pytest tests/test_vios.py -v --student=bai_hoa.c --strict-grading
> ```

---

## Xử lý sự cố

| Bạn thấy | Nguyên nhân | Cách sửa |
|---|---|---|
| `[LOI] Thieu Python` hoặc `Thieu gcc` | Chưa cài, hoặc mới cài xong chưa mở lại cửa sổ | Đóng cửa sổ đó, mở lại. Nếu vẫn lỗi thì chạy lại `cai_dat.bat` |
| `Ten file ... khong cho biet thuoc de bai nao` | Tên file không có `vios`/`solar` | Trả lời `1` (Vios) hoặc `2` (Solar), hoặc Enter để bỏ qua |
| `Khong doan duoc de bai tu ten file` | Chạy lệnh tay mà không có `--ask` | Thêm `--vios`/`--solar`, hoặc thêm `--ask` |
| `Trong thu muc khong co file .c nao doan duoc` | Tất cả tên file đều không rõ đề | Đổi tên thành `vios_...c` hoặc `solar_...c` |
| `Khong phai thu muc` | Sai đường dẫn | Dùng đường dẫn đầy đủ, cần dấu nháy kép nếu có khoảng trắng |
| Bài bị trễ điểm dù học viên làm đúng | Đang ở chế độ 1 | Chạy lại với chế độ 2 (chấm chặt) |
| `BIEN DICH THAT BAI` | Lỗi biên dịch C | Đọc thông báo gcc ngay dòng dưới; thường do thiếu thư viện hoặc sai kiểu dữ liệu |
| Chấm bị treo, phải bấm `Ctrl+C` | Bài học viên rơi vào vòng lặp vô hạn | Mỗi test case chạy tối đa 10 giây; bài treo sẽ bị FAIL, không kéo dài cả buổi chấm |

Mọi bài học viên đều được chạy trong thư mục riêng và tự động bị giới hạn thời
gian, nên một bài lỗi không làm treo cả buổi chấm.

---

## Test linh hoạt thế nào

*(Các mục dưới đây chỉ áp dụng khi bật chế độ 2 / `--strict`.)*

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

---

## Học viên nộp gì

Một file `.c` duy nhất, dựa trên template. Không cần đổi tên, nhưng đặt tên
`vios_<mssv>.c` / `solar_<mssv>.c` cho dễ chấm.

Bắt buộc giữ nguyên:

- Thứ tự đọc bằng `scanf` (7 số, thứ tự cố định)
- Tên và kiểu 5 hàm
- Các dòng `printf` trong `main()`, **đặc biệt dòng có chữ `trung binh`**

> Dòng chứa `trung binh` là dòng duy nhất bộ chấm dùng để lấy giá trị trung bình
> để so số. In sai từ này thì bài đúng vẫn bị trừ điểm.

---

## Lưu ý khi phát bài

- **Xoá `vios_solution.c` và `solar_solution.c`** trước khi gửi cho học viên —
  đó là đáp án. Hai file này **không có** trong repo này.
- Template giao đi đã bỏ sẵn phần lời giải trong 5 hàm `TODO`.
- Không cần sửa gì trong `tests/cases.py` để dùng bộ chấm này.

---

## Các file trong bộ test

| File | Dùng để |
|---|---|
| `cham.bat` | **Kéo file `.c` vào đây, hoặc double-click** để chấm bài |
| `cai_dat.bat` | Cài Python + `gcc`, chạy 1 lần duy nhất |
| `cham_lop.bat` | Chấm cả lớp, luôn ở chế độ chặt |
| `run_tests.py` | Chấm bài bằng lệnh, in bảng điểm |
| `vios_template.c` / `solar_template.c` | File giao cho học viên — 5 hàm có `TODO` |
| `tests/cases.py` | Toàn bộ test case và thuật toán so kết quả |
| `TEST_CASES.md` | **Đặc tả đầy đủ**: quy tắc đề, thuật toán chấm, bảng 34 case, ma trận coverage |
| `bainop/` | Thư mục bỏ file `.c` vào (tự tạo lần đầu) |
| `ket_qua.txt` / `ket_qua_lop.txt` | Kết quả lần chấm gần nhất (tự sinh) |

---

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

`expects` / `not_expects` / `avg` chỉ được dùng ở chế độ 2. Đặt
`"no_output_ok": True` nếu case đó chạy xong mà không in gì vẫn được tính PASS
(dùng cho case thiếu dữ liệu).

Chạy lại là xong. Thêm test mà không sửa `cases.py` sẽ không được nhận.
