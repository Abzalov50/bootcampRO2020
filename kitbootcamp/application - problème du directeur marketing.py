import sys

from kitbootcamp.solver import SCIP

# Paramètres du solveur
solver_name = 'SCIP'
solver = sys.modules[__name__].__getattribute__(solver_name)

# Création d'un modèle
m = solver('Optimisation de la pub')

# Données du problème
budget = 2e6  # Budget du directeur
nb_mini_pub_mag = 20   # Nb minimal de pubs en magazine

# Variables de décision
x1 = m.add_var(lb=0, vtype=m.INTEGER, name='x1')  # Nb de pubs télévisées
x2 = m.add_var(lb=20, vtype=m.INTEGER, name='x2')  # Nb de pubs en magazine

# Contraintes
m.add_constr(70e3 * x1 + 40e3 * x2 <= budget, name='c_budget')

# Fonction objectif
m.set_objective(20e6 * x1 + 10e6 * x2, 'max')

# Résolution du problème
m.optimize()
print()
print('************************* RESULTATS')
print()
x1 = m.get_var_by_name('x1')
x2 = m.get_var_by_name('x2')
print('**** La solution optimale est :', x1, 'pubs télévisées et', x2, 'pubs en magazine')
print('**** Le nombre optimal de personnes atteintes est de', m.objval)
    