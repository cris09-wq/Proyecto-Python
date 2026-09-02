"""
Módulo main.py
Punto de entrada de la aplicación DriveSafe.
Muestra el menú principal y llama a las funciones de los otros módulos.
"""

import os
from clientes import (
    registrar_cliente,
    consultar_clientes,
    registrar_instructor,
    consultar_instructores
)
from vehiculos import (
    registrar_vehiculo,
    consultar_vehiculos
)
from citas import (
    programar_cita,
    consultar_citas,
    registrar_asistencia,
    historial_por_cliente
)


def crear_carpeta_data():
    """Crea la carpeta data/ si todavía no existe, para poder guardar los archivos."""
    if not os.path.exists("data"):
        os.makedirs("data")


def mostrar_menu():
    print("\n===== ACADEMIA DRIVESAFE =====")
    print("1. Registrar cliente")
    print("2. Consultar clientes")
    print("3. Registrar instructor")
    print("4. Consultar instructores")
    print("5. Registrar vehículo")
    print("6. Consultar vehículos")
    print("7. Programar cita")
    print("8. Consultar citas")
    print("9. Registrar asistencia")
    print("10. Historial de prácticas por cliente")
    print("0. Salir")


def main():
    crear_carpeta_data()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_cliente()
        elif opcion == "2":
            consultar_clientes()
        elif opcion == "3":
            registrar_instructor()
        elif opcion == "4":
            consultar_instructores()
        elif opcion == "5":
            registrar_vehiculo()
        elif opcion == "6":
            consultar_vehiculos()
        elif opcion == "7":
            programar_cita()
        elif opcion == "8":
            consultar_citas()
        elif opcion == "9":
            registrar_asistencia()
        elif opcion == "10":
            historial_por_cliente()
        elif opcion == "0":
            print("Gracias por usar DriveSafe. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida, intente de nuevo.")


if __name__ == "__main__":
    main()
