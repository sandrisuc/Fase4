from modelos.cliente import Cliente, ClienteInvalidoError

if __name__ == "__main__":
    print("=== PROBANDO SISTEMA SOFTWARE FJ ===")
    
    # Prueba 1: Creación correcta de un cliente
    try:
        cliente1 = Cliente("1047400123", "Ana Pérez", "ana.perez@email.com", "3001234567")
        print("Registro exitoso:", cliente1.obtener_detalles())
    except ClienteInvalidoError as err:
        print("Error controlado:", err)

    print("\n--- Probando validaciones estrictas y excepciones ---")
    
    # Prueba 2: Datos inválidos (Debe lanzar excepción y registrar log)
    try:
        cliente_malo = Cliente("123", "Lu", "correo-invalido", "abc")
        print(cliente_malo.obtener_detalles())
    except ClienteInvalidoError as err:
        print("Excepción capturada correctamente:", err)