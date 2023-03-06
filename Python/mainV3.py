# IMPORTATION DES MODULES

import csv
import datetime
import struct
import time



#CALCUL TEMPS DU PROGRAMME
start = time.time()


# FONCTIONS DE TRANSFERT ET FONCTION GENERALE

# FONCTION POUR RECUPER LES BITS

def binaire_from_bytes(texte_encoded):
    texte_bits = ''.join(format(byte, '08b') for byte in texte_encoded)  # Conversion en bits
    return texte_bits


# FONCTION DATE POUR TROUVER LA DATE

def seconds_to_date(seconds):
    # Définit la date de référence (1er janvier 1970 à 00:00:00 UTC)
    reference_date = datetime.datetime(1970, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)

    # Ajoute le nombre de secondes à la date de référence pour obtenir la date correspondante
    date = reference_date + datetime.timedelta(seconds=seconds)

    # Formate la date et l'heure dans une chaîne de caractères
    formatted_date = date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    return formatted_date

def seconds_to_date2(seconds):
    # Définit la date de référence (20 JANVIER 2020 à 00:00:00 UTC)
    reference_date = datetime.datetime(2000, 1, 1, 12, 0, 0, 0, datetime.timezone.utc)

    # Ajoute le nombre de secondes à la date de référence pour obtenir la date correspondante
    date = reference_date + datetime.timedelta(seconds=seconds)

    # Formate la date et l'heure dans une chaîne de caractères
    formatted_date = date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    return formatted_date

# FONCTION DE TRASNFERT POUR ADRESSE MAC

# J'ai modifie les valeur des trois prermiers case du tableau car elle etait en maj et que les valeurs de la trame non
# Rajout d'une Ligne dans le tableau car dans le excel il y a une valeur TBD

tableau_mac = {
    "0010ec01e541": "00:10:EC:01:E5:41 (ordi_1)",
    "0010ec01e543": "00:10:EC:01:E5:43 (ordi_2)",
    "0010ec01e544": "00:10:EC:01:E5:44 (ordi_3)",
    "001f295794f2": "00:1f:29:57:94:f (ordi_4)",
    "001f295794f3": "00:1f:29:57:94:f3 (ordi_5)",
    "b47af1e3416b": "b4:7a:f1:e3:41:6b (ordi_6)",
    "ffffffffffff": "FF:FF:FF:FF:FF:FF (TBD)"
}

def transfert_mac(valeur_brute):
    if valeur_brute in tableau_mac:
        return tableau_mac[valeur_brute]
    else:
        return None


# FONCTION TRANSFERT IP 

tableau_ip = {
    "A9FEAD05": "169.254.173.5 (ordi_1)",
    "A9FEADE0": "169.254.173.224 (ordi_2)",
    "A9FEAE05": "169.254.174.5 (ordi_3)",
    "A9FEAEDF": "169.254.174.223 (ordi_4)",
    "A9FEAF05": "169.254.175.5 (ordi_5)",
    "A9FEAFDE": "169.254.175.222 (ordi_6)"
}

def transfert_ip(valeur_brute):
    valeur_brute = valeur_brute.upper()
    if valeur_brute in tableau_ip:
        return tableau_ip[valeur_brute]
    else:
        return None


# FONCTION TRANSFERT FT_7 POUR LABEL ( FIELD_14 )

tableau_ft7 = {
    "0": "0 FT_7_label_1",
    "1": "1 FT_7_label_2",
}

def transfert_ft7(valeur_brute):
    valeur_brute = valeur_brute[3]
    if valeur_brute in tableau_ft7:
        return tableau_ft7[valeur_brute]
    else:
        return None
    
# FONCTION DE TRANSFERT FT_5 POUR LABEL ( FIELD_17 )

tableau_ft5 = {
    0: "0 FT_5_label_1",
    1: "1 FT_5_label_2",
    2: "2 FT_5_label_3",
    3: "3 FT_5_label_4",
    4: "4 FT_5_label_5",
    5: "5 FT_5_label_6",
    6: "6 FT_5_label_7",
    7: "7 FT_5_label_8",
}

def transfert_ft5(valeur_brute):
    valeur_brute = valeur_brute[8:11]
    valeur_brute_v2 = int(valeur_brute,2)
    if valeur_brute_v2 in tableau_ft5:
        return tableau_ft5[valeur_brute_v2]
    else:
        return None

# FONCTION DE TRANSFERT FT_2 POUR LABEL ( Field_18 )

tableau_ft2 = {
    0: "0 FT_2_label_1",
    1: "1 FT_2_label_2"
}

def transfert_ft2(valeur_brute):
    valeur_brute = valeur_brute[11:16]
    valeur_brute_v2 = int(valeur_brute,2)
    if valeur_brute_v2 in tableau_ft2:
        return tableau_ft2[valeur_brute_v2]
    else:
        return None

# FONCTION TRANSFERT FT_3 POUR LABEL ( FIELD_28 )

tableau_ft3 = {
    "0": "0 FT_3_label_1",
    "1": "1 FT_3_label_2",
    "2": "2 FT_3_label_3",
    "3": "3 FT_3_label_4",
    "4": "4 FT_3_label_5",
}



def transfert_ft3(valeur_brute):
    if valeur_brute in tableau_ft3:
        return tableau_ft3[valeur_brute]
    else:
        return None
    


# FOnction TRANSFERT FT_4 POUR LABEL ( Field_29 )

tableau_ft4 = {
    "0": "0 FT_4_label_1",
    "1": "1 FT_4_label_2",
    "2": "2 FT_4_label_3",
    "3": "3 FT_4_label_4",
    "4": "4 FT_4_label_5",
    "5": "5 FT_4_label_6",
    "6": "6 FT_4_label_7",
    "7": "7 FT_4_label_8",
    "8": "8 FT_4_label_9",
    "9": "9 FT_4_label_10",
    "a": "10 FT_4_label_11",
    "b": "11 FT_4_label_12",
    "c": "12 FT_4_label_13",
    "d": "13 FT_4_label_14",
    "e": "14 FT_4_label_15",
    "f": "15 FT_4_label_16",

}

def transfert_ft4(valeur_brute):
    if valeur_brute in tableau_ft4:
        return tableau_ft4[valeur_brute]
    else:
        return None

# FONCTION DE TRANSFERT POUR LABEL ( Field_32 )

tableau_ft1 = {
    1: "1 FT_1_label_1",
    2: "2 FT_1_label_2",
    3: "3 FT_1_label_3",
    17: "17 FT_4_label_17",
    192: "192 FT_4_label_192",
    208: "208 FT_4_label_208",
}

def transfert_ft1(valeur_brute):
    if valeur_brute in tableau_ft1:
        return tableau_ft1[valeur_brute]
    else:
        return None
    
# FONCTION DE TRANSFERT POUR LABEL ( BENCH_5 )

tableau_ft0 = {
    0: "1 FT_0_label_1",
    1: "2 FT_0_label_2",
}

def transfert_ft0(valeur_brute):
    if valeur_brute in tableau_ft0:
        return tableau_ft0[valeur_brute]
    else:
        return None



# DEBUT DU PROGRAMME PRINCIPALE


with open("ethernet.result_data", "rb") as f:
    # ouverture du fichier CSV en mode écriture
    with open("ethernet.result_data.csv", mode='w', newline='') as csv_file:
        # déclaration des colonnes dans l'en-tête du fichier CSV
        fieldnames = ['Trame', 'Date', 'Bench 3', 'Bench 5', 'Taille de la trame','Mac_Src','Mac_Dst','Type','Field_2','Field_3','Field_4','Field_5','Field_6','Field_7','MAC_Sender','Source_IP','Sender_IP','Dest_IP','MAC_Target','Field_9','Target_IP','Field_10','Field_11','Field_14','Field_16','Field_17','Field_18','Field_20','Field_21','Field_23','Field_25','Field_26','Field_28','Field_29','Field_30','Field_32','Field_33_34_35','Time Packet (cal)','PMID']
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

                field_14_transfert = transfert_ft7(binaire_from_bytes(field_1345678_bytes))

                # FIEL_16 FONCTION TRANSFERT FT7

                field_16 = binaire_from_bytes(field_1345678_bytes)
                field_16 = field_16[5:8]

                # FIELD_17 FONCTION DE TRANSFERT FT5
                field_17 = transfert_ft5(binaire_from_bytes(field_1345678_bytes))

                #FIELD_18 FONCTION TRANFERST FT2
                field_18 = transfert_ft2(binaire_from_bytes(field_1345678_bytes))

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
                field_28 = field_28[2:8]
                field_28 = int(field_28,2)
                field_28 = hex(field_28)[2:]
                field_28_transfert = transfert_ft3(field_28)

                # Field_29,30
                field_2930_bytes = f.read(2)
                #field_2930 = field_2930_bytes.hex()

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

                writer.writerow({'Trame': trame_count, 'Date': date2, 'Bench 3': bench3, 'Bench 5': field_5_transfert, 'Taille de la trame': size, 'Mac_Src': mac_src_transfert, 'Mac_Dst': mac_dst_transfert, 'Type':type[1:4],'Field_2':field_2,'Field_3':field_3,'Field_4':field_4,'Field_5':field_5,'Field_6':field_6,'Field_7':field_7,'Source_IP':source_ip_transfert,'Dest_IP':dest_ip_transfert,'Field_9':field_9,'Field_10':field_10,'Field_11':field_11,'Field_14': field_14_transfert,'Field_16':field_16,'Field_17':field_17,'Field_18':field_18,'Field_20':field_20,'Field_21':field_21,'Field_23':field_23,'Field_25':field_25,'Field_26':field_26,'Field_28':field_28_transfert,'Field_29':field_29_transfert,'Field_30':field_30,'Field_32':field_32_transfert,'Field_33_34_35':field_33_34_35,'Time Packet (cal)':time_packet})
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
                writer.writerow({'Trame': trame_count, 'Date': date2, 'Bench 3': bench3, 'Bench 5': field_5_transfert, 'Taille de la trame': size, 'Mac_Src': mac_src_transfert, 'Mac_Dst': mac_dst_transfert, 'Type':type[1:4],'Field_2':field_2,'Field_3':field_3,'Field_4':field_4,'Field_5':field_5,'Field_6':field_6,'MAC_Sender':mac_sender_transfert,'Sender_IP':sender_ip_transfert,'MAC_Target':mac_target_tranfert,'Target_IP':target_ip_tranfert})
                # aller à la trame suivante
                f.seek((size-6-6-2-2-2-1-1-2-6-4-6-4), 1)
                # incrémentation du compteur de trames
                trame_count += 1
            
end = time.time()
elapsed = end - start

print("-----------------------------------------------")
print("Nombre De Trame : " ,trame_count)
print("Temps d execution :", elapsed ,"ms")
print("-----------------------------------------------")