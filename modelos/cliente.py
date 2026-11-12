import logging
import re
from modelos.entidad_base import EntidadBase

# ==========================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================
class SoftwareFJError(Exception):
    """Excepción base para el sistema de Software FJ."""
    pass

class ClienteInvalidoError(SoftwareFJError):
    """Excepción lanzada cuando los datos del cliente no son válidos."""
    pass

# ==========================================
# CLASE CLIENTE (Encapsulación y Validaciones)
# ==========================================
class Cliente(EntidadBase):
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
        try:
            if not valor or not str(valor).isdigit() or len(str(valor)) < 6:
                raise ValueError("La cédula debe contener solo números y tener al menos 6 dígitos.")
            self._cedula = str(valor)
        except ValueError as e:
            logging.error(f"Error de validación en Cédula: {e}")
            raise ClienteInvalidoError(f"Cédula inválida ({valor}): {e}")

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        try:
            if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
                raise ValueError("El nombre no puede estar vacío y debe tener al menos 3 caracteres.")
            self._nombre = valor.strip()
        except ValueError as e:
            logging.error(f"Error de validación en Nombre: {e}")
            raise ClienteInvalidoError(f"Nombre inválido ({valor}): {e}")

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        try:
            if not valor or not re.match(patron, valor):
                raise ValueError("El formato del correo electrónico no es válido.")
            self._correo = valor
        except ValueError as e:
            logging.error(f"Error de validación en Correo: {e}")
            raise ClienteInvalidoError(f"Correo inválido ({valor}): {e}")

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        try:
            if not valor or not str(valor).isdigit() or len(str(valor)) < 7:
                raise ValueError("El teléfono debe contener solo dígitos y al menos 7 caracteres.")
            self._telefono = str(valor)
        except ValueError as e:
            logging.error(f"Error de validación en Teléfono: {e}")
            raise ClienteInvalidoError(f"Teléfono inválido ({valor}): {e}")

    def obtener_detalles(self) -> str:
        return f"Cliente: {self.nombre} | Cédula: {self.cedula} | Correo: {self.correo} | Teléfono: {self.telefono}"
