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
- Instalar los requisitos con `pip install neo4j pandas pyyaml`.
- Configurar el archivo `config.yaml` (ver detalles más abajo).
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
### 5. Consultas Definidas en Cypher

A continuación, se presentan las consultas diseñadas para analizar los datos en la base de datos Neo4j. Estas queries permiten obtener información sobre los partidos, equipos, y jugadoras en la liga.

#### 1. Ver la cantidad total de partidos jugados
Esta consulta cuenta el número total de nodos `Game`, que representan los partidos en la liga.

```cypher
MATCH (game:Game)
RETURN COUNT(game) AS TotalGames;
```

#### 2. Resultados de los partidos
Para saber cómo quedaron los partidos, puedes ejecutar la siguiente consulta. Cambia el número del partido (`game.number`) según el partido que desees analizar.

```cypher
MATCH (team:Team)-[:PLAYS_IN]->(game:Game {number: 1}) // Cambia el número del juego según corresponda
OPTIONAL MATCH (play:Play)-[:BELONGS_TO_GAME]->(game)
WHERE play.result = "Gol" AND play.team = team.name
RETURN team.name AS Team, COUNT(play) AS Goals
ORDER BY Goals DESC;
```

#### 3. Jugadoras que anotaron goles
Esta consulta muestra qué jugadoras anotaron goles, el equipo al que pertenecen, el equipo oponente contra el que anotaron, el número del partido, y la cantidad de goles anotados.

```cypher
MATCH (player:Player)-[:BELONGS_TO]->(team:Team),
      (play:Play)-[:BELONGS_TO_GAME]->(game:Game),
      (player)-[:SCORES_GOAL]->(play),
      (otherTeam:Team)-[:PLAYS_IN]->(game)
WHERE play.result = "Gol" AND otherTeam <> team
RETURN player.name AS Player,
       team.name AS PlayerTeam,
       otherTeam.name AS OpponentTeam,
       game.number AS MatchNumber,
       COUNT(play) AS GoalsScored
ORDER BY MatchNumber, GoalsScored DESC;
```

#### 4. Jugadoras con más goles
Para identificar qué jugadoras anotaron más de un gol en la liga, se puede usar la siguiente consulta. Retorna el nombre de la jugadora, su equipo y la cantidad total de goles anotados, ordenados de mayor a menor.

```cypher
MATCH (player:Player)-[:BELONGS_TO]->(team:Team),
      (play:Play)-[:BELONGS_TO_GAME]->(game:Game),
      (player)-[:SCORES_GOAL]->(play)
WHERE play.result = "Gol"
WITH player, team, COUNT(play) AS TotalGoals
WHERE TotalGoals > 1
RETURN player.name AS Player,
       team.name AS Team,
       TotalGoals
ORDER BY TotalGoals DESC;
```

---

Estas consultas permiten explorar y analizar diferentes aspectos del modelo de datos, proporcionando insights valiosos sobre la liga y el desempeño de sus equipos y jugadoras. Puedes ejecutarlas directamente en Neo4j Browser para visualizar los resultados.

---

## Configuración del Archivo `config.yaml`

Crea un archivo llamado `config.yaml` en la raíz del proyecto con las credenciales para conectarte a Neo4j. Aquí tienes un ejemplo:

```yaml
neo4j:
  uri: "bolt://localhost:7687"
  username: "neo4j"
  password: "Jr20020194"
```

Este archivo es utilizado por el script para cargar las credenciales necesarias al establecer la conexión con Neo4j. Asegúrate de modificar los valores según tu configuración.

---

## Configuración del Archivo `docker-compose.yaml`

Para simplificar el despliegue de la base de datos Neo4j, puedes usar Docker y `docker-compose`. Crea un archivo llamado `docker-compose.yaml` con el siguiente contenido:

```yaml
version: '3.8'
services:
  neo4j:
    image: neo4j:latest
    container_name: neo4j-db
    ports:
      - "7474:7474" # Puerto para el navegador de Neo4j
      - "7687:7687" # Puerto para conexiones Bolt
    environment:
      - NEO4J_AUTH=neo4j/Jr20020194 # Usuario y contraseña
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs
      - neo4j_import:/var/lib/neo4j/import
      - neo4j_plugins:/plugins

volumes:
  neo4j_data:
  neo4j_logs:
  neo4j_import:
  neo4j_plugins:
```

### Pasos para Usar Docker Compose

1. Instala [Docker Desktop](https://www.docker.com/).
2. Navega al directorio donde está el archivo `docker-compose.yaml`.
3. Ejecuta el siguiente comando para levantar el contenedor:
   ```bash
   docker-compose up -d
   ```
4. Accede al navegador de Neo4j en [http://localhost:7474](http://localhost:7474) con las credenciales `neo4j/Jr20020194`.

---

## Instrucciones para Ejecutar el Script

1. Asegúrate de que el contenedor de Neo4j esté corriendo.
2. Verifica que el archivo `config.yaml` esté configurado correctamente.
3. Ejecuta el script con:
   ```bash
   python main.py
   ```

El script se conectará automáticamente a la base de datos Neo4j en el contenedor y cargará los datos desde el archivo CSV.

---

## Código disponible:
- `main.py`: Script principal para cargar datos en Neo4j.
- `config.yaml`: Archivo de configuración para las credenciales de la base de datos.
- `docker-compose.yaml`: Archivo para desplegar Neo4j en un contenedor.
- `Jugadoras y Equipos.csv`: Dataset de entrada con 100 registros para la liga.

---

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