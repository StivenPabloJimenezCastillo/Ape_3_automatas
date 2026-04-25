def e_comerce(comprador):
    estados = {"q0"}

    for simbolo in comprador:
        nuevo_estado = set()
        for estado in estados:

            if estado == "q0":
                if simbolo == "HOME" :
                    nuevo_estado.add("q1")
            elif estado =="q1":
                if simbolo == "SEARCH":
                    nuevo_estado.update(["q1","q2"])
            elif estado == "q2":
                if simbolo == "CART":
                    nuevo_estado =("q3")

            

        estados =nuevo_estado
    return "q3" in estados



casos = [
    ["HOME", "SEARCH", "CART"],
    ["HOME", "SEARCH", "SEARCH", "CART"],
    ["HOME", "CART"],
    ["SEARCH", "HOME", "CART"],
    ["HOME", "SEARCH"],
]

for c in casos:
    if e_comerce(c):
        print(c, "→ ACEPTADO")
    else:
        print(c, "→ RECHAZADO")