import logging
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.persistence.repository.asistencia_repository.interface.interface_asistencia_repository import IAsistenciaRepository
from app.persistence.repository.persona_repository.interface.interface_persona_repository import IPersonaRepository
from app.persistence.repository.repository_factory import RepositoryFactory
from app.persistence.repository.reunion_repository.interface.interface_reunion_repository import IReunionRepository
from app.services.asistencia_manager import AsistenciaManager
from app.services.email_service.impl.email_service import EmailService
from app.services.reunion_manager import ReunionManager
from app.utils.enviroment import settings


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["app.ioc.container"])

    logger = providers.Singleton(logging.getLogger, __name__)

    email_service = providers.Factory(
        EmailService,
        logger=logger,
        smtp_server=settings.smtp_server,
        smtp_port=settings.smtp_port,
        smtp_password=settings.smtp_password,
        smtp_email=settings.smtp_email
    )


@inject
def get_reunion_manager(
    db: Session = Depends(get_db),
    logger: logging.Logger = Depends(Provide[Container.logger]),
) -> ReunionManager:
    factory = RepositoryFactory(db=db)
    reunion_repository: IReunionRepository = factory.get_repository(
        IReunionRepository)
    return ReunionManager(logger, reunion_repository)


@inject
def get_asistencia_manager(
    db: Session = Depends(get_db),
    logger: logging.Logger = Depends(Provide[Container.logger]),
    email_service=Depends(Provide[Container.email_service])
) -> AsistenciaManager:
    factory = RepositoryFactory(db=db)
    reunion_repository: IReunionRepository = factory.get_repository(
        IReunionRepository)
    asistencia_repository: IAsistenciaRepository = factory.get_repository(
        IAsistenciaRepository)
    persona_repository: IPersonaRepository = factory.get_repository(
        IPersonaRepository)
    return AsistenciaManager(logger, asistencia_repository, reunion_repository, persona_repository, email_service)
