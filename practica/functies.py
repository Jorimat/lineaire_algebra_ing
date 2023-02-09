# nodige functies voor discrete dynamische systemen
from sympy import *
import matplotlib.pyplot as plt


def bepaalKarPol(A, kar = 'lamda'):
    init_printing(pretty_print = True)
    karPol = A.charpoly(symbols(kar))
    ontbinding = factor(karPol)
    return ontbinding


def bepaalEW(A):
    EW = A.eigenvals()
    eigenwaarden = list(EW.keys())
    eigenwaarden.sort(reverse = True, key = abs)
    return eigenwaarden

def maakP(A):
    L = bepaalEW(A)
    EV = A.eigenvects()
    P = Matrix()
    for i in range(len(L)):
        for j in range(len(EV)):
            if L[i] == EV[j][0]: # dezelfde eigenwaarde
                k = EV[j][1]
                if k == 1:
                    P = P.row_join(EV[j][2][0])
                else:
                    for t in range(len(EV[j][2])):
                        P = P.row_join(EV[j][2][t])
    return P
    
def maakD(A):
    EW = A.eigenvals()
    n = A.shape[0]
    eigenwaarden = []
    m = []
    for key, value in EW.items():
        eigenwaarden.append(key)
        m.append(value)
    k = len(EW) # aantal eigenwaarden
    L = []
    for i in range(k):
        L.extend([eigenwaarden[i]]*m[i])
    L.sort(reverse = True, key = abs)
    D = zeros(n)
    for i in range(len(L)):
        D[i,i] = L[i]
    return D


def plotOplossingen(A, c1, c2, k):
    bepaalKarPol(A)
    P = maakP(A)
    D = maakD(A)
    X1 = zeros(k+1, len(c1))
    X2 = zeros(k+1, len(c2))
    plt.figure()
    ax = plt.axes()
    plt.xlabel("$x_1$")
    plt.ylabel("$x_2$")
    kleur = ["blue", "green", "red", "cyan", "magenta", "gray", "purple", "brown", "pink", "yellow", "olive", "orange"]
    # berekening xk    
    h = list(range(1, len(c1)+1))#[1, 2, 3, 4]
    for j in range(len(c1)):
        x1 = []#[c1[j]]
        x2 = []#[c2[j]]
        for i in range(-1,k):
            x1.append(c1[j]*(D[0,0]**(i+1))*P[0,0] + c2[j]*(D[1,1]**(i+1))*P[0,1])
            x2.append(c1[j]*(D[0,0]**(i+1))*P[1,0] + c2[j]*(D[1,1]**(i+1))*P[1,1])
        X1[:,j] = x1
        X2[:,j] = x2
        plt.plot(x1, x2, 'o', color = kleur[j])
        h[j], = plt.plot(x1, x2, kleur[j]) # lijnen
    ax.minorticks_on()
    s = maakLegende(c1, c2)
    plt.legend(h, s, bbox_to_anchor=(1.04,1), loc="upper left")
    plt.tight_layout(rect = [0, 0, 1, 1])
    for i in range(len(c1)):
#        plt.plot(c1[i], c2[i], 'ko')
        plt.plot(X1[0,i], X2[0,i], 'ko')
        plt.grid(True, which = 'both')
    return X1, X2

def plotOplossingenC(A, x0, y0, k):
    plt.figure()
    ax = plt.axes()
    kleur = ["blue", "green", "red", "cyan", "magenta", "gray", "purple", "brown", "pink", "yellow", "olive", "orange"]
    plt.grid(True, which = 'both', axis = 'both')
    X1 = zeros(k+1, len(x0))
    X2 = zeros(k+1, len(y0))
    n = len(x0)
    h = list(range(1, n+1))
    # ax = plt.axes()
    for t in range(n):
        X = Matrix([x0[t], y0[t]])
        for i in range(1, k+1):
    #        xk = A**i*x0
            xk = A*X[:,i-1]
            X = X.row_join(xk)
        X1[:,t] = list(X[0,:])
        X2[:,t] = list(X[1,:])
        plt.plot(X[0,:], X[1,:], 'ko', color = kleur[t])
        h[t], = plt.plot(list(X[0,:]), list(X[1,:]), kleur[t])
    
    for i in range(n):
        plt.plot(x0[i], y0[i], 'ko')
    plt.xlabel("$x_1$")
    plt.ylabel("$x_2$")
    s = maakLegende2(x0, y0)
    plt.legend(h, s, bbox_to_anchor=(1.04,1), loc="upper left")
    plt.tight_layout(rect = [0, 0, 1, 1])
    return X1, X2
    
def maakLegende(c1, c2):
    s = []
    for i in range(len(c1)):
        s.append('($c_1,c_2$) = (' + str(c1[i]) + ',' + str(c2[i]) + ')')
    return s

def maakLegende2(x0, y0):
    s = []
    for i in range(len(x0)):
        s.append('($x_{1_0},x_{2_0}$) = (' + str(x0[i]) + ',' + str(y0[i]) + ')')
    return s