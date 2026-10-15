# Panduan Pengujian Model AI dengan Kamera Laptop (Branch: `local`)

Dokumen ini menjelaskan alur kerja pengujian sistem Smart Home CCTV pada branch **`local`**, yang dikonfigurasi khusus untuk **1 Kamera (Webcam Laptop `/dev/video0`)**.

Dengan branch ini, pengujian model Face Recognition, deteksi plat nomor (ANPR), dan pengiriman alert Telegram dapat diuji langsung di laptop tanpa memerlukan CCTV fisik (RTSP IP Camera) dan tanpa mengganggu kode branch produksi (`main`).

---

## 1. Arsitektur Lingkungan Lokal

```
[ Laptop Webcam (/dev/video0) ]
              │ (v4l2 via ffmpeg)
              ▼
   [ MediaMTX RTSP Server ] ──▶ RTSP: rtsp://localhost:8554/halaman_depan
              │               ──▶ WebRTC / WHEP: http://localhost:8889/halaman_depan
              ▼
[ SvelteKit Dashboard (Port 3000) ]  ──▶ Browser UI Live Stream & Model Testbench
              │
              ▼
[ AI Workers & Backend API (Port 8000) ] ──▶ YuNet + SFace / DB Whitelist / Telegram
```

---

## 2. Cara Menjalankan Lingkungan Lokal

Cukup jalankan script launcher lokal:
```bash
./scripts/start_laptop_local.sh
```

Script ini otomatis akan:
1. Memverifikasi device webcam `/dev/video0`.
2. Menjalankan container MediaMTX (port 8554, 8888, 8889).
3. Menjalankan container pendukung (Backend API, MQTT, Dispatcher, SvelteKit Dashboard).
4. Melakukan bridging stream webcam laptop `/dev/video0` ke RTSP `rtsp://localhost:8554/halaman_depan`.

---

## 3. Cara Menguji Model AI

### A. Pengujian melalui Dashboard UI
1. Buka browser: `http://localhost:3000`
2. Pada panel **PENGUJIAN MODEL AI** di sebelah kanan:
   - **Test Face Model**: Menguji kecocokan embedding wajah penghuni (cosine threshold 0.36).
   - **Test ANPR TNKB**: Menguji validasi regex dan pencocokan whitelist plat kendaraan keluarga vs asing.
   - **Simulasi Loitering Alert**: Menguji skenario deteksi orang tak dikenal berdiri lebih dari 45 detik.

### B. Pengujian melalui Terminal (Interactive CLI)
Jalankan script test bench:
```bash
# Uji seluruh model (Wajah & Plat)
python3 scripts/test_model_laptop.py

# Uji deteksi wajah dari webcam selama 15 detik
python3 scripts/test_model_laptop.py --mode face --duration 15

# Uji plat kendaraan tertentu
python3 scripts/test_model_laptop.py --mode plate --plate "B 1234 XYZ"
```

---

## 4. Perbedaan Branch `local` vs `main`

| Fitur | Branch `local` | Branch `main` (Production) |
|---|---|---|
| **Kamera CCTV** | 1 Kamera (Webcam laptop `/dev/video0`) | 2 Kamera Fisik (Halaman Depan & Carport RTSP) |
| **Stream Server** | MediaMTX Simulator port 8554/8889 | Frigate NVR + go2rtc H.265 VAAPI Hardware Accel |
| **Tujuan** | Eksperimen & tuning model AI | Deployment server Dokploy / Mini PC produksi |
| **UI Dashboard** | Layout 1-kamera dengan Model Testbench | Multi-grid 2-CCTV dengan dynamic event overlays |
