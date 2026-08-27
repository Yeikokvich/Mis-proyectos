def leer_almacenar_datos (nombre_archivo):
    lista_transacciones = []
    with open (nombre_archivo, "r", encoding = "utf-8") as archivo:
        for linea in archivo:
            partes = linea.split ("-")
            if not linea:
                continue
            if "ID" in linea or "Value" in linea:
                continue
            transacciones = {           
                "Transaction_ID": partes[0],
                "transaction_type": partes[1],
                "value": int(partes[2]),
            }   
            lista_transacciones.append(transacciones)
        return lista_transacciones

def calcular_valor_total (lista_transacciones):
    total = 0
    for transacciones in lista_transacciones:
        total = total + transacciones ["value"] 
    return total       

def filtrar_por_tipo (lista_transacciones, transaction_type):
    lista_filtrada = []
    for transacciones in lista_transacciones:
        if transacciones ["transaction_type"] == transaction_type:
            lista_filtrada.append(transacciones)
    return lista_filtrada

def ejecutar():
    transacciones = leer_almacenar_datos("semana_1/Procesador_transacciones/transacciones.txt")
    print ("----INICIO DE PROCESAMIENTO LIMPIO----")
    print ()
    
    total = calcular_valor_total(transacciones)
    print("Valor total de transacciones:", total)
    
    creditos = filtrar_por_tipo(transacciones, "Crédito")
    print("Créditos adquiridos:")
    for credito in creditos:
        print("Crédito:", credito["value"])
    print ("----FIN PROCESAMIENTO----")
ejecutar()