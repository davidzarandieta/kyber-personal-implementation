from simple_implementation import *
import random
import math
import numpy as np

n = 3  # Parámetro de seguridad
p = 11  # Número primo entre n^2 y 2n^2
epsilon = 1  # Valor arbitrario > 0
m = round((1 + epsilon) * (n + 1) * math.log(p))  # Parámetro seguridad

alpha_n = alpha(n)

s = generar_s(n, p)
a = generar_a(m, n, p)
e = generar_e(m, alpha_n, n)
b = [calcular_bi(a_i, s, e[i]) for i, a_i in enumerate(a)]

print (a)
a_transpose = np.transpose(a)
print(a_transpose)

e1 = generar_e(m, alpha_n, n)
e2 = generar_e(m, alpha_n, n)
r = generar_s(n, p)


bit = 1
 
u = np.dot(a_transpose, r) + e1
v = np.dot(a_transpose, r) + e2 + bit

bit_decrypted = v - np.transpose(s) * u
