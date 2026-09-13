import random
import pandas as pd


class EmpleadoBase:
    """Define los datos y comportamientos comunes de los empleados."""

    def __init__(self, nombre, salario_base, ciudad):
        self.nombre = nombre
        self.ciudad = ciudad

        # Se usa el setter desde la creación para validar el salario.
        self.salario_base = salario_base

    @property
    def salario_base(self):
        """Obtiene el salario base."""
        return self._salario_base

    @salario_base.setter
    def salario_base(self, nuevo_salario):
        """Valida y actualiza el salario base."""
        nuevo_salario = int(nuevo_salario)

        # Un salario de cero es válido, pero uno negativo no.
        if nuevo_salario < 0:
            raise ValueError("El salario no puede ser negativo.")

        self._salario_base = nuevo_salario

    def calcular_pago(self):
        """Define el cálculo de pago que implementará cada clase hija."""
        raise NotImplementedError(
            "Cada tipo de empleado calcula su pago."
        )

    def obtener_informacion(self):
        """Retorna la información principal del empleado."""
        # Los anchos fijos mantienen las columnas alineadas en consola.
        return (
            f"{self.nombre:<12} | "
            f"{type(self).__name__:<20} | "
            f"{self.ciudad:<13} | "
            f"${self.salario_base:>12,.0f}"
        )


class EmpleadoPlanta(EmpleadoBase):
    """Representa un empleado de planta."""

    def calcular_pago(self):
        """Calcula el salario base más un 30 %."""
        return self.salario_base * 1.30


class EmpleadoContratista(EmpleadoBase):
    """Representa un empleado contratista."""

    def calcular_pago(self):
        """Retorna el salario base del contratista."""
        return self.salario_base


def crear_empleado(nombre, tipo, salario_base, ciudad):
    """Crea un empleado según el tipo recibido."""

    # Normalizar el tipo permite aceptar diferencias de formato en el Excel.
    tipo = tipo.strip().upper()

    if tipo == "PLANTA":
        return EmpleadoPlanta(
            nombre,
            salario_base,
            ciudad
        )

    if tipo == "CONTRATISTA":
        return EmpleadoContratista(
            nombre,
            salario_base,
            ciudad
        )

    # Los tipos no contemplados no deben crear objetos inválidos.
    raise ValueError(
        f"tipo desconocido '{tipo}'"
    )


def leer_empleados_excel(nombre_archivo):
    """Lee y valida los empleados almacenados en Excel."""
    empleados = []
    df = pd.read_excel(nombre_archivo)

    # Normaliza las columnas para evitar errores por espacios o mayúsculas.
    df.columns = [
        str(c).strip().lower()
        for c in df.columns
    ]

    columnas_necesarias = {
        "nombre",
        "tipo",
        "salario_base"
    }

    # Sin estas columnas no es posible construir empleados válidos.
    if not columnas_necesarias.issubset(df.columns):
        faltan = (
            columnas_necesarias
            - set(df.columns)
        )

        print(
            f"  [Error] Al Excel le faltan columnas: {faltan}"
        )

        return empleados

    for _, fila in df.iterrows():

        # Las filas incompletas se ignoran antes de intentar procesarlas.
        if (
            pd.isna(fila["nombre"])
            or pd.isna(fila["tipo"])
            or pd.isna(fila["salario_base"])
        ):
            print(
                "  [Aviso] Fila incompleta ignorada."
            )
            continue

        nombre = str(
            fila["nombre"]
        ).strip()

        tipo = str(
            fila["tipo"]
        ).strip().upper()

        salario = fila["salario_base"]

        # Ciudad es opcional, por eso puede quedar como texto vacío.
        ciudad = (
            str(fila["ciudad"]).strip()
            if (
                "ciudad" in df.columns
                and not pd.isna(fila["ciudad"])
            )
            else ""
        )

        try:
            empleado = crear_empleado(
                nombre,
                tipo,
                salario,
                ciudad
            )

            if empleado is not None:
                empleados.append(empleado)

        # Una fila inválida no debe detener el procesamiento del archivo.
        except ValueError as error:
            print(
                f"  [Aviso] Se ignoro {nombre}: {error}"
            )

    return empleados


def salario_promedio(empleados):
    """Calcula el salario base promedio de los empleados."""

    # Evita una división entre cero si no se cargaron empleados.
    if not empleados:
        return 0

    total_salarios = 0

    for empleado in empleados:
        total_salarios += empleado.salario_base

    return total_salarios / len(empleados)


def sortear_bono(empleados):
    """Sortea un bono entre los empleados de planta."""
    empleados_planta = []

    # Se filtra por clase para aprovechar la jerarquía de objetos creada.
    for empleado in empleados:
        if isinstance(empleado, EmpleadoPlanta):
            empleados_planta.append(empleado)

    # El sorteo solo puede realizarse si existen empleados elegibles.
    if not empleados_planta:
        return None, 0

    ganador = random.choice(empleados_planta)
    bono = 2000000

    return ganador, bono


def ejecutar_quiz():
    """Ejecuta el procesamiento y muestra los resultados."""
    empleados = leer_empleados_excel(
        "empleados.xlsx"
    )

    print("\n--- NOMINA ---")

    print(
        f"{'Nombre':<12} | "
        f"{'Tipo':<20} | "
        f"{'Ciudad':<13} | "
        f"{'Salario base':>13} | "
        f"{'Pago total':>13}"
    )

    print("-" * 82)

    # calcular_pago() responde según la clase concreta de cada empleado.
    for empleado in empleados:
        print(
            empleado.obtener_informacion(),
            "|",
            f"${empleado.calcular_pago():>12,.0f}"
        )

    print("-" * 82)

    print(
        f"Salario promedio: "
        f"${salario_promedio(empleados):,.0f}"
    )

    # El bono es una funcionalidad adicional y no altera el salario guardado.
    ganador, bono = sortear_bono(empleados)

    if ganador:
        print("\n--- BONO EMPRESARIAL ---")
        print(f"Ganador: {ganador.nombre}")
        print(f"Bono: ${bono:,.0f}")
        print(
            f"Pago con bono: "
            f"${ganador.calcular_pago() + bono:,.0f}"
        )
    else:
        print(
            "\nNo hay empleados de planta "
            "para realizar el sorteo."
        )


ejecutar_quiz()