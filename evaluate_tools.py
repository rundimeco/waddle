from cleaneval_tool import *
import glob
import re, json, sys
import statistics as st
from generic_functions import *
from scoring_functions import get_new_scores, display_results, update_scores

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
results_light = {}

for path_cleaned in glob.glob(path_cleaned_all+"/*"):
  TOOL = re.split("/", path_cleaned)[-1]
  print("Evaluating %s..."%TOOL)
  all_results["cleaning_tools"].append(TOOL)
  for cleaned_file in glob.glob(path_cleaned+"/*"):
    filename = re.split("/", cleaned_file)[-1]
    reference_file = path_reference+"/"+filename

    if use_lg:
        char = {"lg":dic_lg[filename]}

    clean_eval_scores = evaluate_file(cleaned_file, reference_file)
    new_scores = get_new_scores(cleaned_file, reference_file)#TODO:merge
    new_scores["clean_eval"] = {x:clean_eval_scores[x] for x in liste_measures}
    dic_global, dic_car = update_scores(dic_global, dic_car, new_scores, char, TOOL)
  results_light = display_results(dic_global, dic_car, TOOL, results_light)

json_out_light = "results_light_%s.json"%dataset_name
write_utf8(json_out_light, json.dumps(results_light, indent=2), verbose=True)

all_results["global"] = dic_global
all_results["characteristics"] = dic_car

json_out_path = "results_%s.json"%dataset_name
write_utf8(json_out_path, json.dumps(all_results, indent=2), verbose=True)
