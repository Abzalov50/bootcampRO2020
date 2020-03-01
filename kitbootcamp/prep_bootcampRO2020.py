from math import sqrt


def prog_eq_2nd_degre(a, b, c):
    # Test de confirmité des arguments
    if a == 0:
        print('ERREUR: Le premier argument doit être différent de 0')
        return
    
    sol = solution_eq_2nd_degre(a, b, c)
    
    if sol is None:
        print("L'équation n'admet pas de solutions.")
    elif len(sol) == 1:
        print("L'équation admet une solution double:", sol[0])
    else:
        print("L'équation admet deux solutions:", sol[0], "et", sol[1])


def solution_eq_2nd_degre(a, b, c):
    # Calcul du discriminant
    D = b*b - 4 * a * c
    
    if D > 0:
        x_1 = (-b - sqrt(D)) / (2 * a)
        x_2 = (-b + sqrt(D)) / (2 * a)
        res = (x_1, x_2)
    elif D == 0:
        x_0 = -b / (2 * a)
        res = (x_0,)
    else:
        res = None
    return res

