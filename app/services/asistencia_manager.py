from logging import Logger

from app.models.inputs.asistencia.asistencia_assing import AssingAsistencia
from app.models.inputs.asistencia.user_asistencia_assing import UserAssingAsistencia
from app.models.outputs.response_estado import EstadoResponse
from app.persistence.models.asistencia import Asistencia
from app.persistence.repository.asistencia_repository.interface.interface_asistencia_repository import IAsistenciaRepository
from app.persistence.repository.persona_repository.interface.interface_persona_repository import IPersonaRepository
from app.persistence.repository.reunion_repository.interface.interface_reunion_repository import IReunionRepository
from app.utils.exceptions_handlers.models.error_response import AppException


class AsistenciaManager:
    def __init__(self, logger: Logger,
                 asistencia_repository: IAsistenciaRepository,
                 reunion_repository: IReunionRepository,
                 persona_repository: IPersonaRepository):
        self.logger = logger
        self.asistencia_repository = asistencia_repository
        self.reunion_repository = reunion_repository
        self.persona_repository = persona_repository

    def assign_assistance(self, reunion_id: int, data: AssingAsistencia) -> EstadoResponse:
        self.logger.info(
            f"Intentando asignar asistencia: reunion_id={reunion_id}, persona_id={data.persona_id}")

        # Validar que la reunión exista
        reunion = self.reunion_repository.get(reunion_id)
        if reunion is None:
            self.logger.warning(f"Reunión con ID={reunion_id} no existe")
            raise AppException("Reunión no existe")

        asistencia = self.asistencia_repository.get_by_reunion_and_persona(
            reunion_id, data.persona_id)
        if asistencia is not None:
            raise AppException("ya registraste la asistencia")

        # Validar que la persona exista
        persona = self.persona_repository.get(data.persona_id)
        if persona is None:
            self.logger.warning(f"Persona con ID={data.persona_id} no existe")
            raise AppException("Persona a asignar asistencia no existe")

        # Crear asistencia
        self.asistencia_repository.create(Asistencia(
            asistenteId=data.persona_id,
            reunionId=reunion_id
        ))
        self.logger.info(
            f"Asistencia creada correctamente: reunion_id={reunion_id}, persona_id={data.persona_id}")

        return EstadoResponse(estado="Exitoso", message="Asistencia creada exitosamente")

    def delete_assistance(self, reunion_id: int, persona_id: int) -> EstadoResponse:
        self.logger.info(
            f"Intentando eliminar asistencia: reunion_id={reunion_id}, persona_id={persona_id}"
        )

        asistencia = self.asistencia_repository.get_by_reunion_and_persona(
            reunion_id, persona_id
        )
        if asistencia is None:
            self.logger.warning(
                f"No existe asistencia para reunion_id={reunion_id}, persona_id={persona_id}"
            )
            raise AppException("La asistencia no existe")

        self.asistencia_repository.delete(asistencia.id)
        self.logger.info(
            f"Asistencia eliminada correctamente: reunion_id={reunion_id}, persona_id={persona_id}"
        )

        return EstadoResponse(estado="Exitoso", message="Asistencia eliminada exitosamente")

    def user_assing_assistance(self, reunion_id: int, data: UserAssingAsistencia) -> EstadoResponse:
        self.logger.info(
            f"Intentando registrar asistencia con código: reunion_id={reunion_id}, persona_id={data.persona_id}, codigo={data.codigo_asistencia}"
        )
        reunion = self.reunion_repository.get(reunion_id)
        if not reunion:
            self.logger.warning(f"Reunión con ID={reunion_id} no existe")
            raise AppException("No existe esa reunión")

        asistencia = self.asistencia_repository.get_by_reunion_and_persona(
            reunion_id, data.persona_id)
        if asistencia is not None:
            raise AppException("ya registraste la asistencia")

        persona = self.persona_repository.get(data.persona_id)
        if not persona:
            self.logger.warning(f"Persona con ID={data.persona_id} no existe")
            raise AppException("No existe esa persona")

        if reunion.codigoAsistencia is None:
            self.logger.warning(
                f"La reunión ID={reunion_id} no tiene un código de asistencia generado")
            raise AppException("No se ha generado un código de asistencia")

        if data.codigo_asistencia != reunion.codigoAsistencia:
            self.logger.warning(
                f"Código inválido para reunión ID={reunion_id}: recibido={data.codigo_asistencia}, esperado={reunion.codigoAsistencia}"
            )
            raise AppException("Código de asistencia inválido")

        self.asistencia_repository.create(Asistencia(
            asistenteId=data.persona_id,
            reunionId=reunion_id
        ))

        self.logger.info(
            f"Asistencia registrada exitosamente: reunion_id={reunion_id}, persona_id={data.persona_id}"
        )

        return EstadoResponse(estado="Exitoso", message="Asistencia creada exitosamente")
