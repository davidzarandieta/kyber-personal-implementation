# Based on https://github.com/GiacomoPope/kyber-py
from polynomials import *
from modules import *

R = PolynomialRing(17, 4)
M = Module(R)

def genkey():
  s0 = R([0,1,-1,1])
  s1 = R([0,1,0,1])
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


  e0 = R([1,0,1,0])
  e1 = R([-1,1,0,0])
  e = M([e0,e1]).transpose()

  t = A @ s + e
  return A,t,s

A,t,s=genkey()

print("A->",A)
print("t->",t)

r0 = R([0,1,-1,1]) 
r1 = R([-1,0,0,1])
r = M([r0, r1]).transpose()
    
e_10 = R([0,1,1,0])
e_11 = R([0,0,1,1])
e_1 = M([e_10, e_11]).transpose()
    
e_2 = R([0,-1,-1,-1])

m = [1,1,0,1]
poly_m = R.decode(m).decompress(1)

print("Message: ",poly_m)
    
u = A.transpose() @ r + e_1

v = (t.transpose() @ r)[0][0] + e_2 - poly_m  

print("u->",u)
print("v->",v)

m_n = v - (s.transpose() @ u)[0][0]

m_n_reduced = m_n.compress(1)

# Convert each degree of x^n to a string of 1s and 0s if x^n is not present
m_n_reduced_str = ""
for i in range(len(m)):
    if m_n_reduced[i] != 0:
        m_n_reduced_str += "1"
    else:
        m_n_reduced_str += "0"

print("Reduced message: ", m_n_reduced_str)
print("\nBefore reduced: ",m_n)
print("Decrypted: ",m_n_reduced_str)