# Análisis de Fragilidad: Programación Estructurada y el Riesgo de Escalabilidad

Este documento presenta un análisis crítico sobre la fragilidad de la **Programación Estructurada (PE)** orientada a procedimientos cuando se enfrenta al crecimiento de requerimientos, específicamente al escalar de un modelo simple a manejar **10 o más tipos de transacciones diferentes**.

---

##  El Problema Estructural al Escalar a Múltiples Tipos

En el paradigma de la programación estructurada tradicional, los datos se representan como estructuras pasivas y planas (como diccionarios o tuplas) que están completamente desconectadas de las funciones que los manipulan. 

Cuando el sistema crece para soportar múltiples casuísticas (ej. créditos, débitos, comisiones, transferencias, reembolsos, inversiones, impuestos, etc.), este desacoplamiento extremo genera graves problemas de mantenimiento y depuración (*debugging*).

---

##  ¿Por qué tener datos separados de la lógica crea un riesgo crítico de *debugging*?

### 1. Dispersión Masiva de Condicionales (*If/Else Hell*)
Al no poseer la lógica encapsulada dentro de la estructura de datos, cada función de procesamiento (`calcular_total`, `validar_reglas`, `aplicar_impuestos`, `filtrar_por_tipo`) se ve obligada a implementar bloques masivos de condiciones múltiples (`if/elif/else`) para evaluar qué hacer según el tipo de transacción. 
* **El riesgo de depuración:** Si se añade un tipo de transacción número 11, el desarrollador debe cazar y modificar de forma manual **todas** las funciones dispersas en el código. Olvidar actualizar tan solo un bloque `elif` genera fallos silenciosos o excepciones en tiempo de ejecución difíciles de rastrear.

### 2. Pérdida de Localidad de Referencia y Trazabilidad Rota
En un modelo estructurado, los datos fluyen como parámetros mutables a través de una tubería de funciones procedurales independientes. 
* **El riesgo de depuración:** Cuando una transacción de tipo 7 llega con un valor corrupto o una clave faltante (`KeyError`), el rastreo del error (*stack trace*) solo indica dónde falló la función final (por ejemplo, al sumar), pero no ofrece pistas sobre cuál de las múltiples funciones intermedias alteró o malinterpretó la estructura del diccionario original. El desarrollador debe recorrer mentalmente todo el flujo procedural de arriba a abajo.

### 3. Ausencia de Contratos de Datos y Tipado Estricto
Los diccionarios planos permiten que cualquier función modifique las claves o inyecte nuevos campos de manera arbitraria (por ejemplo, un módulo puede usar `"value"`, otro `"monto"`, y otro `"valor_neto"`).
* **El riesgo de depuración:** Al no existir un esquema encapsulado o validación de tipos por entidad, las discrepancias en los nombres de las claves o en los tipos de datos (como pasar un string en lugar de un entero) no se detectan al escribir el código, manifestándose como errores inesperados en producción al procesar combinaciones complejas de transacciones.

### 4. Violación del Principio de Responsabilidad Única a Nivel de Módulo
A medida que aumentan los tipos de transacciones, las funciones procedurales crecen en complejidad ciclomática para intentar resolver las reglas de negocio de todos los tipos en un solo lugar.
* **El riesgo de depuración:** Las funciones se vuelven monolíticas. Aislar un error en las reglas de cálculo específicas para el tipo 4 implica leer y depurar código que mezcla la lógica de los otros 9 tipos, aumentando exponencialmente la carga cognitiva del desarrollador.

---

##  Conclusión Arquitectónica

La separación estricta entre datos pasivos y lógica procedural funciona adecuadamente en scripts pequeños y lineales. Sin embargo, al escalar en complejidad de dominio (múltiples tipos de datos), esta aproximación se vuelve sumamente **frágil**, convirtiendo el *debugging* en una tarea costosa y propensa a errores humanos. 

La solución estructural natural ante este escenario de escalabilidad es evolucionar hacia paradigmas más cohesionados, como la **Programación Orientada a Objetos (POO)** —donde cada tipo de transacción encapsula sus propios datos y su propia lógica de comportamiento mediante polimorfismo—, eliminando por completo los gigantescos árboles de decisiones condicionales.