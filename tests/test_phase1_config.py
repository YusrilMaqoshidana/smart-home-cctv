"""Test suite for Phase 1: Repository configuration, Dokploy Compose, and Frigate Config."""

import os
import unittest
import yaml

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class TestPhase1Config(unittest.TestCase):
    """Test expectations for Phase 1 configurations."""

    def test_env_example_exists_and_has_required_keys(self):
        """Verify .env.example contains essential configuration keys."""
        env_path = os.path.join(REPO_ROOT, ".env.example")
        self.assertTrue(os.path.isfile(env_path), ".env.example must exist")

        with open(env_path, "r", encoding="utf-8") as f:
            content = f.read()

        required_keys = [
            "FRIGATE_RTSP_USER",
            "FRIGATE_RTSP_PASSWORD",
            "TELEGRAM_BOT_TOKEN",
            "TELEGRAM_CHAT_ID",
            "ENABLE_AUDIO_MODULE",
            "DATA_STORAGE_PATH",
        ]
        for key in required_keys:
            self.assertIn(key, content, f"Key {key} must be present in .env.example")

    def test_dokploy_compose_yaml_validity_and_limits(self):
        """Verify compose.dokploy.yaml has required services, limits, and iGPU device."""
        compose_path = os.path.join(REPO_ROOT, "compose.dokploy.yaml")
        self.assertTrue(os.path.isfile(compose_path), "compose.dokploy.yaml must exist")

        with open(compose_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self.assertIn("services", data, "Compose must have 'services'")
        services = data["services"]

        # 1. Frigate Service
        self.assertIn("frigate", services, "Frigate service must be defined")
        frigate = services["frigate"]
        self.assertIn("image", frigate)
        self.assertIn("ghcr.io/blakeblackshear/frigate", frigate["image"])

        # Check iGPU passthrough
        devices = frigate.get("devices", [])
        has_dri = any("/dev/dri" in dev for dev in devices)
        self.assertTrue(has_dri, "Frigate must have /dev/dri passthrough for Intel iGPU decoding")

        # Check resource limits for M70q coexistence
        deploy = frigate.get("deploy", {})
        resources = deploy.get("resources", {})
        limits = resources.get("limits", {})
        self.assertTrue(limits, "Frigate must have resource limits defined")
        self.assertIn("cpus", limits, "CPU limit must be specified")
        self.assertIn("memory", limits, "Memory limit must be specified")

        # 2. MQTT Service
        self.assertIn("mqtt", services, "MQTT broker service must be defined")

        # 3. Custom services
        self.assertIn("dispatcher", services, "Dispatcher service must be defined")
        self.assertIn("ai-workers", services, "AI workers service must be defined")
        self.assertIn("web-dashboard", services, "Web dashboard service must be defined")

    def test_frigate_config_yaml_validity(self):
        """Verify configs/frigate/config.yaml defines cameras, vaapi hwaccel, and mqtt."""
        config_path = os.path.join(REPO_ROOT, "configs", "frigate", "config.yaml")
        self.assertTrue(os.path.isfile(config_path), "configs/frigate/config.yaml must exist")

        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        # Check MQTT
        self.assertIn("mqtt", config, "MQTT block must be present")
        self.assertEqual(config["mqtt"].get("host"), "mqtt")

        # Check ffmpeg hwaccel
        ffmpeg = config.get("ffmpeg", {})
        hwaccel_args = str(ffmpeg.get("hwaccel_args", ""))
        self.assertIn("vaapi", hwaccel_args.lower(), "Hardware acceleration must use VAAPI for Intel UHD 630")

        # Check cameras
        cameras = config.get("cameras", {})
        self.assertIn("halaman_depan", cameras, "Camera 'halaman_depan' must be configured")
        self.assertIn("carport", cameras, "Camera 'carport' must be configured")

        # Check detect objects
        objects = config.get("objects", {})
        track_list = objects.get("track", [])
        for obj in ["person", "car", "motorcycle"]:
            self.assertIn(obj, track_list, f"Object '{obj}' must be tracked in objects.track")


if __name__ == "__main__":
    unittest.main()
