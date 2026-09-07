# Semana 3 - Robustez con POO

## Descripción

Este proyecto refactoriza el sistema de transacciones desarrollado anteriormente para aplicar los pilares de Programación Orientada a Objetos.

El programa lee transacciones desde el archivo `transactions.txt`, valida los datos, crea diferentes objetos según el tipo de transacción y calcula el impacto correspondiente.

La refactorización aplica:

- Encapsulamiento.
- Herencia.
- Polimorfismo.
- Validación de datos.
- Manejo de errores.

El objetivo es evitar que datos inválidos detengan la ejecución completa del programa.

---

## Archivos

### `diseno_pilares_poo.py`

Contiene las clases, validaciones, lectura del archivo y ejecución principal del programa.

### `transactions.txt`

Contiene las transacciones utilizadas para probar el funcionamiento del sistema.

Cada línea utiliza el siguiente formato:

```text
ID,TIPO,MONTO
```

Ejemplo:

```text
T001,CREDITO,500000
T002,DEBITO,80000
T003,EFECTIVO,10000
```

---

# Estructura del programa.

## TransaccionBase

`TransaccionBase` contiene los datos y comportamientos comunes de todas las transacciones.

Los atributos principales se almacenan internamente como:

```python
self._id_transaccion
self._monto
```

El acceso y modificación de estos valores se controla mediante propiedades y setters.

Esto permite validar los datos antes de almacenarlos.

---

## Encapsulamiento

El monto se consulta mediante un getter:

```python
@property
def monto(self):
    return self._monto
```

Su modificación pasa por un setter:

```python
@monto.setter
def monto(self, nuevo_monto):
```

Antes de almacenar el monto, el programa comprueba que el valor sea válido.

El identificador de la transacción utiliza el mismo sistema para verificar su formato antes de almacenarlo.

---

## Herencia

Las diferentes transacciones heredan de `TransaccionBase`.

```python
class TransaccionCredito(TransaccionBase):
```

```python
class TransaccionDebito(TransaccionBase):
```

```python
class TransaccionEfectivo(TransaccionBase):
```

Esto permite reutilizar el constructor, propiedades, setters y métodos comunes sin repetirlos en cada clase.

---

## Polimorfismo

`TransaccionBase` define el método común:

```python
calcular_impacto()
```

Cada clase hija implementa su propia versión.

### Crédito

Calcula un impacto equivalente al 2% del monto.

```text
500000 -> 10000
```

### Débito

Aplica una comisión fija de:

```text
1500
```

### Efectivo

Calcula un impacto equivalente al 1% del monto.

```text
10000 -> 100
```

El programa puede llamar:

```python
transaccion.calcular_impacto()
```

sin comprobar manualmente qué clase de transacción está procesando.

Cada objeto ejecuta su implementación correspondiente.

---

# Validación de datos

El archivo `transactions.txt` contiene registros válidos y registros inválidos incluidos intencionalmente.

El objetivo es comprobar que un dato incorrecto pueda ser detectado y omitido sin detener el procesamiento de las demás transacciones.

---

## Error: monto negativo

Se incluyeron transacciones con montos negativos:

```text
T005,CREDITO,-1
T008,DEBITO,-5000
T011,CREDITO,-250000
```

El setter de `monto` detecta que el valor es menor que cero y genera un error controlado.

El programa reporta:

```text
Se omitio la transaccion T005, el valor no puede ser negativo
```

La transacción no se almacena y el programa continúa procesando el archivo.

---

## Error: monto igual a cero

Se incluyó intencionalmente:

```text
T013,CREDITO,0
```

El programa considera `0` como un monto inválido.

El setter genera el error correspondiente y el lector reporta:

```text
Se omitio la transaccion T013, 0 no es un valor valido
```

La ejecución continúa normalmente.

---

## Error: tipo de transacción desconocido

Los tipos reconocidos por el sistema son:

```text
CREDITO
DEBITO
EFECTIVO
```

Se incluyó intencionalmente:

```text
T009,SI ME PAGARON,300000
```

`SI ME PAGARON` no corresponde a ninguna clase disponible.

La función `crear_transaccion()` detecta el tipo desconocido y genera un error controlado.

El programa reporta:

```text
Se omitio la transaccion T009, tipo de transaccion no reconocido
```

El registro se descarta y las siguientes transacciones continúan procesándose.

---

## Error: identificador inválido

Los identificadores válidos utilizan el formato:

```text
T###
```

Ejemplos:

```text
T001
T025
T999
```

El setter de `id_transaccion` comprueba:

- Longitud del identificador.
- Uso de `T` como primer carácter.
- Presencia de tres números después de `T`.

Se puede utilizar un registro como el siguiente para comprobar esta validación:

```text
X014,CREDITO,500000
```

Cuando el formato no es válido, el programa reporta:

```text
No se reconocio X014, verificar manualmente
```

El registro no se almacena y el procesamiento continúa.

---

# Manejo de errores

La función `leer_transacciones()` procesa los registros utilizando un bloque `try/except`.

Los setters y funciones de validación generan errores mediante `ValueError`.

El lector captura estos errores, identifica su causa y muestra la leyenda correspondiente.

De esta forma, un registro inválido no detiene todo el programa.

El flujo general es:

```text
Leer registro
    |
Separar datos
    |
Crear transaccion
    |
Validar ID y monto
    |
    +---- Datos validos ----> Almacenar transaccion
    |
    +---- Datos invalidos --> Reportar error y continuar
```

---

# Ejecución

El programa se ejecuta desde la carpeta del proyecto con:

```bash
python diseno_pilares_poo.py
```

El archivo `transactions.txt` debe encontrarse en la misma carpeta.

La estructura esperada es:

```text
Pilares_Poo/
|
|-- diseno_pilares_poo.py
|-- transactions.txt
|-- README.md
```

---

# Resultado

Las transacciones válidas se cargan y procesan normalmente.

Las transacciones inválidas son detectadas, reportadas y omitidas sin detener el programa.

Una ejecución de prueba produce errores controlados como:

```text
Se omitio la transaccion T005, el valor no puede ser negativo
Se omitio la transaccion T008, el valor no puede ser negativo
Se omitio la transaccion T009, tipo de transaccion no reconocido
Se omitio la transaccion T011, el valor no puede ser negativo
Se omitio la transaccion T013, 0 no es un valor valido
```

Después de procesar estos errores, el programa continúa mostrando las transacciones válidas y sus respectivos impactos.

---

# Conceptos aplicados

**Encapsulamiento:** protege los atributos y valida sus modificaciones mediante getters y setters.

**Herencia:** permite que Crédito, Débito y Efectivo reutilicen la estructura definida en `TransaccionBase`.

**Polimorfismo:** permite utilizar `calcular_impacto()` sobre diferentes objetos y obtener un comportamiento específico para cada tipo.

**Robustez:** permite identificar datos inválidos y continuar la ejecución sin perder las demás transacciones.