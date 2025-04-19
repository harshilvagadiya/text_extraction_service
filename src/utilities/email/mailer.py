import aiosmtplib
from email.message import EmailMessage
from typing import Optional
from loguru import logger
from src.config.manager import settings


class MailerError(Exception):
    pass


class Mailer:
    def __init__(
        self,
        server: str = settings.SMTP_SERVER,
        port: int = settings.SMTP_PORT,
        username: str = settings.SMTP_USERNAME,
        password: str = settings.SMTP_PASSWORD,
        from_email: str = settings.SMTP_FROM_EMAIL,
        use_tls: bool = settings.SMTP_USE_TLS,
    ):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.from_email = from_email
        self.use_tls = use_tls

    async def send_email(
        self, to_email: str, subject: str, body: str, html: Optional[str] = None
    ) -> None:
        message = EmailMessage()
        message["From"] = self.from_email
        message["To"] = to_email
        message["Subject"] = subject
        message.set_content(body)

        if html:
            message.add_alternative(html, subtype="html")

        logger.debug(
            f"Attempting to send email to {to_email} via {self.server}:{self.port}"
        )

        try:
            await aiosmtplib.send(
                message,
                hostname=self.server,
                port=self.port,
                username=self.username,
                password=self.password,
                start_tls=self.use_tls,
            )
            logger.info(f"Email sent successfully to {to_email}")
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            raise MailerError(f"Failed to send email to {to_email}") from e


def get_mailer() -> Mailer:
    return Mailer()
