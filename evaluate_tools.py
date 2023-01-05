from cleaneval_tool import *
import glob
import re, json, sys
import statistics as st
from generic_functions import *
from scoring_functions import get_new_scores, display_results, update_scores
import os
from optparse import OptionParser

def get_parser():
    """Returns a command line parser
    Returns:
        OptionParser. The command line parser
    """
    parser = OptionParser()
    parser.add_option("-p", "--path_corpus", dest="path_corpus",
                      help="""path to cleaned and reference data
                              default: 'corpora/corpus_sample/'
		      Expected :
                      - MAIN_PATH/reference: all the reference files
                      - MAIN_PATH/cleaned/toto: files obtained via method toto 
                           """, 
                      type="string", default="corpora/corpus_sample/")
    parser.add_option('-u', '--use_lg', help='Use a json file indicating the language of each document to compute statistics by language. If the file is missing, no per language statistics will be computed.  Path: \'MAIN_PATH/doc_lg.json\' Default: True' ,action='store_true', default = True)
    parser.add_option('-r', '--results_path', help='Path to store results. Default: RESULTS' , type="string", default = "RESULTS")
    parser.add_option('-L', '--logs_path', help='Path to store logs. Default: LOGS' , type="string", default = "LOGS")
    return parser

def manage_options(options):
  for path in [options.logs_path, options.results_path]:
    os.makedirs(path, exist_ok=True)
  path_corpus  = options.path_corpus
  dic_path = {"reference": "%s/reference/"%path_corpus,
              "cleaned"  : "%s/cleaned/"%path_corpus}
  path_langues = "%s/doc_lg.json"%path_corpus
  use_lg = options.use_lg
  dic_lg = {}
  if use_lg==True:
    try:
      dic_lg = get_json(path_langues)
    except:
      print("Languages of the corpus are unknown, '%s' missing"%path_langues)
      print("See Corpus/doc_lg.json to see an example of the format")
      use_lg = False

  return use_lg, dic_lg, dic_path, path_langues

parser     = get_parser()
options, _ = parser.parse_args()

use_lg, dic_lg, dic_path, path_langues = manage_options(options)

dataset_name = re.sub("/","", dic_path["cleaned"])
liste_measures = ["precision", "recall", "f-score"]

all_results = {"cleaning_tools": []}
dic_global= {"clean_eval":{}, "voc_eval_res":{}, "KL_res":{}, 
	     "occ_eval_res":{}}
dic_car = {x:{} for x in dic_global.keys()}
results_light = {}

#TODO: ceci ne sert à rien car tout n'est aps dispo en html !
reference_path = {"global":glob.glob(dic_path["reference"]+"/*"), "lg":{}}

#Better:
liste_docs_traites = []
path_log = "LOGS/waddle_eval.log"
w_log = open(path_log, "w")
log_output = 0
#TODO: simplifier la ligne ci-dessous ?

for cpt, dic_path["cleaned"] in enumerate(glob.glob(dic_path["cleaned"]+"/*")):
  TOOL = re.split("/", dic_path["cleaned"])[-1]
  print("Evaluating %s..."%TOOL)
  all_results["cleaning_tools"].append(TOOL)
  for cleaned_file in glob.glob(dic_path["cleaned"]+"/*"):
    filename = re.split("/", cleaned_file)[-1]
    reference_file = dic_path["reference"]+"/"+filename
    char = {"default":"def"}
    if use_lg:
        if filename in dic_lg:
          LG = dic_lg[filename]
        else:
          LG = "unknown"
          w_log.write("%s : not in %s"%(filename, path_langues ))
          log_output+=1 
        if cpt==0:
          #TODO: cleaner ceci
          reference_path["lg"][re.sub("/{1,}", "/", reference_file)] = LG
        char = {"lg":LG}
    else:
      LG = "unknown"

    liste_docs_traites.append([reference_file, LG])
    clean_eval_scores = evaluate_file(cleaned_file, reference_file)
    new_scores = get_new_scores(cleaned_file, reference_file)#TODO:merge
    new_scores["clean_eval"] = {x:clean_eval_scores[x] for x in liste_measures}
    dic_global, dic_car = update_scores(dic_global, dic_car, new_scores, char, TOOL)
  results_light = display_results(dic_global, dic_car, TOOL, results_light)

print(len(liste_docs_traites))
w_log.close()
print("%i lines in %s"%(log_output, path_log)) 

json_out_light = "RESULTS/results_light_%s.json"%dataset_name
write_utf8(json_out_light, json.dumps(results_light, indent=2), verbose=True)

all_results["global"] = dic_global
all_results["characteristics"] = dic_car
all_results["reference_files"] = liste_docs_traites

json_out_path = "RESULTS/results_%s.json"%dataset_name
write_utf8(json_out_path, json.dumps(all_results, indent=2), verbose=True)
