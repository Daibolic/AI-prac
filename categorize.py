from wordnik import *
from nltk.stem.snowball import EnglishStemmer
import enchant
from collections import defaultdict

depth = 2

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

"communication":["interpersonal","negotiation","influencing","presentation","verbal","written","listening","clients"],

"collaboration":["teamwork","together","group","team","relationships"],

"responsibility":["credible","repsonsible","prepared","prioritize","confidentiality"],

"leadership":["visionary","strategic","leader","coach","lead"],

"entrepreneurial":["bold","risk","uncertainty"],

"diverse":["inclusive"],

"motivated":["driven","passionate"],

"detail":["meticulous","complexity"],

"agile":["fast","dynamic"],

"execute":["solve","develop","design","implement","deliver","build","plan","do"]}

synlist = defaultdict(set)

reltypes = {"hyponym","synonym","equivalent"}
expandtype = "etymologically-related-term"

#to synlist, add words 
def expSynlist(word,cat,i):
    if d.check(word) and i<=2:
        synlist[cat].add(word)
        related = wordApi.getRelatedWords(word)
        if related:
            for rel in related:
                if rel.relationshipType in reltypes:
                    synlist[cat] |= set([word if word not in categories and d.check(word) else "" for word in rel.words])

                if rel.relationshipType == expandtype:
                    for term in rel.words:
                        expSynlist(term,cat,i+1)
            synlist[cat].discard("")


#initialize soft skills dict
for cat in categories:
    expSynlist(cat,cat,0)
    for term in categories[cat]:
        expSynlist(term,cat,0)


def categorize1(word):
    """If stem(word) matches stem(item) where item synlist[x], return x
    """
    lst = []
    wstem = stemmer.stem(word)
    for key in synlist:
        for syn in synlist[key]:
            if stemmer.stem(syn)==wstem:
                lst.append(key)
    return lst

def categorize2(word):
    """
    If any w in d.suggest(stem(word)) in synlist[x],return x
    """
    lst = []
    for key in synlist:
        for w in d.suggest(stemmer.stem(word)):
            if w in synlist[key]:
                lst.append(key)
    return lst

def categorize3(word):
    """
    if word in synlist[x], return x
    """
    lst = []
    for key in synlist:
        if word in synlist[key] or word==key:
            lst.append(key)
    return lst

def categorize(word):
    """run categorize1,2,3 on dictionary words.
    """
    if not d.check(word):
        return []

    l1 = categorize1(word)
    l2 = categorize2(word)
    l3 = categorize3(word)
    return l1+l2+l3

    count = defaultdict(int)
    for item in l1+l2+l3:
        count[item]+=1
    maxval = 0 
    match = None
    for key in count:
        if count[key]>maxval:
            maxval = count[key]
            match = key 
    return match

def categorize_related(word):
    """
    Given a word, categorize it by running categorize() on related words.
    """
    if not d.check(word):
        return []

    lst = []
    related = wordApi.getRelatedWords(word)
    if related:
        for rel in related:
            if rel.relationshipType in reltypes :
                for relword in rel.words+["same-context"]:
                    #print "item in related words: ", relword
                    m = categorize(relword)
                    if m:
                        lst += m
    return lst

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

def main_cat(word,i):
    """
    Runs full scheme of categorization functions for depth = 2. 
    i keeps track of current depth (initial expected = 0) 
    """
    match1 = categorize(word)
    if match1:
        return count_major(match1)

    match3 = []
    if i==0:
        stemlst = d.suggest(stemmer.stem(word))
        for item in stemlst:
            m2 = main_cat(item,i+1)
            match3 += m2
    if match3:
        return count_major(match3)

    match2 = categorize_related(word)
    if match2:
        return count_major(match2)

    return []


def printcat(word):
    print word ," is categorized to ", main_cat(word,0)

#Test list#
lst = ["original","unconventional","together","uncertainty","risks","innovate","diversity","inclusive","creative","bold","brilliant","detail-oriented","negotiation","management","dynamic","negotiating","influencing","innovating","problem-solving","team","entrepreneurial","interpersonal","fast-paced","collaborative","prepared","authentic","listener","prioritize","committed","deliver","curious","unconventionally"]

#for l in lst:
#    printcat(l)