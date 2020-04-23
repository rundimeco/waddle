
This repository documents ongoing work on the evaluation of main text extraction from web pages.


### Installation


Most tools work on Python3 only
You need to have pip installed (https://pip.pypa.io/en/stable/installing/)

Run the following command to install all the packages :

pip install -r requirements.txt
(can take a while)

NB: If you are a windows user, take a look at this page : https://projects.raspberrypi.org/en/projects/using-pip-on-windows/2


### Evaluation

now you can run this command:
python test_all_tools.py


Directories:

* `Corpus/html`	 	raw html files
* `Corpus/cleaned`	cleaned file, one directory by tool
* `Corpus/reference`	reference cleaning version (needed for evaluation)


### Information

Web-Assembled Data-Driven Language-oriented Evaluation. [Just because](https://en.wikipedia.org/wiki/Chris_Waddle).

Authors: Gaël Lejeune & Adrien Barbaresi.

  Corpus/reference	reference cleaning version (needed for evaluation)

##TODO: Add instructions and a make for processing everything
