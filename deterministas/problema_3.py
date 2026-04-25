"""Un compilador necesita validar si una cadena de texto representa un número válido en notación científica (ej: +3.14e-10, .5e2).
"""

def validar_numero(cadena):
    estado = 'q0'
    
    signos = {'+', '-'}
    digitos = set('0123456789')
    punto = '.'
    exponente = {'e', 'E'}
    
    for simbolo in cadena:
        if estado == 'q0':
            if simbolo in signos:
                estado = 'q1'
            elif simbolo in digitos:
                estado = 'q2'
            elif simbolo == punto:
                estado = 'q3'
            elif simbolo in exponente:
                estado = 'q_er'
            else:
                return 'Cadena no válida'
        elif estado == 'q1':
            if simbolo in digitos:
                estado = 'q2'
            else:
                return 'Cadena no válida'
        elif estado == 'q2':
            if simbolo == punto:
                estado = 'q3'
            elif simbolo in exponente:
                estado = 'q4'
            else:
                return 'Cadena no válida'
        elif estado == 'q3':
            if simbolo in digitos:
                estado = 'q3'
            elif simbolo in exponente:
                estado = 'q4'
            else:
                return 'Cadena no válida'
        elif estado == 'q4':
            if simbolo in digitos:
                estado = 'q5'
            elif simbolo in signos:
                estado = 'q6'
            elif simbolo in punto:
                estado = 'q_er'
            else:
                return 'Cadena no válida'
        elif estado == 'q5':
            if simbolo in digitos:
                estado = 'q5'
            else:
                return 'Cadena no válida'
        elif estado == 'q6':
            if simbolo in digitos:
                estado = 'q5'
            elif simbolo in signos:
                estado = 'q_er'
            else:
                return 'Cadena no válida'

    if estado == 'q5':
        return 'Número válido en notación científica'
    elif estado == 'q_er':
        return 'Número no válido (error en la cadena)'
    else:        
        return 'Cadena incompleta o no válida'
    
# pruebas
print(f"+3.14e-10: {validar_numero('+3.14e-10')}")  # Número válido en notación científica
print(f".5e2: {validar_numero('.5e2')}")  # Número válido en notación científica
print(f"3.14e: {validar_numero('3.14e')}")  # Cadena incompleta o no válida
print(f"e10: {validar_numero('e10')}")  # Cadena no válida
print(f"3.14e-: {validar_numero('3.14e-')}")  # Cadena incompleta o no válida


