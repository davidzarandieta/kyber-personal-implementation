# Based on https://github.com/GiacomoPope/kyber-py
from polynomials import *
from modules import *
import random
import numpy as np
import math

n= 4
p= 17
alpha = 1 / (math.sqrt(n) * math.log(n)**2) # Parámetro para calcular la desviación estándar
desviacion_estandar = alpha * math.sqrt(n)  # Desviación estándar

R = PolynomialRing(p,n)
M = Module(R)

def generate_e(n, desviacion_estandar):
  valores_normales = np.random.normal(loc=0, scale=desviacion_estandar, size=n)
  valores_absolutos = np.abs(valores_normales)
  valores_enteros_error = np.round(valores_absolutos).astype(int)
  return list(valores_enteros_error)

print("error e: ",generate_e(n, desviacion_estandar))

def genkey():
  
  s0 = R([random.randint(-1,1) for _ in range(n)])
  s1 = R([random.randint(-1, 1) for _ in range(n)])
  s = M([s0,s1]).transpose()

  A00 = R([11,16,16,6])
  A01 = R([3,6,4,9])
  A10 = R([1,10,3,5])
  A11 = R([15,9,1,6])
  A = M([[A00, A01],[A10, A11]])

  A00 = R([1,6,16,6])
  A01 = R([10,0,5,0])
  A10 = R([4,5,8,3])
  A11 = R([4,2,8,9])
  A = M([[A00, A01],[A10, A11]])


  e0 = R(generate_e(n, desviacion_estandar))
  e1 = R(generate_e(n, desviacion_estandar))
  e = M([e0,e1]).transpose()

  t = A @ s + e
  return A,t,s

A,t,s=genkey()

print("A->",A)
print("t->",t)

m = [1,1,0,1]

def encrypt(A,t,m):
  r0 = R(generate_e(n, desviacion_estandar)) 
  r1 = R(generate_e(n, desviacion_estandar))
  r = M([r0, r1]).transpose()
      
  e_10 = R(generate_e(n, desviacion_estandar))
  e_11 = R(generate_e(n, desviacion_estandar))
  e_1 = M([e_10, e_11]).transpose()
      
  e_2 = R(generate_e(n, desviacion_estandar))

  poly_m = R.decode(m).decompress(1)

  print("Message: ",poly_m)
      
  u = A.transpose() @ r + e_1

  v = (t.transpose() @ r)[0][0] + e_2 - poly_m  

  return u,v

u,v=encrypt(A,t,m)
print("u->",u)
print("v->",v)

def decrypt(u,v,s,m):
  m_n = v - (s.transpose() @ u)[0][0]

  m_n_reduced = m_n.compress(1)

  # Convert each degree of x^n to a string of 1s and 0s if x^n is not present
  m_n_reduced_str = ""
  for i in range(len(m)):
      if m_n_reduced[i] != 0:
          m_n_reduced_str += "1"
      else:
          m_n_reduced_str += "0"
  
  return m_n_reduced_str,m_n,m_n_reduced

def bits_to_string(m):
    m_str = ""
    for i in range(len(m)):
              if m[i] != 0:
                  m_str += "1"
              else:
                  m_str += "0"
    return m_str

m_str = bits_to_string(m)
m_n_reduced_str,m_n,m_n_reduced=decrypt(u,v,s,m)

print("Reduced message: ", m_str)
print("\nBefore reduced: ",m_n)
print("Decrypted: ",m_n_reduced_str)


def calculate_accuracy(trials):
    correct_count = 0

    for _ in range(trials):
        m = [random.randint(0, 1) for _ in range(n)]
        A, t, s = genkey()
        u, v = encrypt(A,t,m)
        m_n_reduced_str,m_n,m_n_reduced=decrypt(u,v,s,m)
        m_str = bits_to_string(m)

        if m_str == m_n_reduced_str:
            correct_count += 1

    accuracy = (correct_count / trials) * 100
    return accuracy

# Ejemplo de uso
trials = 10000  # Número de pruebas a realizar
accuracy = calculate_accuracy(trials)
print(f"El porcentaje de acierto es: {accuracy:.2f}%")  