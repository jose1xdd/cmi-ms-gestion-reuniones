from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse

from app.ioc.container import get_asistencia_manager
from app.models.inputs.asistencia.asistencia_assing import AssingAsistencia
from app.models.inputs.asistencia.user_asistencia_assing import UserRegisterAsistencia
from app.models.outputs.asistencia.asistencia_persona import AsistenciaIndividual
from app.models.outputs.paginated_response import PaginatedAsistenciaPersonas
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
    data: UserRegisterAsistencia,
    asistencia_manager: AsistenciaManager = Depends(get_asistencia_manager)
):
    response = asistencia_manager.user_register_assistance(reunion_id, data)
    return JSONResponse(content=response.model_dump(exclude_none=True), status_code=201)


@asistencia_router.get(
    "/{reunion_id}/personas",
    response_model=PaginatedAsistenciaPersonas,
    status_code=status.HTTP_200_OK
)
def get_personas_with_asistencia(
    reunion_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
    query: Optional[str] = Query(None, description="Buscar por documento, nombre o apellido"),
    asistencia_manager: AsistenciaManager = Depends(get_asistencia_manager)
):
    return asistencia_manager.get_personas_with_asistencia(
        page=page,
        page_size=page_size,
        reunion_id=reunion_id,
        query=query
    )



@asistencia_router.get(
    "/{reunion_id}/persona/{persona_id}",
    response_model=AsistenciaIndividual,
    status_code=status.HTTP_200_OK
)
def get_personas_with_asistencia(
    reunion_id: int,
    persona_id: int,
    asistencia_manager: AsistenciaManager = Depends(get_asistencia_manager)
):
    return asistencia_manager.get_asistencia_persona(persona_id, reunion_id)
