from cleaneval_tool import *
from generic_functions import *
from scoring_functions import get_new_scores, display_results, update_scores

import glob
import re
import json
import sys
import os

def create_str_ner(json_path, str_path):
    """
    Transforme la liste d'entités en une string
    les mots des entités multi-mots sont concaténés
    """
    with open(json_path) as f:
        liste = json.load(f)
    liste = [re.sub("\s", "", x) for x in liste]
    with open(str_path, "w") as w:
        w.write(" ".join(liste))

def get_model_name(chemin):
    model_name = re.split("_", chemin)[-1]
    model_name =re.sub("\.json", "", model_name)
    return model_name

if len(sys.argv)==1:
  print("Donner le chemin des dossiers auteurs en argument (généralement DATA/)")
  exit()

os.makedirs("tmp", exist_ok=True)

path_auteurs = sys.argv[1]
liste_dossiers_auteurs = glob.glob(f"{path_auteurs}/*")
if len(liste_dossiers_auteurs)==0:
  print("Problème with path auteurs: pas de dossier trouvés")
  exit()
#TOD: dans le code d'extraction des entités, créer le nossier NER
for auteur in liste_dossiers_auteurs:
    if "ADAM" not in auteur:
        continue
    print("-"*20)
    #NB: La structure est différente : un level de plus dans le dossier OCR
    reference_files = glob.glob(f"{auteur}/REF/NER/*.json")
    ocr_paths = glob.glob(f"{auteur}/OCR/*/NER/*.json")
    print(re.split("/",auteur)[-1])
    print("Number of reference files : ",len(reference_files))
    print("Number of OCR versions : ",len(ocr_paths))
    for reference_file in reference_files:
        print(reference_file)
        model_name_ref = get_model_name(reference_file)
        create_str_ner(reference_file, "tmp/ref.txt")
        for ocr_path in ocr_paths:
            model_name_ocr = get_model_name(ocr_path)
            if model_name_ref!=model_name_ocr:
                continue
            configuration = re.split("/", ocr_path)[-1]
            sim_path = "/".join(re.split("/", ocr_path)[:-1])+"/SIM/"
            os.makedirs(sim_path, exist_ok=True)
            create_str_ner(ocr_path, "tmp/ocr.txt")
            ocr_file = "tmp/ocr.txt"
            ref_file = "tmp/ref.txt"
            clean_eval_scores = evaluate_file(ocr_file, ref_file)
            #remove tags:
            clean_eval_scores = {x:y for x,y in clean_eval_scores.items() if "tag" not in x}
            new_scores = get_new_scores(ocr_file, ref_file)#TODO:merge
            #TODO: CER, WER
            json_path   = f"{sim_path}sim_{configuration}"
            new_scores["clean_eval"] = clean_eval_scores
            print("  Writing:",json_path)
            with open(json_path, "w") as w:
                w.write(json.dumps(new_scores, indent=2))
