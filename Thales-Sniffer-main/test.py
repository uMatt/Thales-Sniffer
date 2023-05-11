import argparse
import json

parser = argparse.ArgumentParser(
    prog = "ProgramName",
    description="test",
    epilog="azeazeaeaze")

parser.add_argument('filename')
args = parser.parse_args()

with open(args.filename, 'r') as f:
    v = json.load(f)

print(v)

tableau_ft0 = v

def transfert_ft0(valeur_brute):
    if valeur_brute in tableau_ft0:
        return tableau_ft0[valeur_brute]
    else:
        return None

print(transfert_ft0("0"))