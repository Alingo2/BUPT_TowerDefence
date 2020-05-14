import math
from matplotlib import pyplot as plt
def zuhe(a,b):
    res=0
    k=1
    j=1
    for i in range(0,a):
        k=k*(a-i)
        j=j*(b-i)
    res=j/k
    return res

def cul(m,q):
    x=[]
    y=[]
    y1=[]
    p1=10
    p2=5000
    s=50
    for i in range (0,m+1):
        x.append(i)
        E=0
        print(i)
        if i<=q:
            for j in range(1,i+1):
                #print(E)
                E=E+(p2*j+p1*(i-j))*(zuhe(j,q)*zuhe(i-j,m-q)/zuhe(i,m))
            E=E+p1*i*(zuhe(i,m-q))/zuhe(i,m)
            print(E)
        else:
            for j in range(1,q+1):
                print(E)
                E=E+(p2*j+p1*(i-j))*(zuhe(j,q)*zuhe(i-j,m-q)/zuhe(i,m))
            print(E)
            E=E+i*p1*(zuhe(i,m-q)/zuhe(i,m))
            print(E)
        E = E - s * i
        y.append(E)
        if i==0:
            y1.append(0)
        else:
            y1.append(E/i)

    plt.plot(x,y)
    plt.show()
    plt.plot(x,y1)
    plt.show()

print(zuhe(8,0))
#cul(5,0)
cul(80,8)
print(zuhe(2,5))