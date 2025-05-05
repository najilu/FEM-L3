from typing import Callable

import numpy as np
from point import Point

def get_shape_functions(triangle_principale, i) -> Callable[[float, float], float]:
    """
    Cette fonction calcul la i*ème fonction de forme du triangle considéré
    :param triangle: le triangle dont on veut considéré les fonctions de forme
    :param i: le numéro du sommet sur lequel la fonction de forme doit valoir 1
    :return: la fonction de forme conrrespondante.
    """
    coords = np.array([p.get_coord() for p in triangle_principale.points])  # on récupère les coordonnées des points
    A = np.hstack((coords, np.ones((3, 1))))  # on initialise une matrice 3x3 de la forrme (coordonnées + 1)
    rhs = np.zeros(3) # on initialise le second membre à 0
    rhs[i-1] = 1  # on place à 1 dans le vecteur à la ligne pour laquelle la fonction doit être non nul
    phi_coeffs = np.linalg.solve(A, rhs)  # Résout le système pour obtenir les coefficients de phi
    def phi_function(x:float,y:float) -> float:
        """
        Fonction de forme qui vaut 1 sur les triangles qui vaut 1 sur le sommet i et 0 sur tout les autres sommets
        :param x: float
        :param y: float
        :return: float
        """
        p = Point(x,y,1) #on transforme les coordonées en un point pour vérifier si il appartient à un triangle dont un des sommets est le sommets i
        # si c'est le cas alors la fonction vaut une valeur non nul, sinon elle vaut 0
        if is_point_in_triangle(p, triangle_principale): # a refaire on check pas assez de triangle
            return  phi_coeffs[0] * x + phi_coeffs[1] * y + phi_coeffs[2]
        else:
            return 0
    return phi_function


def grad_phi(i:int) -> np.array:
    """
    Calcul du gradient des fonctions de forme sur le triangle de référence
    :param i: un entier qui est compris entre 0 et 2, il correspond à qu'elle fonctions de forme de référence l'on choisie
    :return: le vecteur gradient
    """
    match i :
        case 0:
            return np.array([[-1], [-1]])
        case 1:
            return np.array([[1], [0]])
        case 2:
            return np.array([[0], [1]])

def psi(eta:float, nu:float, i:int) -> float:
    """
    Calcul de la i-ème fonction de référence en fonction des coordonnées paramétriques
    :param eta: première coordonnée paramétrique
    :param nu:  seconde coordonnée paramétrique
    :param i: int qui permet de choisir parmi les trois fonctions de forme de référence
    :return: float
    """
    match i :
        case 1:
            return 1-eta-nu
        case 2:
            return eta
        case 3:
            return nu

def phi_ref(triangle, eta:float, nu:float, i:int, mesh) -> float:
    """
    Calcul d'une fonction de forme sur un triangle avec les coordonnées d'un point dans le triangle de référence,
    on utilise le changement de variable dont on a parlé dans le polycopié
    :param triangle: triangle qui contient un des sommets de la fonctions de forme considéré
    :param eta: première coordonnées paramétrique
    :param nu: seconde coordonnées paramétrique
    :param i: int qui perrmet de choisir le sommet
    :return: float
    """
    x1,y1 = triangle.get_boundary(1).get_coord()
    x2,y2 = triangle.get_boundary(2).get_coord()
    x3,y3 = triangle.get_boundary(3).get_coord()

    vec = psi(eta, nu, 1) * np.array([[x1,y1]]) + psi(eta, nu, 2) * np.array([[x2,y2]]) + psi(eta, nu, 3) * np.array([[x3,y3]])
    x,y = vec[0][0], vec[0][1]
    match i:
        case 1: return get_shape_functions(triangle, 1)(x,y)
        case 2: return get_shape_functions(triangle, 2)(x,y)
        case 3: return get_shape_functions(triangle, 3)(x,y)

def sign(p1 : Point, p2 : Point, p3 : Point) -> float:
    """
    Calcul pour savoir dans qu'elle demi-plan formé par les deux derniers points, le premier point donné est.
    :param p1:
    :param p2:
    :param p3:
    :return: float
    """
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - \
           (p2[1] - p1[1]) * (p3[0] - p1[0])

def is_point_in_triangle(point : Point, triangle, epsilon=0.01) -> bool:
    """
    Vérifie si un point est dans le triangle ou non, epsilon est la précision demandé (il sert pour éviter qu'un point sur un somemt ne soit pas compté dedans)
    :param point: le point dont on test l'appartenance
    :param triangle: le triangle dont on cherhce à savoir si le point appartient ou non
    :param epsilon: précision
    :return: bool
    """
    P = point.get_coord()
    A = triangle.get_boundary(1).get_coord()
    B = triangle.get_boundary(2).get_coord()
    C = triangle.get_boundary(3).get_coord()
    d1 = sign(P, A, B)
    d2 = sign(P, B, C)
    d3 = sign(P, C, A)

    has_neg = (d1 < -epsilon) or (d2 < -epsilon) or (d3 < -epsilon)
    has_pos = (d1 > epsilon) or (d2 > epsilon) or (d3 > epsilon)

    # Si le point n'est pas dans l'intersection des demi espaces alors il est en dehors du triangle
    if has_neg and has_pos:
        return False
    elif abs(d1) <= epsilon or abs(d2) <= epsilon or abs(d3) <= epsilon:
        return True



