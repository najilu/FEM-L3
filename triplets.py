class Triplets:
    def __init__(self):
        """
        Le but de cette classe est de créer une structure de données pouvant être modifiée à la volée et contenir des doublons
        afin d'ensuite obtenir une matrice COO et CSR.
        """
        self.data : tuple = ([], ([],[])) # on crée la structure de données qui représente les coefficients non nuls d'une matrice
    def __str__(self):
        return str(self.data)
    def append(self, i:int, j:int, val:float) -> None:
        """

        :param i: la ligne du coefficient non nul
        :param j: la colonne du coefficient non nul
        :param val: la valeur de coefficient
        :return: None
        """
        self.data[1][0].append(i)
        self.data[1][1].append(j)
        self.data[0].append(val)

    def getData(self):
        """
        Permet de récupérer la structure de données.
        :return: tupple(List, tupple(list, List))
        """
        return self.data