from logging import Logger
from datetime import datetime, time
from app.models.inputs.reunion.reunion_create import ReunionCreate
from app.models.inputs.reunion.reunion_filters import ReunionFilter
from app.models.inputs.reunion.reunion_update import ReunionUpdate
from app.models.outputs.response_estado import EstadoResponse
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

    def get_all(self, page: int, page_size: int, filters: ReunionFilter) -> list[Reunion]:
        self.logger.info("Consultando todas las reuniones")
        return self.reunion_repository.find_all_reunion(page, page_size, filters)

    def update(self, reunion_id: int, data: ReunionUpdate) -> EstadoResponse:
        self.logger.info(f"Intentando actualizar reunión ID={reunion_id} "
                         f"con datos: {data}")

        # Validar hora
        self._validar_hora_actual(data.fecha, data.horaInicio, "actualizar")

        # Validar existencia
        reunion = self.reunion_repository.get(reunion_id)
        if not reunion:
            self.logger.warning(
                f"No se encontró reunión con ID={reunion_id} para actualizar")
            raise AppException(f"No existe reunión con ID={reunion_id}")

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

    def generate_asistencia_code(self, reunion_id: int) -> EstadoResponse:
        self.logger.info(
            f"Generando código de asistencia para reunión ID={reunion_id}")

        reunion = self.reunion_repository.get(reunion_id)
        if not reunion:
            self.logger.warning(
                f"No se encontró la reunión con ID={reunion_id}")
            raise AppException(
                f"No se encontró reunión con el ID={reunion_id}")

        codigo = generate_code()
        reunion.codigoAsistencia = codigo
        self.reunion_repository.update(reunion_id, reunion)

        self.logger.info(
            f"Código de asistencia generado exitosamente para reunión ID={reunion_id}: {codigo}"
        )

        return EstadoResponse(
            estado="Exitoso",
            message="Código de reunión actualizado exitosamente",
            data={"codigo": codigo}
        )

    def delete_asistencia_code(self, reunion_id: int) -> EstadoResponse:
        self.logger.info(
            f"eliminando código de asistencia para reunión ID={reunion_id}")

        reunion = self.reunion_repository.get(reunion_id)
        if not reunion:
            self.logger.warning(
                f"No se encontró la reunión con ID={reunion_id}")
            raise AppException(
                f"No se encontró reunión con el ID={reunion_id}")
        reunion.codigoAsistencia = None
        self.update(reunion_id, reunion)

        self.logger.info(
            f"Código de asistencia eliminado exitosamente para reunión ID={reunion_id}"
        )
        return EstadoResponse(
            estado="Exitoso",
            message="Código de reunión actualizado exitosamente"
        )
