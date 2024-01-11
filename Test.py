from scipy.optimize import fsolve

# Définir l'équation qu'on veut résoudre
def equation(r):
    return 2000 * (1 + r)**102 - 0.2

# Donner une valeur pour prendre un guess
initial_guess = 0.01

# Trouver r
r_solution = fsolve(equation, initial_guess)
print(r_solution[0])