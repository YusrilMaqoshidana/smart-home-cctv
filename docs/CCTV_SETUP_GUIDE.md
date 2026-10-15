# Panduan Lengkap Konfigurasi Kedatangan CCTV
## Smart Home Surveillance & Anomaly Detection System (Frigate NVR + Dokploy)

Dokumen ini disusun sebagai panduan langkah demi langkah saat perangkat kamera CCTV fisik (Reolink / TP-Link Tapo / Hikvision) tiba besok, agar integrasi ke sistem Frigate NVR, AI worker, dan bot Telegram berjalan lancar dan optimal.

---

## 1. Checklist Pra-Pemasangan

Sebelum memasang kamera secara permanen pada dinding/plafon:
- [ ] Lakukan **uji coba di atas meja (*bench test*)** terlebih dahulu selama 10–15 menit untuk memastikan unit kamera, adaptor/PoE, dan port LAN berfungsi normal.
- [ ] Siapkan kabel LAN (UTP/STP Cat5e atau Cat6) dengan panjang yang sesuai dari titik kamera menuju Switch / Router.
- [ ] Pastikan Anda memiliki akses ke router rumah (alamat gateway, umumnya `192.168.1.1` atau `192.168.0.1`) untuk melihat IP kamera yang terhubung.

---

## 2. Pemasangan Fisik & Sudut Kamera Optimal

Untuk memaksimalkan akurasi deteksi wajah (**InsightFace**) dan plat nomor (**ANPR TNKB**):

```mermaid
graph TD
    subgraph Kamera 1: Halaman Depan & Gerbang
        H1["Ketinggian Ideal: 2.2 – 2.6 meter"]
        A1["Sudut Kemiringan: 15° – 20° ke bawah"]
        F1["Fokus: Area wajah saat orang berjalan dari pagar ke teras"]
    end

    subgraph Kamera 2: Carport & Garasi
        H2["Ketinggian Ideal: 2.2 – 2.5 meter"]
        A2["Sudut Kemiringan: 20° – 30° ke arah plat kendaraan"]
        F2["Fokus: Posisi plat nomor mobil/motor saat berhenti"]
    end
```

> [!TIP]
> **Hindari Sudut Terlalu Curam**: Jika kamera dipasang terlalu tinggi (> 3 meter) dengan sudut menunduk tajam, model wajah hanya akan melihat puncak kepala/topi orang, dan plat nomor kendaraan akan terdistorsi perspektifnya.

---

## 3. Pengaturan Jaringan & IP Statis (DHCP Reservation)

Sistem Frigate NVR membutuhkan alamat IP kamera yang permanen agar koneksi stream RTSP tidak putus saat router restart.

### Langkah-langkah di Router Rumah:
1. Buka browser dan login ke admin panel router (misal `http://192.168.1.1`).
2. Masuk ke menu **DHCP Server** &rarr; **Static Lease / Address Reservation / MAC-to-IP Binding**.
3. Temukan MAC Address dari kedua kamera, lalu pasangkan ke IP tetap:
   - **Kamera 1 (Halaman Depan)**: `192.168.1.101`
   - **Kamera 2 (Carport)**: `192.168.1.102`
4. Simpan konfigurasi router (*Save & Apply*).

---

## 4. Konfigurasi Lokal Kamera (RTSP & Akun Lokal)

Lakukan konfigurasi melalui aplikasi mobile resmi kamera (Reolink App / Tapo App) atau Web Interface kamera melalui browser PC:

### A. Untuk TP-Link Tapo (C325WB / C310 / C320WS)
1. Buka aplikasi **Tapo App** di smartphone.
2. Pilih kamera &rarr; ikon Gerigi (**Device Settings**).
3. Masuk ke **Advanced Settings** &rarr; **Camera Account**.
4. Buat akun lokal kamera:
   - **Username**: `admin`
   - **Password**: Buat password lokal yang kuat (misal `RumahAman2027!`).
5. Format URL RTSP Tapo:
   - **Stream Utama (2K/High)**: `rtsp://admin:password@192.168.1.101:554/stream1`
   - **Sub Stream (720p/Low)**: `rtsp://admin:password@192.168.1.101:554/stream2`

### B. Untuk Reolink (CX410 / RLC-810A / RLC-510A)
1. Buka browser di PC dan ketik IP kamera: `http://192.168.1.101` (atau gunakan Reolink Client App).
2. Masuk ke **Network** &rarr; **Advanced** &rarr; **Server Settings**:
   - Centang **RTSP** (Port 554).
   - Centang **ONVIF** (Port 8000).
3. Masuk ke **Camera** &rarr; **Stream**:
   - **Clear Stream (Main)**: Resolusi 2560x1440 (2K), Frame Rate 20–25 FPS, Bitrate 4096 Kbps.
   - **Fluent Stream (Sub)**: Resolusi 1280x720 (atau 640x360), Frame Rate **7 FPS**, Bitrate 512 Kbps.
4. Format URL RTSP Reolink:
   - **Stream Utama (Main)**: `rtsp://admin:password@192.168.1.101:554/h264Preview_01_main`
   - **Sub Stream (Sub)**: `rtsp://admin:password@192.168.1.101:554/h264Preview_01_sub`

---

## 5. Menghubungkan Kamera ke Frigate NVR

Setelah IP dan akun kamera siap, perbarui file konfigurasi di repositori `smart-home-cctv`:

### Langkah A: Update File `.env`
Buka file `.env` di server atau laptop Anda, sesuaikan nilai kredensial:
```dotenv
FRIGATE_RTSP_USER=admin
FRIGATE_RTSP_PASSWORD=RumahAman2027!
CAMERA_FRONT_IP=192.168.1.101
CAMERA_CARPORT_IP=192.168.1.102
```

### Langkah B: Periksa `configs/frigate/config.yaml`
Pastikan path input RTSP sudah sesuai dengan merek kamera yang Anda gunakan:

```yaml
cameras:
  halaman_depan:
    ffmpeg:
      inputs:
        # Sub-stream untuk inferensi deteksi AI (Sangat hemat komputasi)
        - path: rtsp://{FRIGATE_RTSP_USER}:{FRIGATE_RTSP_PASSWORD}@{CAMERA_FRONT_IP}:554/h264Preview_01_sub # atau /stream2 untuk Tapo
          roles:
            - detect
        # Main-stream untuk rekaman rekaman jernih (2K/4K)
        - path: rtsp://{FRIGATE_RTSP_USER}:{FRIGATE_RTSP_PASSWORD}@{CAMERA_FRONT_IP}:554/h264Preview_01_main # atau /stream1 untuk Tapo
          roles:
            - record
    detect:
      width: 1280
      height: 720
      fps: 7

  carport:
    ffmpeg:
      inputs:
        - path: rtsp://{FRIGATE_RTSP_USER}:{FRIGATE_RTSP_PASSWORD}@{CAMERA_CARPORT_IP}:554/h264Preview_01_sub
          roles:
            - detect
        - path: rtsp://{FRIGATE_RTSP_USER}:{FRIGATE_RTSP_PASSWORD}@{CAMERA_CARPORT_IP}:554/h264Preview_01_main
          roles:
            - record
    detect:
      width: 1280
      height: 720
      fps: 7
```

---

## 6. Verifikasi & Pengujian Sistem

1. **Jalankan Stack Dokploy**:
   ```bash
   docker compose -f compose.dokploy.yaml up -d
   ```
2. **Cek Web UI Dashboard (SvelteKit SSR)**:
   - Buka browser: `http://localhost:3000` (atau domain Dokploy Anda).
   - Pastikan kedua video kamera tampil lancar tanpa freeze.
3. **Uji Coba Deteksi Orang & Notifikasi Telegram**:
   - Berjalanlah melintasi area halaman depan.
   - Pantau grup Telegram **`CCTV Rumah Alert`**: bot akan mengirimkan foto snapshot crop wajah dengan status peringatan jika wajah belum terdaftar.
4. **Daftarkan Wajah via Dashboard**:
   - Buka tab **Wajah Keluarga** di dashboard.
   - Daftarkan nama Anda & anggota keluarga.
   - Lakukan uji coba jalan kembali di depan kamera: sistem kini akan mengenali wajah Anda dan **menekan alarm darurat** (*Family Suppressed*).

---

## 7. Troubleshooting Umum

| Gejala Masalah | Penyebab Umum | Solusi Cepat |
|---|---|---|
| Stream kamera hitam / *Timeout 404* | Password kamera salah atau port RTSP (554) belum aktif di kamera. | Uji buka stream di VLC Player: `Media` &rarr; `Open Network Stream` &rarr; masukkan URL RTSP. |
| Penggunaan CPU mendadak tinggi (> 50%) | Frigate meng-decode video resolusi 2K/4K pada role `detect`. | Pastikan role `detect` hanya mengonsumsi **Sub Stream (720p @ 7 FPS)**, bukan Main Stream. |
| Plat nomor silau/putih total di malam hari | Pantulan lampu inframerah (IR) bawaan kamera memantulkan cat reflektif plat. | Aktifkan mode **Color Night Vision** (lampu ambient warm / F1.0 full color) dan matikan lampu IR hitam-putih. |
| Bot Telegram tidak mengirim pesan | Bot ter-kick dari grup atau ID chat berubah. | Pastikan bot berstatus Admin di grup `CCTV Rumah Alert` dan Chat ID di `.env` adalah `-1003933666444`. |
