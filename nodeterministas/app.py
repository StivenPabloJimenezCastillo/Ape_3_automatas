import re
from xml.sax.saxutils import escape

from flask import Flask, render_template, request

app = Flask(__name__)

automatas = {
    "telemetria": {
        "nombre": "IoT: HDR (TEMP | HUM)* CRC",
        "alfabeto": ["HDR", "TEMP", "HUM", "CRC"],
        "estados": ["q0", "q1", "q2", "q3"],
        "inicial": "q0",
        "finales": ["q3"],
        "transiciones": {
            ("q0", "HDR"): ["q1"],
            ("q1", "TEMP"): ["q1", "q2"],
            ("q1", "HUM"): ["q1", "q2"],
            ("q1", "CRC"): ["q3"],
            ("q2", "TEMP"): ["q2"],
            ("q2", "HUM"): ["q2"],
            ("q2", "CRC"): ["q3"],
        }
    },

    "proteina": {
        "nombre": "Proteina: K G X* F",
        "alfabeto": ["K", "G", "X", "F"],
        "estados": ["q0", "q1", "q2", "q3", "q4"],
        "inicial": "q0",
        "finales": ["q4"],
        "transiciones": {
            ("q0", "K"): ["q1"],
            ("q1", "G"): ["q2"],
            ("q2", "X"): ["q2", "q3"],
            ("q2", "F"): ["q4"],
            ("q3", "F"): ["q4"],
        }
    },

    "ecommerce": {
        "nombre": "E-commerce: HOME SEARCH+ CART",
        "alfabeto": ["HOME", "SEARCH", "CART"],
        "estados": ["q0", "q1", "q2", "q3"],
        "inicial": "q0",
        "finales": ["q3"],
        "transiciones": {
            ("q0", "HOME"): ["q1"],
            ("q1", "SEARCH"): ["q1", "q2"],
            ("q2", "CART"): ["q3"],
        }
    }
}


def ejecutar_automata(automata, entrada):
    estados_actuales = {automata["inicial"]}
    pasos = []

    for simbolo in entrada:
        nuevos_estados = set()

        for estado in estados_actuales:
            clave = (estado, simbolo)

            if clave in automata["transiciones"]:
                nuevos_estados.update(automata["transiciones"][clave])

        pasos.append({
            "simbolo": simbolo,
            "antes": sorted(estados_actuales),
            "despues": sorted(nuevos_estados)
        })

        estados_actuales = nuevos_estados

    aceptado = any(estado in automata["finales"] for estado in estados_actuales)

    return aceptado, pasos, sorted(estados_actuales)


def parsear_entrada(seleccionado, entrada_texto):
    texto = (entrada_texto or "").strip().upper()

    if not texto:
        return []

    if seleccionado == "proteina":
        # Proteina usa simbolos de un solo caracter: K G X F.
        limpio = re.sub(r"[\s,;]+", "", texto)
        return list(limpio)

    # Telemetria y e-commerce usan tokens (HDR, TEMP, HOME, etc.).
    return [token for token in re.split(r"[\s,;]+", texto) if token]


def construir_diagrama_svg(automata):
    estados = automata["estados"]
    estado_inicial = automata["inicial"]
    estados_finales = set(automata["finales"])

    transiciones_agrupadas = {}
    for (origen, simbolo), destinos in automata["transiciones"].items():
        for destino in destinos:
            transiciones_agrupadas.setdefault((origen, destino), []).append(simbolo)

    separacion = 220
    posicion_y = 210
    radio = 36
    margen = 130
    ancho = max(760, margen * 2 + separacion * max(len(estados) - 1, 1))
    alto = 460

    posiciones = {
        estado: (margen + indice * separacion, posicion_y)
        for indice, estado in enumerate(estados)
    }

    lineas = [
        f'<svg class="diagrama-svg" viewBox="0 0 {ancho} {alto}" role="img" aria-label="Diagrama del automata">',
        "<defs>",
        "<marker id='flecha' markerWidth='10' markerHeight='10' refX='8' refY='3' orient='auto' markerUnits='strokeWidth'>",
        "<path d='M0,0 L0,6 L9,3 z' fill='#34495e' />",
        "</marker>",
        "</defs>",
        f'<text x="{ancho / 2}" y="34" text-anchor="middle" class="titulo-svg">{escape(automata["nombre"])}</text>',
        f'<text x="30" y="{posicion_y + 6}" class="inicio-svg">Inicio</text>',
        f'<line x1="82" y1="{posicion_y}" x2="{posiciones[estado_inicial][0] - radio}" y2="{posicion_y}" class="flecha-svg" marker-end="url(#flecha)" />',
    ]

    for (origen, destino), simbolos in transiciones_agrupadas.items():
        x1, y1 = posiciones[origen]
        x2, y2 = posiciones[destino]
        etiquetas = ", ".join(dict.fromkeys(simbolos))

        if origen == destino:
            control_y = y1 - 118
            lineas.extend([
                f'<path d="M {x1} {y1 - radio} C {x1 + 78} {control_y}, {x1 + 78} {control_y}, {x1} {y1 - radio - 2}" class="flecha-svg curva-svg" marker-end="url(#flecha)" />',
                f'<text x="{x1 + 78}" y="{control_y - 10}" text-anchor="middle" class="etiqueta-svg">{escape(etiquetas)}</text>',
            ])
            continue

        control_y = y1 - 120
        control_x = (x1 + x2) / 2
        lineas.extend([
            f'<path d="M {x1} {y1 - radio} Q {control_x} {control_y} {x2} {y2 - radio}" class="flecha-svg curva-svg" marker-end="url(#flecha)" />',
            f'<text x="{control_x}" y="{control_y - 12}" text-anchor="middle" class="etiqueta-svg">{escape(etiquetas)}</text>',
        ])

    for estado, (x, y) in posiciones.items():
        clase = "estado-svg estado-inicial" if estado == estado_inicial else "estado-svg"
        if estado in estados_finales:
            lineas.append(f'<circle cx="{x}" cy="{y}" r="{radio + 8}" class="estado-final-exterior" />')
        lineas.append(f'<circle cx="{x}" cy="{y}" r="{radio}" class="{clase}" />')
        lineas.append(f'<text x="{x}" y="{y + 5}" text-anchor="middle" class="estado-texto">{escape(estado)}</text>')

    lineas.append("</svg>")
    return "\n".join(lineas)


@app.route("/", methods=["GET", "POST"])
def index():
    seleccionado = "telemetria"
    entrada_texto = ""
    resultado = None
    pasos = []
    estados_finales = []

    if request.method == "POST":
        seleccionado = request.form["automata"]
        entrada_texto = request.form["entrada"]

        entrada = parsear_entrada(seleccionado, entrada_texto)
        automata = automatas[seleccionado]

        resultado, pasos, estados_finales = ejecutar_automata(automata, entrada)

    automata = automatas[seleccionado]
    diagramas = {clave: construir_diagrama_svg(item) for clave, item in automatas.items()}

    return render_template(
        "index.html",
        automatas=automatas,
        automata=automata,
        diagramas=diagramas,
        seleccionado=seleccionado,
        entrada_texto=entrada_texto,
        resultado=resultado,
        pasos=pasos,
        estados_finales=estados_finales
    )


if __name__ == "__main__":
    app.run(debug=True)