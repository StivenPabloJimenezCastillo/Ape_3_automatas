def ndt(adn):
    estados = {"q0"}

    for simbolo in adn:
        nuevo_estado = set()

        for estado in estados:
            if estado == "q0":
                if simbolo.lower() == "k":
                    nuevo_estado.add("q1")

            elif estado == "q1":
                if simbolo.lower() == "g":
                    nuevo_estado.add("q2")

            elif estado == "q2":
                if simbolo.lower() == "x":
                    nuevo_estado.update(["q2", "q3"])
                elif simbolo.lower() == "f":
                    nuevo_estado.add("q4")

            elif estado == "q3":
                if simbolo.lower() == "f":
                    nuevo_estado.add("q4")

        estados = nuevo_estado

    return "q4" in estados

adn =["GKFFX","KGXXXXF","KGFXXX","KGF"]

for c in adn:
    if ndt(c):
        print(c,"Aceptada")
    else:
        print(c,"rechazada")
