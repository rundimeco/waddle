from cleaneval_tool import *
import glob
import re, json, sys
import statistics as st
from generic_functions import *
from scoring_functions import get_new_scores, display_results, update_scores

main_path = "corpora/corpus_sample/"

if len (sys.argv)!=2:
  print("-"*20)
  print("Usage : python evaluate_all.py PATH_CORPUS")
  print("default : %s"%(main_path))
  print("-"*20)
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
  use_lg = False#TODO: check if it works

dataset_name = re.sub("/","", path_cleaned_all)
liste_measures = ["precision", "recall", "f-score"]

all_results = {"cleaning_tools": []}
dic_global= {"clean_eval":{}, "voc_eval_res":{}, "KL_res":{}, 
	     "occ_eval_res":{}}
dic_car = {x:{} for x in dic_global.keys()}
results_light = {}

reference_path = {"global":glob.glob(path_reference+"/*"), "lg":{}}

for cpt, path_cleaned in enumerate(glob.glob(path_cleaned_all+"/*")):
  TOOL = re.split("/", path_cleaned)[-1]
  print("Evaluating %s..."%TOOL)
  all_results["cleaning_tools"].append(TOOL)
  for cleaned_file in glob.glob(path_cleaned+"/*"):
    filename = re.split("/", cleaned_file)[-1]
    reference_file = path_reference+"/"+filename

    if use_lg:
        LG = dic_lg[filename]
        if cpt==0:
          reference_path["lg"].setdefault(LG, [])
          reference_path["lg"][LG].append(reference_file)
        char = {"lg":LG}

    clean_eval_scores = evaluate_file(cleaned_file, reference_file)
    new_scores = get_new_scores(cleaned_file, reference_file)#TODO:merge
    new_scores["clean_eval"] = {x:clean_eval_scores[x] for x in liste_measures}
    dic_global, dic_car = update_scores(dic_global, dic_car, new_scores, char, TOOL)
  results_light = display_results(dic_global, dic_car, TOOL, results_light)

json_out_light = "RESULTS/results_light_%s.json"%dataset_name
write_utf8(json_out_light, json.dumps(results_light, indent=2), verbose=True)

all_results["global"] = dic_global
all_results["characteristics"] = dic_car
all_results["reference_files"] = reference_path

json_out_path = "RESULTS/results_%s.json"%dataset_name
write_utf8(json_out_path, json.dumps(all_results, indent=2), verbose=True)
