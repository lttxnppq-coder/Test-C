#include <stdio.h>
#include <string.h>

// ============================================================
// BAI TAP: Giam sat ECU Toyota Vios 2007
// File mau cho hoc vien - chi can dien logic vao 5 ham co TODO
// Thu tu nhap (stdin): tocDoXe, nhietDoDongCo, cheDoLai, 4 toc do banh
// Vi du input: 60 85 2 40 41 40 42
// ============================================================
//
// LUU Y: khong doi thu tu doc bang scanf, khong doi ten ham,
// khong xoa cac dong printf trong main(). Bo test tu dong dua
// input vao va so sanh ket qua.

// ---- HAM 1: danh gia nhiet do ----------------------------------
// Tra ve chuoi trang thai nhiet do: "NORMAL", "HIGH", "OVERHEAT"
// Quy tac:  temp <= 90.0  -> "NORMAL"
//          temp <= 105.0 -> "HIGH"
//          con lai       -> "OVERHEAT"
// Dung if / else if / else. Chu y bien 90.0 va 105.0 van thuoc
// ve nhom dau tien (dung <= chu khong dung <).
const char* danhGiaNhietDo(float temp) {
    // TODO: viet if / else if / else tai day
    (void)temp;
    return "TODO";
}

// ---- HAM 2: lay ten che do lai ----------------------------------
// Quy tac:  1 -> "ECO", 2 -> "NORMAL", 3 -> "SPORT"
//          bat ky gia tri nao khac -> "NORMAL"
// Dung switch / case (co default).
const char* layTenCheDo(int mode) {
    // TODO: viet switch / case tai day
    (void)mode;
    return "TODO";
}

// ---- HAM 3: tinh van toc trung binh 4 banh ----------------------
// Tra ve (w1 + w2 + w3 + w4) / 4.0f
float tinhTocDoTrungBinh(float w1, float w2, float w3, float w4) {
    // TODO: viet phep chia tai day
    (void)w1; (void)w2; (void)w3; (void)w4;
    return 0.0f;
}

// ---- HAM 4: kiem tra co banh nao qua toc khong -----------------
// Tra ve 1 neu co banh nao > 120.0 km/h, nguoc lai 0.
// Dung vong lap for duyet DU 4 phan tu.
// Chuyen 120.0 KHONG lai qua toc (dung > chu khong dung >=).
int laQuaToc(float speeds[4]) {
    // TODO: viet vong lap for tai day
    (void)speeds;
    return 0;
}

// ---- HAM 5: kiem tra canh bao nguy hiem ------------------------
// Tra ve 1 (nguy hiem) neu  temp > 105.0  HOAC  co banh qua toc.
// Nguoc lai tra ve 0 (an toan).
int laNguyHiem(float temp, float speeds[4]) {
    // TODO: viet if tai day, tapn dung ham 4
    (void)temp; (void)speeds;
    return 0;
}

int main(void) {
    float tocDoXe, nhietDo;
    int cheDoLai;
    float banh[4];

    // Nhap du lieu - thu tu co dinh de test tu dong
    // Neu nhap thieu, chuong trinh se ket thuc
    if (scanf("%f", &tocDoXe) != 1) return 0;
    if (scanf("%f", &nhietDo) != 1) return 0;
    if (scanf("%d", &cheDoLai) != 1) return 0;
    for (int i = 0; i < 4; i++) {
        if (scanf("%f", &banh[i]) != 1) return 0;
    }

    // Hien thi lai thong so dau vao
    printf("Toc do xe: %.1f km/h\n", tocDoXe);
    printf("Nhiet do dong co: %.1f C\n", nhietDo);
    printf("Che do lai: %s\n", layTenCheDo(cheDoLai));

    // Danh gia nhiet do
    const char* ttNhiet = danhGiaNhietDo(nhietDo);
    printf("Trang thai nhiet do: %s\n", ttNhiet);
    if (strcmp(ttNhiet, "OVERHEAT") == 0) {
        printf("Canh bao: Nhiet do vuot nguong cho phep!\n");
    }

    // Duyet mang banh xe
    printf("Toc do 4 banh: %.1f %.1f %.1f %.1f km/h\n", banh[0], banh[1], banh[2], banh[3]);
    float avg = tinhTocDoTrungBinh(banh[0], banh[1], banh[2], banh[3]);
    printf("Van toc trung binh 4 banh: %.2f km/h\n", avg);

    if (laQuaToc(banh)) {
        printf("Canh bao: Qua toc! Co banh vuot 120 km/h\n");
    } else {
        printf("Toc do banh xe binh thuong\n");
    }

    // Ket luan an toan
    if (laNguyHiem(nhietDo, banh)) {
        printf("Ket luan: NGUY HIEM\n");
    } else {
        printf("Ket luan: AN TOAN\n");
    }

    return 0;
}
