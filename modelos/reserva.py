from modelos.entidad_base import EntidadBase
from modelos.cliente import Cliente
from modelos.servicio import Servicio
import logging

# Configuración de logs
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")

class ReservaInvalidaError(Exception):
    """Excepción personalizada para errores en la gestión de reservas."""
    pass

class Reserva(EntidadBase):
    """Clase que representa una reserva de un servicio realizada por un cliente."""
    
    contador_id = 1

    def __init__(self, cliente: Cliente, servicio: Servicio, cantidad: int):
        self._id_reserva = f"RES-{Reserva.contador_id:03d}"
        Reserva.contador_id += 1
        
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.estado = "Pendiente"

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @cliente.setter
    def cliente(self, valor: Cliente):
        if not isinstance(valor, Cliente):
            raise ReservaInvalidaError("La reserva debe estar asociada a un objeto Cliente válido.")
        self._cliente = valor

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @servicio.setter
    def servicio(self, valor: Servicio):
        if not isinstance(valor, Servicio):
            raise ReservaInvalidaError("La reserva debe estar asociada a un objeto Servicio válido.")
        self._servicio = valor

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int):
        try:
            val_int = int(valor)
            if val_int <= 0:
                raise ValueError("La cantidad debe ser mayor a 0.")
            self._cantidad = val_int
        except (ValueError, TypeError) as e:
            raise ReservaInvalidaError(f"Cantidad inválida ({valor}): debe ser un entero positivo.") from e

    def confirmar_reserva(self):
        """Confirma la reserva si se encuentra pendiente."""
        if self.estado == "Confirmada":
            raise ReservaInvalidaError(f"La reserva {self._id_reserva} ya se encuentra confirmada.")
        if self.estado == "Cancelada":
            raise ReservaInvalidaError(f"No se puede confirmar una reserva que ya fue cancelada.")
        self.estado = "Confirmada"
        logging.info(f"Reserva {self._id_reserva} confirmada exitosamente.")

    def cancelar_reserva(self):
        """Cancela la reserva activa o pendiente."""
        if self.estado == "Cancelada":
            raise ReservaInvalidaError(f"La reserva {self._id_reserva} ya está cancelada previamente.")
        self.estado = "Cancelada"
        logging.info(f"Reserva {self._id_reserva} cancelada.")

    def obtener_detalles(self) -> str:
        return (f"ID Reserva: {self._id_reserva} | Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} | Cantidad: {self.cantidad} | Estado: {self.estado}")
