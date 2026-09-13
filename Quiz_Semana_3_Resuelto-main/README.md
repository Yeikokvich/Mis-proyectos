# Quiz Semana 3 - Pilares de POO

## Descripción

Este proyecto corresponde al Quiz de la Semana 3 sobre Programación Orientada a Objetos.

Para desarrollar la actividad se utilizó el código base proporcionado en el quiz. La estructura inicial del programa y la función encargada de leer y validar el archivo Excel ya estaban incluidas.

Siguiendo las instrucciones, la función de lectura del Excel se conservó sin modificar su funcionamiento.

El trabajo realizado se concentró en completar las partes indicadas en los TODO, aplicar encapsulamiento, herencia y polimorfismo, y agregar una funcionalidad propia.

También se realizaron cambios en la presentación de los resultados en consola para facilitar su lectura.

---

## Archivos

El proyecto utiliza los siguientes archivos:

- `quiz_nomina.py`: código principal del quiz.
- `empleados.xlsx`: información de los empleados.
- `requirements.txt`: dependencias necesarias para trabajar con el archivo Excel.

---

# Código proporcionado

El ejercicio incluía una estructura inicial sobre la cual se debía trabajar.

Entre las partes ya proporcionadas se encontraba la función:

```python
leer_empleados_excel()
```

Esta función se encarga de leer `empleados.xlsx`, comprobar las columnas requeridas, ignorar registros incompletos y manejar errores durante la creación de empleados.

Siguiendo las instrucciones del ejercicio, esta lógica se conservó y se utilizó como base para el resto del programa.

La lectura utiliza `pandas`, mientras que `openpyxl` permite trabajar con el archivo `.xlsx`.

---

# Partes completadas

## Encapsulamiento del salario

Una de las partes que se debía completar era el manejo de `salario_base`.

El salario se almacena internamente en:

```python
self._salario_base
```

y se accede mediante una propiedad:

```python
@property
def salario_base(self):
    return self._salario_base
```

Para modificarlo se utiliza un setter:

```python
@salario_base.setter
def salario_base(self, nuevo_salario):
    nuevo_salario = int(nuevo_salario)

    if nuevo_salario < 0:
        raise ValueError("El salario no puede ser negativo.")

    self._salario_base = nuevo_salario
```

De esta manera se cumple con el encapsulamiento solicitado y se valida el salario antes de almacenarlo.

El valor `0` se mantiene como válido, mientras que los valores negativos generan un `ValueError`.

El constructor utiliza:

```python
self.salario_base = salario_base
```

para que el valor inicial también pase por el setter.

---

## Herencia

La plantilla establece una clase principal:

```python
EmpleadoBase
```

y dos clases derivadas:

```python
EmpleadoPlanta
EmpleadoContratista
```

Las clases hijas heredan de `EmpleadoBase`:

```python
class EmpleadoPlanta(EmpleadoBase):
```

```python
class EmpleadoContratista(EmpleadoBase):
```

De esta forma comparten los atributos y comportamientos definidos en la clase base.

---

## Polimorfismo

El método:

```python
calcular_pago()
```

se encuentra definido en la clase base y posteriormente es implementado de manera diferente en cada clase hija.

Para los empleados de planta:

```python
def calcular_pago(self):
    return self.salario_base * 1.30
```

Esto representa el salario base más el 30 % indicado en el ejercicio.

Para los contratistas:

```python
def calcular_pago(self):
    return self.salario_base
```

Por esta razón el programa puede utilizar:

```python
empleado.calcular_pago()
```

para cualquier empleado.

El resultado depende de la clase del objeto que esté siendo procesado, sin necesidad de comprobar nuevamente su tipo.

---

# Creación de objetos

También se completó la función:

```python
crear_empleado()
```

Esta función recibe la información procesada por el lector y crea el objeto correspondiente.

```python
if tipo == "PLANTA":
    return EmpleadoPlanta(...)

if tipo == "CONTRATISTA":
    return EmpleadoContratista(...)
```

Si el tipo recibido no corresponde a ninguno de los tipos permitidos, se genera:

```python
ValueError
```

Esto permite que el manejo de errores ya incluido en el lector pueda ignorar el registro y continuar con los siguientes empleados.

---

# Salario promedio

Se completó la función:

```python
salario_promedio()
```

Esta funcionalidad calcula el promedio de los salarios base de los empleados válidos.

Se añadió además una comprobación:

```python
if not empleados:
    return 0
```

para evitar una división entre cero si no existen empleados cargados.

Para la presentación en consola, el resultado se muestra sin decimales innecesarios.

Por ejemplo:

```text
3273684.210526316
```

se presenta como:

```text
$3,273,684
```

Este cambio afecta solamente la presentación del resultado y no el cálculo realizado por el programa.

---

# Organización de la salida

Después de comprobar que los resultados del ejercicio eran correctos, se decidió mejorar únicamente su presentación en consola.

La primera salida mostraba los datos de forma correcta, pero las diferencias de longitud entre nombres, tipos de empleado, ciudades y cantidades hacían que fueran difíciles de leer.

Por esta razón se utilizaron anchos de campo en las `f-strings`.

Por ejemplo:

```python
f"{self.nombre:<12}"
```

permite reservar espacio para el nombre y alinearlo hacia la izquierda.

Para las cantidades se utilizó un formato como:

```python
f"${self.salario_base:>12,.0f}"
```

Esto permite alinear las cantidades, separar los miles y eliminar decimales que no son necesarios para la presentación.

La salida final se organiza en las columnas:

```text
Nombre | Tipo | Ciudad | Salario base | Pago total
```

Este cambio se realizó únicamente para mejorar la legibilidad de la consola y no modifica los datos originales ni las reglas de cálculo.

---

# Funcionalidad propia: sorteo de bono

Además de las funciones solicitadas, se implementó una funcionalidad adicional:

```python
sortear_bono()
```

La idea consiste en simular un sorteo empresarial en el cual uno de los empleados de planta recibe un bono extraordinario de:

```text
$2,000,000
```

Los contratistas no participan en este sorteo.

Para identificar a los empleados elegibles se utiliza:

```python
isinstance(empleado, EmpleadoPlanta)
```

La decisión de utilizar `isinstance()` permite trabajar con los objetos que ya fueron creados por el programa, en lugar de volver a consultar el texto original del Excel.

Los empleados de planta se agregan a una lista y posteriormente se selecciona un ganador utilizando:

```python
random.choice(empleados_planta)
```

La función retorna:

```python
ganador, bono
```

Si no existen empleados de planta, retorna:

```python
None, 0
```

para evitar intentar realizar un sorteo con una lista vacía.

---

## Tratamiento del bono

El bono se considera un pago extraordinario.

Por esta razón no modifica:

```python
salario_base
```

del empleado ganador.

Para mostrar el resultado se calcula:

```python
ganador.calcular_pago() + bono
```

De esta manera se conserva el salario almacenado originalmente y el bono solamente se suma al pago mostrado para el ganador.

Además, como `calcular_pago()` utiliza polimorfismo, se conserva el cálculo correspondiente al tipo de empleado.

---

# Módulo random

Para realizar el sorteo se agregó:

```python
import random
```

`random` forma parte de la biblioteca estándar de Python, por lo que no requiere instalación adicional ni debe agregarse a `requirements.txt`.

Las dependencias externas del proyecto continúan siendo las proporcionadas para trabajar con Excel:

```text
pandas
openpyxl
```

---

# Ejecución

Primero se instalan las dependencias:

```bash
python -m pip install -r requirements.txt
```

Después se ejecuta:

```bash
python quiz_nomina.py
```

El programa:

1. Lee los empleados desde el Excel.
2. Muestra los avisos correspondientes a registros inválidos.
3. Construye los empleados válidos.
4. Muestra la nómina organizada.
5. Calcula el salario promedio.
6. Realiza el sorteo del bono entre los empleados de planta.

El ganador del bono puede cambiar entre ejecuciones debido a que la selección es aleatoria.

---
# Principios de diseño SOLID

Además de los pilares de Programación Orientada a Objetos, la solución aplica los principios de diseño SRP y OCP de SOLID.

## SRP - Principio de Responsabilidad Única

El principio de Responsabilidad Única establece que cada componente debe concentrarse en una responsabilidad determinada.

En la solución se procuró separar las diferentes tareas del programa en clases y funciones específicas.

Por ejemplo:

```python
leer_empleados_excel()
```

se encarga de leer y procesar los registros provenientes del archivo Excel. Esta función fue proporcionada como parte de la estructura inicial del ejercicio y se mantuvo de acuerdo con las instrucciones.

La función:

```python
crear_empleado()
```

tiene una responsabilidad diferente: crear el objeto correspondiente a partir de los datos ya procesados.

Por otro lado:

```python
salario_promedio()
```

se ocupa únicamente de calcular el promedio de los salarios base.

La funcionalidad adicional también se mantuvo separada:

```python
sortear_bono()
```

Su responsabilidad consiste en determinar qué empleados pueden participar y seleccionar aleatoriamente al ganador del bono.

Finalmente:

```python
ejecutar_quiz()
```

coordina las funciones anteriores y presenta los resultados en consola.

Esta separación evita concentrar la lectura del archivo, creación de objetos, cálculos, sorteo y ejecución general dentro de una única función.

---

## OCP - Principio Abierto/Cerrado

El principio Abierto/Cerrado propone que una estructura pueda extenderse con nuevos comportamientos sin tener que modificar innecesariamente el código que ya funciona.

Este principio se observa principalmente en la jerarquía de empleados.

La clase:

```python
EmpleadoBase
```

define el comportamiento común y establece el método:

```python
calcular_pago()
```

Las clases hijas implementan este comportamiento según sus propias reglas:

```python
class EmpleadoPlanta(EmpleadoBase):
    def calcular_pago(self):
        return self.salario_base * 1.30
```

```python
class EmpleadoContratista(EmpleadoBase):
    def calcular_pago(self):
        return self.salario_base
```

Gracias al polimorfismo, el código encargado de procesar la nómina puede utilizar:

```python
empleado.calcular_pago()
```

sin necesitar conocer la fórmula específica de cada clase.

Esto permite que el comportamiento relacionado con el cálculo de pago se extienda mediante nuevas clases sin tener que modificar la lógica que recorre y procesa los objetos existentes.

Por ejemplo, conceptualmente podría añadirse otro tipo de empleado con su propia implementación de `calcular_pago()` manteniendo el mismo mecanismo utilizado por la nómina.

También se procuró conservar sin cambios la lógica de lectura del Excel proporcionada en el ejercicio y desarrollar las funcionalidades adicionales mediante funciones separadas.

---

## Relación entre POO y SOLID

Los pilares de POO y los principios SOLID utilizados se relacionan dentro de la solución:

- **Encapsulamiento:** protege y valida el salario mediante `@property` y `@setter`.
- **Herencia:** permite que `EmpleadoPlanta` y `EmpleadoContratista` reutilicen la estructura de `EmpleadoBase`.
- **Polimorfismo:** permite utilizar `calcular_pago()` con diferentes comportamientos según el objeto.
- **SRP:** distribuye lectura, creación, cálculos y sorteo entre componentes con responsabilidades diferenciadas.
- **OCP:** permite extender los comportamientos de los empleados mediante nuevas clases sin modificar el mecanismo general que calcula sus pagos.

# Resultado

La solución conserva las partes del programa que fueron proporcionadas y completa las secciones solicitadas utilizando los tres pilares trabajados en el quiz:

- Encapsulamiento mediante `salario_base`, `@property` y `@setter`.
- Herencia mediante `EmpleadoBase`, `EmpleadoPlanta` y `EmpleadoContratista`.
- Polimorfismo mediante las diferentes implementaciones de `calcular_pago()`.

Como funcionalidad adicional se implementó el sorteo del bono empresarial y, como mejora de presentación, se organizó la salida de la nómina en columnas sin modificar los cálculos del ejercicio.

---

## Autor

Jacob Camacho