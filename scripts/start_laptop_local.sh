#!/usr/bin/env bash
# ==============================================================================
# Smart Home CCTV - Local Laptop Testbench Launcher
# Branch: local (1 Camera - Laptop Webcam /dev/video0)
# ==============================================================================
set -e

echo "======================================================================"
echo "  [LOCAL BRANCH] Smart Home CCTV - Laptop Testbench (1 CCTV /dev/video0)"
echo "======================================================================"

# 1. Verify /dev/video0 webcam exists
if [ ! -e /dev/video0 ]; then
    echo "❌ Error: Webcam device /dev/video0 tidak ditemukan!"
    echo "Pastikan kamera laptop terpasang atau tidak diblokir privasi."
    exit 1
fi
echo "✅ Webcam /dev/video0 terdeteksi."

# 2. Check if venv exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# 3. Ensure MediaMTX RTSP container is running
echo "🚀 Memeriksa MediaMTX container..."
if ! docker inspect -f '{{.State.Running}}' cctv-mediamtx-sim 2>/dev/null | grep -q "true"; then
    docker run -d --name cctv-mediamtx-sim \
      -p 8554:8554 \
      -p 8888:8888 \
      -p 8889:8889 \
      --restart unless-stopped \
      bluenviron/mediamtx:latest
    sleep 2
fi
echo "✅ MediaMTX RTSP Server siap di port 8554 (WebRTC di port 8889)."

# 4. Start local docker compose services (if not already running)
echo "🚀 Memeriksa container core services..."
docker compose -f compose.dokploy.yaml up -d --no-recreate mqtt backend-api dispatcher ai-workers web-dashboard

echo "======================================================================"
echo "  Core Services Berjalan:"
echo "  - Web Dashboard SSR : http://localhost:3000"
echo "  - Backend REST API  : http://localhost:8000"
echo "  - WebRTC Video Live : http://localhost:8889/halaman_depan"
echo "======================================================================"

# 5. Launch webcam RTSP streamer using ffmpeg
echo "🎥 Memulai streaming /dev/video0 ke rtsp://localhost:8554/halaman_depan..."
echo "Tekan Ctrl+C untuk menghentikan webcam stream."

ffmpeg -nostdin -re -f v4l2 -input_format mjpeg -video_size 1280x720 \
  -i /dev/video0 \
  -c:v libx264 -preset ultrafast -tune zerolatency -pix_fmt yuv420p -b:v 1500k \
  -f rtsp -rtsp_transport tcp rtsp://localhost:8554/halaman_depan
