# IMPORTATION DES MODULES

import sqlite3
import csv

#Etablissement de connexion
#Etablissement de connexion
conn = sqlite3.connect('SnifferEthernet.db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS TRAME(numero_trame INTEGER PRIMARY KEY AUTOINCREMENT,numero INTEGER,date TEXT,bench_3 TEXT,bench_5 TEXT, Taille INTEGER,Mac_Src TEXT,Mac_Dst TEXT,type TEXT,Field_2 INTEGER,Field_3 INTEGER,Field_4 INTEGER, Field_5 INTEGER,Field_6 INTEGER,Field_7 INTEGER,MAC_Sender TEXT,Source_IP TEXT,Sender_IP TEXT,Dest_IP TEXT,MAC_Target TEXT,Field_9 INTEGER,Target_IP TEXT,Field_10 INTEGER,Field_11 INTEGER,Field_14 TEXT,Field_16 TEXT,Field_17 TEXT,Field_18 TEXT,Field_20 INTEGER,Field_21 INTEGER,Field_23 TEXT,Field_25 TEXT,Field_26 TEXT,Field_28 TEXT,Field_29 TEXT,Field_30 INTEGER,Field_32 TEXT,Field_33_34_35 TEXT,Packet TEXT,PMID TEXT)")

# Récupération du numéro maximum actuel
cur.execute("SELECT MAX(numero) FROM TRAME")
result = cur.fetchone()
max_numero = result[0] if result[0] else 0  # Si la valeur est nulle, on utilise 0 comme valeur de départ
max_numero += 1  # Incrémentation du numéro une seule fois


#cur.execute("DELETE FROM TRAME") # supprime tout de la table REPERTOIRE

# Ouvrir le fichier CSV et lire les données
with open('ethernet.result_data.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Ignorer la première ligne (en-tête)
    for row in csvreader:
        # Insérer les données dans la table
        cur.execute('INSERT INTO TRAME(numero_trame, numero, date, bench_3, bench_5,Taille,Mac_Src,Mac_Dst,type,Field_2,Field_3,Field_4,Field_5,Field_6,Field_7,MAC_Sender,Source_IP,Sender_IP,Dest_IP,MAC_Target,Field_9,Target_IP,Field_10,Field_11,Field_14,Field_16,Field_17,Field_18,Field_20,Field_21,Field_23,Field_25,Field_26,Field_28,Field_29,Field_30,Field_32,Field_33_34_35,Packet,PMID) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',(max_numero,row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33],row[34],row[35],row[36],row[37]))

# Commit des modifications et fermeture de la connexion à la base de données
conn.commit()
conn.close()

#cur.execute("DELETE FROM TRAME;") # supprime tout de la table REPERTOIRE