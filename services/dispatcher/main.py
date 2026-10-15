"""Main MQTT event dispatcher entrypoint for Smart Home CCTV."""

import json
import logging
import os
import time
from services.common.database import DatabaseManager
from services.ai_workers.face_worker import FaceWorker
from services.ai_workers.anpr_worker import ANPRWorker
from services.dispatcher.telegram_gateway import TelegramGateway
from services.dispatcher.event_dispatcher import EventDispatcher

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def main():
    db_path = os.getenv("DATABASE_PATH", "/app/data/cctv.db")
    mqtt_host = os.getenv("MQTT_HOST", "mqtt")
    mqtt_port = int(os.getenv("MQTT_PORT", "1883"))
    mqtt_topic = os.getenv("MQTT_TOPIC_FRIGATE", "frigate/events")
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    go2rtc_url = os.getenv("GO2RTC_EXTERNAL_URL", "http://localhost:1984")

    logger.info("Starting CCTV Dispatcher Service...")
    logger.info("Database: %s", db_path)
    logger.info("MQTT Broker: %s:%d (Topic: %s)", mqtt_host, mqtt_port, mqtt_topic)

    db = DatabaseManager(db_path)
    face_worker = FaceWorker(db=db)
    anpr_worker = ANPRWorker(db=db)
    telegram_gateway = TelegramGateway(bot_token=bot_token, chat_id=chat_id, go2rtc_url=go2rtc_url)

    dispatcher = EventDispatcher(
        db=db,
        face_worker=face_worker,
        anpr_worker=anpr_worker,
        telegram_gateway=telegram_gateway,
    )

    try:
        import paho.mqtt.client as mqtt

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logger.info("Connected to MQTT Broker successfully.")
                client.subscribe(mqtt_topic)
            else:
                logger.error("Failed to connect to MQTT broker, code %d", rc)

        def on_message(client, userdata, msg):
            try:
                payload = json.loads(msg.payload.decode("utf-8"))
                result = dispatcher.process_frigate_event(payload)
                logger.debug("Processed event: %s", result)
            except Exception as e:
                logger.error("Error processing MQTT message: %s", e)

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        while True:
            try:
                client.connect(mqtt_host, mqtt_port, 60)
                client.loop_forever()
            except Exception as err:
                logger.warning("MQTT connection failed (%s), retrying in 5 seconds...", err)
                time.sleep(5)
    except ImportError:
        logger.warning("paho-mqtt not installed; running in idle standby mode.")
        while True:
            time.sleep(3600)


if __name__ == "__main__":
    main()
