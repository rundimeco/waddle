import glob
import langid
import re
import statistics
import time
import warnings
from tools import *
from generic_functions import *

warnings.filterwarnings("ignore")

options = get_args()
source = "html" #
corpus_base = options.corpus_base
liste_fic = glob.glob("%s/%s/*"%(corpus_base, source))
if len(liste_fic)==0:
  print("No files in '%s/%s/'"%(corpus_base, source))
  print("-"*30)
  print("For processing the fully annotated Daniel corpus :")
  print("python test_all_tools.py -c corpora/Corpus_daniel_v2.1/")
  print("-"*30)
  print("exiting ...")
  exit()
else:
  print("Processing '%s/%s/'"%(corpus_base, source))

modes ={
        ##Comment lines to use just some tools
	"BP3":["", "Article", "Largest", "KeepEverything"],
        #"DRAG":[""], ##TODO:solution to deprecated joblib (sklearn) error
	"GOO":[""],
	"HTML2TEXT":[""],
	"INSCRIPTIS":[""],
	"JT":["", "_english", "_langid", "_trueLg"], 
        "NEWSPAPER":[""],
#        "NEWSPLEASE":[""],
	"READABILITY":[""],
	"TRAF":["", "Fallback", "Comments", "FallbackComments"],
        #"TRAF_BL":[""],
        "READ_py":[""],##TODO: what happens with missing css ?
        "HTML-text":[""]
	}
durations = {}
diagnostic = {"empty_files":{}}
for tool in modes.keys():
  for mode in modes[tool]:
    destination = "%s/cleaned/%s%s"%(corpus_base,tool, mode)
    print("tool (Mode) :: %s(%s)"%(tool, mode))
    is_done = check_done(destination, corpus_base, options)
    if is_done==True and options.force==False:
      continue
    start = time.time()
    for cpt, fic in enumerate(liste_fic):
      namefic = re.split("/", fic)[-1]
      path_out = "%s/%s"%(destination, namefic)
      if options.force==False and os.path.exists(path_out):
        continue
      str_text = read_utf8(fic, options.verbose)
      list_paragraphs = apply_tool(tool, str_text, mode)
      if list_paragraphs ==[""]:
        diagnostic.setdefault(namefic,  [])
        diagnostic[namefic].append([tool, mode])
      write_utf8(path_out, "<p>%s</p>"%"</p>\n<p>".join(list_paragraphs))
    duration = time.time()-start
    durations["%s(%s)"%(tool, mode)] = duration
    print("  duration:%f"%(duration))

import json

write_utf8("%s/durations.json"%corpus_base, json.dumps(durations, indent= 2), verbose=True)
write_utf8("%s/diagnostics.json"%corpus_base, json.dumps(diagnostic, indent= 2), verbose=True)
