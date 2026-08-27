# procesador_ventas.py
# Actividad 1.2 - Programacion Estructurada (version de clase)
# Lee ventas de un archivo y las procesa con funciones.
# Cada linea de ventas.txt tiene:  ProductoID, Categoria, Valor
# Para ejecutar:  python procesador_ventas.py


# 1) Leer el archivo y guardar las ventas en una lista de diccionarios
def cargar_ventas(nombre_archivo):
    lista_ventas = []
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.split(",")   # separar por guiones
            if not linea:
                continue
            if "ProductoID" in linea or "Valor" in linea:
                continue
            venta = {
                "producto_id": partes[0],
                "categoria": partes[1],
                "valor": int(partes[2]),  # convertir el valor a numero
            }
            lista_ventas.append(venta)
    return lista_ventas


# 2) Sumar el valor de todas las ventas
def calcular_valor_total(lista_ventas):
    total = 0
    for venta in lista_ventas:
        total = total + venta["valor"]
    return total


# 3) Dejar solo las ventas de una categoria
def filtrar_por_categoria(lista_ventas, categoria):
    lista_filtrada = []
    for venta in lista_ventas:
        if venta["categoria"] == categoria:
            lista_filtrada.append(venta)
    return lista_filtrada


# 4) Funcion principal que usa todas las demas
def ejecutar_sistema():
    ventas = cargar_ventas("ventas.txt")

    total = calcular_valor_total(ventas)
    print("Valor total de las ventas:", total)

    electronica = filtrar_por_categoria(ventas, "ELECTRONICA")
    print("Ventas de ELECTRONICA:")
    for venta in electronica:
        print(venta)


# Iniciar el programa
ejecutar_sistema()