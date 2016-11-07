import nltk


def contains_keyword(sen):
    """ Returns a bool

    Checks if sen contains predefined keywords.
    """
    #TODO
    return False

def contains_pattern_a(sen):
    """ Returns a bool

    Checks if sen contains predefined patterns:
        (RB)*(JJ|VBN)*(NN|NNS)(TO|IN)
        e.g. Strong ability to...
             Familiarity with...
             High proficiency in...
    """
    #TODO
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
