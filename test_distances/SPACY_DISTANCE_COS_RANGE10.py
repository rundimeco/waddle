import re
import glob
import spacy
import json
import sklearn
import os
import shutil
from sklearn.neighbors import DistanceMetric
import scipy
from sklearn.feature_extraction.text import CountVectorizer
def get_voc(tokens):
  d_abs= {}
  for tok in tokens:
    d_abs.setdefault(tok, 0)
    d_abs[tok]+=1
  l = len(tokens)
  d_rel = {x:y/l for x, y in d_abs.items()}
  return d_abs, d_rel

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
def get_cosine(dic1, dic2):
  vec1, vec2 =  dic2vec(dic1, dic2, 0)
  return scipy.spatial.distance.cosine(vec1, vec2)

def lire_fichier (chemin):
    f = open(chemin , encoding = 'utf−8')
    chaine = f.read ()
    f.close ()
    return chaine

def stocker( chemin, contenu):
    w =open(chemin, "w")
    w.write(json.dumps(contenu , indent = 2))
    w.close()
    print(chemin)
def get_tokens(path):
#  text = normalize(slurp_file(path), False, False)
#  return re_WS.split(text)    
  return lire_fichier(path).split()
def get_new_scores(DET_file, GT_file):
  scores= {}
  tokens_GT = get_tokens(GT_file)
  tokens_DET = get_tokens(DET_file)
  GT_abs, GT_rel = get_voc(tokens_GT)
  DET_abs, DET_rel = get_voc(tokens_DET)
  scores["KL_res"] = {
                      "Cosine Dist.":get_cosine(GT_rel, DET_rel)}
  return scores

def get_distances(texte1, texte2, N=1, liste_name =["jaccard", "braycurtis","dice", "cosinus"] ):
    dico = {}
    for metric_name in liste_name :
        dico[metric_name] = []
        liste_resultat_dist2 = []
        for n_max in range(1, N+1):###range([min, default = 0], max, [step, default = 1]) 
            V = CountVectorizer(ngram_range=(1,n_max ), analyzer='word') 
            X = V.fit_transform([texte1, texte2]).toarray()
            if metric_name!= "cosinus" :  
                dist = DistanceMetric.get_metric(metric_name)     
                distance_tab1=dist.pairwise(X)
                liste_resultat_dist2.append(distance_tab1[0][1])
            else: 
                distance_tab1=sklearn.metrics.pairwise.cosine_distances(X) 
                liste_resultat_dist2.append(distance_tab1[0][1])
            dico[metric_name] = liste_resultat_dist2
    return dico

path1 = "../../../2022/These_Caroline/NER_Comparaison/DATA/ADAM/OCR/ADAM_TESSERACT-BIN/ADAM_Mon-village_Tesseract-BIN.txt"
path2 = "../../../2022/These_Caroline/NER_Comparaison/DATA/ADAM/REF/ADAM_Mon-village_PP.txt"

print(get_distances(lire_fichier(path1), lire_fichier(path2)))
print(get_new_scores(path1, path2))#lire_fichier(path1), lire_fichier(path2)))
