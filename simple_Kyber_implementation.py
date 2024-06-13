# Based on https://github.com/GiacomoPope/kyber-py
from polynomials import *
from modules import *
import random
import numpy as np
import math


n= 7 # Parámetro de seguridad que define el tamaño del mensaje en bits
p= 53 # Número primo entre n^2 y 2n^2
alpha = 1 / (math.sqrt(n) * math.log(n)**2) # Parámetro para calcular la desviación estándar
desviacion_estandar = alpha * n  # Desviación estándar
m = [random.randint(0,1) for _ in range(n)] #el mensaje constará de n bits [0,1,...,n-1

R = PolynomialRing(p,n) #Anillo de polinomios con coeficientes en Z_p
M = Module(R) #Módulo de polinomios con coeficientes en Z_p


#GENERAR CLAVE PRIVADA
def generate_s(n):
  # Función para generar uniformemente la clave s
  s0 = R([random.randint(-1,1) for _ in range(n)])
  s1 = R([random.randint(-1, 1) for _ in range(n)])
  s = M([s0,s1]).transpose()
  return s

s = generate_s(n)

print("s->",s)

#GENERAR CLAVE PÚBLICA
def generate_a(n):
  # Función para generar aleatoriamente la clave a
  A00 = R([random.randint(0, p - 1) for _ in range(n)])
  A01 = R([random.randint(0, p - 1) for _ in range(n)])
  A10 = R([random.randint(0, p - 1) for _ in range(n)])
  A11 = R([random.randint(0, p - 1) for _ in range(n)])
  A = M([[A00, A01],[A10, A11]])
  return A

A = generate_a(n)


def generate_e(n, desviacion_estandar):
  # Función para generar el error e
  valores_normales = np.random.normal(loc=0, scale=desviacion_estandar, size=n)
  valores_absolutos = np.abs(valores_normales)
  valores_enteros_error = np.round(valores_absolutos).astype(int)
  return list(valores_enteros_error)

e0 = R(generate_e(n, desviacion_estandar))
e1 = R(generate_e(n, desviacion_estandar))
e = M([e0,e1]).transpose()

def calculate_b(A,s,e):
    # Producto punto entre A y s para definir b
    b = A @ s + e
    return b

b = calculate_b(A,s,e)


print("A->",A)
print("e->",e)
print("b->",b)

#ENCRIPTACIÓN


def bits_to_string(m):
    # Convertir los bits a una cadena de 1s y 0s
    m_str = ""
    for i in range(len(m)):
              if m[i] != 0:
                  m_str += "1"
              else:
                  m_str += "0"
    return m_str

m_str = bits_to_string(m)
print("Reduced message: ", m_str)
def encrypt(A,b,m):
  # Generar r, e_1, e_2
  r0 = R(generate_e(n, desviacion_estandar))
  r1 = R(generate_e(n, desviacion_estandar))
  r = M([r0, r1]).transpose()
      
  e_10 = R(generate_e(n, desviacion_estandar))
  e_11 = R(generate_e(n, desviacion_estandar))
  e_1 = M([e_10, e_11]).transpose()
      
  e_2 = R(generate_e(n, desviacion_estandar))
  # Calcular m a polinomio y reescalado
  poly_m = R.decode(m).decompress(1)

  print("Message: ",poly_m)
  # Calcular u y v    
  u = A.transpose() @ r + e_1

  v = (b.transpose() @ r)[0][0] + e_2 + poly_m  

  return u,v,e_1,e_2,r

u,v,e_1,e_2,r=encrypt(A,b,m)
print("e_1->",e_1)
print("e_2->",e_2)
print("r->",r)
print("u->",u)
print("v->",v)

def decrypt(u,v,s,m):
  # Calcular m_n
  m_n = v - (s.transpose() @ u)[0][0]

  m_n_reduced = m_n.compress(1)

  # Convertir m_n_reduced a una cadena de 1s y 0s
  m_n_reduced_str = ""
  for i in range(len(m)):
      if m_n_reduced[i] != 0:
          m_n_reduced_str += "1"
      else:
          m_n_reduced_str += "0"
  
  return m_n_reduced_str,m_n,m_n_reduced

m_n_reduced_str,m_n,m_n_reduced=decrypt(u,v,s,m)


print("Reduced: ",m_n_reduced)
print("Decrypted: ",m_n_reduced_str)


#PRUEBA DE RENDIMIENTO DE LA IMPLEMENTACIÓN

def calcular_porcentaje_acierto(intentos):
    correct_count = 0

    for _ in range(intentos):
        m = [random.randint(0, 1) for _ in range(n)]
        s = generate_s(n)
        A = generate_a(n)
        e0 = R(generate_e(n, desviacion_estandar))
        e1 = R(generate_e(n, desviacion_estandar))
        e = M([e0,e1]).transpose()
        b = calculate_b(A,s,e)
        u, v, e_1,e_2,r = encrypt(A,b,m)
        m_n_reduced_str,m_n,m_n_reduced=decrypt(u,v,s,m)
        m_str = bits_to_string(m)

        if m_str == m_n_reduced_str:
            correct_count += 1

    precision = (correct_count / intentos) * 100
    return precision

# Ejemplo de uso
intentos = 20000  # Número de pruebas a realizar
precision = calcular_porcentaje_acierto(intentos)
print(f"El porcentaje de acierto es: {precision:.2f}%")