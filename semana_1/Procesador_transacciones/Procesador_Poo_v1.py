class Transaccion:
    def __init__(self, id_, tipo, monto):
        self.id_ = id_
        self.tipo = tipo
        self.monto = monto

    def obtener_informacion(self):
        return f"ID: {self.id_}, Tipo: {self.tipo}, Monto: {self.monto}"

    def __str__(self):
        return self.obtener_informacion()


def leer_almacenar_datos(nombre_archivo):
    lista_transacciones = []

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.split("-")

            if not linea:
                continue

            if "ID" in linea or "Value" in linea:
                continue

            nueva_transaccion = Transaccion(
                partes[0],
                partes[1],
                int(partes[2])
            )

            lista_transacciones.append(nueva_transaccion)

    return lista_transacciones


def calcular_valor_total(lista_transacciones):
    total = 0

    for transaccion in lista_transacciones:
        total = total + transaccion.monto

    return total


def filtrar_por_tipo(lista_transacciones, transaction_type):
    lista_filtrada = []

    for transaccion in lista_transacciones:
        if transaccion.tipo == transaction_type:
            lista_filtrada.append(transaccion)

    return lista_filtrada


def ejecutar():
    transacciones = leer_almacenar_datos("transacciones.txt")

    print("----INICIO DE PROCESAMIENTO LIMPIO----")
    print()

    total = calcular_valor_total(transacciones)
    print("Valor total de transacciones:", total)

    creditos = filtrar_por_tipo(transacciones, "Crédito")
    print("Créditos adquiridos:")

    for credito in creditos:
        print("Crédito:", credito.monto)

    print("----FIN PROCESAMIENTO----")


ejecutar()