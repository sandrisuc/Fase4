
import logging

from modelos.entidad_base import EntidadBase, SoftwareFJError
from modelos.cliente import Cliente
from modelos.servicio import Servicio, ServicioEquipo


class ReservaInvalidaError(SoftwareFJError):
    """Error personalizado para situaciones inválidas en las reservas."""
    pass


class Reserva(EntidadBase):
    """Representa una reserva de un servicio realizada por un cliente."""

    contador_id = 1

    def __init__(
        self,
        cliente: Cliente,
        servicio: Servicio,
        duracion: int
    ):
        self._id_reserva = f"RES-{Reserva.contador_id:03d}"
        Reserva.contador_id += 1

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion

        # Los equipos se alquilan por días.
        # Las salas y asesorías se manejan por horas.
        if isinstance(servicio, ServicioEquipo):
            self._unidad_duracion = "días"
        else:
            self._unidad_duracion = "horas"

        self._estado = "Pendiente"

        logging.info(
            "Reserva %s creada para el cliente %s.",
            self._id_reserva,
            self.cliente.nombre
        )

    @property
    def id_reserva(self) -> str:
        return self._id_reserva

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @cliente.setter
    def cliente(self, valor: Cliente):
        if not isinstance(valor, Cliente):
            raise ReservaInvalidaError(
                "La reserva debe tener un cliente válido."
            )
        self._cliente = valor

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @servicio.setter
    def servicio(self, valor: Servicio):
        if not isinstance(valor, Servicio):
            raise ReservaInvalidaError(
                "La reserva debe tener un servicio válido."
            )
        self._servicio = valor

    @property
    def duracion(self) -> int:
        return self._duracion

    @duracion.setter
    def duracion(self, valor: int):
        try:
            if isinstance(valor, bool):
                raise ValueError("La duración debe ser un número entero.")

            valor_entero = int(valor)

            if valor_entero <= 0:
                raise ValueError("La duración debe ser mayor que cero.")

            # Evita aceptar valores decimales como 2.5 horas.
            if str(valor).strip() != str(valor_entero):
                raise ValueError("La duración debe ser un número entero.")

            self._duracion = valor_entero

        except (ValueError, TypeError) as error:
            raise ReservaInvalidaError(
                f"Duración inválida ({valor}). Debe ser un entero positivo."
            ) from error

    @property
    def cantidad(self) -> int:
        """Compatibilidad con las pruebas anteriores del proyecto."""
        return self.duracion

    @property
    def unidad_duracion(self) -> str:
        return self._unidad_duracion

    @property
    def estado(self) -> str:
        return self._estado

    def confirmar_reserva(self):
        """Confirma una reserva que se encuentre pendiente."""

        if self.estado == "Confirmada":
            raise ReservaInvalidaError(
                f"La reserva {self.id_reserva} ya está confirmada."
            )

        if self.estado == "Cancelada":
            raise ReservaInvalidaError(
                "No se puede confirmar una reserva cancelada."
            )

        self._estado = "Confirmada"

        logging.info(
            "Reserva %s confirmada correctamente.",
            self.id_reserva
        )

    def cancelar_reserva(self):
        """Cancela una reserva pendiente o confirmada."""

        if self.estado == "Cancelada":
            raise ReservaInvalidaError(
                f"La reserva {self.id_reserva} ya está cancelada."
            )

        self._estado = "Cancelada"

        logging.info(
            "Reserva %s cancelada correctamente.",
            self.id_reserva
        )

    def calcular_costo(self) -> float:
        """Calcula el costo usando la duración de la reserva."""

        try:
            costo = self.servicio.calcular_costo(self.duracion)
            logging.info(
                "Costo calculado para la reserva %s: %.2f",
                self.id_reserva,
                costo
            )
            return costo

        except SoftwareFJError as error:
            logging.exception(
                "No fue posible calcular el costo de la reserva %s.",
                self.id_reserva
            )
            raise ReservaInvalidaError(
                "Error al calcular el costo de la reserva."
            ) from error

    def obtener_detalles(self) -> str:
        return (
            f"ID Reserva: {self.id_reserva} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion} {self.unidad_duracion} | "
            f"Estado: {self.estado}"
        )
