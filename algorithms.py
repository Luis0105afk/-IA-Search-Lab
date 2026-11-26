
from collections import deque
from heapq import heappush, heappop
import random

# ==========================================================
# COLORES
# ==========================================================

GREEN = "#58D8A4"
PINK = "#E48BA9"
PURPLE = "#C8A6E8"
CORAL = "#FF967C"
GOLD = "#F5C76B"

# ==========================================================
# LECCIONES
# ==========================================================

LESSONS = {

    "Ciega": (
        "🔎",
        "Búsqueda ciega o no informada",
        GREEN,

        [
            (
                "Definición",
                "La búsqueda ciega explora estados sin "
                "estimar su cercanía al objetivo. Conoce "
                "el estado inicial, las acciones y la "
                "condición de solución."
            ),

            (
                "Funcionamiento de BFS",
                "BFS utiliza una cola FIFO. Primero visita "
                "el estado inicial, después todos sus "
                "vecinos y posteriormente los siguientes "
                "niveles del grafo."
            ),

            (
                "Características",
                "• No utiliza heurísticas.\n"
                "• Explora por niveles.\n"
                "• Registra los estados visitados.\n"
                "• Encuentra rutas mínimas en pasos "
                "cuando las aristas tienen igual costo."
            ),

            (
                "Ventajas y desventajas",
                "VENTAJAS\n"
                "• Fácil implementación.\n"
                "• Es completo en grafos finitos.\n"
                "• Encuentra rutas mínimas en pasos.\n\n"
                "DESVENTAJAS\n"
                "• Puede explorar muchos estados.\n"
                "• Puede consumir bastante memoria."
            ),

            (
                "Aplicaciones",
                "• Laberintos.\n"
                "• Redes de computadoras.\n"
                "• Redes sociales.\n"
                "• Exploración de grafos.\n"
                "• Videojuegos."
            ),

            (
                "Ejemplo",
                "En un laberinto, BFS explora primero "
                "las casillas cercanas al inicio y "
                "continúa por niveles hasta encontrar "
                "la salida."
            )
        ]
    ),

    "Heuristica": (
        "🎯",
        "Búsqueda heurística o informada",
        PINK,

        [
            (
                "Definición",
                "La búsqueda heurística utiliza "
                "información adicional para orientar "
                "la exploración hacia estados "
                "que parecen prometedores."
            ),

            (
                "Funcionamiento de A*",
                "A* utiliza:\n\n"
                "f(n) = g(n) + h(n)\n\n"
                "g(n): costo recorrido.\n"
                "h(n): costo restante estimado.\n"
                "f(n): costo total estimado.\n\n"
                "Prioriza los estados con menor f(n)."
            ),

            (
                "Características",
                "• Utiliza una heurística.\n"
                "• Considera costos acumulados.\n"
                "• Emplea una cola de prioridad.\n"
                "• Puede encontrar rutas óptimas "
                "bajo condiciones apropiadas."
            ),

            (
                "Ventajas y desventajas",
                "VENTAJAS\n"
                "• Orienta la exploración.\n"
                "• Puede reducir los estados explorados.\n\n"
                "DESVENTAJAS\n"
                "• Necesita una heurística adecuada.\n"
                "• Puede consumir mucha memoria."
            ),

            (
                "Aplicaciones",
                "• Navegación GPS.\n"
                "• Robótica.\n"
                "• Videojuegos.\n"
                "• Planificación de rutas.\n"
                "• Rompecabezas."
            ),

            (
                "Ejemplo",
                "En una cuadrícula, A* puede utilizar "
                "la distancia Manhattan para estimar "
                "cuántos movimientos faltan "
                "hasta el destino."
            )
        ]
    ),

    "Evolutiva": (
        "🧬",
        "Búsqueda evolutiva",
        CORAL,

        [
            (
                "Definición",
                "Los algoritmos evolutivos son métodos "
                "de optimización inspirados en procesos "
                "de evolución biológica. Trabajan con "
                "poblaciones de soluciones candidatas."
            ),

            (
                "Funcionamiento",
                "1. Crear una población.\n"
                "2. Evaluar la aptitud.\n"
                "3. Seleccionar individuos.\n"
                "4. Cruzar características.\n"
                "5. Aplicar mutaciones.\n"
                "6. Crear nuevas generaciones."
            ),

            (
                "Características",
                "• Trabajan con poblaciones.\n"
                "• Utilizan selección.\n"
                "• Emplean cruzamiento.\n"
                "• Introducen mutaciones.\n"
                "• No garantizan siempre el óptimo global."
            ),

            (
                "Ventajas y desventajas",
                "VENTAJAS\n"
                "• Son flexibles.\n"
                "• Exploran espacios complejos.\n\n"
                "DESVENTAJAS\n"
                "• Requieren muchas evaluaciones.\n"
                "• Dependen de sus parámetros."
            ),

            (
                "Aplicaciones",
                "• Optimización de horarios.\n"
                "• Transporte.\n"
                "• Diseño industrial.\n"
                "• Selección de características.\n"
                "• Ajuste de parámetros."
            ),

            (
                "Ejemplo",
                "En un problema de rutas, cada individuo "
                "puede representar una secuencia de "
                "destinos. Las rutas se evalúan, "
                "seleccionan, combinan y modifican."
            )
        ]
    )
}

# ==========================================================
# BANCO DE PREGUNTAS
# ==========================================================

QUESTIONS = {

    "Ciega": [

        (
            "¿Qué estructura utiliza BFS?",
            [
                "Cola FIFO",
                "Pila LIFO",
                "Población",
                "Heurística"
            ],
            0,
            "BFS utiliza una cola FIFO."
        ),

        (
            "¿Cómo explora BFS?",
            [
                "Por mutación",
                "Por niveles",
                "Por aptitud",
                "Al azar"
            ],
            1,
            "BFS explora por niveles."
        ),

        (
            "¿Qué NO usa la búsqueda ciega?",
            [
                "Estados",
                "Acciones",
                "Heurísticas",
                "Objetivos"
            ],
            2,
            "No utiliza estimaciones heurísticas."
        ),

        (
            "¿Cuándo encuentra BFS la ruta mínima en pasos?",
            [
                "Siempre",
                "Con mutación",
                "Solo con A*",
                "Con aristas de igual costo"
            ],
            3,
            "BFS minimiza el número de aristas."
        ),

        (
            "¿Qué significa FIFO?",
            [
                "Primero en entrar, primero en salir",
                "Último en entrar, primero en salir",
                "Mayor aptitud primero",
                "Menor heurística primero"
            ],
            0,
            "First In, First Out."
        )
    ],

    "Heuristica": [

        (
            "¿Qué función utiliza A*?",
            [
                "f=g-h",
                "f=g+h",
                "f=g×h",
                "f=h-g"
            ],
            1,
            "A* utiliza f(n)=g(n)+h(n)."
        ),

        (
            "¿Qué representa h(n)?",
            [
                "Población",
                "Mutación",
                "Costo restante estimado",
                "Generación"
            ],
            2,
            "h(n) estima el costo restante."
        ),

        (
            "¿Dónde puede utilizarse A*?",
            [
                "Cruzamiento",
                "Selección genética",
                "Mutación",
                "Navegación"
            ],
            3,
            "A* puede utilizarse para planificar rutas."
        ),

        (
            "¿Qué representa g(n)?",
            [
                "Costo acumulado",
                "Población",
                "Mutación",
                "Probabilidad"
            ],
            0,
            "g(n) representa el costo recorrido."
        ),

        (
            "¿Para qué sirve una heurística?",
            [
                "Crear individuos",
                "Orientar la búsqueda",
                "Crear genes",
                "Eliminar objetivos"
            ],
            1,
            "Ayuda a priorizar estados."
        )
    ],

    "Evolutiva": [

        (
            "¿Qué operaciones utiliza un algoritmo genético?",
            [
                "FIFO",
                "A*",
                "Selección, cruzamiento y mutación",
                "Solo BFS"
            ],
            2,
            "Son operaciones de los algoritmos genéticos."
        ),

        (
            "¿Qué es una población?",
            [
                "Una cola",
                "Una heurística",
                "Una ruta fija",
                "Conjunto de soluciones"
            ],
            3,
            "Contiene soluciones candidatas."
        ),

        (
            "¿Qué mide la aptitud?",
            [
                "Calidad de una solución",
                "Nodos BFS",
                "Tamaño del mapa",
                "Tiempo"
            ],
            0,
            "La aptitud mide la calidad de una solución."
        ),

        (
            "¿Qué es una mutación?",
            [
                "Una cola",
                "Cambio aleatorio",
                "Un nodo",
                "Una heurística"
            ],
            1,
            "Introduce variación aleatoria."
        ),

        (
            "¿Qué busca mejorar la evolución?",
            [
                "La cola FIFO",
                "Los nodos BFS",
                "La calidad de soluciones",
                "El menú"
            ],
            2,
            "Busca mejorar las soluciones."
        )
    ]
}

# ==========================================================
# DIRECCIONES
# ==========================================================

DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1)
]

# ==========================================================
# OBTENER CASILLAS VECINAS
# ==========================================================

def neighbors(maze, position):

    r, c = position

    for dr, dc in DIRECTIONS:

        nr = r + dr
        nc = c + dc

        if (
            0 <= nr < len(maze)
            and 0 <= nc < len(maze[0])
            and maze[nr][nc] == 0
        ):

            yield nr, nc

# ==========================================================
# ALGORITMOS DE BÚSQUEDA BFS Y A*
# ==========================================================

def search_path(
    maze,
    start,
    goal,
    algorithm="BFS"
):

    previous = {start: None}

    visited = []

    # ======================================================
    # BÚSQUEDA CIEGA BFS
    # ======================================================

    if algorithm == "BFS":

        queue = deque([start])

        while queue:

            current = queue.popleft()

            visited.append(current)

            if current == goal:
                break

            for nxt in neighbors(maze, current):

                if nxt not in previous:

                    previous[nxt] = current

                    queue.append(nxt)

    # ======================================================
    # BÚSQUEDA HEURÍSTICA A*
    # ======================================================

    else:

        def heuristic(pos):

            return (
                abs(pos[0] - goal[0])
                + abs(pos[1] - goal[1])
            )

        heap = [
            (heuristic(start), 0, start)
        ]

        best = {start: 0}

        while heap:

            _, cost, current = heappop(heap)

            if cost != best.get(current):
                continue

            visited.append(current)

            if current == goal:
                break

            for nxt in neighbors(maze, current):

                new_cost = cost + 1

                if new_cost < best.get(
                    nxt,
                    float("inf")
                ):

                    best[nxt] = new_cost

                    previous[nxt] = current

                    heappush(
                        heap,
                        (
                            new_cost + heuristic(nxt),
                            new_cost,
                            nxt
                        )
                    )

    # ======================================================
    # RECONSTRUIR RUTA
    # ======================================================

    if goal not in previous:

        return [], visited

    path = []

    current = goal

    while current is not None:

        path.append(current)

        current = previous[current]

    return path[::-1], visited

# ==========================================================
# GENERADOR DE LABERINTOS
# ==========================================================

def generate_maze(level):

    sizes = {
        "Fácil": (11, 15),
        "Medio": (15, 19),
        "Difícil": (19, 25)
    }

    rows, cols = sizes[level]

    maze = [
        [1] * cols
        for _ in range(rows)
    ]

    maze[1][1] = 0

    stack = [(1, 1)]

    while stack:

        r, c = stack[-1]

        options = []

        for dr, dc in [
            (-2, 0),
            (2, 0),
            (0, -2),
            (0, 2)
        ]:

            nr = r + dr
            nc = c + dc

            if (
                1 <= nr < rows - 1
                and 1 <= nc < cols - 1
                and maze[nr][nc] == 1
            ):

                options.append(
                    (nr, nc, dr, dc)
                )

        if options:

            nr, nc, dr, dc = random.choice(
                options
            )

            maze[r + dr // 2][c + dc // 2] = 0

            maze[nr][nc] = 0

            stack.append((nr, nc))

        else:

            stack.pop()

    return (
        maze,
        (1, 1),
        (rows - 2, cols - 2)
    )

# ==========================================================
# GENERADOR DEL JUEGO CAZADOR DE TESOROS
# ==========================================================

def treasure_board(level):

    sizes = {
        "Fácil": (9, 11),
        "Medio": (11, 15),
        "Difícil": (13, 19)
    }

    density = {
        "Fácil": 0.14,
        "Medio": 0.20,
        "Difícil": 0.24
    }

    counts = {
        "Fácil": 3,
        "Medio": 5,
        "Difícil": 7
    }

    rows, cols = sizes[level]

    start = (0, 0)

    while True:

        maze = [
            [
                1 if random.random() < density[level] else 0
                for _ in range(cols)
            ]
            for _ in range(rows)
        ]

        maze[0][0] = 0

        queue = deque([start])

        reachable = {start}

        while queue:

            current = queue.popleft()

            for nxt in neighbors(maze, current):

                if nxt not in reachable:

                    reachable.add(nxt)

                    queue.append(nxt)

        if len(reachable) >= rows * cols * 0.55:

            break

    free = list(reachable - {start})

    treasure_count = counts[level]

    treasures = set(
        random.sample(
            free,
            treasure_count
        )
    )

    available_exits = list(
        set(free) - treasures
    )

    exit_pos = random.choice(
        available_exits
    )

    return (
        maze,
        start,
        exit_pos,
        treasures
    )

# ==========================================================
# GLOSARIO
# ==========================================================

TERMS = {

    "🤖 Inteligencia Artificial":
        "Sistemas capaces de realizar tareas "
        "asociadas con capacidades inteligentes.",

    "⚙️ Algoritmo":
        "Secuencia ordenada de pasos "
        "para resolver un problema.",

    "🔎 Búsqueda ciega":
        "Exploración sin estimaciones heurísticas.",

    "🎯 Búsqueda heurística":
        "Búsqueda guiada por información adicional.",

    "🧬 Búsqueda evolutiva":
        "Optimización inspirada en la evolución.",

    "📌 BFS":
        "Búsqueda en anchura por niveles.",

    "⭐ A*":
        "Algoritmo que combina g(n) y h(n).",

    "🧠 Heurística":
        "Estimación para priorizar estados.",

    "🧬 Algoritmo genético":
        "Método de selección, cruzamiento "
        "y mutación.",

    "📊 Aptitud":
        "Medida de calidad de una solución.",

    "🔀 Mutación":
        "Cambio aleatorio en una solución.",

    "👥 Población":
        "Conjunto de soluciones candidatas.",

    "💎 Tesoro":
        "Objetivo intermedio que el jugador "
        "debe recoger.",

    "🤖 Machine Learning":
        "Aprendizaje de patrones a partir de datos.",

    "🚫 No_corresponde":
        "Etiqueta para textos ajenos "
        "a las categorías estudiadas."
}
