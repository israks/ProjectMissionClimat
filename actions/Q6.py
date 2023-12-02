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
        self.title('Q6 : graphique sur la corrélation températures minimales - coût de travaux (Isère / 2018)')
        display.defineGridDisplay(self, 1, 1)

        query = """
            SELECT strftime('%m', date_mesure) as mois, AVG(temperature_min_mesure) as moymin
            FROM Mesures
            WHERE code_departement = 38 AND strftime('%Y', date_mesure) = '2018'
            GROUP BY mois
        """

        # Extraction des données et affichage dans le tableau
        result = []
        try:
            cursor = db.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            print("Erreur : " + repr(e))

        # Extraction et préparation des valeurs à mettre sur le graphique
        tabmois_temp = []
        tabmin = []

        for row in result:
            tabmois_temp.append(row[0])
            tabmin.append(row[1])

        datetime_dates = [datetime.strptime(date, '%m') for date in tabmois_temp]

        query2 = """
            SELECT strftime('%m', date_travaux) as mois, SUM(cout_total_ht_travaux) as total_cout_travaux
            FROM Travaux JOIN Departements USING (code_region)
            WHERE strftime('%Y', date_travaux) = '2018' AND code_departement = 13 
            GROUP BY mois
        """

        # Extraction des données et affichage dans le tableau
        result2 = []
        try:
            cursor = db.data.cursor()
            result2 = cursor.execute(query2)

        except Exception as e:
            print("Erreur : " + repr(e))

        tabmois_travaux = []
        tabcouts = []

        for row in result2:
            tabmois_travaux.append(row[0])
            tabcouts.append(row[1])

        datetime_dates2 = [datetime.strptime(date, '%m') for date in tabmois_travaux]


        fig = Figure(figsize=(10, 6), dpi=100)
        plot1 = fig.add_subplot(111)

        # Plot des températures minimales moyennes
        plot1.plot(range(len(datetime_dates)), tabmin, color='red', label='Moyenne de la température minimum')

        plot1.set_xticks(range(len(datetime_dates)))
        plot1.set_xticklabels(tabmois_temp, rotation=45, ha="right")

        plot1.set_xlabel('Mois')
        plot1.set_ylabel('Moyenne de la température miniminum')

        plot1.legend()


        # Ajout de la deuxième série de données sur le même subplot
        plot2 = plot1.twinx()
        plot2.plot(range(len(datetime_dates2)), tabcouts, color='green', label='Coût total travaux')
        plot2.set_ylabel('Coût total travaux')

        plot2.legend()


        # Affichage du graphique
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

        print(tabmois_temp)
        print(tabmin)
        print(tabmois_travaux)
        print(tabcouts)
