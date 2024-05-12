import math
import random
import numpy as np
import itertools

n = 3  # Parámetro de seguridad
p = 11  # Número primo entre n^2 y 2n^2
epsilon = 1  # Valor arbitrario > 0
m = round((1 + epsilon) * (n + 1) * math.log(p))  # Parámetro seguridad

def alpha(n):
    # Función que satisface una distribución de probabilidad 𝜒 donde 𝛼(𝑛) es una función que satisface α(n)=o(1/(√n log n)),
    # lo que significa que el límite de n tendiendo a infinito de α(n) es (√n log n) igual a 0.
    return 1 / (math.sqrt(n) * math.log(n)**2)

alpha_n = alpha(n)  # Valor de alpha(n)

# CLAVE PRIVADA
def generar_s(n, p):
    # Función para generar uniformemente la clave s
    return [random.randint(0, p - 1) for _ in range(n)]

s = generar_s(n, p)  # Clave privada s

print("La clave privada s generada uniformemente en Z_{}^{} es: {}".format(p, n, s))

# CLAVE PUBLICA
def generar_a(m, n, p):
    # Función para generar aleatoriamente la clave a
    return [[random.randint(0, p - 1) for _ in range(n)] for _ in range(m)]

def generar_e(m, alpha, n):
    # Función para generar el error e
    return [random.randint(0, round(alpha * (n + 1) * math.log(p))) for _ in range(m)]

a = generar_a(m, n, p)  # Clave pública a
e = generar_e(m, alpha_n, n)  # Error e

print("Los vectores a generados independientemente en Z_{}^{} son:".format(p, n))
for i, vector in enumerate(a, start=1):
    print("a{}: {}".format(i, vector))
print("\nLos elementos e generados independientemente según la distribución χ son:", e)

def calcular_bi(a, s, e):
    dot_product = np.dot(a, s)  # Producto punto entre a y s
    b = dot_product + e  # Sumar el error e
    return b

b = [calcular_bi(a_i, s, e[i]) for i, a_i in enumerate(a)]  # Calcular b_i para cada a_i

print("La clave pública es:", b)

# ENCRIPTACION

def choose_random_subset(m):
    # Generar todos los subconjuntos posibles de [m]
    all_subsets = list(itertools.chain.from_iterable(itertools.combinations(range(m), r) for r in range(m + 1)))
    # Elegir un subconjunto al azar
    random_subset = random.choice(all_subsets)
    return random_subset

S = choose_random_subset(m)  # Subconjunto S
print("El conjunto S elegido al azar es:", S)

def encrypt_bit(bit, S, a, b, p):
    sum_a = np.zeros_like(a[0])
    for i in S:
        sum_a += a[i]
    sum_b = sum(b[i] for i in S)
    print(sum_a, sum_b)
    if bit == 0:
        return sum_a.tolist(), sum_b
    elif bit == 1:
        return sum_a.tolist(), ((p // 2) + sum_b)

bit = 0  # Bit a encriptar
encrypted_values = encrypt_bit(bit, S, a, b, p)
print("Los valores encriptados para el bit", bit, "son:", encrypted_values)

# DESENCRIPTACION

def decrypt(encrypted_values, s, p):
    sum_a, sum_b = encrypted_values
    dot_product = np.dot(sum_a, s)
    diff = (sum_b - dot_product)
    
    # Verificar si la diferencia es más cercana a p/2 que a 0
    if diff <= p // 2:
        return 0
    else:
        return 1


resultado_desencriptado = decrypt(encrypted_values, s, p)
print("El resultado desencriptado es:", resultado_desencriptado)
