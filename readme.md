
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



### Tools

|Cat.   |Outil          | Version|Adresse Github& Référence|
|I |\textsc{Html2text} | 2020.1.16 |\href{https://github.com/Alir3z4/html2text/}{Alir3z4/html2text/}    ||
|I      &\textsc{Inscriptis} | 1.0      |\href{https://github.com/weblyzard/inscriptis}{weblyzard/inscriptis}           ||
|II |\textsc{Newspaper3k} |0.2.8        |\href{https://github.com/codelucas/newspaper}{codelucas/newspaper}             ||
|II|\textsc{News-please} |1.4.25 |\href{https://github.com/fhamborg/news-please}{fhamborg/news-please}  | \cite{HamborgEtAl:2017}|
|II|\textsc{Readability} |0.7.1         |\href{https://github.com/buriy/python-readability}{buriy/python-readability}||
|III|\textsc{Boilerpy3} |1.0.2  |\href{https://github.com/jmriebold/BoilerPy3}{jmriebold/BoilerPy3}             |\cite{KohlschutterEtAl:2010}|
|III|\textsc{Dragnet} |2.0.4    |\href{https://github.com/dragnet-org/dragnet}{dragnet-org/dragnet}     | \cite{PetersEtAl:2013}|
|III|\textsc{Goose3} |3.1.6     |\href{https://github.com/goose3/goose3}{goose3/goose3}                 ||
|III|\textsc{JusText} |2.2.0    |\href{https://github.com/miso-belica/jusText}{miso-belica/jusText}             | \cite{Pomikalek:2011}|
|III |\textsc{Trafilatura} |0.4.1       |\href{https://github.com/adbar/trafilatura}{adbar/trafilatura}         | \cite{Barbaresi:2019b}|

|Cat. |Outil |Version|Github|Reference|

  ------ --------------------------- ----------- ------------------------------------------------------------------------- --------------------------
|I      |[Html2text]{.smallcaps}     2020.1.16   [Alir3z4/html2text/](https://github.com/Alir3z4/html2text/)               
  |I      |[Inscriptis]{.smallcaps}    1.0         [weblyzard/inscriptis](https://github.com/weblyzard/inscriptis)           
  |II     |[Newspaper3k]{.smallcaps}   0.2.8       [codelucas/newspaper](https://github.com/codelucas/newspaper)             
  |II     |[News-please]{.smallcaps}   1.4.25      [fhamborg/news-please](https://github.com/fhamborg/news-please)           [@HamborgEtAl:2017]
  |II     |[Readability]{.smallcaps}   0.7.1       [buriy/python-readability](https://github.com/buriy/python-readability)   
  |III    |[Boilerpy3]{.smallcaps}     1.0.2       [jmriebold/BoilerPy3](https://github.com/jmriebold/BoilerPy3)             [@KohlschutterEtAl:2010]
  |III    |[Dragnet]{.smallcaps}       2.0.4       [dragnet-org/dragnet](https://github.com/dragnet-org/dragnet)             [@PetersEtAl:2013]
  |III    |[Goose3]{.smallcaps}        3.1.6       [goose3/goose3](https://github.com/goose3/goose3)                         
  |III    |[JusText]{.smallcaps}       2.2.0       [miso-belica/jusText](https://github.com/miso-belica/jusText)             [@Pomikalek:2011]
  |III    |[Trafilatura]{.smallcaps}   0.4.1       [adbar/trafilatura](https://github.com/adbar/trafilatura)                 [@Barbaresi:2019b]


### Information

Web-Assembled Data-Driven Language-oriented Evaluation. [Just because](https://en.wikipedia.org/wiki/Chris_Waddle).

Authors: Gaël Lejeune & Adrien Barbaresi.

  Corpus/reference	reference cleaning version (needed for evaluation)

##TODO: Add instructions and a make for processing everything
