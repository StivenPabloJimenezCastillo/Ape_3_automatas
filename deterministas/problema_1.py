"""Un sistema de pagos debe asegurar que una transacción pase por los estados correctos (Autorización
-> Captura -> Liquidación) antes de ser considerada "Completada". No se puede liquidar sin capturar.
"""
def transicion(cadena):
    estado = 'q0'
    """autorizado = a, captura= c, liquidacion = l, cancelar = f"""
    for simbolo in cadena:
        if estado == 'q0':
            if simbolo ==  'a':
                estado = 'q1'
            elif simbolo == 'f':
                return 'q_er'
            else:
                return 'Cadena no válida'
        elif estado == 'q1':
            if simbolo == 'c':
                estado = 'q2'
            elif simbolo == 'f':
                return 'q_er'
            else:
                return 'Cadena no válida'
        elif estado == 'q2':
            if simbolo == 'l':
                estado = 'q3'
            elif simbolo == 'f':
                return 'q_er'
            else:
                return 'Cadena no válida'
        
    if estado == 'q3':
        return 'Transacción completada (Estado de liquidación)'
    elif estado == 'q_er':
        return 'Transacción cancelada (Estado de error)'
    else:
        return 'Cadena incompleta'
    
# Pruebas
"""print(transicion('af'))  # Transacción cancelada (Estado de error)
print(transicion('acll'))  # Transacción cancelada (Estado de error)
print(transicion('aclf'))  # Transacción cancelada (Estado de error)
print(transicion('af'))  # Transacción cancelada (Estado de error)
print(transicion('f'))  # Transacción cancelada (Estado de error)
print(transicion('al'))  # Transacción cancelada (Estado de error)
print(transicion('acl'))  # Transacción completada (Estado de liquidación)
"""