import math

import numpy as np
from fontTools.misc.bezierTools import epsilon

import fem_utils
from point import Point
from segment import Segment

class Triangle:
    N: int
    name: str = "Triangle"

    def __init__(self, points: list[Point], id: int, physical_tag: int = -1):
        """
        La classe représente les éléments 2d du maillage triangulaire c'est-à-dire les triangles
        :param points: les sommets du triangle
        :param id: l'id est un paramètre unique permettant de trouver de quel triangle on parle.
        :param physical_tag:  c'est un paramètre utile dans gmsh qui permet de séparer les objets par groupe, on s'en
        sert ici principalement pour différencier les objets du bord (de tag 0) du reste (de tag -1).
        (Le paramètre est ici uniquement présent pour la modularité du code, si l'on voulait implémenter les
        éléments finis en 3d.)
        """
        self.points = points
        self.id = id
        self.physical_tag = physical_tag

    def get_boundary(self,i:int) -> Point:
        """
        Renvoie le i-ème sommet du triangle, orienté directement dans le sens trigonométrique grâce à gmsh
        :param i: choix du sommet
        :return: Point
        """
        return self.points[i-1]


    def area(self) -> float:
        """
        Calcul de l'aire du triangle à l'aide de la formule de Héron
        :return: floating
        """
        s1 = Segment([self.points[0], self.points[1]],-1)
        s2 = Segment([self.points[1], self.points[2]],-1)
        s3 = Segment([self.points[2], self.points[0]],-1)
        demi_par = (s1.area() + s2.area() + s3.area())/2
        return math.sqrt(demi_par* (demi_par-s1.area()) * (demi_par-s2.area()) * (demi_par-s3.area()))

    def jac(self) -> float:
        """
        Calcul du jacobien du changement de variable passant du triangle de référence au triangle considéré
        :return: float
        """
        return self.area() * 2

    def gaussPoint(self, order:int=2) -> float:
        """
        Calcul des informations nécéssaires à la quadrature de Gauss
        :param order: On demande l'ordre de précision, ici seul l'ordre 2 est implémenté car il suffit amplement
        :return: (float,float,float,float) (du type (eta,nu,omega,point de gauss)
        """
        eta = []
        nu = []
        omega =[]
        gauss_point = []
        if order == 2:
            eta = [1/6,4/6,1/6]
            nu = [1/6,1/6,4/6]
            omega = [1/6,1/6,1/6]
            for m in range(3):
                sum = 0
                for i in range(1,4):
                    x,y =self.get_boundary(i).get_coord()
                    sum += np.array([[x,y]]) * fem_utils.psi(eta[m],nu[m], i)
                gauss_point.append(sum)

        return eta, nu, omega, gauss_point







