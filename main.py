import random
from polynomials import *
from modules import *

# Función para convertir un texto string en un polinomio usando codificación ASCII
def text_to_polynomial(text, q, n):
    ascii_values = [ord(char) for char in text]
    # Truncar la lista de coeficientes si es más larga que el grado máximo permitido
    ascii_values = ascii_values[:n]
    # Rellena el texto con caracteres nulos para alcanzar la longitud requerida
    while len(ascii_values) < n:
        ascii_values.append(0)
    return PolynomialRing(q, n)(ascii_values)

# Función para convertir un polinomio en texto usando decodificación ASCII
def polynomial_to_text(polynomial):
    # Obtener los coeficientes del polinomio
    coefficients = polynomial.coeffs
    # Convertir los coeficientes a caracteres ASCII
    ascii_chars = [chr(coeff) for coeff in coefficients]
    # Unir los caracteres en una cadena
    return ''.join(ascii_chars)


# Genera las claves
def genkey():
    s0 = R([0,1,-1,1])
    s1 = R([0,1,0,1])
    s = M([s0,s1]).transpose()

    A00 = R([11,16,16,6])
    A01 = R([3,6,4,9])
    A10 = R([1,10,3,5])
    A11 = R([15,9,1,6])
    A = M([[A00, A01],[A10, A11]])

    e0 = R([1,0,1,0])
    e1 = R([-1,1,0,0])
    e = M([e0,e1]).transpose()

    t = A @ s + e
    return A, t, s

# Cifra un mensaje
def encrypt(message, A):
    r0 = R([0,1,-1,1]) 
    r1 = R([-1,0,0,1])
    r = M([r0, r1]).transpose()
    
    e_10 = R([0,1,1,0])
    e_11 = R([0,0,1,1])
    e_1 = M([e_10, e_11]).transpose()
    
    e_2 = R([0,-1,-1,-1])

    m = text_to_polynomial(message, 17, 4)
    
    u = A.transpose() @ r + e_1
    v = (t.transpose() @ r)[0][0] + e_2 - m
    
    return u, v

# Descifra un mensaje
def decrypt(u, v, s):
    m_n = v - (s.transpose() @ u)[0][0]
    m_n_reduced = m_n.compress(1)
    return m_n_reduced

# Ejemplo de uso
R = PolynomialRing(17, 4)
M = Module(R)

A, t, s = genkey()
print("A->", A)
print("t->", t)

message = "hello"
print("Mensaje original:", message)

u, v = encrypt(message, A)
print("u->", u)
print("v->", v)

decrypted_message = decrypt(u, v, s)
print("Mensaje descifrado:", decrypted_message)
