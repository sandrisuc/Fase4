import os
import sys

# Agregamos la carpeta raíz del proyecto al path una sola vez
RAIZ_PROYECTO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if RAIZ_PROYECTO not in sys.path:
    sys.path.insert(0, RAIZ_PROYECTO)

from modelos.cliente import Cliente, ClienteInvalidoError
from modelos.servicio import (
    ExcepcionServicioError,
    ServicioAsesoria,
    ServicioEquipo,
    ServicioSala,
)

# Revisa en modelos/reserva.py cómo se llaman exactamente la clase de reserva y su excepción
try:
    from modelos.reserva import Reserva, ReservaInvalidaError
except ImportError as e:
    print(f"[Aviso import reserva] {e}")
    Reserva = None
    ReservaInvalidaError = Exception


def ejecutar_simulaciones():
    print("=" * 50)
    print("   SISTEMA INTEGRAL SOFTWARE FJ - SIMULACIONES    ")
    print("=" * 50)

    clientes_registrados = []
    servicios_creados = []
    reservas_realizadas = []

    # ==========================================
    # CASOS VÁLIDOS (Operaciones 1 a 5)
    # ==========================================

    print("\n--- [SIMULACIÓN 1] Registro de Cliente Válido ---")
    try:
        c1 = Cliente("1047400123", "Ana Pérez", "ana.perez@email.com", "3001234567")
        clientes_registrados.append(c1)
        print(f"Éxito: Cliente registrado -> {c1.obtener_detalles()}")
    except (ClienteInvalidoError, Exception) as e:
        print(f"Error inesperado: {e}")

    print("\n--- [SIMULACIÓN 2] Creación de Servicio Válido (Sala) ---")
    try:
        s1 = ServicioSala("SAL-01", "Sala A-1", 50000.0, incluye_equipos=True)
        servicios_creados.append(s1)
        costo = s1.calcular_costo(4)
        print(f"Éxito: Servicio creado -> {s1.obtener_detalles()} | Costo (4h): ${costo:,.2f}")
    except (ExcepcionServicioError, Exception) as e:
        print(f"Error inesperado: {e}")

    print("\n--- [SIMULACIÓN 3] Creación de Servicio Válido (Equipo) ---")
    try:
        s2 = ServicioEquipo("EQ-01", "Proyector HD", 20000.0, deposito_garantia=100000.0)
        servicios_creados.append(s2)
        costo = s2.calcular_costo(3)
        print(f"Éxito: Servicio creado -> {s2.obtener_detalles()} | Costo (3 días): ${costo:,.2f}")
    except (ExcepcionServicioError, Exception) as e:
        print(f"Error inesperado: {e}")

    print("\n--- [SIMULACIÓN 4] Creación de Servicio Válido (Asesoría) ---")
    try:
        s3 = ServicioAsesoria("ASE-01", "Consultoría Python", 100000.0, especialidad="Backend")
        servicios_creados.append(s3)
        costo = s3.calcular_costo(2, descuento_porcentaje=10.0)
        print(f"Éxito: Servicio creado -> {s3.obtener_detalles()} | Costo (2h, 10% desc): ${costo:,.2f}")
    except (ExcepcionServicioError, Exception) as e:
        print(f"Error inesperado: {e}")

    print("\n--- [SIMULACIÓN 5] Creación de Reserva Exitosa ---")
    try:
        if Reserva is None:
            raise RuntimeError("Revisa el nombre de la clase en modelos/reserva.py")
        r1 = Reserva(clientes_registrados[0], servicios_creados[0], 2)
        r1.confirmar_reserva()
        reservas_realizadas.append(r1)
        print(f"Éxito: Reserva confirmada -> {r1.obtener_detalles()}")
    except Exception as e:
        print(f"Error en simulación 5: {e}")

    # ==========================================
    # CASOS INVÁLIDOS Y EXCEPCIONES (Operaciones 6 a 10)
    # ==========================================

    print("\n--- [SIMULACIÓN 6] Error: Registro de Cliente Inválido ---")
    try:
        c_malo = Cliente("123", "Lu", "correo-invalido", "abc")
        print(c_malo.obtener_detalles())
    except ClienteInvalidoError as err:
        print(f"Excepción capturada correctamente: {err}")
    except Exception as e:
        print(f"Error general capturado: {e}")

    print("\n--- [SIMULACIÓN 7] Error: Servicio con Tarifa Negativa ---")
    try:
        s_malo = ServicioSala("SAL-02", "Sala B", -50000.0)
        print(s_malo.obtener_detalles())
    except ExcepcionServicioError as err:
        print(f"Excepción capturada correctamente: {err}")
    except Exception as e:
        print(f"Error general capturado: {e}")

    print("\n--- [SIMULACIÓN 8] Error: Horas o Días Inválidos en Cálculo de Costo ---")
    try:
        if not servicios_creados:
            raise RuntimeError("No hay servicios creados para probar cálculo inválido.")
        servicios_creados[0].calcular_costo(-2)
    except ExcepcionServicioError as err:
        print(f"Excepción capturada correctamente: {err}")
    except Exception as e:
        print(f"Error general capturado: {e}")

    print("\n--- [SIMULACIÓN 9] Error: Reserva con Datos Nulos ---")
    try:
        if Reserva is None:
            raise RuntimeError("Revisa el nombre de la clase en modelos/reserva.py")
        servicio_ref = servicios_creados[0] if servicios_creados else None
        r_mala = Reserva(None, servicio_ref, 0)
        r_mala.confirmar_reserva()
    except Exception as e:
        print(f"Excepción capturada correctamente: {e}")

    print("\n--- [SIMULACIÓN 10] Error: Cancelar Reserva Ya Cancelada ---")
    try:
        if Reserva is None or not clientes_registrados or len(servicios_creados) < 2:
            raise RuntimeError("Falta la clase Reserva o servicios para probar cancelación.")
        r2 = Reserva(clientes_registrados[0], servicios_creados[1], 1)
        r2.cancelar_reserva()
        r2.cancelar_reserva()
    except Exception as e:
        print(f"Excepción capturada correctamente: {e}")

    print("\n" + "=" * 50)
    print("  SIMULACIONES FINALIZADAS. REVISA LOS MENSAJES.   ")
    print("=" * 50)


if __name__ == "__main__":
    ejecutar_simulaciones()