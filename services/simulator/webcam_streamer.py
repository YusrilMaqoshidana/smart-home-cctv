"""Webcam RTSP Simulator Service: Streams laptop webcam /dev/video0 to local RTSP stream for Frigate testing."""

import os
import signal
import subprocess
import sys
import time


def ensure_mediamtx_running():
    """Ensure MediaMTX RTSP container is running."""
    inspect = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.Running}}", "cctv-mediamtx-sim"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if inspect.returncode != 0 or "true" not in inspect.stdout.lower():
        print("Starting MediaMTX RTSP server container...")
        subprocess.run(["docker", "rm", "-f", "cctv-mediamtx-sim"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(
            [
                "docker", "run", "-d",
                "--name", "cctv-mediamtx-sim",
                "-p", "8554:8554",
                "-p", "8888:8888",
                "-p", "8889:8889",
                "bluenviron/mediamtx:latest",
            ],
            check=True,
        )
        time.sleep(2)
        print("MediaMTX RTSP server ready on port 8554.")


def start_ffmpeg_stream():
    """Launch persistent ffmpeg process encoding /dev/video0 to RTSP."""
    cmd = [
        "ffmpeg", "-nostdin", "-re",
        "-f", "v4l2", "-input_format", "mjpeg", "-video_size", "1280x720",
        "-i", "/dev/video0",
        "-c:v", "libx264", "-preset", "ultrafast", "-tune", "zerolatency",
        "-pix_fmt", "yuv420p", "-b:v", "1500k",
        "-f", "rtsp", "-rtsp_transport", "tcp",
        "rtsp://localhost:8554/halaman_depan",
    ]
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    print("=" * 60)
    print("  Smart Home CCTV - Webcam RTSP Stream Simulator")
    print("  Source: /dev/video0 (Laptop Webcam)")
    print("  RTSP Output: rtsp://localhost:8554/halaman_depan")
    print("  WebRTC Live: http://localhost:8889/halaman_depan")
    print("=" * 60)

    ensure_mediamtx_running()

    running = True

    def handle_sig(sig, frame):
        nonlocal running
        print("\nStopping webcam stream...")
        running = False

    signal.signal(signal.SIGINT, handle_sig)
    signal.signal(signal.SIGTERM, handle_sig)

    while running:
        print("Launching webcam ffmpeg stream...")
        proc = start_ffmpeg_stream()
        while running and proc.poll() is None:
            time.sleep(1)

        if proc.poll() is not None and running:
            print(f"FFmpeg process exited with code {proc.returncode}. Restarting in 2s...")
            time.sleep(2)

    if proc and proc.poll() is None:
        proc.terminate()
        proc.wait()
    print("Webcam stream stopped.")


if __name__ == "__main__":
    main()
