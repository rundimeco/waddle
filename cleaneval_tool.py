#!/usr/bin/env python2.5
# encoding: utf-8
"""
cleaneval.py v1.0
Simple and fast evaluation of CleanEval-1 tasks (precision, recall, F-score).
"""

import sys
import os
import string
import re
from math import *
from difflib import SequenceMatcher
from getopt import getopt, GetoptError

help_message = '''
This is cleaneval.py version 1.0 -- Copyright (C) 2008 by Stefan Evert
Usage:  cleaneval.py [options] <texts_dir> <gold_dir> [<align_dir>]
Options:
  -t    print total precision/recall for all files (micro-averaged)
        (does not print results for individual files)
  -n    omit table header (e.g. to combine multiple tables)
  -s    calculate summary statistics (mean / s.d.) and print on STDERR
  -a    remove non-ASCII characters before comparison
  -u    calculate unlabelled segmentation accuracy
Evaluates automatically cleaned files in directory <texts_dir> against
gold standard files in directory <gold_dir>.  Correspoding files in the 
two directories must have identical names and there must be no other files
in these directories.
The script prints a TAB-delimited evaluation table on standard output, which
can be redirected to a file and read into R, Excel or a similar application.
Precision, recall and F-score are calculated as percentages of whitespace-
delimited words.  Accuracy of segment identification is measured by precision,
recall and F-score for labelled or unlabelled segment marker tags (if the
option -u is specified, no distinction is made between types <p>, <h> and <l>).
If the third argument is given, full alignments will be written to separate
files in directory <align_dir>.
'''

def slurp_file(filename):
	fh = open(filename)
	body = fh.read()
	fh.close()
	return body

re_URL = re.compile("^\s*URL.*$", re.MULTILINE)
re_TAG = re.compile("(<[phl]>)", re.IGNORECASE)
re_WS = re.compile("\s+")
re_CTRL = re.compile("[\x00-\x1F]+")
re_HI = re.compile("[\x80-\xFF]+")

def normalize(text, ascii=False, unlabelled=False):
	text = re_URL.sub("", text)           # remove URL line at start of gold standard files
	text = re_CTRL.sub(" ", text)         # replace any control characters by spaces (includes newlines)

	if unlabelled:
		text = re_TAG.sub("\n<p> ", text) # start each segment on new line, normalise tags
	else:
		text = re_TAG.sub("\n\g<1> ", text)  # only break lines before segment markers

	text = re_WS.sub(" ", text)           # normalise whitespace (including line breaks) to single spaces
	if ascii:
		text = re_HI.sub("", text)        # delete non-ASCII characters (to avoid charset problems)

	return text

## return diff as list of tuples ("equal"/"insert"/"delete", [text words], [gold words])
def make_diff(alignment, text_w, gold_w):
	diff = []
	for tag, i1, i2, j1, j2 in alignment.get_opcodes():
		text_region = text_w[i1:i2]
		gold_region = gold_w[j1:j2]
		if tag == "replace":
			diff.append( ("delete", text_region, []) )
			diff.append( ("insert", [], gold_region) )
		else:
			diff.append( (tag, text_region, gold_region) )
	return diff

## return evaluation measures for given diff:
##   (f-score, precision, recall, [labelled] segmentation f-score, precision, recall)
def evaluate(diff):
	tp = fp = fn = 0
	tag_tp = tag_fp = tag_fn = 0
	for tag, text, gold in diff:
		text_tags = 0
		for i in filter(re_TAG.match, text):text_tags+=1
#		text_tags = len( filter(re_TAG.match, text) )
		gold_tags = 0
		for i in filter(re_TAG.match, gold):gold_tags+=1
#		gold_tags = len( filter(re_TAG.match, gold) )
		text_l = len(text)
		gold_l = len(gold)
		if tag == "delete":
			fp += text_l
			tag_fp += text_tags
		elif tag == "insert":
			fn += gold_l
			tag_fn += gold_tags
		else:
			tp += text_l
			tag_tp += text_tags
			assert text_l == gold_l
			assert text_tags == gold_tags

	n_text = tp + fp if tp + fp > 0 else 1
	n_gold = tp + fn if tp + fn > 0 else 1
	precision = float(tp) / n_text
	recall = float(tp) / n_gold
	precision_plus_recall = precision + recall if precision + recall > 0 else 1
	f_score = 2 * precision * recall / precision_plus_recall

	tags_text = tag_tp + tag_fp if tag_tp + tag_fp > 0 else 1
	tags_gold = tag_tp + tag_fn if tag_tp + tag_fn > 0 else 1
	tag_precision = float(tag_tp) / tags_text
	tag_recall = float(tag_tp) / tags_gold
	precision_plus_recall = tag_precision + tag_recall if tag_precision + tag_recall > 0 else 1
	tag_f_score = 2 * tag_precision * tag_recall / precision_plus_recall

	out = {	"f-score":100 * f_score, "precision":100 * precision, "recall":100 * recall, 
		"tag_f_score":100 * tag_f_score, "tag_precision":100 * tag_precision, "tag_recall":100 * tag_recall, 
		"tp":tp, "fp":fp, "fn":fn, 
		"tag_tp":tag_tp, "tag_fp":tag_fp, "tag_fn":tag_fn}
	return out

def write_alignment(diff, filename):
	fh = file(filename, "w")
	for tag, text_seg, gold_seg in diff:
		if tag == "delete":
			print >> fh, "<" * 40, "(false positive)"
			print >> fh, " ".join(text_seg)
		if tag == "insert":
			print >> fh, ">" * 40, "(false negative)"
			print >> fh, " ".join(gold_seg)
		if tag == "equal":
			print >> fh, "=" * 40
			print >> fh, " ".join(gold_seg)
	fh.close()


#opt_total = ('-t', '') in options
#opt_noheader = ('-n', '') in options
#opt_summary = ('-s', '') in options
#opt_unlabelled = ('-u', '') in options
#opt_ascii = ('-a', '') in options

def evaluate_tokenList(text_words, gold_words):
  
  alignment = SequenceMatcher(None, text_words, gold_words)
  diff = (alignment, text_words, gold_words)
  eval_list = evaluate(diff)
  return eval_list



def evaluate_file(text_file, gold_file):
  import langid
  filename = text_file
  opt_ascii = False
  opt_unlabelled = False
  opt_noheader = True
  opt_total = False
  opt_summary = False
  sum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ss = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  text = normalize(slurp_file(text_file), opt_ascii, opt_unlabelled)
  gold = normalize(slurp_file(gold_file), opt_ascii, opt_unlabelled)
  lang = langid.classify(gold)
  text_words = re_WS.split(text)
  gold_words = re_WS.split(gold)
  if lang[0]=="zh":#TODO: correct for tags
    text_words = [x for x in text] 
    gold_words = [x for x in gold]
  alignment = SequenceMatcher(None, text_words, gold_words)
  diff = make_diff(alignment, text_words, gold_words)
  eval_list = evaluate(diff)
  return eval_list

if __name__=="__main__":
  print("toto")
  import sys
  print(evaluate_file(sys.argv[1], sys.argv[2]))
