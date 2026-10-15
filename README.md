# Smart Home CCTV & Anomaly Detection System (Frigate NVR + ML + Dokploy)

Sistem pengawasan dan deteksi anomali mandiri berbasis **Frigate NVR 0.15+**, **InsightFace**, **Indonesian ANPR (TNKB)**, dan **Dokploy** pada server **Lenovo ThinkCentre M70q** (Intel Core i7-9700T, RAM 32 GB, NVMe 1 TB).

## Struktur Repositori

```text
smart-home-cctv/
├── compose.dokploy.yaml       # Docker Compose terpadu untuk Dokploy
├── .env.example              # Template variabel lingkungan
├── configs/
│   ├── frigate/config.yaml   # Konfigurasi Frigate NVR (preset-vaapi Intel iGPU)
│   └── mosquitto/mosquitto.conf
├── services/
│   ├── common/database.py    # SQLite DatabaseManager, Cosine Vector Matching, Regex TNKB
│   ├── ai_workers/           # FaceWorker, ANPRWorker, AudioWorker
│   ├── dispatcher/           # EventDispatcher & TelegramGateway
│   └── web_dashboard/        # REST API Dashboard & Web UI
└── tests/                    # Unit & E2E Test Suite (18 tests)
```

## Menjalankan Unit & Integration Tests

```bash
PYTHONPATH=. python3 -u -m unittest discover -v -s tests
```
Semua 18 pengujian mencakup:
- Validasi Compose Dokploy (resource limits & passthrough `/dev/dri`).
- Validasi Frigate Config (kamera Halaman Depan & Carport, VAAPI hwaccel).
- Database CRUD & Cosine Similarity matching ($\ge 0.68$).
- Validasi Regex Plat Nomor Indonesia (TNKB).
- Klasifikasi Wajah & Deteksi Loitering (> 45 detik).
- Event Dispatcher Cooldown Debounce (180 detik).
- REST API Dashboard & End-to-End Simulation Pipeline.
