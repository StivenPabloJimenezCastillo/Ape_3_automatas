"""Una cerradura inteligente que se bloquea después de 3 intentos fallidos. El autómata debe contar los fallos implícitamente en los estados.
"""

def cerradura(cadena):
    estado = 'q0'
    """Intento fallido = i, intento exitoso = c"""
    # alfabeto = {c, i}  C=correcto, i=incorrecto
    for simbolo in cadena:
        if estado == 'q0':
            if simbolo == 'c':
                estado = 'q3'
            elif simbolo == 'i':
                estado = 'q1'
            else:
                return 'Cadena no válida'
        elif estado == 'q1':
            if simbolo == 'c':
                estado = 'q3'
            elif simbolo == 'i':
                estado = 'q2'
            else:
                return 'Cadena no válida'
        elif estado == 'q2':
            if simbolo == 'c':
                estado = 'q3'
            elif simbolo == 'i':
                estado = 'q_er'
            else:
                return 'Cadena no válida'

    if estado == 'q3':
        return 'Exito: Cerradura abierta'
    elif estado == 'q_er':
        return 'Error: Cerradura bloqueada'
    
# Pruebas
print(f"cc {cerradura('cc')}")  # Exito: Cerradura abierta
print(f"iic {cerradura('iic')}")  # Exito: Cerradura abierta
print(f"iii {cerradura('iii')}")  # Error: Cerradura bloqueada
print(f"ic {cerradura('ic')}")  # Exito: Cerradura abierta
print(f"i {cerradura('i')}")  # Cadena incompleta"""
    