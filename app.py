
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import requests
import random
import os
from datetime import datetime

from algorithms import (
    LESSONS,
    QUESTIONS,
    TERMS,
    neighbors,
    search_path,
    generate_maze,
    treasure_board
)

# ==========================================================
# IA SEARCH LAB 8.0 WEB
# ==========================================================

st.set_page_config(
    page_title="IA Search Lab 8.0",
    page_icon="🔎",
    layout="wide"
)

keyboard = components.declare_component(
    "game_keyboard",
    path=str(Path(__file__).parent / "keyboard")
)

s = st.session_state

# ==========================================================
# ESTADO DE LA APLICACIÓN
# ==========================================================

initial_state = {
    "page": "Inicio",
    "read": {},
    "used": False,
    "history": [],
    "quiz_data": None,
    "quiz_round": 0,
    "active": False,
    "last": {},
    "game": None,
    "last_keyboard_event": None
}

for k, v in initial_state.items():
    if k not in s:
        s[k] = v

# ==========================================================
# DISEÑO
# ==========================================================

st.markdown("""
<style>

h1, h2, h3 {
    color: #58D8A4;
}

[data-testid="stSidebar"] {
    background: #252025;
}

.stButton button {
    border-color: #584650;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# MENÚ LATERAL
# ==========================================================

labels = {
    "Inicio": "🏠 Inicio",
    "Ciega": "🔎 Búsqueda ciega",
    "Heuristica": "🎯 Búsqueda heurística",
    "Evolutiva": "🧬 Búsqueda evolutiva",
    "Clasificador": "🤖 Clasificador ML",
    "Historial": "🕒 Historial",
    "Juegos": "🎮 Zona de juegos",
    "Evaluador": "📝 Evaluador",
    "Glosario": "📚 Glosario"
}

with st.sidebar:

    st.title("✦ IA SEARCH LAB")
    st.caption("LABORATORIO DE IA · V8.0 WEB")

    for key, label in labels.items():

        if st.button(
            label,
            key="nav_" + key,
            use_container_width=True,
            disabled=s.active and key != "Evaluador",
            type="primary" if s.page == key else "secondary"
        ):
            s.page = key
            st.rerun()

    st.caption(
        "🔒 Evaluación en curso"
        if s.active
        else "✓ Navegación disponible"
    )

ready = (
    all(s.read.get(k, False) for k in LESSONS)
    and s.used
)

page = s.page

# ==========================================================
# INICIO
# ==========================================================

if page == "Inicio":

    st.title("IA Search Lab 8.0")

    st.write(
        "Laboratorio educativo de algoritmos de búsqueda "
        "e inteligencia artificial. Explora BFS, A* y "
        "algoritmos evolutivos, practica con los juegos "
        "y comprueba tus conocimientos."
    )

    st.subheader("Progreso del aprendizaje")

    for k in LESSONS:

        st.write(
            ("✅" if s.read.get(k) else "⬜")
            + " "
            + LESSONS[k][1]
        )

    st.write(
        ("✅" if s.used else "⬜")
        + " Clasificación de texto exitosa"
    )

    progress = (
        sum(bool(s.read.get(k)) for k in LESSONS)
        + int(s.used)
    ) / 4

    st.progress(progress)

    st.info(
        "Evaluador disponible"
        if ready
        else "Completa las tres lecturas y una "
             "clasificación para desbloquear el evaluador."
    )

# ==========================================================
# LECCIONES
# ==========================================================

elif page in LESSONS:

    icon, title, color, sections = LESSONS[page]

    st.title(icon + " " + title)

    for i, (name, content) in enumerate(sections, 1):

        with st.container(border=True):

            st.subheader(f"{i:02d} | {name}")
            st.text(content)

    if st.button("▶ Ejecutar demostración"):

        if page == "Evolutiva":

            st.info(
                "SELECCIÓN → CRUZAMIENTO → MUTACIÓN "
                "→ NUEVA GENERACIÓN.\n\n"
                "La aptitud mide la calidad de cada solución."
            )

        else:

            board, start, goal = generate_maze("Fácil")

            alg = "BFS" if page == "Ciega" else "A*"

            path, visited = search_path(
                board,
                start,
                goal,
                alg
            )

            st.success(
                f"{alg}: {len(path)-1} pasos · "
                f"{len(visited)} casillas exploradas"
            )

    if st.button(
        "✓ Marcar como leído",
        disabled=s.read.get(page, False)
    ):

        s.read[page] = True
        st.rerun()

    if s.read.get(page):

        st.success("Lectura completada")

# ==========================================================
# CLASIFICADOR MACHINE LEARNING
# ==========================================================

elif page == "Clasificador":

    st.title("🤖 Clasificador inteligente")

    st.write(
        "Analiza palabras y definiciones "
        "con Machine Learning for Kids."
    )

    st.write(
        "Ciega · Heurística · Evolutivo · No_corresponde"
    )

    value = st.text_area(
        "Escribe el texto que deseas analizar"
    )

    if st.button("🔎 Analizar texto"):

        try:
            key = st.secrets.get("ML_API_KEY", "")
        except Exception:
            key = ""

        key = key or os.getenv("ML_API_KEY", "")

        if not value.strip():

            st.warning(
                "Introduce una palabra o definición."
            )

        elif not key:

            st.error(
                "Configura ML_API_KEY en los secretos "
                "de Streamlit."
            )

        else:

            try:

                with st.spinner("Consultando el modelo..."):

                    response = requests.get(
                        "https://machinelearningforkids.co.uk/"
                        "api/scratch/"
                        + key
                        + "/classify",
                        params={"data": value.strip()},
                        timeout=20
                    )

                if not response.ok:

                    st.error(
                        f"Error HTTP {response.status_code}. "
                        "Comprueba la clave y el modelo."
                    )

                else:

                    predictions = sorted(
                        [
                            {
                                "category": str(x["class_name"]),
                                "confidence": float(x["confidence"])
                            }
                            for x in response.json()
                        ],
                        key=lambda x: x["confidence"],
                        reverse=True
                    )

                    best = predictions[0]

                    record = dict(
                        date=datetime.now().isoformat(
                            timespec="seconds"
                        ),
                        text=value,
                        **best,
                        predictions=predictions
                    )

                    s.history.insert(0, record)

                    s.used = True

            except (
                requests.RequestException,
                ValueError,
                KeyError,
                IndexError,
                TypeError
            ):

                st.error(
                    "No se pudo obtener una clasificación válida."
                )

    if s.history:

        r = s.history[0]

        st.subheader("Último resultado")

        st.success(
            f"{r['category']} · {r['confidence']:.1f}%"
        )

        st.dataframe(
            r["predictions"],
            hide_index=True
        )

# ==========================================================
# HISTORIAL
# ==========================================================

elif page == "Historial":

    st.title("🕒 Historial de clasificaciones")

    if st.button("Borrar historial"):

        s.history = []
        st.rerun()

    for r in s.history:

        with st.expander(
            f"{r['text']} — {r['category']} "
            f"({r['confidence']:.1f}%)"
        ):

            st.caption(r["date"])

            st.dataframe(
                r["predictions"],
                hide_index=True
            )

    if not s.history:

        st.info("Sin consultas registradas.")

# ==========================================================
# ZONA DE JUEGOS
# ==========================================================

elif page == "Juegos":

    st.title("🎮 Zona de juegos")

    mode = st.selectbox(
        "Juego",
        ["Laberinto IA", "Cazador de tesoros"]
    )

    level = st.selectbox(
        "Dificultad",
        ["Fácil", "Medio", "Difícil"]
    )

    if (
        st.button("Nuevo tablero")
        or s.game is None
        or s.game["mode"] != mode
        or s.game["level"] != level
    ):

        if mode == "Laberinto IA":

            board, start, goal = generate_maze(level)
            treasures = set()

        else:

            board, start, goal, treasures = treasure_board(
                level
            )

        s.game = dict(
            mode=mode,
            level=level,
            board=board,
            start=start,
            goal=goal,
            player=start,
            treasures=treasures,
            total=len(treasures),
            steps=0,
            path=[],
            visited=[],
            message="",
            finished=False
        )

    g = s.game

    # ======================================================
    # MOVIMIENTO DEL JUGADOR
    # ======================================================

    def move(dr, dc):

        if g["finished"]:
            return

        r, c = g["player"]

        nxt = (r + dr, c + dc)

        if nxt not in neighbors(
            g["board"],
            g["player"]
        ):
            return

        g["player"] = nxt

        g["steps"] += 1

        g["treasures"].discard(nxt)

        g["path"] = []
        g["visited"] = []
        g["message"] = ""

        if nxt == g["goal"]:

            if not g["treasures"]:

                g["finished"] = True

                g["message"] = "🏆 ¡Nivel completado!"

                if mode == "Laberinto IA":

                    shortest = search_path(
                        g["board"],
                        g["start"],
                        g["goal"]
                    )[0]

                    g["message"] += (
                        f" Ruta mínima: "
                        f"{len(shortest)-1} pasos."
                    )

            else:

                g["message"] = (
                    "Todavía faltan tesoros."
                )

    # ======================================================
    # CONTROLES W, A, S, D
    # ======================================================

    st.write(
        "**Controles:** W = arriba, A = izquierda, "
        "S = abajo, D = derecha."
    )

    event = keyboard(
        disabled=g["finished"],
        key="game_keyboard_input",
        default=None
    )

    if (
        isinstance(event, dict)
        and event.get("id") != s.get("last_keyboard_event")
    ):

        s.last_keyboard_event = event.get("id")

        directions = {
            "w": (-1, 0),
            "a": (0, -1),
            "s": (1, 0),
            "d": (0, 1)
        }

        if event.get("key") in directions:

            move(*directions[event["key"]])

    # ======================================================
    # RESOLVER CON BFS O A*
    # ======================================================

    def solve(alg):

        if mode == "Laberinto IA":

            path, visited = search_path(
                g["board"],
                g["start"],
                g["goal"],
                alg
            )

        else:

            options = [
                search_path(
                    g["board"],
                    g["player"],
                    target,
                    "BFS"
                )
                for target in sorted(
                    g["treasures"] or {g["goal"]}
                )
            ]

            path, visited = min(
                (x for x in options if x[0]),
                key=lambda x: len(x[0]),
                default=([], [])
            )

        g["path"] = path
        g["visited"] = visited

        g["message"] = (
            f"{alg}: {len(path)-1} pasos · "
            f"{len(visited)} casillas exploradas"
            if path
            else "Sin ruta disponible."
        )

    cols = st.columns(3)

    if mode == "Laberinto IA":

        cols[0].button(
            "Resolver BFS",
            on_click=solve,
            args=("BFS",)
        )

        cols[1].button(
            "Resolver A*",
            on_click=solve,
            args=("A*",)
        )

    else:

        cols[0].button(
            "Pista BFS",
            on_click=solve,
            args=("BFS",)
        )

    if cols[2].button("Limpiar ruta"):

        g["path"] = []
        g["visited"] = []
        g["message"] = ""

    # ======================================================
    # CONTADOR
    # ======================================================

    if mode != "Laberinto IA":

        st.caption(
            f"Movimientos: {g['steps']} | "
            f"Tesoros: "
            f"{g['total']-len(g['treasures'])}"
            f"/{g['total']}"
        )

    else:

        st.caption(
            f"Movimientos: {g['steps']}"
        )

    # ======================================================
    # DIBUJAR TABLERO
    # ======================================================

    rows = len(g["board"])
    cols_n = len(g["board"][0])

    path = set(g["path"])
    visited = set(g["visited"])

    cells = []

    for r, row in enumerate(g["board"]):

        for c, wall in enumerate(row):

            p = (r, c)

            color = "#584650" if wall else "#211C20"

            symbol = ""

            if p in visited:

                color = "#52646a"

            if p in path:

                color = "#C8A6E8"

            if p == g["start"]:

                color = "#286a54"

            if p == g["goal"]:

                color = "#F5C76B"
                symbol = "★"

            if p in g["treasures"]:

                color = "#FF967C"
                symbol = "◆"

            if p == g["player"]:

                color = "#58D8A4"
                symbol = "●"

            cells.append(
                f'<div style="background:{color};'
                'aspect-ratio:1;'
                'display:grid;'
                'place-items:center;'
                'color:#191719;'
                'font-size:clamp(8px,2vw,20px)">'
                f'{symbol}</div>'
            )

    st.markdown(
        '<div style="display:grid;'
        f'grid-template-columns:repeat({cols_n},1fr);'
        'gap:2px;max-width:720px">'
        + "".join(cells)
        + "</div>",
        unsafe_allow_html=True
    )

    st.caption(
        "Verde: jugador · Amarillo: salida · "
        "Morado: ruta · Gris claro: exploración · "
        "Naranja: tesoro"
    )

    if g["message"]:

        st.info(g["message"])

    # ======================================================
    # BOTONES DE MOVIMIENTO ALTERNATIVOS
    # ======================================================

    a, b, c = st.columns(3)

    b.button(
        "W ↑ Arriba",
        on_click=move,
        args=(-1, 0),
        use_container_width=True,
        disabled=g["finished"]
    )

    a, b, c = st.columns(3)

    a.button(
        "A ← Izquierda",
        on_click=move,
        args=(0, -1),
        use_container_width=True,
        disabled=g["finished"]
    )

    b.button(
        "S ↓ Abajo",
        on_click=move,
        args=(1, 0),
        use_container_width=True,
        disabled=g["finished"]
    )

    c.button(
        "D → Derecha",
        on_click=move,
        args=(0, 1),
        use_container_width=True,
        disabled=g["finished"]
    )

# ==========================================================
# EVALUADOR CORREGIDO
# ==========================================================

elif page == "Evaluador":

    st.title("📝 Evaluador")

    def new_quiz():

        questions = []

        for category, bank in QUESTIONS.items():

            i = random.choice([
                i
                for i in range(len(bank))
                if i != s.last.get(category)
            ])

            s.last[category] = i

            q, opts, correct, explanation = bank[i]

            options = list(opts)

            random.shuffle(options)

            questions.append(
                dict(
                    q=q,
                    options=options,
                    correct=opts[correct],
                    explanation=explanation
                )
            )

        s.quiz_round += 1

        s.quiz_data = dict(
            questions=questions,
            answers=None
        )

        s.active = True

    # ======================================================
    # REQUISITOS DEL TEST
    # ======================================================

    if not ready:

        st.warning(
            "Completa las tres lecturas "
            "y una clasificación exitosa."
        )

    elif s.quiz_data is None:

        if st.button("Comenzar test"):

            new_quiz()
            st.rerun()

    # ======================================================
    # PREGUNTAS
    # ======================================================

    elif s.quiz_data["answers"] is None:

        # El identificador del formulario es diferente
        # del identificador de los datos del examen.

        with st.form("quiz_form"):

            answers = [
                st.radio(
                    f'{i+1}. {q["q"]}',
                    q["options"],
                    index=None,
                    key=f"question_{s.quiz_round}_{i}"
                )
                for i, q in enumerate(
                    s.quiz_data["questions"]
                )
            ]

            if st.form_submit_button("Calificar"):

                if None in answers:

                    st.warning(
                        "Responde las tres preguntas."
                    )

                else:

                    s.quiz_data["answers"] = answers

                    s.active = False

                    st.rerun()

    # ======================================================
    # RESULTADOS DEL TEST
    # ======================================================

    else:

        score = 0

        for q, a in zip(
            s.quiz_data["questions"],
            s.quiz_data["answers"]
        ):

            st.write(q["q"])

            correct = a == q["correct"]

            score += correct

            st.write(
                ("✅ " if correct else "❌ ") + a
            )

            st.caption(
                "Solución: "
                + q["correct"]
                + " · "
                + q["explanation"]
            )

        st.success(
            f"Calificación: {score}/3 · "
            f"{score/3*100:.1f}%"
        )

        if st.button("Reiniciar test"):

            new_quiz()
            st.rerun()

# ==========================================================
# GLOSARIO
# ==========================================================

elif page == "Glosario":

    st.title("📚 Glosario")

    for term, definition in TERMS.items():

        with st.container(border=True):

            st.subheader(term)

            st.write(definition)
