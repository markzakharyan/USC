#!/usr/bin/env python3.7
import re
import subprocess
import sys
from collections import defaultdict
# import logging


# logger = logging.getLogger(__name__)

MIN_ARTICLES = 1	# number of articles where words need to appear
line_trans = str.maketrans('–’', "-\'")
words_split_re = re.compile(r'[^\w\-\']')
# capture compound words (such as "non-profit") and single letter words (such as "a")
is_word_re = re.compile(r'(^\w.*\w$)|(^\w$)')
not_is_word_re = re.compile(r'.*\d.*')

#USC physics & astronomy faculty from https://dornsife.usc.edu/cf/phys/phys_faculty_roster.cfm
phrases = ['itzhak bars', 'gene bickers', 'james boedicker', 'peter chung', 'rosa di felice', 'moh el-naggar', 'jack feinberg', 'peter foster', 'vera gluscevic', 'christopher gould', 'stephan haas', 'christoph haselwandter', 'clifford johnson', 'rajiv kalia', 'vitaly kresin', 'eli levenson-falk', 'grace lu', 'yunqiu kelly luo', 'amber miller', 'dennis nemeschansky', 'kris pardo', 'elena pierpaoli', 'krzysztof pilch', 'edward rhodes', 'hubert saleur', 'robin shakeshaft', 'nicholas warner', 'paolo zanardi', 'todd brun', 'stephen cronin', 'paul dapkus', 'martin gundersen', 'mercedeh khajavikhan', 'joseph kunc', 'aaron lauda', 'anthony levi', 'daniel lidar', 'anupam madhukar', 'aiichiro nakano', 'fabien pinaud', 'michelle povinelli', 'oleg prezhdo', 'remo rohs', 'susumu takahashi', 'armand tanguay', 'priya vashishta', 'andrey vilesov', 'alan willner', 'geraldine peters', 'satish thittamaranahalli ka', 'tameem albash', 'lorenzo campos venuti', 'hamid chabok', 'itay hen', 'scott macdonald', 'lara martini', 'nicolas moure', 'andrew newman', 'vahe peroomian', 'kenneth phillips', 'anthony piro', 'nan yu', 'gerd bergmann', 'hans bozler', 'tu-nan chang', 'werner dã¤ppen', 'melvin daybell', 'leonid didkovsky', 'richard thompson', 'william wagner', 'robert wu']

if not len(sys.argv) > 1:
	sys.stderr.write("Usage: %s dumps/*.bz2\n" % sys.argv[0])
	sys.exit(1)


# collect data

word_uses = defaultdict(int)
word_docs = {}

doc_no = 0
currArticle = -1
for fn in sys.argv[1:]:
	sys.stderr.write("Processing %s\n" % fn)
	with subprocess.Popen(
		"wikiextractor --no-templates -o - %s" % fn,
		stdout=subprocess.PIPE,
		shell=True
	) as proc:
		while True:
			line = proc.stdout.readline()
			if not line:
				break
			if line.startswith(b'<'):
				doc_no += 1
				if not line.startswith(b'</'):
					currArticle = int(line.decode('utf-8').split("id=\"")[1].split("\"")[0])
				continue
			line = line.decode('utf-8')
			line = line.translate(line_trans)
			line = line.lower()
			for phrase in phrases:
				count = line.count(f" {phrase} ")
				if count <= 0:
					continue
				word_uses[phrase] += count
				if not phrase in word_docs:
					word_docs[phrase] = {currArticle} #{doc_no}
				else:
					word_docs[phrase].add(currArticle) #doc_no)
				# logger.info("%s %d %s" % (phrase, word_uses[phrase], str(word_docs[phrase])))

# save raw data

words = list(word_uses.keys())
words.sort(key=lambda w: word_uses[w], reverse=True)
for word in words:
	print("%s %d %s" % (word, word_uses[word], str(word_docs[word])))
