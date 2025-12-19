# Importar Base primero
from app.config.database import Base

from app.persistence.models.persona import Persona
from app.persistence.models.familia import Familia
from app.persistence.models.miembro_familia import MiembroFamilia
from app.persistence.models.usuario import Usuario

# Exportar todo
__all__ = ['Base', 'Persona', 'Familia', 'MiembroFamilia', 'Usuario']
