from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from app.ioc.container import get_reunion_manager
from app.models.inputs.reunion.reunion_create import ReunionCreate
from app.models.inputs.reunion.reunion_filters import ReunionFilter
from app.models.inputs.reunion.reunion_update import ReunionUpdate
from app.models.outputs.paginated_response import PaginatedReunion
from app.models.outputs.response_estado import EstadoResponse
from app.models.outputs.reunion.reunion_out import ReunionOut
from app.services.reunion_manager import ReunionManager


reunion_router = APIRouter(prefix="/reunion", tags=["Reunion"])


@reunion_router.post(
    "/create",
    response_model=EstadoResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_reunion(
    data: ReunionCreate,
    manager: ReunionManager = Depends(get_reunion_manager)
):
    response = manager.create(data)
    return JSONResponse(content=response.model_dump(exclude_none=True), status_code=201)


@reunion_router.get(
    "/{reunion_id}",
    response_model=ReunionOut,
    status_code=status.HTTP_200_OK
)
def obtener_reunion(
    reunion_id: int,
    manager: ReunionManager = Depends(get_reunion_manager)
):
    return manager.get(reunion_id)


@reunion_router.get(
    "/",
    response_model=PaginatedReunion,
    status_code=status.HTTP_200_OK
)
def listar_reuniones(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
    filters: ReunionFilter = Depends(),
    manager: ReunionManager = Depends(get_reunion_manager)
):
    return manager.get_all(page, page_size, filters.model_dump(exclude_none=True))


@reunion_router.put(
    "/{reunion_id}",
    response_model=EstadoResponse,
    status_code=status.HTTP_200_OK
)
def actualizar_reunion(
    reunion_id: int,
    data: ReunionUpdate,
    manager: ReunionManager = Depends(get_reunion_manager)
):
    response = manager.update(reunion_id, data)
    return JSONResponse(content=response.model_dump(exclude_none=True), status_code=200)


@reunion_router.delete(
    "/{reunion_id}",
    response_model=EstadoResponse,
    status_code=status.HTTP_200_OK
)
def eliminar_reunion(
    reunion_id: int,
    manager: ReunionManager = Depends(get_reunion_manager)
):
    response = manager.delete(reunion_id)
    return JSONResponse(content=response.model_dump(exclude_none=True), status_code=200)

@reunion_router.patch(
    "/{reunion_id}/abrir",
    status_code=status.HTTP_200_OK,
    response_model=EstadoResponse,
    summary="Abre una reunión (PROGRAMADA → EN_CURSO)"
)
def abrir_reunion(
    reunion_id: int,
    manager: ReunionManager = Depends(get_reunion_manager),
):
    return manager.abrir_reunion(reunion_id)


@reunion_router.patch(
    "/{reunion_id}/cerrar",
    status_code=status.HTTP_200_OK,
    response_model=EstadoResponse,
    summary="Cierra una reunión (EN_CURSO → CERRADA)"
)
def cerrar_reunion(
    reunion_id: int,
    manager: ReunionManager = Depends(get_reunion_manager),
):
    return manager.cerrar_reunion(reunion_id)