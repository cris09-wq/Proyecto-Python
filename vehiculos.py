import json

ARCHIVO_VEHICULOS = "data/vehiculos.json"


def cargar_vehiculos():
    try:
        with open(ARCHIVO_VEHICULOS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []


def guardar_vehiculos(vehiculos):
    with open(ARCHIVO_VEHICULOS, "w", encoding="utf-8") as archivo:
        json.dump(vehiculos, archivo, indent=4, ensure_ascii=False)


def buscar_vehiculo_por_placa(placa):
    placa = placa.upper().replace(" ", "")
    for vehiculo in cargar_vehiculos():
        if vehiculo["placa"] == placa:
            return vehiculo
    return None


def registrar_vehiculo():
    placa = input("Placa del vehículo: ").upper().replace(" ", "")
    if len(placa) == 0:
        print("La placa no puede estar vacía.")
        return

    if buscar_vehiculo_por_placa(placa) is not None:
        print("Ya existe un vehículo registrado con esa placa.")
        return

    tipo = input("Tipo de vehículo (moto/carro): ").lower().replace(" ", "")
    if tipo not in ("moto", "carro"):
        print("Tipo de vehículo no válido. Debe ser 'moto' o 'carro'.")
        return

    vehiculos = cargar_vehiculos()
    vehiculos.append({"placa": placa, "tipo": tipo, "disponible": True})
    guardar_vehiculos(vehiculos)
    print("Vehículo registrado con éxito.")


def consultar_vehiculos(solo_disponibles=False):
    vehiculos = cargar_vehiculos()

    if solo_disponibles:
        vehiculos = [v for v in vehiculos if v["disponible"]]

    if len(vehiculos) == 0:
        print("No hay vehículos para mostrar.")
        return

    print("\n--- VEHÍCULOS ---")
    for vehiculo in vehiculos:
        estado = "Disponible" if vehiculo["disponible"] else "No disponible"
        print(f"Placa: {vehiculo['placa']} | Tipo: {vehiculo['tipo']} | Estado: {estado}")


def cambiar_disponibilidad(placa, disponible):
    vehiculos = cargar_vehiculos()
    placa = placa.upper().replace(" ", "")

    for vehiculo in vehiculos:
        if vehiculo["placa"] == placa:
            vehiculo["disponible"] = disponible

    guardar_vehiculos(vehiculos)
