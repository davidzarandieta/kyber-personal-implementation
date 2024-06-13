import math
import random
import numpy as np
import itertools

n = 4  # Parámetro de seguridad
p = 17  # Número primo entre n^2 y 2n^2
epsilon = 0.35  # Valor arbitrario > 0
m = round((1 + epsilon) * (n + 1) * math.log(p))  # Parámetro seguridad
alpha = 1 / (math.sqrt(n) * math.log(n)**2) # Parámetro para calcular la desviación estándar
desviacion_estandar = alpha * math.sqrt(n)  # Desviación estándar
bit = 1 # Bit a encriptar


# CLAVE PRIVADA
def generate_s(n, p):
    # Función para generar uniformemente la clave s
    return [random.randint(0, p - 1) for _ in range(n)]

s = generate_s(n, p)  # Clave privada s

print("La clave privada s generada uniformemente en Z_{}^{} es: {}".format(p, n, s))

# CLAVE PUBLICA
def generate_a(m, n, p):
    # Función para generar aleatoriamente la clave a
    return [[random.randint(0, p - 1) for _ in range(n)] for _ in range(m)]

def generate_e(m, desviacion_estandar, p):
    # Función para generar el error e
    valores_normales = np.random.normal(loc=0, scale=desviacion_estandar, size=m)
    valores_absolutos = np.abs(valores_normales)
    valores_enteros_error = np.round(valores_absolutos).astype(int)
    return valores_enteros_error

a = generate_a(m, n, p) # Clave pública a
e = generate_e(m, epsilon, p)  # error e

print("Los vectores a generados independientemente en Z_{}^{} son:".format(p, n))
for i, vector in enumerate(a, start=1):
    print("a{}: {}".format(i, vector))
print("\nLos elementos e generados independientemente según la distribución χ son:", e)

def calculate_bi(a, s, e):
    dot_product = np.dot(a, s)  # Producto punto entre a y s
    b = dot_product + e  # Sumar el error e
    return b

b = [calculate_bi(a_i, s, e[i]) for i, a_i in enumerate(a)]  # Calcular b_i para cada a_i

print("La clave b es:", b)

# ENCRIPTADO

def choose_random_subset(m):
    # Generar todos los subconjuntos posibles de [m]
    all_subsets = list(itertools.chain.from_iterable(itertools.combinations(range(m), r) for r in range(m + 1)))
    # Elegir un subconjunto al azar
    random_subset = random.choice(all_subsets)
    return random_subset

S = choose_random_subset(m)  # Subconjunto S
print("El conjunto S elegido al azar es:", S)



def encrypt_bit(bit, S, a, b, p):
    # Calcular la suma de los vectores a y b para los elementos en S
    sum_a = np.zeros_like(a[0])
    for i in S:
        sum_a += a[i]
    sum_b = sum(b[i] for i in S)
    # Si el bit es 0, devolver la suma de los vectores a y b
    if bit == 0:
        return sum_a.tolist(), sum_b
    # Si el bit es 1, devolver la suma de los vectores a y b más p/2
    elif bit == 1:
        return sum_a.tolist(), ((p // 2) + sum_b)


encrypted_values = encrypt_bit(bit, S, a, b, p)
print("Los valores encriptados para el bit", bit, "son:", encrypted_values)

# DESENCRIPTADO

def decrypt(encrypted_values, s, p):
    sum_a, sum_b = encrypted_values
    dot_product = np.dot(sum_a, s)
    diff = (sum_b - dot_product)

    print("El resultado de la desencriptación es:", diff)
    if diff < 0: #si es neqativo se le va sumando p para obtener el mod p
        diff += p
    
    # Verificar si la diferencia es más cercana a p/2 que a 0
    if diff < (p // 2)/2:
        return 0
    else:
        return 1



resultado_desencriptado = decrypt(encrypted_values, s, p)
print("El resultado desencriptado es:", resultado_desencriptado)


#PRUEBA DE RENDIMIENTO DE LA IMPLEMENTACIÓN

""" def calcular_porcentaje_acierto(n):
    coincidencias = 0

    for _ in range(n):
        bit_original = random.choice([0, 1])
        s= generate_s(n, p)
        a = generate_a(m, n, p)
        e = generate_e(m, epsilon, p)
        b = [calculate_bi(a_i, s, e[i]) for i, a_i in enumerate(a)]
        S = choose_random_subset(m)
        bit_encriptado = encrypt_bit(bit_original, S, a, b, p)
        bit_desencriptado = decrypt(bit_encriptado, s, p)

        if bit_original == bit_desencriptado:
            coincidencias += 1

    porcentaje_acierto = (coincidencias / n) * 100
    return porcentaje_acierto

n = 1000  # Número de bits a probar
porcentaje_acierto = calcular_porcentaje_acierto(n)
print(f"El porcentaje de acierto es: {porcentaje_acierto:.2f}%") """