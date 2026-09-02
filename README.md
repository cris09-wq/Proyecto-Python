# Academia DriveSafe — Sistema de Registro de Prácticas

Aplicación de consola en Python para gestionar clientes, instructores,
vehículos y citas de práctica de conducción, con persistencia en
archivos locales (JSON y CSV).

## Estructura del proyecto

```
drivesafe/
├── main.py           -> Menú principal y punto de entrada del programa
├── clientes.py        -> Registro y consulta de clientes e instructores
├── vehiculos.py         -> Registro, consulta y disponibilidad de vehículos
├── citas.py               -> Programar citas, asistencia e historial
└── data/                    -> Carpeta donde se guardan los archivos generados
    ├── clientes.json
    ├── instructores.json
    ├── vehiculos.json
    └── citas.csv
```

La carpeta `data/` se crea automáticamente la primera vez que se
ejecuta el programa, así que puede iniciar sin ningún archivo dentro.

## Requisitos

- Python 3.8 o superior.
- No se necesita instalar ninguna librería externa: solo se usan
  módulos que ya vienen incluidos con Python (`json`, `csv`, `os`).

## Cómo ejecutar el programa

1. Abra una terminal dentro de la carpeta `drivesafe/`.
2. Ejecute:

   ```
   python main.py
   ```

3. Aparecerá el menú principal:

   ```
   ===== ACADEMIA DRIVESAFE =====
   1. Registrar cliente
   2. Consultar clientes
   3. Registrar instructor
   4. Consultar instructores
   5. Registrar vehículo
   6. Consultar vehículos
   7. Programar cita
   8. Consultar citas
   9. Registrar asistencia
   10. Historial de prácticas por cliente
   0. Salir
   ```

4. Escriba el número de la opción que desea usar y presione Enter.

## Ejemplo de uso recomendado (en este orden)

1. **Opción 1** — Registrar un cliente (ej: nombre "Juan Perez", documento "123", vehículo "carro").
2. **Opción 3** — Registrar un instructor (ej: nombre "Ana Gomez", documento "555", especialidad "carro").
3. **Opción 5** — Registrar un vehículo (ej: placa "ABC123", tipo "carro").
4. **Opción 7** — Programar una cita: el programa le mostrará automáticamente los instructores registrados y los vehículos disponibles antes de pedirle los datos.
5. **Opción 8** — Consultar las citas programadas (todas, por cliente o por fecha).
6. **Opción 9** — Registrar la asistencia de la cita (Si/No) y las observaciones.
7. **Opción 10** — Ver el historial de prácticas ya realizadas por ese cliente.

---

## Explicación detallada del código, por bloques

### `clientes.py` — Clientes e instructores

**Persistencia (JSON):** `cargar_datos(ruta)` abre el archivo con
`with open(...)` y usa `json.load` para convertir el contenido en una
lista de Python. Si el archivo todavía no existe (primera ejecución),
captura el error y devuelve una lista vacía. `guardar_datos(ruta, datos)`
hace lo contrario: usa `json.dump` para escribir toda la lista en el
archivo.

**Clientes:** `registrar_cliente()` pide nombre, documento y tipo de
vehículo. Usa `.replace(" ", "")` para quitar espacios del documento
(evita duplicados por errores de digitación), valida con
`if len(documento) == 0` que no quede vacío, y llama a
`buscar_cliente_por_documento` para asegurarse de que el documento sea
único antes de guardar. `consultar_clientes()` simplemente recorre la
lista y la imprime.

**Instructores:** sigue la misma lógica que clientes (documento único,
sin espacios), y además valida que la especialidad sea "moto" o "carro".

### `vehiculos.py` — Vehículos y su disponibilidad (módulo nuevo)

Este módulo se separó de `clientes.py` para cumplir mejor el
requerimiento funcional de **"Administrar vehículos disponibles"**: al
tener su propio archivo, es más fácil de mantener y de reutilizar desde
`citas.py`.

- `registrar_vehiculo()` pide placa y tipo, limpia la placa con
  `.replace(" ", "").upper()` y valida que no exista otra igual.
- `consultar_vehiculos(solo_disponibles=False)` puede mostrar **todos**
  los vehículos o, si se le pasa `solo_disponibles=True`, filtrar solo
  los que están libres en ese momento — esto es lo que usa `citas.py`
  para mostrarle al usuario opciones válidas antes de pedirle una placa.
- `buscar_vehiculo_por_placa(placa)` devuelve el vehículo o `None`.
- `cambiar_disponibilidad(placa, disponible)` marca un vehículo como
  ocupado o libre; se usa automáticamente al programar una cita y al
  registrar la asistencia.

### `citas.py` — Programar citas, asistencia e historial

**Persistencia (CSV):** aquí se usa `import csv`. `cargar_citas()` abre
el archivo con `with open` y usa `csv.DictReader` para leer cada fila
como un diccionario. `guardar_citas()` usa `csv.DictWriter`, llama a
`escritor.writeheader()` para escribir la fila de encabezados, y luego
`escritor.writerow(cita)` por cada cita, para escribir todas las filas.

**Programar cita:** antes de pedir el documento del instructor, muestra
la lista de instructores registrados; antes de pedir la placa, muestra
solo los vehículos **disponibles** — así el usuario no tiene que
recordar datos de memoria. Luego valida en orden: que el cliente exista,
que el instructor exista, que el vehículo exista y esté disponible, que
la fecha y hora tengan el formato esperado (`if len(...)`), y que la
duración sea un número válido usando `float(duracion_texto)` dentro de
un `try/except` (si el usuario escribe letras, el programa no se
rompe). Si todo es correcto, guarda la cita y marca el vehículo como no
disponible con `cambiar_disponibilidad(..., disponible=False)`.

**Consultar, asistencia e historial:** `consultar_citas()` permite ver
todas las citas o filtrarlas por cliente o fecha usando comprensión de
listas (`[cita for cita in citas if ...]`). `registrar_asistencia()`
busca la cita por id, actualiza si asistió y las observaciones, y si
asistió "Si", libera el vehículo automáticamente. `historial_por_cliente()`
filtra todas las citas de ese cliente que ya fueron asistidas.

### `main.py` — Menú principal

Crea la carpeta `data/` si no existe, muestra el menú dentro de un
bucle `while True`, y usa una cadena de `if/elif` para llamar a la
función correspondiente según la opción elegida, hasta que el usuario
escribe `0` para salir.

---

## Notas sobre las validaciones

- No se permite registrar dos clientes, instructores o vehículos con
  el mismo documento o placa (evita duplicados).
- El tipo de vehículo y la especialidad solo aceptan "moto" o "carro".
- La duración de la práctica debe ser un número (puede tener decimales,
  ejemplo: 1.5 horas).
- Un vehículo queda marcado como "no disponible" mientras tiene una
  cita pendiente, y vuelve a estar disponible cuando se registra la
  asistencia con "Si".

## Persistencia de datos

- Clientes e instructores se guardan en `data/clientes.json` y
  `data/instructores.json`.
- Los vehículos se guardan en `data/vehiculos.json`.
- Las citas se guardan en `data/citas.csv`, con una fila por cada cita
  programada.
- Toda la información permanece guardada aunque se cierre el programa,
  ya que se lee y se escribe en estos archivos cada vez que se usa una
  opción del menú.
