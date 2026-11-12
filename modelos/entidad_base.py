from abc import ABC, abstractmethod

class EntidadBase(ABC):
    """Clase abstracta que representa entidades generales del sistema."""
    
    @abstractmethod
    def obtener_detalles(self) -> str:
        pass
