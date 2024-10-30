## Code to find the optimal friction model parameters based on comfort qualitative assessment given by user using 
## GLISp optimization algorithm
##
## PACKAGES

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from glis.solvers import GLIS
from glis.solvers import GLISp

## OPTIMIZATION PARAMETERS CONSTRAINTS
#
# 0 - f_s   : Stiction coefficient (f_s >= f_c)
# 1 - f_c   : Coulomb friction coefficient (f_c >= 0)
# 2 - v_bk  : Stribeck's breakaway velocity (v_bk >= 0)
# 3 - delta : Factors modeling Stribeck's effect (delta >= 0)
# 4 - k_v   : Viscous friction coefficient
# 
# Recap :
# First four parameters define the Equivalent total friction coefficient f(V), that depends on V (relative velocity 
# between the cable and the sheat).Equivalent total friction coefficient f(V) is then used to compute the resulting 
# friction force F_a on the cable, that also depends on V and k_v, which is in turn used in the controller.

lb =np.array([-0.5,-0.5,-0.5,-0.5,-0.5])    # lower bound
ub =np.array([10,10,10,10,10])              # upper bound

# Matrices/array for Linear inequalities constraints
A = np.array([[1,-1,0,0,0],[0,0,0,-1,0],[0,0,-1,0,0],[0,0,0,0,-1],[0,-1,0,0,0]])
b = np.array([0,0,0,0,0])

# Non-linear function for Equivalent total friction coefficient constraint (-1 <= f(V) <= 1)
def f(x,V):
    friction = x[1] + (x[0] + x[1]) *np.exp((-abs(V)/x[2])**x[3])
    return friction

def g(x,V):
    if f(x,V) > 1:
        nl_function = f(V)-1
    elif f(x.V) < -1:
        nl_function = -1-f(V)
    else:
        nl_function = 0
    
    return nl_function

## PROBLEM : To impose the non-linear constraint on the Equivalent total friction coefficient f(V) we also need 
#            information on the relative velocity between cable and sheat, which we don't have during the 
#            optimization. 

## PREFERENCE ACQUISITION

def get_user_choice():
    choices = ["A", "B", "C"]
    # print("Please select one of the following options:")
    # for choice in choices:
    #     print(f"- {choice}")

    user_choice = input("Enter your choice : \n A - FIRST config is better then SECOND config ; \n B - SECOND config is better then FIRST config ; \n C - Both config are the same \n").strip().upper()
    
    while user_choice not in choices:
        print("Invalid choice. Please select A, B, or C.")
        user_choice = input("Enter your choice : \n A - FIRST config is better then SECOND config ; \n B - SECOND config is better then FIRST config ; \n C - Both config are the same \n").strip().upper()
        
    return user_choice

## PREFERENCE FUNCTION

def pref_fun(x1,x2):

    tol = 1.e-3     # comparison tolerance

    print("PRIMA CONFIGURAZIONE :" , x1 , "*TEST DELLA PRIMA CONFIGURAZIONE*" ) # Qui bisogna inserire il codice per testare la prima configurazione
    print("SECONDA CONFIGURAZIONE :" , x2 , "*TEST DELLA SECONDA CONFIGURAZIONE*" ) # Qui bisogna inserire il codice per testare la seconda configurazione

    choice = get_user_choice()

    if choice == "A":
        pref = -1
    elif choice == "B":
        pref = 1
    else:
        pref = 0
    
    return pref

## OPTIMIZATION

prob = GLISp(bounds=(lb,ub),n_initial_random=5,A=A,b=b)    # initialize GLISp object

xbest, x = prob.initialize()    # get first two random samples

max_prefs = 10   # maximum number of pairwise comparisons

for k in range(max_prefs):
    pref = pref_fun(x, xbest) # evaluate preference
    x = prob.update(pref)
    xbest = prob.xbest
xopt=xbest                    # final optimizer

print(xopt)