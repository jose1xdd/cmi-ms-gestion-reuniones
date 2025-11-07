from abc import ABC, abstractmethod


class IEmailService(ABC):
    @abstractmethod
    def send_email_asistencia(destinatary: str,nombre: str,titulo: str,fecha: str,hora: str,ubicacion: str):
            pass