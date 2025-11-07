from logging import Logger
from typing import Optional

from app.models.inputs.asistencia.asistencia_assing import AssingAsistencia
from app.models.inputs.asistencia.user_asistencia_assing import UserRegisterAsistencia
from app.models.outputs.asistencia.asistencia_persona import AsistenciaIndividual
from app.models.outputs.paginated_response import PaginatedAsistenciaPersonas
from app.models.outputs.response_estado import EstadoResponse
from app.persistence.models.asistencia import Asistencia
from app.persistence.models.enum import EstadoReunion
from app.persistence.repository.asistencia_repository.interface.interface_asistencia_repository import IAsistenciaRepository
from app.persistence.repository.persona_repository.interface.interface_persona_repository import IPersonaRepository
from app.persistence.repository.reunion_repository.interface.interface_reunion_repository import IReunionRepository
from app.services.email_service.interface.interface_email_service import IEmailService
from app.utils.exceptions_handlers.models.error_response import AppException


class AsistenciaManager:
    def __init__(self, logger: Logger,
                 asistencia_repository: IAsistenciaRepository,
                 reunion_repository: IReunionRepository,
                 persona_repository: IPersonaRepository,
                 email_service: IEmailService):
        self.logger = logger
        self.email_service = email_service
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
        
        if reunion.estado != EstadoReunion.EN_CURSO.value:
            self.logger.warning(
                f"[AsistenciaManager] ⚠️ Reunión ID={reunion_id} no está en curso (estado actual: {reunion.estado.value})"
            )
            raise AppException("Solo se puede registrar asistencia mientras la reunión está EN CURSO")
        
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

    def user_register_assistance(self,reunion_id: int,data: UserRegisterAsistencia) -> EstadoResponse:
        """
        Registra la asistencia de un usuario a una reunión usando su número de documento,
        validando que la reunión esté en curso, y envía un correo de confirmación.
        """
        self.logger.info(f"[AsistenciaManager] 📝 Registro de asistencia - Reunión ID={reunion_id}")

        # 1️⃣ Validar que la reunión exista
        reunion = self.reunion_repository.get(reunion_id)
        if not reunion:
            self.logger.warning(f"[AsistenciaManager] ❌ Reunión ID={reunion_id} no existe")
            raise AppException("No existe esa reunión")

        # 2️⃣ Validar que la reunión esté en curso
        if reunion.estado != EstadoReunion.EN_CURSO.value:
            self.logger.warning(
                f"[AsistenciaManager] ⚠️ Reunión ID={reunion_id} no está en curso (estado actual: {reunion.estado.value})"
            )
            raise AppException("Solo se puede registrar asistencia mientras la reunión está EN CURSO")

        # 3️⃣ Buscar persona por documento
        persona = self.persona_repository.get(data.numero_documento)
        if not persona:
            self.logger.warning(
                f"[AsistenciaManager] ❌ Persona con documento {data.numero_documento} no encontrada"
            )
            raise AppException("No existe ninguna persona con ese número de documento")

        # 4️⃣ Validar si ya registró asistencia
        asistencia_existente = self.asistencia_repository.get_by_reunion_and_persona(
            reunion_id, persona.id
        )
        if asistencia_existente:
            self.logger.info(f"[AsistenciaManager] ⚠️ Ya existe asistencia para persona {persona.id}")
            raise AppException("Ya registraste la asistencia para esta reunión")

        # 5️⃣ Registrar asistencia
        self.asistencia_repository.create(
            Asistencia(asistenteId=persona.id, reunionId=reunion_id)
        )
        self.logger.info(
            f"[AsistenciaManager] ✅ Asistencia creada correctamente (reunión={reunion_id}, persona={persona.id})"
        )

        # Enviar correo de confirmación
        fecha = reunion.fecha.strftime(
            "%d/%m/%Y") if reunion.fecha else "No definida"
        hora = (
            f"{reunion.horaInicio.strftime('%H:%M')} - {reunion.horaFinal.strftime('%H:%M')}"
            if reunion.horaInicio and reunion.horaFinal
            else "No especificada"
        )
        self.email_service.send_email_asistencia(
            destinatary=data.correo_electronico,
            nombre=data.nombre_completo,
            titulo=reunion.titulo or "Reunión Comunitaria",
            fecha=fecha,
            hora=hora,
            ubicacion=reunion.ubicacion or "No especificada",
        )
        
        return EstadoResponse(
            estado="Exitoso",
            message=f"Asistencia registrada exitosamente para {data.nombre_completo}",
        )

    def get_personas_with_asistencia(
        self, page: int,
        page_size: int,
        reunion_id: int,
        numero_documento: Optional[str] = None,
        nombre: Optional[str] = None,
        apellido: Optional[str] = None
    ) -> PaginatedAsistenciaPersonas:
        self.logger.info(
            f"Consultando personas con asistencia: reunion_id={reunion_id}, page={page}, page_size={page_size}"
        )

        # Validar reunión
        reunion = self.reunion_repository.get(reunion_id)
        if reunion is None:
            self.logger.warning(f"Reunión con ID={reunion_id} no existe")
            raise AppException("Reunión no existe")

        result = self.asistencia_repository.get_personas_with_asistencia(
            page=page,
            page_size=page_size,
            reunion_id=reunion_id,
            numero_documento=numero_documento,
            nombre=nombre,
            apellido=apellido
        )

        return result

    def get_asistencia_persona(self, persona_id: int, reunion_id: int) -> AsistenciaIndividual:
        asistencia = self.asistencia_repository.get_by_reunion_and_persona(
            reunion_id, persona_id)
        result = False
        if asistencia is not None:
            result = True
        return AsistenciaIndividual(asistencia_persona=result)
