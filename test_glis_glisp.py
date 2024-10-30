# PACKAGES

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from glis.solvers import GLIS
from glis.solvers import GLISp

# FUNCTION DEFINITION

def six_hump_camel(x):
    return (4-2.1*x[0]**2+x[0]**4/3)*(x[0]**2)+x[0]*x[1]+(-4+4*x[1]**2)*x[1]**2

# GRID

x = np.linspace(-2, 2, 500)  # x values from -2 to 2
y = np.linspace(-1, 1, 500)  # y values from -1 to 1
X, Y = np.meshgrid(x, y)  # Create a grid
Z = six_hump_camel([X,Y])  # Function evaluation

# 2D CONTOUR PLOT

plt.contour(X, Y, Z, levels=50, cmap="viridis")  # Adjust levels for detail and choose a color map
plt.xlabel("x")
plt.ylabel("y")
plt.title("Six-Hump Camel Function")
plt.colorbar(label="Function Value")  # Color bar legend
plt.show()  # Display the plot

# 3D SURFACE PLOT

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor='none', alpha=0.8)
ax.set_title("3D Visualization of the Six-Hump Camel Function")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("Function Value")
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label="Function Value")
plt.show()

# GLIS OPTIMIZATION

lb = np.array([-2.0, -1.0]) # Lower bound
ub = np.array([2.0, 1.0])   # Upper bound 
prob = GLIS(bounds=(lb,ub), n_initial_random=10)        # initialize GLIS object
xopt, fopt = prob.solve(six_hump_camel,max_evals=60)    # solve problem
xseq=np.array(prob.X)
fseq=np.array(prob.F)
fbest_seq = prob.fbest_seq

# GLIS 2D CONTOUR PLOT

print(fseq)

plt.contour(X, Y, Z, levels=50, cmap="viridis")  # Adjust levels for detail and choose a color map
plt.xlabel("x")
plt.ylabel("y")
plt.title("Six-Hump Camel Function")
plt.colorbar(label="Function Value")  # Color bar legend

plt.scatter(xseq[0:49,0],xseq[0:49,1], color="red", label="First 50 Iterations", s=10, edgecolor="black")
plt.legend()
plt.scatter(xseq[50:59,0],xseq[50:59,1], color="yellow", label="Last 10 Iterations", s=30, edgecolor="black")
plt.legend()

plt.show()  # Display the plot

# GLIS 3D SURFACE PLOT

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor='none', alpha=0.8)
ax.set_title("3D Visualization of the Six-Hump Camel Function")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("Function Value")
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label="Function Value")

ax.scatter(xseq[0:49,0],xseq[0:49,1], fseq[0:49], color="red", label="First 50 Iterations", s=10, edgecolor="black")
ax.legend()
ax.scatter(xseq[50:59,0],xseq[50:59,1], fseq[50:59], color="white", label="Last 10 Iterations", s=30, edgecolor="black")
ax.legend()

plt.show()

# GLISp OPTIMIZATION

def pref_fun(x1,x2):
	# Synthetic preference function mapping (x1,x2) to {-1,0,1}
    tol = 1.e-3
    f1 = six_hump_camel(x1)
    f2 = six_hump_camel(x2)
    if f1 <= f2 - tol:
        pref = -1
    elif f1 >= f2 + tol:
        pref = 1
    else:
        pref = 0
    return pref

lb = np.array([-2.0, -1.0]) # Lower bound
ub = np.array([2.0, 1.0])   # Upper bound 
prob = GLISp(bounds=(lb, ub), n_initial_random=10)    # initialize GLISp object
xopt = prob.solve(pref_fun, max_prefs=60)             # solve problem
xseq=np.array(prob.X)
fseq=np.array(prob.F)

# GLISp 2D CONTOUR PLOT

plt.contour(X, Y, Z, levels=50, cmap="viridis")  # Adjust levels for detail and choose a color map
plt.xlabel("x")
plt.ylabel("y")
plt.title("Six-Hump Camel Function")
plt.colorbar(label="Function Value")  # Color bar legend

plt.scatter(xseq[0:49,0],xseq[0:49,1], color="red", label="First 50 Iterations", s=10, edgecolor="black")
plt.legend()
plt.scatter(xseq[50:59,0],xseq[50:59,1], color="yellow", label="Last 10 Iterations", s=30, edgecolor="black")
plt.legend()

plt.show()  # Display the plot

# GLISp 3D SURFACE PLOT

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor='none', alpha=0.8)
ax.set_title("3D Visualization of the Six-Hump Camel Function")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("Function Value")
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label="Function Value")

ax.scatter(xseq[0:49,0],xseq[0:49,1], six_hump_camel([xseq[0:49,0],xseq[0:49,1]]), color="red", label="First 50 Iterations", s=10, edgecolor="black")
ax.legend()
ax.scatter(xseq[50:59,0],xseq[50:59,1], six_hump_camel([xseq[50:59,0],xseq[50:59,1]]), color="white", label="Last 10 Iterations", s=30, edgecolor="black")
ax.legend()

plt.show()
