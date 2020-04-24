import glob
import langid
import re
import statistics
import time
from tools import *
from generic_functions import *

import warnings
warnings.simplefilter("ignore")

options = get_args()
source = "html" #
corpus_base = options.corpus_base
liste_fic = glob.glob("%s/%s/*"%(corpus_base, source))

##TODO: add prints (corpus directory ...)

modes ={
        ##Comment lines to use just some tools
	#"BP3":["", "Article", "Largest", "KeepEverything"],
        #"DRAG":[""],
	#"GOO":[""],
	#"HTML2TEXT":[""],
	#"INSCRIPTIS":[""],
	#"JT":["", "_english", "_langid", "_trueLg"], 
        #"NEWSPAPER":[""],
        #"NEWSPLEASE":[""],
	#"READABILITY":[""],
	"TRAF":["", "Fallback", "Comments", "FallbackComments"]
	}

## TODO: send warnings to a log
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
      list_paragraphs = apply_tool(tool, fic, mode)
      if list_paragraphs ==[""]:
        diagnostic.setdefault(namefic,  [])
        diagnostic[namefic].append([tool, mode])
      write_utf8(path_out, "<p>%s</p>"%"</p>\n<p>".join(list_paragraphs))
    print("  duration:%f"%(time.time()-start))

import json
write_utf8("diagnostics.json", json.dumps(diagnostic, indent= 2))
