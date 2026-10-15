"""Telegram Bot Gateway for sending rich CCTV surveillance alerts and handling actions."""

from typing import Any, Dict, List, Optional


class TelegramGateway:
    """Formats and prepares Telegram alerts with photos, emojis, and inline buttons."""

    def __init__(self, bot_token: str, chat_id: str, go2rtc_url: str = "http://localhost:1984"):
        """Initialize TelegramGateway.

        Args:
            bot_token: Telegram Bot Token.
            chat_id: Target Chat or Group ID.
            go2rtc_url: Base URL for camera WebRTC live streaming.
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.go2rtc_url = go2rtc_url

    def build_alert_payload(
        self,
        camera: str,
        title: str,
        description: str,
        alert_level: str = "info",
        photo_path: Optional[str] = None,
        event_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Construct Telegram sendPhoto or sendMessage payload.

        Args:
            camera: Camera name (e.g., 'halaman_depan' or 'carport').
            title: Headline summary.
            description: Detailed context.
            alert_level: 'info', 'warning', or 'emergency'.
            photo_path: Optional file path or URL to snapshot image.
            event_id: Event ID for inline action tracking.

        Returns:
            Dictionary matching Telegram Bot API request body.
        """
        emoji_map = {
            "resident": "🟢",
            "guest": "🟡",
            "courier": "🔵",
            "warning": "🟠",
            "emergency": "🔴",
            "info": "ℹ️",
        }
        status_emoji = emoji_map.get(alert_level, "🔔")
        cam_display = "Halaman Depan" if "halaman" in camera.lower() else "Carport & Garasi"

        caption_text = (
            f"{status_emoji} *{title}*\n"
            f"📍 *Lokasi*: {cam_display}\n"
            f"📝 {description}\n"
        )

        buttons_row_1 = [
            {
                "text": "👋 Tandai Tamu (3 Jam)",
                "callback_data": f"whitelist_guest:{event_id or 'unknown'}",
            },
            {
                "text": "❌ Abaikan",
                "callback_data": f"dismiss:{event_id or 'unknown'}",
            },
        ]

        inline_keyboard: List[List[Dict[str, str]]] = [buttons_row_1]

        # Telegram rejects 'localhost' URLs in inline buttons
        if self.go2rtc_url and self.go2rtc_url.startswith("https://"):
            inline_keyboard.append([
                {
                    "text": "📹 Lihat Live Stream",
                    "url": f"{self.go2rtc_url}/stream.html?src={camera}",
                }
            ])
        else:
            inline_keyboard.append([
                {
                    "text": "📹 Request Snapshot Kamera",
                    "callback_data": f"snapshot:{camera}",
                }
            ])

        payload = {
            "chat_id": self.chat_id,
            "caption": caption_text,
            "parse_mode": "Markdown",
            "reply_markup": {"inline_keyboard": inline_keyboard},
        }

        if photo_path:
            payload["photo"] = photo_path

        return payload
