
#### generic import ####
import glob
import json
import langid
import os
import re
import statistics as st

def check_done(destination, corpus_base, options):
  directory_existed = mkdirs(destination)
  if directory_existed:
    print("  Directory already exists :%s"%destination)
    NBdone = len(glob.glob("%s/*"%destination))
    NBtodo = len(glob.glob("%s/html/*"%corpus_base))
    if NBdone==NBtodo and options.force==False:
      print("  ->Already done (%i docs), next"%NBdone)
      return True
    else:
      status = "restarted" if options.force == True else "interrupted"
      print("  ->Process %s (%i/%i) docs"%(status, NBdone, NBtodo))
  return False
  
def get_args():
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option("-c", "--corpus_base", dest="corpus_base",
		  default = "Corpus",
                  help="Corpus to process", metavar="INPUT")
  parser.add_option("-v", "--verbose",
                   action="store_true", dest="verbose", default=False,
                   help="print status messages to stdout")
  parser.add_option("-F", "--force",
                   action="store_true", dest="force", default=False,
                   help="Force redoing already done experiments")
  (options, args) = parser.parse_args()
  return options

def mkdirs(path):
  """
  create directory if needed
  returns True if directory already existed
  """
  try:
    os.makedirs(path)
    return False
  except:
    return True

def read_utf8(fic):
  """
  Reading files
  """
  f = open(fic, "r", encoding = "utf-8")#TODO: Fix encoding issues
  str_text = f.read()
  f.close()
  return str_text

def write_utf8(path, content):
  """
  Write the file
  """
  w = open(path, "w", encoding = "utf-8")
  w.write(content)
  w.close()

def get_measures(dic, beta=1):
  """
  Computing measures form True Positives ....
  """
  TP, FP, FN = dic["TP"], dic["FP"], dic["FN"]
  if TP == 0:
      return {"recall": 0, "precision": 0, "f-score":0}
  R = 100*float(TP)/(TP+FN)
  P = 100*float(TP)/(TP+FP)
  B = beta*beta
  F = (1+B)*P*R/(B*P+R)
  return {"recall": round(R,4),"precision":round(P,4),"f-score": round(F, 4)}

def get_stats(liste):
  """
  returns mean and standard deviation form a list of numbers
  """
  std=0
  if max(liste)>0:
    if len(liste)>1:
      mean = round(st.mean(liste),2)
      std  = round(st.stdev(liste),2)
    else:
      mean = round(liste[0],2)
  else:
    mean = 0
  return mean, std

def get_langid(str_text):
  """
  When needed: identify language
  """
  dic_lg = {	"el":"Greek", "en":"English", "pl":"Polish", 
		"ru":"Russian", "zh": "Chinese"}#TODO; more generic
  langid.set_languages(list(dic_lg.keys()))
  lang = dic_lg[langid.classify(str_text)[0]]
  return lang
