# IMPORTATION DES MODULES

import csv
import datetime
import struct
import time
import argparse
import sys
import json



#CALCUL TEMPS DU PROGRAMME
start = time.time()


#Lancer fichier ligne de commande
def xxxxxxx():
    '''parser = argparse.ArgumentParser()
parser.add_argument('tableau_ft0')
parser.add_argument('tableau_ft1')
parser.add_argument('tableau_ft2')
parser.add_argument('tableau_ft3')
parser.add_argument('tableau_ft4')
parser.add_argument('tableau_ft5')
parser.add_argument('tableau_ft6')
parser.add_argument('tableau_ft7')
parser.add_argument('tableau_ip')
parser.add_argument('tableau_mac')
args = parser.parse_args()
    return
    '''

with open('Code_Python_Bdd/fonctions/tableau_ft0.txt', "r") as f:
    tableau_ft0 = json.load(f)

with open('Code_Python_Bdd/fonctions/tableau_ft1.txt', "r") as f:
    tableau_ft1 = json.load(f)

'''
with open('Code_Python_Bdd/fonctions/tableau_ft2.txt', "r") as f:
    tableau_ft2 = json.load(f)

with open('Code_Python_Bdd/fonctions/tableau_ft3.txt', "r") as f:
    tableau_ft3 = json.load(f)

with open('Code_Python_Bdd/fonctions/tableau_ft4.txt', "r") as f:
    tableau_ft4 = json.load(f)

with open('Code_Python_Bdd/fonctions/tableau_ft5.txt', "r") as f:
    tableau_ft5 = json.load(f)

with open('Code_Python_Bdd/fonctions/tableau_ft6.txt', "r") as f:
    tableau_ft6 = json.load(f)

with open('Code_Python_Bdd/fonctions/tableau_ft7.txt', "r") as f:
    tableau_ft7 = json.load(f)

with open('Code_Python_Bdd/fonctions/tableau_ip.txt', "r") as f:
    tableau_ip = json.load(f)

with open('Code_Python_Bdd/fonctions/tableau_mac.txt', "r") as f:
    tableau_mac = json.load(f)'''

# FONCTIONS DE TRANSFERT ET FONCTION GENERALE

# FONCTION POUR RECUPERER LES BITS

def binaire_from_bytes(texte_encoded):
    '''traduit bits en octets'''
    texte_bits = ''.join(format(byte, '08b') for byte in texte_encoded)  # Conversion en bits
    return texte_bits


# FONCTION DATE POUR TROUVER LA DATE

def seconds_to_date(seconds):
    '''temps en seconde et traduit en fonction de la norme IEEE754 en date '''
    # Définit la date de référence (1er janvier 1970 à 00:00:00 UTC)
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

def transfert_ft1(valeur_brute):
    if valeur_brute in tableau_ft1:
        return tableau_ft1[valeur_brute]
    else:
        return None
    
# FONCTION DE TRANSFERT POUR LABEL ( BENCH_5 )

def transfert_ft0(valeur_brute):
    if valeur_brute in tableau_ft0:
        return tableau_ft0[valeur_brute]
    else:
        return None

tableau_ft6= {  "33C01" :"(MID_1)",
                "33C02"	:"(MID_2)",
                "33C03"	:"(MID_3)",
                "33C04"	:"(MID_4)",
                "33C05"	:"(MID_5)",
                "33C06"	:"(MID_6)",
                "33C07"	:"(MID_7)",
                "33C08"	:"(MID_8)",
                "33C09"	:"(MID_9)",
                "33C0A"	:"(MID_10)",
                "33C0B"	:"(MID_11)",
                "33C0C"	:"(MID_12)",
                "33C0D"	:"(MID_13)",
                "33C0E"	:"(MID_14)",
                "33C0F"	:"(MID_15)",
                "33C10"	:"(MID_16)",
                "33C11"	:"(MID_17)",
                "33C12"	:"(MID_18)",
                "33C13"	:"(MID_19)",
                "33C14"	:"(MID_20)",
                "33C15"	:"(MID_21)",
                "33C16"	:"(MID_22)",
                "33C17"	:"(MID_23)",
                "33C18"	:"(MID_24)",
                "33C19"	:"(MID_25)",
                "33C1A"	:"(MID_26)",
                "33C1B"	:"(MID_27)",
                "33C1C"	:"(MID_28)",
                "33C1D"	:"(MID_29)",
                "33C1E"	:"(MID_30)",
                "33C1F"	:"(MID_31)",
                "33C20"	:"(MID_32)",
                "33C21"	:"(MID_33)",
                "33C22"	:"(MID_34)",
                "33C23"	:"(MID_35)",
                "33C24"	:"(MID_36)",
                "33C25"	:"(MID_37)",
                "33C26"	:"(MID_38)",
                "33C27"	:"(MID_39)",
                "33C28"	:"(MID_40)",
                "33C29"	:"(MID_41)",
                "33C2A"	:"(MID_42)",
                "33C2B"	:"(MID_43)",
                "33C41"	:"(MID_44)",
                "33C42"	:"(MID_45)",
                "33C43"	:"(MID_46)",
                "33C44"	:"(MID_47)",
                "33C45"	:"(MID_48)",
                "33C46"	:"(MID_49)",
                "33C47"	:"(MID_50)",
                "33C61"	:"(MID_51)",
                "33C62"	:"(MID_52)",
                "33C63"	:"(MID_53)",
                "33C64"	:"(MID_54)",
                "33C65"	:"(MID_55)",
                "33C66"	:"(MID_56)",
                "33C67"	:"(MID_57)",
                "33C68"	:"(MID_58)",
                "33C69"	:"(MID_59)",
                "33D08"	:"(MID_60)",
                "33D10"	:"(MID_61)",
                "33D11"	:"(MID_62)",
                "33D18"	:"(MID_63)",
                "33D60"	:"(MID_64)",
                "33DC0"	:"(MID_65)",
                "33DC8"	:"(MID_66)",
                "33DC9"	:"(MID_67)",
                "34C01"	:"(MID_68)",
                "34C02"	:"(MID_69)",
                "34C03"	:"(MID_70)",
                "34C04"	:"(MID_71)",
                "34C05"	:"(MID_72)",
                "34C06"	:"(MID_73)",
                "34C07"	:"(MID_74)",
                "34C08"	:"(MID_75)",
                "34C09"	:"(MID_76)",
                "34C0A"	:"(MID_77)",
                "34C0B"	:"(MID_78)",
                "34C0C"	:"(MID_79)",
                "34C0D"	:"(MID_80)",
                "34C0E"	:"(MID_81)",
                "34C0F"	:"(MID_82)",
                "34C10"	:"(MID_83)",
                "34C11"	:"(MID_84)",
                "34C12"	:"(MID_85)",
                "34C13"	:"(MID_86)",
                "34C14"	:"(MID_87)",
                "34C15"	:"(MID_88)",
                "34C16"	:"(MID_89)",
                "34C17"	:"(MID_90)",
                "34C18"	:"(MID_91)",
                "34C19"	:"(MID_92)",
                "34C1A"	:"(MID_93)",
                "34C1B"	:"(MID_94)",
                "34C1C"	:"(MID_95)",
                "34C1D"	:"(MID_96)",
                "34C1E"	:"(MID_97)",
                "34C1F"	:"(MID_98)",
                "34C21"	:"(MID_99)",
                "34C22"	:"(MID_100)",
                "34C23"	:"(MID_101)",
                "34C24"	:"(MID_102)",
                "34C25"	:"(MID_103)",
                "34C26"	:"(MID_104)",
                "34C27"	:"(MID_105)",
                "34C28"	:"(MID_106)",
                "34C29"	:"(MID_107)",
                "34C2A"	:"(MID_108)",
                "34C41"	:"(MID_109)",
                "34C43"	:"(MID_110)",
                "34C44"	:"(MID_111)",
                "34C45"	:"(MID_112)",
                "34C46"	:"(MID_113)",
                "34C47"	:"(MID_114)",
                "34C61"	:"(MID_115)",
                "34C62"	:"(MID_116)",
                "34C63"	:"(MID_117)",
                "34C64"	:"(MID_118)",
                "34C65"	:"(MID_119)",
                "34C66"	:"(MID_120)",
                "34C67"	:"(MID_121)",
                "34C68"	:"(MID_122)",
                "34C69"	:"(MID_123)",
                "34D08"	:"(MID_124)",
                "34D18"	:"(MID_125)",
                "34D60"	:"(MID_126)",
                "34DC0"	:"(MID_127)",
                "8033C01"	:"(MID_128)",
                "8033C02"	:"(MID_129)",
                "8033C03"	:"(MID_130)",
                "8033C04"	:"(MID_131)",
                "8033C05"	:"(MID_132)",
                "8033C06"	:"(MID_133)",
                "8033C07"	:"(MID_134)",
                "8033C08"	:"(MID_135)",
                "8033C09"	:"(MID_136)",
                "8033C0A"	:"(MID_137)",
                "8033C0B"	:"(MID_138)",
                "8033C0C"	:"(MID_139)",
                "8033C0D"	:"(MID_140)",
                "8033C0E"	:"(MID_141)",
                "8033C0F"	:"(MID_142)",
                "8033C10"	:"(MID_143)",
                "8033C11"	:"(MID_144)",
                "8033C12"	:"(MID_145)",
                "8033C13"	:"(MID_146)",
                "8033C14"	:"(MID_147)",
                "8033C15"	:"(MID_148)",
                "8033C16"	:"(MID_149)",
                "8033C17"	:"(MID_150)",
                "8033C18"	:"(MID_151)",
                "8033C19"	:"(MID_152)",
                "8033C1A"	:"(MID_153)",
                "8033C1B"	:"(MID_154)",
                "8033C1C"	:"(MID_155)",
                "8033C1D"	:"(MID_156)",
                "8033C1E"	:"(MID_157)",
                "8033C21"	:"(MID_158)",
                "8033C22"	:"(MID_159)",
                "8033C23"	:"(MID_160)",
                "8033C24"	:"(MID_161)",
                "8033C25"	:"(MID_162)",
                "8033C26"	:"(MID_163)",
                "8033C27"	:"(MID_164)",
                "8033C28"	:"(MID_165)",
                "8033C29"	:"(MID_166)",
                "8033C2A"	:"(MID_167)",
                "8033C2B"	:"(MID_168)",
                "8033C2C"	:"(MID_169)",
                "8033C2D"	:"(MID_170)",
                "8033C2E"	:"(MID_171)",
                "8033C2F"	:"(MID_172)",
                "8033C41"	:"(MID_173)",
                "8033C42"	:"(MID_174)",
                "8033C43"	:"(MID_175)",
                "8033C46"	:"(MID_176)",
                "8033C47"	:"(MID_177)",
                "8033C48"	:"(MID_178)",
                "8033C49"	:"(MID_179)",
                "8033C4A"	:"(MID_180)",
                "8033C61"	:"(MID_181)",
                "8033C62"	:"(MID_182)",
                "8033C63"	:"(MID_183)",
                "8033C64"	:"(MID_184)",
                "8033C65"	:"(MID_185)",
                "8033C66"	:"(MID_186)",
                "8033D08"	:"(MID_187)",
                "8033D09"	:"(MID_188)",
                "8033D18"	:"(MID_189)",
                "8033D19"	:"(MID_190)",
                "8033D60"	:"(MID_191)",
                "8033D61"	:"(MID_192)",
                "8033D62"	:"(MID_193)",
                "8033DC0"	:"(MID_194)",
                "8033DC1"	:"(MID_195)",
                "8033DC8"	:"(MID_196)",
                "8034C01"	:"(MID_197)",
                "8034C02"	:"(MID_198)",
                "8034C03"	:"(MID_199)",
                "8034C04"	:"(MID_200)",
                "8034C05"	:"(MID_201)",
                "8034C06"	:"(MID_202)",
                "8034C07"	:"(MID_203)",
                "8034C08"	:"(MID_204)",
                "8034C09"	:"(MID_205)",
                "8034C0A"	:"(MID_206)",
                "8034C0B"	:"(MID_207)",
                "8034C0C"	:"(MID_208)",
                "8034C0D"	:"(MID_209)",
                "8034C0E"	:"(MID_210)",
                "8034C0F"	:"(MID_211)",
                "8034C10"	:"(MID_212)",
                "8034C11"	:"(MID_213)",
                "8034C12"	:"(MID_214)",
                "8034C13"	:"(MID_215)",
                "8034C14"	:"(MID_216)",
                "8034C15"	:"(MID_217)",
                "8034C16"	:"(MID_218)",
                "8034C17"	:"(MID_219)",
                "8034C18"	:"(MID_220)",
                "8034C19"	:"(MID_221)",
                "8034C1A"	:"(MID_222)",
                "8034C1B"	:"(MID_223)",
                "8034C1C"	:"(MID_224)",
                "8034C1D"	:"(MID_225)",
                "8034C1E"	:"(MID_226)",
                "8034C21"	:"(MID_227)",
                "8034C22"	:"(MID_228)",
                "8034C23"	:"(MID_229)",
                "8034C24"	:"(MID_230)",
                "8034C25"	:"(MID_231)",
                "8034C26"	:"(MID_232)",
                "8034C27"	:"(MID_233)",
                "8034C28"	:"(MID_234)",
                "8034C29"	:"(MID_235)",
                "8034C2A"	:"(MID_236)",
                "8034C2B"	:"(MID_237)",
                "8034C2C"	:"(MID_238)",
                "8034C2D"	:"(MID_239)",
                "8034C2E"	:"(MID_240)",
                "8034C2F"	:"(MID_241)",
                "8034C41"	:"(MID_242)",
                "8034C42"	:"(MID_243)",
                "8034C43"	:"(MID_244)",
                "8034C46"	:"(MID_245)",
                "8034C47"	:"(MID_246)",
                "8034C48"	:"(MID_247)",
                "8034C49"	:"(MID_248)",
                "8034C4A"	:"(MID_249)",
                "8034C61"	:"(MID_250)",
                "8034C62"	:"(MID_251)",
                "8034C63"	:"(MID_252)",
                "8034C64"	:"(MID_253)",
                "8034C65"	:"(MID_254)",
                "8034C66"	:"(MID_255)",
                "8034D08"	:"(MID_256)",
                "8034D08"	:"(MID_257)",
                "8034D09"	:"(MID_258)",
                "8034D18"	:"(MID_259)",
                "8034D19"	:"(MID_260)",
                "8034D60"	:"(MID_261)",
                "8034D61"	:"(MID_262)",
                "8034D62"	:"(MID_263)",
                "8034DC0"	:"(MID_264)",
                "8034DC1"	:"(MID_265)",
            }

def transfert_ft6(valeur_brute):#rajouter parenthese tableau
    if valeur_brute in tableau_ft6:
        return tableau_ft6[valeur_brute]
    else :
        return
    

# DEBUT DU PROGRAMME PRINCIPALE


with open("Code_Python_Bdd/ethernet.result_data", "rb") as f:
    # ouverture du fichier CSV en mode écriture
    with open("ethernet.result_data.csv", mode='w', newline='') as csv_file:
        # déclaration des colonnes dans l'en-tête du fichier CSV
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

# IMPORTATION DES MODULES

#cur.execute("DELETE FROM TRAME;") # supprime tout de la table REPERTOIRE
            
end = time.time()
elapsed = end - start

print("-----------------------------------------------")
print("Nombre De Trame : " ,trame_count)
print("Temps d execution :", elapsed ,"ms")
print("-----------------------------------------------")