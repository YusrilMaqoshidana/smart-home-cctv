# Panduan Konfigurasi Produksi 2 CCTV Fisik (Branch: `main`)

Dokumen ini menjelaskan arsitektur dan panduan konfigurasi **Smart Home CCTV versi Produksi (Branch: `main`)** yang dirancang untuk **2 Kamera CCTV Fisik (RTSP IP Camera)** dengan akselerasi iGPU Intel VAAPI, deteksi Frigate NVR, AI Face Recognition (InsightFace), ALPR (Plat Nomor TNKB Indonesia), dan SvelteKit SSR Dashboard.

---

## 1. Arsitektur Produksi 2 CCTV

```
               [ 2x IP CCTV (RTSP Stream H.264/H.265) ]
                    │                           │
                    │                           │
   [ Cam 1: Halaman Depan & Gerbang ]   [ Cam 2: Carport & Barrier Gate ]
                    │                           │
                    ▼                           ▼
        ┌───────────────────────────────────────────────────┐
        │       Frigate NVR 0.15+ (Hardware Accel VAAPI)    │
        │   - Deteksi Substream (1280x720 @ 7fps)           │
        │   - Perekaman Mainstream (1920x1080 @ 15fps)      │
        │   - go2rtc WebRTC Gateway (Port 8555 / 8554)      │
        └─────────────────────────┬─────────────────────────┘
                                  │ MQTT Topics (frigate/events)
                                  ▼
        ┌───────────────────────────────────────────────────┐
        │            Mosquitto MQTT Broker (Port 1883)      │
        └───────┬───────────────────────────────────┬───────┘
                │                                   │
                ▼                                   ▼
┌──────────────────────────────┐    ┌──────────────────────────────┐
│  AI Workers (Port Internal)  │    │  Dispatcher & Telegram Bot   │
│  - InsightFace (512d Cosine) │    │  - Cooldown & Debounce Logic │
│  - ANPR OCR (Indonesian TNKB)│    │  - Notifikasi Darurat Foto   │
│  - SQLite Database (cctv.db) │    │  - Auto Mute Alarm Keluarga  │
└───────────────┬──────────────┘    └──────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────┐
│  SvelteKit SSR Tactical Dashboard (Port 3000)            │
│  - Multi-Grid 2x2 View untuk 2 CCTV Fisik                │
│  - Dynamic Status & Live Event Log dari Database         │
│  - Manajemen Whitelist Wajah Penghuni & Plat TNKB        │
└──────────────────────────────────────────────────────────┘
```

---

## 2. Alokasi Peran 2 Kamera CCTV

### Kamera 1: `halaman_depan` (Perimeter Gerbang & Teras Depan)
- **Tujuan**: Deteksi orang tak dikenal (*unknown loitering* > 45 detik) dan identifikasi wajah keluarga (*InsightFace / ArcFace*).
- **Zona Deteksi**:
  - `perimeter_gerbang`: Mendeteksi siapa saja yang berada di depan pagar luar.
  - `teras_depan`: Mendeteksi paket kurir atau orang yang melangkah masuk ke teras.
- **RTSP URL Contoh (Dahua/Hikvision/Tapo)**:
  - Substream (Deteksi): `rtsp://user:pass@192.168.1.50:554/h264Preview_01_sub`
  - Mainstream (Rekam): `rtsp://user:pass@192.168.1.50:554/h264Preview_01_main`

### Kamera 2: `carport` (Carport & Barrier Gate)
- **Tujuan**: Deteksi kendaraan masuk, pengenalan plat nomor TNKB Indonesia (*ALPR*), dan pemicu buka portal otomatis (*Barrier Gate GPIO/Relay*).
- **Zona Deteksi**:
  - `area_parkir`: Mendeteksi mobil/motor berhenti di area carport.
  - `pintu_garasi`: Mendeteksi akses ke pintu dalam garasi.
- **RTSP URL Contoh**:
  - Substream (Deteksi): `rtsp://user:pass@192.168.1.51:554/stream2`
  - Mainstream (Rekam): `rtsp://user:pass@192.168.1.51:554/stream1`

---

## 3. Konfigurasi Environment (`.env`)

Pada server produksi, atur file `.env` dengan IP dan kredensial kamera Anda:
```env
# Kredensial Kamera RTSP
FRIGATE_RTSP_USER=admin
FRIGATE_RTSP_PASSWORD=PasswordCCTV123!
CAMERA_FRONT_IP=192.168.1.50
CAMERA_CARPORT_IP=192.168.1.51

# Telegram Security Bot Gateway
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=-100xxxxxxxxxx

# Hardware Storage Path
DATA_STORAGE_PATH=/data/cctv_storage
```

---

## 4. Cara Menjalankan Versi Produksi

Jalankan stack container Dokploy:
```bash
docker compose -f compose.dokploy.yaml up -d --build
```

Setelah seluruh container berjalan:
- Dashboard SvelteKit: **`http://<SERVER_IP>:3000`**
- Frigate NVR Admin: **`http://<SERVER_IP>:5000`**
- Backend REST API: **`http://<SERVER_IP>:8000`**

---

## 5. Perbedaan Cabang Git (`main` vs `local`)

- **`main` (Branch ini)**:
  - Dikhususkan untuk **2 Kamera CCTV Fisik (RTSP)**.
  - Tampilan UI sepenuhnya dinamis (tanpa mock bounding box hardcoded).
  - Terintegrasi dengan Frigate NVR dan akselerasi iGPU Intel VAAPI.
- **`local`**:
  - Dikhususkan untuk **1 Kamera (Laptop Webcam `/dev/video0`)**.
  - Dilengkapi simulator MediaMTX dan interactive model tester CLI untuk validasi AI model di laptop pengembang.
