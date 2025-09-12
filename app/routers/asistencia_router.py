from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.ioc.container import get_asistencia_manager
from app.models.inputs.asistencia.asistencia_assing import AssingAsistencia
from app.models.inputs.asistencia.user_asistencia_assing import UserAssingAsistencia
from app.models.outputs.response_estado import EstadoResponse
from app.services.asistencia_manager import AsistenciaManager


asistencia_router = APIRouter(prefix="/asistencia", tags=["Asistencia"])


@asistencia_router.post(
    "/assign/{reunion_id}",
    response_model=EstadoResponse,
    status_code=status.HTTP_201_CREATED
)
def assign_asistencia(
    reunion_id: int,
    data: AssingAsistencia,
    asistencia_manager: AsistenciaManager = Depends(get_asistencia_manager)
):
    response = asistencia_manager.assign_assistance(reunion_id, data)
    return JSONResponse(content=response.model_dump(exclude_none=True), status_code=201)


@asistencia_router.delete(
    "/{reunion_id}/{persona_id}",
    response_model=EstadoResponse,
    status_code=status.HTTP_200_OK
)
def delete_asistencia(
    reunion_id: int,
    persona_id: int,
    asistencia_manager: AsistenciaManager = Depends(get_asistencia_manager)
):
    response = asistencia_manager.delete_assistance(reunion_id, persona_id)
    return JSONResponse(content=response.model_dump(exclude_none=True), status_code=200)

@asistencia_router.post(
    "/user-assign/{reunion_id}",
    response_model=EstadoResponse,
    status_code=status.HTTP_201_CREATED
)
def user_assign_asistencia(
    reunion_id: int,
    data: UserAssingAsistencia,
    asistencia_manager: AsistenciaManager = Depends(get_asistencia_manager)
):
    response = asistencia_manager.user_assing_assistance(reunion_id, data)
    return JSONResponse(content=response.model_dump(exclude_none=True), status_code=201)
