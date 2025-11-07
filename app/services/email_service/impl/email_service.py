import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.services.email_service.interface.interface_email_service import IEmailService
from app.utils.emails import ASISTENCIA_CONFIRMACION_TEMPLATE


class EmailService(IEmailService):
    def __init__(
        self,
        logger: logging.Logger,
        smtp_server: str,
        smtp_port: int,
        smtp_password: str,
        smtp_email: str,
    ):
        self.logger = logger
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_password = smtp_password
        self.smtp_email = smtp_email

    def _build_message(self, destinatary: str, subject: str, body_html: str) -> MIMEMultipart:
        """Construye el mensaje con HTML."""
        message = MIMEMultipart("alternative")
        message["From"] = self.smtp_email
        message["To"] = destinatary
        message["Subject"] = subject
        message.attach(MIMEText(body_html, "html"))
        return message

    def _send(self, destinatary: str, message: MIMEMultipart):
        """Envía el mensaje usando SMTP."""
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_email, self.smtp_password)
                server.sendmail(self.smtp_email, destinatary, message.as_string())

            self.logger.info(f"Correo enviado a: {destinatary}")
        except Exception as e:
            self.logger.error(f"Error al enviar correo a {destinatary}: {e}")
            raise

    def send_email_asistencia(self,destinatary: str,nombre: str,titulo: str,fecha: str,hora: str,ubicacion: str):
        body_html = (
            ASISTENCIA_CONFIRMACION_TEMPLATE
            .replace("{{nombre}}", nombre)
            .replace("{{titulo}}", titulo)
            .replace("{{fecha}}", fecha)
            .replace("{{hora}}", hora)
            .replace("{{ubicacion}}", ubicacion)
        )

        message = self._build_message(
            destinatary=destinatary,
            subject=f"Confirmación de Asistencia - {titulo}",
            body_html=body_html,
        )
        self._send(destinatary, message)

        self.logger.info(f"[EmailService] ✅ Correo de asistencia enviado a {destinatary}")