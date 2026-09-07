class TransaccionBase:
    """Define datos y comportamiento comun de las transacciones."""

    def __init__(self, id_transaccion, monto):
        self.id_transaccion = id_transaccion
        self.monto = monto

    @property
    def id_transaccion(self):
        return self._id_transaccion

    @id_transaccion.setter
    def id_transaccion(self, nuevo_id):
        # Valida formato de identificador.
        nuevo_id = str(nuevo_id).strip().upper()

        if (
            len(nuevo_id) != 4
            or nuevo_id[0] != "T"
            or not nuevo_id[1:].isdigit()
        ):
            raise ValueError("ID_INVALIDO")

        self._id_transaccion = nuevo_id

    @property
    def monto(self):
        return self._monto

    @monto.setter
    def monto(self, nuevo_monto):
        # Convierte y valida monto.
        nuevo_monto = int(nuevo_monto)

        if nuevo_monto < 0:
            raise ValueError("NEGATIVO")

        if nuevo_monto == 0:
            raise ValueError("CERO")

        self._monto = nuevo_monto

    def calcular_impacto(self):
        # Delega calculo a clases hijas.
        raise NotImplementedError(
            "Cada tipo de transaccion debe definir su impacto."
        )

    def obtener_informacion(self):
        # Obtiene datos principales.
        return (
            f"{self.id_transaccion} | "
            f"{type(self).__name__} | "
            f"${self.monto}"
        )


class TransaccionCredito(TransaccionBase):
    """Representa transaccion de credito."""

    def calcular_impacto(self):
        # Calcula impacto por interes del 2%.
        return round(self.monto * 0.02, 2)


class TransaccionDebito(TransaccionBase):
    """Representa transaccion de debito."""

    def calcular_impacto(self):
        # Calcula impacto por comision fija.
        return 1500


class TransaccionEfectivo(TransaccionBase):
    """Representa transaccion en efectivo."""

    def calcular_impacto(self):
        # Calcula impacto del 1%.
        return round(self.monto * 0.01, 2)


def crear_transaccion(id_transaccion, tipo, monto):
    """Crea transaccion segun tipo recibido."""

    tipo = tipo.strip().upper()

    if tipo == "CREDITO":
        return TransaccionCredito(id_transaccion, monto)

    if tipo == "DEBITO":
        return TransaccionDebito(id_transaccion, monto)

    if tipo == "EFECTIVO":
        return TransaccionEfectivo(id_transaccion, monto)

    raise ValueError("TIPO_INVALIDO")


def leer_transacciones(nombre_archivo):
    """Lee archivo y almacena transacciones validas."""

    transacciones = []

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            if not linea.strip():
                continue

            try:
                # Separa datos del archivo.
                id_transaccion, tipo, monto = linea.strip().split(",")

                # Crea y almacena transaccion.
                transaccion = crear_transaccion(
                    id_transaccion,
                    tipo,
                    monto
                )

                transacciones.append(transaccion)

            except ValueError as error:
                # Clasifica y reporta errores.
                error = str(error)

                if error == "NEGATIVO":
                    print(
                        f"Se omitio la transaccion {id_transaccion}, "
                        "el valor no puede ser negativo"
                    )

                elif error == "CERO":
                    print(
                        f"Se omitio la transaccion {id_transaccion}, "
                        "0 no es un valor valido"
                    )

                elif error == "TIPO_INVALIDO":
                    print(
                        f"Se omitio la transaccion {id_transaccion}, "
                        "tipo de transaccion no reconocido"
                    )


                else:
                    print(
                        f"Se omitio la transaccion {id_transaccion}: {error}"
                    )

    return transacciones


def ejecutar_sistema():
    """Ejecuta lectura, calculo y salida de datos."""

    # Lee archivo principal de transacciones.
    transacciones = leer_transacciones("transactions.txt")

    print("\n--- Transacciones cargadas ---")

    for transaccion in transacciones:
        # Calcula impacto segun tipo de objeto.
        print(
            transaccion.obtener_informacion(),
            "-> impacto:",
            transaccion.calcular_impacto()
        )


if __name__ == "__main__":
    ejecutar_sistema()