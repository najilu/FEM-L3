import gmsh
from typing import List

from point import Point
from segment import Segment
from triangle import Triangle


class Mesh:
    def __init__(self):
        """
        La classe Mesh est la représentation d'un maillage triangulaire de gmsh en liste de Point, Segment, Triangle,
        Il aurait été possible de tout gérer avec gmsh mais cela permet une meilleure modularité.
        Pour implémenter la méthode des éléments finis dans d'autres dimensions, il suffirait de créer une interface
        et de considérer les interfaces plutôt que les classes Point, Segment, Triangle.
        Le constructeur ne prend volontairement aucun paramètre afin de pouvoir remplir la mesh avec une fonction.
        """
        self.points : list = [] # représente tous les points du maillage
        self.segments : list = [] # représente tous les segments du maillage
        self.triangles : list = [] # représente tous les triangles du maillage
        self.Npts : int = 0 # représente le nombre de points dans le maillage
        self.Nseg : int = 0 # représente le nombre de segments dans le maillage
        self.Ntri : int = 0 # représente le nombre de triangles du maillage

    @staticmethod
    def get_physical_tag(dim :int, tag : int) -> int:
        """
        Cette méthode permet de savoir si un élément de dimension dim du maillage gmsh possède un tag physical
        :param dim: la dimension de l'élément considéré
        :param tag: le tag de l'élément considéré
        :return: le physical tag ou bien -1 si l'objet n'en a pas
        """
        for phys_dim, phys_tag in gmsh.model.getPhysicalGroups(): # on parcourt tous les groupes physiques
            # on récupère tous les tags des éléments de ce groupe
            entities = gmsh.model.getEntitiesForPhysicalGroup(phys_dim, phys_tag)

            # Vérifie si la dimension correspond et si notre tag est dans les tags du groupe
            if dim == phys_dim and tag in entities:
                return phys_tag
        return -1

    def GmshToMesh(self, filename:str) -> None:
        """
        Cette fonction a pour but de lire un fichier msh (c'est à dire un maillage de gmsh) pour le convertir en notre
        structure de données evoquée plus haut
        :param filename: le nom du fichier .msh
        :return: Ne retourne rien mais remplit les informations de l'objet sur lequel il est appelé
        """
        gmsh.initialize() # lance l'API gmsh
        gmsh.open(filename) # charge en mémoire le fichier demandé
        nodes = gmsh.model.mesh.getNodes() # récupère tous les points du maillage sous la forme (list, list, list)
        # la première liste contient les tags des points
        # la deuxième leurs coordonnées sous la forme [x1,y1,x2,y2...]
        # la troisième, qui ne nous intéresse pas, donne les coordonnées paramétriques.
        points = [0 for _ in range(len(nodes[0])+1)] # on initialise la liste de points afin de pouvoir les ranger en suivant l'ordre de gmsh
        for i in range(len(nodes[0])):
            p = Point(gmsh.model.mesh.getNode(nodes[0][i])[0][0], gmsh.model.mesh.getNode(nodes[0][i])[0][1], i)
            index = nodes[0][i]
            points[int(index)] = p

        d1element_infos = gmsh.model.mesh.getElements(dim=1) # on récupère tous les éléments de dimension 1 du maillage sous la forme (lit, list, list)
        #Nous ne nous intéresserons qu'à la deuxième (la première n'étant que le type d'élément considéré), qui contient le tag de chaque élément
        elements_tags = d1element_infos[1][0]
        segments = [0 for _ in range(len(elements_tags) + 1)]
        i = 0
        for tag in elements_tags: #on parcourt tous les tags
            segment_boundaries = gmsh.model.mesh.getElement(tag)[1] #la fonction getElement renvoie son type, puis les tags des sommets, on stock donc les tags des sommets
            phys_tag = Mesh.get_physical_tag(1, tag) #on récupère le tag physique pour savoir si le segment est sur le bord ou non
            segment = Segment([points[segment_boundaries[0]], points[segment_boundaries[1]]], i, phys_tag) # notre façon de stocker les points permet que l'index dans la liste soit le tag du point
            segments[int(tag)] = segment
            i+= 1

        #on fait de même pour les triangles
        d2element_infos = gmsh.model.mesh.getElements(dim=2)
        elements_tags = d2element_infos[1][0]
        triangles = []
        i = 0
        for tag in elements_tags:
            triangle_boundaries_tags = gmsh.model.mesh.getElement(tag)[1]
            phys_tag = Mesh.get_physical_tag(2, tag)
            triangle = Triangle([points[triangle_boundaries_tags[0]], points[triangle_boundaries_tags[1]],
                                 points[triangle_boundaries_tags[2]]], i, phys_tag)
            triangles.append(triangle)
            i += 1

        gmsh.finalize() #on ferme l'api gmsh
        # on remplit les différents attributs
        self.points = points[1:]  # on ne récupère pas le premier élément car il n'est pas un point, en effet tous les tags commencent à 1 donc on ne peut avoir d'élément en position 0
        self.segments = segments[1:]
        self.triangles = triangles
        self.Npts = len(self.points)
        self.Nseg = len(self.segments)
        self.Ntri = len(self.triangles)




