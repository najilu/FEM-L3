class Point:

    N : int
    name : str = "Point"

    def __init__(self, x:float, y:float, id:int):
        """
        La classe point représente les points du maillage 2D
        :param x: la coordonnée en abscisse du point considéré
        :param y:  la coordonnée en ordonnée du point considéré
        :param id: l'id est un paramètre unique permettant de trouver de quel point on parle, il sert surtout pour
        le calcul matriciel.
        """
        self.x : float = x
        self.y : float = y
        self.id : int = id

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def get_coord(self) -> tuple:
        """
        Permet d'obtenir les coordonnées d'un point
        :return: un tuple (int,int)
        """
        return self.x, self.y

    def get_id(self) -> int:
        """
        Permet d'obtenir l'identifiant du point
        :return: un nombre entier supérieur strict à 0.
        """
        return self.id

    def __eq__(self, other) -> bool:
        """
        C'est un override de la fonction equal, cela permet de donner un sens a Point1 = Point2
        :param other: l'autre point avec lequel on veut comparer
        :return: un boolean
        """
        if not isinstance(other, Point): #test si le paramètre other n'est pas un point pour que la suite est un sens
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        """
        C'est aussi un override, ici par convention il est obligatoire de modifier le hash si equal est modifié, en effet
        le hash est un identifiant unique à un objet obtenue à partir de paramètre, il faut donc qu'il dépende des mêmes
        paramètre que equal car il est déterministe, deux objet avec mêmes hash sont normalement égaux, cette comparaison
        est par exemple utilisé dans les sets.
        :return:
        """
        return hash(self.id) # fonction intégré en python pour calculer le hash