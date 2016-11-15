import nltk

keywords = {
    'detail', 'analysis', 'curious', 'learning', 'ask', 'risks',
    'team', 'development', 'preferred', 'skill', 'skills', 'research',
    'knowledge', 'technical', 'programming', 'computer', 'applications',
    'market', 'trading', 'software', 'engineering', 'idea', 'ideas',
    'financial', 'system', 'systems', 'value', 'creative', 'capability',
    'capabilities', 'requirements', 'diverse', 'services', 'statistics',
    'management', 'and/or', 'c++', 'java', 'python', 'c', 'matlab', 'r',
    'windows', 'linux', 'c#',
    'code', 'algorithms', 'e.g', 'entrepreneurial', 'server-side', 'user-interface',
    'user-interfaces', 'analyst', 'analysts', 'bachelor', 'masters', 'graduate', 'leadership',
    'solid', 'interpersonal', 'communication', 'fast-paced', 'optimize', 'optimized',
    'demonstrate', 'demonstrated', 'goals', 'good', 'quantitative', 'equity'
}

def num_keywords(sen):
    """ Returns a number

    Checks how many predefined keywords sen contains.
    """
    counter = 0
    for word in nltk.word_tokenize(sen):
        if (word.lower() in keywords):
            counter +=  1
    return counter

def contains_pattern_a(sen):
    """ Returns a bool

    Checks if sen contains predefined patterns:
        (RB)*(JJ|VBN)*(NN|NNS)(TO|IN)
        e.g. Strong ability to...
             Familiarity with...
             High proficiency in...
    """
    tagged = nltk.pos_tag(nltk.word_tokenize(sen))
    i = 0
    j = 0
    while (i < len(tagged)):
        stage = 0
        j = i
        for (_, t) in tagged[j:]:
            i = i + 1
            if (stage == 0):
                if (t == 'RB'):
                    continue
                elif (t == 'JJ' or t == 'VBN'):
                    stage = 1
                    continue
                elif (t == 'NN' or t == 'NNS'):
                    stage = 2
                    continue
                else:
                    break
            elif (stage == 1):
                if (t == 'JJ' or t == 'VBN'):
                    continue
                elif (t == 'NN' or t == 'NNS'):
                    stage = 2
                    continue
                else:
                    break
            elif (stage == 2):
                if (t == 'TO' or t == 'IN'):
                    return True
                else:
                    break
            else:
                break
    return False

def contains_pattern_b(sen):
    """ Returns a bool

    Checks if sen contains predefined patterns:
        (JJ)*(IN)(NNP)
        e.g. Proficient in C++
                Familiar with Office
    """
    tagged = nltk.pos_tag(nltk.word_tokenize(sen))
    i = 0
    j = 0
    while (i < len(tagged)):
        stage = 0
        j = i
        for (_, t) in tagged[j:]:
            i = i + 1
            if (stage == 0):
                if (t == 'JJ'):
                    continue
                elif (t == 'IN'):
                    stage = 1
                    continue
                else:
                    break
            elif (stage == 1):
                if (t == 'NNP' or t == 'NNPS'):
                    return True
                else:
                    break
            else:
                break
    return False


def sentence_features(sen):
    features = {}
    features["num_keywords"] = num_keywords(sen)
    features["has_pattern_a"] = contains_pattern_a(sen)
    features["has_pattern_b"] = contains_pattern_b(sen)

    return features