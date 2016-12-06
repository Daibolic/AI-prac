from wordnik import *
from nltk.stem.snowball import EnglishStemmer
import enchant
from collections import defaultdict

depth = 2
synfile = "catsynonyms.txt"
stemfile = "catstem.txt"

#Wordnik api
apiUrl = 'http://api.wordnik.com/v4'
apiKey = '8c3a6e647d1e786a1110902e3af0beccf436103460eade92f'
client = swagger.ApiClient(apiKey,apiUrl)
wordApi = WordApi.WordApi(client)

#Pyenchant Api
d = enchant.Dict("en_US")

#stemmer
stemmer = EnglishStemmer()

#soft skills
categories = {"creativity":["creative","innovative","original","authentic","curious","unconventional","quirky"], 

"communication":["interpersonal","negotiation","influencing","presentation","verbal","written","listening","clients","human","personal","interpersonal"],

"collaboration":["teamwork","together","group","team","relationships"],

"responsibility":["credible","repsonsible","prepared","prioritize","confidentiality","consistent"],

"leadership":["visionary","strategic","leader","coach","lead"],

"entrepreneurial":["bold","risk","uncertainty"],

"diverse":["inclusive"],

"motivated":["driven","passionate"],

"detail":["meticulous","complexity"],

"agile":["fast","dynamic"],

"execute":["solve","develop","design","implement","deliver","build","plan","do"]}

synlist = defaultdict(set)
stemlist = defaultdict(set)

reltypes = {"hyponym","synonym","equivalent"}
expandtype = "etymologically-related-term"

#to synlist, add words 
def exp_synlist(word,cat,i):
    global synlist
    #dict for synonyms
    if d.check(word) and i<=depth:
        synlist[cat].add(word)
        related = wordApi.getRelatedWords(word)
        if related:
            for rel in related:
                if rel.relationshipType in reltypes:
                    synlist[cat] |= set([word if word not in categories and d.check(word) else "" for word in rel.words])

                if rel.relationshipType == expandtype:
                    for term in rel.words:
                        exp_synlist(term,cat,i+1)
            synlist[cat].discard("")
    f = open(synfile,"w")
    f.write(repr(dict(synlist)))
    f.close()
    exp_stemlist()


def exp_stemlist():
    #creating a dict for stems:
    global stemlist
    for key in synlist:
        stemlist[key] = {stemmer.stem(word) for word in synlist[key]}
    f = open(stemfile,"w")
    f.write(repr(dict(stemlist)))
    f.close()


def load_synlist(redo=False):
    """
    set redo to True if data must be downloaded 
    set to False if local data is to be used
    """
    global synlist,stemlist
    f = open(synfile)
    strs = f.read()
    f.close()
    if strs and not redo:
        synlist = defaultdict(set,eval(strs))
    else:
        init_synlist()

    g = open(stemfile)
    strs2 = g.read()
    g.close()
    if strs2 and not redo:
        stemlist = defaultdict(set,eval(strs2))
    else:
        exp_stemlist()

def init_synlist():
    for cat in categories:
        exp_synlist(cat,cat,0)
        for term in categories[cat]:
            exp_synlist(term,cat,0)

def match_stem(word):
    """If stem(word) matches stem(item) where item synlist[x], return x
    """
    lst = []
    wstem = stemmer.stem(word)
    for key in stemlist:
        if wstem in stemlist[key]:
            lst.append(key)
    return lst

def match_suggest(word):
    """
    If any w in d.suggest(stem(word)) in synlist[x],return x
    """
    lst = []
    for key in synlist:
        for w in d.suggest(stemmer.stem(word)):
            if w in synlist[key]:
                lst.append(key)
    return lst

def match_full(word):
    """
    if word in synlist[x], return x
    """
    lst = []
    for key in synlist:
        if word in synlist[key] or word==key:
            lst.append(key)
    return lst

def categorize(word):
    l1 = match_full(word)
    if l1:
        return l1

    l2 = match_suggest(word)
    if l2:
        return l2 

    l3 = match_stem(word)
    if l3:
        return l3

    return []


def count_major(wordlst):
    """
    Given a list of words, return the word with maximum frequency
    """
    matches = []
    count = defaultdict(int)
    for item in wordlst:
        count[item]+=1
    maxval = max(count.values())
    for key in count:
        if count[key]==maxval:
            matches.append(key)
    return matches

def categorize_related(word):
    """
    Given a word, categorize it by running categorize() on related words.
    """
    related = wordApi.getRelatedWords(word)
    if related:
        for rel in related:
            if rel.relationshipType=="equivalent":
                for relword in rel.words[0:min(2,len(rel.words))]:
                    if d.check(relword):
                        m = categorize(relword)
                        if m:
                            return m
    return []

def main_cat(word):
    if not d.check(word):
        return []

    match1 = categorize(word)
    if match1:
        return count_major(match1)

    match2 = categorize_related(word)
    if match2:
        return count_major(match2)

    return []


def printcat(word):
    print word ," is categorized to ", main_cat(word)

def get_category(word):
    return main_cat(word)



#Test list#
lst = ["original","unconventional","together","uncertainty","risks","innovate","diversity","inclusive","creative","bold","brilliant","detail-oriented","negotiation","management","dynamic","negotiating","influencing","innovating","problem-solving","team","entrepreneurial","interpersonal","fast-paced","collaborative","prepared","authentic","listener","prioritize","committed","deliver","curious","unconventionally"]

load_synlist()
