from scipy.stats import entropy
import sys, re, glob
from tools import *
from cleaneval_tool import *
import scipy

def get_voc(tokens):
  d_abs= {}
  for tok in tokens:
    d_abs.setdefault(tok, 0)
    d_abs[tok]+=1
  l = len(tokens)
  d_rel = {x:y/l for x, y in d_abs.items()}
  return d_abs, d_rel

def get_tokens(path):
  text = normalize(slurp_file(path), False, False)
  return re_WS.split(text)

def occ_eval(GT_abs, DET_abs):
  dic = {"TP":0, "FP":0, "FN":0}
  for cle, eff_GT in GT_abs.items():
    eff_DET = 0
    if cle in DET_abs:
      eff_DET = DET_abs[cle]
    FN = max(0, eff_GT-eff_DET)
    FP = max(0, eff_DET-eff_GT)
    dic["FN"] += FN
    dic["FP"] += FP
    dic["TP"] += eff_GT-FN
  for cle, eff_DET in DET_abs.items():
    if cle not in GT_abs:
      dic["FP"]+=eff_DET
  return dic

def dic2vec(dic1, dic2, smoothing=0): #TODO: improve with list comprehension
  L1, L2 = [], []
  for cle1, proba1 in dic1.items():
    L1.append(proba1)
    proba2 = smoothing 
    if cle1 in dic2:
      proba2=dic2[cle1]
    L2.append(proba2)
  for cle2, proba2 in dic2.items():
    L2.append(proba2)
    proba1 = smoothing 
    if cle2 in dic1:
      proba1 = dic1[cle2]
    L1.append(proba1)
  return L1, L2

def get_Kullback(dic1, dic2):
  smoothing = 0.00001#si une des probas est zero, KL est infini 
  vec1, vec2 =  dic2vec(dic1, dic2, smoothing)
  return entropy(vec1, qk=vec2)

def get_cosine(dic1, dic2):
  vec1, vec2 =  dic2vec(dic1, dic2, 0)
  return scipy.spatial.distance.cosine(vec1, vec2)

def get_euclidean(dic1, dic2):
  vec1, vec2 =  dic2vec(dic1, dic2, 0)
  return scipy.spatial.distance.euclidean(vec1, vec2)

def get_new_scores(DET_file, GT_file):
  scores= {}
  toto = ["precision", "recall", "f-score"]
  tokens_GT = get_tokens(GT_file)
  tokens_DET = get_tokens(DET_file)
  GT_abs, GT_rel = get_voc(tokens_GT)
  DET_abs, DET_rel = get_voc(tokens_DET)
  voc_GT = set(GT_abs.keys())
  voc_DET = set(DET_abs.keys())
  dic = {"TP":len(voc_GT.intersection(voc_DET)),
	 "FP":len(voc_DET.difference(voc_GT)),
	 "FN":len(voc_GT.difference(voc_DET))}
  scores["voc_eval_res"] = {x: get_measures(dic)[x] for x in toto}
  scores["KL_res"] = {"KL divergence":get_Kullback(GT_rel, DET_rel),
		      "Euclidean Dist.":get_euclidean(GT_rel, DET_rel),
		      "Cosine Dist.":get_cosine(GT_rel, DET_rel)}
  dic2 = occ_eval(GT_abs,DET_abs)
  scores["occ_eval_res"] = {x: get_measures(dic2)[x] for x in toto}
  return scores

def update_scores(dic_global, dic_car, new_scores, char, TOOL):
    for score_typ in new_scores.keys():
      dic_global[score_typ].setdefault(TOOL, {})
      dic_car[score_typ].setdefault(TOOL, {})
      for mes, val in new_scores[score_typ].items():
        dic_global[score_typ][TOOL].setdefault(mes, [])
        dic_global[score_typ][TOOL][mes].append(val)
        for name, char_val  in char.items():
          dic_car[score_typ][TOOL].setdefault(name , {})
          dic_car[score_typ][TOOL][name].setdefault(char_val, {})
          dic_car[score_typ][TOOL][name][char_val].setdefault(mes, [])
          dic_car[score_typ][TOOL][name][char_val][mes].append(val)
    return dic_global, dic_car

def display_results(dic_global, dic_car, TOOL, results_light):
  results_light[TOOL]={}
  for eval_type in ["clean_eval", "occ_eval_res"]:
    print("--",eval_type)
    L_P = dic_global[eval_type][TOOL]["precision"]
    P = round(st.mean(L_P),4)
    L_R = dic_global[eval_type][TOOL]["recall"]
    R = round(st.mean(L_R),4)
    F = (1+1)*P*R/(1*P+R)
    results_light[TOOL][eval_type] = {"global":F}
    print("  F-score (micro): %f (%i files)"%(F, len(L_P)))
    for caract, d in dic_car[eval_type][TOOL].items():
      print("  By %s:"%caract)
      results_light[TOOL][eval_type]["caract"] = {}
      l_f = []
      for name, res in d.items():
        L = res["f-score"]
        F = round(st.mean(L),4)
        l_f.append(F)
        print("    %s:%f (%i files)"%(name, F, len(L)))
        results_light[TOOL][eval_type]["caract"][name]=F
    print("    F-score (macro): %f"%(st.mean(l_f)))
  return results_light
