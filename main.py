import numpy as np
from matplotlib import pyplot as plt
from scipy.sparse import coo_matrix, csr_matrix

import fem_utils
from mesh import Mesh
from triplets import Triplets

mesh = Mesh()
# on charge le maillage 2d crée par gmsh
mesh.GmshToMesh("square.msh")

#On commence l'algorithme d'assemblage
triplets_A = Triplets()

#on remplie les données de la matrice A en commençant par calculer les éléments de masse élémentaire
for triangle in mesh.triangles:
    elementary_mass_matrix = (abs(triangle.area())/12) * np.array([[2,1,1],[1,2,1],[1,1,2]])
    for i in range(3):
        for j in range(3):
            triplets_A.append(triangle.get_boundary(i).get_id(), triangle.get_boundary(j).get_id(), elementary_mass_matrix[i][j])

# puis on calcul les éléments de masse élémentaire pour la matrice de rigidité

for triangle in mesh.triangles:
    x1,y1 = triangle.get_boundary(1).get_coord()
    x2,y2 = triangle.get_boundary(2).get_coord()
    x3,y3 = triangle.get_boundary(3).get_coord()
    Bp = (1/triangle.jac())*np.array([[(y3-y1),(y1-y2)],[(x1-x3),(x2-x1)]])
    for i in range(3):
        for j in range(3):
            elementary_rigid_composant= triangle.area() * fem_utils.grad_phi(j).transpose() @ (Bp.transpose() @ Bp) @ fem_utils.grad_phi(i)
            triplets_A.append(triangle.get_boundary(i).get_id(), triangle.get_boundary(j).get_id(), elementary_rigid_composant[0][0])

#on implémente le second membre de l'équation différentielle au dérivée partielles
def f(x,y):
    A = 1 / (1*np.pi ** 2)
    return A *  np.exp(-((x - 0.5)**2 + (y - 0.5)**2) / 1**2)

# On calcul le second membre du système linéaire
B = np.zeros((144,1)).transpose()
for point in mesh.points:
    for triangle in mesh.triangles:
        if point in triangle.points:
            sum = 0
            for i in range(1,4):
                eta_list, nu_list, omega_list, gauss_point_list = triangle.gaussPoint()
                for eta, nu, omega, gauss_point in zip(eta_list, nu_list, omega_list, gauss_point_list):

                    sum += omega*f(gauss_point[0][0], gauss_point[0][1])*fem_utils.phi_ref(triangle, eta, nu,i, mesh)
    B[0][point.get_id()] += sum*abs(triangle.jac())

#application de la condition de Dirichlet:
for segment in mesh.segments:
    if segment.physical_tag == 0:
        id1 = segment.get_boundary(1).get_id()
        id2 = segment.get_boundary(2).get_id()
        for i in range(len(triplets_A.getData()[0])):
            if triplets_A.getData()[1][0][i] == id1 or triplets_A.getData()[1][0][i] == id2 :
                triplets_A.getData()[0][i] = 0
        triplets_A.append(id1, id1, 1)
        triplets_A.append(id2, id2, 1)
        B[0][id1] = 0
        B[0][id2] = 0

# On transforme notre jeu de donnée en une matrice COO pour ensuite pouvoir la convertir en matrice CSR et réaliser les
# calculs.
A_COO = coo_matrix(triplets_A.getData())
A_csr = csr_matrix(A_COO)

#calcul et stockage d'une base de l'espace approché
phi = [None for i in range(mesh.Npts)]
node_check = []
for triangle in mesh.triangles:
    id1 = triangle.get_boundary(1).get_id()
    id2 = triangle.get_boundary(2).get_id()
    id3 = triangle.get_boundary(3).get_id()
    if id1 not in node_check:
        phi[id1-1] = fem_utils.get_shape_functions(triangle,1)
        node_check.append(id1)
    if id2 not in node_check:
        phi[id2-1] = fem_utils.get_shape_functions(triangle,2)
        node_check.append(id2)
    if id3 not in node_check:
        phi[id3-1] = fem_utils.get_shape_functions(triangle,3)
        node_check.append(id3)

# calcul de la solution approchée
U = np.linalg.solve(A_csr.toarray(), B.transpose())

def sol(x,y):
    result = 0
    for i in range(1,mesh.Npts):
        result += U[i] * phi[i](x,y)
    return result

def plot_solution_on_grid(mesh, sol_func, title="Solution sur grille"):

    # Extraire les points du domaine pour l'affiche graphique
    x_coords = [p.x for p in mesh.points]
    y_coords = [p.y for p in mesh.points]
    xmin, xmax = min(x_coords), max(x_coords)
    ymin, ymax = min(y_coords), max(y_coords)

    # Créer une grille régulière
    N = 100  # plus grand = plus fin
    X, Y = np.meshgrid(np.linspace(xmin, xmax, N),
                       np.linspace(ymin, ymax, N))

    # Évaluer la solution sur la grille
    Z = np.vectorize(sol_func)(X, Y)

    # Tracer la surface
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('sol(x, y)')
    ax.set_title(title)
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

    plt.tight_layout()
    plt.show()

plot_solution_on_grid(mesh, sol) # affichage graphique
