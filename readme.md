
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

We defined three categories: (I) tools designed to extract all the textual content (recall-oriented tools), usually not focused on press articles; (II) tools focusing on the readability of web pages and (III) tools dedicated to text content extraction.

| Cat. | Tool                                      | Version   | Github               | Reference |
|:-----|:-------------------------------------------|:----------|:-----------------------------|:----------|
| I    | <span class="smallcaps">Html2text</span>   | 2020.1.16 | [Alir3z4/html2text/][]       |[https://core.ac.uk/download/pdf/127601559.pdf]           |
| I    | <span class="smallcaps">Inscriptis</span>  | 1.0       | [weblyzard/inscriptis][]     |           |
| II   | <span class="smallcaps">Newspaper3k</span> | 0.2.8     | [codelucas/newspaper][]      |           |
| II   | <span class="smallcaps">News-please</span> | 1.4.25    | [fhamborg/news-please][]     |           |
| II   | <span class="smallcaps">Readability</span> | 0.7.1     | [buriy/python-readability][] |           |
| III  | <span class="smallcaps">Boilerpy3</span>   | 1.0.2     | [jmriebold/BoilerPy3][]      |[https://www.l3s.de/~kohlschuetter/publications/wsdm187-kohlschuetter.pdf]           |
| III  | <span class="smallcaps">Dragnet</span>     | 2.0.4     | [dragnet-org/dragnet][]      | [http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.402.4694&rep=rep1&type=pdf]          |
| III  | <span class="smallcaps">Goose3</span>      | 3.1.6     | [goose3/goose3][]            |           |
| III  | <span class="smallcaps">JusText</span>     | 2.2.0     | [miso-belica/jusText][]      |[https://is.muni.cz/th/45523/fi_d/phdthesis.pdf]           |
| III  | <span class="smallcaps">Trafilatura</span> | 0.4.1     | [adbar/trafilatura][]        |[https://hal.archives-ouvertes.fr/hal-02447264/document]           |

  [Alir3z4/html2text/]: https://github.com/Alir3z4/html2text/
  [weblyzard/inscriptis]: https://github.com/weblyzard/inscriptis
  [codelucas/newspaper]: https://github.com/codelucas/newspaper
  [fhamborg/news-please]: https://github.com/fhamborg/news-please
  [buriy/python-readability]: https://github.com/buriy/python-readability
  [jmriebold/BoilerPy3]: https://github.com/jmriebold/BoilerPy3
  [dragnet-org/dragnet]: https://github.com/dragnet-org/dragnet
  [goose3/goose3]: https://github.com/goose3/goose3
  [miso-belica/jusText]: https://github.com/miso-belica/jusText
  [adbar/trafilatura]: https://github.com/adbar/trafilatura


### Information

Web-Assembled Data-Driven Language-oriented Evaluation. [Just because](https://en.wikipedia.org/wiki/Chris_Waddle).

Authors: Gaël Lejeune & Adrien Barbaresi.

  Corpus/reference	reference cleaning version (needed for evaluation)

##TODO: Add instructions and a make for processing everything

Node js issues (readabilipy) see : https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-18-04-fr

Encoding errors :
utf-8 should be the norm but in fact is not
 Some issues and possible solutions :
 (Non-ISO extended-ASCII text) : https://superuser.com/questions/669700/non-iso-extended-ascii-text


 Windows OS issues:

 - cchardet : https://github.com/PyYoshi/cChardet/issues/61
