# quiz_empresas.py
# Quiz 1 - Fundamentos de programacion (Programacion Estructurada + POO)
# Tu tarea: completar todos los bloques marcados con "# TODO".
# Cada linea de empresas.txt tiene:  nombre, sector, num_empleados, ingresos_anuales
# Para ejecutar:  python quiz_empresas.py
#
# CONSEJO: ve completando un TODO a la vez y ejecuta el archivo para ver como
#          se va llenando la salida. Al inicio veras resultados vacios o en cero.


# 1) LA CLASE: representa UNA empresa (datos + comportamiento juntos)
class Empresa:
    """Representa UNA empresa: encapsula sus datos y su comportamiento."""

    # El CONSTRUCTOR se ejecuta al crear el objeto y guarda sus datos.
    # 'self' es el propio objeto que se esta construyendo.
    def __init__(self, nombre, sector, num_empleados, ingresos_anuales):
        # TODO: guarda cada parametro como un atributo del objeto (self.xxx = ...).
        #       Recuerda convertir num_empleados e ingresos_anuales a numero con int().
        pass

    def obtener_informacion(self):
        """Devuelve los datos de la empresa como un texto legible."""
        # TODO: devuelve un texto con los datos del objeto, por ejemplo:
        #       "TechNova | TECNOLOGIA | 150 empleados | $500000000"
        #       Usa un f-string con los atributos de self.
        return ""


# 2) Leer el archivo y crear una LISTA DE OBJETOS Empresa
def leer_empresas(nombre_archivo):
    """Lee el archivo y crea un objeto Empresa por cada linea valida.

    Una linea es INVALIDA si num_empleados es menor o igual a 0:
    en ese caso NO se crea el objeto (se ignora el registro).
    """
    empresas = []
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            nombre, sector, num_empleados, ingresos_anuales = linea.strip().split(",")
            # TODO: si int(num_empleados) > 0, crea un objeto Empresa y agregalo a la lista.
            pass
    return empresas


# 3) Sumar los ingresos de todas las empresas
def calcular_total_ingresos(empresas):
    """Devuelve la suma de los ingresos_anuales de todas las empresas."""
    # TODO: recorre la lista y suma el atributo ingresos_anuales de cada empresa.
    return 0


# 4) Quedarse solo con las empresas de un sector
def filtrar_por_sector(empresas, sector):
    """Devuelve una lista con las empresas cuyo sector coincide."""
    # TODO: devuelve una lista solo con las empresas de ese sector.
    return []


# 5) Encontrar la empresa con mas empleados
def empresa_con_mas_empleados(empresas):
    """Devuelve el objeto Empresa que tiene mas empleados."""
    # TODO: recorre la lista y devuelve la empresa con el mayor num_empleados.
    #       Si la lista esta vacia, devuelve None.
    return None


# 6) Calcular el promedio de empleados
def promedio_empleados(empresas):
    """Devuelve el promedio de empleados de todas las empresas."""
    # TODO: suma los empleados y divide entre la cantidad de empresas.
    #       Si la lista esta vacia, devuelve 0 (evita dividir entre cero).
    return 0


# 7) Funcion principal: usa todo lo anterior y muestra los resultados
def ejecutar_quiz():
    empresas = leer_empresas("empresas.txt")

    print("--- Empresas registradas ---")
    for empresa in empresas:
        print(empresa.obtener_informacion())

    print("\nTotal de ingresos:", calcular_total_ingresos(empresas))

    print("\n--- Empresas del sector TECNOLOGIA ---")
    for empresa in filtrar_por_sector(empresas, "TECNOLOGIA"):
        print(empresa.obtener_informacion())

    mejor = empresa_con_mas_empleados(empresas)
    if mejor is not None:
        print("\nEmpresa con mas empleados:", mejor.obtener_informacion())

    print("\nPromedio de empleados:", promedio_empleados(empresas))


# Iniciar el programa
ejecutar_quiz()
