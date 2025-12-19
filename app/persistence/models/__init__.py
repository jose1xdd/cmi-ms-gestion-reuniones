# Importar Base primero
from app.config.database import Base

# Importar modelos en orden de dependencia
from app.persistence.models.parcialidad import Parcialidad
from app.persistence.models.persona import Persona
from app.persistence.models.familia import Familia
from app.persistence.models.miembro_familia import MiembroFamilia
from app.persistence.models.usuario import Usuario

# Exportar todo
__all__ = ['Base', 'Parcialidad', 'Persona', 'Familia', 'MiembroFamilia', 'Usuario']
