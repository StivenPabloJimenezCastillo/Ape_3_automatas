from flask import Flask, render_template, request

app = Flask(__name__)


automatas = {
    "pagos": {
        "nombre": "Sistema de pagos: a -> c -> l",
        "descripcion": "Debe autorizar, capturar y liquidar en ese orden.",
        "alfabeto": ["a", "c", "l", "f"],
        "estados": ["q0", "q1", "q2", "q3", "q_er"],
        "inicial": "q0",
        "finales": ["q3"],
        "transiciones": {
            ("q0", "a"): "q1",
            ("q0", "f"): "q_er",
            ("q1", "c"): "q2",
            ("q1", "f"): "q_er",
            ("q2", "l"): "q3",
            ("q2", "f"): "q_er",
        },
        "placeholder": "Ej: acl",
        "nota": "Usa simbolos de un caracter: a (autoriza), c (captura), l (liquida), f (cancela).",
    },
    "cerradura": {
        "nombre": "Cerradura inteligente: maximo 3 intentos",
        "descripcion": "Se abre con c y se bloquea con tres i consecutivas.",
        "alfabeto": ["c", "i"],
        "estados": ["q0", "q1", "q2", "q3", "q_er"],
        "inicial": "q0",
        "finales": ["q3"],
        "transiciones": {
            ("q0", "c"): "q3",
            ("q0", "i"): "q1",
            ("q1", "c"): "q3",
            ("q1", "i"): "q2",
            ("q2", "c"): "q3",
            ("q2", "i"): "q_er",
            ("q_er", "c"): "q_er",
            ("q_er", "i"): "q_er",
            ("q3", "c"): "q3",
            ("q3", "i"): "q3",
        },
        "placeholder": "Ej: iic",
        "nota": "Usa simbolos de un caracter: c (correcto) e i (incorrecto).",
    },
    "cientifica": {
        "nombre": "Compilador: numero en notacion cientifica",
        "descripcion": "Valida cadenas como +3.14e-10 o .5e2.",
        "alfabeto": ["+", "-", ".", "e", "E", "0-9"],
        "estados": ["q0", "q1", "q2", "q3", "q4", "q5", "q6", "q_er"],
        "inicial": "q0",
        "finales": ["q5"],
        "transiciones": {
            ("q0", "signo"): "q1",
            ("q0", "digito"): "q2",
            ("q0", "."): "q3",
            ("q0", "exp"): "q_er",
            ("q1", "digito"): "q2",
            ("q2", "."): "q3",
            ("q2", "exp"): "q4",
            ("q3", "digito"): "q3",
            ("q3", "exp"): "q4",
            ("q4", "digito"): "q5",
            ("q4", "signo"): "q6",
            ("q5", "digito"): "q5",
            ("q6", "digito"): "q5",
        },
        "placeholder": "Ej: +3.14e-10",
        "nota": "Se procesa caracter por caracter. Debe terminar en exponente numerico valido.",
    },
}


def token_cientifica(simbolo):
    if simbolo.isdigit():
        return "digito"
    if simbolo in {"+", "-"}:
        return "signo"
    if simbolo in {"e", "E"}:
        return "exp"
    if simbolo == ".":
        return "."
    return "otro"


def parsear_entrada(clave_automata, entrada_texto):
    texto = (entrada_texto or "").strip()
    if not texto:
        return []

    if clave_automata == "cientifica":
        return list(texto)

    limpio = "".join(texto.split()).lower()
    return list(limpio)


def ejecutar_automata(clave_automata, automata, entrada):
    estado_actual = automata["inicial"]
    pasos = []
    error = None

    for simbolo in entrada:
        estado_previo = estado_actual

        if clave_automata == "cientifica":
            token = token_cientifica(simbolo)
            destino = automata["transiciones"].get((estado_actual, token))
            simbolo_mostrado = simbolo
        else:
            destino = automata["transiciones"].get((estado_actual, simbolo))
            simbolo_mostrado = simbolo

        if destino is None:
            error = "No existe transicion para el simbolo en el estado actual."
            pasos.append(
                {
                    "simbolo": simbolo_mostrado,
                    "antes": estado_previo,
                    "despues": "-",
                    "observacion": "Transicion invalida",
                }
            )
            break

        estado_actual = destino
        pasos.append(
            {
                "simbolo": simbolo_mostrado,
                "antes": estado_previo,
                "despues": estado_actual,
                "observacion": "Transicion aplicada",
            }
        )

    aceptado = error is None and estado_actual in automata["finales"]

    if error:
        mensaje = "Cadena rechazada: transicion no definida."
    elif aceptado:
        mensaje = "Cadena aceptada por el automata."
    else:
        mensaje = "Cadena rechazada: termino en estado no final."

    return {
        "aceptado": aceptado,
        "estado_final": estado_actual,
        "pasos": pasos,
        "mensaje": mensaje,
        "error": error,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    seleccionado = "pagos"
    entrada_texto = ""
    resultado = None

    if request.method == "POST":
        seleccionado = request.form.get("automata", "pagos")
        entrada_texto = request.form.get("entrada", "")

        automata = automatas[seleccionado]
        entrada = parsear_entrada(seleccionado, entrada_texto)
        resultado = ejecutar_automata(seleccionado, automata, entrada)

    automata = automatas[seleccionado]

    return render_template(
        "index.html",
        automatas=automatas,
        automata=automata,
        seleccionado=seleccionado,
        entrada_texto=entrada_texto,
        resultado=resultado,
    )


if __name__ == "__main__":
    app.run(debug=True)
