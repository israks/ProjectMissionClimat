import tkinter as tk
from utils import display
from utils import db
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(1000, 600, self)
        self.title('Q6 : graphique sur la corrélation températures minimales - coût de travaux (Isère / 2022)')
        display.defineGridDisplay(self, 1, 1)

        query = """
            SELECT strftime('%m', Mesures.date_mesure) as mois, ROUND(AVG(temperature_min_mesure), 2) as moy_min, SUM(cout_total_ht_travaux) AS tot_couts
            FROM Mesures JOIN Departements USING (code_departement) JOIN Travaux USING (code_region)
            GROUP BY mois
            HAVING nom_departement = 'ISERE' AND strftime('%Y', Meusres.date_mesure) = 2022
        """

        # Extraction des données et affichage dans le tableau
        result = []
        try:
            cursor = db.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            print("Erreur : " + repr(e))

        # Extraction et préparation des valeurs à mettre sur le graphique
        tabmois = []
        tabmin = []
        tabcouts = []


        for row in result:
            tabmin.append(row[1])
            tabmois.append(row[0])
            tabcouts.append(row[2])

        # Formatage des dates pour l'affichage sur l'axe x
        datetime_dates = [datetime.strptime(date, '%m') for date in tabmois]

        # Ajout de la figure et du subplot qui contiendront le graphique
        fig = Figure(figsize=(10, 6), dpi=100)
        plot1 = fig.add_subplot(111)

        # Affichage des courbes
        plot1.plot(range(len(datetime_dates)), tabmin, color='b', label='moy des temp. min')
        plot1.plot(range(len(datetime_dates)), tabcouts, color='r', label='total des couts')

        # Configuration de l'axe x pour n'afficher que le numéro du mois
        xticks = [i for i, date in enumerate(datetime_dates) if date.day == 1]
        xticklabels = [date.strftime('%m') for date in datetime_dates if date.day == 1]
        plot1.set_xticks(xticks)
        plot1.set_xticklabels(xticklabels, rotation=45)
        plot1.legend()

        # Affichage du graphique
        canvas = FigureCanvasTkAgg(fig,  master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
