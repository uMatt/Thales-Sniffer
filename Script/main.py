'''
Pour lancer le code ./main.py "localisation du chemin relatif du ficBinaire" --"Fichier REP" --"Nom Du test"

Exemple :
    python Script\main.py Script\ethernet.result_data --fichier_REP Script\Vt_DEMO_power_on.rep --nom TEST2

    python Script\main.py Script\ethernet.result_data --fichier_REP Script\Vt_DEMO_power_on.rep

    python Script\main.py Script\ethernet.result_data --nom TEST
'''

# IMPORTATION DES MODULES

import csv
import datetime
import struct
import time
import argparse
import sys
import json
import sqlite3
import csv
import re
import mysql.connector

#CALCUL TEMPS DU PROGRAMME
start = time.time()

'''
Fonction pour recuperer les informations du fichier_rep
    - Besoin du chemin on se situe le fichier rep
    - Les prefix qu'on a besoin pour lancer la recherche
'''


prefix = [r'\* Test                                :',r'\* Execution begin date                :'] # Les informations a recuperer 
def recuperation_fichier_rep(chemin, prefix):
    ligne_recontre = []
    with open(chemin, 'r') as fichier:
        for ligne in fichier:
            for i in range(len(prefix)):
                if re.search(prefix[i], ligne):
                    ligne_recontre.append(ligne.rstrip('\n'))
    ligne_recontre[0] = ligne_recontre[0].split(":")[1].strip()
    ligne_recontre[0] = ligne_recontre[0].split('"')[1].strip()
    ligne_recontre[1] = ligne_recontre[1].split(":")[1].strip()
    return ligne_recontre


'''
Parser va permettre de lancer le programme avec differentes options
    - ficBinaire
    - ficNom
    - ficRep
'''

# Ajout des parametres 
parser = argparse.ArgumentParser(description='Description de votre programme.')
parser.add_argument('fichier_binaire', help='Chemin vers le fichier binaire (obligatoire)')
parser.add_argument('--fichier_REP', help='Chemin vers le fichier REP (optionnel)')
parser.add_argument('--nom', help='Nom du fichier (optionnel)')

args = parser.parse_args()

# Voir si le fichier binaire est bien present
fichier_binaire = args.fichier_binaire

# Voir si le fichier REP est specifie
if args.fichier_REP:
    fichier_REP = args.fichier_REP
    date_actuelle, nom = recuperation_fichier_rep(fichier_REP,prefix)
    # Vérifier si le nom du fichier est également spécifié
    if args.nom:
        nom = args.nom
else:
    # Si le fichier REP n'est pas spécifié, le nom de fichier est obligatoire
    if args.nom:
        nom = args.nom
        # Récupérer la date et l'heure actuelles
        maintenant = datetime.datetime.now()
        date_actuelle = maintenant.strftime("%Y-%m-%d %H:%M")
    else:
        exit(1)


'''
Pour pouvoir recuperer toute les informations sur les fonctions depuis le fichier JSON
'''

chemin_json = "Script/fonctions_transfert.json" # Chemin du JSON

with open(chemin_json, 'r') as json_file: # Ouverture du fichier JSON
    informations = json.load(json_file)

# Accéder au tableau tableau_ft0
tableau_ft0 = informations['tableau_ft0']
tableau_ft1 = informations['tableau_ft1']
tableau_ft2 = informations['tableau_ft2']
tableau_ft3 = informations['tableau_ft3']
tableau_ft4 = informations['tableau_ft4']
tableau_ft5 = informations['tableau_ft5']
tableau_ft6 = informations['tableau_ft6']
tableau_ft7 = informations['tableau_ft7']
tableau_ip = informations['tableau_ip']
tableau_mac = informations['tableau_mac']

'''
Fonction pour le script:
    - binaire_from_bytes ( Un text encoded )
    - seconds_to_date ( Un nombre de seconde )
    - seconds_to_date2 ( Un nombre de seconde ) differente de l'autre fonction car date de depart differente
'''

# FONCTION POUR RECUPERER LES BITS

def binaire_from_bytes(texte_encoded): 
    '''traduit bits en octets'''
    texte_bits = ''.join(format(byte, '08b') for byte in texte_encoded)  # Conversion en bits
    return texte_bits

# FONCTION DATE POUR TROUVER LA DATE

def seconds_to_date(seconds): 
    '''temps en seconde et traduit en fonction de la norme IEEE754 en date ''' 
    reference_date = datetime.datetime(1970, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)

    # Ajoute le nombre de secondes à la date de référence pour obtenir la date correspondante
    date = reference_date + datetime.timedelta(seconds=seconds)

    # Formate la date et l'heure dans une chaîne de caractères
    formatted_date = date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]#manque temps virgule

    return formatted_date


def seconds_to_date2(seconds):
    # Définit la date de référence (1 JANVIER 2000 à 12:00:00 UTC)
    reference_date = datetime.datetime(2000, 1, 1, 12, 0, 0, 0, datetime.timezone.utc)

    # Ajoute le nombre de secondes à la date de référence pour obtenir la date correspondante
    date = reference_date + datetime.timedelta(seconds=seconds)

    # Formate la date et l'heure dans une chaîne de caractères
    formatted_date = date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    return formatted_date

# J'ai modifie les valeur des trois prermiers case du tableau car elle etait en maj et que les valeurs de la trame non
# Rajout d'une Ligne dans le tableau car dans le excel il y a une valeur TBD


'''
Fonction de Transert :
    - transfert_mac
    - transfert_ip
    - transfert_ft7
    - transfert_ft6
    - transfert_ft5
    - transfert_ft4
    - transfert_ft3
    - transfert_ft2
    - transfert_ft1
    - transfert_ft0
'''

# FONCTION DE TRASNFERT POUR ADRESSE MAC

def transfert_mac(valeur_brute):
    if valeur_brute in tableau_mac:
        return tableau_mac[valeur_brute]
    else:
        return None


# FONCTION TRANSFERT IP 

def transfert_ip(valeur_brute):
    valeur_brute = valeur_brute.upper()
    if valeur_brute in tableau_ip:
        return tableau_ip[valeur_brute]
    else:
        return None

# FONCTION TRANSFERT FT_7 POUR LABEL ( FIELD_14 )

def transfert_ft7(valeur_brute):
    valeur_brute = valeur_brute[3]
    if valeur_brute in tableau_ft7:
        return tableau_ft7[valeur_brute]
    else:
        return None
    
# FONCTION DE TRANSFERT FT_6

def transfert_ft6(valeur_brute):#rajouter parenthese tableau
    if valeur_brute in tableau_ft6:
        return tableau_ft6[valeur_brute]
    else :
        return

# FONCTION DE TRANSFERT FT_5 POUR LABEL ( FIELD_17 )

def transfert_ft5(valeur_brute):
    valeur_brute = valeur_brute[8:11]
    valeur_brute_v2 = int(valeur_brute,2)
    valeur_brute_v2 = str(valeur_brute_v2)
    if valeur_brute_v2 in tableau_ft5:
        return tableau_ft5[valeur_brute_v2]
    else:
        return None
    
# FOnction TRANSFERT FT_4 POUR LABEL ( Field_29 )

def transfert_ft4(valeur_brute):
    if valeur_brute in tableau_ft4:
        return tableau_ft4[valeur_brute]
    else:
        return None

# FONCTION TRANSFERT FT_3 POUR LABEL ( FIELD_28 )

def transfert_ft3(valeur_brute):
    if valeur_brute in tableau_ft3:
        return tableau_ft3[valeur_brute]
    else:
        return None

# FONCTION DE TRANSFERT FT_2 POUR LABEL ( Field_18 )

def transfert_ft2(valeur_brute):
    valeur_brute = valeur_brute[11:16]
    valeur_brute_v2 = int(valeur_brute,2)
    valeur_brute_v2 = str(valeur_brute_v2)
    if valeur_brute_v2 in tableau_ft2:
        return tableau_ft2[valeur_brute_v2]
    else:
        return None


# FONCTION DE TRANSFERT FT_1 POUR LABEL ( Field_32 )

def transfert_ft1(valeur_brute):
    if valeur_brute in tableau_ft1:
        return tableau_ft1[valeur_brute]
    else:
        return None
    
# FONCTION DE TRANSFERT FT_0 POUR LABEL ( BENCH_5 )

def transfert_ft0(valeur_brute):
    if valeur_brute in tableau_ft0:
        return tableau_ft0[valeur_brute]
    else:
        return None

    

'''
Debut du programme principale
'''


with open(fichier_binaire, "rb") as f:
    # ouverture du fichier CSV en mode écriture
    with open("Result\ethernet.result_data.csv", mode='w', newline='') as csv_file:
        # déclaration des colonnes 
        fieldnames = ['Date', 'Bench 3', 'Bench 5', 'Taille de la trame','Mac_Src','Mac_Dst','Type','Field_2','Field_3','Field_4','Field_5','Field_6','Field_7','MAC_Sender','Source_IP','Sender_IP','Dest_IP','MAC_Target','Field_9','Target_IP','Field_10','Field_11','Field_14','Field_16','Field_17','Field_18','Field_20','Field_21','Field_23','Field_25','Field_26','Field_28','Field_29','Field_30','Field_32','Field_33_34_35','Time Packet (cal)','PMID']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # écriture de l'en-tête
        writer.writeheader()

        # initialisation du compteur de trames
        trame_count = 1
        while True:
            # ignorer les 8 premiers octets
            f.read(8)

            # lecture de la date en hexadécimal
            date_bytes = f.read(8)
            if not date_bytes:
                break  # fin du fichier
            date = date_bytes.hex()
            date2 = struct.unpack("<d", struct.pack("Q",int("0x"+date, 16)))[0]
            date2 = seconds_to_date(date2)
            # lecture de Bench 3 en hexadécimal
            bench3_bytes = f.read(4)
            bench3 = int.from_bytes(bench3_bytes, byteorder='big')

            # lecture de Bench 4, 5, 6 en hexadécimal
            bench456_bytes = f.read(4)
            #bench456 = bench456_bytes.hex()
            field_5 = binaire_from_bytes(bench456_bytes)
            field_5 =field_5[12:16]
            field_5 = int(field_5,2)
            field_5 = str(field_5)
            field_5_transfert = transfert_ft0(field_5)

            # lecture de la taille de trame en décimal
            size_bytes = f.read(4)
            size = int.from_bytes(size_bytes, byteorder='big')

            # ADDRESSE MAC SRC
            mac_src_bytes = f.read(6)
            mac_src = mac_src_bytes.hex()
            mac_src_transfert = transfert_mac(mac_src)

            # ADDRESSE MAC DST
            mac_dst_bytes = f.read(6)
            mac_dst = mac_dst_bytes.hex()
            mac_dst_transfert = transfert_mac(mac_dst)

            # TYPE TRAME UDP/ARP

            # Modification au niveau du write en bas pour afficher 800 et non 0800

            type_bytes = f.read(2)
            type = type_bytes.hex()

            if type == '0800':
                # FIELD_2
                field_2_bytes = f.read(2)
                field_2 = int.from_bytes(field_2_bytes, byteorder='big')
                # FIELD_3
                field_3_bytes = f.read(2)
                field_3 = int.from_bytes(field_3_bytes, byteorder='big')
                # FIELD_4
                field_4_bytes = f.read(2)
                field_4 = int.from_bytes(field_4_bytes, byteorder='big')
                # FIELD_5
                field_5_bytes = f.read(2)
                field_5 = int.from_bytes(field_5_bytes, byteorder='big')
                # FIELD_6
                field_6_bytes = f.read(1)
                field_6 = int.from_bytes(field_6_bytes, byteorder='big')
                # FIELD_7
                field_7_bytes = f.read(1)
                field_7 = int.from_bytes(field_7_bytes, byteorder='big')

                # SKIP FIELD_8
                f.read(2)

                # source_ip
                source_ip_bytes = f.read(4)
                source_ip = source_ip_bytes.hex()
                source_ip_transfert = transfert_ip(source_ip)
                # dest_ip
                dest_ip_bytes = f.read(4)
                dest_ip = dest_ip_bytes.hex()
                dest_ip_transfert = transfert_ip(dest_ip)
                # FIELD_9
                field_9_bytes = f.read(2)
                field_9 = int.from_bytes(field_9_bytes, byteorder='big')
                # FIELD_10
                field_10_bytes = f.read(2)
                field_10 = int.from_bytes(field_10_bytes, byteorder='big')
                # FIELD_11 VALIDATION DES TRANSFERTS
                field_11_bytes = f.read(2)
                field_11 = int.from_bytes(field_11_bytes, byteorder='big')
                # SKIP FIELD_12
                f.read(2)
                # Field_13,14,15,16,17,18
                field_1345678_bytes = f.read(2)
                field_1345678 = field_1345678_bytes.hex()

                # FIELD_14 FONCTION TRANSERT FT7
                field_14 = binaire_from_bytes(field_1345678_bytes)
                field_14 = field_14[3]
                field_14_transfert = transfert_ft7(binaire_from_bytes(field_1345678_bytes))

                # FIEL_16 FONCTION TRANSFERT FT7

                field_16 = binaire_from_bytes(field_1345678_bytes)
                field_16 = field_16[5:8]

                # FIELD_17 FONCTION DE TRANSFERT FT5
                field_17 = transfert_ft5(binaire_from_bytes(field_1345678_bytes))

                #FIELD_18 FONCTION TRANFERST FT2
                field_18 = transfert_ft2(binaire_from_bytes(field_1345678_bytes))
                field18 = binaire_from_bytes(field_1345678_bytes)
                field18 = field18[11:16]
                # Field_19,20
                field_1920_bytes = f.read(2)
                field_1920 = field_1920_bytes.hex()

                #FIELD_20 FONCTION
                field_20 = bin(int(field_1920, 16))[2:]
                field_20 = field_20[2:16]
                field_20 = int(field_20,2)

                # Field_21
                field_21_bytes = f.read(2)
                field_21 = int.from_bytes(field_21_bytes, byteorder='big')


                # Field_22,23,24,25,26
                field_2223242526_bytes = f.read(1)
                #field_2223242526 = field_2223242526_bytes.hex()

                # Field 23

                field_23 = binaire_from_bytes(field_2223242526_bytes)
                field_23 = field_23[4]
                # Field 25
                field_25 = binaire_from_bytes(field_2223242526_bytes)
                field_25 = field_25[6]

                # Field 26
                field_26 = binaire_from_bytes(field_2223242526_bytes)
                field_26 = field_26[7]


                # Field_27,28
                field_2728_bytes = f.read(1)
                #field_2728 = field_2728_bytes.hex()

                # FIELD 28
                field_28 = binaire_from_bytes(field_2728_bytes)
                field28 = field_28[2:8]
                field_28 = field_28[2:8]
                field_28 = int(field_28,2)
                field_28 = hex(field_28)[2:]
                field_28_transfert = transfert_ft3(field_28)

                # Field_29,30
                field_2930_bytes = f.read(2)
                field2930 = binaire_from_bytes(field_2930_bytes)
                field_2930 = field_2930_bytes.hex()

                # FIELD 29
                field_29 = binaire_from_bytes(field_2930_bytes)
                field_29 = field_29[:6]
                field_29 = int(field_29,2)
                field_29 = hex(field_29)[2:]
                field_29_transfert = transfert_ft4(field_29)

                # FIELD 30

                field_30 = binaire_from_bytes(field_2930_bytes)
                field_30 = field_30[6:]
                field_30 = int(field_30,2)
                
                # SKIP FIELD_31
                f.read(1)

                # Field_32
                field_32_bytes = f.read(1)
                #field_32 = field_32_bytes.hex()
                field_32 = binaire_from_bytes(field_32_bytes)
                field_32 = int(field_32,2)
                field_32 = str(field_32)
                field_32_transfert = transfert_ft1(field_32)

                # Field_33
                field_33_bytes = f.read(2)
                field_33 = field_33_bytes.hex()

                # Field_34
                field_34_bytes = f.read(2)
                field_34 = field_34_bytes.hex()

                # Field_35
                field_35_bytes = f.read(2)
                field_35 = field_35_bytes.hex()

                # Field 33_34_35

                field_33_34_35 = field_33 + field_34
                field_33_34_35 = int(field_33_34_35, 16)
                field_33_34_35 = field_33_34_35 + (int(field_35,16)/65536)

                time_packet = seconds_to_date2(field_33_34_35)

    ############################>>>>>>>>>PMID<<<<<<<<<<<<<<###################################

                pmid=str(field_14)+str(field18)+str(field28)+str(field2930)
                pmid = int(pmid,2)
                pmid = hex(pmid)
                pmid = pmid.split('0x')
                pmid = pmid[1]
                mid = transfert_ft6(pmid.upper())
                #print(pmid+str(mid))
                writer.writerow({'Date': date2, 'Bench 3': bench3, 'Bench 5': field_5_transfert, 'Taille de la trame': size, 'Mac_Src': mac_src_transfert, 'Mac_Dst': mac_dst_transfert, 'Type':type[1:4],'Field_2':field_2,'Field_3':field_3,'Field_4':field_4,'Field_5':field_5,'Field_6':field_6,'Field_7':field_7,'Source_IP':source_ip_transfert,'Dest_IP':dest_ip_transfert,'Field_9':field_9,'Field_10':field_10,'Field_11':field_11,'Field_14': field_14_transfert,'Field_16':field_16,'Field_17':field_17,'Field_18':field_18,'Field_20':field_20,'Field_21':field_21,'Field_23':field_23,'Field_25':field_25,'Field_26':field_26,'Field_28':field_28_transfert,'Field_29':field_29_transfert,'Field_30':field_30,'Field_32':field_32_transfert,'Field_33_34_35':field_33_34_35,'Time Packet (cal)':time_packet, 'PMID':pmid+str(mid)})
                # aller à la trame suivante
                f.seek((size-6-6-2-2-2-2-2-1-1-4-2-4-2-2-2-2-2-2-2-1-1-2-1-1-2-2-2), 1)
                # incrémentation du compteur de trames
                trame_count += 1
            elif type == '0806':
                field_2_bytes = f.read(2)
                field_2 = int.from_bytes(field_2_bytes, byteorder='big')
                # FIELD_3
                field_3_bytes = f.read(2)
                field_3 = int.from_bytes(field_3_bytes, byteorder='big')
                # FIELD_4
                field_4_bytes = f.read(1)
                field_4 = int.from_bytes(field_4_bytes, byteorder='big')
                # FIELD_5
                field_5_bytes = f.read(1)
                field_5 = int.from_bytes(field_5_bytes, byteorder='big')
                # FIELD_6
                field_6_bytes = f.read(2)
                field_6 = field_6_bytes.hex()
                # MAC Sender
                mac_sender_bytes = f.read(6)
                mac_sender = mac_sender_bytes.hex()
                mac_sender_transfert = transfert_mac(mac_sender)
                # Sender IP
                sender_ip_bytes = f.read(4)
                sender_ip = sender_ip_bytes.hex()
                sender_ip_transfert = transfert_ip(sender_ip)
                # MAC TARGET
                mac_target_bytes = f.read(6)
                mac_target = mac_target_bytes.hex()
                mac_target_tranfert = transfert_mac(mac_target)
                # TARGET IP
                target_ip_bytes = f.read(4)
                target_ip = target_ip_bytes.hex()
                target_ip_tranfert = transfert_ip(target_ip)
                writer.writerow({'Date': date2, 'Bench 3': bench3, 'Bench 5': field_5_transfert, 'Taille de la trame': size, 'Mac_Src': mac_src_transfert, 'Mac_Dst': mac_dst_transfert, 'Type':type[1:4],'Field_2':field_2,'Field_3':field_3,'Field_4':field_4,'Field_5':field_5,'Field_6':field_6,'MAC_Sender':mac_sender_transfert,'Sender_IP':sender_ip_transfert,'MAC_Target':mac_target_tranfert,'Target_IP':target_ip_tranfert})
                # aller à la trame suivante
                f.seek((size-6-6-2-2-2-1-1-2-6-4-6-4), 1)
                # incrémentation du compteur de trames
                trame_count += 1



# SQL

# Connection MY SQL
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'DBThales',
    'raise_on_warnings': True
}

conn = mysql.connector.connect(**config)
cur = conn.cursor()

#VOIR SI TABLE EXISTE
cur.execute("SHOW TABLES LIKE 'TRAME'")
result = cur.fetchone()

if result is None:
    cur.execute("CREATE TABLE TRAME(numero INTEGER PRIMARY KEY AUTO_INCREMENT, numero_trame INTEGER, date TEXT, PMID TEXT, bench_3 TEXT, bench_5 TEXT, Taille INTEGER,Mac_Src TEXT,Mac_Dst TEXT,type TEXT,Field_2 INTEGER,Field_3 INTEGER,Field_4 INTEGER,Field_5 INTEGER,Field_6 INTEGER,Field_7 TEXT,MAC_Sender TEXT,Source_IP TEXT,Sender_IP TEXT,Dest_IP TEXT,MAC_Target TEXT,Field_9 TEXT,Target_IP TEXT,Field_10 TEXT,Field_11 TEXT,Field_14 TEXT,Field_16 TEXT,Field_17 TEXT,Field_18 TEXT,Field_20 TEXT,Field_21 TEXT,Field_23 TEXT,Field_25 TEXT,Field_26 TEXT,Field_28 TEXT,Field_29 TEXT,Field_30 TEXT,Field_32 TEXT,Field_33_34_35 TEXT,Packet TEXT)")


#VOIR SI TABLE EXISTE
cur.execute("SHOW TABLES LIKE 'INFO'")
result = cur.fetchone()

if result is None:
    cur.execute("CREATE TABLE INFO(trame INTEGER,nom TEXT,date TEXT)")




# Récupération du numéro maximum actuel
cur.execute("SELECT MAX(numero_trame) FROM TRAME")
result = cur.fetchone()
max_numero = result[0] if result[0] else 0  # Si la valeur est nulle, on utilise 0 comme valeur de départ
max_numero += 1
#cur.execute("DELETE FROM TRAME") # supprime tout de la table REPERTOIRE


#AJOUT DES VALEURS
cur.execute("INSERT INTO INFO(trame, nom, date) VALUES (%s, %s, %s)", (max_numero, nom, date_actuelle))

# Ouvrir le fichier CSV et lire les données
with open('Result\ethernet.result_data.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Ignorer la première ligne (en-tête)
    for row in csvreader:
        # Insérer les données dans la table
        cur.execute('INSERT INTO TRAME(numero_trame, date, bench_3, bench_5, Taille,Mac_Src,Mac_Dst,type,Field_2,Field_3,Field_4,Field_5,Field_6,Field_7,MAC_Sender,Source_IP,Sender_IP,Dest_IP,MAC_Target,Field_9,Target_IP,Field_10,Field_11,Field_14,Field_16,Field_17,Field_18,Field_20,Field_21,Field_23,Field_25,Field_26,Field_28,Field_29,Field_30,Field_32,Field_33_34_35,Packet,PMID) VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (max_numero, row[0], row[1], row[2], row[3], row[4], row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33],row[34],row[35],row[36],row[37]))
        #cur.execute('INSERT INTO TRAME(numero_trame, date, bench_3, bench_5, Taille,Mac_Src,Mac_Dst,type,Field_2,Field_3,Field_4,Field_5,Field_6,Field_7,MAC_Sender,Source_IP,Sender_IP,Dest_IP,MAC_Target,Field_9,Target_IP,Field_10,Field_11,Field_14,Field_16,Field_17,Field_18,Field_20,Field_21,Field_23,Field_25,Field_26,Field_28,Field_29,Field_30,Field_32,Field_33_34_35,Packet) VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (max_numero, row[0], row[1], row[2], row[3], row[4], row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33],row[34],row[35],row[36]))
        #cur.execute('INSERT INTO TRAME(numero, numero_trame, date, bench_3, bench_5, Taille, Mac_Src, Mac_Dst, type, Field_2, Field_3, Field_4, Field_5, Field_6, Field_7, MAC_Sender, Source_IP, Sender_IP, Dest_IP, MAC_Target, Field_9, Target_IP, Field_10, Field_11, Field_14, Field_16, Field_17, Field_18, Field_20, Field_21, Field_23, Field_25, Field_26, Field_28, Field_29, Field_30, Field_32, Field_33_34_35, Packet, PMID) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (max_numero, row[0], row[1], None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None))        
        #cur.execute('INSERT INTO TRAME(numero, numero_trame, date, bench_3, bench_5,Taille,Mac_Src,Mac_Dst,type,Field_2,Field_3,Field_4,Field_5,Field_6,Field_7,MAC_Sender,Source_IP,Sender_IP,Dest_IP,MAC_Target,Field_9,Target_IP,Field_10,Field_11,Field_14,Field_16,Field_17,Field_18,Field_20,Field_21,Field_23,Field_25,Field_26,Field_28,Field_29,Field_30,Field_32,Field_33_34_35,Packet,PMID) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',(max_numero,row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33],row[34],row[35],row[36],row[37]))

# Commit des modifications et fermeture de la connexion à la base de données
conn.commit()
conn.close()

#cur.execute("DELETE FROM TRAME;") # supprime tout de la table REPERTOIRE

end = time.time()
elapsed = end - start

print("-----------------------------------------------")
print("Nombre De Trame : " ,trame_count)
print("Temps d execution :", elapsed ,"ms")
print("-----------------------------------------------")