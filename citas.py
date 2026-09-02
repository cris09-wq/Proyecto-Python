import csv
from clientes import buscar_cliente_por_documento, buscar_instructor_por_documento, consultar_instructores
from vehiculos import buscar_vehiculo_por_placa, cambiar_disponibilidad, consultar_vehiculos

ARCHIVO_CITAS = "data/citas.csv"
CAMPOS = ["id", "documento_cliente", "documento_instructor", "placa_vehiculo",
          "fecha", "hora", "duracion", "asistio", "observaciones"]


def cargar_citas():
    try:
        with open(ARCHIVO_CITAS, "r", encoding="utf-8", newline="") as archivo:
            return list(csv.DictReader(archivo))
    except FileNotFoundError:
        return []


def guardar_citas(citas):
    with open(ARCHIVO_CITAS, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
        escritor.writeheader()
        for cita in citas:
            escritor.writerow(cita)


def generar_nuevo_id(citas):
    if len(citas) == 0:
        return 1
    return int(citas[-1]["id"]) + 1


def programar_cita():
    documento_cliente = input("Documento del cliente: ").replace(" ", "")
    if buscar_cliente_por_documento(documento_cliente) is None:
        print("El cliente no existe. Regístrelo primero.")
        return

    print("\nInstructores registrados:")
    consultar_instructores()
    documento_instructor = input("\nDocumento del instructor: ").replace(" ", "")
    if buscar_instructor_por_documento(documento_instructor) is None:
        print("El instructor no existe. Regístrelo primero.")
        return

    print("\nVehículos disponibles:")
    consultar_vehiculos(solo_disponibles=True)
    placa_vehiculo = input("\nPlaca del vehículo: ").upper().replace(" ", "")
    vehiculo = buscar_vehiculo_por_placa(placa_vehiculo)

    if vehiculo is None:
        print("El vehículo no existe. Regístrelo primero.")
        return
    if not vehiculo["disponible"]:
        print("Ese vehículo no está disponible en este momento.")
        return

    fecha = input("Fecha de la cita (AAAA-MM-DD): ").replace(" ", "")
    hora = input("Hora de la cita (HH:MM): ").replace(" ", "")
    if len(fecha) != 10 or len(hora) != 5:
        print("Formato de fecha u hora incorrecto.")
        return

    try:
        duracion = float(input("Duración de la práctica en horas (ejemplo: 1.5): "))
    except ValueError:
        print("La duración debe ser un número (ejemplo: 1 o 1.5).")
        return

    if duracion <= 0:
        print("La duración debe ser mayor a cero.")
        return

    citas = cargar_citas()
    nueva_cita = {
        "id": generar_nuevo_id(citas),
        "documento_cliente": documento_cliente,
        "documento_instructor": documento_instructor,
        "placa_vehiculo": placa_vehiculo,
        "fecha": fecha,
        "hora": hora,
        "duracion": duracion,
        "asistio": "Pendiente",
        "observaciones": ""
    }

    citas.append(nueva_cita)
    guardar_citas(citas)
    cambiar_disponibilidad(placa_vehiculo, disponible=False)
    print("Cita programada con éxito. Id de la cita:", nueva_cita["id"])


def consultar_citas():
    citas = cargar_citas()
    if len(citas) == 0:
        print("No hay citas programadas todavía.")
        return

    print("\n1. Ver todas las citas")
    print("2. Filtrar por documento de cliente")
    print("3. Filtrar por fecha")
    opcion = input("Seleccione una opción: ")

    if opcion == "2":
        documento = input("Documento del cliente: ").replace(" ", "")
        citas = [cita for cita in citas if cita["documento_cliente"] == documento]
    elif opcion == "3":
        fecha = input("Fecha (AAAA-MM-DD): ").replace(" ", "")
        citas = [cita for cita in citas if cita["fecha"] == fecha]

    if len(citas) == 0:
        print("No se encontraron citas con ese filtro.")
        return

    print("\n--- CITAS ---")
    for cita in citas:
        print(f"Id: {cita['id']} | Cliente: {cita['documento_cliente']} | "
              f"Instructor: {cita['documento_instructor']} | Vehículo: {cita['placa_vehiculo']} | "
              f"Fecha: {cita['fecha']} | Hora: {cita['hora']} | Duración: {cita['duracion']}h | "
              f"Asistió: {cita['asistio']}")


def registrar_asistencia():
    citas = cargar_citas()
    id_cita = input("Ingrese el id de la cita: ").replace(" ", "")

    cita_encontrada = None
    for cita in citas:
        if cita["id"] == id_cita:
            cita_encontrada = cita

    if cita_encontrada is None:
        print("No se encontró una cita con ese id.")
        return

    asistio = input("¿El cliente asistió? (Si/No): ").capitalize().replace(" ", "")
    if asistio not in ("Si", "No"):
        print("Respuesta no válida. Escriba Si o No.")
        return

    cita_encontrada["asistio"] = asistio
    cita_encontrada["observaciones"] = input("Observaciones de la práctica: ")
    guardar_citas(citas)

    if asistio == "Si":
        cambiar_disponibilidad(cita_encontrada["placa_vehiculo"], disponible=True)

    print("Asistencia registrada con éxito.")


def historial_por_cliente():
    documento = input("Documento del cliente: ").replace(" ", "")
    historial = [cita for cita in cargar_citas()
                 if cita["documento_cliente"] == documento and cita["asistio"] == "Si"]

    if len(historial) == 0:
        print("Este cliente no tiene prácticas realizadas todavía.")
        return

    print("\n--- HISTORIAL DE PRÁCTICAS ---")
    for cita in historial:
        print(f"Fecha: {cita['fecha']} | Hora: {cita['hora']} | Duración: {cita['duracion']}h | "
              f"Instructor: {cita['documento_instructor']} | Observaciones: {cita['observaciones']}")
