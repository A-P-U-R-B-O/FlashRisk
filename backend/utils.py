import logging
import os
from typing import Optional

try:
    from twilio.rest import Client as TwilioClient
except ImportError:
    TwilioClient = None

def configure_logging(log_level: str = "INFO"):
    """
    Configures application-wide logging.
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

class NotificationManager:
    """
    Handles sending notifications via various channels (SMS, email, etc.).
    Extend to support push, Slack, etc.
    """
    def __init__(
        self,
        twilio_sid: Optional[str] = None,
        twilio_token: Optional[str] = None,
        twilio_from: Optional[str] = None,
        default_sms_to: Optional[str] = None,
    ):
        self.twilio_sid = twilio_sid or os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_token = twilio_token or os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_from = twilio_from or os.getenv("TWILIO_FROM_NUMBER")
        self.default_sms_to = default_sms_to or os.getenv("DEFAULT_SMS_TO")
        self.twilio_client = None
        if TwilioClient and self.twilio_sid and self.twilio_token:
            self.twilio_client = TwilioClient(self.twilio_sid, self.twilio_token)
        else:
            logging.warning("Twilio not configured. SMS alerts will be disabled.")

    async def notify_all(self, title: str, message: str):
        """
        Send notifications to all configured channels.
        """
        logging.info(f"Notifying users: {title} - {message[:60]}...")
        await self.send_sms_alert(f"{title}\n{message}")
        # Extend here for more channels: email, push, Slack, etc.

    async def send_sms_alert(self, body: str):
        """
        Send an SMS alert using Twilio.
        """
        if not self.twilio_client or not self.twilio_from or not self.default_sms_to:
            logging.warning("SMS notification skipped: Twilio not fully configured.")
            return
        try:
            self.twilio_client.messages.create(
                body=body,
                from_=self.twilio_from,
                to=self.default_sms_to
            )
            logging.info(f"SMS alert sent to {self.default_sms_to}")
        except Exception as e:
            logging.error(f"Failed to send SMS alert: {e}")
