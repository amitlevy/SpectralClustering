from invoke import task, call
import numpy as np
import sys

# Tasks file

@task(help={'k': "k is the number of clusters",'n' : "n is the number of data points", "Random" : "If Random=True, k and n are chosen randomly."})
def run(c, k=None, n=None, Random = True):
    MAX_N = 350
    MAX_K = 20
    
    print("****************************************************************")
    clean(c)
    build(c)
    print("****************************************************************")
    print("Max K,N are {},{} for both 3d and 2d.".format(MAX_K,MAX_N))
    
    if Random:
        print("Random is set to True")
        n = np.random.randint(MAX_N//2, MAX_N)
        print("Randomly selected n = ", n)
        k = np.random.randint(MAX_K//2, MAX_K)
        print("Randomly selected k = ", k)
    
    if k == None:
        sys.exit("FATAL: k is missing, and random is set to false.")
    if n == None:
        sys.exit("FATAL: n is missing, and random is set to false.")

    if Random:
        print("****************************************************************")
        print("Running random")
        c.run("python3.8.5 main.py " + str(k) + " " + str(n) + " --Random")
    else:
        print("****************************************************************")
        print("Running non random")
        c.run("python3.8.5 main.py " + str(k) + " " + str(n) + " --no-Random")


def clean(c):
    print("cleaning..")
    c.run("rm -rf build __pycache__ mykmeanssp.cpython-38-x86_64-linux-gnu.so")
    print("done cleaning!")
    
def build(c):
    print("building..")
    c.run("python3.8.5 setup.py build_ext --inplace")
    print("done building!")
    
    
    

