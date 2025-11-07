from logging import Logger
from datetime import datetime, time
from app.models.inputs.reunion.reunion_create import ReunionCreate
from app.models.inputs.reunion.reunion_filters import ReunionFilter
from app.models.inputs.reunion.reunion_update import ReunionUpdate
from app.models.outputs.response_estado import EstadoResponse
from app.persistence.models.enum import EstadoReunion
from app.persistence.models.reunion import Reunion
from app.persistence.repository.reunion_repository.interface.interface_reunion_repository import IReunionRepository
from app.utils.exceptions_handlers.models.error_response import AppException
from app.utils.util_functions import generate_code


class ReunionManager:
    def __init__(self, logger: Logger, reunion_repository: IReunionRepository):
        self.logger = logger
        self.reunion_repository = reunion_repository

    def _validar_hora_actual(self, fecha, hora: time, accion: str):
        """Valida que la hora no sea anterior a la actual si la fecha es hoy"""
        ahora = datetime.now()
        if fecha == ahora.date() and hora < ahora.time():
            raise AppException(
                f"No se puede {accion} una reunión con hora anterior a la actual")

    def create(self, data: ReunionCreate) -> EstadoResponse:
        self.logger.info(f"Intentando crear reunión: {data.titulo} "
                         f"[{data.fecha} {data.horaInicio}-{data.horaFinal}]")

        # Validar hora
        self._validar_hora_actual(data.fecha, data.horaInicio, "crear")

        # Validar conflictos
        conflicto = self.reunion_repository.existe_conflicto_reunion(
            fecha=data.fecha,
            hora_inicio=data.horaInicio,
            hora_final=data.horaFinal
        )

        if conflicto:
            self.logger.warning(f"Conflicto detectado al agendar reunión: "
                                f"[{data.fecha} {data.horaInicio}-{data.horaFinal}]")
            raise AppException(
                f"Existe una reunión en ese rango de fechas [{data.fecha} {data.horaInicio}-{data.horaFinal}]")

        # Crear reunión si no hay conflictos
        reunion = self.reunion_repository.create(data)
        self.logger.info(f"Reunión creada exitosamente con ID={reunion.id}")
        return EstadoResponse(estado="Exitoso", message="Reunión creada exitosamente", data=reunion.to_dict())

    def get(self, reunion_id: int) -> Reunion:
        self.logger.info(f"Consultando reunión con ID={reunion_id}")
        reunion = self.reunion_repository.get(reunion_id)
        if not reunion:
            self.logger.warning(f"Reunión con ID={reunion_id} no encontrada")
            raise AppException(
                f"No se encontró la reunión con ID={reunion_id}")
        return reunion

    def get_all(self, page: int, page_size: int, filters: ReunionFilter):
        self.logger.info("Consultando todas las reuniones")
        return self.reunion_repository.find_all_reunion(page, page_size, filters)

    def update(self, reunion_id: int, data: ReunionUpdate) -> EstadoResponse:
        self.logger.info(f"Intentando actualizar reunión ID={reunion_id} "
                         f"con datos: {data}")

        # Validar existencia
        reunion = self.reunion_repository.get(reunion_id)
        if not reunion:
            self.logger.warning(
                f"No se encontró reunión con ID={reunion_id} para actualizar")
            raise AppException(f"No existe reunión con ID={reunion_id}")
        # Validar hora nueva
        self._validar_hora_actual(data.fecha, data.horaInicio, "actualizar")
        conflicto = None
        if (data.horaInicio is not None or data.horaFinal is not None):
            # Validar conflictos
            conflicto = self.reunion_repository.existe_conflicto_reunion(
                fecha=data.fecha,
                hora_inicio=data.horaInicio,
                hora_final=data.horaFinal,
                reunion_id=reunion_id  # para no chocar consigo misma
            )
        if conflicto:
            raise AppException(
                f"Existe una reunión en ese rango de fechas [{data.fecha} {data.horaInicio}-{data.horaFinal}]")

        # Actualizar
        self.reunion_repository.update(reunion_id, data)
        self.logger.info(f"Reunión ID={reunion_id} actualizada correctamente")
        return EstadoResponse(estado="Exitoso", message="Reunión actualizada exitosamente")

    def delete(self, reunion_id: int) -> EstadoResponse:
        self.logger.info(f"Intentando eliminar reunión ID={reunion_id}")

        # Validar existencia
        reunion = self.reunion_repository.get(reunion_id)
        if not reunion:
            self.logger.warning(
                f"No se encontró reunión con ID={reunion_id} para eliminar")
            raise AppException(f"No existe reunión con ID={reunion_id}")

        # Validar hora (no permitir borrar reuniones pasadas de hoy)
        self._validar_hora_actual(
            reunion.fecha, reunion.horaInicio, "eliminar")

        # Eliminar
        self.reunion_repository.delete(reunion_id)
        self.logger.info(f"Reunión ID={reunion_id} eliminada correctamente")
        return EstadoResponse(estado="Exitoso", message="Reunión eliminada exitosamente")
    
    def abrir_reunion(self, reunion_id: int) -> EstadoResponse:
        """
        Cambia el estado de la reunión de PROGRAMADA a EN_CURSO.
        """
        self.logger.info(f"[ReunionManager] Intentando abrir reunión ID={reunion_id}")

        reunion = self.reunion_repository.get(reunion_id)
        if not reunion:
            raise AppException("La reunión no existe")

        if reunion.estado != EstadoReunion.PROGRAMADA.value:
            self.logger.warning(
                f"[ReunionManager] No se puede abrir la reunión ID={reunion_id} porque está en estado {reunion.estado}"
            )
            raise AppException("Solo se pueden abrir reuniones en estado PROGRAMADA")

        reunion_actualizada = self.reunion_repository.update_estado(
            reunion_id, EstadoReunion.EN_CURSO.value
        )

        self.logger.info(
            f"[ReunionManager] ✅ Reunión ID={reunion_id} cambiada a estado EN_CURSO"
        )
        return EstadoResponse(
            estado="Exitoso",
            message=f"La reunión '{reunion_actualizada.titulo}' ha sido abierta correctamente",
        )
    def cerrar_reunion(self, reunion_id: int) -> EstadoResponse:
        """
        Cambia el estado de la reunión de EN_CURSO a CERRADA.
        """
        self.logger.info(f"[ReunionManager] Intentando cerrar reunión ID={reunion_id}")

        reunion = self.reunion_repository.get(reunion_id)
        if not reunion:
            raise AppException("La reunión no existe")

        if reunion.estado != EstadoReunion.EN_CURSO.value:
            self.logger.warning(
                f"[ReunionManager] No se puede cerrar la reunión ID={reunion_id} porque está en estado {reunion.estado}"
            )
            raise AppException("Solo se pueden cerrar reuniones en estado EN_CURSO")

        reunion_actualizada = self.reunion_repository.update_estado(
            reunion_id, EstadoReunion.CERRADA.value
        )

        self.logger.info(
            f"[ReunionManager] ✅ Reunión ID={reunion_id} cambiada a estado CERRADA"
        )
        return EstadoResponse(
            estado="Exitoso",
            message=f"La reunión '{reunion_actualizada.titulo}' ha sido cerrada correctamente",
        )