## Code to test the GLISp algorithm in order to maximise the comfort of a pair of jeans
##
## PACKAGES

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from glis.solvers import GLIS
from glis.solvers import GLISp

## OPTIMIZATION PARAMETERS
#
# 0 - Waist Measurement Range: 61 cm - 107 cm (Adjustable in 2.5 cm increments)
# 1 - Inseam Length     Range: 66 cm - 91 cm (Adjustable in 2.5 cm increments)
# 2 - Hip Measurement   Range: 76 cm - 127 cm (Adjustable in 2.5 cm increments)
# 3 - Thigh Measurement Range: 41 cm - 76 cm (Adjustable in 1.25 cm increments)
# 4 - Front Rise        Range: 18 cm - 30.5 cm (Adjustable in 1.25 cm increments)
# 5 - Back Rise         Range: 25.5 cm - 41 cm (Adjustable in 1.25 cm increments)
# 6 - Leg Opening       Range: 20 cm - 46 cm (Adjustable in 1.25 cm increments)
#

lb =np.array([61,66,76,41,18,25.5,20])      # lower bound
ub =np.array([107,91,127,76,30.5,41,46])    # upper bound

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

prob = GLISp(bounds=(lb,ub),n_initial_random=5)    # initialize GLISp object

xbest, x = prob.initialize()    # get first two random samples

max_prefs = 10   # maximum number of pairwise comparisons

for k in range(max_prefs):
    pref = pref_fun(x, xbest) # evaluate preference
    x = prob.update(pref)
    xbest = prob.xbest
xopt=xbest                    # final optimizer

print(xopt)