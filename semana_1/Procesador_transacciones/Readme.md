# Análisis de Fragilidad del Procesador de Transacciones

## Descripción

El programa analizado tiene como objetivo leer transacciones almacenadas en un archivo de texto, calcular su valor total y permitir su filtrado según el tipo de transacción.

Aunque el programa funciona correctamente cuando recibe datos con el formato esperado, presenta varios puntos de fragilidad que pueden provocar errores ante entradas incompletas, malformadas o diferentes a las previstas originalmente.

---

## Fragilidades Identificadas

### 1. Validación inadecuada de líneas vacías

La comprobación de líneas vacías se realiza mediante:

`if not linea`

Sin embargo, una línea que contiene únicamente un salto de línea (`\n`) sigue siendo una cadena no vacía, por lo que puede superar esta validación.

Posteriormente, al dividir la línea y acceder directamente a posiciones como `partes[1]` o `partes[2]`, el programa puede generar un `IndexError` si no existen suficientes elementos.

**Consecuencia:** El programa puede detener su ejecución al encontrar líneas vacías o con una estructura incompleta.

**Mejora propuesta:** Limpiar y validar cada línea antes de procesarla, además de comprobar que contenga la cantidad de elementos esperada.

---

### 2. Ausencia de limpieza de cadenas

Los datos obtenidos del archivo no son limpiados antes de almacenarse. Esto puede provocar que espacios adicionales o caracteres como `\n` formen parte de los valores procesados.

Por ejemplo:

`"Crédito"` y `"Crédito "`

serían considerados valores diferentes en una comparación exacta.

**Consecuencia:** Los filtros y comparaciones pueden producir resultados incorrectos aunque visualmente los datos parezcan iguales.

**Mejora propuesta:** Normalizar los datos eliminando espacios y saltos de línea innecesarios antes de almacenarlos o compararlos.

---

### 3. Conversión numérica sin manejo de errores

El programa convierte directamente el valor de cada transacción mediante:

`int(partes[2])`

Si el campo contiene caracteres no numéricos, está vacío o posee un formato inesperado, Python generará un `ValueError`.

**Consecuencia:** Una única transacción malformada puede detener completamente el procesamiento del archivo.

**Mejora propuesta:** Validar el contenido antes de realizar la conversión o implementar un mecanismo de manejo de excepciones que permita identificar y omitir registros inválidos.

---

### 4. Dependencia de una ruta de archivo fija

Si la ubicación del archivo se encuentra escrita directamente dentro del programa (*hardcoded*), el funcionamiento queda ligado a una estructura específica de carpetas o a un equipo determinado.

**Consecuencia:** El programa pierde portabilidad y resulta más difícil reutilizarlo, probarlo o ejecutarlo en otros entornos.

**Mejora propuesta:** Permitir que la ruta o el nombre del archivo sean proporcionados como parámetros externos.

---

## Conclusión

El programa cumple con sus funciones principales bajo condiciones controladas, pero depende en gran medida de que el archivo de entrada tenga exactamente la estructura esperada.

Las principales fragilidades están relacionadas con la falta de validación y normalización de los datos, el manejo limitado de errores y la dependencia de valores definidos directamente en el código.

La implementación de validaciones previas, manejo de excepciones y parametrización permitiría aumentar la **robustez**, **mantenibilidad** y **reutilización** del programa sin modificar su propósito original.
