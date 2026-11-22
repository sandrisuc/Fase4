from abc import abstractmethod
from modelos.entidad_base import EntidadBase, SoftwareFJError

class ExcepcionServicioError(SoftwareFJError):
    """Excepción específica para errores relacionados con los servicios."""
    pass

class Servicio(EntidadBase):
    """Clase abstracta que representa un servicio ofrecido por el sistema."""

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
        self._codigo = valor

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or len(valor.strip()) < 3:
            raise ExcepcionServicioError("El nombre del servicio debe tener al menos 3 caracteres.")
        self._nombre = valor

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float):
        try:
            val_float = float(valor)
            if val_float < 0:
                raise ExcepcionServicioError(f"La tarifa base no puede ser negativa ('{valor}').")
            self._tarifa_base = val_float
        except (ValueError, TypeError) as e:
            raise ExcepcionServicioError(f"Tarifa base inválida ('{valor}'): debe ser un valor numérico.") from e

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        pass


class ServicioSala(Servicio):
    """Clase que representa el alquiler de una sala."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, incluye_equipos: bool = False):
        super().__init__(codigo, nombre, tarifa_base)
        self.incluye_equipos = incluye_equipos

    def calcular_costo(self, horas: int) -> float:
        try:
            h = int(horas)
            if h <= 0:
                raise ExcepcionServicioError("Las horas de alquiler deben ser mayores a 0.")
        except (ValueError, TypeError) as e:
            raise ExcepcionServicioError(f"Cantidad de horas inválida ('{horas}').") from e
        
        costo = self.tarifa_base * h
        if self.incluye_equipos:
            costo *= 1.15  # 15% adicional si incluye equipos
        return costo

    def obtener_detalles(self) -> str:
        equipos_str = "Sí" if self.incluye_equipos else "No"
        return f"Servicio Sala: {self.nombre} | Código: {self.codigo} | Tarifa Base: ${self.tarifa_base:,.2f} | Equipos: {equipos_str}"


class ServicioEquipo(Servicio):
    """Clase que representa el alquiler de un equipo."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, deposito_garantia: float):
        super().__init__(codigo, nombre, tarifa_base)
        self.deposito_garantia = deposito_garantia

    def calcular_costo(self, dias: int) -> float:
        try:
            d = int(dias)
            if d <= 0:
                raise ExcepcionServicioError("Los días de alquiler deben ser mayores a 0.")
        except (ValueError, TypeError) as e:
            raise ExcepcionServicioError(f"Cantidad de días inválida ('{dias}').") from e
        
        return (self.tarifa_base * d) + self.deposito_garantia

    def obtener_detalles(self) -> str:
        return f"Servicio Equipo: {self.nombre} | Código: {self.codigo} | Tarifa Diario: ${self.tarifa_base:,.2f} | Depósito: ${self.deposito_garantia:,.2f}"


class ServicioAsesoria(Servicio):
    """Clase que representa una asesoría profesional."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, especialidad: str):
        super().__init__(codigo, nombre, tarifa_base)
        self.especialidad = especialidad

    def calcular_costo(self, horas: int, descuento_porcentaje: float = 0.0) -> float:
        try:
            h = int(horas)
            if h <= 0:
                raise ExcepcionServicioError("Las horas de asesoría deben ser mayores a 0.")
        except (ValueError, TypeError) as e:
            raise ExcepcionServicioError(f"Cantidad de horas de asesoría inválida ('{horas}').") from e
        
        subtotal = self.tarifa_base * h
        descuento = subtotal * (descuento_porcentaje / 100.0)
        return subtotal - descuento

    def obtener_detalles(self) -> str:
        return f"Servicio Asesoría: {self.nombre} | Código: {self.codigo} | Especialidad: {self.especialidad} | Tarifa/h: ${self.tarifa_base:,.2f}"
