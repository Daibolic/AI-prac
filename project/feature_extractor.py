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

def contains_nnp(tagged):
    """ Returns a boolean
        Test if the sentence contains a proper noun
    """
    for (_ , t) in tagged:
        if (t == "NNP" or t == "NNPS"):
            return True

def num_keywords(tokens):
    """ Returns a number

    Checks how many predefined keywords sen contains.
    """
    counter = 0
    for word in tokens:
        if (word.lower() in keywords):
            counter +=  1
    return counter

def contains_pattern_a(tagged):
    """ Returns a bool

    Checks if sen contains predefined patterns:
        (RB)*(JJ|VBN)*(NN|NNS)(TO|IN)
        e.g. Strong ability to...
             Familiarity with...
             High proficiency in...
    """
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

def contains_pattern_b(tagged):
    """ Returns a bool

    Checks if sen contains predefined patterns:
        (JJ)*(IN)(NNP)
        e.g. Proficient in C++
                Familiar with Office
    """
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
    """ Given a sentence sen, generate a feature set for the sentence,
        for identifying if the sentence is useful or not
    """
    tokens = nltk.word_tokenize(sen)
    tagged = nltk.pos_tag(tokens)
    features = {}
    features["num_keywords"] = num_keywords(tokens)
    features["has_pattern_a"] = contains_pattern_a(tagged)
    features["has_pattern_b"] = contains_pattern_b(tagged)
    features["has_NNP"] = contains_nnp(tagged)

    return features

##################### For sentence categorization #############################

#Keywords that signal education requirement
educ_keyword = {
    'bachelor', 'masters', 'master', 'phd', 'doctorate', 'graduate', 'degree',
    'math', 'mathematics', 'statistics', 'systems'
}

#Keywords that identify requirements
iden_keyword = {
    'demonstrated', 'preferred', 'advantageous', 'required', 'familiar',
    'familiarity', 'requirements'
}

#other helpful keywords
other_keyword = {
    'quantitative', 'alpha', 'beta', 'financial', 'equities', 'portfolios',
    'portfolio', 'equity', 'research', 'skill', 'skills'
}

#Key phrases as tuples
key_phrase = {
    ('experience', 'with'), ('experience', 'of'), ('computer', 'science'),
    ('such', 'as'), ('risk', 'management')
}

def has_educ_keyword(tokens):
    """ Returns True if the tokens include a keyword for educational requirement
    """
    for w in tokens:
        if (w.lower() in educ_keyword):
            return True
    return False

def has_iden_keyword(tokens):
    """ Returns True if contains identifying keyword for requirement
    """
    for w in tokens:
        if (w.lower() in iden_keyword):
            return True
    return False

def num_other_keyword(tokens):
    """ Returns an int num, the number of other_keyword in tokens
    """
    num = 0
    for w in tokens:
        if (w.lower() in other_keyword):
            num += 1
    return num

def has_key_phrase(tokens):
    """ Returns True if contains key_phrase
    """
    l = len(tokens)
    for i in range(l):
        if (i+1 < l):
            t = tuple(map(lambda x: x.lower(), tokens[i:i+2]))
            if (t in key_phrase):
                return True
    return False


def cat_features(sen):
    """ Given a sentence sen, generate a feature set for the sentence,
        for identifying if the sentence is about skills or personal quailty
    """
    tokens = nltk.word_tokenize(sen)
    tagged = nltk.pos_tag(tokens)
    features = {}    
    features["has_NNP"] = contains_nnp(tagged)
    features["has_educ"] = has_educ_keyword(tokens)
    features["has_iden"] = has_iden_keyword(tokens)
    features["num_other"] = num_other_keyword(tokens)
    features["has_key_phrase"] = has_key_phrase(tokens)
    return features