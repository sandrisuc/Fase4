from modelos.entidad_base import EntidadBase, SoftwareFJError
import re

class ClienteInvalidoError(SoftwareFJError):
    """Excepción específica para errores en los datos del cliente."""
    pass

class Cliente(EntidadBase):
    """Clase que representa a un cliente del sistema."""

    def __init__(self, cedula: str, nombre: str, correo: str, telefono: str):
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def cedula(self) -> str:
        return self._cedula

    @cedula.setter
    def cedula(self, valor: str):
        if not valor or not valor.isdigit() or len(valor) < 5:
            raise ClienteInvalidoError(f"Cédula inválida ('{valor}'): debe contener al menos 5 dígitos numéricos.")
        self._cedula = valor

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or len(valor.strip()) < 3:
            raise ClienteInvalidoError(f"Nombre inválido ('{valor}'): debe tener al menos 3 caracteres.")
        self._nombre = valor

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not valor or not re.match(patron, valor):
            raise ClienteInvalidoError(f"Correo electrónico inválido ('{valor}').")
        self._correo = valor

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not valor.isdigit() or len(valor) < 7:
            raise ClienteInvalidoError(f"Teléfono inválido ('{valor}'): mínimo 7 dígitos.")
        self._telefono = valor

    def obtener_detalles(self) -> str:
        return f"Cliente: {self.nombre} | Cédula: {self.cedula} | Correo: {self.correo}"
