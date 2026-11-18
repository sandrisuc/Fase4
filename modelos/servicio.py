from abc import abstractmethod
from modelos.entidad_base import EntidadBase
from functools import singledispatchmethod
import logging

# Configuración básica de logging para el sistema
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")

class ExcepcionServicioError(Exception):
    """Excepción personalizada para errores en la gestión de servicios."""
    pass

class Servicio(EntidadBase):
    """Clase abstracta que representa un servicio en el sistema Software FJ."""
    
    def __init__(self, codigo: str, nombre: str, tarifa_base: float):
        self.codigo = codigo
        self.nombre = nombre
        self.tarifa_base = tarifa_base

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str):
        if not valor or not valor.strip():
            raise ExcepcionServicioError("El código del servicio no puede estar vacío.")
        self._codigo = valor.strip()

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float):
        try:
            val_float = float(valor)
            if val_float < 0:
                raise ValueError("La tarifa base no puede ser negativa.")
            self._tarifa_base = val_float
        except (ValueError, TypeError) as e:
            logging.error(f"Error de validación en Tarifa Base: {e}")
            raise ExcepcionServicioError(f"Tarifa base inválida ({valor}): debe ser un número mayor o igual a 0.") from e

    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        """Método abstracto para el cálculo de costos del servicio."""
        pass

    def obtener_detalles(self) -> str:
        return f"Código: {self.codigo} | Nombre: {self.nombre} | Tarifa Base: ${self.tarifa_base:,.2f}"


class ServicioSala(Servicio):
    """Servicio especializado de alquiler de salas (salas de juntas, coworking)."""
    
    def __init__(self, codigo: str, nombre: str, tarifa_base: float, incluye_equipos: bool = False):
        super().__init__(codigo, nombre, tarifa_base)
        self.incluye_equipos = incluye_equipos

    @singledispatchmethod
    def calcular_costo(self, horas: int):
        """Calcula el costo por horas de la sala."""
        pass

    @calcular_costo.register(int)
    @calcular_costo.register(float)
    def _(self, horas: float):
        if horas <= 0:
            raise ExcepcionServicioError("Las horas de alquiler de la sala deben ser mayores a 0.")
        costo = self.tarifa_base * horas
        if self.incluye_equipos:
            costo += 50000  # Recargo fijo por equipos audiovisuales
        return costo

    @calcular_costo.register(str)
    def _(self, horas_str: str):
        try:
            horas = float(horas_str)
            return self.calcular_costo(horas)
        except ValueError as e:
            raise ExcepcionServicioError(f"Formato de horas inválido para Sala: {horas_str}") from e

    def obtener_detalles(self) -> str:
        base = super().obtener_detalles()
        recargo = "Sí ($50,000 adic.)" if self.incluye_equipos else "No"
        return f"[Sala] {base} | Incluye Equipos: {recargo}"


class ServicioEquipo(Servicio):
    """Servicio especializado de alquiler de equipos y accesorios tecnológicos."""
    
    def __init__(self, codigo: str, nombre: str, tarifa_base: float, deposito_garantia: float):
        super().__init__(codigo, nombre, tarifa_base)
        self.deposito_garantia = deposito_garantia

    @property
    def deposito_garantia(self) -> float:
        return self._deposito_garantia

    @deposito_garantia.setter
    def deposito_garantia(self, valor: float):
        if float(valor) < 0:
            raise ExcepcionServicioError("El depósito de garantía no puede ser negativo.")
        self._deposito_garantia = float(valor)

    def calcular_costo(self, dias: int):
        """Calcula el costo por días de alquiler de equipos más el depósito."""
        if dias <= 0:
            raise ExcepcionServicioError("Los días de alquiler de equipo deben ser mayores a 0.")
        return (self.tarifa_base * dias) + self.deposito_garantia

    def obtener_detalles(self) -> str:
        base = super().obtener_detalles()
        return f"[Equipo] {base} | Depósito de Garantía: ${self.deposito_garantia:,.2f}"


class ServicioAsesoria(Servicio):
    """Servicio especializado de asesorías técnicas o de sistemas."""
    
    def __init__(self, codigo: str, nombre: str, tarifa_base: float, especialidad: str):
        super().__init__(codigo, nombre, tarifa_base)
        self.especialidad = especialidad

    def calcular_costo(self, horas: int, descuento_porcentaje: float = 0.0):
        """Calcula el costo de la asesoría aplicando opcionalmente un porcentaje de descuento."""
        if horas <= 0:
            raise ExcepcionServicioError("Las horas de asesoría deben ser mayores a 0.")
        if not (0 <= descuento_porcentaje <= 100):
            raise ExcepcionServicioError("El porcentaje de descuento debe estar entre 0 y 100.")
        
        subtotal = self.tarifa_base * horas
        descuento = subtotal * (descuento_porcentaje / 100)
        return subtotal - descuento

    def obtener_detalles(self) -> str:
        base = super().obtener_detalles()
        return f"[Asesoría] {base} | Especialidad: {self.especialidad}"
