Sistema Integral de Clientes, Servicios y Reservas - Software FJ

Descripcion del Proyecto
Sistema orientado a objetos desarrollado en Python para la empresa Software FJ. Permite gestionar clientes, servicios (salas, equipos y asesorias) y reservas de manera estable y robusta, implementando un manejo avanzado de excepciones, herencia, polimorfismo y encapsulacion sin el uso de bases de datos.

Integrantes del Grupo
- Sandra Marcela (Lider)
- Luis Argel (Desarrollador 1)
- Rafael Coneo (Desarrollador 2)
- Andrés Leones (Desarrollador 3)
- Erick Moscote (Desarrollador 4)

Estructura de Modulos y Asignacion de Tareas (Issues)

1. Modulo de Clientes y Excepciones Base (modelos/cliente.py)
   - Descripcion: Gestion de datos personales, encapsulacion con propiedades, validaciones estrictas de cedula, correo y telefono, y definicion de excepciones personalizadas.
   - Estado: Desarrollado (Asignado a Sandra Marcela).

2. Modulo de Servicios y Clases Abstractas (modelos/servicio.py)
   - Descripcion: Creacion de la clase abstracta Servicio y servicios especializados aplicando polimorfismo y metodos de costos.
   - Estado: Disponible para asignacion (Luis Argel).

3. Modulo de Reservas y Validaciones (modulos/reserva.py)
   - Descripcion: Clase Reserva que integra cliente, servicio y estados, implementando manejo de excepciones.
   - Estado: Disponible para asignacion (Rafael Coneo).

4. Modulo de Registro de Logs y Errores (sistema_errores.log)
   - Descripcion: Sistema centralizado para capturar y registrar automaticamente todos los eventos y errores en tiempo de ejecucion.
   - Estado: Disponible para asignacion (Andrés Leones).

5. Modulo de Pruebas y Simulacion (pruebas/test_operaciones.py)
   - Descripcion: Script encargado de simular al menos 10 operaciones completas para demostrar la estabilidad del programa.
   - Estado: Disponible para asignacion (Erick Moscote).

Instrucciones de Ejecucion
1. Clonar el repositorio.
2. Ejecutar el archivo principal mediante la terminal:
   python main.py
