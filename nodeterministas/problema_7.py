def telemetria(dispositivo):
    estados = {"q0"}

    for simbolo in dispositivo:
        nuevos_estados = set()

        for estado in estados:
            if estado == "q0":
                if simbolo == "HDR":
                    nuevos_estados.add("q1")

            elif estado == "q1":
                if simbolo == "TEMP" or simbolo == "HUM":
                    nuevos_estados.update(["q1", "q2"])
                elif simbolo == "CRC":
                    nuevos_estados.add("q3")

            elif estado == "q2":
                if simbolo == "TEMP" or simbolo == "HUM":
                    nuevos_estados.add("q2")
                elif simbolo == "CRC":
                    nuevos_estados.add("q3")

        estados = nuevos_estados

    return "q3" in estados
casos = [
    ["HDR", "CRC"],
    ["HDR", "TEMP", "CRC"],
    ["HDR", "HUM", "CRC"],
    ["HDR", "TEMP", "HUM", "TEMP", "CRC"],
    ["TEMP", "HDR", "CRC"],
    ["HDR", "TEMP"],
    ["HDR", "CRC", "TEMP"]
]

for c in casos:
    if telemetria(c):
        print(c, "-> ACEPTADO")
    else:
        print(c, "-> RECHAZADO")