from abc import ABC, abstractmethod
import logging

# Configuración UNICA de logs hacia un archivo físico (Pide el profesor)
logging.basicConfig(
    filename="sistema_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    encoding="utf-8"
)

class SoftwareFJError(Exception):
    """Excepción base unificada para todo el sistema (Pide el profesor)."""
    pass

class EntidadBase(ABC):
    """Clase abstracta que representa entidades generales del sistema."""

    @abstractmethod
    def obtener_detalles(self) -> str:
        pass
