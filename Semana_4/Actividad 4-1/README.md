# Semana 4 - Manejo de errores con Try-Except

## Descripción

Este proyecto continúa el sistema de procesamiento de transacciones desarrollado durante la Semana 3.

En la versión anterior se implementaron los pilares principales de la Programación Orientada a Objetos, junto con diferentes validaciones para impedir la creación de transacciones con datos incorrectos.

En esta actividad se mejora la robustez del programa mediante el uso de bloques `try-except`, permitiendo detectar registros corruptos, informar el error encontrado y continuar procesando las demás transacciones sin detener la ejecución completa del sistema.

---

# Archivos

## `robustez_try_except.py`

Contiene las clases de transacciones, las validaciones, la lectura del archivo y la implementación del manejo de excepciones mediante `try-except`.

## `transacciones_corruptas.txt`

Contiene siete registros utilizados para comprobar el funcionamiento del manejo de errores.

El archivo incluye cuatro registros válidos y tres registros corruptos intencionalmente.

Cada línea utiliza el formato:

```text
ID,TIPO,MONTO
```

Los registros utilizados son:

```text
C001,DEBITO,150000
C002,CREDITO,500000
C003,DEBITO,texto_invalido
C004,CREDITO,-200000
C005,DEBITO,45000
C006,DEBITO
C007,CREDITO,10000
```

---

# Recapitulación del código anterior

Durante la Semana 3 se refactorizó el sistema utilizando Programación Orientada a Objetos.

El programa utiliza una clase base llamada:

```python
TransaccionBase
```

Esta clase contiene los datos y comportamientos comunes de las diferentes transacciones.

A partir de ella se implementaron las clases:

```python
TransaccionCredito
TransaccionDebito
TransaccionEfectivo
```

Estas clases utilizan herencia para reutilizar la estructura definida en `TransaccionBase`.

También se aplicó polimorfismo mediante el método:

```python
calcular_impacto()
```

Cada tipo de transacción implementa su propia forma de calcular el impacto.

Las transacciones de crédito calculan un 2% del monto, las transacciones de débito utilizan una comisión fija de 1500 y las transacciones en efectivo calculan un 1%.

---

# Validaciones implementadas anteriormente

La clase `TransaccionBase` utiliza propiedades y setters para validar los datos antes de almacenarlos.

Por ejemplo, el setter del monto convierte el valor recibido a un número entero:

```python
nuevo_monto = int(nuevo_monto)
```

Si el valor no puede convertirse a un número, Python genera un `ValueError`.

También se verifica que el monto sea mayor que cero.

```python
if nuevo_monto < 0:
    raise ValueError("NEGATIVO")

if nuevo_monto == 0:
    raise ValueError("CERO")
```

De esta manera, los objetos no pueden almacenar montos inválidos.

El identificador de la transacción también es validado antes de ser almacenado.

Para esta actividad se permiten identificadores con el formato:

```text
C###
```

También se mantiene compatibilidad con el formato anterior:

```text
T###
```

---

# Función `crear_transaccion()`

La función:

```python
crear_transaccion()
```

recibe el identificador, el tipo y el monto de una transacción.

Dependiendo del tipo recibido, crea el objeto correspondiente.

Por ejemplo:

```python
if tipo == "CREDITO":
    return TransaccionCredito(id_transaccion, monto)

if tipo == "DEBITO":
    return TransaccionDebito(id_transaccion, monto)
```

Si el tipo de transacción no corresponde a ninguno de los tipos reconocidos, se genera un `ValueError`.

---

# Implementación de Try-Except

El principal cambio realizado durante la Semana 4 se encuentra en la función:

```python
leer_transacciones()
```

Esta función es el punto crítico del programa porque se encarga de leer cada registro del archivo, separar sus datos y crear los objetos.

Un registro corrupto podría generar una excepción y detener completamente la ejecución.

Para evitarlo, la lógica de procesamiento de cada registro se colocó dentro de un bloque:

```python
try:
```

El flujo utilizado es:

```text
Leer línea
    |
Separar datos
    |
Comprobar cantidad de datos
    |
Crear objeto
    |
Validar datos
    |
    +---- Correcto ----> Guardar transacción
    |
    +---- Error -------> Capturar excepción
                             |
                        Registrar error
                             |
                        Continuar lectura
```

---

# Bloque `try`

Dentro del bloque `try` se ejecutan las operaciones que pueden producir errores.

Primero se separan los datos:

```python
datos = linea.strip().split(",")
```

Después se verifica que el registro contenga los tres datos necesarios:

```python
if len(datos) != 3:
    raise TypeError("DATOS_INSUFICIENTES")
```

Si existen los tres datos, se almacenan en:

```python
id_transaccion, tipo, monto = datos
```

Finalmente se intenta crear la transacción:

```python
transaccion = crear_transaccion(
    id_transaccion,
    tipo,
    monto
)
```

Si ninguna operación genera una excepción, la transacción se considera válida y se almacena en la lista.

```python
transacciones.append(transaccion)
```

---

# Manejo de `ValueError`

El primer bloque `except` captura errores de tipo:

```python
except ValueError as error:
```

Este tipo de excepción se utiliza principalmente para errores de conversión y validación.

En el archivo de prueba existen dos situaciones que producen este error.

## Texto en lugar de un monto

```text
C003,DEBITO,texto_invalido
```

El programa intenta convertir:

```text
texto_invalido
```

a un número entero.

Como esta conversión no es posible, Python genera un `ValueError`.

## Monto negativo

```text
C004,CREDITO,-200000
```

En este caso la conversión a número funciona correctamente, pero el setter detecta que el monto es negativo y genera:

```python
raise ValueError("NEGATIVO")
```

El bloque `except ValueError` captura ambos errores y muestra el registro que produjo el problema.

```python
except ValueError as error:
    print(
        f"Error ValueError en el registro "
        f"{linea.strip()}: {error}"
    )
```

Después de mostrar el mensaje, el programa continúa automáticamente con la siguiente iteración del ciclo.

---

# Manejo de `TypeError`

El segundo tipo de excepción utilizado es:

```python
except TypeError as error:
```

Este error se utiliza cuando un registro no contiene todos los datos necesarios para crear una transacción.

El archivo contiene intencionalmente:

```text
C006,DEBITO
```

Este registro solamente contiene dos datos:

```text
ID,TIPO
```

pero el sistema necesita:

```text
ID,TIPO,MONTO
```

Antes de intentar crear el objeto, el programa comprueba la cantidad de datos:

```python
if len(datos) != 3:
    raise TypeError("DATOS_INSUFICIENTES")
```

La excepción es capturada mediante:

```python
except TypeError as error:
    print(
        f"Error TypeError en el registro "
        f"{linea.strip()}: {error}"
    )
```

El registro corrupto se descarta y el programa continúa con el siguiente.

---

# Estrategia de recuperación

La estrategia implementada es una recuperación pasiva.

Cuando ocurre un error, el programa:

1. Detecta la excepción.
2. Identifica el registro que produjo el problema.
3. Muestra el tipo de error.
4. Descarta el registro corrupto.
5. Continúa procesando las siguientes líneas.

No es necesario detener o reiniciar el programa.

El ciclo `for` simplemente continúa con el siguiente registro después de ejecutar el bloque `except`.

---

# Resultado esperado

Al procesar `transacciones_corruptas.txt`, los registros:

```text
C001
C002
C005
C007
```

son procesados correctamente.

Los registros:

```text
C003
C004
C006
```

generan errores controlados.

Una ejecución produce resultados similares a:

```text
Error ValueError en el registro C003,DEBITO,texto_invalido: invalid literal for int()
Error ValueError en el registro C004,CREDITO,-200000: NEGATIVO
Error TypeError en el registro C006,DEBITO: DATOS_INSUFICIENTES

--- Transacciones cargadas ---
C001 | TransaccionDebito | $150000 -> impacto: 1500
C002 | TransaccionCredito | $500000 -> impacto: 10000.0
C005 | TransaccionDebito | $45000 -> impacto: 1500
C007 | TransaccionCredito | $10000 -> impacto: 200.0
```

---

# Conclusión

La implementación de `try-except` permite aumentar la robustez del sistema de transacciones.

En la versión anterior las clases ya podían detectar datos inválidos mediante validaciones y excepciones. En esta actividad se complementa ese comportamiento haciendo que la función encargada de leer el archivo pueda recuperarse de esos errores.

El programa ahora puede encontrar registros corruptos, registrar el problema y continuar trabajando con las transacciones válidas.

Esto evita que un único dato incorrecto provoque la interrupción completa de la ejecución.
