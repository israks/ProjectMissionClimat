import sqlite3
from sqlite3 import IntegrityError
import pandas

# Pointeur sur la base de données
data = sqlite3.connect("data/climat_france.db")
data.execute("PRAGMA foreign_keys = 1")

# Fonction permettant d'exécuter toutes les requêtes sql d'un fichier
# Elles doivent être séparées par un point-virgule
def updateDBfile(data:sqlite3.Connection, file):

    # Lecture du fichier et placement des requêtes dans un tableau
    createFile = open(file, 'r')
    createSql = createFile.read()
    createFile.close()
    sqlQueries = createSql.split(";")

    # Exécution de toutes les requêtes du tableau
    cursor = data.cursor()
    for query in sqlQueries:
        cursor.execute(query)

# Action en cas de clic sur le bouton de création de base de données
def createDB():
    try:
        # On exécute les requêtes du fichier de création
        updateDBfile(data, "data/createDB.sql")
    except Exception as e:
        print ("L'erreur suivante s'est produite lors de la création de la base : " + repr(e) + ".")
    else:
        data.commit()
        print("Base de données créée avec succès.")

# En cas de clic sur le bouton d'insertion de données

def insertDB():
    try:
        # '{}' : paramètre de la requête qui doit être interprété comme une chaine de caractères dans l'insert
        # {}   : paramètre de la requête qui doit être interprété comme un nombre dans l'insert
        # la liste de noms en 3e argument de read_csv_file correspond aux noms des colonnes dans le CSV
        # ATTENTION : les attributs dans la BD sont généralement différents des noms de colonnes dans le CSV
        # Exemple : date_mesure dans la BD et date_obs dans le CSV

        # On ajoute les anciennes régions
        read_csv_file(
            "data/csv/Communes.csv", ';',
            "insert into Regions values ({},'{}')",
            ['Code Région', 'Région']
        )

        # On ajoute les nouvelles régions
        read_csv_file(
            "data/csv/AnciennesNouvellesRegions.csv", ';',
            "insert into Regions values ({},'{}')",
            ['Nouveau Code', 'Nom Officiel Région Majuscule']
        )

        # On ajoute les départements référencés avec les anciennes régions
        read_csv_file(
            "data/csv/Communes.csv", ';',
            "insert into Departements (code_departement, nom_departement, code_region) values ('{}','{}', {})",
            ['Code Département', 'Département', 'Code Région']
        )

        # On renseigne la zone climatique des départements
        read_csv_file(
            "data/csv/ZonesClimatiques.csv", ';',
            "update Departements set zone_climatique = '{}' where code_departement = '{}'",
            ['zone_climatique', 'code_departement']
        )

        # On modifie les codes région des départements pour les codes des nouvelles régions
        read_csv_file(
            "data/csv/AnciennesNouvellesRegions.csv", ';',
            "update Departements set code_region = {} where code_region = {}",
            ['Nouveau Code', 'Anciens Code']
        )

        # On supprime les anciennes régions, sauf si l'ancien code et le nouveau sont identiques (pour ne pas perdre les régions qui n'ont pas changé de code)
        read_csv_file(
            "data/csv/AnciennesNouvellesRegions.csv", ';',
            "delete from Regions where code_region = {} and {} <> {}",
            ['Anciens Code', 'Anciens Code', 'Nouveau Code']
        )
        print("Les erreurs UNIQUE constraint sont normales car on insère une seule fois les Regions et les Départemments")
        print("Insertion de mesures en cours...cela peut prendre un peu de temps")
        # On ajoute les mesures
        read_csv_file(
             "data/csv/Mesures.csv", ';',
             "insert into Mesures values ('{}','{}', {}, {}, {})",
             ['code_insee_departement', 'date_obs', 'tmin', 'tmax', 'tmoy']
        )

        # On ajoute les communes
        read_csv_file(
            "data/csv/Communes.csv", ';',
            "insert into Communes values ({}, '{}', '{}', {}, {}, {}, {}, {}, '{}')",
            ['Code Commune', 'Commune', 'Statut', 'Altitude Moyenne', 'Population', 'Superficie', 'Code Canton',
             'Code Arrondissement', 'Code Département']
        )


        # On ajoute les travaux d'isolation dans les tables Travaux et Isolations
        read_csv_file_travaux(
            "data/csv/Isolation.csv", ';',
            "insert into Travaux (cout_total_ht_travaux, cout_induit_ht_travaux, date_travaux, type_logement_travaux, annee_construction_logement_travaux, code_region) values ({}, {}, '{}', '{}', '{}', {})",
            "insert into Isolations values ({}, '{}', '{}', {}, {})",
            ['cout_total_ht', 'cout_induit_ht', 'date_x', 'type_logement', 'annee_construction', 'code_region'],
            ['poste_isolation', 'isolant', 'epaisseur', 'surface']
        )

        # On ajoute les travaux de chauffage dans les tables Travaux et Chauffages
        read_csv_file_travaux(
            "data/csv/Chauffage.csv", ';',
            "insert into Travaux (cout_total_ht_travaux, cout_induit_ht_travaux, date_travaux, type_logement_travaux, annee_construction_logement_travaux, code_region) values ({}, {}, '{}', '{}', '{}', {})",
            "insert into Chauffages values ({}, '{}', '{}', '{}', '{}')",
            ['cout_total_ht', 'cout_induit_ht', 'date_x', 'type_logement', 'annee_construction', 'code_region'],
            ['energie_chauffage_avt_travaux', 'energie_chauffage_installee', 'generateur', 'type_chaudiere']
        )

        # On ajoute les travaux de panneaux photovolatiques dans les tables Travaux et Photovoltaiques
        read_csv_file_travaux(
            "data/csv/Photovoltaique.csv", ';',
            "insert into Travaux (cout_total_ht_travaux, cout_induit_ht_travaux, date_travaux, type_logement_travaux, annee_construction_logement_travaux, code_region) values ({}, {}, '{}', '{}', '{}', {})",
            "insert into Photovoltaiques values ({}, {}, '{}')",
            ['cout_total_ht', 'cout_induit_ht', 'date_x', 'type_logement', 'annee_construction', 'code_region'],
            ['puissance_installee', 'type_panneaux']
        )

    except Exception as e:
        print ("L'erreur suivante s'est produite lors de l'insertion des données : " + repr(e) + ".")
    else:
        data.commit()
        print("Un jeu de test a été inséré dans la base avec succès.")

# En cas de clic sur le bouton de suppression de la base
def deleteDB():
    try:
        updateDBfile(data, "data/deleteDB.sql")
    except Exception as e:
        print ("L'erreur suivante s'est produite lors de la destruction de la base : " + repr(e) + ".")
    else:
        data.commit()
        print("La base de données a été supprimée avec succès.")

def read_csv_file(csvFile, separator, query, columns):
    # Lecture du fichier CSV csvFile avec le séparateur separator
    # pour chaque ligne, exécution de query en la formatant avec les colonnes columns
    df = pandas.read_csv(csvFile, sep=separator)
    df = df.where(pandas.notnull(df), 'null')

    cursor = data.cursor()
    for ix, row in df.iterrows():
        try:
            tab = []
            for i in range(len(columns)):
                # pour échapper les noms avec des apostrophes, on remplace dans les chaines les ' par ''
                if isinstance(row[columns[i]], str):
                    row[columns[i]] = row[columns[i]].replace("'","''")
                tab.append(row[columns[i]])

            formatedQuery = query.format(*tab)

            # On affiche la requête pour comprendre la construction ou débugger !
            print(formatedQuery)

            cursor.execute(formatedQuery)
        except IntegrityError as err:
            print(err)


def read_csv_file_travaux(csvFile, separator, query_travaux, query_type, columns_travaux, columns_type):
    # Lecture du fichier CSV csvFile avec le séparateur separator
    # pour chaque ligne, exécution des requêtes query_travaux et query_type
    # en les formatant avec les colonnes columns_travaux et columns_type

    df = pandas.read_csv(csvFile, sep=separator)
    df = df.where(pandas.notnull(df), 'null')

    cursor = data.cursor()

    for ix, row in df.iterrows():
        try:
            tab_travaux = []
            tab_type = []

            for i in range(len(columns_travaux)):
                if isinstance(row[columns_travaux[i]], str):
                    row[columns_travaux[i]] = row[columns_travaux[i]].replace("'", "''")
                tab_travaux.append(row[columns_travaux[i]])

            # Formatage de la requête pour la table Travaux
            formatedQueryTravaux = query_travaux.format(*tab_travaux)

            print(formatedQueryTravaux)

            # Exécution de la requête pour la table Travaux
            cursor.execute(formatedQueryTravaux)

            # Récupération de l'id_travaux généré automatiquement
            id_travaux = cursor.lastrowid

            for i in range(len(columns_type)):
                if isinstance(row[columns_type[i]], str):
                    row[columns_type[i]] = row[columns_type[i]].replace("'", "''")
                tab_type.append(row[columns_type[i]])

            # Ajout de l'id_travaux à la liste pour la table du type travaux
            tab_type.insert(0, id_travaux)

            # Formatage de la requête pour la table du type travaux
            formatedQueryType = query_type.format(*tab_type)

            print(formatedQueryType)

            # Exécution de la requête pour la table Isolations
            cursor.execute(formatedQueryType)

        except IntegrityError as err:
            print(err)
