from generic_functions import *

#### tools import ####
from boilerpy3 import extractors
#from dragnet import extract_content
from goose3 import Goose
import html2text
import html_text
import inscriptis 
import justext
from newspaper import fulltext
from newsplease import NewsPlease
from readabilipy import simple_json_from_html_string
from readability import Document
from trafilatura import extract
from trafilatura.core import baseline
from lxml import etree, html


def apply_tool(tool, str_text, mode):
  if tool == "BP3":
    list_paragraphs = get_paragraphs_BP3(str_text, mode)
  elif tool == "DRAG":
    text_det = extract_content(str_text)
    list_paragraphs = re.split("\n", text_det)
  elif tool=="GOO":
    list_paragraphs = get_paragraphs_GOO(str_text, mode)
  elif tool=="HTML2TEXT":
    text_det = html2text.html2text(str_text)
    list_paragraphs = re.split("\n\n", text_det)
  elif tool=="INSCRIPTIS":
    text_det = inscriptis.get_text(str_text)
    list_paragraphs = re.split("\n", text_det)
  elif tool=="JT":
    list_paragraphs = get_paragraphs_JT(str_text, mode)
  elif tool == "NEWSPAPER":
    try:
      text_det = fulltext(str_text)
    except:
      text_det =""
    list_paragraphs = re.split("\n\n", text_det)
  elif tool == "NEWSPLEASE":
    list_paragraphs = get_paragraphs_newsplease(str_text, mode)
  elif tool == "READABILITY":
    try:
      text_det = Document(str_text).summary(html_partial = True)
    except:
      text_det = ""
    list_paragraphs = re.split("\n", text_det)#TODO: clean this output ?
  ##TODO: raise error
  elif tool == "TRAF":
    list_paragraphs = get_paragraphs_traf(str_text, mode)
  elif tool == "TRAF_BL":
    list_paragraphs = get_paragraphs_traf_baseline(str_text, mode)
  elif tool == "READ_py":
    try:
      list_paragraphs = get_paragraphs_readabilipy(str_text, mode)
    except:
      print("Error readabilipy")
      list_paragraphs = [""]
  elif tool == "HTML-text":
    list_paragraphs = get_paragraphs_html_text(str_text, mode)
  return list_paragraphs


def get_paragraphs_BP3(str_text, mode):
  """
  using Boilerpy3
  """
  if mode =="":
    BP_extractor = extractors.DefaultExtractor()    
  elif mode =="Article":
    BP_extractor = extractors.ArticleExtractor()    
  elif mode =="Largest":
    BP_extractor = extractors.LargestContentExtractor()
  else:
    BP_extractor = extractors.KeepEverythingExtractor()
  from contextlib import redirect_stderr
  with open(os.devnull, 'w') as devnull:
    with redirect_stderr(devnull):
      try: 
        text_det = BP_extractor.get_content(str_text)
      except:
        text_det = ""
  return re.split("\n",text_det)


def get_paragraphs_GOO(str_text, mode):
  """
  using Goose
  """
  g = Goose()
  article = g.extract(raw_html=str_text)
  list_paragraphs = re.split("\n\n",article.cleaned_text)
  g.close()
  return list_paragraphs


def get_all_stop_words():
  """
  For the language independent version of Justext
  """
  stop_words = set()
  for language in justext.get_stoplists():
      stop_words.update(justext.get_stoplist(language))
  return stop_words


def get_paragraphs_JT(str_text,  mode):
  """
  using Justext
  """
  if mode=="_english":
    stop = justext.get_stoplist("English")
  else:
    lang = get_langid(str_text)
    if lang=="Chinese":
      stop = set()
    else:
      stop = justext.get_stoplist(lang)
  if len(stop)==0:
    any_lang_stop_words = get_all_stop_words()
    paragraphs = justext.justext(str_text, any_lang_stop_words)
  else:
    paragraphs = justext.justext(str_text, stop)
  list_paragraphs = [x.text for x in paragraphs if not x.is_boilerplate]
  return list_paragraphs


def get_paragraphs_newsplease(str_text, mode):
  """
  using Newsplease
  """
  try:
    text_det = NewsPlease.from_html(str_text.encode(), url=None).maintext
    if text_det is None:
      list_paragraphs = [""]
    else:
      list_paragraphs = re.split("\n", text_det)
  except:
    list_paragraphs = [""]
  return list_paragraphs


def get_paragraphs_traf(str_text, mode):
  """
  using Trafilatura
  """
  no_fb, comm = True, False
  if "Fallback" in mode:
    no_fb = False
  if "Comments" in mode:
    comm = True
#  try:
  s = extract(str_text, no_fallback=no_fb, include_comments=comm)
  #except:
   # s = None
  if s is None:
    list_paragraphs = [""]
  else:
    list_paragraphs = re.split("\n", s)
  return list_paragraphs


def get_paragraphs_traf_baseline(str_text, mode):
  """
  using Trafilatura baseline
  """
  _, result, _ = baseline(str_text)
  return re.split("\n", result)


def get_paragraphs_readabilipy(str_text, mode):
  """
  using ReadabiliPy, requires NodeJS version >= 10
  """
  try:
      article = simple_json_from_html_string(str_text, use_readability=True)
  except (TypeError, ValueError):
      return ['']
  returnlist = []
  for textelem in article['plain_text']:
      returnlist.append(textelem['text'])
  return returnlist


def get_paragraphs_html_text(str_text, mode):
  """
  using html_text
  """
  try:
      text = html_text.extract_text(str_text, guess_layout=False)
  except TypeError:
      return ['']
  return re.split("\n", text)
