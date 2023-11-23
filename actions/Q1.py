import tkinter as tk
from utils import display
from tkinter import ttk

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(600, 400, self)
        self.title('Q1 : départements de la région Auvergne-Rhône-Alpes')
        display.defineGridDisplay(self, 2, 1)
        
        ttk.Label(self, text="Modifier cette fonction en s'inspirant du code de F1, pour qu'elle affiche la liste des départements (code_departement, nom_departement) de la région Auvergne-Rhône-Alpes",
                  wraplength=500, anchor="center", font=('Helvetica', '10', 'bold')).grid(sticky="we", row=0)


        columns = ('code_departement', 'nom_departement')
        query = """SELECT code_departement, nom_departement
                    FROM Departements JOIN Regions USING (code_region)
                    WHERE nom_region = 'AUVERGNE RHONE ALPES'
                """

        tree = display.createTreeViewDisplayQuery(self, columns, query,200)
        tree.grid(row=0, sticky="nswe")

