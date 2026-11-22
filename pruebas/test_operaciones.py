
import os
import sys
import logging

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
from modelos.reserva import Reserva, ReservaInvalidaError


def ejecutar_simulaciones():
    logging.info("=== INICIO DE SIMULACIONES SISTEMA SOFTWARE FJ ===")
    print("=" * 60)
    print("   SISTEMA INTEGRAL SOFTWARE FJ - SIMULACIONES OFICIALES")
    print("=" * 60)

    clientes_registrados = []
    servicios_creados = []
    reservas_realizadas = []

    # ==========================================
    # CASOS VÁLIDOS (Operaciones 1 a 5) con try / except / else
    # ==========================================

    print("\n--- [SIMULACIÓN 1] Registro de Cliente Válido (try/except/else) ---")
    try:
        c1 = Cliente("1047400123", "Ana Pérez", "ana.perez@email.com", "3001234567")
    except ClienteInvalidoError as e:
        logging.error(f"Simulación 1 falló: {e}")
        print(f"Error controlado: {e}")
    else:
        clientes_registrados.append(c1)
        logging.info(f"Simulación 1 exitosa: {c1.obtener_detalles()}")
        print(f"Éxito (bloque else): Cliente registrado -> {c1.obtener_detalles()}")

    print("\n--- [SIMULACIÓN 2] Creación de Servicio Válido (Sala) ---")
    try:
        s1 = ServicioSala("SAL-01", "Sala A-1", 50000.0, incluye_equipos=True)
        costo = s1.calcular_costo(4)
    except ExcepcionServicioError as e:
        logging.error(f"Simulación 2 falló: {e}")
        print(f"Error controlado: {e}")
    else:
        servicios_creados.append(s1)
        logging.info(f"Simulación 2 exitosa: {s1.obtener_detalles()}")
        print(f"Éxito: {s1.obtener_detalles()} | Costo (4h): ${costo:,.2f}")

    print("\n--- [SIMULACIÓN 3] Creación de Servicio Válido (Equipo) ---")
    try:
        s2 = ServicioEquipo("EQ-01", "Proyector HD", 20000.0, deposito_garantia=100000.0)
        costo = s2.calcular_costo(3)
    except ExcepcionServicioError as e:
        logging.error(f"Simulación 3 falló: {e}")
        print(f"Error controlado: {e}")
    else:
        servicios_creados.append(s2)
        logging.info(f"Simulación 3 exitosa: {s2.obtener_detalles()}")
        print(f"Éxito: {s2.obtener_detalles()} | Costo (3 días): ${costo:,.2f}")

    print("\n--- [SIMULACIÓN 4] Creación de Servicio Válido (Asesoría) ---")
    try:
        s3 = ServicioAsesoria("ASE-01", "Consultoría Python", 100000.0, especialidad="Backend")
        costo = s3.calcular_costo(2, descuento_porcentaje=10.0)
    except ExcepcionServicioError as e:
        logging.error(f"Simulación 4 falló: {e}")
        print(f"Error controlado: {e}")
    else:
        servicios_creados.append(s3)
        logging.info(f"Simulación 4 exitosa: {s3.obtener_detalles()}")
        print(f"Éxito: {s3.obtener_detalles()} | Costo (2h, 10% desc): ${costo:,.2f}")

    print("\n--- [SIMULACIÓN 5] Creación de Reserva Exitosa ---")
    try:
        r1 = Reserva(clientes_registrados[0], servicios_creados[0], 2)
        r1.confirmar_reserva()
    except ReservaInvalidaError as e:
        logging.error(f"Simulación 5 falló: {e}")
        print(f"Error controlado: {e}")
    else:
        reservas_realizadas.append(r1)
        logging.info(f"Simulación 5 exitosa: {r1.obtener_detalles()}")
        print(f"Éxito: Reserva confirmada -> {r1.obtener_detalles()}")

    # ==========================================
    # CASOS INVÁLIDOS (Operaciones 6 a 10) con try / except / finally
    # ==========================================

    print("\n--- [SIMULACIÓN 6] Error: Cédula Inválida (try/except/finally) ---")
    try:
        c_malo = Cliente("123", "Lu", "correo-invalido", "abc")
        print(c_malo.obtener_detalles())
    except ClienteInvalidoError as err:
        logging.warning(f"Simulación 6 - Excepción esperada: {err}")
        print(f"Excepción capturada correctamente: {err}")
    finally:
        print("Bloque finally ejecutado: validación de cliente finalizada.")

    print("\n--- [SIMULACIÓN 7] Error: Servicio con Tarifa Negativa ---")
    try:
        s_malo = ServicioSala("SAL-02", "Sala B", -50000.0)
        print(s_malo.obtener_detalles())
    except ExcepcionServicioError as err:
        logging.warning(f"Simulación 7 - Excepción esperada: {err}")
        print(f"Excepción capturada correctamente: {err}")

    print("\n--- [SIMULACIÓN 8] Error: Horas Inválidas en Cálculo de Costo ---")
    try:
        servicios_creados[0].calcular_costo(-2)
    except ExcepcionServicioError as err:
        logging.warning(f"Simulación 8 - Excepción esperada: {err}")
        print(f"Excepción capturada correctamente: {err}")

    print("\n--- [SIMULACIÓN 9] Error: Reserva con Datos Nulos ---")
    try:
        r_mala = Reserva(None, servicios_creados[0], 0)
        r_mala.confirmar_reserva()
    except ReservaInvalidaError as err:
        logging.warning(f"Simulación 9 - Excepción esperada: {err}")
        print(f"Excepción capturada correctamente: {err}")

    print("\n--- [SIMULACIÓN 10] Error: Doble Cancelación de Reserva (try/except/finally) ---")
    try:
        r2 = Reserva(clientes_registrados[0], servicios_creados[1], 1)
        r2.cancelar_reserva()
        r2.cancelar_reserva()
    except ReservaInvalidaError as err:
        logging.warning(f"Simulación 10 - Excepción esperada: {err}")
        print(f"Excepción capturada correctamente: {err}")
    finally:
        logging.info("=== FIN DE SIMULACIONES SISTEMA SOFTWARE FJ ===")
        print("Bloque finally ejecutado: auditoría de reservas finalizada.")

    print("\n" + "=" * 60)
    print("  SIMULACIONES FINALIZADAS. LOG GUARDADO EN sistema_fj.log")
    print("=" * 60)


if __name__ == "__main__":
    ejecutar_simulaciones()
