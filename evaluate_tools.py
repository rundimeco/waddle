from cleaneval_tool import *
import glob
import re, json, sys
import statistics as st
from generic_functions import *
from scoring_functions import get_new_scores

main_path = "Corpus"

if len (sys.argv)!=2:
  print("Usage : python evaluate_all.py PATH_CORPUS")
  print("default : %s"%(main_path))
else:
  main_path = sys.argv[1]

path_reference = "%s/reference/"%main_path
path_cleaned_all = "%s/cleaned/"%main_path
path_langues = "%s/doc_lg.json"%main_path

use_lg = True
try:
  dic_lg = get_json(path_langues)
except:
  print("Document languages for current corpus is missing : %s"%path_langues)
  print("See Corpus/doc_lg.json to see an example")
  use_lg = False

dataset_name = re.sub("/","", path_cleaned_all)
liste_measures = ["precision", "recall", "f-score"]

all_results = {"cleaning_tools": []}
dic_global= {"clean_eval":{}, "voc_eval_res":{}, "KL_res":{}, 
	     "occ_eval_res":{}}

dic_car = {x:{} for x in dic_global.keys()}

if use_lg:
  caracteristics = ["lg"]
else:
  caracteristics = []

results_light = {}

for path_cleaned in glob.glob(path_cleaned_all+"/*"):
  TOOL = re.split("/", path_cleaned)[-1]
  print("Evaluating %s..."%TOOL)
  all_results["cleaning_tools"].append(TOOL)
  for cleaned_file in glob.glob(path_cleaned+"/*"):

    filename = re.split("/", cleaned_file)[-1]
    reference_file = path_reference+"/"+filename

    if use_lg:
      list_car = [dic_lg[filename]]

    clean_eval_scores = evaluate_file(cleaned_file, reference_file)
    new_scores = get_new_scores(cleaned_file, reference_file)
    new_scores["clean_eval"] = {x:clean_eval_scores[x] for x in liste_measures}
    for score_typ in new_scores.keys():
      dic_global[score_typ].setdefault(TOOL, {})
      dic_car[score_typ].setdefault(TOOL, {})
      for mes, val in new_scores[score_typ].items():
        dic_global[score_typ][TOOL].setdefault(mes, [])
        dic_global[score_typ][TOOL][mes].append(val)
        for cc, caract in enumerate(caracteristics):
          dic_car[score_typ][TOOL].setdefault(caract , {})
          dic_car[score_typ][TOOL][caract].setdefault(list_car[cc], {})
          dic_car[score_typ][TOOL][caract][list_car[cc]].setdefault(mes, [])
          dic_car[score_typ][TOOL][caract][list_car[cc]][mes].append(val)
  L_P = dic_global["clean_eval"][TOOL]["precision"]
  P = round(st.mean(L_P),4)
  L_R = dic_global["clean_eval"][TOOL]["recall"]
  R = round(st.mean(L_R),4)
  F = (1+1)*P*R/(1*P+R)
  results_light[TOOL] = {"global":F}
  print("  F-score : %f (%i files)"%(F, len(L_P)))
  for caract, d in dic_car["clean_eval"][TOOL].items():
    print("  By %s:"%caract)
    results_light[TOOL]["caract"] = {}
    for name, res in d.items():
        L = res["f-score"]
        F = round(st.mean(L),4)
        print("    %s:%f (%i files)"%(name, F, len(L)))
        results_light[TOOL]["caract"][name]=F

json_out_path = "results_light_%s.json"%dataset_name
write_utf8(json_out_path, json.dumps(results_light, indent=2))
print("Results in JSON format : %s"%json_out_path)

all_results["global"] = dic_global
all_results["characteristics"] = dic_car

json_out_path = "results_%s.json"%dataset_name
write_utf8(json_out_path, json.dumps(all_results, indent=2))
print("Results in JSON format : %s"%json_out_path)
