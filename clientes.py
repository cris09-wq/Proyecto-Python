import json

ARCHIVO_CLIENTES = "data/clientes.json"
ARCHIVO_INSTRUCTORES = "data/instructores.json"


def cargar_datos(ruta_archivo):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []


def guardar_datos(ruta_archivo, datos):
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


# --- Clientes ---

def buscar_cliente_por_documento(documento):
    documento = documento.replace(" ", "")
    for cliente in cargar_datos(ARCHIVO_CLIENTES):
        if cliente["documento"] == documento:
            return cliente
    return None


def registrar_cliente():
    nombre = input("Nombre del cliente: ")
    documento = input("Documento del cliente: ").replace(" ", "")

    if len(documento) == 0:
        print("El documento no puede estar vacío.")
        return

    if buscar_cliente_por_documento(documento) is not None:
        print("Ya existe un cliente registrado con ese documento.")
        return

    tipo_vehiculo = input("Tipo de vehículo (moto/carro): ").lower().replace(" ", "")
    if tipo_vehiculo not in ("moto", "carro"):
        print("Tipo de vehículo no válido. Debe ser 'moto' o 'carro'.")
        return

    clientes = cargar_datos(ARCHIVO_CLIENTES)
    clientes.append({"nombre": nombre, "documento": documento, "tipo_vehiculo": tipo_vehiculo})
    guardar_datos(ARCHIVO_CLIENTES, clientes)
    print("Cliente registrado con éxito.")


def consultar_clientes():
    clientes = cargar_datos(ARCHIVO_CLIENTES)

    if len(clientes) == 0:
        print("No hay clientes registrados todavía.")
        return

    print("\n--- LISTA DE CLIENTES ---")
    for cliente in clientes:
        print(f"Nombre: {cliente['nombre']} | Documento: {cliente['documento']} | Vehículo: {cliente['tipo_vehiculo']}")


# --- Instructores ---

def buscar_instructor_por_documento(documento):
    documento = documento.replace(" ", "")
    for instructor in cargar_datos(ARCHIVO_INSTRUCTORES):
        if instructor["documento"] == documento:
            return instructor
    return None


def registrar_instructor():
    nombre = input("Nombre del instructor: ")
    documento = input("Documento del instructor: ").replace(" ", "")

    if len(documento) == 0:
        print("El documento no puede estar vacío.")
        return

    if buscar_instructor_por_documento(documento) is not None:
        print("Ya existe un instructor con ese documento.")
        return

    especialidad = input("Especialidad (moto/carro): ").lower().replace(" ", "")
    if especialidad not in ("moto", "carro"):
        print("Especialidad no válida.")
        return

    instructores = cargar_datos(ARCHIVO_INSTRUCTORES)
    instructores.append({"nombre": nombre, "documento": documento, "especialidad": especialidad})
    guardar_datos(ARCHIVO_INSTRUCTORES, instructores)
    print("Instructor registrado con éxito.")


def consultar_instructores():
    instructores = cargar_datos(ARCHIVO_INSTRUCTORES)

    if len(instructores) == 0:
        print("No hay instructores registrados todavía.")
        return

    print("\n--- LISTA DE INSTRUCTORES ---")
    for instructor in instructores:
        print(f"Nombre: {instructor['nombre']} | Documento: {instructor['documento']} | Especialidad: {instructor['especialidad']}")
