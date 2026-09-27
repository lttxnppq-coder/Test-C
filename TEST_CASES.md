# BỘ TEST TỰ ĐỘNG - ĐẶC TẢ ĐẦY ĐỦ

Tài liệu này mô tả **toàn bộ** bộ test tự động cho 2 đề bài tập C. Mục tiêu là
**đủ thông tin để dựng lại bộ test này từ đầu**, không cần đọc code.

Nếu chỉ cần dùng bộ test có sẵn thì đọc `README.md`. Nếu muốn kiểm tra lại tính
đúng đắn của test case, đọc tài liệu này.

| | |
|---|---|
| Ngôn ngữ test | Python 3.8+ (không bắt buộc pytest) |
| Trình biên dịch | gcc (`-std=c99`) |
| Số test case | 34 (Vios 17, Solar 17) |
| **Mặc định** | **Chạy được**: biên dịch được + chạy không lỗi + có in kết quả |
| `--strict` | Chấm chặt: thêm so khớp từ khóa, sai số trung bình 0.06 |

> **Đọc trước khi dùng.** Mặc định bộ test **không** kiểm tra logic 5 hàm có đúng
> hay không — một bài mà 5 hàm vẫn còn nguyên dạng `return "TODO"` từ template
> vẫn đạt 17/17. Nếu cần chấm điểm logic thì bắt buộc thêm `--strict`
> (pytest dùng tên khác, xem [Mục 7.2](#72-lệnh)). Chi tiết ở
> [Mục 3](#3-thuật-toán-chấm).

---

## 1. Đặc tả đề Vios

### 1.1. Dữ liệu vào (stdin)

Đọc **đúng 7 số theo thứ tự cố định**, phân tách bằng dấu cách hoặc xuống dòng
đều được (bắt buộc phải dùng `scanf`):

| # | Biến | Kiểu | Ý nghĩa |
|---|---|---|---|
| 1 | `tocDoXe` | float | Tốc độ xe (km/h) |
| 2 | `nhietDo` | float | Nhiệt độ động cơ (°C) |
| 3 | `cheDoLai` | int | Chế độ lái: 1 ECO, 2 NORMAL, 3 SPORT |
| 4-7 | `banh[0..3]` | float | Tốc độ 4 bánh (km/h) |

Ví dụ: `60 85 2 40 41 40 42`

### 1.2. Năm hàm cài đặt

```c
const char* danhGiaNhietDo(float temp);      /* NORMAL | HIGH | OVERHEAT */
const char* layTenCheDo(int mode);            /* ECO | NORMAL | SPORT */
float tinhTocDoTrungBinh(float w1, float w2, float w3, float w4);
int    laQuaToc(float speeds[4]);            /* 1 = có bánh > 120, 0 = không */
int    laNguyHiem(float temp, float speeds[4]);
```

### 1.3. Quy tắc nghiệp vụ

| Hàm | Quy tắc | Biên |
|---|---|---|
| `danhGiaNhietDo` | `temp <= 90` → `"NORMAL"`<br>`temp <= 105` → `"HIGH"`<br>còn lại → `"OVERHEAT"` | 90.0 phải ra NORMAL, 90.1 ra HIGH<br>105.0 phải ra HIGH, 105.1 ra OVERHEAT |
| `layTenCheDo` | `1` → `"ECO"`, `2` → `"NORMAL"`, `3` → `"SPORT"`, mọi giá trị khác → `"NORMAL"` | mode 0 và mode 99 đều ra NORMAL |
| `tinhTocDoTrungBinh` | `(w1+w2+w3+w4)/4.0f` | |
| `laQuaToc` | 1 nếu **bất kỳ** phần tử nào `> 120.0f` | đúng 120.0 **không** quá tốc |
| `laNguyHiem` | 1 nếu `temp > 105` **HOẶC** `laQuaToc() == 1` | nhiệt đúng 105 **không** nguy hiểm |

Yêu cầu cấu trúc của đề: dùng `if/else if/else` (hàm 1), `switch/case` có
`default` (hàm 2 và hàm 3 phải duyệt đủ 4 phần tử bằng `for`).

### 1.4. Dòng output chứa giá trị trung bình

Bắt buộc có, vì bộ test đọc giá trị trung bình từ dòng này:

```
Van toc trung binh 4 banh: 40.75 km/h
```

---

## 2. Đặc tả đề Solar

### 2.1. Dữ liệu vào (stdin)

Đọc **đúng 7 số theo thứ tự cố định**:

| # | Biến | Kiểu | Ý nghĩa |
|---|---|---|---|
| 1 | `congSuat` | float | Công suất phát (kW) |
| 2 | `nhietDoPin` | float | Nhiệt độ pin (°C) |
| 3 | `cheDo` | int | Chế độ inverter: 1 OFF-GRID, 2 GRID-TIED, 3 HYBRID, 4 FAULT |
| 4-7 | `dienAp[0..3]` | float | Điện áp 4 chuỗi (V) |

Ví dụ: `50.5 40 2 420.5 418.0 425.2 455.0`

### 2.2. Năm hàm cài đặt

```c
const char* danhGiaNhietDoPin(float temp);   /* OPTIMAL | HIGH_TEMP | CRITICAL_HEAT */
const char* layTenInverter(int mode);          /* OFF-GRID | GRID-TIED | HYBRID | FAULT */
float tinhDienApTrungBinh(float v[4]);
int    laQuaAp(float v[4]);                   /* 1 = có chuỗi > 450, 0 = không */
int    laNguyHiem(float temp, float v[4]);
```

### 2.3. Quy tắc nghiệp vụ

| Hàm | Quy tắc | Biên |
|---|---|---|
| `danhGiaNhietDoPin` | `temp < 45` → `"OPTIMAL"`<br>`temp <= 65` → `"HIGH_TEMP"`<br>còn lại → `"CRITICAL_HEAT"` | 45.0 phải ra HIGH_TEMP (**dùng `<`, tuyệt đối không dùng `<=`**)<br>44.9 và 65.0 ra HIGH_TEMP, 65.1 ra CRITICAL_HEAT |
| `layTenInverter` | `1` → `"OFF-GRID"`, `2` → `"GRID-TIED"`, `3` → `"HYBRID"`, `4` → `"FAULT"`, mọi giá trị khác → `"FAULT"` | mode 0 và mode 99 đều ra FAULT |
| `tinhDienApTrungBinh` | `(v0+v1+v2+v3)/4.0f`, duyệt đủ 4 phần tử bằng `for` | |
| `laQuaAp` | 1 nếu bất kỳ chuỗi nào `> 450.0f` | đúng 450.0V **không** quá áp |
| `laNguyHiem` | 1 nếu trạng thái nhiệt là `CRITICAL_HEAT` **HOẶC** `laQuaAp() == 1` | |

Hai điểm **dễ sai nhất** của đề Solar:

1. Ngưỡng là `< 45` chứ không phải `<= 45`.
2. `default` của `layTenInverter` phải trả `"FAULT"`. Học viên hay copy nhầm
   câu `default: return "NORMAL";` từ bài Vios sang.

### 2.4. Dòng output chứa giá trị trung bình

```
Dien ap trung binh: 429.67 V
```

---

## 3. Thuật toán chấm

Mỗi test case gồm 4 bước. Thực hiện theo đúng thứ tự.

### Hai chế độ chấm

Đây là điểm quan trọng nhất của bộ test. Bước 1–3 luôn chạy; **bước 4 chỉ chạy
khi bật `--strict`**.

| | Mặc định — "chạy được" | `--strict` — "chấm chiem" |
|---|---|---|
| Bước 1 biên dịch | ✅ phải biên dịch được | ✅ phải biên dịch được |
| Bước 2 chạy, `rc == 0`, không treo | ✅ | ✅ |
| Có in ra kết quả | ✅ (trừ case thiếu dữ liệu) | ✅ (trừ case thiếu dữ liệu) |
| Bước 4: `expects` / `not_expects` | ❌ không kiểm | ✅ kiểm |
| Bước 4: giá trị trung bình | ❌ không kiểm | ✅ kiểm, sai số 0.06 |

Bật `--strict`:

```
python run_tests.py bai.c --vios --strict
python -m pytest tests/test_vios.py --student=bai.c --strict-grading
```

> ⚠️ **Hệ quả của chế độ mặc định**: 5 hàm viết sai logic hoặc còn nguyên dạng
> `return "TODO"` đều vẫn PASS, miễn là chương trình biên dịch được và chạy
> không lỗi. Bộ chấm mặc định **không phân biệt được bài làm đúng với bài làm
> chưa làm gì**. Nếu mục đích là chấm điểm học viên thì phải dùng `--strict`.
>
> Trường `no_output_ok: True` đánh dấu 2 case thiếu dữ liệu (`16_input_thieu`),
> với các case đó chạy xong mà không in gì vẫn được tính PASS.

### Bước 1 - Biên dịch

```
gcc -std=c99 -O2 -finput-charset=UTF-8 -fexec-charset=UTF-8 -o bai.exe bai.c
```

- `-finput-charset=UTF-8` và `-fexec-charset=UTF-8` là **bắt buộc** trên
  Windows. Nếu thiếu, hệ thống dùng ANSI (cp1252), chuỗi có dấu của học viên sẽ
  thành `?` và không bao giờ khớp được.
- Nếu `returncode != 0` → báo "Biên dịch thất bại" kèm log gcc, dừng.
- Bản dịch lỗi nên kèm gợi ý: thiếu `#include <stdio.h>`/`<string.h>`, sai tên
  hàm so với template, dùng hàm của `conio.h` (`clrscr`, `gotoxy`), thiếu `return`.

### Bước 2 - Chạy

Chạy exe, ghi 7 số của case vào stdin, timeout **10 giây**, thử lại tối đa **3 lần**.

- `returncode != 0` → fail.
- Vòng lặp vô hạn sẽ bị bắt bởi timeout.
- **Phải thử lại**, và phải thử lại cho **cả hai** loại lỗi sau:
  1. **Timeout** — máy đang chạy nặng, hoặc antivirus quét file mới biên dịch.
  2. **`WinError 5` "Access is denied" / `WinError 32`** — Windows khoá tạm thời
     file `.exe` vừa tạo ra, chưa chạy được ngay. Trường hợp này **không phải
     lỗi của học viên**, chỉ là hệ điều hành.
- Không có bước thử lại này thì một bài làm đúng vẫn bị tính là FAIL vì lý do
  máy, đã gặp thật cả hai loại trong quá trình kiểm thử.
- Đọc stdout dưới dạng **bytes**, rồi thử giải mã theo thứ tự
  `utf-8` → `cp1258` → `cp1252` → `latin-1`, lấy encoding **đầu tiên giải mã
  được mà không sinh ký tự thay thế**.

### Bước 3 - Chuẩn hóa output

Áp dụng lần lượt:

1. `lower()`
2. Tách thành phần Unicode (`NFD`) rồi xoá mọi ký tự hạng `Mn` (dấu thanh, dấu huyền…)
3. `đ` → `d` (ký tự U+0111 không tách thành phần được nên phải thay riêng)
4. Mọi ký tự **không** thuộc `[a-z0-9]` → thay bằng một dấu cách
5. Gom nhiều dấu cách liền nhau thành một, cắt đầu cuối

Ví dụ:

| Chuỗi gốc | Sau chuẩn hóa |
|---|---|
| `Trang thai nhiet do: OVERHEAT` | `trang thai nhiet do overheat` |
| `NGUY HIỂM!!!` | `nguy hiem` |
| `nguy hiem` | `nguy hiem` |
| `GRID-TIED` | `grid tied` |
| `Dien ap trung binh: 429.67 V` | `dien ap trung binh 429 67 v` |

Hệ quả: học viên in `NGUY HIỂM`, `Nguy Hiem`, `nguy hiem!!!` đều được chấp nhận.

### Bước 4 - So khớp

Bước này **chỉ chạy khi bật `--strict`**. Xem [Hai chế độ chấm](#hai-chế-độ-chấm).

**4a. Kiểm `expects`** - mỗi từ khóa phải xuất hiện trong output đã chuẩn hóa.
Cả từ khóa cũng được chuẩn hóa trước khi so.

**4b. Kiểm `not_expects`** - mỗi từ khóa phải **không** xuat hiện.

Cả hai dùng so khớp **có biên từ**: `(?<![a-z0-9])` + từ khóa + `(?![a-z0-9])`.
Tức là `qua ap` **không** khớp với `qua ap lao`, nhưng `high` **có** khớp với
`high temp` (vì trong output thật sự có chữ đó).

> Sai lầm cần tránh khi viết test: **không** thêm `"normal"` vào `not_expects`
> của một case mà nhiệt độ ≤ 90. Trạng thái nhiệt `"NORMAL"` luôn xuất hiện
> trong output, nên case đó sẽ fail dù học viên làm đúng. Tương tự `"high"` với
> Solar. Bộ test này đã dùng nhiệt độ 100 (ra `HIGH`) cho các case chỉ kiểm
> chế độ lái để tránh xung đột này.

**4c. Kiểm giá trị trung bình** - chỉ khi case có trường `avg`:

1. Tìm dòng nào trong output có chứa chuỗi `trung binh` (sau chuẩn hóa).
   - Không có dòng nào → fail với thông báo yêu cầu in đúng dòng của template.
2. Với mỗi dòng tìm được, lấy phần sau dấu `:` cuối cùng (tránh con số "4" trong
   chữ "4 banh"); nếu dòng không có `:` thì lấy cả dòng.
3. Trích mọi số thực trong phần đó.
4. Pass nếu **có ít nhất một số** cách giá trị mong đợi không quá **0.06**.

> Sai số 0.06 thay vì 0.01 là cố ý: học viên có thể in `%.1f` thay vì `%.2f`
> mà logic vẫn đúng, không nên phạt. Sai số tuyệt đối lớn nhất do làm tròn
> `%.1f` là 0.05, nên 0.06 là ngưỡng vừa đủ.

> **Không** quét toàn bộ output để tìm số trung bình. Input được in ra bởi chính
> chương trình, nên case `50 50 50 50` (trung bình = 50) sẽ khớp với giá trị
> input đã in và assert trở nên vô nghĩa. Đó là lý do các case trong bộ này
> dùng bộ số phân biệt nhau, ví dụ `402 400 398 400` thay vì `400 400 400 400`.

---

## 4. Bảng test case

Cột `stdin` ghi bằng dấu `/` là xuống dòng, các số trên cùng một dòng là cách
nhập bằng dấu cách.

### 4.1. Đề Vios

| ID | stdin | expects | not_expects | avg |
|---|---|---|---|---|
| `01_normal_an_toan` | `60 / 85 / 1 / 40 41 40 42` | `normal`, `eco`, `an toan`, `binh thuong` | `nguy hiem`, `overheat`, `high`, `qua toc` | 40.75 |
| `02_bien_90_normal` | `50 / 90 / 1 / 50 52 48 50` | `normal`, `eco`, `an toan` | `overheat`, `high`, `nguy hiem`, `qua toc` | 50 |
| `03_bien_90_1_high` | `50 / 90.1 / 1 / 50 52 48 50` | `high`, `eco` | `normal`, `overheat`, `nguy hiem` | 50 |
| `04_bien_105_high` | `50 / 105 / 3 / 50 52 48 50` | `high`, `sport` | `overheat`, `normal`, `eco`, `nguy hiem` | 50 |
| `05_bien_105_1_overheat` | `50 / 105.1 / 2 / 50 52 48 50` | `overheat`, `normal`, `nguy hiem` | `an toan`, `high` | 50 |
| `06_qua_toc_index1` | `80 / 80 / 2 / 40 121 40 40` | `normal`, `qua toc`, `nguy hiem` | `an toan`, `overheat`, `eco`, `sport` | 60.25 |
| `07_bien_120_an_toan` | `80 / 80 / 2 / 118 119 120 120` | `normal`, `an toan`, `binh thuong` | `nguy hiem`, `qua toc`, `overheat` | 119.25 |
| `08_bien_120_1_nguyhiem` | `80 / 80 / 2 / 120.1 100 100 100` | `qua toc`, `nguy hiem` | `an toan`, `binh thuong` | 105.025 |
| `09_qua_toc_index3` | `80 / 80 / 2 / 40 40 40 121` | `qua toc`, `nguy hiem` | `an toan`, `binh thuong` | 60.25 |
| `10_drive_eco` | `60 / 100 / 1 / 40 42 38 40` | `eco`, `high`, `an toan` | `normal`, `sport`, `nguy hiem`, `overheat` | 40 |
| `11_drive_sport` | `60 / 100 / 3 / 40 42 38 40` | `sport`, `high`, `an toan` | `eco`, `normal`, `nguy hiem`, `overheat` | 40 |
| `12_drive_default_99` | `60 / 100 / 99 / 40 42 38 40` | `normal`, `high`, `an toan` | `eco`, `sport`, `nguy hiem`, `overheat` | 40 |
| `13_drive_default_0` | `60 / 100 / 0 / 40 42 38 40` | `normal`, `high`, `an toan` | `eco`, `sport`, `nguy hiem`, `overheat` | 40 |
| `14_combo_full` | `180 / 110 / 3 / 130 125 121 119` | `overheat`, `sport`, `qua toc`, `nguy hiem` | `an toan`, `binh thuong`, `eco` | 123.75 |
| `15_input_mot_dong` | `60 85 1 40 41 40 42` | `normal`, `eco`, `an toan` | `nguy hiem`, `overheat` | 40.75 |
| `16_input_thieu` | `50 / 85 / 2 / 40` | - | `an toan`, `nguy hiem`, `overheat`, `qua toc` | - |
| `avg_chinh_xac` | `60 / 80 / 2 / 40.5 41.0 40.0 40.8` | - | - | 40.575 |

### 4.2. Đề Solar

| ID | stdin | expects | not_expects | avg |
|---|---|---|---|---|
| `01_optimal_an_toan` | `50.5 / 40 / 2 / 380.2 381.5 379.8 382.0` | `optimal`, `grid tied`, `an toan`, `binh thuong` | `nguy hiem`, `critical heat`, `qua ap`, `high temp` | 380.875 |
| `02_bien_45_high_temp` | `50 / 45 / 1 / 402 400 398 400` | `high temp`, `off grid`, `an toan` | `optimal`, `critical heat`, `nguy hiem`, `qua ap` | 400 |
| `03_bien_65_high_temp` | `50 / 65 / 3 / 402 400 398 400` | `high temp`, `hybrid`, `an toan` | `critical heat`, `optimal`, `nguy hiem` | 400 |
| `04_bien_65_1_critical` | `50 / 65.1 / 2 / 402 400 398 400` | `critical heat`, `grid tied`, `nguy hiem` | `an toan`, `high temp`, `optimal`, `qua ap` | 400 |
| `05_qua_ap_mau_slide` | `50 / 40 / 2 / 420.5 418.0 425.2 455.0` | `optimal`, `qua ap`, `nguy hiem` | `an toan`, `binh thuong` | 429.675 |
| `06_bien_450_an_toan` | `50 / 40 / 2 / 450 450 450 450` | `optimal`, `grid tied`, `an toan`, `binh thuong` | `nguy hiem`, `qua ap`, `critical heat` | 450 |
| `07_bien_450_1_nguyhiem` | `50 / 40 / 2 / 450.1 400 400 400` | `qua ap`, `nguy hiem` | `an toan`, `binh thuong` | 412.525 |
| `08_inverter_fault` | `50 / 40 / 4 / 402 400 398 400` | `fault`, `an toan` | `off grid`, `grid tied`, `hybrid`, `nguy hiem` | 400 |
| `09_inverter_offgrid` | `50 / 40 / 1 / 402 400 398 400` | `off grid`, `an toan` | `grid tied`, `hybrid`, `fault`, `nguy hiem` | 400 |
| `10_inverter_hybrid` | `50 / 40 / 3 / 402 400 398 400` | `hybrid`, `an toan` | `off grid`, `grid tied`, `fault`, `nguy hiem` | 400 |
| `11_inverter_default_99` | `50 / 40 / 99 / 402 400 398 400` | `fault`, `an toan` | `off grid`, `grid tied`, `hybrid`, `nguy hiem` | 400 |
| `12_inverter_default_0` | `50 / 40 / 0 / 402 400 398 400` | `fault`, `an toan` | `off grid`, `grid tied`, `hybrid`, `nguy hiem` | 400 |
| `13_combo_full` | `60 / 70 / 4 / 460 470 400 400` | `critical heat`, `fault`, `qua ap`, `nguy hiem` | `an toan`, `binh thuong`, `optimal`, `high temp` | 432.5 |
| `14_input_mot_dong` | `50.5 40 2 420.5 418.0 425.2 455.0` | `optimal`, `grid tied`, `qua ap`, `nguy hiem` | `an toan`, `binh thuong` | 429.675 |
| `15_temp_44_9` | `50 / 44.9 / 2 / 402 400 398 400` | `optimal`, `grid tied`, `an toan` | `high temp`, `critical heat`, `nguy hiem` | 400 |
| `16_input_thieu` | `50 / 40 / 2 / 400` | - | `an toan`, `nguy hiem`, `qua ap`, `critical heat` | - |
| `avg_chinh_xac` | `50 / 40 / 2 / 431.5 428.25 435.0 447.25` | - | - | 435.5 |

### 4.3. Vì sao chọn các giá trị này

| Kỹ thuật chọn input | Lý do |
|---|---|
| Cặp biên `90`/`90.1`, `105`/`105.1` | Bắt lỗi `<` thay cho `<=` |
| Cặp biên `120`/`120.1`, `450`/`450.1` | Bắt lỗi `>=` thay cho `>` |
| Biên `45` và `44.9`, `65` và `65.1` | Bắt lỗi `<= 45` thay cho `< 45` |
| Giá trị vượt ngưỡng đặt ở **index 0, 1, 2 và 3** | Bắt lỗi `for (i = 0; i < 3; i++)` — đề bài yêu cầu duyệt **đủ 4 phần tử**. Chỉ đặt ở index 0 hoặc 1 thì lỗi này lọt. |
| Bộ số `402 400 398 400` thay cho `400 400 400 400` | Trung bình không trùng với giá trị input nào, tránh assert vô nghĩa |
| Mode lạ `0` và `99` cho **cả hai** đề | Bắt lỗi `default` sai, đặc biệt là copy nhầm `"NORMAL"` từ Vios sang Solar |
| Case riêng cho `mode` chỉ kiểm chế độ lái, nhiệt độ đặt `100` | Trạng thái `HIGH` không trùng tên chế độ lái nào, nên `not_expects` kiểm được chính xác |
| Case nhập 7 số trên **một dòng** | Buộc dùng `scanf`; học viên đọc theo dòng sẽ hỏng |
| Case nhập **thiếu dữ liệu** | Không được in kết luận dựa trên biến chưa khởi tạo |
| Mode `2` ở các case nhiệt độ vùng NORMAL | Chấp nhận tên chế độ trùng trạng thái nhiệt; các case đó kiểm biên chứ không kiểm `not_expects` chế độ |

---

## 5. Ma trận coverage

### 5.1. Hàm nào bị case nào bắt

| Hàm | Vios | Solar |
|---|---|---|
| Đánh giá nhiệt độ (`if/else`) | 01, 02, 03, 04, 05 | 01, 02, 03, 04, 15 |
| Tên chế độ (`switch`) | 01, 04, 05, 10, 11, 12, 13 | 01, 02, 03, 04, 08, 09, 10, 11, 12 |
| Trung bình (`for`) | tất cả, riêng `avg_chinh_xac` | tất cả, riêng `avg_chinh_xac` |
| Ngưỡng (`for` + so sánh) | 06, 07, 08, 09, 14 | 05, 06, 07, 13, 14 |
| Kết luận nguy hiểm (`if` + OR) | 05, 06, 08, 09, 14 | 04, 05, 07, 13, 14 |
| Nhập dữ liệu | 15, 16 | 14, 16 |

### 5.2. Những lỗi đã chứng minh bộ test bắt được

Chạy thử trên các bản sửa lỗi cố ý, tất cả đều bị phát hiện **với `--strict`**.
Ở chế độ mặc định thì cả 4 lỗi dưới đây đều PASS, vì không hề kiểm logic:

| Bản sửa | Case fail | Thông báo |
|---|---|---|
| Solar: `default` trả `"NORMAL"` thay vì `"FAULT"` | 11, 12 | `Thiếu từ khóa 'fault'` |
| Solar: `for (i = 0; i < 3; i++)` | 01-07, 13, 15, `avg_chinh_xac` | `Sai giá trị trung bình` |
| Vios: `temp < 90.0f` thay vì `<=` | 02 | `Thiếu từ khóa 'normal'` + `Không được xuất hiện 'high'` |
| Vios: chia 3 thay vì chia 4 | 01-15, `avg_chinh_xac` | `Sai giá trị trung bình` |

Ngược lại, ở **cả hai** chế độ thì lỗi làm chương trình không chạy được đều bị
bắt: không biên dịch được, lỗi runtime (`rc != 0`), treo vòng lặp vô hạn, hoặc
thoát ra mà không in gì.

### 5.3. Cố ý không kiểm

Những điều sau **không** bị phạt, và đây là quyết định có chủ đích:

| Không kiểm | Lý do |
|---|---|
| **Logic 5 hàm (mặc định)** | **Chế độ mặc định cố ý chỉ kiểm "chạy được". Bật `--strict` để kiểm logic** |
| In sai `tocDoXe` / `congSuat` | Đề chỉ yêu cầu xử lý 5 hàm logic; hai số này chỉ đọc rồi in lại |
| Học viên viết lại hàm `main()` / đổi định dạng `printf` | Bị phạt gián tiếp: phải in đúng dòng chứa `trung binh` và giữ các từ khóa đã quy định |
| Dùng `while` thay vì `for`, dùng biến thay vì mảng | Vẫn cho điểm. Muốn phạt thì bật `--check-style` |
| Hardcode kết quả thay vì tính | Không bắt được bằng test black-box. Nếu cần thì `--check-style` soi cấu trúc mã nguồn |
| Học viên in thêm dòng giải thích chứa từ khóa bị cấm | Rất hiếm, chấp nhận rủi ro để đừng phạt oang |

### 5.4. Kiểm tra cấu trúc (`--check-style`)

Tắt mặc định. Bật bằng `--check-style` (pytest) hoặc `--style` (script).
Soi mã nguồn, đòi có `for (`, `switch (`, `if (`. Học viên dùng `while` hoặc
cấu trúc khác vẫn làm bài đúng thì sẽ bị trừ điểm, nên chỉ bật khi muốn chấm
đúng yêu cầu "dùng `for` / `switch` / `if`" của đề.

---

## 6. Các quyết định cố ý

| Quyết định | Nội dung |
|---|---|
| Mode 4 `FAULT` + nhiệt độ và điện áp bình thường | Kết luận là **`AN TOAN`**. Đề chỉ nói nguy hiểm khi `CRITICAL_HEAT` hoặc quá áp. Nếu đề thật có ý khác thì sửa `expects`/`not_expects` của case `08`. |
| Không phân biệt hoa thường / dấu tiếng Việt | Nhờ bước chuẩn hóa. `NGUY HIỂM` = `Nguy Hiem` = `nguy hiem!!!` |
| Không so output chính xác | Chỉ so từ khóa và giá trị trung bình, để học viên tự do trình bày |
| Sai số 0.06 | Chấp nhận in `%.1f` lẫn `%.2f` |
| Cho phép thừa dòng trong output | Không kiểm độ dài dòng, chỉ kiểm từ khóa |
| Timeout 10 giây, thử lại 3 lần (kể cả lỗi `WinError 5`) | Chương trình chỉ đọc 7 số nên chạy trong vài mili giây; thời gian dài là do máy bận, không phải do học viên viết chậm. Vòng lặp vô hạn vẫn bị bắt. `WinError 5` là Windows khoá file `.exe` vừa biên dịch, không phải lỗi bài làm. |
| `not_expects` kiểm tra **mọi** từ khóa | Không có danh sách whitelist. Bản cũ chỉ enforce 3-4 từ nên nhiều case "cấm" thực ra không được kiểm |

---

## 7. Môi trường và cách chạy

### 7.1. Yêu cầu

| Thành phần | Phiên bản | Ghi chú |
|---|---|---|
| gcc | bất kỳ | có trong MinGW-w64, TDM-GCC, MSYS2, hoặc Linux/macOS |
| Python | 3.8+ | |
| pytest | 7.0+ | **không bắt buộc**, chỉ để xem báo cáo đẹp hơn |

Kiểm tra nhanh:

```
gcc --version
python --version
```

### 7.2. Lệnh

Dùng `run_tests.py` (không cần pytest):

```bat
:: Chạy bộ test lấy đáp án mẫu làm chuẩn đối chiếu
python run_tests.py

:: Chấm bài của học viên
python run_tests.py bai_hoa.c --vios
python run_tests.py bai_phuong.c --solar
python run_tests.py "C:\duong\dan\bai.c" --vios

:: Tự đoán đề từ tên file (chứa "vios" hoặc "solar")
python run_tests.py bai_vios_hoa.c

:: Chấm cả một thư mục bài nộp
python run_tests.py --batch "bainop" --vios
python run_tests.py --batch "bainop" --solar
python run_tests.py --batch "bainop" --vios --style

:: Bật chấm chặt (kiểm tra logic 5 hàm + giá trị trung bình)
python run_tests.py bai_hoa.c --vios --strict
python run_tests.py --batch "bainop" --vios --strict --style
```

Dùng pytest (báo cáo chi tiết hơn):

```bat
pytest tests/ -v
pytest tests/test_vios.py -v --student=bai_hoa.c
pytest tests/test_solar.py -v --student=bai_phuong.c --strict-grading
pytest tests/ -v --strict-grading --check-style
```

> **Lưu ý về tên cờ:** `run_tests.py` dùng `--strict`, nhưng **pytest đã dùng sẵn
> `--strict`** cho `--strict-markers` nên không cho đặt trùng. Với pytest phải
> gõ `--strict-grading` (hoặc `--cham-chiem`). Cả hai cờ đều có sẵn dưới dạng
> viết tắt không dấu để dễ gõ: `--cham-chiem`.

### 7.3. Mã thoát

| Mã | Nghĩa |
|---|---|
| 0 | Tất cả PASS |
| 1 | Có ít nhất một FAIL |
| 2 | Lỗi tham số dòng lệnh (thiếu `--vios`/`--solar`, file không tồn tại) |

Dùng mã thoát để lấy điểm tự động trong lớp:

```bat
for %%f in (bainop\*.c) do @python run_tests.py "%%f" --vios > "bainop\%%~nxf.txt"
```

### 7.4. Chấm bằng file `.bat` (cách cho người không rành lệnh)

| File | Việc làm |
|---|---|
| `cham.bat` | Copy `.c` vào `bainop\` → double-click → chọn `1` (chạy được) hoặc `2` (chấm chặt) → đọc màn hình, kết quả lưu `ket_qua.txt` |
| `cham_lop.bat` | Chấm cả lớp, **luôn dùng `--strict`**, kết quả lưu `ket_qua_lop.txt`. Có thể truyền thư mục khác: `cham_lop.bat "C:\path\bainop"` |

`cham.bat` tự tạo thư mục `bainop` ở lần chạy đầu tiên.

Khi bỏ `--vios`/`--solar` mà dùng `--batch`, bộ test **đoán đề cho từng file** từ
tên file (chứa `vios` hoặc `solar`). File không đoán được được **bỏ qua** và liệt
kê ra màn hình để người chấm đổi tên — **không** tính là FAIL, tránh hiểu nhầm
bài học viên làm sai.

Các lỗi mà `cham.bat` tự phát hiện trước khi chạy: không có Python, không có
gcc. Cả hai đều báo rõ cần cài gì.

### 7.5. Bố cục thư mục

```
.
├─ TEST_CASES.md          tài liệu này
├─ README.md              hướng dẫn dùng ngắn
├─ requirements.txt
├─ pytest.ini
├─ cham.bat               double-click để chấm thư mục bài nộp
├─ cham_lop.bat           chấm cả lớp, luôn dùng --strict
├─ run_tests.py           chấm bài, không cần pytest
├─ vios_template.c        file giao cho học viên (đã bỏ đáp án)
├─ solar_template.c       file giao cho học viên (đã bỏ đáp án)
├─ bainop/                thư mục bỏ bài học viên vào (tự tạo, không commit)
└─ tests/
   ├─ cases.py            34 test case + toàn bộ thuật toán chấm
   ├─ conftest.py         biên dịch, chạy exe, hook pytest
   ├─ test_vios.py        17 test Vios
   └─ test_solar.py       17 test Solar
```

Hai file đáp án mẫu `vios_solution.c` và `solar_solution.c` **nằm ngoài repo**.
Khi có chúng, `python run_tests.py` (không tham số) sẽ tự chấm cả hai đề để đối
chiếu — kết quả mong đợi là `34/34` PASS. Nếu không có, lệnh đó sẽ báo hướng
dẫn thay vì chạy. Chấm bài thật thì luôn dùng `--student` hoặc tham số file.

> **Không** đưa `vios_solution.c` / `solar_solution.c` vào kho chung hoặc gửi cho
> học viên. Tương tự, **xoá `drivers_*` và `app.js`** nếu đã đóng gói vào đây.
