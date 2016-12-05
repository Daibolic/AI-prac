def split_tag(tagged):
    words = []
    tags = []
    for (w, t) in tagged:
        words.append(w)
        tags.append(t)
    return (words, tags)


def extract_skill_phrase(tagged, skills):
    """ Given a tagged skills sentence and a dictionary that maps
        phrase to its category, updates the dicionary
    """
    nouns = {'NNS', 'NN'}
    adjs = {'JJ', 'JJR', 'JJS'}
    (words, tags) = split_tag(tagged)
    length = len(words)
    head = 0
    probe = 0

    while (head < length):
        if (tags[head] == 'IN' or tags[head] == 'CC' or tags[head] == ','):
            probe += 1
            while (probe < length and (tags[probe] in nouns)):
                probe += 1
            if (probe - head != 1):
                key = " ".join(words[head + 1: probe])
                skills[key] = "NP"              
            head = probe
        elif (tags[head] == 'NNP' or tags[head] == 'NNPS'):
            key = words[head]
            skills[key] = 'NNP'
            head += 1
            probe = head
        elif (tags[head] == 'VBG'):
            probe += 1
            flag = 0
            while (probe < length):
                if (tags[probe] in adjs and not flag):
                    probe += 1
                elif (tags[probe] in nouns and not flag):
                    flag = 1
                    probe += 1
                elif (tags[probe] in nouns and flag):
                    probe += 1
                else:
                    break
            if (probe - head != 1):
                key = " ".join(words[head:probe])
                skills[key] = 'VP'
            head = probe
        elif (tags[head] in adjs):
            probe += 1
            flag = 0
            while (probe < length):
                if (tags[probe] in adjs and not flag):
                    probe += 1
                elif (tags[probe] in nouns and not flag):
                    flag = 1
                    probe += 1
                elif (tags[probe] in nouns and flag):
                    probe += 1
                else:
                    break
            if (probe - head != 1):
                key = " ".join(words[head:probe])
                skills[key] = 'NP'
            head = probe
        else:
            head += 1
            probe = head

def extract_adjectives(tagged, adjs):
    for (w, t) in tagged:
        if (t == 'JJ'):
            adjs[w] = t
