from cleaneval_tool import *
from generic_functions import *
from scoring_functions import get_new_scores, display_results, update_scores

import glob
import re
import json
import sys
if len(sys.argv)==1:
  print("Donner le chemin des dossiers auteurs en argument (généralement DATA/)")
  exit()

path_auteurs = sys.argv[1]
liste_dossiers_auteurs = glob.glob(f"{path_auteurs}/*")
print(liste_dossiers_auteurs)
if len(liste_dossiers_auteurs)==0:
  print("Problème with path auteurs: pas de dossier trouvés")
  exit()
for auteur in liste_dossiers_auteurs:
    print("-"*20)
    reference_files = glob.glob(f"{auteur}/REF/*.txt")
    ocr_paths = glob.glob(f"{auteur}/OCR/*")
    print(re.split("/",auteur)[-1])
    print("Number of reference files : ",len(reference_files))
    print("Number of OCR versions : ",len(ocr_paths))
    for reference_file in reference_files:
        print(reference_file)
        for ocr_path in ocr_paths:
            print(ocr_path)
            ocr_file = glob.glob(f"{ocr_path}/*.txt")[0]
            clean_eval_scores = evaluate_file(ocr_file, reference_file)
            #remove tags:
            clean_eval_scores = {x:y for x,y in clean_eval_scores.items() if "tag" not in x}
            new_scores = get_new_scores(ocr_file, reference_file)#TODO:merge
            #TODO: CER, WER
            json_path   = f"{ocr_file}.json"
            new_scores["clean_eval"] = clean_eval_scores
            print("  Writing:",json_path)
            with open(json_path, "w") as w:
                w.write(json.dumps(new_scores, indent=2))
