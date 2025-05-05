import numpy as np
from point import Point


class Segment:
    N : int
    name : str = "Segment"
    def __init__(self, points : list[Point], id : int, physical_tag : int=-1):
        """
        La classe représente les éléments 1d du maillage triangulaire c'est à dire les segments
        :param points: ce sont les deux extrémités du segment
        :param id: l'id est un paramètre unique permettant de trouver de quel segment on parle
        :param physical_tag: c'est un paramètre utile dans gmsh qui permet de séparer les objets par groupe, on s'en
        sert ici principalement pour différencier les objets du bord (de tag 0) du reste (de tag -1).
        """
        self.p : list[Point] = points
        self.id : int = id
        self.physical_tag : int = physical_tag

    def area(self) -> np.floating:
        """
        Calcul de l'aire du rectangle (c'est-à-dire sa longueur)
        :return: float
        """
        return  np.linalg.norm(np.array(self.p[0].get_coord()) - np.array(self.p[1].get_coord()))

    def jac(self) -> np.floating:
        """
        Calcul du jacobien du changement de variable qui envoie le segment de référence dans un segment particulier
        (Ne sert pas ici car on considère un maillage 2d mais la fonction est là dans le cas où l'on vodurait implémenter
        les éléments finis en une dimension)
        :return: float
        """
        return self.area()

    def get_boundary(self, i:int):
        """
        Retourne le premier ou le deuxième sommet, ils sont déjà orientés dans le sens trigo grâce à gmsh.
        :param i: permet de choisir le sommet voulu
        :return: Point
        """
        return self.p[i-1]