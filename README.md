# Proyecto: Base de Datos NoSQL con Neo4j

## Descripción General

Este proyecto utiliza Neo4j como base de datos NoSQL para modelar una liga de jugadoras de fútbol, sus equipos y los partidos que juegan. La elección de Neo4j se debe a su naturaleza basada en grafos, que es ideal para modelar relaciones complejas y consultas que implican múltiples niveles de conexión, como las relaciones entre jugadoras, equipos, ligas y jugadas realizadas en los partidos.

El repositorio incluye scripts para cargar datos desde un archivo CSV y generar automáticamente una estructura de liga, equipos, jugadoras, partidos y jugadas. También se incluyen instrucciones claras para replicar el entorno y realizar modificaciones en los datos.

---

## Tareas

### 1. **Ventajas y Desventajas de Neo4j (NoSQL)**
- **Ventajas:**
  - Ideal para modelar y analizar relaciones complejas entre entidades.
  - Consultas más intuitivas con Cypher, un lenguaje diseñado para grafos.
  - Alto rendimiento en búsquedas de relaciones y conexiones profundas.
- **Desventajas:**
  - Curva de aprendizaje más pronunciada comparada con bases de datos relacionales.
  - No es óptimo para datos tabulares o no relacionales que no requieren muchas conexiones.
  - Puede requerir mayor capacidad de memoria en comparación con otras bases de datos.

### 2. **Esquema de la Base de Datos**
El esquema está basado en nodos y relaciones:
- Nodos:
  - `League`: Representa la liga (única en este caso, `Mini Liga`).
  - `Team`: Representa los equipos participantes.
  - `Player`: Representa las jugadoras.
  - `Game`: Representa los partidos jugados.
  - `Play`: Representa las jugadas realizadas en cada partido.
- Relaciones:
  - `PARTICIPATES_IN`: Conecta equipos con la liga.
  - `BELONGS_TO`: Conecta jugadoras con sus equipos.
  - `PLAYS_IN`: Conecta equipos con partidos.
  - `BELONGS_TO_GAME`: Conecta jugadas con los partidos donde ocurrieron.
  - `MAKES_PASS` y `SCORES_GOAL`: Relacionan jugadoras con jugadas.

### 3. **Sentencias de Inserción**
El script utiliza Python y la biblioteca `neo4j` para cargar datos desde un archivo CSV (`Jugadoras y Equipos.csv`) e insertar nodos y relaciones en la base de datos. El script:
1. Lee el archivo CSV.
2. Inserta jugadoras y equipos asociados a una liga.
3. Genera partidos entre equipos aleatorios, asegurando que cada equipo juega exactamente dos partidos.
4. Inserta jugadas realizadas en cada partido.

Para ejecutar el script:
- Instalar los requisitos con `pip install neo4j pandas`.
- Configurar el archivo CSV en la ruta `C:/Users/jesus/Desarrollo/Big Data/Jugadoras y Equipos.csv`.
- Ejecutar el script Python.

### 4. **Sentencias de Modificación**
Para cambiar los nombres de dos jugadoras a mayúsculas:
```cypher
MATCH (p:Player {name: 'NombreOriginal1'})
SET p.name = 'NOMBREORIGINAL1';

MATCH (p:Player {name: 'NombreOriginal2'})
SET p.name = 'NOMBREORIGINAL2';
```

---

## Instrucciones para Crear la Base de Datos

1. Instalar [Docker Desktop](https://www.docker.com/).
2. Descargar la imagen de Neo4j ejecutando el siguiente comando:
   ```bash
   docker pull neo4j
   ```
3. Configurar y ejecutar el contenedor Neo4j. Se puede usar una configuración básica desde Docker Desktop o una personalizada en `docker-compose`.

---

### Código disponible:
- Script en Python para inserción y generación de datos (`main.py`).
- Ejemplo de archivo CSV (`Jugadoras y Equipos.csv`).

---

## Sección "Código"

El repositorio contiene:
- `main.py`: Script principal para cargar datos en Neo4j.
- `Jugadoras y Equipos.csv`: Dataset de entrada con 100 registros para la liga.
- Documentación adicional sobre cómo configurar y ejecutar el entorno.

### Acceso al Código
El código está disponible públicamente en el siguiente repositorio:
[Repositorio de GitHub](https://github.com/Sevillanojr3/actividadBDNOSQL_ATBD.git)

Por favor, accede al enlace para revisar el proyecto.

## Agradecimientos y Uso de Herramientas de Apoyo

En el desarrollo de este proyecto, se utilizó **ChatGPT**, un modelo de inteligencia artificial de OpenAI, como herramienta de soporte para las siguientes tareas:

1. **Conexión a la Base de Datos Neo4j:**
   - ChatGPT ayudó a definir el código necesario para establecer la conexión a la base de datos utilizando la biblioteca `neo4j` en Python.
   - Se proporcionaron ejemplos prácticos y ajustados para garantizar que los datos fueran cargados correctamente desde el archivo CSV al entorno de Neo4j.

2. **Definición de Consultas (Queries) en Cypher:**
   - ChatGPT fue una herramienta clave para redactar y optimizar las queries en Cypher utilizadas para:
     - Crear nodos y relaciones (jugadoras, equipos, ligas, partidos y jugadas).
     - Implementar modificaciones específicas en los datos, como cambios en los nombres de las jugadoras.
     - Generar lógica avanzada, como jugadas aleatorias y condiciones basadas en resultados.

3. **Redacción y Formato del README:**
   - ChatGPT ayudó a estructurar y dar formato al README, asegurando que la documentación fuera clara, profesional y comprensible.
   - Se incluyeron explicaciones detalladas sobre el esquema, sentencias de inserción y modificación, y pasos necesarios para replicar el entorno.

---

El uso de ChatGPT permitió acelerar el desarrollo del proyecto y garantizar un nivel de detalle adecuado en cada etapa del proceso. Esta herramienta no solo facilitó la creación de código funcional, sino que también fue fundamental para organizar y documentar correctamente el proyecto.

Si estás interesado en aprender más sobre cómo aprovechar herramientas de inteligencia artificial como ChatGPT para apoyar en proyectos similares, no dudes en explorarlo. Es una herramienta poderosa que puede complementar tus habilidades y optimizar tu tiempo de desarrollo. 

¡Gracias por revisar este proyecto! 😊

--- 
**Nota:** Todos los detalles necesarios para ejecutar el proyecto están incluidos en este archivo README y en la documentación del repositorio.
