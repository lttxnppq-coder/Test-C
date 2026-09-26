#include <stdio.h>
#include <string.h>

// ============================================================
// BAI TAP: Giam sat Tram Dien Mat Troi Ap Mai
// File mau cho hoc vien - chi can dien logic vao 5 ham co TODO
// Thu tu nhap (stdin): congSuat (kW), nhietDoPin (C), cheDoInverter (1-4), 4 dien ap chuoi (V)
// Vi du input: 50.5 40 2 420.5 418.0 425.2 455.0
// ============================================================
//
// LUU Y: khong doi thu tu doc bang scanf, khong doi ten ham,
// khong xoa cac dong printf trong main(). Bo test tu dong dua
// input vao so sanh ket qua.

// ---- HAM 1: danh gia nhiet do pin -------------------------------
// Tra ve "OPTIMAL", "HIGH_TEMP" hoac "CRITICAL_HEAT"
// Quy tac:  temp < 45.0   -> "OPTIMAL"
//          temp <= 65.0  -> "HIGH_TEMP"
//          con lai        -> "CRITICAL_HEAT"
// CHI Y RAT QUAN TRONG: nguong la < 45 chu khong phai <= 45,
// nen 45.0 phai ra HIGH_TEMP. Dung if / else if / else.
const char* danhGiaNhietDoPin(float temp) {
    // TODO: viet if / else if / else tai day
    (void)temp;
    return "TODO";
}

// ---- HAM 2: lay ten che do inverter ------------------------------
// Quy tac:  1 -> "OFF-GRID", 2 -> "GRID-TIED", 3 -> "HYBRID", 4 -> "FAULT"
//          bat ky gia tri nao khac -> "FAULT"
// Dung switch / case (co default).
// CHI Y: default phai la "FAULT", KHONG phai "NORMAL".
const char* layTenInverter(int mode) {
    // TODO: viet switch / case tai day
    (void)mode;
    return "TODO";
}

// ---- HAM 3: tinh dien ap trung binh 4 chuoi ---------------------
// Tra ve (v0 + v1 + v2 + v3) / 4.0f
// Dung vong lap for duyet DU 4 phan tu.
float tinhDienApTrungBinh(float v[4]) {
    // TODO: viet vong lap for tai day
    (void)v;
    return 0.0f;
}

// ---- HAM 4: kiem tra co chuoi nao qua ap khong ------------------
// Tra ve 1 neu co chuoi nao > 450.0V, nguoc lai 0.
// Dung vong lap for duyet DU 4 phan tu.
// Chuyen 450.0V KHONG lai qua ap (dung > chu khong dung >=).
int laQuaAp(float v[4]) {
    // TODO: viet vong lap for tai day
    (void)v;
    return 0;
}

// ---- HAM 5: kiem tra trang thai an toan chung -------------------
// Tra ve 1 (nguy hiem) neu  nhiet do pin >= CRITICAL_HEAT  HOAC  co chuoi qua ap.
// Nguoc lai tra ve 0 (an toan).
// CHI Y: che do FAULT khong lam cho ket luan la NGUY HIEM.
// De chi bat NGUY HIEM khi CRITICAL_HEAT hoac qua ap.
int laNguyHiem(float temp, float v[4]) {
    // TODO: viet if tai day, tapn dung ham 1 va ham 4
    (void)temp; (void)v;
    return 0;
}

int main(void) {
    float congSuat, nhietDo;
    int cheDo;
    float dienAp[4];

    if (scanf("%f", &congSuat) != 1) return 0;
    if (scanf("%f", &nhietDo) != 1) return 0;
    if (scanf("%d", &cheDo) != 1) return 0;
    for (int i = 0; i < 4; i++) {
        if (scanf("%f", &dienAp[i]) != 1) return 0;
    }

    // Bao cao chi tiet dang bang
    printf("Cong suat phat: %.2f kW\n", congSuat);
    printf("Nhiet do pin: %.1f C\n", nhietDo);
    printf("Trang thai nhiet do: %s\n", danhGiaNhietDoPin(nhietDo));
    printf("Che do Inverter: %s\n", layTenInverter(cheDo));
    printf("Dien ap 4 chuoi: %.1f %.1f %.1f %.1f V\n", dienAp[0], dienAp[1], dienAp[2], dienAp[3]);

    float avg = tinhDienApTrungBinh(dienAp);
    printf("Dien ap trung binh: %.2f V\n", avg);

    if (laQuaAp(dienAp)) {
        printf("Canh bao: Qua ap! Co chuoi vuot 450V\n");
    } else {
        printf("Dien ap cac chuoi binh thuong\n");
    }

    if (laNguyHiem(nhietDo, dienAp)) {
        printf("Ket luan: NGUY HIEM\n");
    } else {
        printf("Ket luan: AN TOAN\n");
    }

    // Them canh bao neu cheDo FAULT
    if (cheDo == 4) {
        printf("Trang thai: FAULT - Can kiem tra he thong\n");
    }

    return 0;
}
